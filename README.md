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
[<img
  src="thermal/transient/01_heatsink/results/movie.gif"
  width="200"
  title="Heat transfer analysis of a heatsink">
](thermal/transient/01_heatsink/)

This repository demonstrates how to set up, run, and evaluate FEA simulations using practical engineering examples. It aims to provide a structured and accessible reference for learning finite element analysis, understanding simulation workflows, and exploring the capabilities of CalculiX.

## Repository Structure
```text
calculix-fea-examples/
├── src/  
│   ├── postprocessing_scripts/
│   ├── run_all.py
│   └── run_example.py
├── structural/          
│   ├── linear_static/
│   └── nonlinear_static/
├── thermal/                
│   ├── steady_state/
│   └── transient/
├── INSTALLATION.md
├── LICENSE
├── pyproject.toml
└── README.md
```

The repository is organized by physical domain and analysis type. Each analysis type (e.g. steady_state) inside of a physical domain (e.g. thermal) contains examples. Each example is intended to be self-contained, with its own model files, documentation, and relevant results.

## Prerequisites
* CalculiX GraphiX (cgx) and CrunchiX (ccx) 2.23, see [INSTALLATION](INSTALLATION.md) for Windows 11 x64 and Ubuntu/Debian .

## Getting Started
1. Clone and install this repository:
```bash
git clone https://github.com/mkhan138/calculix-fea-examples
cd calculix-fea-examples
python -m venv .venv
```

2. Activate the environment:

For Ubuntu/Debian:
```bash
source .venv/bin/activate
```

For Windows 11:
```bash
.\.venv\Scripts\Activate.ps1
```

then install from the root repository:
```bash
python -m pip install --upgrade pip
python -m pip install .
```

3. Execute the following from root directory for running all examples on this repository:
```bash
run-all
```

4. For running a specific example in the repository, navigate to an example directory:
```bash
cd structural/linear_static/01_cube/
```

5. Execute the following from example directory:
```bash
run-example
```

See the individual example directories for model-specific instructions.

## Validation and Accuracy
Where applicable, simulation results will be compared against analytical solutions, established benchmarks, or other reference data.

The examples are intended for educational and exploratory purposes. Results depend on the assumptions, material models, mesh quality, boundary conditions, and solver settings used in each case.

## Contributing
Suggestions, corrections, and additional examples are welcome. Contributions should include a clear description of the problem, the model assumptions, and instructions for reproducing the results.

## License
See the repository [LICENSE](LICENSE) for terms of use and redistribution.