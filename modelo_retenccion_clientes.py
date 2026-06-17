import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import os
import warnings
warnings.filterwarnings("ignore")

# ============================================================
# MODELO 2 - Predicción de Retención de Clientes
# ¿Cuántos días pasarán hasta que un cliente vuelva a comprar?
# Requiere haber corrido primero el ETL (joaquin.py)
# que genera dataset_limpio.csv con columnas en español
# ============================================================

base_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(base_dir, "dataset_limpio.csv"))
print(f"Dataset cargado: {df.shape}")

# ------------------------------------------------------------
# TARGET
# dias_ultima_compra → cuántos días pasaron desde la última compra
# El modelo aprende a predecir este valor para nuevos clientes
# ------------------------------------------------------------

# ------------------------------------------------------------
# FEATURES - perfil completo del cliente
# ------------------------------------------------------------
features = [
    # Perfil socioeconómico
    "ingreso",
    "edad",

    # Comportamiento de gasto
    "gasto_total",
    "gasto_vinos",
    "gasto_carnes",
    "gasto_frutas",
    "gasto_pescado",
    "gasto_dulces",
    "gasto_premium",

    # Canales de compra
    "compras_web",
    "compras_catalogo",
    "compras_tienda",
    "compras_descuento",
    "total_compras",
    "visitas_web_mensual",

    # Familia
    "ninos_hogar",
    "adolescentes_hogar",

    # Historial con campañas
    "acepto_campania_1",
    "acepto_campania_2",
    "acepto_campania_3",
    "acepto_campania_4",
    "acepto_campania_5",
    "queja"
]

X = df[features].copy()
y = df["dias_ultima_compra"]

# Eliminar filas con nulos residuales
mask = X.notna().all(axis=1) & y.notna()
X, y = X[mask], y[mask]
print(f"Filas para entrenar: {len(X)}")

# ------------------------------------------------------------
# TRAIN / TEST SPLIT
# ------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Train: {len(X_train)} | Test: {len(X_test)}")

# ------------------------------------------------------------
# ENTRENAR MODELOS
# ------------------------------------------------------------
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

# ------------------------------------------------------------
# RESULTADOS
# ------------------------------------------------------------
print("\n" + "="*50)
print("REGRESIÓN LINEAL")
print(f"  MAE (error promedio en días): {mean_absolute_error(y_test, y_pred_lr):.2f}")
print(f"  R²  (ajuste del modelo):      {r2_score(y_test, y_pred_lr):.4f}")

print("\nRANDOM FOREST")
print(f"  MAE (error promedio en días): {mean_absolute_error(y_test, y_pred_rf):.2f}")
print(f"  R²  (ajuste del modelo):      {r2_score(y_test, y_pred_rf):.4f}")
print("="*50)

# ------------------------------------------------------------
# IMPORTANCIA DE VARIABLES
# ------------------------------------------------------------
importancias = pd.Series(rf.feature_importances_, index=features)
importancias = importancias.sort_values(ascending=False)

print("\nVARIABLES MÁS IMPORTANTES para predecir el retorno:")
for var, val in importancias.items():
    barra = "█" * int(val * 50)
    print(f"  {var:<25} {barra} {val*100:.1f}%")

# ------------------------------------------------------------
# SEGMENTACIÓN DE RIESGO
# Clasifica cada cliente según días predichos de retorno
# ------------------------------------------------------------
df_test = X_test.copy()
df_test["dias_reales"]    = y_test.values
df_test["dias_predichos"] = y_pred_rf

def clasificar_riesgo(dias):
    if dias <= 20:
        return "🟢 Volverá pronto"
    elif dias <= 50:
        return "🟡 Riesgo moderado"
    else:
        return "🔴 Riesgo alto de abandono"

df_test["segmento"] = df_test["dias_predichos"].apply(clasificar_riesgo)

print("\nDISTRIBUCIÓN DE SEGMENTOS:")
print(df_test["segmento"].value_counts().to_string())

# ------------------------------------------------------------
# PREDICCIÓN DE EJEMPLO
# ------------------------------------------------------------
print("\n" + "="*50)
print("EJEMPLOS DE PREDICCIÓN:")

clientes = pd.DataFrame([
    {   # Cliente activo, gasta mucho
        "ingreso": 80000, "edad": 42, "gasto_total": 1200,
        "gasto_vinos": 500, "gasto_carnes": 400, "gasto_frutas": 50,
        "gasto_pescado": 100, "gasto_dulces": 80, "gasto_premium": 70,
        "compras_web": 8, "compras_catalogo": 4, "compras_tienda": 6,
        "compras_descuento": 2, "total_compras": 20, "visitas_web_mensual": 3,
        "ninos_hogar": 0, "adolescentes_hogar": 0,
        "acepto_campania_1": 1, "acepto_campania_2": 0,
        "acepto_campania_3": 1, "acepto_campania_4": 0,
        "acepto_campania_5": 1, "queja": 0
    },
    {   # Cliente inactivo, gasta poco
        "ingreso": 25000, "edad": 55, "gasto_total": 80,
        "gasto_vinos": 20, "gasto_carnes": 30, "gasto_frutas": 5,
        "gasto_pescado": 10, "gasto_dulces": 10, "gasto_premium": 5,
        "compras_web": 1, "compras_catalogo": 0, "compras_tienda": 2,
        "compras_descuento": 1, "total_compras": 4, "visitas_web_mensual": 8,
        "ninos_hogar": 2, "adolescentes_hogar": 1,
        "acepto_campania_1": 0, "acepto_campania_2": 0,
        "acepto_campania_3": 0, "acepto_campania_4": 0,
        "acepto_campania_5": 0, "queja": 1
    }
])

predicciones = rf.predict(clientes)
perfiles = ["Cliente activo (gasto alto, sin hijos)", 
            "Cliente inactivo (gasto bajo, con hijos y queja)"]

for perfil, dias in zip(perfiles, predicciones):
    riesgo = clasificar_riesgo(dias)
    print(f"\n  {perfil}")
    print(f"  Días estimados para volver: {dias:.0f} días → {riesgo}")

print("\n" + "="*50)