import pickle
import params
import shutil

ruta = params.ruta
pwd_grupos = ruta + f"/clusters - {params.startDate} - {params.endDate} : Size {params.no_cluster}.txt"
with open(pwd_grupos, 'rb') as fp2:
    ward = pickle.load(fp2)

etiquetas = ward[5].labels_

for index, labels in enumerate(etiquetas):
    ruta_imagen = ruta + '/Imágenes/'
    if index < 406:
        imagen = f'Ciclo {index}.png'
    elif 406 <= index < 1499:
        imagen = f'Ciclo {index + 1}.png'
    if index >= 1499:
        imagen = f'Ciclo {index + 2}.png'

    repositorio = ruta_imagen + f'{labels}/'
    shutil.move(ruta_imagen + imagen, repositorio + imagen)
