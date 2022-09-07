# _Autor:_    __Salavador Navas__
# _Revisión:_ __05/08/2020__


import os
import xarray as xr
from pyesgf.logon import LogonManager
from pyesgf.search import SearchConnection
import tqdm
import numpy as np
from netCDF4 import Dataset
from math import *
import sys
from myproxy.client import MyProxyClient
from OpenSSL import SSL
import requests
import cordex as cx
from ESFG_utils import rotated_grid_transform

MyProxyClient.SSL_METHOD = SSL.TLSv1_2_METHOD
os.environ['HDF5_USE_FILE_LOCKING'] = 'FALSE'

def download_data(path_output,url,size):
    import time
    headers = requests.head(url, headers={'accept-encoding': ''}).headers
    r = requests.get(url, allow_redirects=True, stream=True,  verify=False,timeout=5)
    file_size = size
    downloaded = 0
    start = last_print = time.time()
    #name = path_output+v+'/'+sc+'/'+'R_'+v+'_'+sc+'_COR_SIG.zip'
    with open(path_output, 'wb') as fp:
        for chunk in r.iter_content(chunk_size=4096 * 64):
            downloaded += fp.write(chunk)
            now = time.time()
            if now - last_print >= 1:
                pct_done = round(downloaded / file_size * 100)
                speed = round(downloaded / (now - start) / 1024)
                print(f"Download {pct_done} % done, avg speed {speed} kbps")
                last_print = time.time()


def download_ESGF_data(Open_ID, password, server, project, experiment,time_frequency, variables, domain,lon_min,lat_min,lon_max,lat_max, path_output):
    """Esta función nos permite descargar masivamente mediante WGET los diferentes ficheros netcdf que contienen los servidrores de ESGF sobre cambio climático.
    
    El servidor por defecto que se va a utilizar es: https://esgf-data.dkrz.de/projects/esgf-dkrz/.
    
    Parámetros:
    ---------------------
    Open_ID         : string. ID de tu usuario para acceder a la base de datos correspondiente del servidor
    password        : string. Contraseña correspondiente a la ID
    server          : string. Servidor del que se desea descargar la información. Ejemplo: https://esgf-data.dkrz.de/esg-search
    project         : string. Proyecto dentro del servidor del que se quiere descargar los datos. Ejemplo: CORDEX, CMIP5, CMIP6
    experiment      : string. Escenarios de cambio climático. Ejemplo: historical, rcp26, rcp45, rcp85
    time_frequency  : string. Frecuencia de la base de datos que se quiere. Ejemplo: 1hr, 6hr, day, mon
    variable        : string. Variable que se desea descargar: tasmax, tasmin, pr 
    domain          : string. En el caso de que se desee descargar CORDEX, se debe de incluir el nombre de la malla. Ejemplo: EUR-11
    lon_min         : float. Longitud mínima de la malla de estudio que se quiere descargar
    lat_min         : float. Latitud mínima de la malla de estudio que se quiere descargar
    lon_max         : float. Longitud máxima de la malla de estudio que se quiere descargar
    lat_mac         : float. En el caso de que se desee descargar CORDEX, se debe de incluir el nombre de la malla. Ejemplo: EUR-11
    path_output     : float. Directorio donde se desean guardar los ficheros
    
    Salidas:
    ----------------------
    Ficheros netcdf para cada uno de los escenarios y modelos solicitados
    
    """
    # dir_file=__file__
    # os.chdir(dir_file[:-16])
    # print(dir_file)
    conn = SearchConnection('https://'+server+'/esg-search', distrib=True)
    
    
        
    # with open('wget-plantilla-ESGF.sh', "r+") as out_file:
    #     lines = out_file.readlines()
    for exp in experiment:
        for v in variables:
            not_downloaded=True
            try:
                if project=='CORDEX':
                    lm = LogonManager()
                    lm.logoff()
                    lm.is_logged_on()
                    lm.logon_with_openid(Open_ID, password, bootstrap=True)
                    lm.is_logged_on()
                    
                    ctx = conn.new_context(
                    project=project,
                    experiment=experiment,
                    time_frequency=time_frequency,
                    variable=v,
                    domain=domain,latest=True)
                    
                    info = cx.domain_info("EUR-11")
                    [lon_min_,lat_min_]= rotated_grid_transform((lon_min,lat_min), 1, (180+info['pollon'],-info['pollat']))
                    [lon_max_,lat_max_]= rotated_grid_transform((lon_max,lat_max), 1, (180+info['pollon'],-info['pollat']))
                else:
                    ctx = conn.new_context(
                    project=project,
                    experiment=experiment,
                    time_frequency=time_frequency,
                    variable=v,latest=True)
                if ctx.hit_count==0:
                    continue
                else:
                    variable=v
                    print('######### Descargando variable '+v+' del experimento '+exp)
                    for i in tqdm.tqdm(range(0, ctx.hit_count)):
                        result = ctx.search()[i]
                        result.dataset_id
                        files = result.file_context().search()
                        if len(files)==0:
                            continue
                        else:
                            for file in files:
                                if variable +'_' in file.download_url:
                                    url=file.download_url

                                    if os.path.exists(path_output+variable+'/'+file.filename):
                                        not_downloaded=False
                                    else:
                                        not_downloaded=True
                                    nnn=0
                                    while not_downloaded:
                                        try:
                                            print('...................Descargando '+url)
                                            download_data(path_output+variable+'/'+file.filename+'_erase',file.download_url,file.size)
                                            ds = xr.open_dataset(path_output+variable+'/'+file.filename+'_erase')
                                            
                                            if project=='CORDEX':
                                                da = ds[variable].load()
                                                var_ds=list()
                                                for k in ds[variable].sizes:
                                                    var_ds.append(k)
                                                if 'rlon' in var_ds:
                                                    da = da.sel(rlat=slice(lat_min_-1.5, lat_max_+1.5), 
                                                                rlon=slice(lon_min_-0.5, lon_max_+0.5))
                                                    print('...................Descargando '+url)

                                                elif 'lon' in var_ds:
                                                    da = da.sel(lat=slice(lat_min, lat_max), lon=slice(lon_min, lon_max))
                                                    print('...................Descargando '+url)
                                                    
                                                else:
                                                    print('Sistema de coordenadas no válido')
                                                    not_downloaded=False
                                            else:
                                                
                                            #ds = xr.open_dataset(url, engine = "netcdf4")
                                                ds['lon']=ds.lon-180
                                                da = ds[variable].load()
                                                da = da.sel(lat = slice(lat_min, lat_max), lon = da.lon[(da.lon>lon_min) & (da.lon<lon_max)].data)
                                            #da = da.assign_coords(lon = (((da.lon + 180) % 360) - 180))
                                            #da = da.roll(lon = (-np.nonzero(da.lon.values < 0)[0][0]), roll_coords=True)
                                            da.to_netcdf(path_output+variable+'/'+file.filename)
                                            da.close()
                                            ds.close()
                                            os.remove(path_output+variable+'/'+file.filename+'_erase')
                                            not_downloaded=False
                                        except:
                                            print('Try again...')
                                            nnn=nnn+1
                                            if nnn>10:
                                                print('No se ha descargado el fichero')
                                                break
            except:
                continue         
                
    
    
        




