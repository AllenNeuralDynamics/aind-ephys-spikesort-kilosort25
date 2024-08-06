# Spike sorting with Kilosort2.5 for AIND ephys pipeline
## aind-ephys-spikesort-kilosort25


### Description

This capsule is designed to spike sort ephys data using [Kilosort2.5](https://github.com/MouseLand/Kilosort/tree/c31df11de9a4235c22a20909884f467c3813a2e4) for the AIND pipeline.

This capsule spike sorts preprocessed ephys stream and applies a minimal curation to:

- remove empty units
- remove excess spikes (falling beyond the end of the recording)


### Inputs

The `data/` folder must include the output of the [aind-ephys-preprocessing](https://github.com/AllenNeuralDynamics/aind-ephys-preprocessing), containing 
the `data/preprocessed_{recording_name}` folder.

### Parameters

The `code/run` script takes the following arguments:

```bash
  --n-jobs N_JOBS       Number of jobs to use for parallel processing. Default is -1 (all available cores). 
                        It can also be a float between 0 and 1 to use a fraction of available cores
  --min-drift-channels MIN_DRIFT_CHANNELS
                        Minimum number of channels to enable Kilosort motion correction. Default is 96.
  --params-file PARAMS_FILE
                        Optional json file with parameters
  --params-str PARAMS_STR
                        Optional json string with parameters

```

A list of spike sorting parameters can be found in the `code/params.json`:

```json
{
    "job_kwargs": {
        "chunk_duration": "1s",
        "progress_bar": false
    },
    "sorter": {
        "detect_threshold": 6,
        "projection_threshold": [10, 4],
        "preclust_threshold": 8,
        "car": true,
        "minFR": 0.1,
        "minfr_goodchannels": 0.1,
        "nblocks": 5,
        "sig": 20,
        "freq_min": 150,
        "sigmaMask": 30,
        "nPCs": 3,
        "ntbuff": 64,
        "nfilt_factor": 4,
        "NT": null,
        "AUCsplit": 0.9,
        "do_correction": true,
        "wave_length": 61,
        "keep_good_only": false,
        "skip_kilosort_preprocessing": false,
        "scaleproc": null,
        "save_rez_to_mat": false,
        "delete_tmp_files": ["matlab_files"],
        "delete_recording_dat": false
    }
}
```

### Output

The output of this capsule is the following:

- `results/spikesorted_{recording_name}` folder, containing the spike sorted data saved by SpikeInterface and the spike sorting log
- `results/data_process_spikesorting_{recording_name}.json` file, a JSON file containing a `DataProcess` object from the [aind-data-schema](https://aind-data-schema.readthedocs.io/en/stable/) package.

