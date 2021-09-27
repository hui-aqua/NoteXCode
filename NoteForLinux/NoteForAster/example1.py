# ----------------------------------
# --   University of Stavanger    --
# --           Hui Cheng          --
# ----------------------------------
# Any questions about this code,
# please email: hui.cheng@uis.no
import sys
import os
import time
sys.path.append("/home/magnus/Github/Aster_module/hydromodel/scr/model4aster/")
import hydrodynamicModule as hdm
import nettingFSI as fsi
import seacondition as sc
cwd="/home/magnus/simulationWorks/code_aster_test1/moe2016/"

DEBUT(PAR_LOT='NON',
IGNORE_ALARM=("SUPERVIS_25","DISCRETE_26","UTILITAI8_56")
)
INCLUDE(UNITE=90)
mesh = LIRE_MAILLAGE(UNITE=20)

model = AFFE_MODELE(AFFE=(_F(GROUP_MA=('twines'),
                             MODELISATION=('CABLE'),
                             PHENOMENE='MECANIQUE'),
                          ),
                    MAILLAGE=mesh)
    
elemprop = AFFE_CARA_ELEM(CABLE=_F(GROUP_MA=('twines'),
                                   N_INIT=10.0,
                                   SECTION=3.3732997880723915e-05),
                          MODELE=model)

net = DEFI_MATERIAU(CABLE=_F(EC_SUR_E=0.0001),
                     ELAS=_F(E=40000000, NU=0.2,RHO=1140.0))  #from H.moe 2016
                          # ELAS=_F(E=62500000,NU=0.2,RHO=1140.0))  #from odd m. faltinsen, 2017
                          # ELAS=_F(E=82000000,NU=0.2,RHO=1015.0))  #from H.moe, a. fredheim, 2010
                          # ELAS=_F(E=119366207.319,NU=0.2,RHO=1015.0))#from chun woo lee
                          # ELAS=_F(E=182000000,NU=0.2,RHO=1015.0))

fieldmat = AFFE_MATERIAU(AFFE=(_F(GROUP_MA=('twines'),
                                 MATER=(net)),
                               ),
                         MODELE=model)

gF = AFFE_CHAR_MECA(PESANTEUR=_F(DIRECTION=(0.0, 0.0, -1.0),
                                       GRAVITE=9.81,
                                       GROUP_MA=("twines")),
                      MODELE=model)

buoyF= AFFE_CHAR_MECA(FORCE_NODALE=_F(GROUP_NO=("allnodes"),
                                      FX=0,
                                      FY=0,
                                      FZ=0.10794292167421628,
                                      ),
                      MODELE=model)
            
fixed = AFFE_CHAR_MECA(DDL_IMPO=_F(GROUP_NO=("topnodes"),
                                         LIAISON='ENCASTRE'),
                             MODELE=model)
        
sinkF= AFFE_CHAR_MECA(FORCE_NODALE=_F(GROUP_NO=("sinkers"),
                                      FX=0,
                                      FY=0,
                                      FZ=-4.48,
                                      ),
                      MODELE=model)
            
dt=0.1      # time step
# itimes is the total iterations
duration=10      # time step
itimes=100
tend=itimes*dt

listr = DEFI_LIST_REEL(DEBUT=0.0,
                       INTERVALLE=_F(JUSQU_A=tend,PAS=dt))

times = DEFI_LIST_INST(DEFI_LIST=_F(LIST_INST=listr,PAS_MINI=1e-8),
                       METHODE='AUTO')


NODEnumber=meshinfo['numberOfNodes']
Uinput = [[0.76, 0, 0]]
Fnh= []
l=['None']*((NODEnumber+1))
con = meshinfo['netLines']
sur = meshinfo['netSurfaces']
hdm.row = 1000.0  # [kg/m3]   sea water density

    
hydroModel=hdm.screenModel.forceModel("S1",sur,0.347,0.030461125435606473,0.00141)
netWakeModel=hdm.wakeModel.net2net("factor-1",meshinfo['netNodes'],sur,Uinput[0],[0,0,0],0.00141,0.347)
        
with open(cwd+'/positionOutput/element_in_wake.txt', "w") as file:
    file.write(str(netWakeModel.get_element_in_wake()))
file.close()
with open(cwd+'/positionOutput/hydro_elements.txt', "w") as file:
    file.write(str(hydroModel.output_hydro_element()))
file.close()

for k in range(0,itimes):
    time_start=time.time()

    INCLUDE(UNITE=91,INFO=0)

    time_end3=time.time()
    time_str = [k, time_end1-time_start,time_end2-time_start,time_end3-time_start]
    
    with open(cwd + '/timing.txt', 'a+') as output_file:
        output_file.write(str(time_str) + os.linesep)
    output_file.close()

IMPR_RESU(FORMAT='MED',
          RESU=_F(CARA_ELEM=elemprop,
                  LIST_INST=listr,
                  NOM_CHAM=('DEPL' ,'SIEF_ELGA'),
                  # TOUT_CMP=(DEPL','ACCE','VITE' ),
                  RESULTAT=resn,
                  TOUT_CMP='OUI'),
          UNITE=80)

stat = CALC_CHAMP(CONTRAINTE=('SIEF_ELNO', ),
                  FORCE=('REAC_NODA', ),
                  RESULTAT=resn)
        
reac = POST_RELEVE_T(ACTION=_F(GROUP_NO=("topnodes"),
                               INTITULE='sum reactions',
                               MOMENT=('DRX', 'DRY', 'DRZ'),
                               NOM_CHAM=('REAC_NODA'),
                               OPERATION=('EXTRACTION', ),
                               POINT=(0.0, 0.0, 0.0),
                               RESULTANTE=('DX', 'DY', 'DZ'),
                               RESULTAT=stat))
IMPR_TABLE(FORMAT_R='1PE12.3',
           TABLE=reac,
           UNITE=8)

FIN()
        