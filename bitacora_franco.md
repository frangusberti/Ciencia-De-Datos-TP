# Bitácora de Trabajo - Proyecto Ciencia de Datos

**Integrantes:** Franco Gusberti
**Dataset:** customer_behavior_dataset.csv
**Fecha de inicio:** 1 de mayo de 2026

---

### [Franco] - 1. Primer contacto con los datos (01/05)
Cargué el dataset usando Pandas para ver con qué me encontraba. El archivo tiene **2240 filas** y **29 columnas**. 

Usé `df.info()` y `df.describe()` para chusmear un poco los números. Vi que hay de todo: años de nacimiento, ingresos, cuántos hijos tienen y cuánto gastaron en cosas como vino o carne.

### [Franco] - 2. Limpieza de columnas "inútiles"
Me puse a ver cuántos valores únicos tiene cada columna y encontré que `Z_CostContact` y `Z_Revenue` tienen siempre el mismo número (3 y 11) para todos los registros. 
**Lo que hice:** Las borré directamente porque no sirven para comparar nada si son todos iguales.

### [Franco] - 3. El lío de los valores nulos
Cuando conté los nulos (`df.isnull().sum()`), saltaron un montón de agujeros, sobre todo en `Kidhome` y `Complain`.

**Mi análisis:**
Llegué a la conclusión de que no son errores, sino que el dato es "cero".
- Si en `Complain` (quejas) no hay nada, es que el cliente nunca se quejó.
- Si en `Kidhome` (hijos) no hay nada, es que no tiene hijos.
- Lo mismo con las campañas de marketing (`AcceptedCmp`).

**Lo que hice:** En lugar de borrar a esos clientes y perder bocha de datos, rellené esos espacios vacíos con el número **0**. Todavía me quedan 24 nulos en `Income` que tengo que ver cómo arreglar (seguramente con la mediana).

### [Franco] - 4. Registro de versiones
- **v1.0:** Cargué el archivo y borré las columnas constantes.
- **v1.1:** Encontré los nulos y rellené casi todos con 0 para no perder filas.
