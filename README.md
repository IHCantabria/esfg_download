# esfg_download



🌎 Nos permite descargar masivamente mediante WGET los diferentes ficheros netcdf que contienen los servidores de ESGF sobre cambio climático

## Documentación

Contiene el código generado para descargar los datos de ESFG y además diferentes funciones que permiten extraer una vez descargados, las diferentes variables de los netcdf en puntos o mallas que el usuario quiera
* [ESFG_Download](https://github.com/navass11/esfg_download/blob/master/ESFG/ESFG_Download.py) contiene las funciones para la descarga de los datos.
* [extract_CORDEX_EUR11](https://github.com/navass11/esfg_download/blob/master/ESFG/extract_CORDEX_EUR11.py) extrae los datos sobre una malla o punto dado por el usuario de los datos de CORDEX ya que se encuentran en coordenadas rotadas

## Ejemplo
```python
import sys
import os
import ESFG
from ESFG import ESFG_Download

# Incluimos los datos necesarios
# ----------------------------
OPENID         = 'https://esgf-node.llnl.gov/esgf-idp/openid/username'
PASSWORD       = 'password'
SERVER         = 'esgf-data.dkrz.de'
PROJECT        = 'CMIP5'
EXPERIMENT     = 'rcp26'
TIME_FRECUENCY = 'day'
VARIABLE       = 'tasmax'
DOMAIN         = 'EUR-11'
PATH_OUTPUT    = '/mnt/CORDEX/'

```