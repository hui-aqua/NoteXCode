# Note for Linux

 A note for a brand new Linux system.

## Suggestion for the Linux system

### 1. Install Linux system (ref: [wikiHow](https://zh.wikihow.com/%E5%AE%89%E8%A3%85Ubuntu-Linux))

Download the system ISO image. Recommend [Linux Mint (20.3)](https://linuxmint.com/edition.php?id=294) and [Ubuntu 20.04.6 LTS (Focal Fossa)](https://releases.ubuntu.com/focal/).
   2. Create a bootable USB drive (Disk >=4 GB).  Recommend [Rufus](https://rufus.ie/en/) and [Universal USB Installer](https://www.pendrivelinux.com/universal-usb-installer-easy-as-1-2-3/).

   3. Restart the computer and install the new Linux system. Suggestions for the system installation:
      >   swap=16+GB \
      >   /boot=2+GB\
      >   /=100+GB \
      >   /home=2TB+

### 2. Log in and Update and upgrade. Select the fastest software source, then use the following commands

   ```shell
   sudo apt-get update
   sudo apt-get upgrade
   ```

### 3. Check the video card

   Usually, no problems.

### 4. Install small useful tools

   ```shell
   sudo apt-get install vlc tmux python python3 python3-numpy vim git python3-matplotlib htop tree pip openmpi-bin libfl-dev 
   ```

   Some of the tools have to be installed manually: [VSCode](https://code.visualstudio.com/download), [Chrome](https://www.google.com/chrome/?platform=linux), [Blender](https://www.blender.org/download/), [Typora](https://typora.io/#linux), [Teamviewer](https://www.teamviewer.com/en/download/linux/)

### 5. Install salome_meca. Recommend version 2020.0.1

   **NOTE** Before the installation verify that when you lunch `python` in a terminal, it is <font color="red">Python2</font>

   1. Download [salome_meca](https://code-aster.org/V2/spip.php?article303) from the website and unzip the package.

      ``` shell
      tar -xvf salome_meca-2020.0.1-1-universal.tgz
      ```

   2. Install using the following command:

      ``` shell
      sudo ./salome_meca-2020.0.1-1-universal.run
      ```

      Install in the directory: /opt/salome2020

   <details>
   <summary>Issue about openGL</summary>
   The FATAL ERROR message is ```OpenGl_Window::CreateWindow: glXCreateContext failed.``` This issue can be fixed by:

   ``` shell
   cd opt/salome2020/V2019.0.3_universal/prerequisites/debianForSalome/lib
   sudo rm libstdc++.so.6.0
   sudo ln -s /usr/lib/x86_64-linux-gnu/libstdc++.so.6 libstdc++.so.6
   ```

   </details>


   <details>
   <summary>Issue about libffi.so.6:</summary>
   The FATAL ERROR message is 

   ``` shell
   ........
   File "/opt/salome2020/V2020.0.1_universal_universal/prerequisites/Python-365/lib/python3.6/ctypes/__init__.py", line 7, in <module>
   from _ctypes import Union, Structure, Array
   ImportError: libffi.so.6: cannot open shared object file: No such file or directory
   ``` 

   This issue can be fixed by:

   ``` shell
   cd opt/salome2020/V2019.0.3_universal/prerequisites/debianForSalome/lib
   sudo apt install libffi7
   sudo rm libffi.so.6
   ln -s /usr/lib/x86_64-linux-gnu/libffi.so.7 libffi.so.6              
   ```

   </details>

### 6. Install Code_aster 14.6

   1. Download [code aster stable version 14.6.0](https://code-aster.org/FICHIERS/aster-full-src-14.6.0-1.noarch.tar.gz) from the Office website Unzip the package

      ``` shell
      tar -xvf aster-full-src-14.6.0-1.noarch.tar.gz.tar.gz
      ```

   2. Install prerequisites

      ```shell
      sudo apt-get install gcc g++ gfortran cmake python3 python3-dev python3-numpy tk bison flex liblapack-dev libblas-dev libboost-python-dev libboost-numpy-dev zlib1g-dev xterm nedit ddd xemacs21 kwrite gedit gnome-terminal && pip install numpy setuptools matplotlib
      ```

      **NOTE**: If it raises some problem about "blas", please make sure the libopenblas-base libopenblas-dev is not instlled with libblas-dev at the same time.

   3. Install the main program, using the following command in the `aster-full-src-14.6.0` folder

      ```shell
      sudo python3 setup.py install --prefix=/opt/aster146
      ```

   4. Get alias command add the following to the `~`/.bashrc` file, so that you can enter the Code_Aster environment and run simulations easily. **Now, the installation for the series version is finished.**

      ```shell
      alias aster='source /opt/aster146/etc/codeaster/profile.sh'
      ```

   5. **NOTE**: you can test your installation with the following command:

      ```shell
      /opt/aster146/bin/as_run --test sdnl142a
      ```

### 7. Install OpenFOAM 2012

   1. Download openfoam main program and third party from  [OpenFoam](https://dl.openfoam.com/source/v2012/OpenFOAM-v2012.tgz) and [ThirdParty](https://dl.openfoam.com/source/v2012/ThirdParty-v2012.tgz).
   2. Fellow [OpenFOAM® Quick Build Guide](https://develop.openfoam.com/Development/openfoam/-/blob/master/doc/Build.md) and build the source code. I prefer to install in `/opt` with ```sudo su```.


   3. Move the `ThirdParty-v2012.tgz` and `OpenFOAM-v2012.tgz` to `/opt/openfoam` folder with root admin right.
   4. Unzip the package and source the environment under the `/opt/openfoam/OpenFOAM-v2012` folder using:

      ```shell
      source etc/bashrc
      ```

   5. Test the system readiness (optional, not supported for cross-compilation)

      ```shell
      foamSystemCheck 
      ```

   6. Compile OpenFOAM

      ```shell
      ./Allwmake -j -s -q -l
      ```

   7. Post-compilation steps

      ```shell
      foamInstallationTest
      ```
   For other version and more useful tips please find [here](OpenFoam.md)

## Useful tips

1. Right click meum
    - For Linux Mint (only for [Cinnamon edition](https://linuxmint.com/edition.php?id=274) )

      ```shell
      vi ~/.local/share/nemo/action/vscode.nemo_action
      ```

      Then add the following to the file:

      ```shell
      [Nemo Action]
      Name=Open in VS Code
      Comment=Open in VS Code
      Exec=code %F
      Icon-Name=com.visualstudio.code
      Selection=Any
      Extensions=dir;
      ```

2. Bashrc file:

   ```shell
   alias of7='source /opt/openfoam7/etc/bashrc'
   alias of1906='source /opt/openfoam/OpenFOAM-v1906/etc/bashrc'
   alias of2012='source /opt/openfoam/OpenFOAM-v2012/etc/bashrc'
   alias of1812='source /opt/openfoam/OpenFOAM-v1812/etc/bashrc'
   alias of301='source /opt/OpenFOAM/OpenFOAM-3.0.1/etc/bashrc'
   alias of240='source /opt/OpenFOAM/OpenFOAM-2.4.0/etc/bashrc'
   alias ofe40='source /opt/foam/foam-extend-4.0/etc/bashrc'
   alias ofe41='source /opt/foam/foam-extend-4.1/etc/bashrc'
   alias of6='source /opt/openfoam6/etc/bashrc'

   alias aster='source /opt/aster146/etc/codeaster/profile.sh'
   alias salome2020='/opt/salome2020/appli_V2020.0.1_universal_universal/salome &'
   ```
