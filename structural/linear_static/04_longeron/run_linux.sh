#!/bin/bash

cd "$(dirname "$0")" || exit 1

# Build geometry and mesh
cgx -b longeron_rod.fbd

# Solve using ccx
ccx -i longeron_rod

# Visualize axial displacement
cgx -b post_d1.fbd

# Visualize axial stress
cgx -b post_Sxx.fbd