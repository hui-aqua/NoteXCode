# Note for Linux
 A note for a brand new Linux system.


## Suggestion for the Linux system:

### 1. Install Linux system (ref: [wikiHow](https://zh.wikihow.com/%E5%AE%89%E8%A3%85Ubuntu-Linux))

   1. Download system ISO image. Recommend [Linux Mint (20.3)](https://linuxmint.com/edition.php?id=294) and [Ubuntu Focal](https://releases.ubuntu.com/focal/).
   2. Creat bottable USB drive (Disk >=4 GB).  Recommend [Rufus](https://rufus.ie/en/) maand [Universal USB Installer](https://www.pendrivelinux.com/universal-usb-installer-easy-as-1-2-3/).
   
   3. Restart the computer and install the new linux system.
   >Suggestions for the system installation:\
   >   swap=16+GB \
   >   /boot=2+GB\
   >   /=100+GB \
   >   /home=2TB+

   

### 2. Log in and Update and upgrade. Select the fastest software source, then use the following commands: 

   ```shell
   sudo apt-get update
   sudo apt-get upgrade
   ```
   
### 3. Check the video card

   Usually, no problems.

### 4. Install small useful tools

   ```shell
   sudo apt-get install tmux conky python3 kazam python3-numpy vim git python3-matplotlib htop tree pip openmpi-bin
   ```  

   Some of the tools has to be installed manually.

   - Sublime
   - VSCode
   - Chrome
   - Blender
   - Typora
   - VLC player
   - Kazam
   - Teamviewer

   

### 5. Install [salome_meca](https://code-aster.org/V2/spip.php?article303). Recommend version 2020.0.1.
   1. Download from the website and unzip the package.
      ```
      tar -xvf salome_meca-2020.0.1-1-universal.tgz
      ```
   2. Install using the following command:
      ```
      sudo ./salome_meca-2020.0.1-1-universal.run
      ```
      Install in the directory: /opt/salome2020 

### 6. Install Code_aster 14.6
   1. Download [code aster stable version 14.6.0](https://code-aster.org/FICHIERS/aster-full-src-14.6.0-1.noarch.tar.gz) from the Office website Unzip the package

      ```
      tar -xvf aster-full-src-14.6.0-1.noarch.tar.gz.tar.gz`
      ```

   2. Install prerequiesites
      ```
      sudo apt-get install gcc g++ gfortran cmake python3 python3-dev python3-numpy tk bison flex liblapack-dev libblas-dev libboost-python-dev libboost-numpy-dev zlib1g-dev xterm nedit ddd xemacs21 kwrite gedit gnome-terminal && pip install numpy setuptools matplotlib
      ```
      **NOTE**: If it raise some problem about "blas", please make sure the libopenblas-base libopenblas-dev is not instlled with libblas-dev at the same time.

   3. Install the main program, using the following command in the `aster-full-src-14.6.0` folder
      ```
      sudo python3 setup.py install --prefix=/opt/aster
      ``` 
   4. Get alias command Add the following to the `~/.bashrc` file, so that you can enter the Code_Aster enviroment and run simulations easily. **Now, the installation for the series version is finished.**
      ```
      alias aster='source /opt/aster/etc/codeaster/profile.sh'
      ```
   5. **NOTE**:you can test your installnation with the following command:
      ```
      /opt/aster/bin/as_run --test sdnl142a
      ```
   

### 7. Install OpenFOAM 2012
   1. Download openfoam main program and third party from  [OpenFoam](https://dl.openfoam.com/source/v2012/OpenFOAM-v2012.tgz) and [ThirdParty](https://dl.openfoam.com/source/v2012/ThirdParty-v2012.tgz).
   2. Fellow [OpenFOAM® Quick Build Guide](https://develop.openfoam.com/Development/openfoam/-/blob/master/doc/Build.md) and build the source code. The main steps in the build guide are summarized as:
   3. Move the `ThirdParty-v2012.tgz` and `OpenFOAM-v2012.tgz` to `/opt/openfoam` folder with root admin right.
   4. Unzip the package and source the environment using:
      ```
      source ~/openfoam/OpenFOAM-v2012/etc/bashrc
      ```
   5. Test the system readiness (optional, not supported for cross-compilation) 
      ```
      foamSystemCheck 
      ```
   6. Compile OpenFOAM
      ```
      ./Allwmake -j -s -q -l
      ```
   7. Post-compilation steps
      ```
      foamInstallationTest
      ```



## Useful tips 
1.  Right click meum
    - For Linux Mint
      
      ```
      vi ~/.local/share/nemo/action/vscode.nemo_action
      ```
      Then add the following to the file:
      ```
      [Nemo Action]
      Name=Open in VS Code
      Comment=Open in VS Code
      Exec=code %F
      Icon-Name=com.visualstudio.code
      Selection=Any
      Extensions=dir;
      ```



2. Bashrc file:
   ```
   alias of7='source /opt/openfoam7/etc/bashrc'
   alias of1906='source /opt/openfoam/OpenFOAM-v1906/etc/bashrc'
   alias of2012='source /opt/openfoam/OpenFOAM-v2012/etc/bashrc'
   alias of1812='source /opt/openfoam/OpenFOAM-v1812/etc/bashrc'
   alias of301='source /opt/OpenFOAM/OpenFOAM-3.0.1/etc/bashrc'
   alias of240='source /opt/OpenFOAM/OpenFOAM-2.4.0/etc/bashrc'
   alias ofe40='source /opt/foam/foam-extend-4.0/etc/bashrc'
   alias ofe41='source /opt/foam/foam-extend-4.1/etc/bashrc'
   alias of6='source /opt/openfoam6/etc/bashrc'

   alias aster='source /opt/aster/etc/codeaster/profile.sh'
   alias aqua='source /home/hui/GitCode/Code_Aster/hydromodel/etc/aliases.sh'
   ```