
loadr=[]
                
loadr.append( _F(CHARGE=gF), )
        
loadr.append( _F(CHARGE=fixed), )
        
loadr.append( _F(CHARGE=buoyF), )
        
loadr.append( _F(CHARGE=sinkF), )
        
if k == 0:
    resn = DYNA_NON_LINE(CARA_ELEM=elemprop,
                    CHAM_MATER=fieldmat,
                    COMPORTEMENT=(_F(DEFORMATION='GROT_GDEP',
                                    GROUP_MA=('twines', ),
                                    RELATION='CABLE'),
                                 ),
                    CONVERGENCE=_F(ITER_GLOB_MAXI=1000 ,
                                   RESI_GLOB_RELA=2e-05 ),
                    EXCIT=(loadr),
                    OBSERVATION=_F(GROUP_MA='twines',
                                    NOM_CHAM='DEPL',
                                    NOM_CMP=('DX','DY','DZ'),
                                    INST=k+dt,
                                    OBSE_ETAT_INIT='NON'),
                    SCHEMA_TEMPS=_F(FORMULATION='DEPLACEMENT',
                                   SCHEMA="HHT",
                                   ALPHA=-0.1,
                                   ),
                                   #add damping stablize the oscilations Need to study in the future
                    INCREMENT=_F(LIST_INST=times,INST_FIN=(1+k)*dt),
                    MODELE=model)
else:
    Fnh=tuple(Fnh)
    for i in range (1,NODEnumber+1):
        grpno = 'node%01g' %i
        l[i]=AFFE_CHAR_MECA( FORCE_NODALE=_F(GROUP_NO= (grpno),
                         FX= Fnh[i-1][0],
                         FY= Fnh[i-1][1],
                         FZ= Fnh[i-1][2],),
                         MODELE=model)
    for i in range (1,NODEnumber+1):
        loadr.append( _F(CHARGE=l[i],), )

    resn = DYNA_NON_LINE(CARA_ELEM=elemprop,
    				            CHAM_MATER=fieldmat,
    				            reuse=resn,
                    ETAT_INIT=_F(EVOL_NOLI=resn),
                    COMPORTEMENT=(_F(DEFORMATION='GROT_GDEP',
                                    GROUP_MA=('twines', ),
                                    RELATION='CABLE'),
                                 ),
                    CONVERGENCE=_F(ITER_GLOB_MAXI=1000 ,
                                   RESI_GLOB_RELA=2e-05 ),
                    EXCIT=(loadr),
                    OBSERVATION=_F(GROUP_MA='twines',
                                    NOM_CHAM='DEPL',
                                    NOM_CMP=('DX','DY','DZ'),
                                    INST=k+dt,
                                    OBSE_ETAT_INIT='NON'),
                    SCHEMA_TEMPS=_F(FORMULATION='DEPLACEMENT',
                                   SCHEMA="HHT",
                                    ALPHA=-24.3
                                   ),
                                   #add damping stablize the oscilations Need to study in the future
                    INCREMENT=_F(LIST_INST=times,INST_FIN=(1+k)*dt),
                    MODELE=model,
                    )
        
tblp = POST_RELEVE_T(ACTION=(_F(OPERATION='EXTRACTION',      # For Extraction of values
                          INTITULE='Nodal Displacements',    # Name of the table in .resu file
                          RESULTAT=resn,                     # The result from which values will be extracted(STAT_NON_LINE)
                          NOM_CHAM=('DEPL'),                 # Field to extract. DEPL = Displacements
                          #TOUT_CMP='OUI',
                          NOM_CMP=('DX','DY','DZ'),          # Components of DISP to extract
                          GROUP_NO='allnodes',               # Extract only for nodes of group DISP
                          INST=(1+k)*dt,                     # STAT_NON_LINE calculates for 10 INST. I want only last INST
                           ),),
                  );
         
tblp2 = POST_RELEVE_T(ACTION=(_F(OPERATION='EXTRACTION',      # For Extraction of values
                          INTITULE='Nodal Displacements',    # Name of the table in .resu file
                          RESULTAT=resn,                     # The result from which values will be extracted(STAT_NON_LINE)
                          NOM_CHAM=('VITE'),                 # Field to extract. VITE = velocity,
                          #TOUT_CMP='OUI',
                          NOM_CMP=('DX','DY','DZ'),          # Components of DISP to extract
                          GROUP_NO='allnodes',               # Extract only for nodes of group DISP
                          INST=(1+k)*dt,                     # STAT_NON_LINE calculates for 10 INST. I want only last INST
                           ),),
                  );
time_end1=time.time()                  
posi=fsi.get_position_aster(tblp)
velo_nodes=fsi.get_velocity_aster(tblp2)
with open(cwd+'/positionOutput/velo_'+str(round((k)*dt,3))+'.txt', "w") as file:
    file.write(str(velo_nodes))
file.close()

    
if k < itimes-1:
    del Fnh
    
if k*dt< 0:
    force_increasing_factor=k*dt/0
else:
    force_increasing_factor=1.0    
                
U=Uinput[int(k*dt/duration)]
force_on_element=hydroModel.force_on_element(netWakeModel,posi,U)
Fnh=hydroModel.distribute_force(meshinfo['numberOfNodes'],force_increasing_factor)
with open(cwd+'/positionOutput/posi_'+str(round((k)*dt,3))+'.txt', "w") as file:
    file.write(str(posi))
file.close()

        
if ((1+k)*dt)%30.0==0:
    filename = "REPE_OUT/output-"+str((1+k)*dt)+".rmed"
    DEFI_FICHIER(FICHIER=filename, UNITE=180+k,TYPE='BINARY')
    IMPR_RESU(FORMAT='MED',
          UNITE=180+k,
          RESU=_F(CARA_ELEM=elemprop,
                  NOM_CHAM=('DEPL' ,'SIEF_ELGA'),
                  # LIST_INST=listr,
                  INST=(1+k)*dt,
                  RESULTAT=resn,
                  TOUT_CMP='OUI'),
          )
    DEFI_FICHIER(ACTION='LIBERER', UNITE=180+k)


    stat = CALC_CHAMP(CONTRAINTE=('SIEF_ELNO', ),
                      FORCE=('REAC_NODA', ),
                      RESULTAT=resn)
    reac = POST_RELEVE_T(ACTION=_F(GROUP_NO=('topnodes'),
                                   INTITULE='sum reactions',
                                   MOMENT=('DRX', 'DRY', 'DRZ'),
                                   NOM_CHAM=('REAC_NODA'),
                                   OPERATION=('EXTRACTION', ),
                                   POINT=(0.0, 0.0, 0.0),
                                   RESULTANTE=('DX', 'DY', 'DZ'),
                                   RESULTAT=stat))
    IMPR_TABLE(FORMAT_R='1PE12.3',
               TABLE=reac,
               UNITE=9)
    DETRUIRE(CONCEPT=_F( NOM=(stat)))
    DETRUIRE(CONCEPT=_F( NOM=(reac)))
        
time_end2=time.time()    
DETRUIRE(CONCEPT=_F( NOM=(tblp)))
DETRUIRE(CONCEPT=_F( NOM=(tblp2)))
if k!=0:
    if k < itimes-1:
        for i in range (1,NODEnumber+1):
            DETRUIRE(CONCEPT=_F( NOM=(l[i])))
        