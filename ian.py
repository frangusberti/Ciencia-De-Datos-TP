import os
import pandas as pd
import numpy as np
from datetime import datetime

# Determinar la ruta de la carpeta donde está este script
dir_actual = os.path.dirname(os.path.abspath(__file__))

# Cargar el dataset original
ruta_csv = os.path.join(dir_actual, "customer_behavior_dataset.csv")
df = pd.read_csv(ruta_csv)

# CREAMOS LA COPIA PARA NO ALTERAR EL ORIGINAL
df_copia = df.copy()

print("--- Análisis Inicial ---")
print(f"Dimensiones originales: {df_copia.shape}")

# 1. FORMA DISTINTA DE VER VALORES ÚNICOS Y NULOS
# En lugar de varios prints, creamos un DataFrame resumen que junta todo:
resumen = pd.DataFrame({
    'Tipo de Dato': df_copia.dtypes,
    'Valores Únicos': df_copia.nunique(),
    'Nulos Totales': df_copia.isnull().sum(),
    '% de Nulos': (df_copia.isnull().sum() / len(df_copia)) * 100
})
print("\n--- Resumen de Columnas ---")
print(resumen) 

# 2. FORMA AUTOMATIZADA DE ELIMINAR COLUMNAS CON 1 SOLO VALOR
# En lugar de poner los nombres a mano, busca y elimina columnas que no aportan info.
cols_un_valor = [col for col in df_copia.columns if df_copia[col].nunique() == 1]
print(f"\nEliminando columnas con un solo valor único: {cols_un_valor}")
df_copia = df_copia.drop(columns=cols_un_valor)

# 3. RELLENAR NULOS CON 0 PARA CIERTAS COLUMNAS
columnas_a_cero = [
    'Kidhome', 'MntMeatProducts', 'MntFishProducts', 
    'MntSweetProducts', 'NumDealsPurchases', 
    'AcceptedCmp3', 'AcceptedCmp2', 'Complain', 'Response'
]
columnas_a_cero_existentes = [col for col in columnas_a_cero if col in df_copia.columns]
df_copia[columnas_a_cero_existentes] = df_copia[columnas_a_cero_existentes].fillna(0)

# 4. ALGO ORIGINAL: IMPUTACIÓN INTELIGENTE Y CREACIÓN DE VARIABLES (Feature Engineering)
print("\n--- Aplicando transformaciones originales ---")

# a) Rellenar ingresos con la mediana
if 'Income' in df_copia.columns and df_copia['Income'].isnull().sum() > 0:
    mediana_ingreso = df_copia['Income'].median()
    df_copia['Income'] = df_copia['Income'].fillna(mediana_ingreso)
    print(f"-> Nulos en 'Income' rellenados con la mediana: {mediana_ingreso}")

# b) Crear columna Edad
if 'Year_Birth' in df_copia.columns:
    anio_actual = datetime.now().year
    df_copia['Edad'] = anio_actual - df_copia['Year_Birth']
    print("-> Nueva columna 'Edad' creada a partir de 'Year_Birth'.")

print(f"\nDimensiones finales de la copia: {df_copia.shape}")

# Guardamos la copia en un nuevo archivo CSV para mantener el original intacto
nombre_nuevo_archivo = os.path.join(dir_actual, "customer_behavior_dataset_copia.csv")
df_copia.to_csv(nombre_nuevo_archivo, index=False)
print(f"\n-> ¡Dataset modificado guardado exitosamente en '{nombre_nuevo_archivo}'!")

# 5. TRATAMIENTO DE OUTLIERS
print("\n--- Tratamiento de Outliers ---")
if 'Year_Birth' in df_copia.columns:
    outliers_birth = df_copia[df_copia['Year_Birth'] < 1930].shape[0]
    df_copia = df_copia[df_copia['Year_Birth'] >= 1930]
    print(f"-> Se eliminaron {outliers_birth} registros con 'Year_Birth' < 1930 (posibles errores).")

if 'Income' in df_copia.columns:
    outliers_income = df_copia[df_copia['Income'] > 150000].shape[0]
    df_copia = df_copia[df_copia['Income'] <= 150000]
    print(f"-> Se eliminaron {outliers_income} registros con 'Income' > 150000 (valores extremos).")

print(f"\nDimensiones finales sin outliers: {df_copia.shape}")

# Guardamos el dataset sin outliers
nombre_archivo_final = os.path.join(dir_actual, "customer_behavior_dataset_sin_outliers.csv")
df_copia.to_csv(nombre_archivo_final, index=False)
print(f"\n-> ¡Dataset guardado exitosamente en '{nombre_archivo_final}'!")

# ============================================================================
# 6. MODELO PREDICTIVO - RED NEURONAL (MLPClassifier)
# Objetivo: Predecir la columna 'Response' (si el cliente aceptó la última campaña)
# ============================================================================
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print("\n" + "="*60)
print("   MODELO PREDICTIVO - RED NEURONAL")
print("   Variable objetivo: Response")
print("="*60)

# --- 6.1 Preprocesamiento para el modelo ---
print("\n--- 6.1 Preprocesamiento ---")

# Trabajamos sobre una copia para no alterar df_copia
df_modelo = df_copia.copy()

