@echo off
cd /d "%~dp0"

# Build geometry and mesh
cgx -b plastic_bar.fbd

# Solve using ccx
ccx -i plastic_bar

# Visualize displacement in x direction
cgx -b post_d1.fbd

# Visualize Sxx stress
cgx -b post_Sxx.fbd

# Visualize plastic equivalent strain
cgx -b post_pe.fbd

pause