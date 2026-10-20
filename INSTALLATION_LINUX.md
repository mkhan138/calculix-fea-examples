# CalculiX CrunchiX (ccx) 2.23 Installation Guide

Build CalculiX CrunchiX (ccx) 2.23 and its multithreaded variant from source, together with SPOOLES 2.2 and ARPACK.

## Prerequisites

- An Ubuntu/Debian-based environment with `apt` and `sudo` access.
- An internet connection to download the source archives and ARPACK repository.
- Run the sections below in order, using the same terminal session.

> **Scope:** The commands have been executed and validated against Ubuntu-26.04 LTS.

## 1. Install build dependencies

```bash
# Refresh package metadata and upgrade installed packages.
sudo apt update
sudo apt upgrade

# Install C/Fortran compilers, build tools, download utilities and maths libraries.
sudo apt install -y build-essential gfortran make gcc \
    perl git wget curl bzip2 patch \
    libblas-dev liblapack-dev
```

## 2. Download and extract CalculiX CrunchiX

```bash
# Create the workspace for CalculiX and its dependencies.
mkdir -p ~/CalculiX
cd ~/CalculiX

# Download the solver source, documentation and test cases.
wget https://www.dhondt.de/ccx_2.23.src.tar.bz2
wget https://www.dhondt.de/ccx_2.23.doc.tar.bz2
wget https://www.dhondt.de/ccx_2.23.test.tar.bz2

# Extract all three archives into the workspace.
tar -xjf ccx_2.23.src.tar.bz2
tar -xjf ccx_2.23.doc.tar.bz2
tar -xjf ccx_2.23.test.tar.bz2
```

## 3. Build SPOOLES 2.2

```bash
# Download and extract the sparse solver library.
cd ~/CalculiX
wget https://www.netlib.org/linalg/spooles/spooles.2.2.tgz
mkdir -p SPOOLES.2.2
tar -xzf spooles.2.2.tgz -C SPOOLES.2.2
cd SPOOLES.2.2

# Replace the legacy compiler selection with GCC.
sed -i \
  -e 's|^[[:space:]]*CC[[:space:]]*=[[:space:]]*/usr/lang-4\.0/bin/cc|# CC = /usr/lang-4.0/bin/cc|' \
  -e 's|^[[:space:]]*#[[:space:]]*CC[[:space:]]*=[[:space:]]*gcc|CC = gcc|' \
  Make.inc

# Use level-two optimisation for the library build.
sed -i 's/^[[:space:]]*OPTLEVEL[[:space:]]*=.*/OPTLEVEL = -O2/' Make.inc

# Pass an integer initial value rather than NULL to IVinit.
sed -i 's/IVinit(nfront, NULL)/IVinit(nfront, 0)/g' ETree/src/transform.c

# Build the main library using the available processor cores.
make -j"$(nproc)" lib

# Build the multithreaded SPOOLES components.
cd ~/CalculiX/SPOOLES.2.2/MT/src
make
```

## 4. Build ARPACK

```bash
# Clone the ARPACK source repository.
cd ~/CalculiX
git clone https://github.com/ISCPC/ARPACK.git
cd ARPACK

# Replace the legacy timing routine with the CPU_TIME intrinsic.
cat > UTIL/second.f <<'EOF'
      SUBROUTINE SECOND( T )
      REAL       T
      CALL CPU_TIME(T)
      RETURN
      END
EOF

# Set the workspace, platform name and GNU Fortran compiler options.
sed -i \
  -e 's|^[[:space:]]*home[[:space:]]*=.*|home = $(HOME)/CalculiX/ARPACK|' \
  -e 's|^[[:space:]]*PLAT[[:space:]]*=.*|PLAT = LINUX|' \
  -e 's|^[[:space:]]*FC[[:space:]]*=.*|FC = gfortran|' \
  -e 's|^[[:space:]]*FFLAGS[[:space:]]*=.*|FFLAGS  = -O -fallow-argument-mismatch|' \
  ARmake.inc

# Compile the ARPACK library.
make lib
```

## 5. Build CalculiX 2.23

### Standard executable

```bash
# Enter the extracted solver source directory.
cd ~/CalculiX/CalculiX/ccx_2.23/src

# Apply the supplied return-statement correction at line 468.
sed -i '468s/return NULL;/return;/' readnewmesh.c

# Enable legacy Fortran argument compatibility and select GCC/ARPACK.
sed -i \
  -e '/^[[:space:]]*FFLAGS[[:space:]]*=/ s/$/ -fallow-argument-mismatch/' \
  -e 's/CC=cc/CC=gcc/g' \
  -e 's|../../../ARPACK/libarpack_INTEL\.a|../../../ARPACK/libarpack_LINUX.a|g' \
  Makefile

# Compile the standard executable in parallel.
make -j"$(nproc)"
```

### Multithreaded executable

