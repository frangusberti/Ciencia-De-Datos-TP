# Bitácora de Trabajo Integrada - Proyecto ETL
**Integrantes:** Franco Gusberti, Máxima y Joaquín
**Dataset:** `customer_behavior_dataset.csv`
**Fecha de elaboración:** Mayo 2026

---

## 1. Exploración Inicial y Setup (Trabajo Conjunto)
Franco, Máxima y Joaquín iniciaron el proyecto importando las librerías fundamentales (`pandas`, `numpy`, `datetime`) y realizando la carga del dataset original. 

- **Análisis preliminar:** El equipo ejecutó rutinas de conteo de nulos (`df.isnull().sum()`) y obtuvieron resúmenes estadísticos (`df.describe()`) para entender la forma de los datos y detectar inconsistencias obvias a simple vista (como valores mínimos ilógicos en años y sueldos).
- **Control de Duplicados:** Joaquín implementó un paso inicial fundamental para la sanidad de los datos, identificando y eliminando las filas completamente duplicadas utilizando la función `drop_duplicates()`.

---

## 2. Tratamiento de Valores Nulos
Si bien el equipo detectó la presencia de valores faltantes (especialmente en las columnas de hijos, quejas y campañas), el enfoque para lidiar con ellos tuvo sus diferencias complementarias:

- **Enfoque analítico (Máxima):** Optó por realizar un análisis inicial filtrando únicamente las columnas que presentaban nulos, evaluando la conveniencia de calcular el porcentaje de completitud antes de tomar decisiones apresuradas sobre cómo imputarlos.
- **Enfoque práctico de imputación (Franco):** Analizó la naturaleza de las variables y dedujo que muchos vacíos no eran errores, sino la simple "ausencia" del atributo (ej. no tener hijos o no haber presentado quejas). Por lo tanto:
  - Rellenó los nulos de `Kidhome`, `Complain`, `Response` y gastos con **0**.
  - Rellenó los nulos de `Income` (ingresos) utilizando la **mediana** estadística. Justificó esta decisión en que la mediana es menos sensible a sueldos extremadamente altos (outliers) que el promedio tradicional.
- **Enfoque estadístico global (Joaquín):** Decidió no perder información ni rellenar con ceros. Su enfoque consistió en diferenciar por tipo de dato: imputó todos los nulos numéricos utilizando la **media** (`mean`), y todos los nulos categóricos utilizando la **moda** (`mode`). Además, descubrió que columnas como `Kidhome` estaban cargadas como decimales (`float`) y estandarizó el formato convirtiéndolas obligatoriamente a tipo entero (`int`).

---

## 3. Análisis y Limpieza de Outliers (Valores Atípicos)
El equipo detectó tempranamente la presencia de anomalías graves: personas nacidas antes de 1900 y clientes con ingresos negativos.

- **Detección robusta teórica y programática (Máxima):** Desarrolló un profundo debate estadístico. Descartó el uso del Teorema Central del Límite (TCL) para buscar anomalías, fundamentando que el uso de cuantiles es mucho más robusto. Creó la función automatizada `deteccion_outliers_iqr` basada en el Rango Intercuartílico (IQR) para reportar la cantidad de atípicos por cada columna. Además, iteró con bucles sobre grupos de consumo (`gastos_cotidianos`) y de hábitos (`compras_num`) para validar que no existieran valores de gasto menores a cero.
- **Filtro directo (Franco):** Tomó la información de estas anomalías lógicas y aplicó reglas de negocio directas para limpiar el dataset funcional: filtró y eliminó definitivamente a cualquier usuario cuyo `Year_Birth` fuera anterior a 1930 y cuyo `Income` fuera menor a cero.
- **Técnica de Capping (Joaquín):** Al igual que Máxima, utilizó el método IQR para detectar atípicos, pero decidió no eliminarlos de la base de datos (para no reducir el dataset). En su lugar, aplicó una técnica de **capping** (usando la función `clip()`), reemplazando los valores que excedían los límites directamente por el valor máximo o mínimo permitido por el rango.

---

## 4. Transformaciones y Feature Engineering
Esta sección se dividió en distintas mejoras que enriquecieron considerablemente el dataset original:

- **Estandarización de campañas (Máxima):** Identificó la necesidad de renombrar y estandarizar las variables de marketing (`AcceptedCmp1` a `Campaña 1`, etc.). Además, desarrolló bucles lógicos para calcular los totales de aceptación y rechazo por cada una de las 5 campañas históricas. Evaluó críticamente la redundancia existente en la variable `Response`.
- **Estandarización de Fechas y Creación de Variables (Franco y Joaquín):** 
  - Ambos convirtieron la columna `Dt_Customer` al formato correcto `datetime` (Joaquín además extrajo año y mes en columnas separadas).
  - Hicieron "Feature Engineering" agregando columnas de gran valor analítico: edad del cliente, cantidad total de compras en todos los canales y el gasto total unificado.
- **Renombrado Masivo y Traducción (Joaquín):** Notó que sería más legible trabajar con el dataset en español y en formato estandarizado, por lo que aplicó un diccionario de traducción masiva para convertir las 29 columnas originales (ej. `Year_Birth` a `anio_nacimiento`, `NumWebPurchases` a `compras_web`).

---

## 5. Depuración de Columnas y Exportación
- **Columnas constantes:** Máxima notó que las columnas `Z_CostContact` y `Z_Revenue` requerían atención porque no encajaban en los esquemas lógicos. Franco realizó un análisis de varianza sobre ellas y descubrió que poseían **un único valor** constante (3 y 11 respectivamente) para todos los clientes de la base. Como las columnas sin varianza no aportan información analítica, Franco procedió a eliminarlas (`drop`).
- **Exportación y Auditoría Final:** 
  - Franco exportó un Dataframe limpio bajo el archivo `customer_behavior_LIMPIO.csv`.
  - Por su parte, Joaquín exportó su versión como `dataset_limpio.csv` y añadió un **Reporte de Calidad Final** automatizado. Este script imprime por consola un resumen ejecutivo inmediato de cómo quedó el dataset (nulos restantes, duplicados eliminados, dimensiones finales, y promedios) ideal para el control de calidad antes de la visualización.
