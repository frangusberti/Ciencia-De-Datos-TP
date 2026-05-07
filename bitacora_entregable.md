# Bitácora de Proyecto ETL
**Integrantes:** Franco Gusberti, Máxima Risso Patrón y Joaquín Sanchez
**Dataset:** `customer_behavior_dataset.csv`

---

## 📅 Fecha: 01/05/2026
**Fase:** Exploración y Setup Inicial
**Objetivo:** Comprender la estructura de los datos base.

**Actividades realizadas:**
- Configuración del entorno de trabajo e importación de librerías (`pandas`, `numpy`, `datetime`).
- Carga del archivo original `customer_behavior_dataset.csv`.
- Ejecución de análisis preliminar estadístico mediante `df.describe()` y `df.isnull().sum()`.
- Identificación y eliminación de filas completamente duplicadas utilizando la función `drop_duplicates()`.

**Observaciones:** 
Se detectaron múltiples valores nulos en el dataset y presencias de registros atípicos evidentes (edades desproporcionadas y valores negativos en columnas de ingresos y compras).

---

## 📅 Fecha: 02/05/2026
**Fase:** Tratamiento de Valores Nulos
**Objetivo:** Resolver la ausencia de datos sin perder registros valiosos.

**Actividades realizadas:**
- **Análisis de tipo de dato:** Se decidió no utilizar un único método de imputación para todo el dataset.
- **Imputación por lógica de negocio:** En columnas donde la ausencia del dato implica la no ocurrencia del evento (ej. cantidad de hijos, número de quejas, compras web), se imputó el valor `0`.
- **Imputación estadística:** 
  - Para los nulos en ingresos económicos numéricos (`Income`), se imputó el valor de la **mediana**, para evitar el sesgo que generarían los sueldos extremadamente altos en el cálculo de un promedio tradicional.
  - Para los datos faltantes en categorías de texto, se imputó el valor de la **moda**.
- **Transformación de tipos:** Se estandarizaron a enteros (`int`) columnas numéricas cargadas erróneamente como decimales (`float`).

---

## 📅 Fecha: 04/05/2026
**Fase:** Tratamiento de Outliers y Limpieza Estructural
**Objetivo:** Normalizar la distribución de los datos.

**Actividades realizadas:**
- **Detección estadística:** Se implementó el método del Rango Intercuartílico (IQR) para delimitar los datos esperados, descartando aproximaciones teóricas como el Teorema Central del Límite por ser menos precisas para este conjunto.
- **Técnica de Capping:** En lugar de eliminar las filas con valores atípicos y reducir la base de datos, se aplicó la técnica de capping mediante la función `clip()`. Los valores extremos se ajustaron al límite numérico permitido por el rango IQR.
- **Filtrado de errores de sistema:** Los datos irrefutablemente erróneos (como años de nacimiento anteriores a 1930 o ingresos negativos) fueron filtrados y eliminados.
- **Depuración:** Se eliminaron las columnas `Z_CostContact` y `Z_Revenue`. El análisis demostró que ambas poseían varianza cero (un único valor constante para todos los clientes).

---

## 📅 Fecha: 07/05/2026
**Fase:** Feature Engineering y Exportación Final
**Objetivo:** Enriquecer el modelo y generar el archivo final limpio.

**Actividades realizadas:**
- **Fechas:** Se estandarizó la columna `Dt_Customer` al tipo `datetime` y se separó el año y el mes en nuevas columnas.
- **Nuevas variables:** Se calculó la `edad` de los clientes (año 2026 - año de nacimiento). Se agruparon sumatorias totales para generar las columnas `gasto_total` y `total_compras`.
- **Diccionario de datos:** Se tradujeron y renombraron las 29 columnas del DataFrame al español, adoptando una convención unificada en minúsculas.
- **Auditoría:** Se programó un reporte de calidad automatizado para validar y emitir las dimensiones finales y la cantidad de nulos restantes antes de dar por finalizada la extracción.
- **Cierre:** Exportación exitosa del documento final como `dataset_limpio.csv`.
