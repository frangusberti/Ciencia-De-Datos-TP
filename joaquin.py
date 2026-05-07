import pandas as pd
import numpy as np
from datetime import datetime
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(base_dir, "customer_behavior_dataset.csv"))

# ============================================================
# CONVERSIÓN DE COLUMNAS ENTERAS
# ============================================================
columnas_enteras = ["Kidhome", "Teenhome", "AcceptedCmp1", "AcceptedCmp2", 
                    "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5", 
                    "Complain", "Response"]

for col in columnas_enteras:
    df[col] = df[col].fillna(0).astype(int)  # ✅ Encadenado directo, sin inplace

print("Columnas convertidas a entero ✓")
print(df[columnas_enteras].dtypes)

# ============================================================
# PASO 1: EXPLORACIÓN INICIAL
# ============================================================
print("="*50)
print("PASO 1: EXPLORACIÓN INICIAL")
print("="*50)
print(f"Dimensiones: {df.shape}")
print(f"Columnas: {df.columns.tolist()}")
print(f"\nTipos de datos:\n{df.dtypes}")
print(f"\nPrimeras filas:\n{df.head()}")

# ============================================================
# PASO 2: DETECCIÓN DE VALORES NULOS
# ============================================================
print("\n" + "="*50)
print("PASO 2: DETECCIÓN DE VALORES NULOS")
print("="*50)
nulos = df.isnull().sum()
nulos_pct = (df.isnull().sum() / len(df)) * 100
resumen_nulos = pd.DataFrame({
    "Nulos": nulos,
    "Porcentaje": nulos_pct.round(2)
})
print(resumen_nulos[resumen_nulos["Nulos"] > 0])

# ============================================================
# PASO 3: TRATAMIENTO DE NULOS NUMÉRICOS → MEDIA
# ============================================================
print("\n" + "="*50)
print("PASO 3: REEMPLAZAR NULOS NUMÉRICOS CON LA MEDIA")
print("="*50)
columnas_numericas = df.select_dtypes(include=[np.number]).columns
for col in columnas_numericas:
    if df[col].isnull().sum() > 0:
        media = df[col].mean()
        df[col] = df[col].fillna(media)  
        print(f"  '{col}' → nulos reemplazados con media: {media:.2f}")

# ============================================================
# PASO 4: TRATAMIENTO DE NULOS CATEGÓRICOS → MODA
# ============================================================
print("\n" + "="*50)
print("PASO 4: REEMPLAZAR NULOS CATEGÓRICOS CON LA MODA")
print("="*50)
columnas_categoricas = df.select_dtypes(include=["object", "str"]).columns
for col in columnas_categoricas:
    if df[col].isnull().sum() > 0:
        moda = df[col].mode()[0]
        df[col] = df[col].fillna(moda)  
        print(f"  '{col}' → nulos reemplazados con moda: {moda}")

# ============================================================
# PASO 5: DETECCIÓN DE DUPLICADOS
# ============================================================
print("\n" + "="*50)
print("PASO 5: DETECCIÓN Y ELIMINACIÓN DE DUPLICADOS")
print("="*50)
duplicados = df.duplicated().sum()
print(f"Filas duplicadas encontradas: {duplicados}")
df = df.drop_duplicates()
print(f"Filas después de eliminar duplicados: {len(df)}")

# ============================================================
# PASO 6: DETECCIÓN Y TRATAMIENTO DE OUTLIERS
# ============================================================
print("\n" + "="*50)
print("PASO 6: DETECCIÓN Y TRATAMIENTO DE OUTLIERS (IQR)")
print("="*50)

columnas_numericas_actuales = df.select_dtypes(include=[np.number]).columns
resumen_outliers = []

for col in columnas_numericas_actuales:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    limite_inf = Q1 - 1.5 * IQR
    limite_sup = Q3 + 1.5 * IQR

    n_outliers = df[(df[col] < limite_inf) | (df[col] > limite_sup)].shape[0]

    if n_outliers > 0:
        # Capping: reemplaza outliers por los límites (no elimina filas)
        df[col] = df[col].clip(lower=limite_inf, upper=limite_sup)
        resumen_outliers.append({
            "Columna": col,
            "Outliers detectados": n_outliers,
            "Límite inferior": round(limite_inf, 2),
            "Límite superior": round(limite_sup, 2),
            "Tratamiento": "Capping (clip)"
        })

if resumen_outliers:
    resumen_df = pd.DataFrame(resumen_outliers)
    print(resumen_df.to_string(index=False))
else:
    print("No se detectaron outliers en ninguna columna numérica.")

