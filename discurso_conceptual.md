# Resumen Ejecutivo: Modelo de Predicción de Respuesta a Campañas

## 1. El punto de partida: Los Datos
Contábamos con un conjunto de datos (dataset) que registraba el comportamiento de más de 2.200 clientes de una empresa. Esta información incluía:
*   **Datos demográficos:** Año de nacimiento, nivel educativo, estado civil y si tenían hijos/adolescentes en el hogar.
*   **Datos económicos:** Nivel de ingresos de la familia.
*   **Comportamiento de compra:** Cuánto gastaban en distintas categorías (vinos, frutas, carnes, productos premium, etc.), por qué medio compraban (web, catálogo, tienda física) y hace cuántos días habían realizado su última compra.
*   **Interacción con la empresa:** Si habían aceptado campañas publicitarias anteriores, si se habían quejado alguna vez, y —el dato más importante para nosotros— si habían aceptado o no la **última campaña** ofrecida (variable `Response`).

## 2. Lo que hicimos y por qué (Fase ETL y Preparación)
Antes de poder predecir nada, los datos crudos rara vez sirven. Tuvimos que "limpiar la casa":
*   **Llenar los huecos:** Había clientes sin información de ingresos. En lugar de descartarlos o poner un cero (que arruinaría los promedios), les asignamos el valor "mediano" (el valor del medio de todos los ingresos), que es una medida segura y que no se deja engañar por sueldos súper altos. Para otras cosas, como "compras con descuento", si estaba vacío, asumimos lógicamente que era un cero.
*   **Quitar lo que no suma:** Sacamos columnas que tenían el mismo valor para todos los clientes (como costos fijos) porque no ayudan a diferenciar a un cliente de otro. También sacamos a clientes con edades imposibles (nacidos antes de 1930) o ingresos absurdamente altos, porque esos casos atípicos o "outliers" confunden a los algoritmos.
*   **Crear nueva información (Feature Engineering):** Cambiamos el "año de nacimiento" por la "Edad" actual. Parece un cambio menor, pero para un modelo matemático, trabajar con "50 años" es mucho más directo y útil que entender "nació en 1976".

## 3. El Modelo Predictivo
Con los datos limpios, el objetivo de la empresa era claro: **"No queremos gastar plata en enviar campañas a clientes que nos van a decir que no. Queremos saber quién es propenso a decir que sí."**

Elegimos un modelo de **Red Neuronal Artificial**. ¿Por qué? Porque son excelentes encontrando patrones complejos y ocultos cuando tenemos muchas variables mezcladas (como es el comportamiento humano de compra). 

El modelo analizó a la mayoría de los clientes para "aprender" qué tienen en común los que dicen "Sí" y qué tienen en común los que dicen "No". Luego, lo pusimos a prueba con clientes que el modelo nunca había visto para ver si adivinaba su respuesta.

## 4. Conclusiones y Valor para el Negocio
El modelo demostró ser muy útil, con un nivel de acierto global cercano al **89%**. 

Conceptualmente, ¿qué descubrió la red neuronal? Descubrió el **perfil del cliente receptivo**. Las variables que más pesan a la hora de que alguien acepte una campaña son:
1.  **La frescura (Recency):** Cuanto menos tiempo pasó desde su última compra, más enganchados están con la marca.
2.  **Hijos en el hogar:** Curiosamente, los hogares sin niños mostraron mucha mayor predisposición a aceptar las ofertas.
3.  **Edad y consumo Premium:** Clientes mayores, que tienen el hábito de comprar por la página web y que consumen productos de la categoría "Gold/Premium", son blancos ideales.

**En resumen:** En lugar de disparar campañas a ciegas al 100% de la base de datos (donde históricamente sabemos que el 85% la va a rechazar), ahora la empresa puede usar este modelo para filtrar y dirigir su presupuesto de marketing a ese nicho específico (compradores recientes, maduros, sin hijos chicos, de perfil digital y premium). Esto significa menos gasto, mayor tasa de conversión y clientes menos saturados de publicidad irrelevante.
