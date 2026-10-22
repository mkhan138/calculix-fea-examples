# CalculiX CrunchiX (ccx) 2.23 and CalculiX GraphiX (cgx) 2.23 Installation Guide

## Reference
The binaries included here downloaded from [CalculiX Homepage](https://www.dhondt.de/calculix_2.23_4win.zip). Many thanks to the original authors (Pascal Mossier
and tetgen and glut).

The binaries were provided by:\
rafal.brzegowy@yahoo.com\
Many thanks!\
ccx_i4 - Tacus, SPOOLES, PARDISO (from dll)\
PaStiXccx_dynamic - Tacus, SPOOLES, PARDISO (from dll)\
ccx_dynamic_i8 - SPOOLES, PARDISO (from dll)\
ccx_static - Tacus, SPOOLES, PaStiX\

The dlls from Intel oneAPI MKL library are licensed under [Intel Simplified Software License](https://www.intel.com/content/www/us/en/developer/articles/license/end-user-license-agreement.html) and are hereby distributed with this package as mentioned [here](https://www.intel.com/content/www/us/en/developer/articles/tool/onemkl-license-faq.html).

The binaries of CalculiX are distributed under the GNU General Public License v3.0. Refer to the [LICENSE](LICENSE) with this package.

## Installation Guide
This package uses the original files as mentioned above and place necessary dlls to run all the variations of the ccx and cgx in the zip file.

1. Download the zip file (calculix_2.23_4win11.zip) from the [release](https://github.com/mkhan138/calculix-fea-examples/releases/tag/v1.0.0) section.

2. Unzip and place in non-system folder.

3. Search for "environment variables" and click on "Edit the system environment variables". Then click on "Environment Variables".

4. In the top half (User variables for USERNAME), double click on "Path" and click on "New".

5. Add the folder path where you unzipped the zip file (for example D:\calculix_2.23_4win11), then click "Ok" and then again "Ok".

6. Rename the desired ccx_xyz.exe and cgx_xyz.exe variant in the unzipped folder to ccx.exe and cgx.exe (for example ccx_dynamic.exe to ccx.exe and cgx_GLUT.exe to cgx.exe)

7. Now you can run the executable globally in your system.