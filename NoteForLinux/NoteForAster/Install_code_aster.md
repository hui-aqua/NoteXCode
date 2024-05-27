# How to install Code_Aster

**Note**: Most of the time, Code_Aster is installed with the series way on a computer. 

---

## Install series version
This is a note of the work on linux Mint 19.3
Ref1: ([code_Aster official website](https://www.code-aster.org/spip.php?article272))

### 1. Download the package
Download from the [Office website](https://code-aster.org/V2/spip.php?article272)
Unzip the package 

```
tar -xvf aster-xxxxx.tar.gz
```
**NOTE**: according to my tests, Code_Aster 14.4 is quite unstable for Non-linear dynamic simulations. Thus, I recommond Code_Aster 14.2.

### 2. Install prerequiesites

``` shell
sudo apt-get install gcc g++ gfortran cmake python3 python3-dev python3-numpy tk bison flex liblapack-dev libblas-dev libboost-python-dev libboost-numpy-dev zlib1g-dev xterm nedit ddd xemacs21 kwrite gedit gnome-terminal
```
### 2.1 install python module
We suggest install pip and pip3 first.
```shell
   pip install numpy setuptools matplotlib
```
**NOTE:** If it raise some problem about "blas", please make sure the ```libopenblas-base libopenblas-dev``` is not instlled with ```libblas-dev``` at the same time. 

### 3. Install the main program
   Then Install Code_Aster:	
   ``` shell
   sudo python setup.py install --prefix=/opt/aster
   ```
### 4. Great alias command
 Add the following to the ~/.bashrc, so that you can enter the Code_Aster enviroment and run simulations easily. 

   ``` shell
   alias aster='source /opt/aster/etc/codeaster/profile.sh'
   ```

**Now, the installation for the series version is finished.**

**NOTE:** you can test your installnation with the following command:

```shell
/opt/aster/bin/as_run --test sdnl142a
```


---

## Install parallel version
This is a note of the work to build parallel version on linux Mint 19.3

Ref1: ([A Blog by a Jananese](https://hitoricae.com/2020/05/16/installation-code_aster14-4-to-xubuntu20-04/))

Ref2:([code_aster 14.4 parallel version with PETSc](https://hitoricae.com/2019/11/10/code_aster-14-4-with-petsc/))

Ref3: ([parallel version based on CA14.2](https://code-aster.it/2019/01/12/code_aster-14-2-in-parallelo-su-ubuntu-bionic/))

ref4: https://qiita.com/hiro_kuramoto/items/269ecf6293cfbe38b314

Third-party libraries:

OpenBLAS

ScaLAPACK

Parmetis

Scotch

MUMPS

PETSC





### 1. Install prerequisites

Copy and past the following command to a terminal in order to install these prerequieites.

``` shell
sudo apt-get install gcc g++ gfortran cmake python3 python3-dev python3-numpy tk tcl bison flex liblapack-dev libblas-dev libopenblas-dev libboost-python-dev libboost-numpy-dev zlib1g-dev nedit geany vim ddd

sudo apt-get install checkinstall openmpi-bin libx11-dev grace gettext libboost-all-dev swig libsuperlu-dev
```

****



```shell
$ sudo apt install gfortran g++ python-dev python-numpy liblapack-dev libblas-dev tcl tk zlib1g-dev bison flex checkinstall openmpi-bin libx11-dev cmake grace gettext libboost-all-dev swig libsuperlu-dev
```

### 2. Download and install OpenBLAS 0.2.20

Official website for [OpenBLAS](https://www.openblas.net/)  . The newest version is 0.3.10

```shell
tar xfvz OpenBLAS-0.2.20.tar.gz
cd OpenBLAS-0.2.20
make NO_AFFINITY=1 USE_OPENMP=1
make PREFIX=/opt/OpenBLAS install
```

add openblas to the search path of the shared library.:

```shell
# install the openblas in /opt f
echo /opt/OpenBLAS/lib | sudo tee -a /etc/ld.so.conf.d/openblas.conf 
# this is to write the path to the openblas.conf file
sudo ldconfig
```



### 3. Configure the Code_Aster and install



```shell
sed -i "s:PREFER_COMPILER\ =\ 'GNU':PREFER_COMPILER\ =\'GNU_without_MATH'\nMATHLIB=\ '/opt/OpenBLAS/lib/libopenblas.a':g" setup.cfg
```

The above command is to change the compiler in file "setup.cfg", line 37:

```python
PREFER_COMPILER = 'GNU'
```

to

```python
PREFER_COMPILER = 'GNU_without_MATH'
MATHLIB='/opt/OpenBLAS/lib/libopenblas.a'
```
Then Install Code_Aster:	

``` shell
python3 setup.py install --prefix=~/aster146Parallel
```

In my environment, it seemed to occur when numpy was already installed using pip.
In that case, delete numpy completely with ⇒ `pip3 uninstall numpy`, Then reinstall numpy  with ⇒   `sudo apt install python-numpy`, after that, try to install Code_Aster again. 



After the build complete, to make host file for parallel calculation. (Write the description to the mpi_hostfile)

```shell
echo "$HOSTNAME cpu=$(cat /proc/cpuinfo | grep processor | wc -l)" > ~/aster146Parallel/etc/codeaster/mpi_hostfile 
```

```shell
sudo echo "$HOSTNAME cpu=$(cat /proc/cpuinfo | grep processor | wc -l)" > /opt/aster/etc/codeaster/mpi_hostfile 
```

### 4. ScaLAPACK 2.0.2  [offical website](http://www.netlib.org/scalapack/)

This step is a little tricky.

First download scalapack installer from [here](http://www.netlib.org/scalapack/scalapack_installer.tgz). Then unzip it and try to run the following command in terminal:

```shell
tar xfvz scalapack_installer.tgz
cd scalapack_installer
sudo ./setup.py --lapacklib=/opt/OpenBLAS/lib/libopenblas.a --mpicc=mpicc --mpif90=mpif90 --mpiincdir=/usr/lib/x86_64-linux-gnu/openmpi/include --ldflags_c=-fopenmp --ldflags_fc=-fopenmp --prefix=/opt/scalapack-n

```

Usually, you will get a error message for that cannot find the scalpack file

 ```IOError: [Errno 2] No such file or directory: 'download/./scalapack.tgz'```

You need to download the scalapack 2.0.0 from the official website and rename it to scalapack.tgz , Then move this file to ./build/download

Now you can run the last step again.

```shell
sudo ./setup.py --lapacklib=/opt/OpenBLAS/lib/libopenblas.a --mpicc=mpicc --mpif90=mpif90 --mpiincdir=/usr/lib/x86_64-linux-gnu/openmpi/include --ldflags_c=-fopenmp --ldflags_fc=-fopenmp --prefix=/opt/scalapack-n
```

In the end, you will find that:

```
BLACS: error running BLACS test routines xCbtest
BLACS: Command  -np 4 ./xCbtest
stderr:
**************************************
/bin/sh: 1: -np: not found
**************************************
```

but it is successful if the file /opt/scalapack/lib/libscalapack.a is created.

### 5. Parmetis 4.0.3

First, unzip it.

```
cd ..
tar xvzf parmetis-4.0.3.tar.gz 
cd parmetis-4.0.3
```

Next, rewrite a part of the file of metis / include / metis.h and change it to compile in 64bit mode. (line 33)

```shell
sed -i -e 's/#define IDXTYPEWIDTH 32/#define IDXTYPEWIDTH 64/' metis/include/metis.h
```

Install it with:

```shell
make config prefix=/opt/parmetis-4.0.3 
make
sudo make install
```

Next, let's check the operation.

```shell
cd Graphs
mpirun -np 4 /opt/parmetis-4.0.3/bin/parmetis rotor.graph 1 6 1 1 6 1
```

If there are no errors, it is successful.

My output is :

```shell
reading file: rotor.graph
finished reading file: rotor.graph
[ 99617  1324862 24904 24905] [150] [ 0.000] [ 0.000]
[ 53043   786820 13086 13479] [150] [ 0.000] [ 0.000]
[ 28227   423280  6930  7105] [150] [ 0.000] [ 0.000]
[ 15247   229550  3789  3843] [150] [ 0.000] [ 0.000]
[  8304   124178  2044  2121] [150] [ 0.000] [ 0.000]
[  4617    67768  1123  1170] [150] [ 0.000] [ 0.000]
[  2625    36962   643   685] [150] [ 0.000] [ 0.001]
[  1545    20152   360   408] [150] [ 0.000] [ 0.001]
[   944    11180   221   252] [150] [ 0.000] [ 0.002]
[   609     6230   131   161] [150] [ 0.000] [ 0.005]
[   411     3612    78   116] [150] [ 0.000] [ 0.009]
[   347     2916    72   100] [150] [ 0.000] [ 0.009]
nvtxs:        347, cut:    24723, balance: 1.023 
nvtxs:        411, cut:    22942, balance: 1.050 
nvtxs:        609, cut:    22082, balance: 1.044 
nvtxs:        944, cut:    20501, balance: 1.054 
nvtxs:       1545, cut:    19350, balance: 1.052 
nvtxs:       2625, cut:    18147, balance: 1.049 
nvtxs:       4617, cut:    16956, balance: 1.051 
nvtxs:       8304, cut:    15689, balance: 1.049 
nvtxs:      15247, cut:    14632, balance: 1.049 
nvtxs:      28227, cut:    13468, balance: 1.050 
nvtxs:      53043, cut:    12628, balance: 1.048 
nvtxs:      99617, cut:    11288, balance: 1.047 
Final   6-way Cut:  11288       Balance: 1.047 
```



### 6. Scotch

First, move scotch-6.0.4-aster7.tar.gz included in / aster-full-src-14.6.0 / SRC and unzip it.

```shell
tar xvzf scotch-6.0.4-aster7.tar.gz
cd scotch-6.0.4/src
```

Next, edit Makefile.inc contained in src / as follows.

```makefile
EXE     =
LIB     = .a
OBJ     = .o

MAKE    = make
AR      = ar
ARFLAGS = -ruv
CAT     = cat
CCS     = gcc
CCP     = mpicc
CCD     = gcc
CFLAGS  = -O3 -fPIC -DINTSIZE64 -DCOMMON_FILE_COMPRESS_GZ -DCOMMON_PTHREAD -DCOMMON_RANDOM_FIXED_SEED -DSCOTCH_RENAME -DSCOTCH_RENAME_PARSER -Drestrict=__restrict
CLIBFLAGS   =
LDFLAGS = -fPIC -lz -lm -pthread -lrt
CP      = cp
LEX     = flex -Pscotchyy -olex.yy.c
LN      = ln
MKDIR   = mkdir
MV      = mv
RANLIB  = ranlib
YACC    = bison -pscotchyy -y -b y 
```



Build and check the operation. (**note:** The make command is executed in /src folder)

```shell
make scotch esmumps ptscotch ptesmumps CCD=mpicc
make check
make ptcheck
```



### 7. MUMPS

Again, move mumps-5.1.2-aster6.tar.gz from ~ / software / aster-full-src-14.4.0 / SRC to /opt and unzip it.

```
$ cp ~/software/aster-full-src-14.4.0/SRC/mumps-5.1.2-aster6.tar.gz /opt
$ cd /opt
$ tar xvzf mumps-5.1.2-aster6.tar.gz
$ cd mumps-5.1.2
```

Edit Makefile.inc to suit your environment.
The base file is prepared in the Makefile.inc / directory, so copy it.

```
$　cp Make.inc/Makefile.debian.PAR ./Makefile.inc
```

Modify the library specifications etc. according to the environment.



```makefile
#  This file is part of MUMPS 5.1.2, released
#  on Mon Oct  2 07:37:01 UTC 2017
# These settings for a PC under Debian/linux with standard packages :
# metis (parmetis), scotch (ptscotch), openmpi, gfortran
# packages installation : 
# apt-get install libmetis-dev libparmetis-dev libscotch-dev libptscotch-dev libatlas-base-dev openmpi-bin libopenmpi-dev lapack-dev

# Begin orderings
LSCOTCHDIR = /opt/scotch-6.0.4/lib/
ISCOTCH    = -I/opt/aster/public/metis-5.1.0/include -I/opt/parmetis-4.0.3/include -I/opt/scotch-6.0.4/include
LSCOTCH   = -L$(LSCOTCHDIR)  -Lptesmumps  -lptscotch  -lscotch  -lptscotcherr  -lptscotcherrexit  -lptscotchparmetis
 
LPORDDIR =  $ ( topdir ) / door / lib / 
IPORD     =  -I $ ( topdir ) / door / include / 
LPORD     =  -L $ ( LPORDDIR )  -lpord
 
LMETISDIR = / opt / parmetis-4.0.3 / lib / 
IMETIS     =  -I /opt/parmetis-4.0.3/include/ 
LMETIS     =  -L $ ( LMETISDIR )  -L/opt/aster/public/metis-5.1.0/lib -lparmetis -lmetis

# Corresponding variables reused later
ORDERINGSF = -Dmetis -Dpord -Dparmetis -Dscotch -Dptscotch
ORDERINGSC  = $(ORDERINGSF)

LORDERINGS = $(LMETIS) $(LPORD) $(LSCOTCH)
IORDERINGSF = $(ISCOTCH)
IORDERINGSC = $(IMETIS) $(IPORD) $(ISCOTCH)
# End orderings
################################################################################
PLAT    =
LIBEXT  = .a
OUTC    = -o 
OUTF    = -o 
RM = /bin/rm -f
CC = mpicc
FC = mpif90
FL = mpif90
AR = ar vr 
RANLIB = echo
LAPACK = /opt/OpenBLAS/lib/libopenblas.a
SCALAP = /opt/scalapack/lib/libscalapack.a
INCPAR = -I/usr/lib/x86_64-linux-gnu/openmpi/include 
LIBPAR = $(SCALAP) $(LAPACK) -L/usr/lib/x86_64-linux-gnu/openmpi/lib -lmpi
INCSEQ = -I$(topdir)/libseq
LIBSEQ  = $(LAPACK) -L$(topdir)/libseq -lmpiseq
LIBBLAS = -L/opt/OpenBLAS/lib -lopenblas
LIBOTHERS = -L/usr/lib/x86_64-linux-gnu -lpthread -lutil -ldl

#Preprocessor defs for calling Fortran from C (-DAdd_ or -DAdd__ or -DUPPER)
CDEFS   = -DAdd_

#Begin Optimized options
# uncomment -fopenmp in lines below to benefit from OpenMP
OPTF    = -O -fPIC -DPORD_INTSIZE64 -fopenmp
OPTL    = -O -fopenmp
OPTC    = -O -fPIC -fopenmp
#End Optimized options

INCS = $(INCPAR)
LIBS = $(LIBPAR)
LIBSEQNEEDED =
```

Build and check the operation.

```
$ make all
$ cd examples
$ mpirun -np 4 ./ssimpletest < input_simpletest_real
```

If there is no error, it is OK.



### 8. PETSC



First, unzip it with / opt.

```shell
cd /opt
tar xvzf ~/software/petsc-3.9.4.tar.gz
cd petsc-3.9.4
```

Then open the metis.py file located at /opt/petsc-3.9.4/config/BuildSystem/config/packages and comment out lines 43-48.
It will be the following part.

metis.py:

```python
def configureLibrary(self):
    config.package.Package.configureLibrary(self)
    oldFlags = self.compilers.CPPFLAGS
    self.compilers.CPPFLAGS += ' '+self.headers.toString(self.include)
#    if not self.checkCompile('#include "metis.h"', '#if (IDXTYPEWIDTH != '+ str(self.getDefaultIndexSize())+')\n#error incompatible IDXTYPEWIDTH\n#endif'):
#      if self.defaultIndexSize == 64:
#        msg= '--with-64-bit-indices option requires a metis build with IDXTYPEWIDTH=64.\n'
#      else:
#        msg= 'IDXTYPEWIDTH=64 metis build appears to be specified for a default 32-bit-indices build of PETSc.\n'
#      raise RuntimeError('Metis specified is incompatible!\n'+msg+'Suggest using --download-metis for a compatible metis')

    self.compilers.CPPFLAGS = oldFlags
    return
```

In addition, register the OpenMPI library in LD_LIBRARY_PATH, and then execute configure.

```shell
export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/openmpi/lib/:$LD_LIBRARY_PATH
./configure --with-debugging=0 COPTFLAGS=-O CXXOPTFLAGS=-O FOPTFLAGS=-O --with-shared-libraries=0 --with-scalapack-dir=/opt/scalapack --PETSC_ARCH=linux-metis-mumps --with-metis-dir=/opt/aster/public/metis-5.1.0 --with-parmetis-dir=/opt/parmetis-4.0.3 --with-ptscotch-dir=/opt/scotch-6.0.4 --LIBS="-lgomp" --with-mumps-dir=/opt/mumps-5.1.2 -with-x=0 --with-blas-lapack-lib=[/opt/OpenBLAS/lib/libopenblas.a] --download-hypre=yes --download-ml=yes
```

### TIPS

##### If the hypre download doesn't work

- It will tell you the URL of the download destination github, but it seems that the repository does not exist ...
- Since it is registered in the launchpad of Ubuntu, you can download it from there (file name: hypre_2.14.0.orig.tar.gz).
  　[hypre 2.14.0-5build1 source package in Ubuntu](https://launchpad.net/ubuntu/+source/hypre/2.14.0-5build1)
- After downloading, put it in / opt.
- After that, change `--download-hypre=yes`the part to `--download-hypre=/opt/hypre_2.14.0.orig.tar.gz`and try configure again.

##### If the ml download doesn't work

- This can be downloaded from the specified URL. Download it and place it in / opt. (File name: petsc-pkg-ml-e5040d11aa07.zip)
  [bitbucket pkg-ml](https://bitbucket.org/petsc/pkg-ml/downloads/?tab=downloads)
- Similar to hypre , change `--download-ml=yes`the part to `--download-ml=/opt/petsc-pkg-ml-e5040d11aa07.zip`and run configure again.

After successfully configure, run make.

```
$ make PETSC_DIR=/opt/petsc-3.9.4 PETSC_ARCH=linux-metis-mumps all
$ make PETSC_DIR=/opt/petsc-3.9.4 PETSC_ARCH=linux-metis-mumps check
```







## 11 Side by side Code_Aster

There is a parallel version Code_Aster source file in the Code_Aster source file, so unzip it first.

```shell
$ cd ~/software/aster-full-src-14.4.0/SRC
$ tar xfvz aster-14.4.0.tgz
$ cd aster-14.4.0
```

Comment out lines 362-364 of waftools / mathematicals.py in the above directory.
It will be the following part.

mathematics.py :

```python
# program testing a blacs call, output is 0 and 1
blacs_fragment = r"""
program test_blacs
    integer iam, nprocs
#    call blacs_pinfo (iam, nprocs)
#    print *,iam
#    print *,nprocs
end program test_blacs
"""
```

Next, create ```Ubuntu_gnu_mpi.py``` and ```Ubuntu_gnu.py``` and place them in your current directory (~ / software / aster-full-src-14.4.0 / SRC / aster-14.4.0).

```Ubuntu_gnu_mpi.py```: 

```python
# encoding: utf-8

"""
Fichier de configuration WAF pour version parallﾃｨle sur Ubuntu 13.6 :
- Compilateur : GNU
- MPI         : systﾃｨme (OpenMPI, Ubuntu 13.6)
- BLAS        : OpenBLAS
- Scalapack   : systﾃｨme (Ubuntu 13.6)
- PETSc       : 
"""

import Ubuntu_gnu

def configure(self):
    opts = self.options
    Ubuntu_gnu.configure(self)

    self.env.prepend_value('LIBPATH', [
        '/opt/petsc-3.9.4/linux-metis-mumps/lib',
        '/opt/parmetis-4.0.3/lib',
        '/opt/mumps-5.1.2/lib',])

    self.env.prepend_value('INCLUDES', [
        '/opt/petsc-3.9.4/linux-metis-mumps/include',
        '/opt/petsc-3.9.4/include',
        '/usr/include/superlu',
        '/opt/parmetis-4.0.3/include',
        '/opt/mumps-5.1.2/include',])

    self.env.append_value('LIB', ('X11',))

    opts.parallel = True

    opts.enable_mumps  = True
    opts.mumps_version = '5.1.2'
    opts.mumps_libs = 'dmumps zmumps smumps cmumps mumps_common pord metis scalapack openblas esmumps scotch scotcherr'
#    opts.embed_mumps = True

    opts.enable_petsc = True
    opts.petsc_libs='petsc HYPRE ml'
#    opts.petsc_libs='petsc'
#    opts.embed_petsc = True

#    opts.enable_parmetis  = True
    self.env.append_value('LIB_METIS', ('parmetis'))
    self.env.append_value('LIB_SCOTCH', ('ptscotch','ptscotcherr','ptscotcherrexit','ptesmumps'))
```

```Ubuntu_gnu.py```:

```python
# encoding: utf-8

"""
Fichier de configuration WAF pour version sﾃｩquentielle sur Ubuntu 13.6 :
- Compilateur : GNU
- BLAS        : OpenBLAS
"""
import os

def configure(self):
    opts = self.options

    # mfront path
#    self.env.TFELHOME = '/opt/tfel-3.2.0'

    self.env.append_value('LIBPATH', [
        '/opt/aster/public/hdf5-1.10.3/lib',
        '/opt/aster/public/med-4.0.0/lib',
        '/opt/aster/public/metis-5.1.0/lib',
        '/opt/scotch-6.0.4/lib',
        '/opt/OpenBLAS/lib',
        '/opt/scalapack/lib',])
#        '/opt/tfel-3.2.0/lib',

    self.env.append_value('INCLUDES', [
        '/opt/aster/public/hdf5-1.10.3/include',
        '/opt/aster/public/med-4.0.0/include',
        '/opt/aster/public/metis-5.1.0/include',
        '/opt/scotch-6.0.4/include',
        '/opt/OpenBLAS/include',
        '/opt/scalapack/include',])
#        '/opt/tfel-3.2.0/include',

    opts.'openblas superlu'=maths_libs  
#    opts.embed_math = True

    opts.enable_hdf5 = True
    opts.hdf5_libs  = 'hdf5 z'
#    opts.embed_hdf5 = True

    opts.enable_med = True
    opts.med_libs  = 'med stdc++'
#    opts.embed_med  = True

    opts.enable_mfront = False

    opts.enable_scotch = True
#    opts.embed_scotch  = True

    opts.enable_homard = True
#    opts.embed_aster    = True
#    opts.embed_fermetur = True

    # add paths for external programs
#    os.environ['METISDIR'] = '/opt/aster/public/metis-5.1.0'
#    os.environ['GMSH_BIN_DIR'] = '/opt/aster/public/gmsh-3.0.6-Linux/bin'
    os.environ['HOMARD_ASTER_ROOT_DIR'] = '/opt/aster/public/homard-11.12'

    opts.with_prog_metis = True
#    opts.with_prog_gmsh = True
    # salome: only required by few testcases
    # europlexus: not available on all platforms
#    opts.with_prog_miss3d = True
    opts.with_prog_homard = True
#    opts.with_prog_ecrevisse = True
    opts.with_prog_xmgrace = True
```



I will install it when I am ready.

```shell
$ export ASTER_ROOT=/opt/aster
$ export PYTHONPATH=/$ASTER_ROOT/lib/python3.6/site-packages/:$PYTHONPATH
$ ./waf configure --use-config-dir=$ASTER_ROOT/14.4/share/aster --use-config=Ubuntu_gnu_mpi --prefix=$ASTER_ROOT/PAR14.4MUPT
$ ./waf install -p --jobs=1
```

When you're done, register it with the name 14.4MUPT so that you can use the parallel version of Code_Aster with ASTK.
There is a file called aster in / opt / aster / etc / codeaster /, so add the following to the last line of it.

```python
# Code_Aster versions
# versions can be absolute paths or relative to ASTER_ROOT
# examples : NEW11, /usr/lib/codeaster/NEW11

# default version (overridden by --vers option)
default_vers : stable

# available versions
# DO NOT EDIT FOLLOWING LINE !
#?vers : VVV?
vers : stable:/opt/aster/14.4/share/aster
vers : 14.4MUPT:/opt/aster/PAR14.4MUPT/share/aster
```

That's all.
When you start ASTK, 14.4 MUPT is newly added and can be selected in the Version tab.
[![astk3.png](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F439095%2Fda95ba00-57a1-dc6d-935e-dd89b012f5d6.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=75b9b9e8b34c6fcf356caeb8787e2df5)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F439095%2Fda95ba00-57a1-dc6d-935e-dd89b012f5d6.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=75b9b9e8b34c6fcf356caeb8787e2df5)

Thank you for your hard work!
Thank you to those who have disclosed the information.







































