# Cube

## Purpose
Demonstration of linear static analysis of a single element cube with one face fixed in all three directions.

A cube of dimension 1x1x1 mm with a single C3D20 element is displaced by 0.002 mm in the case of displacement-controlled simulation (left). Similarly, in the case of force-controlled experiment a force of 420 N (equal to 420 N/mm<sup>2</sup> or 420 MPa) is applied (right). The simulation is linear elastic so according to Hooke's law, in the displacement-controlled case (left), a constant von Mises stress of 420 MPa is achieved, whereas in the force-controlled case (right), the cube is displaced by 0.002 mm.

One face of the cube in each translational degree of freedom is constrained. The displacement and force are applied in the positive y-direction.

## Platform
Software: Tested with cgx 2.23/ccx 2.23\
OS: Windows 11 and Ubuntu 26.04 on WSL2 (Windows 11)

## Contents

File                                             | Contents    
:-------------                                   | :-------------
[cube_linearstatic.fbd](cube.fbd)                | Pre-processing script for CGX for generating cube and its mesh    
[cube_linearstatic.inp](cube_linearstatic.inp)   | CCX input for force controlled simulation
[post_d2.fbd](post_d2.fbd)                       | Post-processing script for CGX (contour plot of displacement in y-direction)
[post_mises.fbd](post_mises.fbd)                 | Post-processing script for CGX (contour plot of von Mises stress)
[run_windows.bat](run_windows.bat)               | Run all commands to solve and view the simulations' results on windows
[run_linux.sh](run_linux.sh)                     | Run all commands to solve and view the simulations' results on linux
[run.py](run.py)                                 | Run all commands to solve and view the simulations' results on any platform

## Preprocessing
An example to run the simulation. Second order quadrilateral fully integrated single element (C3D20) is used for the analysis.

Boundary conditions:
* For one face in y-direction: uy = 0 mm
* For one face in x-direction: ux = 0 mm
* For one face in z-direction: uz = 0 mm

Loading:
* For the opposite face in y-direction: uy = 0.002 mm (left cube)
* For the opposite face in y-direction: pressure = -420 MPa (right cube)

### Generating mesh and node sets

```
> cgx -b cube_linearstatic.fbd
```

## Solving
```
> ccx -i cube_linearstatic
```

## Postprocessing
```
> cgx -b post_d2.fbd
```

This creates a contour plot of the displacement in axial direction.

<img src="results/plot_d2.png" width="300" title="Displacement in axial direction">

```
> cgx -b post_mises.fbd
```

This creates a contour plot of the von Mises stress.

<img src="results/plot_mises.png" width="300" title="Von Mises Stress">

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