# Bitácora de Trabajo – Proyecto ETL y Modelo Predictivo
## Introducción a la Ciencia de Datos – Cátedra Arriazu – 1C2026

---

**Integrantes:** Ian Gubert Gamba  
**Dataset:** `customer_behavior_dataset.csv`  
**Herramientas:** Python 3.14, Pandas, NumPy, scikit-learn (MLPClassifier)  
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
| v2.0 | 23/06/2026 01:20 | Ian Gubert Gamba | Implementación del modelo predictivo (Red Neuronal MLPClassifier) para predecir `Response`. Exportación de resultados en `resultados_prediccion_response.csv` |

---

## 6. Conclusiones de la Fase ETL

Se logró automatizar gran parte de la etapa inicial de exploración, identificando dinámicamente columnas sin información útil y tratando de manera justificada los valores faltantes mediante imputaciones lógicas (relleno con 0) y estadísticas (mediana). Se incorporó nueva información creando la columna `Edad`, que aporta valor directo al análisis. Además, se garantizó la robustez de los datos eliminando registros atípicos (outliers) como edades improbables e ingresos extremos. El dataset final limpio y consolidado se guardó exitosamente y se encuentra listo para las siguientes etapas del proyecto.

---

## 7. Modelo Predictivo – Red Neuronal (MLPClassifier)

**Fecha:** 23/06/2026  
**Responsable:** Ian Gubert Gamba

### 7.1 Hipótesis

Se busca predecir la columna **`Response`** (si el cliente aceptó o no la oferta en la última campaña de marketing). La hipótesis es que el comportamiento de compra, los datos demográficos y el historial de respuesta a campañas anteriores permiten anticipar la reacción del cliente ante futuras campañas. Un modelo con buena capacidad predictiva permitiría a la empresa focalizar sus recursos de marketing en los clientes con mayor probabilidad de aceptación.

### 7.2 Preprocesamiento para el modelo

Partiendo del dataset limpio (`customer_behavior_dataset_sin_outliers.csv`, 2229 filas × 28 columnas), se realizaron los siguientes pasos adicionales de preparación:

| Paso | Acción | Detalle |
|------|--------|---------|
| 1 | Eliminación de columnas no predictivas | `ID` (identificador), `Dt_Customer` (fecha de alta), `Year_Birth` (ya representado por `Edad`) |
| 2 | Limpieza de `Marital_Status` | Se mapearon los valores atípicos `"Absurd"`, `"YOLO"` y `"Alone"` (7 registros) a `"Single"` |
| 3 | One-Hot Encoding | Se codificaron `Education` y `Marital_Status` como variables dummy (con `drop_first=True`) |
| 4 | Escalado | Se normalizaron todas las features con `StandardScaler`, ya que las redes neuronales son sensibles a la escala de los datos |

Tras el preprocesamiento, el modelo contó con **30 features** de entrada.

### 7.3 División de datos

Se dividió el dataset en conjuntos de entrenamiento (80%) y testeo (20%) utilizando `train_test_split` con **estratificación** sobre `Response` para mantener la proporción original de clases en ambos conjuntos:

| Conjunto | Registros | Response=1 | Proporción |
|----------|-----------|------------|------------|
| Train | 1783 | 262 | 14.7% |
| Test | 446 | 66 | 14.8% |

> **Nota sobre el desbalance:** el dataset presenta un desbalance considerable (85% clase 0 vs. 15% clase 1). Esto implica que un modelo trivial que siempre prediga "no aceptó" obtendría ~85% de accuracy, por lo que las métricas más representativas son el **recall** y el **f1-score** de la clase positiva.

### 7.4 Arquitectura del modelo

Se implementó un **MLPClassifier** (Multi-Layer Perceptron) de `sklearn.neural_network` con la siguiente configuración:

