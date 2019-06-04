import pickle
import params

ruta = params.ruta
pwd_grupos = ruta + f"/clusters - {params.startDate} - {params.endDate} : Size {params.no_cluster}.txt"
with open(pwd_grupos, 'rb') as fp2:
    ward = pickle.load(fp2)

etiquetas = ward