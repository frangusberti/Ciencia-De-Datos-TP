# Bitácora de Trabajo - Proyecto Ciencia de Datos

**Integrantes:** Franco Gusberti
**Dataset:** customer_behavior_dataset.csv
**Fecha de inicio:** 1 de mayo de 2026

---

### [Franco] - 1. Primer contacto con los datos (01/05)
Cargué el dataset usando Pandas para ver con qué me encontraba. El archivo tiene **2240 filas** y **29 columnas**. 

Usé `df.info()` y `df.describe()` para mirar los números. Vi que hay de todo: años de nacimiento, ingresos, cuántos hijos tienen y cuánto gastaron en cosas como vino o carne.

### [Franco] - 2. Limpieza de columnas "inútiles"
Me puse a ver cuántos valores únicos tiene cada columna y encontré que `Z_CostContact` y `Z_Revenue` tienen siempre el mismo número (3 y 11) para todos los registros. 
**Lo que hice:** Las borré directamente porque no sirven para comparar nada si son todos iguales.

### [Franco] - 3. El lío de los valores nulos
Cuando conté los nulos (`df.isnull().sum()`), saltaron un montón de agujeros, sobre todo en `Kidhome` y `Complain`.

**Mi análisis:**
Llegué a la conclusión de que no son errores de carga, sino que el dato es directamente "cero".
- Si en `Complain` (quejas) no hay nada, es bastante lógico asumir que el cliente nunca se quejó.
- Si en `Kidhome` (hijos) no hay nada, es que no tiene hijos.
- Lo mismo pasa con las campañas de marketing (`AcceptedCmp`).

**Lo que hice:** En lugar de borrar a esos clientes (lo cual nos haría perder mucha información valiosa), rellené esos huecos con el número **0**. 

**Los nulos de Income:** Me quedaron 24 nulos colgados en la columna de sueldos (`Income`). Acá no podía poner 0 porque nadie gana cero. Decidí rellenarlos usando la **mediana** de la columna. Elegí la mediana y no el promedio (media) porque los sueldos suelen tener picos raros (gente que gana fortunas) y eso distorsionaría el valor de reemplazo haciéndolo poco representativo.

### [Franco] - 4. Limpiando la mugre (Outliers)
Me puse a revisar los años de nacimiento y los sueldos para ver si había datos fuera de lugar.
- Encontré años de nacimiento súper bizarros, onda 1893. ¡Es imposible que tengamos clientes de 130 años! Evidentemente fue un error al tipear o datos de prueba. Decidí volar del dataset a todos los nacidos antes de 1930 para limpiar esa mugre.
- También metí un filtro por las dudas para asegurarme de que nadie tenga sueldo negativo, porque lógicamente no tiene sentido tener ingresos bajo cero.

### [Franco] - 5. Ajuste de Fechas y Feature Engineering (Nuevas columnas)
- La columna `Dt_Customer` (cuando se hicieron clientes) estaba guardada como texto. La pasé a formato `datetime` de verdad para que después podamos hacer gráficos o filtrar por fecha sin andar renegando.
- Me armé un par de columnas extra que nos van a re servir para analizar mejor los perfiles de los clientes en la próxima etapa:
  - `Edad`: Resté el año actual (2026) menos el año de nacimiento para tener la edad de frente en lugar de andar calculándola cada vez.
  - `Total_Hijos`: Sumé los nenes (`Kidhome`) y los adolescentes (`Teenhome`) para tener un indicador rápido del tamaño de la familia.
  - `Gasto_Total`: Sumé todas las columnas de productos (vinos, carnes, frutas, etc.) para tener un número general de cuánta plata deja cada cliente y ver quiénes son los más valiosos.

### [Franco] - 6. Desafíos técnicos: Problemas con Git
Más allá de la limpieza de datos, tuvimos un percance con el control de versiones. En un momento mergeamos la rama de un compañero  directo a la rama `main` por accidente, lo que nos desarmó la estructura de ramas individuales que habíamos acordado. Tuvimos que parar, buscar cómo deshacer el lío (tuvimos que hacer un revert del commit del merge) y restaurar `main` a su estado correcto. Nos sirvió de lección para tener más cuidado antes de hacer un merge y mantener las ramas separadas hasta que el código esté 100% chequeado.

### [Franco] - 7. Registro de versiones
- **v1.0:** Cargué el archivo original y borré las columnas constantes (`Z_CostContact` y `Z_Revenue`) que no aportaban nada.
- **v1.1:** Encontré los nulos y rellené casi todos con 0 para no perder filas útiles.
- **v1.2 (02/05 14:15hs):** Rellené los nulos de `Income` con la mediana para esquivar outliers, borré las edades absurdas, acomodé las fechas, armé columnas nuevas estratégicas (Feature Engineering) y exporté el resultado impecable a `customer_behavior_LIMPIO.csv`.
