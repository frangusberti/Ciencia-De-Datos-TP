# Bitácora de Trabajo – Proyecto ETL

**Equipo:** Franco Gusberti (y equipo)
**Dataset:** customer_behavior_dataset.csv
**Fecha de finalización:** 8 de mayo de 2026

---

## 1. EXTRACCIÓN (Extract)

Se procedió a la lectura del conjunto de datos fuente, `customer_behavior_dataset.csv`, mediante el uso de la biblioteca `pandas` en Python.
- **Herramienta de análisis:** Python 3.x, Pandas, NumPy.
- **Dimensiones originales:** 2240 registros por 29 columnas.

## 2. EXPLORACIÓN INICIAL Y DICCIONARIO DE DATOS

En primera instancia, se emplearon funciones descriptivas (`info()`, `describe()`, `shape`) para comprender la naturaleza de las variables y detectar anomalías tempranas.

### Diccionario de Datos

| Variable | Descripción | Tipo |
| :--- | :--- | :--- |
| `ID` | Identificador único del cliente | Numérico |
| `Year_Birth` | Año de nacimiento | Numérico |
| `Education` | Nivel de educación alcanzado | Categórico |
| `Marital_Status` | Estado civil | Categórico |
| `Income` | Ingreso anual del hogar | Numérico |
| `Kidhome` | Cantidad de niños en el hogar | Numérico |
| `Teenhome` | Cantidad de adolescentes en el hogar | Numérico |
| `Dt_Customer` | Fecha de alta como cliente | Fecha (String inicial) |
| `Recency` | Días transcurridos desde la última compra | Numérico |
| `MntWines` / `MntFruits` / etc. | Gastos en categorías específicas de productos | Numérico |
| `NumWebPurchases` / etc. | Frecuencia de compra por canal | Numérico |
| `AcceptedCmp1-5` | Indicador de aceptación de campañas de marketing | Binario (0/1) |
| `Complain` | Indicador de quejas realizadas | Binario (0/1) |
| `Z_CostContact` / `Z_Revenue` | Variables constantes | Numérico |
| `Response` | Respuesta a la última campaña | Binario (0/1) |

## 3. TRANSFORMACIONES (Transform)

Se llevó a cabo un proceso de limpieza de datos y *Feature Engineering* documentado a continuación:

### 3.1 Tratamiento de Columnas Innecesarias
- **Eliminación de constantes:** Se eliminaron las columnas `Z_CostContact` y `Z_Revenue` dado que contenían un único valor constante para todos los clientes (3 y 11, respectivamente), no aportando ninguna variabilidad ni valor analítico al modelo.

### 3.2 Tratamiento de Valores Faltantes (Nulos)
- **Nulos interpretados como cero:** Variables como `Kidhome`, `MntMeatProducts`, métricas de aceptación de campañas (`AcceptedCmp`) y `Complain` presentaban valores nulos que, por el contexto de negocio, representan la ausencia del hecho (ej: cero hijos, ninguna queja). Se rellenaron con el valor `0`.
- **Nulos en Ingresos (`Income`):** Se identificaron 24 registros nulos. Se decidió rellenarlos utilizando la **mediana** de la columna en lugar de la media aritmética, mitigando de esta forma la distorsión que generan los valores atípicos de sueldos extremadamente altos.

### 3.3 Tratamiento de Outliers y Errores de Carga
- **Filas Duplicadas:** Se incluyó un chequeo de eliminación de filas duplicadas para evitar distorsiones en las métricas.
- **Edades Irreales:** Se observaron clientes con años de nacimiento inferiores a 1900 (ej: 1893). Se filtró el dataset preservando únicamente los nacimientos desde el año 1930 en adelante.
- **Valores Financieros Ilógicos:** Se detectaron y eliminaron registros que presentaban valores negativos tanto en la columna de ingresos (`Income` < 0) como en las columnas de gastos por productos (`MntWines`, `MntFruits`, etc. < 0).
- **Tratamiento de Decimales:** Ciertas variables inherentemente discretas (como días desde última compra, `Recency`, y cantidad de compras) poseían decimales (ej. `75.977`). Se aplicó un redondeo matemático y se reconfiguró el tipo de dato a entero.

### 3.4 Transformación de Tipos de Datos y Renombramientos
- **Formateo de Fechas:** La variable `Dt_Customer` fue convertida de texto a objeto `datetime` con el formato `dd-mm-yyyy` para habilitar análisis temporales.
- **Estandarización de Nombres:** Se renombraron diversas variables al idioma español para facilitar la lectura del conjunto de datos (ej: `Year_Birth` a `Anio_Nacimiento`, `Dt_Customer` a `Fecha_Cliente`).

### 3.5 Ingeniería de Características (Feature Engineering)
Se crearon nuevas variables clave para sintetizar el comportamiento del consumidor:
- **`Edad`:** Calculada como 2026 menos el año de nacimiento.
- **`Total_Hijos`:** Sumatoria de `Kidhome` y `Teenhome`.
- **`Gasto_Total`:** Sumatoria de todos los montos de gastos en productos (`Mnt...`).
- **`Total_Compras`:** Sumatoria de transacciones realizadas en todos los canales de venta.

## 4. CARGA (Load)
- El dataset final consolidado y transformado fue exportado a formato CSV bajo el nombre `customer_behavior_LIMPIO.csv`, desactivando la generación del índice por defecto para no interferir con el `ID` del cliente.

## 5. VERSIONADO
- **v1.0 (Franco - 01/05):** Carga inicial, exploración y eliminación de columnas constantes.
- **v1.1 (Franco - 01/05):** Imputación de nulos (con valores 0 y mediana).
- **v1.2 (Franco - 02/05):** Remoción de outliers (edades), formateo de fechas y creación de variables iniciales de negocio.
- **v2.0 (Equipo - 08/05):** Consolidación técnica final. Implementación de eliminación de duplicados, redondeo de variables numéricas discretas, tratamiento integral de valores negativos en métricas de gasto, y formalización de renombramientos y bitácora técnica.
