@echo off
cd /d "%~dp0"

# Build geometry and mesh
cgx -b heatsink_steadyState.fbd

# Solve using ccx
ccx -i heatsink_steadyState

# Visualize the nodal temperature
cgx -b post_temp.fbd

pause