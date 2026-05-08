# Bitácora de Trabajo – Proyecto ETL
## Introducción a la Ciencia de Datos – Cátedra Arriazu – 1C2026

---

**Integrantes:** Ian Gubert Gamba  
**Dataset:** `customer_behavior_dataset.csv`  
**Herramientas:** Python 3.14, Pandas, NumPy  
**Repositorio:** https://github.com/frangusberti/Ciencia-De-Datos-TP

---

## 1. Extracción de Datos

**Fecha:** 01/05/2026  
**Responsable:** Ian Gubert Gamba

### 1.1 Fuente de datos
- Archivo: `customer_behavior_dataset.csv`
- Dimensiones originales: **2216 filas × 29 columnas**

### 1.2 Descripción general del dataset
El dataset contiene información de clientes de una empresa de consumo, incluyendo datos demográficos, hábitos de compra y respuesta a campañas de marketing.

**Período de los datos:** [Completar rango de fechas de Dt_Customer]

### 1.3 Variables del dataset

| # | Variable | Tipo | Descripción |
|---|----------|------|-------------|
| 1 | `ID` | Numérico | Identificador único del cliente |
| 2 | `Year_Birth` | Numérico | Año de nacimiento del cliente |
| 3 | `Education` | Categórico | Nivel educativo (Graduation, PhD, Master, 2n Cycle, Basic) |
| 4 | `Marital_Status` | Categórico | Estado civil (Single, Married, Together, Divorced, Widow, Alone, Absurd, YOLO) |
| 5 | `Income` | Numérico | Ingreso anual del hogar |
| 6 | `Kidhome` | Numérico | Cantidad de niños en el hogar |
| 7 | `Teenhome` | Numérico | Cantidad de adolescentes en el hogar |
| 8 | `Dt_Customer` | Fecha (texto) | Fecha de inscripción como cliente |
| 9 | `Recency` | Numérico | Días transcurridos desde la última compra |
| 10 | `MntWines` | Numérico | Monto gastado en vinos |
| 11 | `MntFruits` | Numérico | Monto gastado en frutas |
| 12 | `MntMeatProducts` | Numérico | Monto gastado en carnes |
| 13 | `MntFishProducts` | Numérico | Monto gastado en pescado |
| 14 | `MntSweetProducts` | Numérico | Monto gastado en dulces |
| 15 | `MntGoldProds` | Numérico | Monto gastado en productos premium/gold |
| 16 | `NumDealsPurchases` | Numérico | Cantidad de compras con descuento |
| 17 | `NumWebPurchases` | Numérico | Cantidad de compras por web |
| 18 | `NumCatalogPurchases` | Numérico | Cantidad de compras por catálogo |
| 19 | `NumStorePurchases` | Numérico | Cantidad de compras en tienda física |
| 20 | `NumWebVisitsMonth` | Numérico | Visitas mensuales al sitio web |
| 21-25 | `AcceptedCmp1` a `AcceptedCmp5` | Binario (0/1) | Si aceptó la campaña de marketing 1 a 5 |
| 26 | `Complain` | Binario (0/1) | Si realizó una queja en los últimos 2 años |
| 27 | `Z_CostContact` | Numérico | Costo de contacto (constante = 3) |
| 28 | `Z_Revenue` | Numérico | Revenue asociado (constante = 11) |
| 29 | `Response` | Binario (0/1) | Si aceptó la oferta en la última campaña |

---

## 2. Exploración Inicial

**Fecha:** 05/05/2026  
**Responsable:** Ian Gubert Gamba

### 2.1 Valores faltantes detectados

| Columna | Cantidad de nulos | Porcentaje | Decisión | Motivo |
|---------|------------------|------------|----------|--------|
| `Income` | [Variable] | [Variable]% | Rellenar con la mediana | Imputación más robusta a outliers |
| Varias (`Kidhome`, `MntMeatProducts`, etc.) | [Variable] | [Variable]% | Rellenar con 0 | La ausencia de datos indica un valor de cero |

### 2.2 Outliers detectados

| Columna | Valor sospechoso | Cantidad | Decisión | Motivo |
|---------|-----------------|----------|----------|--------|
| `Year_Birth` | Valores < 1930 | Dinámico | Eliminar | Edades mayores a 96 años, posibles errores de carga. |
| `Income` | Valores > 150000 | Dinámico | Eliminar | Ingresos extremadamente altos que pueden sesgar el análisis. |

