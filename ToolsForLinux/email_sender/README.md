# email_sender
Monitor a file, when the file is not change with 1 min, then send a email to the target mail box.

Usage:
```buildoutcfg
python main.py [file]
```
For example:
```buildoutcfg
python main.py /home/hui/FSI/tree/log.mpirun
```
For running as background process:
```buildoutcfg
python main.py /home/hui/FSI/tree/log.mpirun > log.email &
```
