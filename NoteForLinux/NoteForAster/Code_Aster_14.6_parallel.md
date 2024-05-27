# Parallelization of Code_Aster 14.6

## 1 Background

First of all, I have tried to install the parallel version code aster on my computer for two days and refer to many blogs and websites. All of them are either too simple or have some issue with my system environments. Here, I will detaily explain the procedure of the installations. 

・[Code_aster 14.6 parallel version with PETSc](https://hitoricae.com/2019/11/10/code_aster-14-4-with-petsc/)
・[Parallelization of Code_Aster 12.6](https://sites.google.com/site/codeastersalomemeca/home/code_asterno-heiretuka/code_asterno-heiretuka-12-6)

* [ref3](https://qiita.com/hiro_kuramoto/items/269ecf6293cfbe38b314)

## 2 Environment

OS : Linux Mint 19.3
Python 3.6.9

## 3 Preparation

Since it will be installed in / opt, change / opt from root to owned by the logged-in user.

```shell
sudo chown "username" / opt 
```

Next, install the packages required to build the parallel version of Code_Aster.

```shell
sudo apt install gfortran g++ python-dev python-numpy liblapack-dev libblas-dev tcl tk zlib1g-dev bison flex checkinstall openmpi-bin libx11-dev cmake grace gettext libboost-all-dev swig libsuperlu-dev
```

Next, download the package that needs to be built from the source from the following site and put it in an appropriate directory (~ / software).

| package    | my version | Latest version | Download destination                                         |
| :--------- | ---------- | :------------- | :----------------------------------------------------------- |
| Code_Aster | 14.6       | 14.6           | [https://www.code-aster.org](https://www.code-aster.org/)    |
| OpenBLAS   | 0.2.0      | 0.3.10         | https://github.com/xianyi/OpenBLAS/                          |
| ScaLAPACK  | 2.0.0      | 2.1.0          | http://www.netlib.org/scalapack/#_scalapack_installer_for_linux |
| Parmetis   | 4.0.3      | 4.0.3          | http://glaros.dtc.umn.edu/gkhome/metis/parmetis/download     |
| Petsc      | 3.9.4      | 3.14.2         | https://www.mcs.anl.gov/petsc/download/index.html            |

## 4 OpenBLAS

First, unzip and install.

```shell
cd ~/software
tar xvzf OpenBLAS-0.2.20.tar.gz 
cd OpenBLAS-0.2.20
make NO_AFFINITY=1 USE_OPENMP=1 
make PREFIX=/opt/aster146p/parallelModules/OpenBLAS install 
```

Add OpenBLAS to the search path of the shared library.

```shell
echo /opt/aster146p/parallelModules/OpenBLAS/lib | sudo tee -a /etc/ld.so.conf.d/openblas.conf 
sudo ldconfig 
```

## 5 Code_Aster with OpenBLAS

In order to parallelize Code_Aster, you need to install the regular version first.
First, unzip it.

```shll
cd ~/software
tar xvzf aster-full-src-14.6.0-1.noarch.tar.gz
cd aster-full-src-14.6.0
```

Then edit the contents of the setup.cfg file.
Change ```PREFER_COMPILER = GNU``` to ```PREFER_COMPILER = GNU_without_MATH``` and specify the OpenBLAS you just installed for MATHLIB.

```shell
sed -i "s:PREFER_COMPILER\ =\ 'GNU':PREFER_COMPILER\ =\'GNU_without_MATH'\nMATHLIB=\ '/opt/aster146p/parallelModules/OpenBLAS/lib/libopenblas.a':g" setup.cfg
```

Install it in / opt / aster.

```shell
python3 setup.py install --prefix=/opt/aster146p
```

You will be asked various questions on the way, but all will be yes.
After the installation is complete, check the operation.

```shell
/opt/aster146p/bin/as_run --vers=14.6 --test forma01a 
```

If there is no error, it is OK.
Create a host file for parallel computing. When forming a cluster with another machine, it seems better to add in the same format.

```shell
echo "$HOSTNAME cpu=$(cat /proc/cpuinfo | grep processor | wc -l)" > /opt/aster146p/etc/codeaster/mpi_hostfile 
```

**TIPS** :  [FAILED] is displayed while running setup.py

In my environment, it seemed to occur when numpy was already installed using pip.
In that case `pip3 uninstall numpy`, delete numpy completely with ⇒ `sudo apt install python-numpy`install numpy with ⇒ install Code_Aster, and try it.

## 6 ScaLAPACK

Unzip and install.

```shell
cd ~/software
tar xvzf scalapack_installer.tgz 
cd scalapack_installer
./setup.py --lapacklib=/opt/aster146p/parallelModules/OpenBLAS/lib/libopenblas.a --mpicc=mpicc --mpif90=mpif90 --mpiincdir=/usr/lib/x86_64-linux-gnu/openmpi/include --ldflags_c=-fopenmp --ldflags_fc=-fopenmp --prefix=/opt/aster146p/parallelModules/scalapack
```

**Usually** it will have an error message, such as:

```IOError: [Errno 2] No such file or directory: 'download/./scalapack.tgz'```

Then You need to:

- Download scalapack-2.0.0.tgz from the official website
- Rename and place scalapack.tgz in ~ / software / scalapack_installer / build / ⇒ Run setup.py again.

At the end of the log

```shell
BLACS: error running BLACS test routines xCbtest
BLACS: Command  -np 4 ./xCbtest
stderr:
**************************************
/bin/sh: 1: -np: not found
**************************************
```

Is displayed, but it is successful if the file /opt/aster146p/parallelModules/scalapack/lib/libscalapack.a is created.



## 7 Parmetis

First, unzip it.

```shell
cd ~/software
tar xvzf parmetis-4.0.3.tar.gz 
cd parmetis-4.0.3
```

Next, rewrite a part of the file of metis / include / metis.h and change it to compile in 64bit mode.

```shell
sed -i -e 's/#define IDXTYPEWIDTH 32/#define IDXTYPEWIDTH 64/' metis/include/metis.h
```

Install it.

```shell
make config prefix=/opt/aster146p/parallelModules/parmetis-4.0.3 
make
make install
```

Next, let's check the operation.

```shell
cd Graphs
mpirun -np 4 /opt/aster146p/parallelModules/parmetis-4.0.3/bin/parmetis rotor.graph 1 6 1 1 6 1
```

If there are no errors, it is successful. On my computer it shows:

```shell
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
Final   6-way Cut:  11288 	Balance: 1.047
```



## 8 Scotch

First, move scotch-6.0.4-aster7.tar.gz included in ~ / software / aster-full-src-14.6.0 / SRC to /opt and unzip it.

```
cp ~/software/aster-full-src-14.6.0/SRC/scotch-6.0.4-aster7.tar.gz /opt/aster146p/parallelModules
cd /opt/aster146p/parallelModules
tar xvzf scotch-6.0.4-aster7.tar.gz
cd scotch-6.0.4
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

Build and check the operation.

```
cd src
make scotch esmumps ptscotch ptesmumps CCD=mpicc
make check
make ptcheck
```

## 9 MUMPS

Again, move mumps-5.1.2-aster6.tar.gz from ~ / software / aster-full-src-14.6.0 / SRC to /opt and unzip it.

```shell
cp ~/software/aster-full-src-14.6.0/SRC/mumps-5.1.2-aster7.tar.gz /opt/aster146p/parallelModules/
cd /opt/aster146p/parallelModules/
tar xvzf mumps-5.1.2-aster7.tar.gz
cd mumps-5.1.2
```

Edit Makefile.inc to suit your environment.
The base file is prepared in the Makefile.inc / directory, so copy it.

```shell
cp Make.inc/Makefile.debian.PAR ./Makefile.inc
```

Modify the library specifications etc. according to the environment.

```makefile
#
# This file is part of MUMPS 5.0.1, changed to be configured by waf scripts
# provided by the Code_Aster team.
#
#Begin orderings

# NOTE that PORD is distributed within MUMPS by default. If you would like to
# use other orderings, you need to obtain the corresponding package and modify
# the variables below accordingly.
# For example, to have Metis available within MUMPS:
#          1/ download Metis and compile it
#          2/ uncomment (suppress # in first column) lines
#             starting with LMETISDIR,  LMETIS
#          3/ add -Dmetis in line ORDERINGSF
#             ORDERINGSF  = -Dpord -Dmetis
#          4/ Compile and install MUMPS
#             make clean; make   (to clean up previous installation)
#
#          Metis/ParMetis and SCOTCH/PT-SCOTCH (ver 5.1 and later) orderings are now available for MUMPS.
#

ISCOTCH    = -I/opt/aster146p/public/metis-5.1.0/include -I/opt/aster146p/parallelModules/parmetis-4.0.3/include -I/opt/aster146p/parallelModules/scotch-6.0.4/include
# You have to choose one among the following two lines depending on
# the type of analysis you want to perform. If you want to perform only
# sequential analysis choose the first (remember to add -Dscotch in the ORDERINGSF
# variable below); for both parallel and sequential analysis choose the second 
# line (remember to add -Dptscotch in the ORDERINGSF variable below)

LSCOTCH    = -L/opt/aster146p/public/metis-5.1.0/lib -L/opt/aster146p/parallelModules/parmetis-4.0.3/lib -L/opt/aster146p/parallelModules/scotch-6.0.4/lib -L/opt/aster146p/parallelModules/scalapack/lib -Wl,-Bdynamic -lesmumps -lptscotch -lptscotcherr -lptscotcherrexit -lscotch -lscotcherr -lscotcherrexit 
#LSCOTCH    = -L$(SCOTCHDIR)/lib -lptesmumps -lptscotch -lptscotcherr


LPORDDIR = $(topdir)/PORD/lib/
IPORD    = -I$(topdir)/PORD/include/
LPORD    = -L$(LPORDDIR) -lpord

#IMETIS    = # Metis doesn't need include files (Fortran interface avail.)
# You have to choose one among the following two lines depending on
# the type of analysis you want to perform. If you want to perform only
# sequential analysis choose the first (remember to add -Dmetis in the ORDERINGSF
# variable below); for both parallel and sequential analysis choose the second 
# line (remember to add -Dparmetis in the ORDERINGSF variable below)

LMETIS    = -L/opt/aster146p/public/metis-5.1.0/lib -L/opt/aster146p/parallelModules/parmetis-4.0.3/lib -L/opt/aster146p/parallelModules/scotch-6.0.4/lib -L/opt/aster146p/parallelModules/scalapack/lib -Wl,-Bdynamic -lparmetis  -Wl,-Bdynamic -lmetis  
#LMETIS    = -L$(LMETISDIR) -lparmetis -lmetis

# The following variables will be used in the compilation process.
# Please note that -Dptscotch and -Dparmetis imply -Dscotch and -Dmetis respectively.
#ORDERINGSF = -Dscotch -Dmetis -Dpord -Dptscotch -Dparmetis
ORDERINGSF  = -Dpord -Dmetis -Dparmetis -Dscotch -Dptscotch
ORDERINGSC  = $(ORDERINGSF)

LORDERINGS = $(LMETIS) $(LPORD) $(LSCOTCH)
IORDERINGSF = $(ISCOTCH)
IORDERINGSC = $(IMETIS) $(IPORD) $(ISCOTCH)

#End orderings
########################################################################
################################################################################

PLAT    =
LIBEXT  = .a
OUTC    = -o 
OUTF    = -o 
RM      = /bin/rm -f
CC      = mpicc
FC      = mpif90
FL      = mpif90
# WARNING: AR must ends with a blank space!
AR      = /usr/bin/ar rcs 
#
RANLIB  = echo

#
INCPAR = -I/opt/aster146p/public/metis-5.1.0/include -I/opt/aster146p/parallelModules/parmetis-4.0.3/include -I/opt/aster146p/parallelModules/scotch-6.0.4/include
LIBPAR = 
#
INCSEQ = -I$(topdir)/libseq
LIBSEQ = -L$(topdir)/libseq -lmpiseq

#
LIBBLAS = -L/opt/aster146p/public/metis-5.1.0/lib -L/opt/aster146p/parallelModules/parmetis-4.0.3/lib -L/opt/aster146p/parallelModules/scotch-6.0.4/lib -L/opt/aster146p/parallelModules/scalapack/lib -Wl,-Bdynamic -lpthread -lm -lblas -llapack -lscalapack -L/opt/aster146p/parallelModules/OpenBLAS/lib -lopenblas 
LIBOTHERS =  -L/opt/aster146p/public/metis-5.1.0/lib -L/opt/aster146p/parallelModules/parmetis-4.0.3/lib -L/opt/aster146p/parallelModules/scotch-6.0.4/lib -L/opt/aster146p/parallelModules/scalapack/lib -Wl,-Bdynamic -ldl -lutil -lpthread   
#Preprocessor defs for calling Fortran from C (-DAdd_ or -DAdd__ or -DUPPER)
CDEFS   = -D_USE_MPI=1 -DHAVE_MPI=1 -D_USE_OPENMP=1 -DHAVE_METIS_H=1 -D_HAVE_METIS=1 -DHAVE_METIS=1 -DHAVE_PARMETIS_H=1 -D_HAVE_PARMETIS=1 -DHAVE_PARMETIS=1 -DHAVE_STDIO_H=1 -DHAVE_SCOTCH=1 -DAdd_ -Dmetis -Dparmetis

#Begin Optimized options
OPTF    = -O -fPIC -DPORD_INTSIZE64 -fopenmp
OPTL    = -O -Wl,--export-dynamic -fopenmp -L/opt/aster146p/public/metis-5.1.0/lib -L/opt/parmetis-4.0.3/lib -L/opt/aster146p/parallelModules/scotch-6.0.4/lib -L/opt/aster146p/parallelModules/scalapack/lib -L/usr/lib -L/usr/lib/x86_64-linux-gnu/openmpi/lib -L/opt/aster146p/public/metis-5.1.0/lib -L/opt/aster146p/parallelModules/parmetis-4.0.3/lib -L/opt/aster146p/parallelModules/scotch-6.0.4/lib -L/opt/aster146p/parallelModules/scalapack/lib -L/usr//lib -L/usr/lib/x86_64-linux-gnu/openmpi/lib -Lnow -Lrelro -L/opt/aster146p/public/metis-5.1.0/lib -L/opt/aster146p/parallelModules/parmetis-4.0.3/lib -L/opt/aster146p/parallelModules/scotch-6.0.4/lib -L/opt/aster146p/parallelModules/scalapack/lib -L/usr//lib -L/usr/lib/x86_64-linux-gnu/openmpi/lib -L/usr/lib/gcc/x86_64-linux-gnu/7 -L/usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu -L/usr/lib/gcc/x86_64-linux-gnu/7/../../../../lib -L/lib/x86_64-linux-gnu -L/lib/../lib -L/usr/lib/x86_64-linux-gnu -L/usr/lib/../lib -L/usr/lib/gcc/x86_64-linux-gnu/7/../../.. -lmpi_usempif08 -lmpi_usempi_ignore_tkr -lmpi_mpifh -lmpi -lgfortran -lquadmath -lpthread -L/opt/aster146p/public/metis-5.1.0/lib -L/opt/aster146p/parallelModules/parmetis-4.0.3/lib -L/opt/aster146p/parallelModules/scotch-6.0.4/lib -L/opt/aster146p/parallelModules/scalapack/lib -L/usr//lib -L/usr/lib/x86_64-linux-gnu/openmpi/lib
OPTC    = -O -fPIC -fopenmp
#End Optimized options

INCS = $(INCPAR)
LIBS = $(LIBPAR)
LIBSEQNEEDED = 
```

Build and check the operation.

```shell
make all
cd examples
mpirun -np 4 ./ssimpletest < input_simpletest_real
```

If there is no error, it is OK. On my computer, it shows:

```python
Entering SMUMPS 5.1.2 with JOB, N, NNZ =   6           5             12
      executing #MPI =      4 and #OMP =     16

 =================================================
 MUMPS compiled with option -Dmetis
 MUMPS compiled with option -Dparmetis
 MUMPS compiled with option -Dptscotch
 MUMPS compiled with option -Dscotch
 =================================================
L U Solver for unsymmetric matrices
Type of parallelism: Working host

 ****** ANALYSIS STEP ********

 ... Structural symmetry (in percent)=   92
 Average density of rows/columns =    2
 ... No column permutation
 Ordering based on AMF 

Leaving analysis phase with  ...
INFOG(1)                                       =               0
INFOG(2)                                       =               0
 -- (20) Number of entries in factors (estim.) =              15
 --  (3) Storage of factors  (REAL, estimated) =              15
 --  (4) Storage of factors  (INT , estimated) =              65
 --  (5) Maximum frontal size      (estimated) =               3
 --  (6) Number of nodes in the tree           =               3
 -- (32) Type of analysis effectively used     =               1
 --  (7) Ordering option effectively used      =               2
ICNTL(6) Maximum transversal option            =               0
ICNTL(7) Pivot order option                    =               7
Percentage of memory relaxation (effective)    =              20
Number of level 2 nodes                        =               0
Number of split nodes                          =               0
RINFOG(1) Operations during elimination (estim)=   1.900D+01
 ** Rank of proc needing largest memory in IC facto        :               0
 ** Estimated corresponding MBYTES for IC facto            :               1
 ** Estimated avg. MBYTES per work. proc at facto (IC)     :               1
 ** TOTAL     space in MBYTES for IC factorization         :               4
 ** Rank of proc needing largest memory for OOC facto      :               0
 ** Estimated corresponding MBYTES for OOC facto           :               1
 ** Estimated avg. MBYTES per work. proc at facto (OOC)    :               1
 ** TOTAL     space in MBYTES for OOC factorization        :               4
 ELAPSED TIME IN ANALYSIS DRIVER=       0.0007

 ****** FACTORIZATION STEP ********


 GLOBAL STATISTICS PRIOR NUMERICAL FACTORIZATION ...
 NUMBER OF WORKING PROCESSES              =               4
 OUT-OF-CORE OPTION (ICNTL(22))           =               0
 REAL SPACE FOR FACTORS                   =              15
 INTEGER SPACE FOR FACTORS                =              65
 MAXIMUM FRONTAL SIZE (ESTIMATED)         =               3
 NUMBER OF NODES IN THE TREE              =               3
 MEMORY ALLOWED (MB -- 0: N/A )           =               0
 RELATIVE THRESHOLD FOR PIVOTING, CNTL(1) =      0.1000D-01
 Convergence error after scaling for ONE-NORM (option 7/8)   = 0.38D+00
 Maximum effective relaxed size of S              =             475
 Average effective relaxed size of S              =             467
 ELAPSED TIME FOR MATRIX DISTRIBUTION      =      0.0000
 ** Memory relaxation parameter ( ICNTL(14)  )            :        20
 ** Rank of processor needing largest memory in facto     :         0
 ** Space in MBYTES used by this processor for facto      :         1
 ** Avg. Space in MBYTES per working proc during facto    :         1

 ELAPSED TIME FOR FACTORIZATION           =      0.0004
 Maximum effective space used in S     (KEEP8(67))               12
 Average effective space used in S     (KEEP8(67))                4
 ** EFF Min: Rank of processor needing largest memory :         0
 ** EFF Min: Space in MBYTES used by this processor   :         1
 ** EFF Min: Avg. Space in MBYTES per working proc    :         1

 GLOBAL STATISTICS 
 RINFOG(2)  OPERATIONS IN NODE ASSEMBLY   = 2.000D+00
 ------(3)  OPERATIONS IN NODE ELIMINATION= 1.900D+01
 INFOG (9)  REAL SPACE FOR FACTORS        =              15
 INFOG(10)  INTEGER SPACE FOR FACTORS     =              65
 INFOG(11)  MAXIMUM FRONT SIZE            =               3
 INFOG(29)  NUMBER OF ENTRIES IN FACTORS  =              15
 INFOG(12)  NUMBER OF OFF DIAGONAL PIVOTS =               0
 INFOG(13)  NUMBER OF DELAYED PIVOTS      =               0
 INFOG(14)  NUMBER OF MEMORY COMPRESS     =               0
 ELAPSED TIME IN FACTORIZATION DRIVER=       0.0010


 ****** SOLVE & CHECK STEP ********


 STATISTICS PRIOR SOLVE PHASE     ...........
 NUMBER OF RIGHT-HAND-SIDES                    =           1
 BLOCKING FACTOR FOR MULTIPLE RHS              =           1
 ICNTL (9)                                     =           1
  --- (10)                                     =           0
  --- (11)                                     =           0
  --- (20)                                     =           0
  --- (21)                                     =           0
  --- (30)                                     =           0
 ** Rank of processor needing largest memory in solve     :         0
 ** Space in MBYTES used by this processor for solve      :         0
 ** Avg. Space in MBYTES per working proc during solve    :         0

 Global statistics
 TIME to build/scatter RHS        =       0.000038
 TIME in solution step (fwd/bwd)  =       0.000093
  .. TIME in forward (fwd) step   =          0.000057
  .. TIME in backward (bwd) step  =          0.000031
 TIME to gather solution(cent.sol)=       0.000004
 TIME to copy/scale RHS (dist.sol)=       0.000000
 ELAPSED TIME IN SOLVE DRIVER=       0.0004
  Solution is    1.00000060       2.00000048       3.00000000       4.00000000       4.99999905    

Entering SMUMPS 5.1.2 with JOB =  -2
      executing #MPI =      4 and #OMP =     16
```



## 10 Petsc

First, unzip it with / opt.

```shell
cd /opt/aster146p/parallelModules
tar xvzf ~/software/petsc-3.9.4.tar.gz
cd petsc-3.9.4
```

Then open the  file located at `/opt/aster146p/parallelModules/petsc-3.9.4/config/BuildSystem/config/packages/metis.py`

and next, comment out lines 43-48.
It will be the following part.

metis.py

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
./configure --COPTFLAGS="-O2" --CXXOPTFLAGS="-O2"  --FOPTFLAGS="-O2"  --with-debugging=0 --with-shared-libraries=1  --with-scalapack-dir=${ASTER_PUBLIC}/scalapack-${SCALAPACK_VER}  --with-mumps-dir=${ASTER_PUBLIC}/mumps-${MUMPS_VER}_mpi  --with-metis-dir=${ASTER_PUBLIC}/metis-${METIS_VER}  --with-ptscotch-dir=${ASTER_PUBLIC}/ptscotch-${SCOTCH_VER} --download-hypre --download-ml  --LIBS="-lgomp" --prefix=${ASTER_PUBLIC}/petsc-${PETSC_VER}
```



```shell
export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/openmpi/lib/:$LD_LIBRARY_PATH
./configure --with-debugging=0 COPTFLAGS=-O CXXOPTFLAGS=-O FOPTFLAGS=-O --with-shared-libraries=0 --with-scalapack-dir=/opt/aster146p/parallelModules/scalapack --PETSC_ARCH=linux-metis-mumps --with-metis-dir=/opt/aster146p/public/metis-5.1.0 --with-parmetis-dir=/opt/aster146p/parallelModules/parmetis-4.0.3 --with-ptscotch-dir=/opt/aster146p/parallelModules/scotch-6.0.4 --LIBS="-lgomp" --with-mumps-dir=/opt/aster146p/parallelModules/mumps-5.1.2 -with-x=0 --with-blas-lapack-lib=[/opt/aster146p/parallelModules/OpenBLAS/lib/libopenblas.a] --download-hypre=yes --download-ml=yes
```

**TIPS**

1. If the hypre download doesn't work

- It will tell you the URL of the download destination github, but it seems that the repository does not exist ...
- Since it is registered in the launchpad of Ubuntu, you can download it from there (file name: hypre_2.14.0.orig.tar.gz).
  　[hypre 2.14.0-5build1 source package in Ubuntu](https://launchpad.net/ubuntu/+source/hypre/2.14.0-5build1)
- After downloading, put it in / opt.
- After that, change `--download-hypre=yes`the part to `--download-hypre=/opt/hypre_2.14.0.orig.tar.gz` and try configure again.

2. If the ml download doesn't work

- This can be downloaded from the specified URL. Download it and place it in / opt. (File name: petsc-pkg-ml-e5040d11aa07.zip)
  [bitbucket pkg-ml](https://bitbucket.org/petsc/pkg-ml/downloads/?tab=downloads)
  
- Similar to hypre , change `--download-ml=yes`the part to `--download-ml=/opt/petsc-pkg-ml-e5040d11aa07.zip`and run configure again.

  

  - [ ] It shows on my computer:

```python
PETSc:
  PETSC_ARCH: linux-metis-mumps
  PETSC_DIR: /opt/petsc-3.9.4
  Scalar type: real
  Precision: double
  Clanguage: C
  Integer size: 32
  shared libraries: disabled
  Memory alignment: 16
xxx=========================================================================xxx
 Configure stage complete. Now build PETSc libraries with (gnumake build):
   make PETSC_DIR=/opt/petsc-3.9.4 PETSC_ARCH=linux-metis-mumps all
xxx=========================================================================xxx

```



After successfully configure, run make.

```shell
make PETSC_DIR=/opt/petsc-3.9.4 PETSC_ARCH=linux-metis-mumps all
make PETSC_DIR=/opt/petsc-3.9.4 PETSC_ARCH=linux-metis-mumps check
```

## 11 Side by side Code_Aster

There is a parallel version Code_Aster source file in the Code_Aster source file, so unzip it first.

```shell
cd ~/software/aster-full-src-14.6.0/SRC
tar xfvz aster-14.6.0.tgz
cd aster-14.6.0
```

Comment out lines 362-364 of `waftools/mathematicals.py` in the above directory.
It will be the following part.

mathematics.py

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

Next, create `mint_gnu_mpi.py` and `mint_gnu.py` and place them in your current directory

 (`~/software/aster-full-src-14.6.0/SRC/aster-14.6.0`).

**mint_gnu_mpi.py:**

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

import mint_gnu

def configure(self):
    opts = self.options
    mint_gnu.configure(self)

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



**mint_gnu.py**:

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
        '/opt/aster146p/public/hdf5-1.10.3/lib',
        '/opt/aster146p/public/med-4.0.0/lib',
        '/opt/aster146p/public/metis-5.1.0/lib',
        '/opt/scotch-6.0.4/lib',
        '/opt/OpenBLAS/lib',
        '/opt/scalapack/lib',])
#        '/opt/tfel-3.2.0/lib',

    self.env.append_value('INCLUDES', [
        '/opt/aster146p/public/hdf5-1.10.3/include',
        '/opt/aster146p/public/med-4.0.0/include',
        '/opt/aster146p/public/metis-5.1.0/include',
        '/opt/scotch-6.0.4/include',
        '/opt/OpenBLAS/include',
        '/opt/scalapack/include',])
#        '/opt/tfel-3.2.0/include',

    opts.maths_libs = 'openblas superlu'  
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
#    os.environ['METISDIR'] = '/opt/aster146p/public/metis-5.1.0'
#    os.environ['GMSH_BIN_DIR'] = '/opt/aster146p/public/gmsh-3.0.6-Linux/bin'
    os.environ['HOMARD_ASTER_ROOT_DIR'] = '/opt/aster146p/public/homard-11.12'

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
export ASTER_ROOT=/opt/aster146p
export PYTHONPATH=/$ASTER_ROOT/lib/python3.6/site-packages/:$PYTHONPATH
./waf configure --use-config-dir=$ASTER_ROOT/14.6/share/aster --use-config=mint_gnu_mpi --prefix=$ASTER_ROOT/PAR14.6MUPT
./waf install -p --jobs=1
```

It shows on my computer:

```shell
'install' finished successfully (15m17.139s)
```



When you're done, register it with the name 14.6MUPT so that you can use the parallel version of Code_Aster with ASTK.

There is a file called aster in / opt / aster / etc / codeaster /, so add the following to the last line of it.

```makefile
# Code_Aster versions
# versions can be absolute paths or relative to ASTER_ROOT
# examples : NEW11, /usr/lib/codeaster/NEW11

# default version (overridden by --vers option)
default_vers : stable

# available versions
# DO NOT EDIT FOLLOWING LINE !
#?vers : VVV?
vers : stable:/opt/aster146p/14.6/share/aster
vers : 14.6MUPT:/opt/aster146p/PAR14.6MUPT/share/aster
```

That's all.
When you start ASTK, 14.6 MUPT is newly added and can be selected in the Version tab.
[![astk3.png](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F439095%2Fda95ba00-57a1-dc6d-935e-dd89b012f5d6.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=75b9b9e8b34c6fcf356caeb8787e2df5)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F439095%2Fda95ba00-57a1-dc6d-935e-dd89b012f5d6.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=75b9b9e8b34c6fcf356caeb8787e2df5)

Thank you for your hard work!
Thank you to those who have disclosed the information.