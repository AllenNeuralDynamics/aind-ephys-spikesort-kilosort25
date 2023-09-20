# Spike sort with Kilosort2.5 for AIND ephys pipeline
## aind-capsule-ephys-spikesort-kilosort25


### Description

This capsule is designed to spike sort ephys data using [Kilosort2.5](https://github.com/MouseLand/Kilosort/tree/c31df11de9a4235c22a20909884f467c3813a2e4) for the AIND pipeline.

This capsule spike sorts preprocessed ephys stream and applies a minimal curation to:

- remove empty units
- remove excess spikes (falling beyond the end of the recording)


### Inputs

The `data/` folder must include the output of the [aind-capsule-ephys-preprocessing](https://github.com/AllenNeuralDynamics/aind-capsule-ephys-preprocessing), containing 
the `data/preprocessed_{recording_name}` folder.

### Parameters

The `code/run` script takes no arguments.

### Output

The output of this capsule is the following:

- `results/spikesorted_{recording_name}` folder, containing the spike sorted data saved by SpikeInterface and the spike sorting log
- `results/data_procress_spikesorting_{recording_name}.json` file, a JSON file containing a `DataProcess` object from the [aind-data-schema](https://aind-data-schema.readthedocs.io/en/stable/) package.

