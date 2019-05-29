import os

# query parameters
startDate = '2018-11-26 00:00'
endDate = '2018-12-29 23:30'
cantidad = 200

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
no_cluster = 7
