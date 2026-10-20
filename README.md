# CalculiX FEA Examples
A collection of finite element analysis (FEA) examples using **[CalculiX](http://www.dhondt.de/)**, an open-source finite element analysis solver.

[<img
  src="structural/linear_static/01_cube/results/plot_d2.png"
  width="200"
  title="Linear elastic displacement of a single element cube">
  ](structural/linear_static/01_cube/)
[<img
  src="structural/linear_static/02_cantilever_beam/results/plot_d2_linearStatic.png"
  width="200"
  title="Linear elastic analysis of a cantilever beam">
](structural/linear_static/02_cantilever_beam/)
[<img
  src="structural/linear_static/03_plate_with_hole_quarter_model/results/plot_mises.png"
  width="200"
  title="Linear elastic analysis of a plate with a hole (quarter model)">
](structural/linear_static/03_plate_with_hole_quarter_model/)

This repository demonstrates how to set up, run, and evaluate FEA simulations using practical engineering examples. It aims to provide a structured and accessible reference for learning finite element analysis, understanding simulation workflows, and exploring the capabilities of CalculiX.

## Repository Structure
```text
calculix-fea-examples/
├── structural/                  # Structural analyses
│   ├── linear_static/             # Linear static analyses
├── INSTALLATION_LINUX.md
├── INSTALLATION_WINDOWS.md
├── LICENSE.md
├── README.md
└── run_all.py
```

The repository is organized by physical domain and analysis type. Each example is intended to be self-contained, with its own model files, documentation, and relevant results.

## Prerequisites
* CalculiX GraphiX (cgx) and CrunchiX (ccx) 2.23, see [INSTALLATION_LINUX](INSTALLATION_LINUX.md) for Ubuntu/Debian or [INSTALLATION_WINDOWS](INSTALLATION_WINDOWS.md) for Windows 11 x64.

## Getting Started
1. Clone this repository:
```bash
git clone https://github.com/mkhan138/calculix-fea-examples
```

2. Navigate to an example directory:
```bash
cd ./calculix-fea-examples/structural/linear_static/01_cube/
```

3. Run the simulation using the CalculiX CrunchiX solver:
```bash
ccx -i cube_linearstatic.inp
```

4. Inspect the results with CalculiX GraphiX.
```bash
cgx -v cube_linearstatic.frd
```

See the individual example directories for model-specific instructions.

5. Execute the following from root directory for running all examples on this repository:
```bash
python run_all.py
```

## Validation and Accuracy
Where applicable, simulation results will be compared against analytical solutions, established benchmarks, or other reference data.

The examples are intended for educational and exploratory purposes. Results depend on the assumptions, material models, mesh quality, boundary conditions, and solver settings used in each case.

## Contributing
Suggestions, corrections, and additional examples are welcome. Contributions should include a clear description of the problem, the model assumptions, and instructions for reproducing the results.

## License
See the repository [LICENSE](LICENSE) for terms of use and redistribution.