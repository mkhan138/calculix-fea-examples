#!/bin/bash

cd "$(dirname "$0")" || exit 1

# Build geometry and mesh
cgx -b heatsink_steadyState.fbd

# Solve using ccx
ccx -i heatsink_steadyState

# Visualize the nodal temperature
cgx -b post_temp.fbd