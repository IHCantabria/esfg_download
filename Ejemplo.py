import sys
import os
import ESFG
from ESFG import ESFG_Download

#OPENID         = 'https://esgf-node.llnl.gov/esgf-idp/openid/s.navas11'
#PASSWORD       = 'Ab1-JZgUndyx'
#SERVER         = 'esgf-data.dkrz.de'
#PROJECT        = 'CMIP5'
#EXPERIMENT     = 'rcp26'
#TIME_FRECUENCY = 'day'
#VARIABLE       = 'tasmax'
#DOMAIN         = 'EUR-11'
#PATH_OUTPUT    = '/mnt/CORDEX/'

OPENID         = str(input("Enter the OPENID: "))
PASSWORD       = str(input("Enter the PASSWORD: "))
SERVER         = str(input("Enter the SERVER: "))
PROJECT        = str(input("Enter the PROJECT: "))
EXPERIMENT     = str(input("Enter the EXPERIMENT: "))
TIME_FRECUENCY = str(input("Enter the TIME_FRECUENCY: "))
VARIABLE       = str(input("Enter the VARIABLE: "))
DOMAIN         = str(input("Enter the DOMAIN: "))
PATH_OUTPUT    = str(input("Enter the PATH_OUTPUT: "))

ESFG_Download.download_ESGF_data(OPENID,PASSWORD,SERVER,PROJECT,EXPERIMENT,TIME_FRECUENCY,VARIABLE,DOMAIN,PATH_OUTPUT)