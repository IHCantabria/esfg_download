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
MyProxyClient.SSL_METHOD = SSL.TLSv1_2_METHOD

def download_ESGF_data(Open_ID, password, server, project, experiment,time_frequency, variable, domain, path_output):
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
    path_output     : string. Directorio donde se desean guardar los ficheros
    
    Salidas:
    ----------------------
    Ficheros netcdf para cada uno de los escenarios y modelos solicitados
    
    """
    dir_file=__file__
    os.chdir(dir_file[:-16])
    print(dir_file)
    conn = SearchConnection('https://'+server+'/esg-search', distrib=True)
    lm = LogonManager()
    lm.logoff()
    lm.is_logged_on()
    lm.logon_with_openid(Open_ID, password, bootstrap=True)
    lm.is_logged_on()
    if project=='CORDEX':
        ctx = conn.new_context(
        project=project,
        experiment=experiment,
        time_frequency=time_frequency,
        variable=variable,
        domain=domain,)
    else:
        ctx = conn.new_context(
        project=project,
        experiment=experiment,
        time_frequency=time_frequency,
        variable=variable,)
        
    with open('wget-plantilla-ESGF.sh', "r+") as out_file:
        lines = out_file.readlines()
        
    
    
    for ct in tqdm.tqdm(range(ctx.hit_count)):
        files_list=list()
        result = ctx.search()[ct]
        lines[22]="openId='"+Open_ID+"'\n"
        lines[23]="search_url='https://"+server+"/esg-search/wget/?distrib=false&dataset_id="+result.dataset_id+"'\n"
        lines_first=lines[:27]
        lines_end=lines[28:]

        files = result.file_context().search()
        ntcf_ds=list()
        ntcf_name=list()
        for file in files:
            try:
                if variable in file.opendap_url:
                    files_list.append("'"+file.filename+"'"+' '+"'"+file.download_url+"'"+' '+"'"+file.checksum_type+"'"+' '+"'"+file.checksum+"'"+'\n')
            except:
                continue
        if len(files_list)==0:
            continue
        else:
            with open(path_output+"Download.sh", "w") as fh:
                for line in (lines_first+files_list+lines_end):
                    fh.write(line)
                    
            conn = SearchConnection('https://'+server+'/esg-search', distrib=True)
            lm = LogonManager()
            lm.logoff()
            lm.is_logged_on()

            lm.logon_with_openid(Open_ID, password)
            lm.is_logged_on()
            os.chdir(path_output)
            os.system('bash '+path_output+'Download.sh'+' H '+Open_ID+' '+ password)   
        
        




