# Note for Linux
 A note for a brand new Linux system.


## Suggestion for the Linux system:

1. Install Linux system (ref: [wikiHow](https://zh.wikihow.com/%E5%AE%89%E8%A3%85Ubuntu-Linux))

   1. Download system ISO image. Recommend [Linux Mint (20.3)](https://linuxmint.com/edition.php?id=294) and [Ubuntu Focal](https://releases.ubuntu.com/focal/).
   2. Creat bottable USB drive (Disk >=4 GB).  Recommend [Rufus](https://rufus.ie/en/) maand [Universal USB Installer](https://www.pendrivelinux.com/universal-usb-installer-easy-as-1-2-3/).
   
   3. Restart the computer and install the new linux system.
   >Suggestions for the system installation:\
   >   swap=16+GB \
   >   /boot=2+GB\
   >   /=100+GB \
   >   /home=2TB+

   

2. Log in and Update and upgrade. Select the fastest software source, then use the following commands: 

   ```shell
   sudo apt-get update
   sudo apt-get upgrade
   ```
   
3. Check the video card

   Usually, no problems.

4. Install small useful tools

   ```shell
   sudo apt-get install tmux conky python3 kazam python3-numpy vim git python-pip python3-pip python3-matplotlib htop tree
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

   

5. Install [salome_meca](https://code-aster.org/V2/spip.php?article303). Recommend version 2020.0.1.
   1. Download from the website and unzip the package.\
      ```
      tar -xvf salome_meca-2020.0.1-1-universal.tgz
      ```
   2. Install using the following command:
      ```
      sudo ./salome_meca-2020.0.1-1-universal.run
      ```
      Install in the directory: /opt/salome2020 

6. Install Code_aster 14.6
   1. Install prerequiesites
   ```
   sudo apt-get install gcc g++ gfortran cmake python3 python3-dev python3-numpy tk bison flex liblapack-dev libblas-dev libboost-python-dev libboost-numpy-dev zlib1g-dev xterm nedit ddd xemacs21 kwrite gedit gnome-terminal 
   ```

   Download from the Office website Unzip the package

   ```
   tar -xvf aster-full-src-14.6.0-1.noarch.tar.gz.tar.gz`
   ```


7. Install OpenFOAM 2012
   Download [OpenFoam](https://dl.openfoam.com/source/v2012/ThirdParty-v2012.tgz) and [ThirdParty](https://dl.openfoam.com/source/v2012/OpenFOAM-v2012.tgz).
   


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
   alias of2006='source /opt/openfoam/OpenFOAM-v2006/etc/bashrc'
   alias of1812='source /opt/openfoam/OpenFOAM-v1812/etc/bashrc'
   alias of301='source /opt/OpenFOAM/OpenFOAM-3.0.1/etc/bashrc'
   alias of240='source /opt/OpenFOAM/OpenFOAM-2.4.0/etc/bashrc'
   alias ofe40='source /opt/foam/foam-extend-4.0/etc/bashrc'
   alias ofe41='source /opt/foam/foam-extend-4.1/etc/bashrc'

   alias of6='source /opt/openfoam6/etc/bashrc'

   alias aster='source /opt/aster/etc/codeaster/profile.sh'
   alias aster144='source /opt/aster144/etc/codeaster/profile.sh'
   alias aqua='source /home/hui/GitCode/Code_Aster/hydromodel/etc/aliases.sh'
   ```