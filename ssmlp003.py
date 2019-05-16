# Generated with SMOP  0.41
import pandas as pd
import numpy as np
import plotea

# ssmlp003.m

# SSMLP003  - SensoSag Minera Los Pelambres
# by Guillermo Vidal Rudloff - Nov 2018
# Algoritmo de Calculo de SensoSag para SAG MLP
# SSMLPnnn calcula las aceleraciones que reciben los sensores
# instalados en el molino SAG de Minera Los Pelambres

# ssmlp001 calculaba detectmax con máximos de zfilt2.
# ssmlp002 lo hace con otro cruce por cero en zona más estable.

# Ver también SensoSag001 a SensoSag009 para Minera Escondida
# Copyright 2017-2018 Guillermo Vidal Rudloff.

# load Imp011512.csv -ascii
datosabc = pd.read_csv('/home/arielmardones/Documentos/Información Inicial - Guillermo/Senso SAG/Matlab SensoSag/MLP001/2018ago1.csv', names=['tiempo', 'accelx', 'accely', 'accelz'], sep=';')

tiempo = datosabc['tiempo'].values
accelx = datosabc['accelx'].values
accely = datosabc['accely'].values
accelz = datosabc['accelz'].values

# Inicialización de variables
contador = 1
usar = 0
n = len(tiempo)
ciclo = np.array([0])

# Identifica los ciclos que existen
for i in np.arange(n - 1):
    if (tiempo[i + 1] - tiempo[i]) > 0.1 / 60 / 60 / 24:
        contador = contador + 1
        ciclo = np.append(ciclo, [i + 1])

# Calcula los datos que tiene cada ciclo
aux_ciclo = ciclo[1::]
datosporciclo = np.append(aux_ciclo, [n]) - ciclo

# Identifica los ciclos que están completos con todos los datos
ciclocompleto = np.array([1 if dato > 500 else 0 for dato in datosporciclo], dtype=int)

# Preallocation of growing variables
# Reinitiallizing others
t = 0
ejetiempo = np.empty(n, dtype=float)
angx1 = np.empty(n, dtype=float)
angx2 = np.empty(n, dtype=float)
angx3 = np.empty(n, dtype=float)
angy1 = np.empty(n, dtype=float)
angy2 = np.empty(n, dtype=float)
angy3 = np.empty(n, dtype=float)
angz1 = np.empty(n, dtype=float)
angz2 = np.empty(n, dtype=float)
angz3 = np.empty(n, dtype=float)
angxyz1 = np.empty(n, dtype=float)
angxyz2 = np.empty(n, dtype=float)
angxyz3 = np.empty(n, dtype=float)

# Comienza las iteraciones para analizar los ciclos correctos y completos
##############################################
# ACA VOY if usar==0 ==> Goto next loop!!
#############################################

