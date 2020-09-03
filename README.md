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

# Read elevation and flow direction rasters
# ----------------------------
from pysheds.grid import Grid

grid = Grid.from_raster('n30w100_con', data_name='dem')
grid.read_raster('n30w100_dir', data_name='dir')
grid.view('dem')
```