# a) Eliminar columnas que no aportan al modelo
cols_eliminar = ['ID', 'Dt_Customer', 'Year_Birth']
df_modelo = df_modelo.drop(columns=[c for c in cols_eliminar if c in df_modelo.columns])
print(f"-> Columnas eliminadas del modelo: {cols_eliminar}")

# b) Limpiar valores raros en Marital_Status (Absurd, YOLO, Alone -> Single)
if 'Marital_Status' in df_modelo.columns:
    valores_raros = ['Absurd', 'YOLO', 'Alone']
    n_raros = df_modelo['Marital_Status'].isin(valores_raros).sum()
    df_modelo['Marital_Status'] = df_modelo['Marital_Status'].replace(valores_raros, 'Single')
    print(f"-> {n_raros} registros con Marital_Status raro mapeados a 'Single'")

# c) One-Hot Encoding de variables categóricas
cols_categoricas = ['Education', 'Marital_Status']
cols_categoricas_existentes = [c for c in cols_categoricas if c in df_modelo.columns]
df_modelo = pd.get_dummies(df_modelo, columns=cols_categoricas_existentes, drop_first=True)
print(f"-> One-Hot Encoding aplicado a: {cols_categoricas_existentes}")

# d) Separar features (X) y target (y)
y = df_modelo['Response']
X = df_modelo.drop(columns=['Response'])

print(f"-> Features: {X.shape[1]} columnas")
print(f"-> Target (Response): {len(y)} registros | Clase 0: {(y==0).sum()} | Clase 1: {(y==1).sum()}")

# e) Escalar features (las redes neuronales son sensibles a la escala)
scaler = StandardScaler()
X_escalado = scaler.fit_transform(X)

# --- 6.2 División Train / Test ---
print("\n--- 6.2 División Train/Test ---")
X_train, X_test, y_train, y_test = train_test_split(
    X_escalado, y, test_size=0.2, random_state=42, stratify=y
)
print(f"-> Train: {X_train.shape[0]} registros | Test: {X_test.shape[0]} registros")
print(f"-> Proporción Response=1 en Train: {(y_train==1).sum()}/{len(y_train)} ({(y_train==1).mean()*100:.1f}%)")
print(f"-> Proporción Response=1 en Test:  {(y_test==1).sum()}/{len(y_test)} ({(y_test==1).mean()*100:.1f}%)")

# --- 6.3 Entrenar Red Neuronal ---
print("\n--- 6.3 Entrenamiento de la Red Neuronal ---")
modelo_rn = MLPClassifier(
    hidden_layer_sizes=(64, 32),  # 2 capas ocultas con 64 y 32 neuronas
    activation='relu',             # función de activación estándar
    solver='adam',                 # algoritmo de optimización de pesos
    max_iter=1000,                 # iteraciones máximas
    random_state=42
)
modelo_rn.fit(X_train, y_train)
print(f"-> Modelo entrenado en {modelo_rn.n_iter_} iteraciones")
print(f"-> Arquitectura: entrada({X_train.shape[1]}) -> capa1(64) -> capa2(32) -> salida(2)")

# --- 6.4 Evaluación ---
print("\n--- 6.4 Evaluación del Modelo ---")
y_pred = modelo_rn.predict(X_test)
y_prob = modelo_rn.predict_proba(X_test)

acc = accuracy_score(y_test, y_pred)
print(f"\n   Accuracy: {acc*100:.2f}%")

print("\n   Classification Report:")
print(classification_report(y_test, y_pred, target_names=['No aceptó (0)', 'Aceptó (1)']))

print("   Matriz de Confusión:")
cm = confusion_matrix(y_test, y_pred)
print(f"                    Predicho 0  Predicho 1")
print(f"   Real 0 (no aceptó):  {cm[0][0]:>6}      {cm[0][1]:>6}")
print(f"   Real 1 (aceptó):     {cm[1][0]:>6}      {cm[1][1]:>6}")

# --- 6.5 Feature Importance (pesos de la red) ---
print("\n--- 6.5 Features más influyentes ---")
# Los pesos de la primera capa nos indican qué features tienen más impacto
pesos_primera_capa = np.abs(modelo_rn.coefs_[0]).mean(axis=1)
feature_names = X.columns.tolist()
importancia = pd.DataFrame({
    'Feature': feature_names,
    'Importancia': pesos_primera_capa
}).sort_values('Importancia', ascending=False)

print("\n   Top 10 features con mayor peso en la red neuronal:")
for i, row in importancia.head(10).iterrows():
    print(f"   {importancia.index.get_loc(i)+1:>2}. {row['Feature']:<30} | Peso: {row['Importancia']:.4f}")

# --- 6.6 Exportar resultados ---
print("\n--- 6.6 Exportación de resultados ---")
resultados = pd.DataFrame({
    'Real': y_test.values,
    'Predicho': y_pred,
    'Probabilidad_Clase_1': y_prob[:, 1]
})
ruta_resultados = os.path.join(dir_actual, "resultados_prediccion_response.csv")
resultados.to_csv(ruta_resultados, index=False)
print(f"-> Resultados guardados en '{ruta_resultados}'")

print("\n" + "="*60)
print("   MODELO COMPLETADO")
print("="*60)
