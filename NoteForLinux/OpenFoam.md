# How to install OpenFOAM

(ref: [openfoamWiki](http://openfoamwiki.net/index.php/Main_Page))

## OpenFoam v2006 (v1906) (.com version)
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



## Useful function and tips
1. Search through the turbulenceProperties file in foam tutorials folder, to find one containing the expression kepsilon (case insensitive) :
      ```shell
      find $FOAM_TUTORIALS -name "turbulenceProperties" | xargs grep -l -i kepsilon
      ```

2. Remove all the timeserises data (folders), a quick way to delete all previous timesteps:
      ```shell
      foamListTimes -rm
      ```
3. A pseudo way to reconstruct case on slurm cluster:
      ``` bash
      #SBATCH -J recinstru
      #SBATCH -p cpu20
      #SBATCH --array=0-19
      #SBATCH -o output_%j.out
      #SBATCH -e errors_%j.err

      NUM=$SLURM_ARRAY_TASK_ID

      source /opt/OpenFOAM/.OF2012.bashrc
      # Source tutorial run functions
      . $WM_PROJECT_DIR/bin/tools/RunFunctions
      t_end=1600
      duration=$t_end/20  # 80

      reconstructPar -time $(($NUM*80)):$(($NUM*80+80)) >log.reconstructPar$NUM
      ```