```bash
# Configure compiler compatibility and dependency paths for the MT build.
sed -i \
  -e '/^[[:space:]]*FFLAGS[[:space:]]*=/ s/$/ -fallow-argument-mismatch/' \
  -e 's/CC=cc/CC=gcc/g' \
  -e '/^[[:space:]]*CFLAGS[[:space:]]*=/ s|\.\./SPOOLES\.2\.2|../../../SPOOLES.2.2|g' \
  -e 's|DIR=../SPOOLES\.2\.2|DIR=../../../SPOOLES.2.2|g' \
  -e 's|../ARPACK/libarpack_INTEL\.a|../../../ARPACK/libarpack_LINUX.a|g' \
  Makefile_MT

# Compile the multithreaded executable.
make -f Makefile_MT
```

> **Compatibility notes:** The `readnewmesh.c` patch depends on the original line numbering. Inspect line 468 before applying it if your source differs. The `sed` commands depend on the supplied makefile text and may silently leave unmatched settings unchanged. Repeating the compiler-flag edits appends the compatibility flag again.

## 6. Install the executables

```bash
# Copy both executables to the system-wide executable directory.
sudo cp ccx_2.23 /usr/local/bin/ccx_static
sudo cp ccx_2.23_MT /usr/local/bin/ccx
```

> **Note:**  ccx_2.23 is renamed as ccx_static and ccx_2.23_MT is renamed as ccx.

## 7. Run the beam test

```bash
# Enter the test directory and run the standard solver.
cd ~/CalculiX/CalculiX/ccx_2.23/test
ccx_static -i beamp

# Set the OpenMP thread count and run the MT executable.
export OMP_NUM_THREADS=4
ccx -i beamp
```

> Both runs use the same job name and directory, so the second run may overwrite output from the first. Check the solver output for successful completion; launching a test alone does not establish that it passed.

## References

- [Official CalculiX downloads](https://www.dhondt.de/)
- [Official CCX 2.23 installation guide](https://www.dhondt.de/ccx_2.23.README.INSTALL)

# CalculiX GraphiX (cgx) 2.23 Installation Guide

Install the precompiled CalculiX GraphiX (cgx) executable in `/usr/local/bin` and launch it from a terminal. No source compilation is included in this procedure.

## Prerequisites

- A Linux desktop with a working graphical display and OpenGL/GLU support.
- A system compatible with the official 64-bit Linux executable.
- `sudo` access for installation in `/usr/local/bin`.

The package-installation commands below are suggested for Ubuntu/Debian. Exact runtime dependencies depend on your distribution and the downloaded binary. These commands have not been executed on your machine.

## 1. Install download utilities

```bash
# Refresh package metadata and install download/decompression tools.
sudo apt update
sudo apt install -y wget bzip2
```

The official guide requires OpenGL and GLU. On Ubuntu/Debian, the following is a suggested starting point if these runtime libraries are missing:

```bash
# Install common OpenGL and GLU runtime libraries.
sudo apt install -y libgl1 libglu1-mesa libxmu6
```

## 2. Download the Linux executable

```bash
# Create a dedicated download directory.
mkdir -p ~/CalculiX/CGX
cd ~/CalculiX/CGX

# Download the official CGX 2.23 compressed executable.
wget http://www.dhondt.de/cgx_2.23.bz2

# Decompress the executable; this is not a tar archive.
bunzip2 cgx_2.23.bz2
```

> Download only from a trusted source. The download link above is the HTTP link published on the official download page.

## 3. Install in /usr/local/bin

```bash
# Ensure the system-wide executable directory exists.
sudo mkdir -p /usr/local/bin

# Copy the executable under the convenient command name cgx.
sudo cp cgx_2.23 /usr/local/bin/cgx

# Give the owner write access and everyone read/execute access.
sudo chmod 755 /usr/local/bin/cgx

# Check which executable your shell resolves.
command -v cgx
```

Expected command path:

```text
/usr/local/bin/cgx
```

This replaces any existing file at `/usr/local/bin/cgx`. Back it up first if you need to retain an older installation.

## 4. Launch CGX

```bash
# Start CGX in a writable working directory with a new model name.
cd ~/CalculiX/CGX
cgx -b dummy.fbd
```

The official installation test uses `cgx -b dummy.fbd`; a graphical window should appear. Run CGX as your normal user, not with `sudo`.

To start a model with your own name:

```bash
# Start the preprocessor using your chosen model filename.
cgx -b model.fbd
```

Move the mouse pointer inside the CGX drawing window before typing CGX commands. To access the menu, move outside the inner drawing rectangle and press the left mouse button.

## References

- [Official CalculiX downloads](https://www.dhondt.de/)
- [Official CGX 2.23 installation guide](https://www.dhondt.de/cgx_2.23.INSTALL)
- [Official CGX introductory tutorial](https://www.dhondt.de/tutorial.txt)