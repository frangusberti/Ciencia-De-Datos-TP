# Bitácora de Trabajo – Proyecto ETL
## Introducción a la Ciencia de Datos – Cátedra Arriazu – 1C2026

---

**Integrantes:** Franco Gusberti  
**Dataset:** `customer_behavior_dataset.csv`  
**Herramientas:** Python 3.14, Pandas, NumPy  
**Repositorio:** https://github.com/frangusberti/Ciencia-De-Datos-TP

---

## 1. Extracción de Datos

**Fecha:** 01/05/2026  
**Responsable:** Franco Gusberti

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

**Fecha:** [Completar]  
**Responsable:** [Nombre]

### 2.1 Valores faltantes detectados

| Columna | Cantidad de nulos | Porcentaje | Decisión | Motivo |
|---------|------------------|------------|----------|--------|
| [Completar] | [Completar] | [Completar]% | [Eliminar/Rellenar con X] | [Motivo] |
| | | | | |
| | | | | |

### 2.2 Outliers detectados

| Columna | Valor sospechoso | Cantidad | Decisión | Motivo |
|---------|-----------------|----------|----------|--------|
| `Year_Birth` | [Completar: ej. valores < 1930] | [Completar] | [Eliminar/Mantener] | [Motivo] |
| `Income` | [Completar: ej. valores negativos] | [Completar] | [Eliminar/Corregir] | [Motivo] |
| `MntWines` | [Completar: ej. valores negativos] | [Completar] | [Eliminar/Corregir] | [Motivo] |
| | | | | |

### 2.3 Observaciones adicionales
- [Completar: columnas constantes, valores raros, duplicados, etc.]

---

## 3. Transformaciones Realizadas

**Fecha:** [Completar]  
**Responsable:** [Nombre]

### 3.1 Tratamiento de valores faltantes

| Columna | Método aplicado | Valor utilizado | Justificación |
|---------|----------------|-----------------|---------------|
| [Completar] | [Mediana/Media/Moda/Eliminación] | [Valor] | [Por qué elegiste este método] |
| | | | |

### 3.2 Tratamiento de outliers

| Columna | Acción | Filas afectadas | Justificación |
|---------|--------|-----------------|---------------|
| [Completar] | [Eliminadas/Corregidas] | [Cantidad] | [Por qué] |
| | | | |

### 3.3 Conversión de tipos de datos

| Columna | Tipo original | Tipo nuevo | Detalle |
|---------|--------------|------------|---------|
| `Dt_Customer` | object (texto) | datetime | Formato: DD-MM-YYYY |
| | | | |

### 3.4 Columnas eliminadas

| Columna | Motivo de eliminación |
|---------|-----------------------|
| `Z_CostContact` | Columna constante (valor = 3 para todos los registros). No aporta información. |
| `Z_Revenue` | Columna constante (valor = 11 para todos los registros). No aporta información. |
| | |

### 3.5 Columnas renombradas

| Nombre original | Nombre nuevo | Motivo |
|----------------|-------------|--------|
| [Completar si aplicaste renombramientos] | | |

### 3.6 Filas eliminadas

| Motivo | Condición | Cantidad eliminada |
|--------|-----------|-------------------|
| [Completar] | [ej. Year_Birth < 1930] | [Cantidad] |
| | | |

### 3.7 Feature Engineering (nuevas columnas creadas)

| Nueva columna | Fórmula / Lógica | Justificación |
|--------------|-------------------|---------------|
| [Completar: ej. Edad] | [ej. 2026 - Year_Birth] | [Para qué sirve] |
| | | |

---

## 4. Carga de Datos

**Fecha:** [Completar]  
**Responsable:** [Nombre]

- Archivo de salida: `customer_behavior_cleaned.csv`
- Dimensiones finales: **[Completar] filas × [Completar] columnas**
- Diferencia respecto al original: [Completar] filas eliminadas, [Completar] columnas eliminadas, [Completar] columnas nuevas

---

## 5. Registro de Versiones

| Versión | Fecha y Hora | Responsable | Descripción del cambio |
|---------|-------------|-------------|----------------------|
| v1.0 | [DD/MM/YYYY HH:MM] | [Nombre] | Carga inicial y exploración del dataset |
| v1.1 | [DD/MM/YYYY HH:MM] | [Nombre] | Tratamiento de valores faltantes |
| v1.2 | [DD/MM/YYYY HH:MM] | [Nombre] | Detección y tratamiento de outliers |
| v2.0 | [DD/MM/YYYY HH:MM] | [Nombre] | Feature engineering y limpieza final |
| v2.1 | [DD/MM/YYYY HH:MM] | [Nombre] | Exportación del dataset limpio |

---

## 6. Conclusiones

[Completar: resumen de lo realizado, decisiones clave tomadas, y estado final del dataset]
