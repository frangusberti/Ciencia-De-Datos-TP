# Bitácora de Proyecto ETL
**Integrantes:** Franco Gusberti, Máxima Risso Patrón y Joaquín Sanchez
**Dataset:** `customer_behavior_dataset.csv`

---

## 📅 Fecha: 01/05/2026

- Se realizó la configuración del entorno de trabajo en Python, importando las librerías base para la manipulación y análisis de datos: `pandas` para el manejo de DataFrames, `numpy` para cálculos matemáticos, y `datetime` para la gestión de fechas.
- Se cargó en memoria el archivo crudo `customer_behavior_dataset.csv`, el cual contaba originalmente con 2240 registros y 29 columnas con información demográfica, de comportamiento de compras y respuesta a campañas de marketing.
- Se ejecutó un análisis preliminar estadístico mediante `df.describe()`, lo que permitió observar inmediatamente medidas de tendencia central y dispersión. A simple vista, este comando reveló inconsistencias críticas, como un valor mínimo en el año de nacimiento (Year_Birth) de 1893, indicando clientes de más de 130 años, y montos ilógicos en otras variables.
- Mediante la instrucción `df.isnull().sum()` se expuso la presencia de múltiples valores nulos en distintas columnas clave, destacándose faltantes en ingresos (`Income`), cantidad de hijos (`Kidhome`, `Teenhome`), número de quejas (`Complain`) y respuestas a campañas promocionales.
- Para asegurar la integridad de la base antes de comenzar a transformarla, se aplicó el método `drop_duplicates()`, identificando y eliminando cualquier fila completamente repetida que pudiera sesgar el análisis futuro.

---

## 📅 Fecha: 02/05/2026

- Tras evaluar el reporte de nulos del día anterior, se decidió aplicar estrategias de imputación segmentadas según la naturaleza estadística de cada variable, en lugar de un enfoque genérico.
- **Imputación por lógica de negocio:** En columnas donde la ausencia del dato implica lógicamente la no ocurrencia de un evento, se imputó directamente el valor `0`. Esto se aplicó a las variables `Kidhome` y `Teenhome` (ausencia de hijos), `Complain` (sin quejas reportadas), `Response` (sin participación) y los montos de gastos sin registrar.
- **Imputación estadística de variables continuas:** Para la columna de ingresos económicos (`Income`), se descartó rellenar con ceros ya que afectaría gravemente el promedio. Se decidió utilizar la **mediana** (`median()`) sobre la media (`mean()`), justificando que la mediana es una medida mucho más robusta y menos sensible a ser arrastrada por los sueldos extremadamente altos (outliers) presentes en la base.
- **Imputación estadística de variables categóricas:** Para los datos faltantes en variables cualitativas o de categorías, se optó por imputar el valor más frecuente del dataset utilizando la **moda** (`mode()[0]`).
- **Limpieza de formatos de datos:** Se detectó que varias columnas numéricas (como cantidad de hijos y número de compras) estaban cargadas en el sistema como números decimales (`float`). Para mantener la coherencia semántica, se estandarizaron forzando su conversión al formato de número entero (`int` o `int64`).

---

## 📅 Fecha: 04/05/2026

- Se abordó el problema de los valores atípicos (outliers) identificados en la primera fase. Para su detección matemática, se implementó el método del Rango Intercuartílico (IQR). Se calcularon el primer y tercer cuartil (`Q1` al 25% y `Q3` al 75%) y se establecieron los límites inferior y superior utilizando la fórmula `Q1 - 1.5*IQR` y `Q3 + 1.5*IQR`.
- **Técnica de Capping:** Se debatió si eliminar las filas que contenían atípicos, pero se concluyó que esto reduciría demasiado el volumen de datos disponibles. En su lugar, se aplicó la técnica de capping utilizando la función `clip()` de Pandas. Esta técnica permitió conservar todos los registros reemplazando únicamente los valores extremos por el valor del límite máximo o mínimo permitido por el rango IQR.
- **Filtros lógicos directos:** A diferencia de los atípicos estadísticos, se aplicó un filtro directo de eliminación para los errores irrefutables de sistema. Mediante una máscara booleana se filtraron y eliminaron todos los registros donde `Year_Birth < 1930` (edades biológicamente improbables) y donde `Income < 0` (ingresos negativos inexistentes en la realidad).
- **Reducción de dimensionalidad:** Se analizaron estadísticamente las variables `Z_CostContact` y `Z_Revenue`. Al calcular la varianza de ambas, el resultado fue nulo, lo que confirmó que contenían un único valor constante para los 2240 clientes (3 y 11 respectivamente). Dado que las columnas sin variabilidad no tienen poder predictivo ni aportan información analítica, fueron eliminadas definitivamente (`drop`).

---

## 📅 Fecha: 07/05/2026

- Se procedió a enriquecer el dataset mediante técnicas de "Feature Engineering" para facilitar futuras visualizaciones y modelos de Machine Learning.
- **Estandarización temporal:** Se transformó la columna `Dt_Customer` (que originalmente era de tipo `object`/texto) al formato estándar `datetime`. De esta columna, se logró extraer el año y el mes de registro del cliente en dos nuevas columnas independientes (`anio_cliente` y `mes_cliente`).
- **Creación de nuevas variables analíticas:**
  - Se creó la columna `edad` calculando la diferencia entre el año actual de análisis (2026) y la columna `Year_Birth`.
  - Se creó la columna `gasto_total` mediante la sumatoria lineal de todas las categorías de consumo del cliente (`MntWines` + `MntFruits` + `MntMeatProducts` + `MntFishProducts` + `MntSweetProducts` + `MntGoldProds`).
  - Se creó la columna `total_compras` sumando las interacciones por tipo de canal (`NumDealsPurchases` + `NumWebPurchases` + `NumCatalogPurchases` + `NumStorePurchases`).
- **Renombrado y estandarización:** Se construyó un diccionario masivo para traducir y renombrar las 29 columnas originales al idioma español. Además, se forzó un formato estandarizado en minúsculas y separado por guiones bajos (por ejemplo: `MntWines` pasó a ser `gasto_vinos`, `Year_Birth` a `anio_nacimiento`, `AcceptedCmp1` a `acepto_campania_1`).
- **Control de Calidad (QA):** Previo a la exportación, se programó un bloque de código para auditar el resultado. Este script imprime un reporte de consola detallando: número final de filas y columnas, confirmación de 0 valores nulos restantes, 0 filas duplicadas y promedios clave de la población.
- **Cierre del proceso:** Se exportó el DataFrame totalmente procesado, validado y en español al disco bajo el nombre definitivo de `dataset_limpio.csv`.
