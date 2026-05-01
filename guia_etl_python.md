# 🐍 Guía: Aprendé a hacer ETL con Python

Esta guía te va a enseñar paso a paso cómo hacer el proceso ETL (Extract, Transform, Load) sobre tu dataset `customer_behavior_dataset.csv`, usando Python y Pandas.

> [!IMPORTANT]
> No te copies el código ciegamente. **Leé cada sección**, entendé qué hace, y escribilo vos mismo en tu script. Así es como se aprende.

---

## 📋 ¿Qué pide el enunciado?

Tu TP pide:
1. Interpretar el dataset (tema, dimensiones, valores faltantes, outliers)
2. Describir las variables
3. Registrar cambios de nombres de columnas
4. Registrar eliminación de filas/columnas con motivo
5. Describir todas las transformaciones realizadas
6. Trabajar con versionado (firma, fecha y hora)

Todo esto se presenta como una **Bitácora de Trabajo**.

---

## Parte 0: Setup – Preparar tu entorno

Antes de empezar, necesitás tener instalado `pandas` y `numpy`. Abrí una terminal y ejecutá:

```bash
pip install pandas numpy
```

Creá un archivo Python nuevo (por ejemplo `mi_etl.py`) y arrancá con estos imports:

```python
import pandas as pd
import numpy as np
from datetime import datetime
```

### ¿Qué es cada cosa?
| Librería | ¿Para qué sirve? |
|----------|------------------|
| `pandas` | Manipular datos en tablas (DataFrames) |
| `numpy` | Operaciones numéricas y matemáticas |
| `datetime` | Trabajar con fechas y horas |

---

## Parte 1: EXTRACT – Cargar los datos

### Concepto
La fase de **extracción** consiste en leer los datos desde su fuente (en este caso un archivo CSV).

### Código
```python
# Leer el archivo CSV
df = pd.read_csv(r"c:\Users\PC\OneDrive\Escritorio\CCiencia datos\customer_behavior_dataset.csv")
```

### Ahora explorá el dataset
Estos comandos te van a servir para entender qué tenés:

```python
# Ver las primeras 5 filas
print(df.head())

# Ver las dimensiones (filas, columnas)
print(f"Dimensiones: {df.shape}")  
# Esto te dice: (2241 filas, 29 columnas) aprox.

# Ver los tipos de datos de cada columna
print(df.dtypes)

# Ver un resumen estadístico
print(df.describe())

# Ver información general (tipos, nulos, memoria)
print(df.info())
```

### 💡 ¿Qué aprendés acá?
- `df.head()` → Muestra las primeras filas. Útil para ver cómo lucen los datos.
- `df.shape` → Te da una **tupla** (filas, columnas). Esto es lo que el enunciado llama "dimensiones".
- `df.dtypes` → Te dice el tipo de cada columna (int, float, object...).
- `df.describe()` → Estadísticas: media, min, max, percentiles. **Acá podés detectar outliers**.
- `df.info()` → Te muestra cuántos valores no-nulos tiene cada columna.

### 🎯 Ejercicio para vos
Ejecutá cada comando y anotá:
- ¿Cuántas filas y columnas hay?
- ¿Qué columnas son numéricas y cuáles son texto?
- ¿Hay columnas con menos valores no-nulos que el total de filas? (eso son nulos)

---

## Parte 2: Entender las variables

### Las columnas de tu dataset

