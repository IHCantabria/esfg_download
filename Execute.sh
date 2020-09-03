#!/bin/bash
echo "Esta función nos permite descargar masivamente mediante WGET los diferentes ficheros netcdf que contienen los servidrores de ESGF sobre cambio climático.
    
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
    Ficheros netcdf para cada uno de los escenarios y modelos solicitados"
sudo chmod 777 Ejemplo.py
python Ejemplo.py