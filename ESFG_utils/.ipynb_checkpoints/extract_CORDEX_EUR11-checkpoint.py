import rotated_grid_transform

 def extract_CORDEX_EUR11(path_input,path_output,area=False,lon_min_area=None,lat_min_area=None,lon_max_area=None,lat_max_area=None,point=True,
                         lon_point=None,lat_point=None,name_point=None):
    """ Esta función permite descargar de G los datos de cambio climático CORDEX de la malla EUR-11 en el punto o area que introduzcamos. La propia función va a elegir el puntos más cercano.
        Además se puede extraer un area seleccionada.
        
        Parámetros:
        --------------------- 
        path_input   : string. Path donde se encuentran los ficheros netcdf descargados
        path_output  : string. Path donde se desean guardar los resultados
        area         : True o False. Opción para saber que tipo de resultados se quiere resultados en un area
        lon_min_area : float. Longitud mínima del area si area está identificada como True
        lat_min_area : float. Latitud mínima del area si area está identificada como True
        lon_max_area : float. Longitud máxima del area si area está identificada como True
        lat_max_area : float. Latitud máxima del area si area está identificada como True
        point        : True o False. Opción para saber que tipo de resultados se quiere resultados en un punto
        lon_point    : float. Longitud del punto 
        lat_point    : float. Latitud del punto
        name_point   : string. Nombre que se quiere dar al punto
        
        Salidas:
        ----------------------
        Coordenadas en sistema WGS84: Fichero CSV para cada uno de los modelos
        Variables para cada modelo: Fichero CSV con los datos extraidos el area o punto introducidos
        
        """
    
    variables=['pr','tasmax','tasmin']
    Experiment=['historical','rcp45','rcp85']
    modelos=[['CNRM-CERFACS-CNRM-CM5','SMHI-RCA4','r1i1p1'],
         ['CNRM-CERFACS-CNRM-CM5','KNMI-RACMO22E','r1i1p1'],
         ['ICHEC-EC-EARTH','SMHI-RCA4','r12i1p1'],
         ['ICHEC-EC-EARTH','KNMI-RACMO22E','r1i1p1'],
         ['ICHEC-EC-EARTH','KNMI-RACMO22E','r12i1p1'],
         ['ICHEC-EC-EARTH','DMI-HIRHAM5','r3i1p1'],
         ['ICHEC-EC-EARTH','CLMcom-CCLM4-8-17','r12i1p1'],
         ['IPSL-IPSL-CM5A-MR','SMHI-RCA4','r1i1p1'],
         ['IPSL-IPSL-CM5A-MR','IPSL-WRF381P','r1i1p1'],
         ['MOHC-HadGEM2-ES','SMHI-RCA4','r1i1p1'],
         ['MOHC-HadGEM2-ES','DMI-HIRHAM5','r1i1p1'],
         ['MOHC-HadGEM2-ES','CLMcom-CCLM4-8-17','r1i1p1'],
         ['MPI-M-MPI-ESM-LR','SMHI-RCA4','r1i1p1'],
         ['MPI-M-MPI-ESM-LR','CLMcom-CCLM4-8-17','r1i1p1'],
         ['NCC-NorESM1-M','DMI-HIRHAM5','r1i1p1']]
    itera=0
    for i in tqdm.tqdm(modelos):
        for ex in Experiment:
            for v in variables:
                direc, root =find(path_input,i[0],i[1],i[2],ex,v)
                if area==True:
                    [lon_min_,lat_min_]= rotated_grid_transform((lon_min_area,lat_min_area), 1, (18,-39.25))
                    [lon_max_,lat_max_]= rotated_grid_transform((lon_max_area,lat_max_area), 1, (18,-39.25))
                    
                    if os.path.exists(path_output+'/'+v+'_EUR-11_'+i[0]+'_'+ex+'_'+i[2]+'_'+i[1]+'_day_'+
                           direc[0][-20:-12]+'_'+direc[-1][-11:-3]+'.csv')==True:
                        continue
                    else:
                        print('### Descargando: '+v+'_EUR-11_'+i[0]+'_'+ex+'_'+i[2]+'_'+i[1]+'_day_'+direc[0][-20:-12]+'_'+direc[-1][-11:-3]+'.csv')
                        da=xr.open_mfdataset(root[0]+'/'+'*.nc')
                        da = da.sel(rlat=slice(lat_min_-1.5, lat_max_+1.5), rlon=slice(lon_min_-0.5, lon_max_+0.5))
                        [XX,YY]=np.meshgrid(da['rlon'].values,da['rlat'].values)
                        [lon_new,lat_new]=rotated_grid_transform((XX,YY), 2, (18,-39.25))
                        try:
                            time=da.indexes['time'].to_datetimeindex()
                        except:
                            time=da.indexes['time']
                        if v=='pr':
                            csv=pd.DataFrame((da[v].values*86400).flatten().reshape(len(time),np.size(XX)),
                                             index=time)
                        else:
                            csv=pd.DataFrame((da[v].values-273).flatten().reshape(len(time),np.size(XX)),
                                             index=time)
                        Coordenadas=pd.DataFrame(index=np.arange(0,len(lon_new.flatten())),columns=['Lon','Lat'])
                        Coordenadas.iloc[:,0]=lon_new.flatten()
                        Coordenadas.iloc[:,1]=lat_new.flatten()

                        csv.to_csv(path_output+v+'_EUR-11_'+i[0]+'_'+ex+'_'+i[2]+'_'+i[1]+'_day_'+
                                   direc[0][-20:-12]+'_'+direc[-1][-11:-3]+'.csv')
                        Coordenadas.to_csv(path_output+'Coordenadas'+'_EUR-11_'+i[0]+'_'+ex+'_'+i[2]+'_'+i[1]+'_day_'+
                                   direc[0][-20:-12]+'_'+direc[-1][-11:-3]+'.csv')
                        if itera==0:
                            fig, ax = plt.subplots(figsize=(14, 10),subplot_kw=dict(projection=ccrs.PlateCarree()))
                            ax.add_feature(cfeature.COASTLINE.with_scale('10m'))
                            ax.add_feature(cfeature.BORDERS.with_scale('10m'))
                            cs=ax.plot(Coordenadas.Lon,Coordenadas.Lat, '.r',alpha=0.5)
                            plt.show()
                        itera=itera+1

                        da.close()
                        
                elif point==True:
                    [lon_min_,lat_min_]= rotated_grid_transform((lon_point,lat_point), 1, (18,-39.25))
                    if os.path.exists(path_output+v+'/'+ex+'/'+v+'_EUR-11_'+i[0]+'_'+ex+'_'+i[2]+'_'+i[1]+'_day_'+
                               direc[0][-20:-12]+'_'+direc[-1][-11:-3]+'_'+name_point+'.csv')==True:
                        continue
                    else:
                        print('### Descargando: '+v+'_EUR-11_'+i[0]+'_'+ex+'_'+i[2]+'_'+i[1]+'_day_'+direc[0][-20:-12]+'_'+direc[-1][-11:-3]+'_'+name_point+'.csv')
                        da=xr.open_mfdataset(root[0]+'/'+'*.nc')
                        da=da.sel(rlat=lat_min_, rlon=lon_min_, method='nearest')
            
                        try:
                            time=da.indexes['time'].to_datetimeindex()
                        except:
                            time=da.indexes['time']
                        if v=='pr':
                            csv=pd.DataFrame((da[v].values*86400).flatten(),index=time)
                        else:
                            csv=pd.DataFrame((da[v].values-273).flatten(),index=time)
                        
                        csv.to_csv(path_output+v+'_EUR-11_'+i[0]+'_'+ex+'_'+i[2]+'_'+i[1]+'_day_'+
                                   direc[0][-20:-12]+'_'+direc[-1][-11:-3]+'_'+name_point+'.csv')

                        da.close()
