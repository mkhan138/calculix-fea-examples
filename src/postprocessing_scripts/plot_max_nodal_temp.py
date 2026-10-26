#!/usr/bin/env python3
"""
This script plots the maximum nodal temperature over time
for a simulation and saves the results as png and csv in
the results folder of the current working directory.

Author: Muhammad Mohsin Khan
Date: October 25, 2026
License: MIT
Repository: https://github.com/mkhan138/calculix-fea-examples
"""

from pathlib import Path
import csv
import argparse

import numpy as np
import matplotlib.pyplot as plt
import pyvista_frd


# ============================================================
# CONFIGURATION
# ============================================================
# Outputs are saved relative to the directory from which
# the script is executed, not the script's own directory.
RESULTS_DIR = Path.cwd() / "results"

CSV_FILE = RESULTS_DIR / "max_temperature.csv"
PNG_FILE = RESULTS_DIR / "max_temperature.png"

TEMPERATURE_UNIT = "°C"


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Extract and plot maximum nodal temperature "
            "versus time from a CalculiX FRD file."
        )
    )

    # FRD input is supplied by the user for each analysis.
    parser.add_argument(
        "frd_file",
        help=(
            "Path to the FRD result file, absolute or relative "
            "to the current working directory."
        ),
    )

    args = parser.parse_args()

    # ========================================================
    # RESOLVE INPUT FILE
    # ========================================================
    frd_file = Path(args.frd_file).expanduser().resolve()

    if not frd_file.is_file():
        parser.error(f"FRD file not found: {frd_file}")

    if frd_file.suffix.lower() != ".frd":
        parser.error("Input file must have a .frd extension.")

    # Create results folder in the current working directory.
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Input file: {frd_file}")
    print(f"Working directory: {Path.cwd()}")
    print(f"Output directory: {RESULTS_DIR.resolve()}")

    # ========================================================
    # READ FRD AND GET SAVED TIME INCREMENTS
    # ========================================================
    reader = pyvista_frd.FRDReader(str(frd_file))

    times = np.asarray(
        reader.time_values, dtype=float
    ).ravel()

    if times.size == 0:
        raise RuntimeError(
            "No time increments found in the FRD file."
        )

    print(f"Saved result increments: {len(times)}\n")

    max_temperatures = []
    valid_times = []

    # ========================================================
    # PROCESS EVERY SAVED INCREMENT
    # ========================================================
    for i, time in enumerate(times):
        reader.set_active_time_point(i)
        mesh = reader.read()

        available = list(mesh.point_data.keys())

        temperature_key = next(
            (
                name for name in available
                if name.upper() in (
                    "NDTEMP", "TEMP", "TEMPERATURE", "NT"
                )
            ),
            None,
        )

        if temperature_key is None:
            raise KeyError(
                f"No nodal temperature field at increment {i}.\n"
                f"Available fields: {available}"
            )

        temperature = np.asarray(
            mesh.point_data[temperature_key],
            dtype=float,
        ).reshape(-1)

        finite = temperature[np.isfinite(temperature)]

        if finite.size == 0:
            raise RuntimeError(
                f"No valid nodal temperatures at time {time:g}."
            )

        maximum = float(np.max(finite))

        valid_times.append(float(time))
        max_temperatures.append(maximum)

        print(
            f"{i + 1:5d}/{len(times)} | "
            f"time = {time:12.6g} | "
            f"Tmax = {maximum:12.6g} "
            f"{TEMPERATURE_UNIT}"
        )

    valid_times = np.asarray(valid_times, dtype=float)
    max_temperatures = np.asarray(
        max_temperatures, dtype=float
    )

    # ========================================================
    # SAVE CSV
    # ========================================================
    with CSV_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.writer(f)
        writer.writerow([
            "time",
            f"maximum_temperature_{TEMPERATURE_UNIT}",
        ])
        writer.writerows(
            zip(valid_times, max_temperatures)
        )

    # ========================================================
    # REPORT GLOBAL PEAK
    # ========================================================
    peak_index = int(np.argmax(max_temperatures))

    print("\n" + "=" * 55)
    print("TRANSIENT THERMAL RESULTS")
    print("=" * 55)
    print(f"Number of increments: {len(valid_times)}")
    print(
        f"Peak temperature: "
        f"{max_temperatures[peak_index]:.6g} "
        f"{TEMPERATURE_UNIT}"
    )
    print(f"Time of peak: {valid_times[peak_index]:.6g}")
    print(f"CSV saved: {CSV_FILE.resolve()}")

    # ========================================================
    # PLOT
    # ========================================================
    fig, ax = plt.subplots(figsize=(9, 5.5))

    ax.plot(
        valid_times,
        max_temperatures,
        linewidth=1.8,
        marker="o" if len(valid_times) <= 50 else None,
        markersize=3,
        label="Maximum nodal temperature",
    )

    ax.scatter(
        valid_times[peak_index],
        max_temperatures[peak_index],
        zorder=3,
        label=(
            f"Peak: {max_temperatures[peak_index]:.5g} "
            f"{TEMPERATURE_UNIT}"
        ),
    )

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=20)

    ax.set_xlabel("Time [s]")
    ax.set_ylabel(
        f"Maximum nodal temperature [{TEMPERATURE_UNIT}]"
    )
    ax.set_title(
        f"{frd_file.stem}: Transient Thermal Response"
    )
    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()

    fig.savefig(
        PNG_FILE,
        dpi=300,
        bbox_inches="tight",
    )

    print(f"PNG saved: {PNG_FILE.resolve()}")
    print("=" * 55)


if __name__ == "__main__":
    main()