import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

# GENERAL IMPORTS
import os
import numpy as np
from pathlib import Path
import shutil
import json
import sys
import time
from datetime import datetime, timedelta

# SPIKEINTERFACE
import spikeinterface as si
import spikeinterface.extractors as se
import spikeinterface.sorters as ss
import spikeinterface.curation as sc

# AIND
from aind_data_schema import Processing
from aind_data_schema.processing import DataProcess

# LOCAL
URL = "https://github.com/AllenNeuralDynamics/aind-capsule-ephys-spikesort-kilosort25"
VERSION = "0.1.0"

### PARAMS ###
n_jobs = os.cpu_count()
job_kwargs = dict(n_jobs=n_jobs, chunk_duration="1s", progress_bar=False)

sorter_name = "kilosort2_5"
sorter_params = dict()

data_folder = Path("../data")
results_folder = Path("../results")
scratch_folder = Path("../scratch")


if os.getenv("AWS_BATCH_JOB_ID") is not None:
    print("PIPELINE: setting symlinks for CUDA libraries")
    src_folder = Path("/mnt/usr/local/cuda-11.4/targets/x86_64-linux/lib/")
    dst_folder = Path("/usr/lib/x86_64-linux-gnu/")
    cuda_libs = [p for p in Path(src).iterdir() if "cuda" in p.name]
    print(cuda_libs)
    for cuda_lib in cuda_libs:
        src = str(cuda_lib)
        dst = str(dst_folder / cuda_lib.name)
        print(f"Creating symlink {src} --> {dst}")
        os.symlink(src, dst)


if __name__ == "__main__":
    data_process_prefix = "data_process_spikesorting"

    ####### SPIKESORTING ########
    print("\n\nSPIKE SORTING")
    sorting_params = None

    print(f"PyKilosort version: {pykilosort.__version__}")

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
            sorting = ss.run_sorter(sorter_name, recording, output_folder=spikesorted_raw_output_folder / recording_name,
                                    verbose=False, delete_output_folder=True, **sorter_params)
        except Exception as e:
            # save log to results
            sorting_output_folder.mkdir()
            shutil.copy(spikesorted_raw_output_folder / "spikeinterface_log.json", sorting_output_folder)
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

        print(f"\tSorting output without empty units: {sorting}")
        spikesorting_notes += f"{len(sorting.unit_ids)} after removing empty templates.\n"
        
        # split back to get original segments
        if recording.get_num_segments() > 1:
            sorting = si.split_sorting(sorting, recording)

        # save results 
        print(f"\tSaving results to {sorting_output_folder}")
        sorting = sorting.save(folder=sorting_output_folder)

        t_sorting_end = time.perf_counter()
        elapsed_time_sorting = np.round(t_sorting_end - t_sorting_start, 2)
    
        # save params in output
        sorting_outputs = dict(
            empty_units=n_empty_units
        )
        spikesorting_process = DataProcess(
                name="Spike sorting",
                version=VERSION, # either release or git commit
                start_date_time=datetime_start_sorting,
                end_date_time=datetime_start_sorting + timedelta(seconds=np.floor(elapsed_time_sorting)),
                input_location=str(data_folder),
                output_location=str(results_folder),
                code_url=URL,
                parameters=sorting_params,
                outputs=sorting_outputs,
                notes=spikesorting_notes
            )
        with open(sorting_output_process_json, "w") as f:
            f.write(spikesorting_process.json(indent=3))

    t_sorting_end_all = time.perf_counter()
    elapsed_time_sorting_all = np.round(t_sorting_end_all - t_sorting_start_all, 2)
    print(f"SPIKE SORTING time: {elapsed_time_sorting_all}s")
