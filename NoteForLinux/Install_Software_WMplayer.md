# How to install VMware Workstation Player on Windows 10

(ref: [VMware - Official Site](https://www.vmware.com))

Go to downloads and select Open Source. Scroll down to Desktop & End-User Computing and select VMware Player.

Download VMware Workstation Player 15.5.6.

After the file is downloaded, restart your computer and open your from downloads:
    ```
    VMware-player-15.5.6.exe
    ```

Proceed with the guidelines given:

1. Accept the terms in the Licence Agreement
2. Mark the Enchanced Keyboard Driver
3. Press install and finish.


Wmware-player installation complete!


## How to install Linux system on Vmware-player(need to enable VT-x from BIOS)

(ref: [LINUX.org](https://www.linux.org/pages/download/))

From the link, download your preferred linux system. In this case Linux Mint is used. 

1. VMware - setup

After downloading, open your WMware-player. 
* Select the `Create a New Virtual Machine` option
* Select `Custom (advanced)` type configuration
* Select `I will install the operating system later`
* Select a Guest operating System :`Linux` and Version `Ubuntu 64-bit`
* Name your Virtual machine (Linux Mint) and select it`s location
* Maximize number of processors and storage
* Create a new virtual disk
* Store virtual disk as a single file
* In processors select `Virtualize Intel VT -x/EPT`
* In `New CD/DVD (SATA)` select `Use ISO image file` and open with your `linuxmint.iso` disk
* Press `Finish` 

 Your Linux Mint should now be ready, you can test by running it using `Power on this virtual machine` 

 2. Linux Mint - setup

 * Select `Start Linux Mint` in the startup window
 * On the desktop press the `Install Linux Mint` disc
 * Installation type: `Erase disk and install Linux Mint

After some minutes, a window saying installation has finished should pop up. Press `Restart Now` 

Linux Mint installation complete!




## How to install OpenFOAM on ubuntu

(ref: [The OpenFOAM Foundation](http:www.openfoam.org))

Go to downloads select OpenFOAM v8.

OpenFOAM can be simply installed for the first time using the `apt` package management tool. 

1. `Copy and paste` the following in a terminal prompt:

    ```
    sudo sh -c "wget -O - https://dl.openfoam.org/gpg.key | apt-key add -"

    sudo add-apt-repository http://dl.openfoam.org/ubuntu
    ```

2. Update the `apt` package list to account the new download repository location:
    ```
    sudo apt-get update
    ```
3. Install OpenFOAM:
    ```
    sudo apt-get -y install openfoam6

    ```

OpenFOAM 6 and ParaView 5.6.0 are now installed in the /opt directory.

After the installation, add the following to the end of  the file "~/.bashrc":
```
alias of6="source /opt/openfoam6/etc/bashrc"
```

OpenFOAM installation complete!

## How to install Code_Aster

(ref: [code-aster.org](https://www.code-aster.org/spip.php?rubrique2))

In order to install Code_Aster you need to install certain prerequisites by inserting the following in a terminal prompt:
```shell
sudo apt-get install gcc g++ gfortran cmake python3 python3-dev python3-numpy tk tcl bison flex liblapack-dev libblas-dev libopenblas-dev libboost-python-dev libboost-numpy-dev zlib1g-dev nedit geany vim ddd
    
sudo apt-get install checkinstall openmpi-bin libx11-dev grace gettext libboost-all-dev swig libsuperlu-dev
```

You can check if the prerequisites are installed by using `synaptic` and search for a specific:
```shell
sudo synaptic
```
If the colour is green in the box, the software is installed. If not, you can mark the box and press `Apply`.

When all the prerequisites are installed you can proceed with the installation of Code_Aster.



1. Installation of Code_Aster

From main menu, press `DOWNLOAD` and select Code_Aster. For non-commercial usage you should select the `stable` version.

Code_Aster is installed by inserting:

``` 
sudo python3 setup.py install --prefix=/opt/aster144
```

2. After the build complete, to make host file for parallel calculation. (Write the description to the mpi_hostfile):
   
```
echo "$HOSTNAME cpu=$(cat /proc/cpuinfo | grep processor | wc -l)" > /opt/aster/etc/codeaster/mpi_hostfile
```
add the following to the end of  the file "~/.bashrc"

After the installation, add the following to the end of  the file "~/.bashrc":
```
alias aster144="source /opt/aster144/etc/bashrc"
```
Code_Aster installation complete!

## How to install Salome-Meca

(ref: [code-aster.org](https://www.code-aster.org/spip.php?rubrique2))

1. Installation

From main menu, press `DOWNLOAD` and select Salome-Meca. 
* Uncompress the file and launch the install:
```
tar xvf Salome-Meca-2017.0.2-LGPL-2.tgz && ./Salome-Meca-2017.0.2-LGPL-2.run
```

Select language `English/French` and proceed. 

To launch Salome-Meca:
```
cd appli_V2017.0.2
./salome
```

Salome-Meca installation complete!














