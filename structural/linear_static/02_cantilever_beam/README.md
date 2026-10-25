# Cantilever Beam

## Purpose
Demonstration of linear static analysis of a cantilever beam fully fixed at one end.

A cantilever beam loaded by point forces at its free end is analyzed. The problem is taken from the CalculiX 2.23 manual. The geometry, loading and boundary conditions are shown in the figure below.

<img src="inputs/problem.png" width="600" title="Problem description">

The beam size is 1000 x 1000 x 8000 mm<sup>3</sup>, which is loaded with a point force of 9x10<sup>6</sup> N and is completely fixed in all directions on the left end. See [analytical solution](reference/analytical_solution_cantilever_beam.ipynb) for the analytical solution.

<img src="inputs/bc.png" width="600" title="Boundary conditions">

The nodes in red show the fixed end of the beam where it is fixed in all directions and the free end is shown in blue where load in applied in positive y direction.

## Platform
Software: Tested with cgx 2.23/ccx 2.23\
OS: Windows 11 and Ubuntu 26.04 on WSL2 (Windows 11)

## Contents

File                                                         | Contents    
:-------------                                               | :-------------
[cantilever_linearstatic.fbd](cantilever_linearstatic.fbd)   | Pre-processing script for CGX for generating cube and its mesh     
[cantilever_linearstatic.inp](cantilever_linearstatic.inp)   | CCX input of the simulation
[post_d2.fbd](post_d2.fbd)                                   | Post-processing script for CGX (contour plot of displacement in y direction)
[post_mises.fbd](post_mises.fbd)                             | Post-processing script for CGX (contour plot of von Mises stress)
[post_Szz.fbd](post_Szz.fbd)                                 | Post-processing script for CGX (contour plot of stress in z direction)
[run_windows.bat](run_windows.bat)                           | Run all commands to solve and view the simulations' results on windows
[run_linux.sh](run_linux.sh)                                 | Run all commands to solve and view the simulations' results on linux
[run.py](run.py)                                             | Run all commands to solve and view the simulations' results on any platform

## Preprocessing
Elements of second order quadrilateral with reduced integration (C3D20R) are used for the analysis.

Boundary conditions:
* Left end fixed in all directions: ux = uy = uz = 0 mm

Loading:
* Point force applied on the right end with 9x10<sup>6</sup> N

### Generating mesh and node sets

```
> cgx -b cantilever_linearstatic.fbd
```

## Solving
```
> ccx -i cantilever_linearstatic
```

## Postprocessing
```
> cgx -b post_d2.fbd
```

This creates a contour plot of the displacement in y direction with a deformation factor of 10. 

<img src="results/plot_d2_linearStatic.png" width="300" title="Displacement in y direction">

This figure shows the deformation of the beam, under the load. As expected, the beam bends due to the lateral force at its right end. The result here exactly matches with the analytical solution, as mentioned in [analytical solution](reference/analytical_solution_cantilever_beam.ipynb).

```
> cgx -b post_mises.fbd
```

This creates a contour plot of the von Mises stress.

<img src="results/plot_mises_linearStatic.png" width="300" title="Von Mises Stress">


```
> cgx -b post_Szz.fbd
```

This creates a contour plot of the stress in axial direction.

<img src="results/plot_Szz_linearStatic.png" width="300" title="Stress in axial direction">

This figure shows the normal stress in axial direction, which is distributed almost linearly across the height of the beam due to the bending moment.

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