import warnings

warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

# GENERAL IMPORTS
import os
import argparse
import numpy as np
from pathlib import Path
import shutil
import json
import time
from pprint import pprint
from datetime import datetime, timedelta

# SPIKEINTERFACE
import spikeinterface as si
import spikeinterface.extractors as se
import spikeinterface.sorters as ss
import spikeinterface.curation as sc

# AIND
from aind_data_schema.core.processing import DataProcess

# LOCAL
URL = "https://github.com/AllenNeuralDynamics/aind-capsule-ephys-spikesort-kilosort25"
VERSION = "0.1.0"

SORTER_NAME = "kilosort2_5"

data_folder = Path("../data")
results_folder = Path("../results")
scratch_folder = Path("../scratch")

# Define argument parser
parser = argparse.ArgumentParser(description="Spike sort ecephys data with Kilosort2.5")

n_jobs_group = parser.add_mutually_exclusive_group()
n_jobs_help = "Duration of clipped recording in debug mode. Default is 30 seconds. Only used if debug is enabled"
n_jobs_help = (
    "Number of jobs to use for parallel processing. Default is -1 (all available cores). "
    "It can also be a float between 0 and 1 to use a fraction of available cores"
)
n_jobs_group.add_argument("static_n_jobs", nargs="?", default="-1", help=n_jobs_help)
n_jobs_group.add_argument("--n-jobs", default="-1", help=n_jobs_help)

params_group = parser.add_mutually_exclusive_group()
params_file_help = "Optional json file with parameters"
params_group.add_argument("static_params_file", nargs="?", default=None, help=params_file_help)
params_group.add_argument("--params-file", default=None, help=params_file_help)
params_group.add_argument("--params-str", default=None, help="Optional json string with parameters")

if __name__ == "__main__":
    args = parser.parse_args()

    N_JOBS = args.static_n_jobs or args.n_jobs
    N_JOBS = int(N_JOBS) if not N_JOBS.startswith("0.") else float(N_JOBS)
    PARAMS_FILE = args.static_params_file or args.params_file
    PARAMS_STR = args.params_str

    # Use CO_CPUS env variable if available
    N_JOBS_CO = os.getenv("CO_CPUS")
    N_JOBS = int(N_JOBS_CO) if N_JOBS_CO is not None else N_JOBS

    if PARAMS_FILE is not None:
        print(f"\nUsing custom parameter file: {PARAMS_FILE}")
        with open(PARAMS_FILE, "r") as f:
            processing_params = json.load(f)
    elif PARAMS_STR is not None:
        processing_params = json.loads(PARAMS_STR)
    else:
        with open("params.json", "r") as f:
            processing_params = json.load(f)

    data_process_prefix = "data_process_spikesorting"

    job_kwargs = processing_params["job_kwargs"]
    job_kwargs["n_jobs"] = N_JOBS
    si.set_global_job_kwargs(**job_kwargs)

    sorter_params = processing_params["sorter"]

    ####### SPIKESORTING ########
    print("\n\nSPIKE SORTING")
    sorting_params = None

    si.set_global_job_kwargs(**job_kwargs)
    t_sorting_start_all = time.perf_counter()

    # check if test
    if (data_folder / "preprocessing_pipeline_output_test").is_dir():
        print("\n*******************\n**** TEST MODE ****\n*******************\n")
        preprocessed_folder = data_folder / "preprocessing_pipeline_output_test"
    else:
        preprocessed_folder = data_folder

    # try results here
    spikesorted_raw_output_folder = scratch_folder / "spikesorted_raw"
    spikesorting_data_processes = []

    preprocessed_folders = [p for p in preprocessed_folder.iterdir() if p.is_dir() and "preprocessed_" in p.name]
    for recording_folder in preprocessed_folders:
        datetime_start_sorting = datetime.now()
        t_sorting_start = time.perf_counter()
        spikesorting_notes = ""

        recording_name = ("_").join(recording_folder.name.split("_")[1:])
        sorting_output_folder = results_folder / f"spikesorted_{recording_name}"
        sorting_output_process_json = results_folder / f"{data_process_prefix}_{recording_name}.json"

        print(f"Sorting recording: {recording_name}")
        recording = si.load_extractor(recording_folder)
        print(recording)

        # we need to concatenate segments for KS
        if recording.get_num_segments() > 1:
            recording = si.concatenate_recordings([recording])

        # run ks2.5
        try:
            sorting = ss.run_sorter(
                SORTER_NAME,
                recording,
                output_folder=spikesorted_raw_output_folder / recording_name,
                verbose=False,
                delete_output_folder=True,
                **sorter_params,
            )
            print(f"\tRaw sorting output: {sorting}")
            n_original_units = int(len(sorting.unit_ids))
            spikesorting_notes += f"\n- KS2.5 found {n_original_units} units, "
            if sorting_params is None:
                sorting_params = sorting.sorting_info["params"]

            # remove empty units
            sorting = sorting.remove_empty_units()
            # remove spikes beyond num_Samples (if any)
            sorting = sc.remove_excess_spikes(sorting=sorting, recording=recording)
            n_non_empty_units = int(len(sorting.unit_ids))
            n_empty_units = n_original_units - n_non_empty_units
            # save params in output
            sorting_outputs = dict(empty_units=n_empty_units)
            print(f"\tSorting output without empty units: {sorting}")
            spikesorting_notes += f"{len(sorting.unit_ids)} after removing empty templates.\n"

            # split back to get original segments
            if recording.get_num_segments() > 1:
                sorting = si.split_sorting(sorting, recording)

            # save results
            print(f"\tSaving results to {sorting_output_folder}")
            sorting = sorting.save(folder=sorting_output_folder)
            shutil.copy(
                spikesorted_raw_output_folder / recording_name / "spikeinterface_log.json", sorting_output_folder
            )
        except Exception as e:
            # save log to results
            (sorting_output_folder).mkdir(parents=True, exist_ok=True)
            shutil.copy(
                spikesorted_raw_output_folder / recording_name / "spikeinterface_log.json", sorting_output_folder
            )
            with open(sorting_output_folder / "spikeinterface_log.json", "r") as f:
                log = json.load(f)
            print("\n\tSPIKE SORTING FAILED!\nError log:\n")
            pprint(log)
            sorting_outputs = dict()
            sorting_params = dict()

        t_sorting_end = time.perf_counter()
        elapsed_time_sorting = np.round(t_sorting_end - t_sorting_start, 2)

        spikesorting_process = DataProcess(
            name="Spike sorting",
            software_version=VERSION,  # either release or git commit
            start_date_time=datetime_start_sorting,
            end_date_time=datetime_start_sorting + timedelta(seconds=np.floor(elapsed_time_sorting)),
            input_location=str(data_folder),
            output_location=str(results_folder),
            code_url=URL,
            parameters=sorting_params,
            outputs=sorting_outputs,
            notes=spikesorting_notes,
        )
        with open(sorting_output_process_json, "w") as f:
            f.write(spikesorting_process.model_dump_json(indent=3))

    t_sorting_end_all = time.perf_counter()
    elapsed_time_sorting_all = np.round(t_sorting_end_all - t_sorting_start_all, 2)
    print(f"SPIKE SORTING time: {elapsed_time_sorting_all}s")
