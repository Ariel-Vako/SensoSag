%% SSMLP003  - SensoSag Minera Los Pelambres
% by Guillermo Vidal Rudloff - Nov 2018
% Algoritmo de Calculo de SensoSag para SAG MLP
% SSMLPnnn calcula las aceleraciones que reciben los sensores
% instalados en el molino SAG de Minera Los Pelambres
%
% ssmlp001 calculaba detectmax con máximos de zfilt2.
% ssmlp002 lo hace con otro cruce por cero en zona más estable.
%
% Ver también SensoSag001 a SensoSag009 para Minera Escondida
% Copyright 2017-2018 Guillermo Vidal Rudloff.

%load Imp011512.csv -ascii

% prompt = 'Qué impactómetro es ';
% imp = input(prompt);

tiempo=datosabc(:,1);
accelx=datosabc(:,2);
accely=datosabc(:,3);
accelz=datosabc(:,4);

contador=1;
usar=0;
clear ciclo

ciclo(contador)=1;

%% Identifica los ciclos que existen
for i=2:length(tiempo);
    if tiempo(i)-tiempo(i-1)>0.1/60/60/24
        contador=contador+1;
        ciclo(contador)=i;
    end
end

datosporciclo=zeros(1,length(ciclo)); %% Preallocating

%% Calcula los datos que tiene cada ciclo
for i=2:length(ciclo)
    datosporciclo(i-1)=ciclo(i)-ciclo(i-1);
end

%% Identifica los ciclos que están completos con todos los datos
ciclocompleto=zeros([1 length(datosporciclo)]);
for i=1:length(datosporciclo)
    if datosporciclo(i)>500;  %% Ciclo 100% full son 544 datos!!!
        ciclocompleto(i)=1;
    end
end

% plot(tiempo(1:544),accelx(1:544),tiempo(1:544),accely(1:544),tiempo(1:544),accelz(1:544))
% plot(tiempo(ciclo(1):ciclo(2)-1),accelx(ciclo(1):ciclo(2)-1),tiempo(ciclo(1):ciclo(2)-1),accely(ciclo(1):ciclo(2)-1),tiempo(ciclo(1):ciclo(2)-1),accelz(ciclo(1):ciclo(2)-1))

%% Prallocation of growing variables
% Reinitiallizing others

t=0;
% energ=zeros(length(ciclo),3);
% largox1=zeros(length(ciclo),3);
%
% fuerzafull=zeros(length(ciclo),31);
%
% frecfull=null(length(ciclo),1);
%
% maximpx=zeros(length(ciclo),1);
% minimpx=zeros(length(ciclo),1);
% maximpy=zeros(length(ciclo),1);
% minimpy=zeros(length(ciclo),1);
% maximpz=zeros(length(ciclo),1);
% minimpz=zeros(length(ciclo),1);
%
% impposx=zeros(length(ciclo),1);
% impnegx=zeros(length(ciclo),1);
% impposy=zeros(length(ciclo),1);
% impnegy=zeros(length(ciclo),1);
% impposz=zeros(length(ciclo),1);
% impnegz=zeros(length(ciclo),1);
%
% bigimpposx=zeros(length(ciclo),1);
% bigimpnegx=zeros(length(ciclo),1);
% bigimpposy=zeros(length(ciclo),1);
% bigimpnegy=zeros(length(ciclo),1);
% bigimpposz=zeros(length(ciclo),1);
% bigimpnegz=zeros(length(ciclo),1);
%
% fecha=NaN(length(ciclo),1);
% impactos=NaN(length(ciclo),1);
% qimpactos=null(length(ciclo),1);
%
% factorcrestax=zeros(length(ciclo),1);
% factorcrestay=zeros(length(ciclo),1);
% factorcrestaz=zeros(length(ciclo),1);
%
% accelxyz=null(length(ciclo),400);
% angulodes=null(length(ciclo),1);
%
% fftmagxyz=null(length(ciclo),400);
%
% rmsaccel=null(length(ciclo),1);

% maxdeltaz=null(length(ciclo),1);
% maxxy=null(length(ciclo),1);
% maxyz=null(length(ciclo),1);
% maxzx=null(length(ciclo),1);
% maxxyz=null(length(ciclo),1);

ejetiempo=null(length(ciclo),1);

angx1=null(length(ciclo),1);
angx2=null(length(ciclo),1);
angx3=null(length(ciclo),1);
angy1=null(length(ciclo),1);
angy2=null(length(ciclo),1);
angy3=null(length(ciclo),1);
angz1=null(length(ciclo),1);
angz2=null(length(ciclo),1);
angz3=null(length(ciclo),1);
angxyz1=null(length(ciclo),1);
angxyz2=null(length(ciclo),1);
angxyz3=null(length(ciclo),1);

