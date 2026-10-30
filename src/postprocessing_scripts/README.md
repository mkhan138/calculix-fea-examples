# Postprocessing scripts

## Purpose
Diverse postprocessing scripts to evaluate the results of a simulation.

## Platform
Software: Tested with Python 3.14.7\
OS: Windows 11 and Ubuntu 26.04 on WSL2 (Windows 11)

## Contents

File                                               | Contents    
:-------------                                     | :-------------
[plot_max_nodal_temp.py](plot_max_nodal_temp.py)   | Plot the max. nodal temperature of a model   


## Setup
To run the scripts, the repository must be installed as mentioned in [README](../../README.md).

### plot_max_nodal_temp.py
This script must be run from an example directory. It is installed as ```plot-max-ndtemp```. An example use is mentioned in [Heatsink example](../../thermal/transient/01_heatsink/README.md). For example:

```bash
cd thermal/transient/01_heatsink/
cgx -b heatsink_transient.fbd
ccx -i heatsink_transient
plot-max-ndtemp heatsink_transient.frd
```