| Columna | ¿Qué significa? | Tipo |
|---------|-----------------|------|
| `ID` | Identificador único del cliente | Numérico |
| `Year_Birth` | Año de nacimiento | Numérico |
| `Education` | Nivel educativo (Graduation, PhD, Master, etc.) | Categórico |
| `Marital_Status` | Estado civil | Categórico |
| `Income` | Ingreso anual del hogar | Numérico |
| `Kidhome` | Cantidad de niños en el hogar | Numérico |
| `Teenhome` | Cantidad de adolescentes en el hogar | Numérico |
| `Dt_Customer` | Fecha en que se hizo cliente | Fecha |
| `Recency` | Días desde la última compra | Numérico |
| `MntWines` | Gasto en vinos | Numérico |
| `MntFruits` | Gasto en frutas | Numérico |
| `MntMeatProducts` | Gasto en carnes | Numérico |
| `MntFishProducts` | Gasto en pescado | Numérico |
| `MntSweetProducts` | Gasto en dulces | Numérico |
| `MntGoldProds` | Gasto en productos gold/premium | Numérico |
| `NumDealsPurchases` | Compras con descuento | Numérico |
| `NumWebPurchases` | Compras por web | Numérico |
| `NumCatalogPurchases` | Compras por catálogo | Numérico |
| `NumStorePurchases` | Compras en tienda | Numérico |
| `NumWebVisitsMonth` | Visitas web mensuales | Numérico |
| `AcceptedCmp1-5` | Si aceptó campaña 1 a 5 | Binario (0/1) |
| `Complain` | Si realizó queja | Binario (0/1) |
| `Z_CostContact` | Costo de contacto (constante) | Numérico |
| `Z_Revenue` | Revenue (constante) | Numérico |
| `Response` | Respuesta a última campaña | Binario (0/1) |

---

## Parte 3: TRANSFORM – Detectar y tratar valores faltantes

### 3.1 Contar valores faltantes

```python
# Ver la cantidad de nulos por columna
nulos = df.isnull().sum()
print(nulos[nulos > 0])  # Solo mostrar las que tienen nulos
```

### ¿Qué hace esto?
- `df.isnull()` → Crea un DataFrame de True/False (True = faltante)
- `.sum()` → Suma los True (cada True vale 1)
- El filtro `[nulos > 0]` → Solo muestra columnas con al menos 1 nulo

### También podés ver el porcentaje de nulos:
```python
porcentaje_nulos = (df.isnull().sum() / len(df)) * 100
print(porcentaje_nulos[porcentaje_nulos > 0].round(2))
```

### 3.2 Decidir qué hacer con los nulos

Hay varias estrategias:

| Estrategia | Cuándo usarla | Código |
|-----------|---------------|--------|
| **Eliminar filas** | Cuando hay pocos nulos | `df.dropna()` |
| **Rellenar con mediana** | Para columnas numéricas con outliers | `df['col'].fillna(df['col'].median())` |
| **Rellenar con media** | Para columnas numéricas sin outliers | `df['col'].fillna(df['col'].mean())` |
| **Rellenar con moda** | Para columnas categóricas | `df['col'].fillna(df['col'].mode()[0])` |

### Ejemplo práctico:
```python
# Rellenar Income (numérica) con la mediana
# ¿Por qué mediana y no media? Porque la mediana no se ve afectada por outliers
df['Income'] = df['Income'].fillna(df['Income'].median())
```

### 💡 Concepto importante: ¿Media vs Mediana?
- **Media** = promedio. Si tenés [1, 2, 3, 100], la media es 26.5 (¡distorsionada por el 100!)
- **Mediana** = el valor del medio. En [1, 2, 3, 100], la mediana es 2.5 (más representativa)

### 🎯 Ejercicio
1. Ejecutá el conteo de nulos
2. Para cada columna con nulos, decidí: ¿eliminás la fila? ¿rellenás? ¿con qué valor?
3. Anotá tu decisión y el motivo (esto va en la bitácora)

---

## Parte 4: TRANSFORM – Detectar outliers (valores atípicos)

### 4.1 ¿Qué es un outlier?
Un valor que está muy lejos del resto. Por ejemplo, un ingreso de -64452 o un año de nacimiento de 1893.

### 4.2 Método visual: Usar `describe()`
```python
print(df.describe())
```
Mirá el `min` y `max` de cada columna. Preguntate:
- ¿Tiene sentido un `Year_Birth` de 1893? (tendría ~133 años 🤔)
- ¿Tiene sentido un `Income` negativo?
- ¿Tiene sentido un `MntWines` negativo?

