import os

# query parameters
startDate = '2018-08-01 00:00'
endDate = '2018-12-30 00:00'
cantidad = 8000

# Lowpass filter bank parameters
thresh = 0.3
wavelet_name = 'sym5'

# Training Size
tamaño_entrenamiento = 0.7

# Directorio Imágenes
# user = getpass.getuser()
ruta = os.path.dirname(os.path.realpath(__file__))
pwd = ruta + '/Imágenes'

# Número de grupos
no_cluster = 5


# import matplotlib.pyplot as plt
# plt.plot(dwt)
# plt.plot(sine2, '--g')