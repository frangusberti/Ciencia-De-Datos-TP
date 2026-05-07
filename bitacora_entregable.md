# Bitácora de Trabajo Integrada - Proyecto ETL
**Integrantes:** Franco Gusberti, Máxima Risso Patrón y Joaquín Sanchez
**Dataset:** `customer_behavior_dataset.csv`
**Fecha:** Mayo 2026

---

## 1. Carga y exploración inicial
Se importaron las librerías `pandas`, `numpy` y `datetime` y se cargó el archivo CSV original. 

- Mediante `df.isnull().sum()` y `df.describe()` se realizó una revisión preliminar para identificar datos nulos y valores inconsistentes (por ejemplo, fechas de nacimiento muy antiguas o ingresos menores a cero).
- Se utilizó `drop_duplicates()` para detectar y eliminar filas repetidas antes de iniciar las transformaciones.

---

## 2. Tratamiento de valores nulos
Se detectaron valores faltantes en varias columnas, como las referentes a cantidad de hijos, quejas y campañas. Se adoptaron los siguientes criterios:

- **Imputación por ceros:** Para las columnas `Kidhome`, `Complain`, `Response` y variables de gastos, se determinó que el valor nulo representaba la ausencia del atributo, por lo que se reemplazaron con el número 0.
- **Media y Mediana:** Para los nulos numéricos (como `Income`), se imputó utilizando la media y la mediana. Se optó por la mediana en los casos donde había sueldos extremos, para evitar sesgar el cálculo.
- **Moda:** Para los datos categóricos faltantes, se imputó el valor más frecuente de la columna.
- **Formatos:** Se corrigieron columnas numéricas que estaban cargadas como decimales (`float`), convirtiéndolas a formato de número entero (`int`).

---

## 3. Manejo de valores atípicos (Outliers)
Se identificaron casos ilógicos como años de nacimiento anteriores a 1930 y sueldos negativos.

- Para buscar estos valores, se utilizó el método del Rango Intercuartílico (IQR), considerando que es más directo y robusto que aproximaciones por Teorema Central del Límite. También se verificó con bucles iterativos que no hubiera montos menores a cero en las categorías de gastos y compras.
- En lugar de descartar todas las filas atípicas, se aplicó la técnica de "capping" con la función `clip()`, la cual reemplaza los valores extremos ajustándolos al límite máximo o mínimo permitido por el rango IQR para conservar la cantidad de registros.
- Los valores correspondientes a errores de carga irrefutables (como fechas de nacimiento imposibles y salarios menores a cero) fueron directamente filtrados del dataset.

---

## 4. Transformaciones y creación de variables
Se agregaron y modificaron variables para facilitar el análisis del modelo en etapas posteriores:

- **Fechas:** Se cambió el formato de la columna `Dt_Customer` al tipo `datetime` y se extrajeron el año y el mes en columnas independientes.
- **Nuevas columnas:** Se calculó la edad del cliente (restando el año de nacimiento al 2026), el total de hijos por hogar y la suma de todas las categorías de gasto del cliente. También se agruparon las compras de todos los canales en un total general.
- **Campañas:** Se renombraron y estandarizaron las columnas de las campañas de marketing, calculando también los totales de aceptación y rechazo histórico.
- **Traducción:** Se renombraron las 29 columnas del dataset al español y a un formato unificado de minúsculas (por ejemplo, de `Year_Birth` a `anio_nacimiento`).

---

## 5. Limpieza final y exportación
- Se eliminaron las columnas `Z_CostContact` y `Z_Revenue`. Al analizarlas, se comprobó que contenían un único valor constante en todo el documento (3 y 11), por lo que no aportaban variación analítica.
- Se exportó el DataFrame final como `dataset_limpio.csv`.
- Se desarrolló un reporte que imprime por consola las métricas del dataset al finalizar el script (cantidad de nulos, filas duplicadas eliminadas, dimensiones y promedios) a modo de control de calidad.
