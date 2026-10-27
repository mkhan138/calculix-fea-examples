# Standalone scripts

## Purpose
Running the examples in the repository.

## Platform
Software: Tested with Python 3.14.7
OS: Windows 11 and Ubuntu 26.04 on WSL2 (Windows 11)

## Contents

File                                    | Contents    
:-------------                          | :-------------
[run_all.py](run_all.py)                | Run all examples from root in the reposiroty    
[run_example.py](run_example.py)        | Run a particular example from the example directory

## Setup
To run the scripts, the repository must be installed as mentioned in [README](../README.md).

### run_all.py
This script runs all the examples in the repository and must be run from the root. It is installed as ```run-all```. After installing this repository, run from root:

```bash
run-all
```

### run_example.py
This script runs a particular example in the repository and must be run from the directory of the example. It is installed as ```run-example```. After installing this repository, run from root:

```bash
cd structural/linear_static/01_cube/
run-all
```