for i in np.arange(n):
    if ciclocompleto[i] == 1:
        t = tiempo[ciclo[i]: ciclo[i + 1]]
        x = accelx[ciclo[i]: ciclo[i + 1]]
        y = accely[ciclo[i]: ciclo[i + 1]]
        z = accelz[ciclo[i]: ciclo[i + 1]]

        # Filtro EJE Z Centrado Promedio 19 datos ==> EJE Z
        zfilt = np.zeros(len(z))
        for j in np.arange(10, len(z) - 9):
            zfilt[j] = np.average(z[j - 9:j + 9 + 1])

        zfilt[0: 10] = zfilt[10]
        zfilt[len(z) - 9: len(z) + 1] = zfilt[len(z) - 10]

        zfilt2 = np.zeros(len(z))
        for j in np.arange(10, len(z) - 9):
            zfilt2[j] = np.average(zfilt[j - 9:j + 9 + 1])

        zfilt2[0: 10] = zfilt2[10]
        zfilt2[len(z) - 9: len(z) + 1] = zfilt2[len(z) - 10]

        # Busca cruce ascendente de zfilt2 por un nivel determinado
        # Permite identificar "cruces por cero" ==> periodo, frec, cero.
        nivelcruce = - 0.5
        detectmax = np.zeros(len(zfilt2) - 1, dtype=int)
        for j in np.arange(len(zfilt2) - 1):
            if zfilt2[j] < nivelcruce < zfilt2[j + 1]:
                detectmax[j] = 1

        # Detecta donde cruce por cero es 1.
        cxcascindex = np.asarray(np.where(detectmax == 1)[0], dtype=int)
        if len(cxcascindex) == 0:
            deltaasc = 0
        elif len(cxcascindex) == 3:  # TODO: PENDIENTES DEL MISMO SIGNO?
            usoa = cxcascindex[1] - cxcascindex[0]
            usob = cxcascindex[2] - cxcascindex[1]
            # usoc = cxcascindex[3] - cxcascindex[1]
            if 250 < usoa < 350:
                cxcascindex = np.array([cxcascindex[1], cxcascindex[2]])
                deltaasc = np.max(cxcascindex) - np.min(cxcascindex)

            if 250 < usob < 350:
                cxcascindex = np.array([cxcascindex[2], cxcascindex[3]])
                deltaasc = np.max(cxcascindex) - np.min(cxcascindex)
        elif len(cxcascindex) > 3:
            deltaasc = 0
        else:
            deltaasc = np.max(cxcascindex) - np.min(cxcascindex)

        # ciclo normal anda en torno a 290.
        if deltaasc < 200:
            usar = 0
        else:
            usar = 1

        # Busca los valores exacto de los cruces por el nivelcruce
        if usar == 1:
            j = np.min(cxcascindex)
            pendizq = zfilt2[j + 1] - zfilt2[j]
            ceroizq = (nivelcruce - zfilt2[j]) / pendizq + j

            j = np.max(cxcascindex)
            pendder = zfilt2[j + 1] - zfilt2[j]
            ceroder = (nivelcruce - zfilt2[j]) / pendder + j

            periodo = ceroder - ceroizq
            frec = 1 / periodo
            omega = (2 * np.pi) / periodo

            maxzf2 = np.max(zfilt2[np.int(ceroizq): np.int(ceroizq) + 150 + 1])

            ejex = np.zeros(np.round(periodo).astype(int), dtype=int)
            sinzz = np.zeros(len(ejex), dtype=float)
            for j in np.arange(len(ejex)):
                ejex[j] = ceroizq + (j - 1)
                sinzz[j] = 1 * np.sin(omega * (ejex[j] - ejex[0])) - (1.0 - maxzf2)

            # busca cruce por nivel del sinzz
            cxccru = np.zeros(1, dtype=int)
            flag = False
            for j in np.arange(len(ejex) - 1):
                if sinzz[j] < nivelcruce < sinzz[j + 1]:
                    if len(cxccru) == 1 and not flag:
                        cxccru[0] = j
                        flag = True
                    else:
                        np.append(cxccru, [j])

            # busca linealiza el cruce exacto por nivelcruce
            if np.max(cxccru) == 0:
                cxccru_min = 100
                usar = 0  # TODO: SALIR DEL CICLO FOR?

            cxccru_min = np.min(cxccru)
            pendizq = sinzz[cxccru_min + 1] - sinzz[cxccru_min]
            ceroizq = (nivelcruce - sinzz[cxccru_min]) / pendizq + cxccru_min
            ejex2 = ejex - ceroizq + 1

            largoejex2 = len(ejex2)
            grados = np.linspace(0, 360, num=largoejex2 - 1, dtype=float)
            pendm = (np.max(grados) - np.min(grados)) / (np.max(ejex2) - np.min(ejex2))
            ysub0 = -np.min(ejex2) * pendm

            # generamos el nuevo eje desde floor(min(ejex2)) a ceil(max(ejex2))
            ejex3 = np.arange(np.floor(np.min(ejex2)), np.ceil(np.max(ejex2)), 1, dtype=int)
            angeje3 = ysub0 + pendm * ejex3
            if np.floor(np.min(ejex2)) < 1:
                usar = 0

        # Solo si usar es diferente a cero, es decir identificó forma de onda a usar
        if usar != 0:
            # Luego decide si usar ascendente o descendente
            #  y plotea el eje X ajustado entre los dos cruces por cero
            if usar == 1:
                t1 = t[np.min(ejex2).astype(int): np.max(ejex2).astype(int) + 1]
                x1 = x[np.min(ejex2).astype(int): np.max(ejex2).astype(int) + 1]
                y1 = y[np.min(ejex2).astype(int): np.max(ejex2).astype(int) + 1]
                z1 = z[np.min(ejex2).astype(int): np.max(ejex2).astype(int) + 1]

            # Calcula t=0 (tinicial) y t=360 tfinal para periodo y frec.
            pendt1 = (t1[1] - t1[0]) / (angeje3[1] - angeje3[0])
            tini = t1[0] - pendt1 * angeje3[0]

            lt1 = len(t1)
            pendt2 = (t1[lt1 - 1] - t1[lt1 - 1 - 1]) / (angeje3[lt1 - 1] - angeje3[lt1 - 1 - 1])
            ysub02 = t1[lt1 - 1 - 1] - pendt2 * angeje3[lt1 - 1 - 1]
            tfin = ysub02 + pendt2 * 360

            periodo = tfin - tini
            frec = 1 / periodo
            omega = (2 * np.pi) / periodo

            fftx = np.abs(np.fft.fft(x1)) / len(x1) * 2
            ffty = np.abs(np.fft.fft(y1)) / len(y1) * 2
            fftz = np.abs(np.fft.fft(z1)) / len(z1) * 2

            angfftx = np.angle(np.fft.fft(x1))
            angffty = np.angle(np.fft.fft(y1))
            angfftz = np.angle(np.fft.fft(z1))
            ajustesinz = angfftz[1] + np.pi / 2
            sinx = fftx[2] * np.sin(omega * (t1 - np.min(t1)) + angfftx[2] + np.pi / 2)
            siny = ffty[2] * np.sin(omega * (t1 - np.min(t1)) + angffty[2] + np.pi / 2)

            # Corrige SINZ
            # Crea una señal sinusoidal de amplitud 1 (2 peak - peak)
            # en fase con la detección de los máximos
            # Corrige nivel para quedar en línea con z1filt.
            # OLD sinz=usar*1*sin(omega*(t1-min(t1)))+mean(z1filt);
            sinz = np.sin(omega * (t1 - np.min(t1)) + angfftz[2] + np.pi / 2 - ajustesinz) - (1 - maxzf2)
            accelx2 = x1 - sinx
            accely2 = y1 - siny
            accelz2 = z1 - sinz

            # Genera el ángulo para graficar en coordenadas polares
            # ==> El ángulo extendido es angeje3.
            grados = angeje3 / 180 * np.pi

            # Calcula los valores absolutos de las aceleraciones
            absaccx = np.abs(accelx2)
            absaccy = np.abs(accely2)
            absaccz = np.abs(accelz2)

            # accelxyz[i, np.arange(len(t1) - 1)] = np.sqrt(accelx2 ** 2 + accely2 ** 2 + accelz2 ** 2)
            magaccel = np.sqrt(accelx2 ** 2 + accely2 ** 2 + accelz2 ** 2)
            fecha = np.min(t1)
            dia = np.floor(fecha)
            hora = np.floor((fecha - dia) * 24)
            minutos = np.floor(fecha - dia - hora / 24 * 24 * 60)
            segundos = np.floor((fecha - dia - hora / 24 - minutos / 24 / 60) * 24 * 60 * 60)

            # frecfull[i] = frec / 24 / 60
            # ------------------------
            plotea.grafica1(grados, z1, sinz, dia, hora, minutos, segundos, magaccel, accelx2, accely2, accelz2, frec / 24 / 60, i)

            # Cálculo de "Centroide" Angular...
            # No se utilizan en plotea -- Ariel_190516
            # newgrad = (grados - np.pi / 2) / np.pi * 180
            # angz2[i] = sum(newgrad * absaccz ** 2) / sum(absaccz ** 2)

            # PAUSE PARA ANALIZAR CASO A CASO
            if usar != 0 and ciclocompleto[i] != 0:
                input()
