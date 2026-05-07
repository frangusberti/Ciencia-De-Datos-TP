# Bitácora de Trabajo Integrada - Proyecto ETL
**Integrantes:** Franco Gusberti, Máxima Risso Patrón y Joaquín Sanchez.
**Dataset:** `customer_behavior_dataset.csv`
**Fecha de elaboración:** Mayo 2026

---

## 1. Exploración Inicial y Setup
Se inició el proyecto importando las librerías fundamentales (`pandas`, `numpy`, `datetime`) y realizando la carga del dataset original. 

- **Análisis preliminar:** Se ejecutaron rutinas de conteo de nulos (`df.isnull().sum()`) y se obtuvieron resúmenes estadísticos (`df.describe()`) para entender la forma de los datos y detectar inconsistencias obvias a simple vista (como valores mínimos ilógicos en años y sueldos).
- **Control de Duplicados:** Se implementó un paso inicial fundamental para la sanidad de los datos, identificando y eliminando las filas completamente duplicadas utilizando la función `drop_duplicates()`.

---

## 2. Tratamiento de Valores Nulos
Tras detectar la presencia de valores faltantes (especialmente en las columnas de hijos, quejas y campañas), se plantearon y aplicaron diferentes enfoques complementarios:

- **Análisis y Evaluación:** Se realizó un análisis inicial filtrando únicamente las columnas que presentaban nulos, evaluando la conveniencia de calcular el porcentaje de completitud antes de tomar decisiones sobre cómo imputarlos.
- **Imputación Lógica:** Al analizar la naturaleza de las variables, se dedujo que muchos vacíos no eran errores, sino la simple "ausencia" del atributo (ej. no tener hijos o no haber presentado quejas). Por lo tanto, se rellenaron los nulos de `Kidhome`, `Complain`, `Response` y gastos con **0**.
- **Imputación Estadística:** Para no perder información valiosa, se aplicó un enfoque diferenciado por tipo de dato:
  - Los nulos numéricos (como los ingresos en `Income`) se imputaron utilizando medidas de tendencia central como la **media** y la **mediana**. Se evaluó que la mediana es menos sensible a sueldos extremadamente altos (outliers).
  - Los nulos categóricos se imputaron utilizando la **moda**.
- **Conversión de Tipos:** Se descubrió que columnas como `Kidhome` estaban cargadas como decimales (`float`) y se estandarizó el formato convirtiéndolas obligatoriamente a tipo entero (`int`).

---

## 3. Análisis y Limpieza de Outliers (Valores Atípicos)
Se detectó tempranamente la presencia de anomalías graves: personas nacidas antes de 1900 y clientes con ingresos negativos.

- **Detección Robusta (IQR):** Se desarrolló un profundo debate estadístico, descartando el uso del Teorema Central del Límite (TCL) para buscar anomalías y fundamentando que el uso de cuantiles es mucho más robusto. Se creó una función automatizada basada en el Rango Intercuartílico (IQR) para reportar la cantidad de atípicos por cada columna. Además, se iteró con bucles sobre grupos de consumo (`gastos_cotidianos`) y de hábitos (`compras_num`) para validar que no existieran valores de gasto menores a cero.
- **Técnica de Capping y Filtrado:** En lugar de eliminar indiscriminadamente todas las filas con valores atípicos (lo cual reduciría el dataset), se aplicó una técnica de **capping** (usando la función `clip()`), reemplazando los valores que excedían los límites directamente por el valor máximo o mínimo permitido por el rango. Para las anomalías lógicas irrefutables (ej. `Year_Birth` anterior a 1930 o `Income` negativo), se aplicaron filtros directos para limpiar el dataset funcional.

---

## 4. Transformaciones y Feature Engineering
Esta sección se dividió en distintas mejoras que enriquecieron considerablemente el dataset original:

- **Estandarización de Campañas:** Se identificó la necesidad de renombrar y estandarizar las variables de marketing. Se desarrollaron bucles lógicos para calcular los totales de aceptación y rechazo por cada una de las 5 campañas históricas, y se evaluó críticamente la redundancia existente en la variable `Response`.
- **Estandarización de Fechas:** Se convirtió la columna `Dt_Customer` al formato correcto `datetime`, y se extrajeron el año y el mes en columnas separadas para facilitar el análisis temporal.
- **Creación de Variables (Feature Engineering):** Se agregaron columnas de gran valor analítico para el negocio: edad del cliente, cantidad total de compras en todos los canales y el gasto total unificado.
- **Renombrado Masivo y Traducción:** Para lograr una mayor legibilidad, se aplicó un diccionario de traducción masiva para convertir las 29 columnas originales al español en un formato estandarizado (ej. `Year_Birth` a `anio_nacimiento`, `NumWebPurchases` a `compras_web`).

---

## 5. Depuración de Columnas y Exportación Final
- **Eliminación de Columnas Constantes:** Se notó que las columnas `Z_CostContact` y `Z_Revenue` requerían atención porque no encajaban en los esquemas lógicos. Un análisis de varianza demostró que poseían **un único valor** constante (3 y 11 respectivamente) para todos los clientes de la base. Al no aportar información analítica, se procedió a eliminarlas (`drop`).
- **Exportación y Auditoría:** Se exportó la versión consolidada del Dataframe bajo el archivo `dataset_limpio.csv`. Además, se añadió un **Reporte de Calidad Final** automatizado que imprime por consola un resumen ejecutivo inmediato de cómo quedó el dataset (nulos restantes, duplicados eliminados, dimensiones finales y promedios), ideal para el control de calidad antes de pasar a la fase de visualización.
