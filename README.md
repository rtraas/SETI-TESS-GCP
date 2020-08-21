# turboCLOUD
Extending Breakthrough Listen's Doppler drift searching algorithm for cloud-compatibility

A repository of my work during my 10-week internship with __[Breakthrough Listen](https://breakthroughinitiatives.org/initiative/1)__ at __[UC-Berkeley SETI Research Center](https://seti.berkeley.edu/)__ @UCBerkeleySETI

Doppler Drift Searches for Radio Technosignatures in Breakthrough Listen's Follow-Up Observations of TESS Targets

## Project Objectives
1. Port __[`turbo_seti`](https://github.com/UCBerkeleySETI/turbo_seti)__ to a `GCP` instance
2. Use __[`GCP` (Google Cloud Platform)](https://console.cloud.google.com/)__ to perform doppler drift searches for radio technosignatures in __[TESS](https://tess.mit.edu/)__ targets

## Getting Started

`turbo_seti_docker_tutorial.ipynb` --- A tutorial on using Docker to get your hands on `turbo_seti`

`docker_run_template.txt` --- A text file containing a template of the command to build a container based off the `turbo_seti` __[docker](https://www.docker.com/)__ image 

`GettingStarted.md` --- Where you should start if you're looking to get started with turboCLOUD.  It explains how to use all of the different functions as well as the ins and outs of turboCLOUD

## Python Scripts

`fileio` --- The main tool used to handle everything you need for fetching files quickly.  Retrieved files are given in absolute paths for quick implementation in any script found in the __[`pipes`](https://github.com/rtraas/turboCLOUD/tree/master/turbo_cloud/pipes)__ directory.


## __[Bash Scripts](https://github.com/rtraas/turboCLOUD/tree/master/turbo_cloud/doppler_search)__
All bash scripts are modified scripts from /datax/scratch/karenp/turbo_event at the Breakthrough Listen Data Center at UC-Berkeley

A tutorial can be found __[here](https://github.com/rtraas/turboCLOUD/tree/master/turbo_cloud/doppler_search)__.

`L_BandFDoppSearch.sh` --- Used to run turboSETI on all L_band files from the GCS bucket "bl_tess" mounted to the directory "/home/raffytraas14/seti_tess/" on the Google Compute Engine Instance

`S_BandFDoppSearch.sh` --- Used to run turboSETI on all S_band files from the GCS bucket "bl_tess" mounted to the directory "/home/raffytraas14/seti_tess/" on the Google Compute Engine Instance

`X_BandFDoppSearch.sh` --- Used to run turboSETI on all X_band files from the GCS bucket "bl_tess" mounted to the directory "/home/raffytraas14/seti_tess/" on the Google Compute Engine Instance

`C_BandFDoppSearch.sh` --- Used to run turboSETI on all C_band files from the GCS bucket "bl_tess" mounted to the directory "/home/raffytraas14/seti_tess/" on the Google Compute Engine Instance
