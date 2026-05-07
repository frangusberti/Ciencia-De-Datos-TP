# Bitácora de Trabajo – Proyecto ETL

# Joaquin 1 de Mayo 21:47: creo conveniente cambiar el idioma de las columnas del data set  ya siempre se es legible con mayusculas y minusculas,pero no logro encontrar el error

# Joaquin 1 de mayo  22:15: en la columna kid home hay valor "float", vamos a cambiar por un dato entero.

# Joaquin 7 de mayo,quiero reemplazar los nulos por la media. Y me tira el error: 
df[col].fillna(media, inplace=True) 
# esta es la linea de codigo donde Pandas  ya no permite modificar un dataFrame a través de una cadena de indexación. df[col] devuelve una copia, por lo que el inplace=True no tiene efecto sobre el DataFrame original.Reeplazo por :
for col in columnas_numericas:
    if df[col].isnull().sum() > 0:
        media = df[col].mean()
        df[col] = df[col].fillna(media) 
        print(f"  '{col}' → nulos reemplazados con media: {media:.2f}")


# Joaquin 7 de mayo,cuando queria tratar los nulos, me daba una advertencia , para funciones de pandas que futuras versiones podian cambiar.

# Manejamos los outlaiers sin eliminarlos.En todas las columnas numéricas usando el método IQR. En lugar de eliminar esas filas, aplicamos capping con .clip(), que consiste en reemplazar los valores fuera del rango permitido por el límite inferior o superior correspondiente, conservando todos lo resgritrados del dataset.
# Y por ultimo generamos  un reporte de calidad final que muestra en una sola vista el estado del dataset después de toda la limpieza: cantidad de filas, columnas, nulos restantes, duplicados, y estadísticas clave como ingreso y gasto promedio.
