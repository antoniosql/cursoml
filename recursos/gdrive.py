## Creamos en Drive una carpeta llamada datos y subimos Tiendas24H.sqlite

## Montamos Google Drive para leer los archivos
from google.colab import drive
drive.mount('/content/gdrive')


conn = sqlite3.connect('/content/gdrive/My Drive/Datos/Tiendas24H.sqlite')