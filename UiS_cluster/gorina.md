# User Guide for gorina  
---  For OpenFoam and Code_Aster ---

## Brief info

This manage system for Gorina cluster uses Slurm, all jobs must be startet with Slurm !
```
 Slurm head node .....: gorina11
 Slurm working nodes .: gorina11-38
```
* Slurm commands
 
```
    List nodes and status: sinfo
    List jobs ...........: scontrol show jobs
    List queue ..........: squeue
    Simple test .........: srun -p cpu20 -N3 /bin/hostname
    Cancel job ..........: scancel job
    Command shell .......: srun -p cpu20 --pty $SHELL
    Requesting two GPU ..: srun -p gpuA100 --gres=gpu:2
```
* Slurm partitions (All nodes have 256 Gbyte of memory.):

```
  cpu36 =  8 nodes with 36 cpu cores @ 2.1GHz, job max runtime is one week
  cpu28 =  2 nodes with 28 cpu cores @ 1.7GHz, job max runtime is one day
  cpu20 = 18 nodes with 20 cpu cores @ 2.4GHz, job max runtime is two weeks
```


**!!! IMPORTANT !!!**

 All jobs *must* be started from your ```/bhome/..``` (or your ```/local/home```).
 This is very important if you run OpenFOAM or if your jobs do a lot of
 file read or write, or creates big files.  If unsure about how much IO
 your job will do, then use ```/bhome```.

 Do *NOT* just run from your HOME, your jobs won't run as fast as they
 could, and they will bog down the /home file server for all of us... 

 Jobs causing heavy load on the ```/home``` file server will be terminated
 without warning...


**Note** Contact [Theodor] <theo@ux.uis.no> if you need direct access to a node for some (debugging?) reason.

## [Quick start guide](Quickstart.md)
## [Job submit script](submitshell/README.MD)