%% Comienza las iteraciones para analizar los ciclos correctos y completos

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% ACA VOY if usar==0 ==> Goto next loop!!
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

for i=1:1:length(ciclo); % Máximo contador!! o length(ciclo)
    %         for i=303:303; % Máximo contador!! o length(ciclo)
    %     figure,
    %     plot(tiempo(ciclo(i):ciclo(i+1)-1),accelx(ciclo(i):ciclo(i+1)-1),tiempo(ciclo(i):ciclo(i+1)-1),accely(ciclo(i):ciclo(i+1)-1),tiempo(ciclo(i):ciclo(i+1)-1),accelz(ciclo(i):ciclo(i+1)-1))
    if ciclocompleto(i)==1;
        
        t=tiempo(ciclo(i):ciclo(i+1)-1);
        x=accelx(ciclo(i):ciclo(i+1)-1);
        y=accely(ciclo(i):ciclo(i+1)-1);
        z=accelz(ciclo(i):ciclo(i+1)-1);
        
        %     figure,
        %     plot(t,x,t,y,t,z);
        
        % Filtro Centrado Promedio 9 datos
        % xfilt=zeros([1 length(x)]);
        % for j=5:length(x)-4;
        %     xfilt(j)=(x(j-4)+x(j-3)+x(j-2)+x(j-1)+x(j)+x(j+1)+x(j+2)+x(j+3)+x(j+4))/9;
        % end
        
        %% Filtro EJE Z Centrado Promedio 19 datos ==> EJE Z
        
        zfilt=zeros([1 length(z)]);
        for j=10:length(z)-9;
            zfilt(j)=(z(j-9)+z(j-8)+z(j-7)+z(j-6)+z(j-5)+z(j-4)+z(j-3)+z(j-2)+z(j-1)+z(j)+z(j+1)+z(j+2)+z(j+3)+z(j+4)+z(j+5)+z(j+6)+z(j+7)+z(j+8)+z(j+9))/19;
        end
        zfilt(1:9)=zfilt(10)*ones([1 9]);
        zfilt(length(z)-9:length(z))=zfilt(length(z)-10)*ones([1 10]);
        
        % Rekete Filtro Centrado Promedio 19 datos
        zfilt2=zeros([1 length(z)]);
        for j=10:length(z)-9;
            zfilt2(j)=(zfilt(j-9)+zfilt(j-8)+zfilt(j-7)+zfilt(j-6)+zfilt(j-5)+zfilt(j-4)+zfilt(j-3)+zfilt(j-2)+zfilt(j-1)+zfilt(j)+zfilt(j+1)+zfilt(j+2)+zfilt(j+3)+zfilt(j+4)+zfilt(j+5)+zfilt(j+6)+zfilt(j+7)+zfilt(j+8)+zfilt(j+9))/19;
        end
        zfilt2(1:9)=zfilt(10)*ones([1 9]);
        zfilt2(length(z)-9:length(z))=zfilt(length(z)-10)*ones([1 10]);
        
        %         % Triple Filtrado Centrado Promedio 19 datos
        %         zfilt3=zeros([1 length(z)]);
        %         for j=10:length(z)-9;
        %             zfilt3(j)=(zfilt2(j-9)+zfilt2(j-8)+zfilt2(j-7)+zfilt2(j-6)+zfilt2(j-5)+zfilt2(j-4)+zfilt2(j-3)+zfilt2(j-2)+zfilt2(j-1)+zfilt2(j)+zfilt2(j+1)+zfilt2(j+2)+zfilt2(j+3)+zfilt2(j+4)+zfilt2(j+5)+zfilt2(j+6)+zfilt2(j+7)+zfilt2(j+8)+zfilt2(j+9))/19;
        %         end
        %         zfilt3(1:9)=zfilt2(10)*ones([1 9]);
        %         zfilt3(length(z)-9:length(z))=zfilt2(length(z)-10)*ones([1 10]);
        
        %         plot(t,z,t,zfilt2)
        
        %% Busca cruce ascendente de zfilt2 por un nivel determinado
        % Permite identificar "cruces por cero" ==> periodo, frec, cero.
        nivelcruce=-0.5;
        detectmax=zeros(1,length(zfilt2));
        for j=1:length(zfilt2)-1;
            if zfilt2(j+1)>nivelcruce && zfilt2(j)<nivelcruce
                detectmax(j)=1;
            end
        end
        
        %         plot(t,z,t,zfilt2,t,detectmax)
        
        %% Detecta donde cruce por cero es 1.
        cxcascindex=find(detectmax);
        
        %% Y calcula la cantidad de tiempo entre dos cruces por cero
        deltaasc=max(cxcascindex)-min(cxcascindex);
        
        pico(i)=length(cxcascindex); 
        
        % si solo detectó un máximo ==> No usar esos datos....(por ahora).
        if isempty(cxcascindex)
            deltaasc=0;
        end
        
        % si detectó más de 2 máximos ==> No usar esos datos....(por ahora).
        if length(cxcascindex)>2;
            deltaasc=0;
        end
        
        % si detectó 3 máximos ==> Ver si es 1-2 o 2-3. Caso 1-3 ?? 
        if length(cxcascindex)==3;
            
            usoa=cxcascindex(2)-cxcascindex(1);
            usob=cxcascindex(3)-cxcascindex(2);
            usoc=cxcascindex(3)-cxcascindex(1);
            if usoa>250 && usoa<350
                cxcascindex=[cxcascindex(1),cxcascindex(2)];
                deltaasc=max(cxcascindex)-min(cxcascindex);
            end
            
            if usob>250 && usob<350
                cxcascindex=[cxcascindex(2),cxcascindex(3)];
                deltaasc=max(cxcascindex)-min(cxcascindex);
            end
            
