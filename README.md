# esfg_download

🌎 Nos permite descargar masivamente mediante WGET los diferentes ficheros netcdf que contienen los servidores de ESGF sobre cambio climático

## Documentación

Contiene el código generado para descargar los datos de ESFG y además diferentes funciones que permiten extraer una vez descargados, las diferentes variables de los netcdf en puntos o mallas que el usuario quiera
* [ESFG_Download](https://github.com/navass11/esfg_download/blob/master/ESFG/ESFG_Download.py) contiene las funciones para la descarga de los datos.
* [extract_CORDEX_EUR11](https://github.com/navass11/esfg_download/blob/master/ESFG/extract_CORDEX_EUR11.py) extrae los datos sobre una malla o punto dado por el usuario de los datos de CORDEX ya que se encuentran en coordenadas rotadas

## Ejemplo descarga de datos de https://esgf-data.dkrz.de/projects/esgf-dkrz/
```python
from ESFG import ESFG_Download

# Incluimos los datos necesarios
# ----------------------------
OPENID         = 'https://esgf-node.llnl.gov/esgf-idp/openid/username'
PASSWORD       = 'password'
SERVER         = 'esgf-data.dkrz.de'
PROJECT        = 'CORDEX'
EXPERIMENT     = 'rcp26'
TIME_FRECUENCY = 'day'
VARIABLE       = 'tasmax'
DOMAIN         = 'EUR-11'
PATH_OUTPUT    = '/mnt/CORDEX/'

ESFG_Download.download_ESGF_data(OPENID,PASSWORD,SERVER,PROJECT,EXPERIMENT,TIME_FRECUENCY,VARIABLE,DOMAIN,PATH_OUTPUT)

```

## Ejemplo para extraer datos de los fichero netcdf descargados a una malla mas pequeña en coordenadas geográficas
```python
from ESFG import extract_CORDEX_EUR11

path_input ='/mnt/CORDEX/'
path_output ='/home/navass/EUR_11_SPAIN/'

extract_CORDEX_EUR11.extract_CORDEX_EUR11(path_input,path_output=path_output,area=True,lon_min_area=-10,lat_min_area=32.5,lon_max_area=5,lat_max_area=45,
                         point=False,lon_point=None,lat_point=None,name_point=None)
```
![Image of SPAIN](https://github.com/navass11/esfg_download/blob/master/SPAIN_CORDEX.png)

## Contenedor Docker para la descarga de datos
![Image of Docker](https://www.docker.com/sites/default/files/d8/2019-07/horizontal-logo-monochromatic-white.png)

En ocasiones existen problemas con la compatibilidad de librerías según el sistema operativo y la versión de python instalada.
Para evitar este tipo de problemas se ha desarrollado un contenedor Docker en el cual sólo es necesario incluir los datos del usuario y se realiza la descarga.

El contenedor puede ser descargado del siguiente repositorio: [My Docker](https://hub.docker.com/r/navass11/esfg_download)