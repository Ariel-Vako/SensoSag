# !/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

"""Consulta Archivos SVIA MQTT"""
__author__ = "Cristofer Robles"
__copyright__ = "Copyright 2018-07-20, highservice"
__version__ = "1.0"

import sys, argparse, csv, os, MySQLdb, time
from datetime import datetime, timedelta
import struct

db = MySQLdb.connect("hstech.sinc.cl", "jsanhueza", "Hstech2018.-)", "ssi_mlp_sag2")
cursor = db.cursor()

# query2 = "SELECT dataX FROM Data_Sensor where fecha_reg = '2018-11-21 18:24:45.080333' ORDER BY fecha_reg DESC"

# cursor.execute(query2)

cursor.execute("SELECT dataZ,estado_data FROM Data_Sensor ORDER BY fecha_reg DESC LIMIT 1 ")

results = cursor.fetchall()

print(results)

lista_y = []
# for row in results:
#    for x in range(540):
#        lista_y.append((ord(row[0][x*2])<<8)+ord(row[0][x*2+1])-2**15)

#    print lista_y
#   exit()
