# Bitácora de Máxima

**Proyecto:** Ciencia de Datos - TP (Procesamiento ETL)
**Archivo de trabajo principal:** `massi.py`

---

## 📅 1 de Mayo de 2026

**Actividades realizadas:**
- **Setup inicial:** Importación de las librerías fundamentales para el análisis de datos (`pandas` como pd, `numpy` como np y `datetime`).
- **Extracción de datos (Extract):** Lectura exitosa del dataset principal `customer_behavior_dataset.csv` mediante la función `pd.read_csv()`.
- **Exploración de valores nulos:** 
  - Se implementó código para contar los valores faltantes por columna (`df.isnull().sum()`).
  - Se filtraron y mostraron por pantalla únicamente las columnas que presentan valores nulos mayores a 0.
  - *Decisión técnica:* Se optó por no calcular el porcentaje de nulos por considerarlo innecesario por el momento. Se planea evaluar qué hacer con estos valores dependiendo de la cantidad de faltantes por categoría.
- **Exploración inicial de Outliers:** 
  - Uso de la función `df.describe()` para obtener un resumen estadístico del dataset.
  - El objetivo principal planteado fue detectar valores atípicos observando los valores mínimos y máximos, buscando específicamente anomalías lógicas (por ejemplo: sueldos negativos o años irreales).

---

## 📅 2 de Mayo de 2026

**Actividades realizadas:**
- **Análisis de Outliers en profundidad:** 
  - Se comenzó a evaluar cómo detectar valores atípicos específicamente para la columna `year_birth`.
  - Se debatió la metodología para definir qué es un "outlier" en cada caso particular (si hacerlo mediante definiciones directas, longitud de cadenas, o utilizando conceptos matemáticos de Probabilidad y Estadística).
- **Corrección de conceptos estadísticos:** 
  - Inicialmente se planteó la hipótesis de utilizar el Teorema Central del Límite (TCL) para establecer rangos de valores válidos.
  - Tras investigar la sugerencia de la guía de ETL, se corrigió este concepto: se comprendió que la detección de outliers **no se basa en el Teorema Central del Límite**, sino que se utiliza el **Rango Intercuartílico (IQR)**. 
  - *Conclusión:* El uso de cuantiles se debe a su **robustez** estadística, ya que, a diferencia de la media y la desviación estándar, no se ven afectados ni sesgados por los propios valores atípicos extremos.
- **Diferenciación entre IQR e Intervalos de Confianza (IC):**
  - Se reflexionó sobre la diferencia entre IQR y los IC basados en el Teorema Central del Límite.
  - Se concluyó que los IC asumen una distribución de probabilidad sobre los parámetros poblacionales (e.g., dónde está la media), mientras que el IQR es un método descriptivo y directo que analiza los datos puntuales buscando aislar el 50% central para descartar anomalías reales sin depender de aproximaciones.
- **Implementación de la función `deteccion_outliers_iqr`:**
  - Se programó la función principal para calcular Q1 (percentil 25) y Q3 (percentil 75) y determinar el Rango Intercuartílico (IQR).
  - Se definieron los límites inferior y superior usando la regla empírica de `1.5 * IQR`.
  - Se implementó la lógica de filtrado de datos utilizando operadores booleanos (`|`) para identificar los valores que exceden estos límites, y se configuró un reporte en consola para mostrar los resultados y la cantidad de outliers encontrados por columna.
- **Interpretación de salidas e Inspección manual:**
  - Se revisaron los resultados de la consola, clarificando la diferencia entre el conteo de valores nulos y los outliers reales devueltos por la función.
  - Se añadieron filtros manuales (`df[df["Year_Birth"]<1930]` y `df[df["Income"]<0]`) para imprimir y visualizar en detalle los registros con anomalías lógicas (edades irreales e ingresos negativos).
  - Se inició la preparación para analizar de forma conjunta las variables asociadas a gastos económicos del cliente.
