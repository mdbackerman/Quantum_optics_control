# Quantum_optics_control

From June to September 2022 I worked in a quantum optics subgroup in the Lukin Group at Harvard University. The subgroup I was in studied 2D materials/TMDs (transition metal dichalcogenides) using spectroscopy and NV centers. During my time I built a CSLM (Confocal Scanning laser Microscope) and wrote software to control the setup for NV-based measurements. Software was written in Python in a Jupyter-Lab notebook and then moved to a GUI-based interface written from scratch using PyQt5. The [QCoDeS](https://qcodes.github.io) data-acquisition framework was used to run the experiment.

## `GUI`

This is a folder containing the GUI-based implementation of the experiment contorl software.

## `room_temp_NV_control`

This file is the notebook running the setup on the optical bench


## `plotting-results`

This file contains all of the collected images from the CSLM once consistently working scanning was acheived.

## `md_file`

This is a running file with old code sections used as reference.

## `nidaqmx_counter_ex`

This file is an older program dedicated to interfacing with the counter input channels on the cDAQ NI-9402 card.
