#!/usr/bin/env python3
"""
This script automates the generation of mesh geometries and parses .frd output 
files for displacement-controlled and force-controlled cube simulations.

Author: Muhammad Mohsin Khan
Date: October 16, 2026
License: MIT
Repository: https://github.com/mkhan138/calculix-fea-examples
"""

import os
import subprocess
import sys

# ==========================================================
# CONFIGURATION
# ==========================================================
WORKDIR = os.getcwd()

CGX = "cgx.exe"
CCX = "ccx.exe"

# Simulation job name (without file extension)
JOB_NAME = "plate_with_hole_quarter"

# Input files
FBD = os.path.join(WORKDIR, f"{JOB_NAME}.fbd")
INP = os.path.join(WORKDIR, f"{JOB_NAME}.inp")

# Post-processing scripts
POSTPROCESSING_FILES = [
    "post_d1.fbd",
    "post_mises.fbd"
]


# ==========================================================
# 1. RUN CGX TO GENERATE THE MESH
# ==========================================================
def run_preprocessing():
    print("\n[1/3] Running CGX batch preprocessing...")

    if not os.path.isfile(FBD):
        sys.exit(f"[ERROR] Geometry script not found: {FBD}")

    try:
        cgx_result = subprocess.run(
            [CGX, "-b", FBD],
            cwd=WORKDIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            check=False,
        )
    except FileNotFoundError:
        sys.exit(f"[ERROR] Could not find CGX executable: {CGX}")

    log_path = os.path.join(WORKDIR, f"{JOB_NAME}_cgx.log")

    with open(log_path, "w", encoding="utf-8", errors="replace") as f:
        f.write(cgx_result.stdout)

    print(cgx_result.stdout)

    if cgx_result.returncode != 0:
        sys.exit(
            f"[ERROR] CGX preprocessing failed. Check {log_path}"
        )

    print("[OK] CGX preprocessing completed.")


# ==========================================================
# 2. RUN CCX SOLVER
# ==========================================================
def run_solver():
    print(f"\n[2/3] Running CalculiX for {JOB_NAME}...")

    if not os.path.isfile(INP):
        sys.exit(f"[ERROR] Input file not found: {INP}")

    try:
        ccx_result = subprocess.run(
            [CCX, "-i", JOB_NAME],
            cwd=WORKDIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            check=False,
        )
    except FileNotFoundError:
        sys.exit(f"[ERROR] Could not find CCX executable: {CCX}")

    log = ccx_result.stdout
    log_path = os.path.join(WORKDIR, f"{JOB_NAME}_solver.log")

    with open(log_path, "w", encoding="utf-8", errors="replace") as f:
        f.write(log)

    print(log)

    if ccx_result.returncode != 0:
        sys.exit(
            f"[ERROR] CCX solver failed. Check {log_path}"
        )

    # Verify that the expected result file was generated.
    frd_path = os.path.join(WORKDIR, f"{JOB_NAME}.frd")

    if not os.path.isfile(frd_path):
        sys.exit(
            f"[ERROR] Solver returned successfully, but the FRD file "
            f"was not found: {frd_path}"
        )

    print(f"[OK] Analysis completed for {JOB_NAME}.")
    print(f"[OK] Results: {frd_path}")


# ==========================================================
# 3. RUN CGX POST-PROCESSING SEQUENTIALLY
# ==========================================================
def run_postprocessing():
    print("\n[3/3] Running CGX post-processing sequentially...")

    for script_name in POSTPROCESSING_FILES:
        script_path = os.path.join(WORKDIR, script_name)

        if not os.path.isfile(script_path):
            print(f"[WARNING] Post-processing script not found: {script_path}")
            continue

        print(f"\n[INFO] Running {script_name}...")
        print("[INFO] Waiting for CGX to finish before continuing...")

        try:
            result = subprocess.run(
                [CGX, "-b", script_path],
                cwd=WORKDIR,
                check=False,
            )
        except FileNotFoundError:
            sys.exit(f"[ERROR] Could not find CGX executable: {CGX}")

        if result.returncode != 0:
            print(
                f"[WARNING] CGX returned an error while running "
                f"{script_name} (exit code {result.returncode})."
            )
            print("[INFO] Continuing to the next script...")

        else:
            print(f"[OK] Finished {script_name}.")

    print("\n[OK] All post-processing scripts have been processed.")


# ==========================================================
# MAIN EXECUTION
# ==========================================================
if __name__ == "__main__":
    # Generate the mesh
    run_preprocessing()

    # Solve the single linear-static simulation
    run_solver()

    # Launch displacement and stress post-processing
    run_postprocessing()

    print("\nAll simulation and post-processing tasks triggered.")