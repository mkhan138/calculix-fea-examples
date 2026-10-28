from pathlib import Path
import csv

import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Settings: tensile bar from X = 0 mm to X = 100 mm
# ------------------------------------------------------------
FRD_FILE = Path("plastic_bar.frd")

X_LEFT = 0.0
X_RIGHT = 100.0
COORD_TOL = 1.0e-5


def read_frd(filename):
    """Read coordinates, DISP and FORC from an ASCII CalculiX FRD.

    Intended for the single-step static tensile-bar example.
    Supports short and long ASCII node-number fields.
    """
    coordinates = {}
    results = {}

    mode = None
    field = None
    time = None
    node_width = 10

    def number(text):
        return float(text.replace("D", "E").replace("d", "e"))

    def nodal_record(line):
        start = 3 + node_width
        node = int(line[3:start])

        # Fixed-width parsing also handles adjacent negative values.
        values = [
            number(line[i:i + 12])
            for i in range(start, len(line.rstrip("\r\n")), 12)
            if line[i:i + 12].strip()
        ]
        return node, values

    with filename.open("r", encoding="ascii", errors="strict") as stream:
        for line_number, line in enumerate(stream, start=1):
            try:
                # Original node coordinates
                if line[4:6] == "2C":
                    mode = "coordinates"
                    field = None

                    # Coordinate-header format indicator
                    fmt = int(line[73:75].strip() or "0")
                    if fmt not in (0, 1):
                        raise ValueError("Binary FRD is not supported.")
                    node_width = 5 if fmt == 0 else 10

                # Result dataset header
                elif line[2:6] == "100C":
                    mode = "results"
                    field = None
                    time = number(line[12:24])

                    fmt = int(line[73:75].strip() or "0")
                    if fmt not in (0, 1):
                        raise ValueError("Binary FRD is not supported.")
                    node_width = 5 if fmt == 0 else 10

                elif line.startswith(" -4") and mode == "results":
                    field = line.split()[1].upper()
                    if field in ("DISP", "FORC"):
                        frame = results.setdefault(time, {})
                        if field in frame:
                            raise ValueError(
                                f"Duplicate {field} at time {time}. "
                                "This script expects a single analysis step."
                            )
                        frame[field] = {}

                elif line.startswith(" -1"):
                    if mode == "coordinates":
                        node, values = nodal_record(line)
                        coordinates[node] = values[:3]

                    elif mode == "results" and field in ("DISP", "FORC"):
                        node, values = nodal_record(line)
                        results[time][field][node] = values[:3]

                elif line.startswith(" -3"):
                    mode = None
                    field = None

            except (ValueError, IndexError) as exc:
                raise ValueError(
                    f"Cannot parse FRD line {line_number}: "
                    f"{line.rstrip()!r}\n{exc}"
                ) from exc

    return coordinates, results


def main():
    coordinates, results = read_frd(FRD_FILE)

    left_nodes = {
        node for node, xyz in coordinates.items()
        if abs(xyz[0] - X_LEFT) <= COORD_TOL
    }
    right_nodes = {
        node for node, xyz in coordinates.items()
        if abs(xyz[0] - X_RIGHT) <= COORD_TOL
    }

    if not left_nodes or not right_nodes:
        raise ValueError(
            "Could not identify both end faces. "
            "Check X_LEFT, X_RIGHT and COORD_TOL."
        )

    rows = []

    for time, frame in sorted(results.items()):
        if "DISP" not in frame or "FORC" not in frame:
            raise ValueError(
                f"Missing DISP or FORC at time {time}. "
                "Request U and RF at the same output frequency."
            )

        displacement = frame["DISP"]
        reaction = frame["FORC"]

        missing_right = right_nodes - displacement.keys()
        missing_left = left_nodes - reaction.keys()

        if missing_right or missing_left:
            raise ValueError(
                f"Incomplete end-face output at time {time}: "
                f"{len(missing_right)} displacement nodes and "
                f"{len(missing_left)} reaction nodes missing."
            )

        u1 = np.mean([displacement[node][0] for node in right_nodes])
        force = -sum(reaction[node][0] for node in left_nodes)

        rows.append((time, u1, force))

    if not rows:
        raise ValueError("No matching displacement/reaction datasets found.")

    # The prescribed example starts unloaded.
    if rows[0][0] > 0.0:
        rows.insert(0, (0.0, 0.0, 0.0))

    data = np.asarray(rows)

    csv_file = FRD_FILE.with_name("force_displacement.csv")
    with csv_file.open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["time_s", "displacement_mm", "force_N"])
        writer.writerows(rows)

    fig, ax = plt.subplots()
    ax.plot(data[:, 1], data[:, 2])
    ax.set_xlabel("Displacement U1 [mm]")
    ax.set_ylabel("Tensile force [N]")
    ax.set_title("Elastic–plastic tensile bar")
    ax.grid(True, linestyle="--", alpha=0.6)
    fig.tight_layout()

    image_file = FRD_FILE.with_name("force_displacement.png")
    fig.savefig(image_file, dpi=300)

    print(f"Left-end nodes:  {len(left_nodes)}")
    print(f"Right-end nodes: {len(right_nodes)}")
    print(f"Final displacement: {data[-1, 1]:.6g} mm")
    print(f"Final tensile force: {data[-1, 2]:.6g} N")
    print(f"Saved: {csv_file}")
    print(f"Saved: {image_file}")

    plt.show()


if __name__ == "__main__":
    main()