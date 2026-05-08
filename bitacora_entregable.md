# Bitácora de Proyecto ETL
**Integrantes:** Franco Gusberti, Máxima Risso Patrón, Ian Francisco Gubert Gamba, Avril Milagros Costa y Joaquín Sanchez
**Dataset:** `customer_behavior_dataset.csv`

---

## 📅 Fecha: 01/05/2026

- **Configuración inicial:** Armamos el entorno de trabajo en Python e importamos las librerías necesarias (`pandas`, `numpy` y `datetime`).
- **Carga de datos:** Leímos el archivo original `customer_behavior_dataset.csv`, que arrancó con 2240 registros y 29 columnas con datos de clientes.
- **Exploración:** Usamos `df.describe()` para ver un pantallazo estadístico rápido. Al toque notamos datos sin mucho sentido, como clientes con año de nacimiento 1893 (¡de más de 130 años!).
- **Detección de nulos:** Para agilizar el trabajo, armamos un resumen automático que nos muestra el tipo de dato, los valores únicos y la cantidad de nulos por columna. Esto nos sirvió para darnos cuenta de que faltaba información importante en ingresos (`Income`), cantidad de hijos y quejas.
- **Limpieza de duplicados:** Para evitar que cualquier dato repetido nos ensucie el análisis futuro, le pasamos un `drop_duplicates()`.

---

## 📅 Fecha: 02/05/2026

- **Tratamiento de nulos:** Decidimos no tratar a todos los nulos por igual, sino ir analizando según la variable.
  - **Lógica de negocio:** En las columnas donde "no hay dato" significa "cero" (como la cantidad de hijos, quejas o campañas aceptadas), pusimos directamente un `0`.
  - **Uso de la mediana:** Para los sueldos (`Income`), no podíamos poner un cero ni usar el promedio porque había sueldos exageradamente altos que nos iban a correr el número. Decidimos usar la **mediana**, que es mucho más representativa.
  - **Uso de la moda:** En el caso de las variables categóricas, decidimos rellenar los huecos con el valor que más se repite (la moda).
- **Ajuste de formatos:** Nos dimos cuenta de que algunas columnas de conteos (como cantidad de hijos) estaban en decimales. Las pasamos a números enteros para que mantengan el sentido lógico.

---

## 📅 Fecha: 04/05/2026

- **Manejo de Outliers (Atípicos):** Implementamos el método del Rango Intercuartílico (IQR) para buscar matemáticamente esos valores que se escapan de la distribución normal. 
- **Técnica de Capping:** Discutimos si convenía borrar las filas con outliers, pero íbamos a perder muchos datos valiosos. En lugar de eso, aplicamos la función `.clip()` para "limitar" los valores extremos al máximo o mínimo permitido por el rango IQR.
- **Filtros por errores graves:** Lo que sí decidimos eliminar definitivamente fueron los registros imposibles. Volamos de la base a los nacidos antes de 1930, a los que tenían sueldos bajo cero y a los sueldos altísimos (> 150.000) que nos desvirtuaban la media de la muestra.
- **Eliminación de columnas inútiles:** Programamos un filtro automático para buscar si alguna columna tenía el mismo valor en todos los clientes. Así detectamos y eliminamos `Z_CostContact` y `Z_Revenue`, porque al no tener variabilidad, no nos sirven para analizar nada.

---

## 📅 Fecha: 07/05/2026

- **Feature Engineering (Nuevas variables):** Empezamos a crear columnas nuevas para aportarle más valor a los datos.
  - Pasamos la fecha de alta (`Dt_Customer`) al formato correcto de fecha y extrajimos el mes y el año de registro.
  - Calculamos la `edad` restando el año de nacimiento al año de análisis (2026).
  - Creamos la columna `gasto_total` sumando todo lo que el cliente gastó en vinos, carnes, frutas, etc.
  - Hicimos lo mismo para crear un `total_compras` sumando los distintos canales de venta.
- **Estandarización (Renombrado):** Para que el dataset sea mucho más cómodo de leer para cualquier analista, renombramos las 29 columnas al español y en formato minúscula con guiones (por ejemplo, pasamos de `Year_Birth` a `anio_nacimiento`).
- **Auditoría final:** Armamos un script para comprobar que el resultado final no tenga nulos, ni duplicados y nos dé un resumen general de validación antes de guardar todo.
- Exportamos el trabajo de limpieza a `dataset_limpio.csv`.

---

## 📅 Fecha: 08/05/2026

- **Últimos ajustes al proceso:** Revisamos los códigos de todos los integrantes del grupo y consolidamos un pipeline final mucho más robusto.
- **Limpieza de gastos negativos:** Detectamos que algunas métricas de gasto en productos (como vinos) tenían valores menores a cero. Al tratarse de un error de sistema irreconciliable con la lógica comercial, descartamos también esos registros.
- **Redondeo final:** Revisamos las variables discretas para asegurarnos de que no nos queden cantidades con decimales. Variables como los días desde la última compra (`Recency`) o la cantidad de transacciones por web/catálogo se redondearon a tipo entero.
- **Consolidación de documentación:** Unificamos las decisiones técnicas de todos (como la justificación de usar la mediana y la técnica de IQR) para redactar esta bitácora y generar el reporte final que presentamos.