### 4.3 Detectar outliers con el rango intercuartílico (IQR)
```python
def detectar_outliers_iqr(df, columna):
    """Detecta outliers usando el método IQR"""
    Q1 = df[columna].quantile(0.25)
    Q3 = df[columna].quantile(0.75)
    IQR = Q3 - Q1
    
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    
    outliers = df[(df[columna] < limite_inferior) | (df[columna] > limite_superior)]
    
    print(f"\n--- {columna} ---")
    print(f"Q1: {Q1}, Q3: {Q3}, IQR: {IQR}")
    print(f"Límites: [{limite_inferior}, {limite_superior}]")
    print(f"Outliers encontrados: {len(outliers)}")
    
    return outliers
```

### ¿Qué es IQR?
- **Q1** (percentil 25): el 25% de los datos están por debajo de este valor
- **Q3** (percentil 75): el 75% de los datos están por debajo
- **IQR** = Q3 - Q1 (el rango donde está el 50% central de los datos)
- Todo lo que esté más allá de `1.5 * IQR` se considera outlier

### Ejemplo de uso:
```python
# Detectar outliers en Income
outliers_income = detectar_outliers_iqr(df, 'Income')
print(outliers_income[['ID', 'Income']])
```

### 4.4 Revisar valores "sospechosos" que ya viste en los datos

En tu dataset, mirando los datos crudos, se ven cosas raras:
```python
# Años de nacimiento sospechosos (personas de más de 120 años)
print(df[df['Year_Birth'] < 1930])  # ¿1893? ¿1899? ¿1900?

# Ingresos negativos
print(df[df['Income'] < 0])

# Valores negativos en gastos (no deberían existir)
columnas_gasto = ['MntWines', 'MntFruits', 'MntMeatProducts', 
                  'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
for col in columnas_gasto:
    negativos = df[df[col] < 0]
    if len(negativos) > 0:
        print(f"{col} tiene {len(negativos)} valores negativos")

# Valores decimales "raros" en Recency (debería ser entero)
print(df[df['Recency'] != df['Recency'].round(0)][['ID', 'Recency']])

# Valor raro en NumWebPurchases (75.977... cuando debería ser entero)
print(df[df['NumWebPurchases'] != df['NumWebPurchases'].round(0)][['ID', 'NumWebPurchases']])
```

### 🎯 Ejercicio
1. Corré la función `detectar_outliers_iqr` para `Income`, `Year_Birth`, y las columnas `Mnt*`
2. Anotá cuáles outliers encontraste
3. Decidí: ¿los eliminás? ¿los corregís? Justificá

---

## Parte 5: TRANSFORM – Limpieza y transformaciones

### 5.1 Tratar outliers que decidiste eliminar/corregir

```python
# Ejemplo: eliminar filas con Year_Birth < 1930 (edades irrealistas)
df = df[df['Year_Birth'] >= 1930]
print(f"Filas después de filtrar Year_Birth: {df.shape[0]}")

# Ejemplo: eliminar filas con Income negativo
df = df[df['Income'] >= 0]

# Ejemplo: corregir valores negativos en gastos (reemplazar por 0 o por NaN)
for col in columnas_gasto:
    df.loc[df[col] < 0, col] = np.nan  # Marcar como faltante para tratar después
```

> [!WARNING]
> Cada vez que eliminés o modifiqués filas, **anotá cuántas y por qué**. Esto va en tu bitácora.

### 5.2 Convertir fechas

```python
# Convertir Dt_Customer a formato fecha
# El formato en el CSV es DD-MM-YYYY
df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], format='%d-%m-%Y', errors='coerce')
```

### ¿Qué significan los parámetros?
- `format='%d-%m-%Y'` → Le dice a pandas cómo está escrita la fecha: día-mes-año
- `errors='coerce'` → Si alguna fecha no se puede convertir, pone NaT (Not a Time) en vez de dar error

### Formatos de fecha comunes:
| Formato | Ejemplo |
|---------|---------|
| `%d-%m-%Y` | 04-09-2012 |
| `%Y-%m-%d` | 2012-09-04 |
| `%m/%d/%Y` | 09/04/2012 |

### 5.3 Eliminar columnas innecesarias

```python
# Z_CostContact y Z_Revenue son constantes (siempre 3 y 11)
# No aportan información → se eliminan
print(df['Z_CostContact'].unique())  # [3] → siempre vale 3
print(df['Z_Revenue'].unique())      # [11] → siempre vale 11

df = df.drop(columns=['Z_CostContact', 'Z_Revenue'])
```

