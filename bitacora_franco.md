# Bitácora de Trabajo - Proyecto Ciencia de Datos

**Integrantes:** Franco Gusberti
**Dataset:** customer_behavior_dataset.csv
**Fecha de inicio:** 1 de mayo de 2026

---

### [Franco] - 1. Primer contacto con los datos (01/05)
Se procedió a la carga del conjunto de datos fuente utilizando la biblioteca Pandas. El archivo contiene inicialmente **2240 filas** y **29 columnas**. 

Mediante el uso de las funciones descriptivas `df.info()` y `df.describe()`, se realizó una exploración preliminar de las variables, identificando métricas clave como fechas de nacimiento, nivel de ingresos, composición familiar y gastos acumulados por categoría de producto.

### [Franco] - 2. Tratamiento de columnas sin variabilidad
Tras analizar el número de valores únicos por columna, se identificó que las variables `Z_CostContact` y `Z_Revenue` contienen valores constantes (3 y 11, respectivamente) en todos los registros. 
**Resolución:** Ambas columnas fueron eliminadas del conjunto de datos, dado que su falta de variabilidad las vuelve irrelevantes para cualquier análisis comparativo o modelo predictivo.

### [Franco] - 3. Imputación de valores nulos
El análisis de valores faltantes (`df.isnull().sum()`) reveló la presencia de datos nulos, principalmente en variables como `Kidhome` y `Complain`.

**Análisis y Resolución:**
- Variables como `Complain` (quejas), `Kidhome` (hijos) y `AcceptedCmp` (aceptación de campañas) con valores nulos no representan errores de carga, sino la ausencia del evento (cero quejas, cero hijos). En consecuencia, para preservar los registros, estos valores fueron imputados con el número **0**.
- En cuanto a la variable `Income` (ingresos), se detectaron 24 valores nulos. Dada la naturaleza de los ingresos y para evitar sesgos provocados por valores atípicos (outliers), se optó por imputar estos datos faltantes utilizando la **mediana** estadística de la columna, ofreciendo un valor de reemplazo más representativo que la media aritmética.

### [Franco] - 4. Detección y tratamiento de valores atípicos (Outliers)
Se realizó una auditoría de las variables demográficas y financieras para identificar inconsistencias.
- **Fechas de nacimiento:** Se encontraron años de nacimiento ilógicos (ej. 1893). Para garantizar la integridad de los datos, se descartaron los registros correspondientes a clientes nacidos antes de 1930.
- **Ingresos y Gastos:** Se implementó un filtro de control de calidad para descartar cualquier registro que presentara ingresos negativos o gastos por debajo de cero, asumiendo dichos casos como errores severos de carga.
- **Duplicados y Decimales:** Se procedió a la eliminación de filas duplicadas y se redondearon las variables inherentemente discretas (como días transcurridos y número de compras).

### [Franco] - 5. Conversión de Tipos de Datos e Ingeniería de Características
- La variable `Dt_Customer` (fecha de alta) fue convertida de formato texto a objeto `datetime` para facilitar futuros análisis temporales.
- **Ingeniería de Características:** Se crearon nuevas variables analíticas para sintetizar el comportamiento del consumidor:
  - `Edad`: Diferencia entre el año actual (2026) y el año de nacimiento.
  - `Total_Hijos`: Sumatoria de las variables `Kidhome` y `Teenhome`.
  - `Gasto_Total`: Sumatoria de las columnas representativas de compras por categoría (vinos, carnes, frutas, etc.).
  - Además, se estandarizaron los nombres de las columnas al idioma español para mayor claridad de lectura.

### [Franco] - 6. Desafíos técnicos: Control de Versiones con Git
Durante la ejecución del proyecto, se presentó un conflicto en el manejo de ramas al integrar cambios a la rama `main` de manera prematura. Esta situación requirió la ejecución de un `revert` sobre el commit de fusión (merge) para restaurar la integridad del código principal. Este incidente permitió reforzar las buenas prácticas de revisión y segregación de ramas previo a la consolidación definitiva del código.

### [Franco] - 7. Registro de versiones
- **v1.0:** Carga de datos y eliminación de variables constantes (`Z_CostContact`, `Z_Revenue`).
- **v1.1:** Imputación estructural de valores nulos.
- **v1.2 (02/05 14:15hs):** Tratamiento de nulos en `Income`, eliminación de outliers demográficos, estandarización de fechas y desarrollo inicial de Feature Engineering.
- **v2.0 (08/05):** Corrección de vocabulario técnico en bitácora y código, implementación de eliminación de duplicados, redondeo de variables numéricas discretas y tratamiento integral de outliers financieros. El resultado consolidado fue exportado al archivo `customer_behavior_LIMPIO.csv`.
