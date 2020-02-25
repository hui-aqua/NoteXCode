# User Guide for gorina  
---  For OpenFoam and Code_Aster ---

The head node, gorina16, is open for SSH from all UiS IP-addresses, access to the other nodes are closed.  Contact [Theodor] <theo@ux.uis.no> if you need direct access to a node for some (debugging?) reason.

## 1. Login and Logout

- Login 

First login to gorina1 by using the following command and your password.
```
ssh -X [USER]@gorina1.ux.uis.no
```
Then login to gorina16 by using the following command:
```
ssh go16
```
Now, you are working in gorina16 where is supposed to run OpenFoam Simulaitons.

**Note:** If you do not have an account, you need to registre first. Please refer to:
http://wiki.ux.uis.no/foswiki/Info/UnixUserReg 

- Logout:

```
[Ctrl] + d
```

## 2. Start and stop simulations

### 2.1 Files transfer
The files transfer can be different according to your operation system.

- For linux system, you can first type the following in file explorer, and then using drag and and drop to transfer your files. 
```
sftp:// [USER]@gorina1.ux.uis.no/nfs/student/[USER]
```
**Note:** You can make a bookmark for further access. 

- For windows system, you can use [Bitvise SSH Client](https://www.bitvise.com/ssh-client-download). 
In the login section, fill the following information, and then you can transfer files through the popping out sftp window.
```
Host: gorina1.ux.uis.no

Port: 22

Username: [USER]
```

### 2.2 Preparing submit files
- Add the [submit.sh](https://github.com/chenghui62000/gorinauis/blob/master/submit.sh) script to the case folder
- Give authority for the script to be editable and executable
```chmod u+x submit.sh ```

### 2.3 Setting enviroment variables

- source OpenFOAM

Commands can be verious according to the version of OpenFOAM that you will use. The folloing are based on OpenFoam 6. 
```
source /opt/OpenFOAM/OpenFOAM-6/etc/bashrc
```

```
source /opt/OpenFOAM/.OF6x.bashrc
```
- source Code_Aster

```
source /opt/aster/etc/codeaster/profile.sh
```

### 2.4 Submit and cancel job

- Submit job ``` sbatch submit.sh```
- Cancel job ``` scancel job_id ```

## 3. Check information
- List queue ``` squeue ```

Status R means it’s running, PD means pending, i.e. that it’s waiting for available resources.
- List nodes and status ``` sinfo ```
- List jobs ``` scontrol show jobs ```
- Monitor processes ``` top ``` or ```htop```
- Cpu info ``` lscpu ```
- Memmory info ``` free -mh ```
- disk info ``` df -h ```

---

Updated 25 Feb. 2020

By Hui Cheng

hui.cheng@uis.no