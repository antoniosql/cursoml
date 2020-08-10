import pyodbc
import pandas as pd 
import sklearn

servidor= "tcp:<servidor>.database.windows.net"
bbdd='<bbdd>'
usuario = '<usuario>'
contraseña='<pwd>'

consulta = "SELECT * FROM ventas"

conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + servidor + ';DATABASE=' + bbdd + ';UID=' + usuario +';PWD=' + contraseña )

DetalleVentas = pd.read_sql(consulta, conexion)
DetalleVentas.head()