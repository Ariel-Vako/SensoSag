# Generated with SMOP  0.41
import pandas as pd
import numpy as np

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

tiempo = datosabc['tiempo']
accelx = datosabc['accelx']
accely = datosabc['accely']
accelz = datosabc['accelz']

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
ciclocompleto = np.array([1 if dato > 500 else 0 for dato in datosporciclo])

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
        t = tiempo[ciclo[i], ciclo[i + 1]]
        x = accelx[ciclo[i], ciclo[i + 1]]
        y = accely[ciclo[i], ciclo[i + 1]]
        z = accelz[ciclo[i], ciclo[i + 1]]

        # Filtro EJE Z Centrado Promedio 19 datos ==> EJE Z
        zfilt = zeros(concat([1, length(z)]))
        # ssmlp003.m:136
        for j in arange(10, length(z) - 9).reshape(-1):
            zfilt[j] = (z(j - 9) + z(j - 8) + z(j - 7) + z(j - 6) + z(j - 5) + z(j - 4) + z(j - 3) + z(j - 2) + z(j - 1) + z(j) + z(j + 1) + z(j + 2) + z(j + 3) + z(j + 4) + z(j + 5) + z(j + 6) + z(j + 7) + z(j + 8) + z(j + 9)) / 19
        # ssmlp003.m:138
        zfilt[arange(1, 9)] = dot(zfilt(10), ones(concat([1, 9])))
        # ssmlp003.m:140
        zfilt[arange(length(z) - 9, length(z))] = dot(zfilt(length(z) - 10), ones(concat([1, 10])))
        # ssmlp003.m:141
        zfilt2 = zeros(concat([1, length(z)]))
        # ssmlp003.m:144
        for j in arange(10, length(z) - 9).reshape(-1):
            zfilt2[j] = (zfilt(j - 9) + zfilt(j - 8) + zfilt(j - 7) + zfilt(j - 6) + zfilt(j - 5) + zfilt(j - 4) + zfilt(j - 3) + zfilt(j - 2) + zfilt(j - 1) + zfilt(j) + zfilt(j + 1) + zfilt(j + 2) + zfilt(j + 3) + zfilt(j + 4) + zfilt(j + 5) + zfilt(j + 6) + zfilt(j + 7) + zfilt(j + 8) + zfilt(
                j + 9)) / 19
        # ssmlp003.m:146
        zfilt2[arange(1, 9)] = dot(zfilt(10), ones(concat([1, 9])))
        # ssmlp003.m:148
        zfilt2[arange(length(z) - 9, length(z))] = dot(zfilt(length(z) - 10), ones(concat([1, 10])))

        ## Busca cruce ascendente de zfilt2 por un nivel determinado
        # Permite identificar "cruces por cero" ==> periodo, frec, cero.
        nivelcruce = - 0.5
        # ssmlp003.m:163
        detectmax = zeros(1, length(zfilt2))
        # ssmlp003.m:164
        for j in arange(1, length(zfilt2) - 1).reshape(-1):
            if zfilt2(j + 1) > nivelcruce and zfilt2(j) < nivelcruce:
                detectmax[j] = 1
        # ssmlp003.m:167
        #         plot(t,z,t,zfilt2,t,detectmax)
        ## Detecta donde cruce por cero es 1.
        cxcascindex = find(detectmax)
        # ssmlp003.m:174
        deltaasc = max(cxcascindex) - min(cxcascindex)
        # ssmlp003.m:177
        if isempty(cxcascindex):
            deltaasc = 0
        # ssmlp003.m:181
        # si detectó más de 2 máximos ==> No usar esos datos....(por ahora).
        if length(cxcascindex) > 2:
            deltaasc = 0
        # ssmlp003.m:186
        if deltaasc < 300:
            usar = 0
        # ssmlp003.m:190
        else:
            usar = 1
        # ssmlp003.m:191
        ## busca los valores exacto de los cruces por el nivelcruce
        if usar == 1:
            j = min(cxcascindex)
            # ssmlp003.m:197
            pendizq = (zfilt2(j + 1) - zfilt2(j))
            # ssmlp003.m:198
            ceroizq = (nivelcruce - zfilt2(j)) / pendizq + j
            # ssmlp003.m:199
            j = max(cxcascindex)
            # ssmlp003.m:201
            pendder = (zfilt2(j + 1) - zfilt2(j))
            # ssmlp003.m:202
            ceroder = (nivelcruce - zfilt2(j)) / pendder + j
            # ssmlp003.m:203
            periodo = ceroder - ceroizq
            # ssmlp003.m:205
            frec = 1 / periodo
            # ssmlp003.m:206
            omega = dot(2, pi) / periodo
            # ssmlp003.m:207
            maxzf2 = max(zfilt2(arange(round(ceroizq), round(ceroizq) + 150)))
            # ssmlp003.m:209
            ## maxzf2=max(zfilt2(round(ceroizq):round(ceroizq)+300));  #==> Datos MLP
            ejex = 0
            # ssmlp003.m:212
            for j in arange(1, round(periodo) + 1).reshape(-1):
                ejex[j] = ceroizq + (j - 1)
            # ssmlp003.m:214
            sinzz = dot(1, sin(dot(omega, (ejex - ejex(1))))) - (1 - maxzf2)
            # ssmlp003.m:217
            # busca cruce por nivel del sinzz
            detectcru = zeros(1, length(sinzz))
            # ssmlp003.m:221
            for j in arange(1, length(sinzz) - 1).reshape(-1):
                if sinzz(j + 1) > nivelcruce and sinzz(j) < nivelcruce:
                    detectcru[j] = 1
            # ssmlp003.m:224
            # busca linealiza el cruce exacto por nivelcruce
            if max(detectcru) > 0:
                cxccru = find(detectcru)
            # ssmlp003.m:231
            else:
                cxccru = 100
                # ssmlp003.m:232
                usar = 0
            # ssmlp003.m:233
            cxccru = min(cxccru)
            # ssmlp003.m:236
            pendizq = (sinzz(cxccru + 1) - sinzz(cxccru))
            # ssmlp003.m:239
            ceroizq = (nivelcruce - sinzz(cxccru)) / pendizq + cxccru
            # ssmlp003.m:240
            ejex2 = ejex - ceroizq + 1
            # ssmlp003.m:241
            ##plot(1:540,zfilt2,ejex2,sinzz)
            largoejex2 = length(ejex2)
            # ssmlp003.m:245
            grados = concat([arange(0, 360, 360 / (largoejex2 - 1))])
            # ssmlp003.m:246
            # Tenemos un ejex2 que equivale a un eje grados 0 a 360°.
            # ambos con la misma cantidad de elementos.
            # pero el ejex2 no tiene indices enteros.
            # Hacemos un eje equivalente para coincidir con los datos x1,
            # y1, z1 que tienen indices enteros.
            #             min(grados)
            #             max(grados)
            #             min(ejex2)
            #             max(ejex2)
            #             floor(min(ejex2))
            #             ceil(max(ejex2))
            pendm = (max(grados) - min(grados)) / (max(ejex2) - min(ejex2))
            # ssmlp003.m:262
            ysub0 = dot(- min(ejex2), pendm)
            # ssmlp003.m:263
            # generamos el nuevo eje desde floor(min(ejex2)) a ceil(max(ejex2))
            ejex3 = concat([arange(floor(min(ejex2)), ceil(max(ejex2)), 1)])
            # ssmlp003.m:267
            angeje3 = ysub0 + dot(pendm, ejex3)
            # ssmlp003.m:269
            if floor(min(ejex2)) < 0:
                usar = 0
        # ssmlp003.m:273
        ## Adicional para evitar un cero más abajo en indice de matriz al t1=...
        if floor(min(ejex2)) < 1:
            usar = 0
        # ssmlp003.m:281
        ## Solo si usar es diferente a cero, es decir identificó forma de onda a usar
        if usar != 0:
            ## Luego decide si usar ascendente o descendente
            #  y plotea el eje X ajustado entre los dos cruces por cero
            if usar == 1:
                t1 = t(arange(floor(min(ejex2)), ceil(max(ejex2))))
                # ssmlp003.m:293
                x1 = x(arange(floor(min(ejex2)), ceil(max(ejex2))))
                # ssmlp003.m:294
                y1 = y(arange(floor(min(ejex2)), ceil(max(ejex2))))
                # ssmlp003.m:295
                z1 = z(arange(floor(min(ejex2)), ceil(max(ejex2))))
            # ssmlp003.m:296
            # plot(angeje3,x1,angeje3,y1,angeje3,z1,'-x')
            # Calcula t=0 (tinicial) y t=360 tfinal para periodo y frec.
            pendt1 = (t1(2) - t1(1)) / (angeje3(2) - angeje3(1))
            # ssmlp003.m:303
            tini = t1(1) - dot(pendt1, angeje3(1))
            # ssmlp003.m:304
            lt1 = length(t1)
            # ssmlp003.m:306
            pendt2 = (t1(lt1) - t1(lt1 - 1)) / (angeje3(lt1) - angeje3(lt1 - 1))
            # ssmlp003.m:307
            ysub02 = t1(lt1 - 1) - dot(pendt2, angeje3(lt1 - 1))
            # ssmlp003.m:308
            tfin = ysub02 + dot(pendt2, 360)
            # ssmlp003.m:309
            periodo = tfin - tini
            # ssmlp003.m:311
            frec = 1 / periodo
            # ssmlp003.m:312
            omega = dot(2, pi) / periodo
            # ssmlp003.m:313
            fftx = dot(abs(fft(x1)) / length(x1), 2)
            # ssmlp003.m:316
            ffty = dot(abs(fft(y1)) / length(y1), 2)
            # ssmlp003.m:317
            fftz = dot(abs(fft(z1)) / length(z1), 2)
            # ssmlp003.m:318
            angfftx = angle(fft(x1))
            # ssmlp003.m:320
            angffty = angle(fft(y1))
            # ssmlp003.m:321
            angfftz = angle(fft(z1))
            # ssmlp003.m:322
            ajustesinz = angfftz(2) + pi / 2
            # ssmlp003.m:324
            sinx = dot(dot(usar, fftx(2)), sin(dot(omega, (t1 - min(t1))) + angfftx(2) + pi / 2 - ajustesinz))
            # ssmlp003.m:325
            siny = dot(dot(usar, ffty(2)), sin(dot(omega, (t1 - min(t1))) + angffty(2) + pi / 2 - ajustesinz))
            # ssmlp003.m:326
            # sinz=usar*1*sin(omega*(t1-min(t1))+angfftz(2)+pi/2)+mean(z1);
            ## Corrige SINZ
            # Crea una señal sinusoidal de amplitud 1 (2 peak - peak)
            # en fase con la detección de los máximos
            # Corrige nivel para quedar en línea con z1filt.
            # OLD sinz=usar*1*sin(omega*(t1-min(t1)))+mean(z1filt);
            sinz = dot(dot(usar, 1), sin(dot(omega, (t1 - min(t1))) + angfftz(2) + pi / 2 - ajustesinz)) - (1 - maxzf2)
            # ssmlp003.m:336
            accelx2 = x1 - sinx
            # ssmlp003.m:338
            accely2 = y1 - siny
            # ssmlp003.m:339
            accelz2 = z1 - sinz
            # ssmlp003.m:340
            #             plot(t1,y1,t1,siny)
            #             plot(t1,z1,t1,sinz)
            ## Genera el ángulo para graficar polar
            # ==> El ángulo extendido es angeje3.
            grados = dot((angeje3.T) / 180, pi)
            # ssmlp003.m:352
            ## Calcula los valores absolutos de las aceleraciones
            absaccx = abs(accelx2)
            # ssmlp003.m:356
            absaccy = abs(accely2)
            # ssmlp003.m:357
            absaccz = abs(accelz2)
            # ssmlp003.m:358
            accelxyz[i, arange(1, length(t1))] = sqrt(multiply(accelx2, accelx2) + multiply(accely2, accely2) + multiply(accelz2, accelz2))
            # ssmlp003.m:360
            magaccel = sqrt(multiply(accelx2, accelx2) + multiply(accely2, accely2) + multiply(accelz2, accelz2))
            # ssmlp003.m:361
            fecha = min(t1)
            # ssmlp003.m:363
            dia = floor(fecha)
            # ssmlp003.m:364
            hora = floor(dot((fecha - dia), 24))
            # ssmlp003.m:365
            minutos = floor(dot(dot((fecha - dia - hora / 24), 24), 60))
            # ssmlp003.m:366
            segundos = floor(dot(dot(dot((fecha - dia - hora / 24 - minutos / 24 / 60), 24), 60), 60))
            # ssmlp003.m:367
            frecfull[i] = frec / 24 / 60
            # ssmlp003.m:369
            #             subplot(2,3,1),plot(grados/pi*180-90,z1,grados/pi*180-90,sinz),grid, grid minor, axis([-90 270 -3 3]),title([num2str(dia),' Nov, ',num2str(hora),':',num2str(minutos),':',num2str(segundos)]); ax = gca; ax.XTick = [-90 -60 -30 0 30 60 90 120 150 180 210 240 270 300 330 360];
            #             subplot(2,3,2),plot(grados/pi*180-90,magaccel),grid, grid minor, axis([-90 270 0 20]);title(['Frecuencia : ',num2str(frecfull(i))]); ax = gca; ax.XTick = [-90 -60 -30 0 30 60 90 120 150 180 210 240 270 300 330 360];
            #             subplot(2,3,3),polar(grados-pi/2,20-magaccel);title(['Ciclo : ',num2str(i)]); pax = gca; pax.View = [-90 90];
            #             subplot(2,3,4),polar(grados-pi/2,20-accelx2);title(['Acel Eje X']); pax = gca; pax.View = [-90 90];
            #             subplot(2,3,5),polar(grados-pi/2,20-accely2);title('Acel Eje Y'); pax = gca; pax.View = [-90 90];
            #             subplot(2,3,6),polar(grados-pi/2,20-accelz2);title(['Acel Eje Z']); pax = gca; pax.View = [-90 90];
            #             figure(2);
            #             subplot(2,2,1),plot(t,x,t,y,t,z); grid; grid minor;
            #             subplot(2,2,2),plot(t,z,t,zfilt2,t,detectmax,'*'); axis([min(t) max(t) -1.5 1.5]);title(['Detectmax: ',num2str(length(cxcascindex))]);grid, grid minor;
            #             subplot(2,3,4),plot(grados/pi*180-90,x1,grados/pi*180-90,sinx); grid, grid minor; axis([-90 270 -1.5 1.5]);ax = gca; ax.XTick = [-90 -60 -30 0 30 60 90 120 150 180 210 240 270 300 330 360];
            #             subplot(2,3,5),plot(grados/pi*180-90,y1,grados/pi*180-90,siny); grid, grid minor; axis([-90 270 -1.5 1.5]);ax = gca; ax.XTick = [-90 -60 -30 0 30 60 90 120 150 180 210 240 270 300 330 360];
            #             subplot(2,3,6),plot(grados/pi*180-90,z1,grados/pi*180-90,sinz); grid, grid minor; axis([-90 270 -2.0 1.0]);ax = gca; ax.XTick = [-90 -60 -30 0 30 60 90 120 150 180 210 240 270 300 330 360];
            #             figure(3);
            #             subplot(2,3,1),plot(grados/pi*180-90,accelx2), axis([90 180 -15 15]), grid, grid minor;title(['Acel Eje X']);
            #             subplot(2,3,4),plot(grados(1:length(accelx2)-1)/pi*180-90,abs(accelx2(1:length(accelx2)-1)-accelx2(2:length(accelx2))));axis([90 180 0 25]), grid, grid minor
            #             subplot(2,3,2),plot(grados/pi*180-90,accely2), axis([90 180 -15 15]), grid, grid minor;title(['Acel Eje Y']);
            #             subplot(2,3,5),plot(grados(1:length(accelx2)-1)/pi*180-90,abs(accely2(1:length(accelx2)-1)-accely2(2:length(accelx2))));axis([90 180 0 25]), grid, grid minor
            #             subplot(2,3,3),plot(grados/pi*180-90,accelz2), axis([90 180 -15 15]), grid, grid minor;title(['Acel Eje Z']);
            #             subplot(2,3,6),plot(grados(1:length(accelx2)-1)/pi*180-90,abs(accelz2(1:length(accelx2)-1)-accelz2(2:length(accelx2))));axis([90 180 0 25]), grid, grid minor
            #             figure(4),
            #             subplot(2,1,1),bar(grados/pi*180-90,abs(accelx2.*accely2));axis([90 180 0 1.1*max(abs(accelx2.*accely2))]); grid, grid minor, title(['AccX * AccY ==> Toe 01']);
            #             subplot(2,1,2),bar(grados(2:length(accelx2))/pi*180-90,abs(accelz2(1:length(accelx2)-1)-accelz2(2:length(accelx2))));axis([90 180 0 1.1*max(abs(accelz2(1:length(accelx2)-1)-accelz2(2:length(accelx2))))]), grid, grid minor; title(['Delta Accel Z ==> Toe 02']);
            #             figure(5),
            #             subplot(2,2,1),bar(grados/pi*180-90,abs(accelx2.*accely2));axis([90 180 0 1.1*max(abs(accelx2.*accely2))]); grid, grid minor, title(['AccX * AccY ==> Toe 01']);
            #             subplot(2,2,2),bar(grados/pi*180-90,abs(accely2.*accelz2));axis([90 180 0 1.1*max(abs(accely2.*accelz2))]); grid, grid minor, title(['AccY * AccZ ==> Toe 01']);
            #             subplot(2,2,3),bar(grados/pi*180-90,abs(accelz2.*accelx2));axis([90 180 0 1.1*max(abs(accelz2.*accelx2))]); grid, grid minor, title(['AccZ * AccX ==> Toe 01']);
            #             subplot(2,2,4),bar(grados/pi*180-90,abs(accelx2.*accely2.*accelz2));axis([90 180 0 1.1*max(abs(accelx2.*accely2.*accelz2))]); grid, grid minor, title(['AccX * AccY * AccZ==> Toe 01']);
            plotea
            newgrad = dot((grados - pi / 2) / pi, 180)
            # ssmlp003.m:407
            angz2[i] = sum(multiply(multiply(newgrad, absaccz), absaccz)) / sum(multiply(absaccz, absaccz))
            # ssmlp003.m:408
            title(concat(['Ang Z2: ', num2str(angz2(i))]))
            ##
        #############################################
        ####### ==> ==> ==> ACA VOY #################
        #############################################
    #     resdeltaz=abs(accelz2(1:length(accelx2)-1)-accelz2(2:length(accelx2)));
    #     k2=find(resdeltaz>0.999999*max(resdeltaz));
    #     if (grados(k2+1)/pi*180-90>120 && grados(k2+1)/pi*180-90<165)
    #         maxdeltaz(i)=grados(k2+1)/pi*180-90;
    #     end
    #     resxy=abs(accelx2.*accely2);
    #     k3=find(resxy>0.999999*max(resxy));
    #     if (grados(k3)/pi*180-90>120 && grados(k3)/pi*180-90<165)
    #         maxxy(i)=grados(k3)/pi*180-90;
    #     end
    #     resyz=abs(accely2.*accelz2);
    #     k4=find(resyz>0.999999*max(resyz));
    #     if (grados(k4)/pi*180-90>120 && grados(k4)/pi*180-90<165)
    #         maxyz(i)=grados(k4)/pi*180-90;
    #     end
    #     reszx=abs(accelz2.*accelx2);
    #     k5=find(reszx>0.999999*max(reszx));
    #     if (grados(k5)/pi*180-90>120 && grados(k5)/pi*180-90<165)
    #         maxzx(i)=grados(k5)/pi*180-90;
    #     end
    #     resxyz=abs(accelx2.*accely2.*accelz2);
    #     k6=find(resxyz>0.999999*max(resxyz));
    #     if (grados(k6)/pi*180-90>120 && grados(k6)/pi*180-90<165)
    #         maxxyz(i)=grados(k6)/pi*180-90;
    #     end
    ## PAUSE PARA ANALIZAR CASO A CASO
    if usar != 0 and ciclocompleto(i) != 0:
        pause

figure(8)
subplot(3, 2, 1)
bar(maxdeltaz)
axis(concat([0, length(ciclo), 120, 160]))
title('maxdeltaz')
subplot(3, 2, 2)
bar(maxxy)
axis(concat([0, length(ciclo), 120, 160]))
title('maxxy')
subplot(3, 2, 3)
bar(maxyz)
axis(concat([0, length(ciclo), 120, 160]))
title('maxyz')
subplot(3, 2, 4)
bar(maxzx)
axis(concat([0, length(ciclo), 120, 160]))
title('maxzx')
subplot(3, 2, 5)
bar(maxxyz)
axis(concat([0, length(ciclo), 120, 160]))
title('maxxyz')
subplot(3, 2, 6)
bar(dot(0.6, maxdeltaz) + dot(0.1, maxxy) + dot(0.1, maxyz) + dot(0.1, maxzx) + dot(0.1, maxxyz))
axis(concat([0, length(ciclo), 120, 160]))
title('promedio ponderado')