### 💡 ¿Por qué eliminar columnas constantes?
Porque no aportan variabilidad. Si todos los clientes tienen el mismo valor, no sirve para diferenciarlos ni para análisis.

### 5.4 Renombrar columnas (opcional pero recomendado)

```python
# Si querés renombrar para que quede más claro:
df = df.rename(columns={
    'Dt_Customer': 'Fecha_Cliente',
    'Year_Birth': 'Anio_Nacimiento',
    'Kidhome': 'Ninos_Hogar',
    'Teenhome': 'Adolescentes_Hogar',
    'Recency': 'Dias_Ultima_Compra'
})
```

> [!NOTE]
> Si renombrás columnas, **registralo** en tu bitácora: columna original → nombre nuevo y motivo.

### 5.5 Eliminar filas duplicadas

```python
# Verificar duplicados
duplicados = df.duplicated().sum()
print(f"Filas duplicadas: {duplicados}")

# Si hay duplicados, eliminarlos
if duplicados > 0:
    df = df.drop_duplicates()
    print(f"Filas después de eliminar duplicados: {df.shape[0]}")
```

---

## Parte 6: TRANSFORM – Feature Engineering (crear nuevas columnas)

### 6.1 Calcular la edad
```python
df['Edad'] = 2026 - df['Year_Birth']
```

### 6.2 Total de hijos
```python
df['Total_Hijos'] = df['Kidhome'] + df['Teenhome']
```

### 6.3 Gasto total
```python
columnas_gasto = ['MntWines', 'MntFruits', 'MntMeatProducts', 
                  'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
df['Gasto_Total'] = df[columnas_gasto].sum(axis=1)
```

### ¿Qué es `axis=1`?
- `axis=0` → Opera sobre filas (vertical, hacia abajo)
- `axis=1` → Opera sobre columnas (horizontal, a lo largo de la fila)

Cuando usás `.sum(axis=1)`, sumás los valores de esas columnas **para cada fila**.

### 6.4 Total de compras
```python
columnas_compras = ['NumDealsPurchases', 'NumWebPurchases', 
                    'NumCatalogPurchases', 'NumStorePurchases']
df['Total_Compras'] = df[columnas_compras].sum(axis=1)
```

---

## Parte 7: LOAD – Guardar el resultado

```python
# Guardar el DataFrame limpio en un nuevo CSV
df.to_csv(r"c:\Users\PC\OneDrive\Escritorio\CCiencia datos\customer_behavior_cleaned.csv", index=False)
print("✅ Archivo guardado exitosamente")
```

### ¿Qué es `index=False`?
Pandas por defecto le agrega un índice numérico (0, 1, 2...) como columna extra al guardar. Con `index=False` evitás eso.

---

## Parte 8: Armar la Bitácora

Tu informe debe documentar **todo** lo que hiciste. Acá va una estructura sugerida:

```
BITÁCORA DE TRABAJO – Proyecto ETL
===================================
Equipo: [nombres]
Fecha: [fecha]

1. EXTRACCIÓN
   - Fuente: customer_behavior_dataset.csv
   - Dimensiones originales: X filas × Y columnas
   - Herramienta: Python 3.x con Pandas

2. EXPLORACIÓN INICIAL
   - Variables numéricas: [listar]
   - Variables categóricas: [listar]
   - Valores faltantes encontrados:
     * Income: X nulos (Y%)
     * Kidhome: X nulos (Y%)
     * [etc.]
   - Outliers detectados:
     * Year_Birth: 3 valores < 1930
     * Income: 1 valor negativo
     * MntWines: 2 valores negativos
     * [etc.]

3. TRANSFORMACIONES
   3.1 Tratamiento de nulos
       - Income: rellenado con mediana ($XX.XXX). Motivo: [...]
       - [etc.]
   3.2 Tratamiento de outliers  
       - Se eliminaron X filas con Year_Birth < 1930. Motivo: edades > 120 años
       - [etc.]
   3.3 Conversión de tipos
       - Dt_Customer: convertido de string a datetime
   3.4 Columnas eliminadas
       - Z_CostContact: eliminada por ser constante (valor = 3)
       - Z_Revenue: eliminada por ser constante (valor = 11)
   3.5 Columnas renombradas
       - [original] → [nuevo nombre]: motivo
   3.6 Feature Engineering
       - Edad = 2026 - Year_Birth
       - Total_Hijos = Kidhome + Teenhome
       - [etc.]

4. CARGA
   - Destino: customer_behavior_cleaned.csv
   - Dimensiones finales: X filas × Y columnas

5. VERSIONADO
   - v1.0 [fecha hora] [nombre]: Exploración inicial
   - v1.1 [fecha hora] [nombre]: Limpieza de nulos
   - v2.0 [fecha hora] [nombre]: Feature engineering
```

