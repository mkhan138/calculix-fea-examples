#!/bin/bash

cd "$(dirname "$0")" || exit 1

# Build geometry and mesh
cgx -b heatsink_transient.fbd

# Solve using ccx
ccx -i heatsink_transient

# Visualize the nodal temperature
cgx -b post_temp.fbd

# Plot max. temperature
python ..\..\..\scripts\plot_max_nd_temp.py heatsink_transient.frd