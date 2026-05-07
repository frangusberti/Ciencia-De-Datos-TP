# Bitácora de Trabajo Integrada - Proyecto ETL
**Integrantes:** Franco Gusberti y Máxima
**Dataset:** `customer_behavior_dataset.csv`
**Fecha de elaboración:** Mayo 2026

---

## 1. Exploración Inicial y Setup (Trabajo Conjunto)
Franco y Máxima iniciaron el proyecto importando las librerías fundamentales (`pandas`, `numpy`, `datetime`) y realizando la carga del dataset original. 

- **Análisis preliminar:** Franco y Máxima ejecutaron rutinas de conteo de nulos (`df.isnull().sum()`) y obtuvieron resúmenes estadísticos (`df.describe()`) para entender la forma de los datos y detectar inconsistencias obvias a simple vista (como valores mínimos ilógicos en años y sueldos).

---

## 2. Tratamiento de Valores Nulos
Si bien Franco y Máxima detectaron la presencia de valores faltantes (especialmente en las columnas de hijos, quejas y campañas), el enfoque para lidiar con ellos tuvo sus diferencias complementarias:

- **Enfoque analítico (Máxima):** Optó por realizar un análisis inicial filtrando únicamente las columnas que presentaban nulos, evaluando la conveniencia de calcular el porcentaje de completitud antes de tomar decisiones apresuradas sobre cómo imputarlos.
- **Enfoque práctico de imputación (Franco):** Analizó la naturaleza de las variables y dedujo que muchos vacíos no eran errores, sino la simple "ausencia" del atributo (ej. no tener hijos o no haber presentado quejas). Por lo tanto:
  - Rellenó los nulos de `Kidhome`, `Complain`, `Response` y gastos con **0**.
  - Rellenó los nulos de `Income` (ingresos) utilizando la **mediana** estadística. Justificó esta decisión en que la mediana es menos sensible a sueldos extremadamente altos (outliers) que el promedio tradicional.

---

## 3. Análisis y Limpieza de Outliers (Valores Atípicos)
Franco y Máxima detectaron tempranamente la presencia de anomalías graves: personas nacidas antes de 1900 y clientes con ingresos negativos.

- **Detección robusta teórica y programática (Máxima):** Desarrolló un profundo debate estadístico. Descartó el uso del Teorema Central del Límite (TCL) para buscar anomalías, fundamentando que el uso de cuantiles es mucho más robusto. Creó la función automatizada `deteccion_outliers_iqr` basada en el Rango Intercuartílico (IQR) para reportar la cantidad de atípicos por cada columna. Además, iteró con bucles sobre grupos de consumo (`gastos_cotidianos`) y de hábitos (`compras_num`) para validar que no existieran valores de gasto menores a cero.
- **Filtro directo (Franco):** Tomó la información de estas anomalías lógicas y aplicó reglas de negocio directas para limpiar el dataset funcional: filtró y eliminó definitivamente a cualquier usuario cuyo `Year_Birth` fuera anterior a 1930 y cuyo `Income` fuera menor a cero.

---

## 4. Transformaciones y Feature Engineering
Esta sección se dividió en distintas mejoras que enriquecieron considerablemente el dataset original:

- **Estandarización de campañas (Máxima):** Identificó la necesidad de renombrar y estandarizar las variables de marketing (`AcceptedCmp1` a `Campaña 1`, etc.). Además, desarrolló bucles lógicos para calcular los totales de aceptación y rechazo por cada una de las 5 campañas históricas. Evaluó críticamente la redundancia existente en la variable `Response`.
- **Estandarización de Fechas y Creación de Variables (Franco):** 
  - Convirtió la columna `Dt_Customer` (que venía como texto) al formato correcto `datetime`.
  - Hizo "Feature Engineering" agregando tres columnas de gran valor analítico para el negocio: `Edad` (2026 - Año de nacimiento), `Total_Hijos` (suma de niños y adolescentes) y `Gasto_Total` (suma de todas las categorías de gasto del cliente).

---

## 5. Depuración de Columnas y Exportación
- **Columnas constantes:** Máxima notó que las columnas `Z_CostContact` y `Z_Revenue` requerían atención porque no encajaban en los esquemas lógicos. Franco realizó un análisis de varianza sobre ellas y descubrió que poseían **un único valor** constante (3 y 11 respectivamente) para todos los clientes de la base. Como las columnas sin varianza no aportan información analítica, Franco procedió a eliminarlas (`drop`).
- **Archivo Final:** Franco exportó el Dataframe ya procesado y limpio bajo un nuevo archivo llamado `customer_behavior_LIMPIO.csv`, el cual será la base para las próximas fases de análisis y visualización del equipo.
