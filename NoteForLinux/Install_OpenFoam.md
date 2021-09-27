# How to install Code_Aster

(ref: [openfoamWiki](http://openfoamwiki.net/index.php/Main_Page))

## OpenFoam v2006 (v1906) (COM version)
1. Download the source code. 

2.  Change to the root user:
      ```
      sudo su
      ```

3. Source the bashrc, eg. if installed under the `~/OpenFOAM` directory

      ```
      source ~/OpenFOAM/OpenFOAM-v2006/etc/bashrc
      ```

4. Test the system readiness (optional, not supported for cross-compilation)

      ```shell
      foamSystemCheck
      ```

5. Compile OpenFOAM

      ```shell
      ./Allwmake -s -l
      ./Allwmake -j -s -q -l
      ./Allwmake -j 4 > log.make 2>&1
      ```
6. Test the Openfoam, Create the user `run` directory:

      ```
      mkdir -p $FOAM_RUN
      ```
    Then, run with a simple tutorial:

      ```
      run
      cp -r $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily ./
      cd pitzDaily
      blockMesh
      simpleFoam
      ```
## OpenFoam7 (6)  (ORG version)

1. Add source:

   ```shell
   sudo sh -c "wget -O - https://dl.openfoam.org/gpg.key | apt-key add -"
   sudo add-apt-repository http://dl.openfoam.org/ubuntu
   ```

2. update 

   ```shell
   sudo apt-get update
   ```

3. Install

   ```shell
   sudo apt-get -y install openfoam7
   ```

4. User Configuration

   add the following to the end of  the file "~/.bashrc"

   ```
   alias of7="source /opt/openfoam7/etc/bashrc"
   ```



## OpenFoam5.x

```
sudo apt install libfl-dev libglu1-mesa-dev libqt4-opengl-dev
```



Finish!