### 2.3 Observaciones adicionales
- [Completar: columnas constantes, valores raros, duplicados, etc.]

---

## 3. Transformaciones Realizadas

**Fecha:** 05/05/2026 - 06/05/2026  
**Responsable:** Ian Gubert Gamba

### 3.1 Tratamiento de valores faltantes

| Columna | Método aplicado | Valor utilizado | Justificación |
|---------|----------------|-----------------|---------------|
| `Income` | Imputación por mediana | Mediana de la columna | Se eligió la mediana por ser menos sensible a valores atípicos. |
| `Kidhome`, `MntMeatProducts`, `MntFishProducts`, `MntSweetProducts`, `NumDealsPurchases`, `AcceptedCmp3`, `AcceptedCmp2`, `Complain`, `Response` | Imputación por constante | 0 | La falta de datos en estas variables (compras, quejas o campañas) implica 0 ocurrencias. |

### 3.2 Tratamiento de outliers

| Columna | Acción | Filas afectadas | Justificación |
|---------|--------|-----------------|---------------|
| `Year_Birth` | Eliminación de registros | Dinámico | Mantener un rango etario razonable para el análisis. |
| `Income` | Eliminación de registros | Dinámico | Evitar distorsiones estadísticas por sueldos excepcionales. |

### 3.3 Conversión de tipos de datos

| Columna | Tipo original | Tipo nuevo | Detalle |
|---------|--------------|------------|---------|
| `Dt_Customer` | object (texto) | datetime | Formato: DD-MM-YYYY |
| | | | |

### 3.4 Columnas eliminadas

| Columna | Motivo de eliminación |
|---------|-----------------------|
| `Z_CostContact` | Eliminada dinámicamente por tener un único valor en toda la columna. No aporta información. |
| `Z_Revenue` | Eliminada dinámicamente por tener un único valor en toda la columna. No aporta información. |

### 3.5 Filas eliminadas

| Motivo | Condición | Cantidad eliminada |
|--------|-----------|-------------------|
| Edades ilógicas | `Year_Birth < 1930` | Dinámico |
| Ingresos extremos | `Income > 150000` | Dinámico |

### 3.6 Feature Engineering (nuevas columnas creadas)

| Nueva columna | Fórmula / Lógica | Justificación |
|--------------|-------------------|---------------|
| `Edad` | `Año actual - Year_Birth` | Conocer la edad actual del cliente facilita la segmentación demográfica y el análisis directo. |

---

## 4. Carga de Datos

**Fecha:** 05/05/2026 - 06/05/2026  
**Responsable:** Ian Gubert Gamba

- Archivo de salida final: `customer_behavior_dataset_sin_outliers.csv`
- Dimensiones finales: **Dinámico filas × 28 columnas**
- Diferencia respecto al original: Dinámico filas eliminadas por outliers, 2 columnas eliminadas (`Z_CostContact`, `Z_Revenue`), 1 columna nueva (`Edad`)

---


## 5. Registro de Versiones

| Versión | Fecha y Hora | Responsable | Descripción del cambio |
|---------|-------------|-------------|----------------------|
| v1.0 | 01/05/2026 10:00 | Ian Gubert Gamba | Carga inicial y exploración del dataset |
| v1.1 | 05/05/2026 20:35 | Ian Gubert Gamba | Automatización de limpieza, imputación de nulos y Feature Engineering (Creación de Edad) |
| v1.2 | 05/05/2026 21:03 | Ian Gubert Gamba | Exportación del dataset modificado en `customer_behavior_dataset_copia.csv` |
| v1.3 | 06/05/2026 23:25 | Ian Gubert Gamba | Tratamiento de outliers y exportación del dataset modificado en `customer_behavior_dataset_sin_outliers.csv` |
---

## 6. Conclusiones

Se logró automatizar gran parte de la etapa inicial de exploración, identificando dinámicamente columnas sin información útil y tratando de manera justificada los valores faltantes mediante imputaciones lógicas (relleno con 0) y estadísticas (mediana). Se incorporó nueva información creando la columna `Edad`, que aporta valor directo al análisis. Además, se garantizó la robustez de los datos eliminando registros atípicos (outliers) como edades improbables e ingresos extremos. El dataset final limpio y consolidado se guardó exitosamente y se encuentra listo para las siguientes etapas del proyecto.
.............
