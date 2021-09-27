# Note for Linux
 A note for the new Linux system.


## Suggestion for the Linux system:

1. Install Linux system (ref: [wikiHow](https://zh.wikihow.com/%E5%AE%89%E8%A3%85Ubuntu-Linux))

   1. Download system image, e.g., [Ubuntu](https://ubuntu.com/), [Linux Mint (19.3)]
   2. Download [Universal USB Installer](https://www.pendrivelinux.com/universal-usb-installer-easy-as-1-2-3/)
   3. Make a USB installer (Disk >3GB)

   Suggestions for the system installation:

   1. swap=16+GB
   2. /boot=2+GB
   3. /=100+GB
   4. /home=2TB+

   

2. Update and upgrade

   ```shell
   sudo apt-get update
   sudo apt-get upgrade
   ```
   
3. Check the video card

   Usually, no problems.

4. Install small useful tools

   ```shell
   sudo apt-get install tmux conky python3 kazam python3-numpy vim git python-pip python3-pip python3-matplotlib
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

   

5. Install scientific software
   - pycharm
   - clion
   - paraview
   - [openfoam (6, 2006, 1906)](./Install_OpenFoam.md)
   - [code_aster](./Install_code_aster.md) 
   - salome_meca (*note* if it can not open AsterStudy try to open salome_meca use the following comman and see the outcome in terminal:
  ```sudo /opt/salome_meca/appli_V2019.0.3_universal/salome ``` )


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