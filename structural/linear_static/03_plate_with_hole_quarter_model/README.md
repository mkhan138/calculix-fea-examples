# Plate with hole (quarter model)

## Purpose
Demonstration of linear static analysis of a plate with hole using quarter model.

<img src="inputs/problem.png" width="600" title="Problem description">

The quarter model of the plate is 100 mm long, 100 wide and 10 mm thick with a hole in the middle with a radius of 20 mm. Symmerty conditions are applied to the left with displacement fixed x direction, and to the bottom with displacement fixed in y direction. One node at x = 0 and y = 100 (top left) is fixed in z direction. A uniform traction load of 100 MPa is applied on the right face.

<img src="inputs/bc.png" width="600" title="Boundary conditions">

The above image shows the x symmetry condition (red), the y symmetry condition (blue), the surface (show by green nodes) where the traction force is applied.

## Platform
Software: Tested with cgx 2.23/ccx 2.23\
OS: Windows 11 and Ubuntu 26.04 on WSL2 (Windows 11)

## Contents

File                                                        | Contents    
:-------------                                              | :-------------
[plate_with_hole_quarter.fbd](plate_with_hole_quarter.fbd)  | Pre-processing script for CGX for generating cube and its mesh 
[plate_with_hole_quarter.inp](plate_with_hole_quarter.inp)  | CCX input for force controlled simulation   
[post_d1.fbd](post_d1.fbd)                                  | Post-processing script for CGX (contour plot of displacement in x-direction)
[post_mises.fbd](post_mises.fbd)                            | Post-processing script for CGX (contour plot of von Mises stress)
[run_windows.bat](run_windows.bat)                          | Run all commands to solve and view the simulations' results on windows
[run_linux.sh](run_linux.sh)                                | Run all commands to solve and view the simulations' results on linux
[run.py](run.py)                                            | Run all commands to solve and view the simulations' results on any platform

## Preprocessing
Second order quadrilateral fully integrated elements (C3D20) are used for the analysis.

Boundary conditions:
* X-symmetry: ux = 0 mm
* Y-symmetry: uy = 0 mm

Loading:
* The face on the right in x-direction: t = 100 MPa

### Generating mesh and node sets

```
> cgx -b plate_with_hole_quarter.fbd
```

## Solving
```
> ccx -i plate_with_hole_quarter
```

## Postprocessing
```
> cgx -b post_d1.fbd
```

This creates a contour plot of the displacement in x direction. The displacement in x direction is nearly similar to the analytical values (see [analytical solution](reference/analytical_solution_quarter_plate_hole.ipynb)

<img src="results/plot_d1.png" width="300" title="Displacement in x direction">

```
> cgx -b post_mises.fbd
```

This creates a contour plot of the von Mises stress. The stresses are little higher than [analytical solution](reference/analytical_solution_quarter_plate_hole.ipynb). This could be due to mesh, but also because the results show nodal averaging and not the stress at integration points.

<img src="results/plot_mises.png" width="300" title="Von mises stress">

## Run complete project
To run the complete project on linux, run:
```
> chmod +x run_linux.sh
> ./run_linux.sh
```

On windows, double click on "run_windows.bat", or open cmd, navigate to the directory and run:
```
> run_windows.bat
```

Using python3 on any platform:
```
> python run.py
```