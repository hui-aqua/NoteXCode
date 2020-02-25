# About submit shell
The system uses SLURM, https://slurm.schedmd.com/overview.html, so Google will provide ample additional information.

The easy way is just change the following parts.

## 1. Job name 
- Line 3

change "h12_2deg" to your name, nolonger than 8 characters

## 2. Processor number
- Line 4

change the 20 to the number of processor addcording to your wish but no larger than 220.

## 3. Node number,

- Line5 

change the 1 to the number of computational node. For each node, it has 20 processors

## 4. Running script

- Line 10-end

add the running script here.