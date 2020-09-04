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
![Image of Docker](https://www.google.com/search?q=docker&rlz=1C1GCEA_enES884ES884&sxsrf=ALeKk02pMGIY5uNolKBvJo889_3kGs14MA:1599202210705&tbm=isch&source=iu&ictx=1&fir=2nMpoCD-VQyHIM%252CDb2pxDwN0aZI0M%252C%252Fm%252F0wkcjgj&vet=1&usg=AI4_-kS7Bsax5UsIovhphD9Ur5tbMvEE2Q&sa=X&ved=2ahUKEwieqsW99M7rAhVnCWMBHdHODB0Q_B16BAgYEAI&biw=1920&bih=888#imgrc=2nMpoCD-VQyHIM)
En ocasiones existen problemas con la compatibilidad de librerías según el sistema operativo y la versión de python instalada.
Para evitar este tipo de problemas se ha desarrollado un contenedor Docker en el cual sólo es necesario incluir los datos del usuario y se realiza la descarga.