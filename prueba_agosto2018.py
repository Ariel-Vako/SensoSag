import pickle
import params

pc = params.ruta + '/pc.txt'
with open(pc, 'rb') as fp:
    pc = pickle.load(fp)

señal = params.ruta + f'/signal_features- {params.startDate} - {params.endDate} : {params.cantidad}.txt'
with open(señal, 'rb') as fp2:
    signal_520agosto2018 = pickle.load(fp2)

pwd_grupos = params.ruta + f"/clusters - {params.startDate} - {params.endDate} : Size {params.no_cluster}.txt"
with open(pwd_grupos, 'rb') as fp2:
    all_cluster = pickle.load(fp2)

# Aplicar la reducción de dimensión a la data de Agosto del 2018.

# Agrupar utilizando el clústering de las señales completas.

# Graficar resultados.