# ============================================================
# PASO 7: TRANSFORMACIÓN DE FECHAS
# ============================================================
print("\n" + "="*50)
print("PASO 7: TRANSFORMACIÓN DE FECHAS")
print("="*50)
df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"], dayfirst=True)
df["anio_cliente"] = df["Dt_Customer"].dt.year
df["mes_cliente"] = df["Dt_Customer"].dt.month
print("Columna 'Dt_Customer' convertida a datetime")
print(f"Rango de fechas: {df['Dt_Customer'].min()} → {df['Dt_Customer'].max()}")

# ============================================================
# PASO 8: CREACIÓN DE NUEVAS VARIABLES
# ============================================================
print("\n" + "="*50)
print("PASO 8: CREACIÓN DE NUEVAS VARIABLES")
print("="*50)
df["edad"] = datetime.now().year - df["Year_Birth"]
df["gasto_total"] = (df["MntWines"] + df["MntFruits"] +
                     df["MntMeatProducts"] + df["MntFishProducts"] +
                     df["MntSweetProducts"] + df["MntGoldProds"])
df["total_compras"] = (df["NumDealsPurchases"] + df["NumWebPurchases"] +
                       df["NumCatalogPurchases"] + df["NumStorePurchases"])
print("Nueva columna 'edad' creada")
print("Nueva columna 'gasto_total' creada")
print("Nueva columna 'total_compras' creada")

# ============================================================
# PASO 9: RENOMBRAR COLUMNAS AL ESPAÑOL
# ============================================================
print("\n" + "="*50)
print("PASO 9: RENOMBRAR COLUMNAS AL ESPAÑOL")
print("="*50)
traduccion = {
    "ID": "id",
    "Year_Birth": "anio_nacimiento",
    "Education": "educacion",
    "Marital_Status": "estado_civil",
    "Income": "ingreso",
    "Kidhome": "ninos_hogar",
    "Teenhome": "adolescentes_hogar",
    "Dt_Customer": "fecha_cliente",
    "Recency": "dias_ultima_compra",
    "MntWines": "gasto_vinos",
    "MntFruits": "gasto_frutas",
    "MntMeatProducts": "gasto_carnes",
    "MntFishProducts": "gasto_pescado",
    "MntSweetProducts": "gasto_dulces",
    "MntGoldProds": "gasto_premium",
    "NumDealsPurchases": "compras_descuento",
    "NumWebPurchases": "compras_web",
    "NumCatalogPurchases": "compras_catalogo",
    "NumStorePurchases": "compras_tienda",
    "NumWebVisitsMonth": "visitas_web_mensual",
    "AcceptedCmp1": "acepto_campania_1",
    "AcceptedCmp2": "acepto_campania_2",
    "AcceptedCmp3": "acepto_campania_3",
    "AcceptedCmp4": "acepto_campania_4",
    "AcceptedCmp5": "acepto_campania_5",
    "Complain": "queja",
    "Z_CostContact": "costo_contacto",
    "Z_Revenue": "ingreso_z",
    "Response": "respuesta_campania"
}
df = df.rename(columns=traduccion)
print("Columnas renombradas al español ✓")

# ============================================================
# PASO 10: EXPORTAR DATASET LIMPIO
# ============================================================
print("\n" + "="*50)
print("PASO 10: EXPORTAR DATASET LIMPIO")
print("="*50)
output_path = os.path.join(base_dir, "dataset_limpio.csv")
df.to_csv(output_path, index=False, encoding="utf-8")
print(f"Dataset exportado a: {output_path}")
print(f"Dimensiones finales: {df.shape}")
print("Veremos que pasa")

# ============================================================
# PASO 11: REPORTE DE CALIDAD DEL DATASET
# ============================================================
print("\n" + "="*50)
print("PASO 11: REPORTE DE CALIDAD FINAL")
print("="*50)

print(f"{'Métrica':<35} {'Valor'}")
print("-" * 50)
print(f"{'Filas totales:':<35} {df.shape[0]}")
print(f"{'Columnas totales:':<35} {df.shape[1]}")
print(f"{'Valores nulos restantes:':<35} {df.isnull().sum().sum()}")
print(f"{'Filas duplicadas restantes:':<35} {df.duplicated().sum()}")
print(f"{'Columnas numéricas:':<35} {len(df.select_dtypes(include=[np.number]).columns)}")
print(f"{'Columnas categóricas:':<35} {len(df.select_dtypes(include=['object','str']).columns)}")
print(f"{'Rango de edad (min-max):':<35} {df['edad'].min()} - {df['edad'].max()}")
print(f"{'Gasto total promedio:':<35} ${df['gasto_total'].mean():.2f}")
print(f"{'Ingreso promedio:':<35} ${df['ingreso'].mean():.2f}")

print("")
print( "DEBEMOS CHEQUEAR Y UNIR NUESTROS CODIGOS PARA EL TP")