| Parámetro | Valor | Justificación |
|-----------|-------|--------------|
| `hidden_layer_sizes` | (64, 32) | 2 capas ocultas: la primera captura patrones generales, la segunda los refina. Se eligieron 64 y 32 neuronas dado que hay 30 features de entrada. |
| `activation` | `relu` | Función de activación estándar recomendada en el material de clase. Desactiva neuronas que no aportan. |
| `solver` | `adam` | Algoritmo de optimización adaptativa de pesos, estándar para este tipo de modelos. |
| `max_iter` | 1000 | Suficiente para la convergencia sin riesgo de sobreajuste. |
| `random_state` | 42 | Reproducibilidad de resultados. |

**Arquitectura:** entrada(30) → capa1(64 neuronas) → capa2(32 neuronas) → salida(2 clases)  
**Convergencia:** el modelo convergió en **295 iteraciones**.

### 7.5 Métricas de evaluación

| Métrica | Clase 0 (No aceptó) | Clase 1 (Aceptó) | Global |
|---------|---------------------|-------------------|--------|
| **Precision** | 0.91 | 0.66 | — |
| **Recall** | 0.96 | 0.47 | — |
| **F1-Score** | 0.93 | 0.55 | — |
| **Accuracy** | — | — | **88.57%** |

**Matriz de confusión:**

|  | Predicho: No aceptó | Predicho: Aceptó |
|---|---|---|
| **Real: No aceptó** | 364 | 16 |
| **Real: Aceptó** | 35 | 31 |

**Lectura de la matriz:**
- De los 380 clientes que realmente no aceptaron, el modelo identificó correctamente a **364** (96% de acierto).
- De los 66 clientes que sí aceptaron, el modelo identificó correctamente a **31** (47% de acierto).
- Cuando el modelo predice que un cliente va a aceptar, acierta el **66%** de las veces.

### 7.6 Features más influyentes

Analizando los pesos de la primera capa de la red neuronal, las 10 características con mayor influencia en la predicción son:

| # | Feature | Peso promedio | Interpretación |
|---|---------|---------------|----------------|
| 1 | `Recency` | 0.2253 | Los días desde la última compra son el factor más relevante. |
| 2 | `Kidhome` | 0.2249 | La presencia de niños en el hogar influye fuertemente. |
| 3 | `Edad` | 0.2221 | La edad del cliente es un predictor importante. |
| 4 | `NumWebPurchases` | 0.2164 | Los clientes que compran por web tienen un patrón diferenciado. |
| 5 | `MntGoldProds` | 0.2080 | El gasto en productos premium revela un perfil de cliente distinto. |
| 6 | `NumWebVisitsMonth` | 0.2078 | La frecuencia de visitas web indica nivel de engagement. |
| 7 | `Marital_Status_Married` | 0.2056 | El estado civil (casado) tiene peso en la decisión. |
| 8 | `Marital_Status_Together` | 0.2039 | Vivir en pareja también influye. |
| 9 | `Marital_Status_Single` | 0.2024 | Los solteros presentan un patrón particular. |
| 10 | `Teenhome` | 0.2015 | La presencia de adolescentes también afecta. |

### 7.7 Conclusiones del modelo predictivo

El modelo de red neuronal logró una **accuracy del 88.57%** en la predicción de `Response`, superando significativamente el baseline de un clasificador trivial (~85%). Si bien el recall de la clase positiva (47%) indica que el modelo no detecta a todos los clientes que aceptarían la campaña, cuando predice una aceptación lo hace con un **66% de precisión**, lo cual ya representa información valiosa para la toma de decisiones.

**Hallazgos clave para el negocio:**
- Los clientes con **compras más recientes** (`Recency` bajo) tienen mayor probabilidad de aceptar nuevas campañas.
- La **composición familiar** (presencia de niños y adolescentes) influye notablemente: hogares sin hijos tienden a responder mejor.
- Los clientes de **mayor edad** y con hábito de **compra por web y productos premium** representan un perfil más receptivo.
- El **estado civil** aporta matices al perfil del cliente que acepta campañas.

**Archivo de resultados:** `resultados_prediccion_response.csv` (contiene las predicciones del conjunto de test con las probabilidades asignadas por el modelo).