---

## 📚 Cheat Sheet – Funciones útiles de Pandas

| Función | ¿Qué hace? | Ejemplo |
|---------|-------------|---------|
| `df.head(n)` | Primeras n filas | `df.head(10)` |
| `df.tail(n)` | Últimas n filas | `df.tail(5)` |
| `df.shape` | (filas, columnas) | `print(df.shape)` |
| `df.dtypes` | Tipos de datos | `print(df.dtypes)` |
| `df.info()` | Resumen completo | `df.info()` |
| `df.describe()` | Estadísticas | `df.describe()` |
| `df.isnull().sum()` | Contar nulos | `df.isnull().sum()` |
| `df['col'].unique()` | Valores únicos | `df['Education'].unique()` |
| `df['col'].value_counts()` | Frecuencia de valores | `df['Education'].value_counts()` |
| `df.duplicated().sum()` | Contar duplicados | `df.duplicated().sum()` |
| `df.dropna()` | Eliminar filas con nulos | `df.dropna(subset=['Income'])` |
| `df['col'].fillna(val)` | Rellenar nulos | `df['col'].fillna(0)` |
| `df.drop(columns=[...])` | Eliminar columnas | `df.drop(columns=['Z_Revenue'])` |
| `df.rename(columns={...})` | Renombrar columnas | `df.rename(columns={'old': 'new'})` |
| `df.drop_duplicates()` | Eliminar duplicados | `df.drop_duplicates()` |
| `pd.to_datetime()` | Convertir a fecha | `pd.to_datetime(df['col'])` |

---

## ⚠️ Errores comunes

### 1. `SettingWithCopyWarning`
```python
# ❌ Mal - puede no funcionar
df_filtrado = df[df['Income'] > 0]
df_filtrado['Edad'] = 2026 - df_filtrado['Year_Birth']

# ✅ Bien - usá .copy()
df_filtrado = df[df['Income'] > 0].copy()
df_filtrado['Edad'] = 2026 - df_filtrado['Year_Birth']
```

### 2. Olvidarse de reasignar
```python
# ❌ Mal - esto NO modifica df
df.drop(columns=['Z_Revenue'])

# ✅ Bien - reasignar el resultado
df = df.drop(columns=['Z_Revenue'])
```

### 3. Confundir `=` con `==`
```python
# ❌ Mal - esto asigna, no compara
df[df['Income'] = 0]

# ✅ Bien - doble igual para comparar
df[df['Income'] == 0]
```

---

## 🚀 Orden de trabajo sugerido

1. **Cargá los datos** y explorá con `head()`, `shape`, `info()`, `describe()`
2. **Contá los nulos** y decidí qué hacer con cada uno
3. **Buscá outliers** con `describe()` y la función IQR
4. **Limpiá**: tratá nulos, eliminá outliers, convertí fechas
5. **Eliminá** columnas constantes (Z_CostContact, Z_Revenue)
6. **Creá** variables nuevas (Edad, Gasto_Total, etc.)
7. **Guardá** el resultado
8. **Documentá todo** en tu bitácora

> [!TIP]
> Trabajá en un Jupyter Notebook si podés. Cada celda puede ser un paso, y podés ir viendo los resultados a medida que avanzás. Si no, usá `print()` después de cada operación para verificar.