%             if usoc>250 && usoc<350
%                 cxcascindex=[cxcascindex(1),cxcascindex(3)];
%                 deltaasc=max(cxcascindex)-min(cxcascindex);
%             end
            
        end
            
                
        
        % Acá define si USAR o NO USAR.
        % Los deltaasc=0 también son NO USAR.
        if deltaasc<200 % ciclo normal anda en torno a 290.
            usar=0;
        else  usar=1;
        end
        
        
        %% busca los valores exacto de los cruces por el nivelcruce
        if usar==1;
            j=min(cxcascindex);
            pendizq=(zfilt2(j+1)-zfilt2(j));
            ceroizq=(nivelcruce-zfilt2(j))/pendizq+j;
            
            j=max(cxcascindex);
            pendder=(zfilt2(j+1)-zfilt2(j));
            ceroder=(nivelcruce-zfilt2(j))/pendder+j;
            
            periodo=ceroder-ceroizq;
            frec=1/periodo;
            omega=2*pi/periodo;
            
            maxzf2=max(zfilt2(round(ceroizq):round(ceroizq)+150));
            %maxzf2=max(zfilt2(round(ceroizq):round(ceroizq)+250));
            
            ejex=0;
            for j=1:round(periodo)+1;
                ejex(j)=ceroizq+(j-1);
            end
            
            sinzz=1*sin(omega*(ejex-ejex(1)))-(1-maxzf2); % ==> sinzz parte de angulo cero
            
            % busca cruce por nivel del sinzz
            
            detectcru=zeros(1,length(sinzz));
            for j=1:length(sinzz)-1;
                if sinzz(j+1)>nivelcruce && sinzz(j)<nivelcruce
                    detectcru(j)=1;
                end
            end
            
            % busca linealiza el cruce exacto por nivelcruce
            
            if max(detectcru)>0
                cxccru=find(detectcru);
            else cxccru=100;
                usar=0;
            end
            
            cxccru=min(cxccru); %%% Si y solo si aparece más de un cruce !!! Toma el menor.
            
            
            pendizq=(sinzz(cxccru+1)-sinzz(cxccru));
            ceroizq=(nivelcruce-sinzz(cxccru))/pendizq+cxccru;
            ejex2=ejex-ceroizq+1;       % ==> corrige eje x para sinzz
            
            %%plot(1:540,zfilt2,ejex2,sinzz)
            
            largoejex2=length(ejex2);
            grados=[0:360/(largoejex2-1):360];
            %plot(grados,sinzz+(1-maxzf2),'-*'), grid;
            
            % Tenemos un ejex2 que equivale a un eje grados 0 a 360°.
            % ambos con la misma cantidad de elementos.
            % pero el ejex2 no tiene indices enteros.
            % Hacemos un eje equivalente para coincidir con los datos x1,
            % y1, z1 que tienen indices enteros.
            
            %             min(grados)
            %             max(grados)
            %             min(ejex2)
            %             max(ejex2)
            %             floor(min(ejex2))
            %             ceil(max(ejex2))
            
            pendm=(max(grados)-min(grados))/(max(ejex2)-min(ejex2));
            ysub0=-min(ejex2)*pendm;
            %ysub0+min(ejex2)*pendm % ==> Debe dar cero.
            
            % generamos el nuevo eje desde floor(min(ejex2)) a ceil(max(ejex2))
            ejex3=[floor(min(ejex2)):1:ceil(max(ejex2))];
            % angulos para eje3.
            angeje3=ysub0+pendm*ejex3;
            
            %si el indice del eje da negativo--- ==> Usar = 0!
            if floor(min(ejex2))<1
                usar=0;
            end
            
            
        end  % termina if usar==1;
        
        
        %% Solo si usar es diferente a cero, es decir identificó forma de onda a usar
        if usar~=0
            
            
            %% Luego decide si usar ascendente o descendente
            %  y plotea el eje X ajustado entre los dos cruces por cero
                       
            
            if usar==1;
                t1=t(floor(min(ejex2)):ceil(max(ejex2)));
                x1=x(floor(min(ejex2)):ceil(max(ejex2)));
                y1=y(floor(min(ejex2)):ceil(max(ejex2)));
                z1=z(floor(min(ejex2)):ceil(max(ejex2)));
            end
            
            %plot(angeje3,x1,angeje3,y1,angeje3,z1,'-x')
            
            % Calcula t=0 (tinicial) y t=360 tfinal para periodo y frec.
            
            pendt1=(t1(2)-t1(1))/(angeje3(2)-angeje3(1));
            tini=t1(1)-pendt1*angeje3(1);
            
            lt1=length(t1);
            pendt2=(t1(lt1)-t1(lt1-1))/(angeje3(lt1)-angeje3(lt1-1));
            ysub02=t1(lt1-1)-pendt2*angeje3(lt1-1);
            tfin=ysub02+pendt2*360;
            
            periodo=tfin-tini;
            frec=1/periodo;
            omega=2*pi/periodo;
            
            % calcula FFT para eliminar sinusoidal
            fftx=abs(fft(x1))/length(x1)*2;
            ffty=abs(fft(y1))/length(y1)*2;
            fftz=abs(fft(z1))/length(z1)*2;
            
            angfftx=angle(fft(x1));
            angffty=angle(fft(y1));
            angfftz=angle(fft(z1));
            
            ajustesinz=angfftz(2)+pi/2;
            sinx=usar*fftx(2)*sin(omega*(t1-min(t1))+angfftx(2)+pi/2);
            siny=usar*ffty(2)*sin(omega*(t1-min(t1))+angffty(2)+pi/2);
            %sinz=usar*fftz(2)*sin(omega*(t1-min(t1))+angfftz(2)+pi/2)+mean(z1);
            %sinz=usar*1*sin(omega*(t1-min(t1))+angfftz(2)+pi/2)+mean(z1);
            
            %% Corrige SINZ
            % Crea una señal sinusoidal de amplitud 1 (2 peak - peak)
            % en fase con la detección de los máximos
            % Corrige nivel para quedar en línea con z1filt.
            % OLD sinz=usar*1*sin(omega*(t1-min(t1)))+mean(z1filt);
            
            sinz=usar*1*sin(omega*(t1-min(t1))+angfftz(2)+pi/2-ajustesinz)-(1-maxzf2); %%
            
            accelx2=x1-sinx;
            accely2=y1-siny;
            accelz2=z1-sinz;
            
            
            %             plot(t1,x1,t1,sinx)
            %             plot(t1,y1,t1,siny)
            %             plot(t1,z1,t1,sinz)
            %
            
            
            %% Genera el ángulo para graficar polar
            % ==> El ángulo extendido es angeje3.
            
            grados=(angeje3')/180*pi;
            %%grados=(grados+90)'/180*pi;
            
            %% Calcula los valores absolutos de las aceleraciones
            absaccx=abs(accelx2);
            absaccy=abs(accely2);
            absaccz=abs(accelz2);
            
            accelxyz(i,1:length(t1))=sqrt(accelx2.*accelx2+accely2.*accely2+accelz2.*accelz2);
            magaccel=sqrt(accelx2.*accelx2+accely2.*accely2+accelz2.*accelz2);
            
            fecha=min(t1);
            dia=floor(fecha);
            hora=floor((fecha-dia)*24);
            minutos=floor((fecha-dia-hora/24)*24*60);
            segundos=floor((fecha-dia-hora/24-minutos/24/60)*24*60*60);
            
            frecfull(i)=frec/24/60;
            ejetiempo(i)=fecha;
            
            
            % %             plotea;
            
            %% Cálculo de "Centroide" angular...
            
            newgrad=(grados-pi/2)/pi*180;  %% Grados de -90 a 270° en grados.
            
            
            angx1(i)=sum(newgrad.*absaccx)/sum(absaccx);
            angx2(i)=sum(newgrad.*absaccx.*absaccx)/sum(absaccx.*absaccx);
            angx3(i)=sum(newgrad.*absaccx.*absaccx.*absaccx)/sum(absaccx.*absaccx.*absaccx);
            
            angy1(i)=sum(newgrad.*absaccy)/sum(absaccy);
            angy2(i)=sum(newgrad.*absaccy.*absaccy)/sum(absaccy.*absaccy);
            angy3(i)=sum(newgrad.*absaccy.*absaccy.*absaccy)/sum(absaccy.*absaccy.*absaccy);
            
            angz1(i)=sum(newgrad.*absaccz)/sum(absaccz);
            angz2(i)=sum(newgrad.*absaccz.*absaccz)/sum(absaccz.*absaccz);
            angz3(i)=sum(newgrad.*absaccz.*absaccz.*absaccz)/sum(absaccz.*absaccz.*absaccz);
            
            angxyz1(i)=sum(newgrad.*magaccel)/sum(magaccel);
            angxyz2(i)=sum(newgrad.*magaccel.*magaccel)/sum(magaccel.*magaccel);
            angxyz3(i)=sum(newgrad.*magaccel.*magaccel.*magaccel)/sum(magaccel.*magaccel.*magaccel);
            
            %             [angx1(i),angx2(i),angx3(i)]
            %             [angy1(i),angy2(i),angy3(i)]
            %             [angz1(i),angz2(i),angz3(i)]
            %             [angxyz1(i),angxyz2(i),angxyz3(i)]
            
               plotea;
            
            newgrad=(grados-pi/2)/pi*180;  %% Grados de -90 a 270° en grados.
            angz2(i)=sum(newgrad.*absaccz.*absaccz)/sum(absaccz.*absaccz);
            title(['Ang Z2: ',num2str(angz2(i))])
            
            
            
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%%%% ==> ==> ==> ACA VOY %%%%%%%%%%%%%%%%%
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            
        end
        
    end
    % %
    % %     resdeltaz=abs(accelz2(1:length(accelx2)-1)-accelz2(2:length(accelx2)));
    % %     k2=find(resdeltaz>0.999999*max(resdeltaz));
    % %     if (grados(k2+1)/pi*180-90>120 && grados(k2+1)/pi*180-90<165)
    % %         maxdeltaz(i)=grados(k2+1)/pi*180-90;
    % %     end
    % %
    % %     resxy=abs(accelx2.*accely2);
    % %     k3=find(resxy>0.999999*max(resxy));
    % %     if (grados(k3)/pi*180-90>120 && grados(k3)/pi*180-90<165)
    % %         maxxy(i)=grados(k3)/pi*180-90;
    % %     end
    % %
    % %     resyz=abs(accely2.*accelz2);
    % %     k4=find(resyz>0.999999*max(resyz));
    % %     if (grados(k4)/pi*180-90>120 && grados(k4)/pi*180-90<165)
    % %         maxyz(i)=grados(k4)/pi*180-90;
    % %     end
    % %
    % %     reszx=abs(accelz2.*accelx2);
    % %     k5=find(reszx>0.999999*max(reszx));
    % %     if (grados(k5)/pi*180-90>120 && grados(k5)/pi*180-90<165)
    % %         maxzx(i)=grados(k5)/pi*180-90;
    % %     end
    % %
    % %     resxyz=abs(accelx2.*accely2.*accelz2);
    % %     k6=find(resxyz>0.999999*max(resxyz));
    % %     if (grados(k6)/pi*180-90>120 && grados(k6)/pi*180-90<165)
    % %         maxxyz(i)=grados(k6)/pi*180-90;
    % %     end
    % %
    
    
    %% PAUSE PARA ANALIZAR CASO A CASO
        if usar~=0 && ciclocompleto(i)~=0;
            pause,
        end
    
    i;
    
end


% % figure(8)
% % subplot(3,2,1),bar(maxdeltaz),axis([0 length(ciclo) 120 160]), title('maxdeltaz');
% % subplot(3,2,2),bar(maxxy),axis([0 length(ciclo) 120 160]), title('maxxy');
% % subplot(3,2,3),bar(maxyz),axis([0 length(ciclo) 120 160]), title('maxyz');
% % subplot(3,2,4),bar(maxzx),axis([0 length(ciclo) 120 160]), title('maxzx');
% % subplot(3,2,5),bar(maxxyz),axis([0 length(ciclo) 120 160]), title('maxxyz');
% % subplot(3,2,6),bar(0.6*maxdeltaz+0.1*maxxy+0.1*maxyz+0.1*maxzx+0.1*maxxyz),axis([0 length(ciclo) 120 160]), title('promedio ponderado');



