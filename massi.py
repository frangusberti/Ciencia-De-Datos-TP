import pandas as pd
import numpy as np
from datetime import datetime
df = pd.read_csv("/Users/maximarissop/Desktop/Ciencia de Datos/Ciencia-De-Datos-TP/customer_behavior_dataset.csv")
nulos = df.isnull().sum()
print(nulos[nulos > 0])

#hasta ahora programe para que cuente valores que faltan en por columna, podria ver el porcentaje de valores nulos si quiero pero me parece medio innecesario
#veo que hago con esos valores nulos pq hay algunas categorias que tienen muchos valores nulos y otras no tantos
#me trato de sacar de encima valores extraños (ejs: años y sueldos negativos)

print(df.describe())

#se detectan esos valores atipicos observando el minimo y el maxixmo valor de las columnas
#Pueden emplearse conceptos de Probabilidad y Estadistica (Teorema Central del Limite) para ver si los valores de las columnas pertenecen o no al rango especificado

#pruebo detectar valores atipicos para la columna de year_birth, tengo que definir que son los outliers en cada caso
#mas facil puede ser sin usar conceptos de PyE, lo hago directamente con definiciones y (longitud de cadena?) pero ahi tendria que hacer uno por uno creo asi que mejor usar PyE
#no es por TCL de PyE, es por el rango intercuantilico (robustez) pq el TCL trabaja sobre aproximaciones del conjunto de datos y no sobre los datos de por si, mientras que el IQR trabaja sobre los datos (por eso en ejs de TCL de PyE ponen APROXIMADAMENTE para que nos demos cuenta que nos piden algo para el TCL)
#pense en que IQR=IC pero esta mal pq IC trabaja asumiendo una probabilidad de que los datos esten en cierto rango "estoy segura que el 80% de los datos estan aca" y usa TCL batantes veces, viendo donde anda la media de los datos (mira incertidumbres sobre los parametros), pero IQR mira directamente los datos que esten bastante mas alejados de lo esperado


#metodo IQR: quiero buscar donde vive la mayoria de los datos, sin usar promedios ni aproximaciones, sino analizando los datos individualmente
#calculando Q1 (el 25% de los datos que estan por debajo del limite inferior ej: dato de Year_Birth: 1890, que es menor a 1930 si es establecido como minimo, imposible que esa persona este viva hoy en dia) y Q3 (el 25% de los datos que estan por encima del limite superior ej: dato de Year_Birth: 2036, esta claramente fuera del limite superior 2020 si este es definido de esa forma, imposible que esa persona exista pq faltan 10 años para su nacimiento)
#cuando hago Q3-Q1 obtengo el ancho del 50% central de la distribucion (viendolo sin los extremos que es donde estan los outliers) para obtener un resultado real y correcto sobre el cual se busca trabajar
#los limites se definen como inferior: Q1-1.5*IQR y superior: Q3+1.5*IQR,  siendo 1.5 un valor empirico, que captura casi todo lo esperable en los datos "normales" y descarta los que no cumplen con las condiciones explicitadas

def deteccion_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3-Q1
    
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    
    outliers = df[(df[column] < limite_inferior) | (df[column] > limite_superior)] 
    #con esta linea de codigo puedo filtrar los datos (de cada columna) tal que cumpla con ambas condiciones impuestas y si difiere, lo descarta. Trabaja sobre el data frame de todo el csv, y por dentro del mismo, sobre los data frame de cada columna
    
    print(f"\n--- {column} ---")
    print(f"Q1: {Q1}, Q3: {Q3}, IQR: {IQR}")
    print(f"Límites: [{limite_inferior}, {limite_superior}]")
    print(f"Outliers encontrados {len(outliers)}")
        
    return outliers

#con la serie de "prints" me devuelve organizados por columna analizada los siguientes valores: count (cantidad de datos por columna), mean (media), std (desvio estandar), min (minimo valor encontrado), max (maximo valor encontrado), 25% (Q1), 50% (IQR), 75% (Q3)
#voy a probar un codigo generico (que aplique a todas las columnas) para mostrar los valores que esten alejados de los limites. Voy a usar la media y el desvio estandar para este calculo pq lo que yo hice recien creo que no me estaria mostrando las anomalias (outliers encontrados)
#mentira me los muestra en cantidad no se leer. Ademas seria una carga enorme para mi compu que me muestre por columna TODOS los outliers (hay columnas que tienen >60 e incluso una con >1000) y ya con ver 10 outliers que me devuelva (ej: outliers_income = -1300, 1 millon, -4000000 etc)
#mentira devuelta no se leer, pq las columnas que yo estaba hablando en el renglon anterior (no las de count mean std etc sino las que aparecen al principio de todo cuando corro el codigo) SON CANTIDAD DE VALORES NO NULOS DE CADA COLUMNA!!!!! estoy medio quemada de la cabeza por Dios....

print(df[df["Year_Birth"]<1930]) #para observar valores irreales de fechas de nacimiento (negativos, decimales no hay creo pero por las dudas los transformo en enteros veo como hago eso)
print(df[df["Income"]<0]) #para ver igresos economicos menores a cero, puesto que no puede haber montos de dinero negativos en ingresos economicos (a menos que la culmna indique balance de cuenta o deudas por ejemplo)

#junto valores de gastos por que tienen todos algo en comun: no se pueden admitir valores menores a cero y son categorias de gastos en productos/ alimentos para la cotidianeidad (por eso no lo junto con la columna Income o Year_Birth) ademas quiero tener una mejor organizacion de los datos y si puedo juntar categorias mejor (siempre y cuando tenga sentido juntarlas ya sea por categoria compartida, limites compartidos etc)
#defino columna total de gastos constituida por cada una de las categorias de gastos:  

gastos_cotidianos = ["MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", "MntGoldProds"]
for col in gastos_cotidianos:
    negativos = df[df[col] < 0] #define las columnas con valores negativos
    if len(negativos) > 0: #define que si hay columnas que cumple la condicion anterior, va mostrarse que columna es y cuantos valores negativos posee
        print(f"{col} tiene {len(negativos)} valores negativos")


 