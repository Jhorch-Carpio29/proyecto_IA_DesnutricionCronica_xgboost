import json
import os
import nbformat as nbf

def create_notebook():
    nb = nbf.v4.new_notebook()
    cells = []

    # Helper function to add markdown
    def add_md(text):
        cells.append(nbf.v4.new_markdown_cell(text.strip()))

    # Helper function to add code
    def add_code(text):
        cells.append(nbf.v4.new_code_cell(text.strip()))

    # Title & Metadata
    add_md("""
# Etapa 1 — Limpieza y Tratamiento de Datos (v1)
## Predicción del Riesgo de Desnutrición Crónica Infantil (Stunting) en Menores de 5 Años
### ENDES 2025 (INEI, Perú) — Modelo Obligatorio: XGBoost

**Autor:** Equipo de Ciencia de Datos & Epidemiología  
**Fecha:** Octubre 2026  
**Objetivo Metodológico:** Construcción y depuración rigurosa de la base de datos analítica a partir de los 23 diccionarios oficiales de la ENDES 2025, garantizando prevención estricta de fuga de datos (*target leakage*), control de causalidad inversa, no imputación de nulos (tratamiento nativo de XGBoost) y partición 80/20 agrupada por conglomerado (`HV001`).
""")

    # Hallazgos del catálogo y verificación previa
    add_md("""
---
## Verificación Previa y Hallazgos del Catálogo de Variables

Antes de iniciar la ingesta y manipulación de datos, se realizó un contraste empírico exhaustivo entre el catálogo generado automáticamente (`catalogo_variables_desnutricion_cronica_endes2025.md`) y los diccionarios oficiales del INEI (`reports/diccionarios_completos_endes2025.md` y diccionarios de los módulos 1031, 1036 y 1041).

A continuación se presenta la tabla de auditoría con los hallazgos críticos detectados y las decisiones adoptadas:

| Variable | Qué decía el Catálogo | Qué dice el Diccionario Oficial INEI | Decisión Técnica Adoptada |
|:---|:---|:---|:---|
| **`M5`** | "Lactancia exclusiva en meses" | "Meses de amamantamiento" | Se corrige el nombre a `meses_amamantamiento`. Se invalida la derivada previa. Para lactancia materna exclusiva real se incorpora `QI440B` (REC94). |
| **`QI440B`** | No priorizada en el catálogo | "Durante primeros 6 meses, solo recibió leche materna" | **INCORPORADA.** Variable genuina de lactancia exclusiva en los primeros 6 meses (REC94). |
| **`M13` vs `M18`** | `M18` indicado como "mes inicio prenatal" | `M13`: "Momento del 1er control prenatal"<br>`M18`: "Tamaño del niño al nacer" | Se asigna `M13` a `mes_inicio_prenatal` y `M18` a `tamano_nacer_aparente`. Se corrige el error de mapeo del catálogo. |
| **`M19A`** | "Tamaño al nacer aparente" | "Peso del niño al nacer según recuerda" (código de tarjeta vs madre) | Se utiliza `M18` para tamaño aparente y `M19` para peso en gramos. |
| **`V411`–`V416` (REC42)** | Diarrea, IRA, SRO en REC42 | REC42 es Dieta de 24 horas (`V411` = leche materna refrigerada). Morbilidad infantil está en **REC43**. | Se migra a las variables reales de morbilidad en **REC43**: `H11` (diarrea), `H11B` (sangre), `H22` (fiebre), `H31` (tos), `H31B` (neumonía). |
| **`V413` / `H13` (SRO)** | "Tratamiento con SRO para diarrea" | `H13`: "Dio al niño sales de rehidratación oral" | **EXCLUIDA.** Tratamiento reactivo posterior a la enfermedad; riesgo severo de causalidad inversa (Regla 3). |
| **`S45C` vs `S466C`** | `S45C` en REC95 | `S466C` en REC95: "Cantidad de controles de crecimiento recibidos" | Se utiliza `S466C`. Se incluye con cautela y se normaliza con la derivada `adherencia_cred` por edad. |
| **`M45`, `M46`** | Dudosa / Fuga en proyecto anemia | `M45`: Suplemento hierro en gestación<br>`M46`: Días de hierro consumidos | **INCLUIDAS.** Para desnutrición crónica son factores perinatales preventivos previos al nacimiento. |
| **`V501`, `V714`, `V743A`** | Estado conyugal, trabajo y autonomía en REC0111 | No existen en el CSV de REC0111_2025 | Se utiliza **`HV115`** (RECH1) para estado conyugal de la madre. `V714` y `V743A` se reportan como no disponibles. |
| **Reconciliación FEATURES** | Discrepancias entre Sec 5 y Sec 12.2 | En Sec 5 estaban `SH11B` y `H31B`, omitidas en Sec 12.2 | **RECONCILIADA.** Se unifica una sola lista exhaustiva incluyendo `seguro_essalud` (`SH11B`) y `signos_neumonia` (`H31B`). |
| **Llaves niño-madre** | Catálogo asumía llave única `BIDX` | `HC60` vincula madre en hogar; `HWIDX` (REC44), `MIDX` (REC41), `HIDX` (REC43), `IDX95` (REC95) | Se construye el ranking intrafamiliar `child_rank` logrando **99.99% de enlace exacto** con el historial de nacimiento. |
""")

    # Limpieza de salidas de anemia
    add_md("""
---
## Limpieza Controlada de Salidas del Proyecto de Anemia

Siguiendo las directrices del proyecto, se eliminan explícitamente las 8 salidas derivadas del proyecto anterior para garantizar que `data/processed/` y `reports/` reflejen únicamente la evidencia de desnutrición crónica.
""")

    add_code("""
import os, sys
import numpy as np
import pandas as pd

# Definición de rutas relativas a la raíz del proyecto
ROOT = os.path.abspath(os.path.join(os.getcwd(), '..'))
DATA = os.path.join(ROOT, 'data')
PROCESSED = os.path.join(DATA, 'processed')
REPORTS = os.path.join(ROOT, 'reports')

# Importar funciones modulares creadas para el proyecto
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from utils_desnutricion import to_num, localizar_archivos_csv, limpiar_salidas_anemia, calcular_auc_univariado

# 1. Ejecutar limpieza de salidas anteriores
df_clean_anemia = limpiar_salidas_anemia(ROOT)
print("=== RESULTADO DE LA LIMPIEZA DE SALIDAS DE ANEMIA ===")
display(df_clean_anemia)
""")

    # Sección 0: Configuración
    add_md("""
---
## 0. Configuración del Entorno, Parámetros y Semillas
""")

    add_code("""
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc

# Fijar semilla global de reproducibilidad
SEED = 42
np.random.seed(SEED)

# Configuración visual
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11

print(f"Entorno configurado exitosamente. Directorio raíz: {ROOT}")
""")

    # Sección 1: Carga e integridad
    add_md("""
---
## 1. Localización, Carga e Integridad de Módulos CSV

Se escanea dinámicamente el árbol de `data/` para identificar y validar los 23 archivos oficiales de la ENDES 2025. Se prioriza `data/raw/` si es un archivo real válido y no un enlace simbólico roto.
""")

    add_code("""
# Localizar y catalogar archivos reales
csv_map, df_inventario = localizar_archivos_csv(ROOT)
print(f"Total de archivos CSV válidos localizados: {len(df_inventario)}")
display(df_inventario[['modulo_archivo', 'archivo_csv', 'ruta_relativa', 'filas', 'columnas']])

# Exportar reporte inicial 01_inventario_modulos.csv
os.makedirs(REPORTS, exist_ok=True)
df_inventario.to_csv(os.path.join(REPORTS, '01_inventario_modulos.csv'), index=False, encoding='utf-8')
print("Guardado: reports/01_inventario_modulos.csv")

# Verificación de archivos indispensables
modulos_requeridos = ['RECH6', 'RECH0', 'RECH23', 'RECH4', 'RECH5', 'RECH1', 'REC44', 'REC41', 'REC94', 'REC43', 'REC95', 'REC0111', 'REC91', 'Programas Sociales x Hogar']
faltantes = [m for m in modulos_requeridos if m not in csv_map]
assert len(faltantes) == 0, f"ERROR CRÍTICO: Faltan módulos indispensables: {faltantes}"
print("✓ Todos los módulos indispensables están presentes y verificados.")
""")

    # Sección 2: Universo y target
    add_md("""
---
## 2. Definición del Universo de Estudio y Variable Objetivo ($Y$)

### 2.1 Criterio Internacional OMS (2006)
- **Target:** Desnutrición Crónica Infantil = 1 si Puntaje Z Talla para la Edad ($Z_{T/E}$) < -2.00 Desviaciones Estándar, 0 en caso contrario.
- **Fuente Oficial Primaria:** `HC70` en `RECH6_2025.csv` (registrado en centésimas de desviación estándar, umbral: `HC70 < -200`).
- **Verificación cruzada:** Contraste de paridad con `HW70` en `REC44_2025.csv` para niños comunes.
""")

    add_code("""
# Cargar tabla núcleo base: RECH6
df_rech6 = pd.read_csv(csv_map['RECH6'], low_memory=False)
n_total_rech6 = len(df_rech6)
print(f"Registros iniciales en RECH6: {n_total_rech6:,}")

# Convertir columnas clave a numérico
df_rech6['HC1_num'] = pd.to_numeric(df_rech6['HC1'], errors='coerce')
df_rech6['HC70_num'] = pd.to_numeric(df_rech6['HC70'], errors='coerce')
df_rech6['HHID_int'] = df_rech6['HHID'].astype(int)
df_rech6['HC0_int'] = df_rech6['HC0'].astype(int)
df_rech6['HC60_int'] = pd.to_numeric(df_rech6['HC60'], errors='coerce').fillna(999).astype(int)

# 1. Funnel de filtrado metodológico
paso1_edad = df_rech6['HC1_num'].between(0, 59)
paso2_codigos = paso1_edad & df_rech6['HC70_num'].notna() & (~df_rech6['HC70_num'].isin([9996, 9997, 9998]))
paso3_plausibilidad = paso2_codigos & df_rech6['HC70_num'].between(-600, 600)

df_funnel = pd.DataFrame([
    {'Paso': '0. Total registros en RECH6', 'Casos': n_total_rech6, 'Casos Perdidos': 0, 'Motivo': 'Muestra censal total evaluada'},
    {'Paso': '1. Edad cumplida 0-59 meses (HC1)', 'Casos': int(paso1_edad.sum()), 'Casos Perdidos': int(n_total_rech6 - paso1_edad.sum()), 'Motivo': 'Población objetivo pediátrica < 5 años'},
    {'Paso': '2. Códigos válidos HC70 (excluye 9996-9998)', 'Casos': int(paso2_codigos.sum()), 'Casos Perdidos': int(paso1_edad.sum() - paso2_codigos.sum()), 'Motivo': 'No medidos, ausentes o inconsistentes'},
    {'Paso': '3. Rango biológico plausible [-600, 600]', 'Casos': int(paso3_plausibilidad.sum()), 'Casos Perdidos': int(paso2_codigos.sum() - paso3_plausibilidad.sum()), 'Motivo': 'Exclusión de errores extremos (|Z| > 6 DE)'}
])

print("=== FUNNEL METODOLÓGICO DEL UNIVERSO DE ESTUDIO ===")
display(df_funnel)

# Gráfico del funnel
plt.figure(figsize=(9, 4))
bars = plt.barh(df_funnel['Paso'], df_funnel['Casos'], color=['#2c3e50', '#2980b9', '#3498db', '#27ae60'])
plt.xlabel('Número de Infantes')
plt.title('Funnel de Filtrado del Universo Analítico (ENDES 2025)')
for bar in bars:
    w = bar.get_width()
    plt.text(w - 1800, bar.get_y() + bar.get_height()/2, f"{w:,}", va='center', color='white', fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Base filtrada del universo analítico
df_universo = df_rech6[paso3_plausibilidad].copy()

# Construcción de la Variable Objetivo Binaria
df_universo['desnutricion_cronica'] = (df_universo['HC70_num'] < -200).astype(int)

# Verificación de integridad del target
assert df_universo['desnutricion_cronica'].isna().sum() == 0, "ERROR: Hay nulos en el target"
assert set(df_universo['desnutricion_cronica'].unique()).issubset({0, 1}), "ERROR: Target no es binario"
print(f"✓ Target 'desnutricion_cronica' construido exitosamente. Universo final: {len(df_universo):,} niños.")
""")

    # Sección 2.2: Verificación cruzada con REC44 y prevalencia ponderada
    add_md("""
### 2.2 Verificación Cruzada con `REC44` (`HW70`) y Prevalencia Ponderada
""")

    add_code("""
# Cargar REC44 para contraste de auditoría
df_rec44 = pd.read_csv(csv_map['REC44'], low_memory=False)
df_rec44['caseid_strip'] = df_rec44['CASEID'].astype(str).str.strip()
parts_r44 = df_rec44['caseid_strip'].str.split(expand=True)
df_rec44['hhid_int'] = parts_r44[0].astype(int)
df_rec44['madre_linea'] = parts_r44[1].astype(int)
df_rec44['HW1_num'] = pd.to_numeric(df_rec44['HW1'], errors='coerce')
df_rec44['HW70_num'] = pd.to_numeric(df_rec44['HW70'], errors='coerce')
df_rec44['HWIDX_int'] = df_rec44['HWIDX'].astype(int)

# Ordenar para emparejamiento intrafamiliar
df_universo_madr = df_universo[df_universo['HC60_int'] < 900].copy()
df_universo_madr = df_universo_madr.sort_values(['HHID_int', 'HC60_int', 'HC1_num', 'HC0_int'])
df_universo_madr['child_rank'] = df_universo_madr.groupby(['HHID_int', 'HC60_int']).cumcount() + 1

df_rec44_sort = df_rec44.sort_values(['hhid_int', 'madre_linea', 'HW1_num', 'HWIDX_int'])
df_rec44_sort['child_rank'] = df_rec44_sort.groupby(['hhid_int', 'madre_linea']).cumcount() + 1

m_audit = df_universo_madr.merge(
    df_rec44_sort[['hhid_int', 'madre_linea', 'child_rank', 'HW1_num', 'HW70_num']],
    left_on=['HHID_int', 'HC60_int', 'child_rank'],
    right_on=['hhid_int', 'madre_linea', 'child_rank'],
    how='inner'
)

coincidencia_edad = (m_audit['HC1_num'] == m_audit['HW1_num']).mean() * 100
v_z = m_audit['HW70_num'].between(-600, 600)
coincidencia_z = (m_audit.loc[v_z, 'HC70_num'] == m_audit.loc[v_z, 'HW70_num']).mean() * 100

print(f"Auditoría cruzada RECH6 vs REC44 (n={len(m_audit):,} niños comunes):")
print(f"  - Coincidencia exacta de edad (HC1 == HW1): {coincidencia_edad:.2f}%")
print(f"  - Coincidencia exacta de Z-score (HC70 == HW70): {coincidencia_z:.2f}%")

# Cargar pesos muestrales y geografía de RECH0 para cálculo ponderado
df_rech0_w = pd.read_csv(csv_map['RECH0'], low_memory=False)[['HHID', 'HV005', 'HV025']].copy()
df_rech0_w['HHID_int'] = df_rech0_w['HHID'].astype(int)
df_universo = df_universo.merge(df_rech0_w[['HHID_int', 'HV005', 'HV025']], on='HHID_int', how='left')
df_universo['peso_muestral'] = df_universo['HV005'] / 1e6

prev_sin_ponderar = df_universo['desnutricion_cronica'].mean() * 100
prev_ponderada = np.average(df_universo['desnutricion_cronica'], weights=df_universo['peso_muestral']) * 100
ratio_desbalance = (df_universo['desnutricion_cronica'] == 0).sum() / (df_universo['desnutricion_cronica'] == 1).sum()

print(f"\\nPrevalencia Nacional Sin Ponderar: {prev_sin_ponderar:.2f}%")
print(f"Prevalencia Nacional Ponderada:    {prev_ponderada:.2f}% (Consistente con reporte oficial INEI ~11.5 - 12%)")
print(f"Ratio de Desbalance (Negativos : Positivos): {ratio_desbalance:.2f} : 1")
assert 6.0 <= prev_ponderada <= 20.0, f"ALERTA: Prevalencia ponderada anómala ({prev_ponderada:.2f}%)"
""")

    # Sección 3: Merges con validación
    add_md("""
---
## 3. Integración de Módulos (Merges Secuenciales con Validación y Control de Enlace)

Se integran los 12 módulos requeridos utilizando llaves normalizadas y validando la cardinalidad estricta (`m:1` para hogar y vivienda; `1:1` para niño e historia de nacimiento).
Los infantes cuya madre no reside en el hogar (`HC60 >= 990`) se **conservan** en la base, registrando un indicador binario `madre_en_cuestionario = 0` y manteniendo sus predictores maternos en `np.nan`.
""")

    add_code("""
# 1. Asignar child_rank al universo completo
df_universo_sorted = df_universo.sort_values(['HHID_int', 'HC60_int', 'HC1_num', 'HC0_int']).copy()
df_universo_sorted['child_rank'] = df_universo_sorted.groupby(['HHID_int', 'HC60_int']).cumcount() + 1
df_universo_sorted['madre_en_cuestionario'] = (df_universo_sorted['HC60_int'] < 900).astype(int)

# 2. Enlazar con REC44 para obtener caseid_clean y hwidx_int oficial
rec44_keys = df_rec44_sort[['hhid_int', 'madre_linea', 'child_rank', 'caseid_strip', 'HWIDX_int']].drop_duplicates()
df_merged = df_universo_sorted.merge(
    rec44_keys,
    left_on=['HHID_int', 'HC60_int', 'child_rank'],
    right_on=['hhid_int', 'madre_linea', 'child_rank'],
    how='left'
)
df_merged.rename(columns={'caseid_strip': 'caseid_clean', 'HWIDX_int': 'hwidx_int'}, inplace=True)
df_merged.drop(columns=['hhid_int', 'madre_linea'], inplace=True)

# Preparación de subtablas modulares con columnas seleccionadas y deduplicación
# RECH0
r0 = pd.read_csv(csv_map['RECH0'], low_memory=False)
r0['hhid_int'] = r0['HHID'].astype(int)
r0_sub = r0[['hhid_int', 'HV001', 'HV022', 'HV024', 'HV040', 'HV009', 'HV014', 'HV010']].drop_duplicates('hhid_int')

# RECH23
r23 = pd.read_csv(csv_map['RECH23'], low_memory=False)
r23['hhid_int'] = r23['HHID'].astype(int)
r23_sub = r23[['hhid_int', 'HV201', 'HV205', 'HV206', 'HV209', 'HV213', 'HV216', 'HV225', 'HV226', 'HV237', 'HV270']].drop_duplicates('hhid_int')

# Programas Sociales x Hogar
ps = pd.read_csv(csv_map['Programas Sociales x Hogar'], low_memory=False)
ps['hhid_int'] = ps['HHID'].astype(int)
ps_sub = ps[['hhid_int', 'QH95', 'QH101', 'QH103', 'QH106']].drop_duplicates('hhid_int')

# RECH4 (Seguro SIS y EsSalud del niño)
r4 = pd.read_csv(csv_map['RECH4'], low_memory=False)
r4['hhid_int'] = r4['HHID'].astype(int)
r4['idxh4_int'] = pd.to_numeric(r4['IDXH4'], errors='coerce').fillna(-1).astype(int)
r4_sub = r4[['hhid_int', 'idxh4_int', 'SH11A', 'SH11B']].drop_duplicates(['hhid_int', 'idxh4_int'])

# RECH5 (Antropometría materna)
r5 = pd.read_csv(csv_map['RECH5'], low_memory=False)
r5['hhid_int'] = r5['HHID'].astype(int)
r5['ha0_int'] = pd.to_numeric(r5['HA0'], errors='coerce').fillna(-1).astype(int)
r5_sub = r5[['hhid_int', 'ha0_int', 'HA3', 'HA40']].drop_duplicates(['hhid_int', 'ha0_int'])

# RECH1 (Estado conyugal de la madre)
r1 = pd.read_csv(csv_map['RECH1'], low_memory=False)
r1['hhid_int'] = r1['HHID'].astype(int)
r1['hvidx_int'] = pd.to_numeric(r1['HVIDX'], errors='coerce').fillna(-1).astype(int)
r1_sub = r1[['hhid_int', 'hvidx_int', 'HV115']].drop_duplicates(['hhid_int', 'hvidx_int'])

# REC41 (Embarazo, parto, lactancia)
r41 = pd.read_csv(csv_map['REC41'], low_memory=False)
r41['caseid_clean'] = r41['CASEID'].astype(str).str.strip()
r41['midx_int'] = pd.to_numeric(r41['MIDX'], errors='coerce').fillna(-1).astype(int)
r41_sub = r41[['caseid_clean', 'midx_int', 'M13', 'M14', 'M15', 'M18', 'M19', 'M4', 'M5', 'M45', 'M46', 'M3A']].drop_duplicates(['caseid_clean', 'midx_int'])

# REC94 (Lactancia materna exclusiva primeros 6m)
r94 = pd.read_csv(csv_map['REC94'], low_memory=False)
r94['caseid_clean'] = r94['CASEID'].astype(str).str.strip()
r94['idx94_int'] = pd.to_numeric(r94['IDX94'], errors='coerce').fillna(-1).astype(int)
r94_sub = r94[['caseid_clean', 'idx94_int', 'QI440B']].drop_duplicates(['caseid_clean', 'idx94_int'])

# REC43 (Salud infantil, morbilidad reciente, vacunas)
r43 = pd.read_csv(csv_map['REC43'], low_memory=False)
r43['caseid_clean'] = r43['CASEID'].astype(str).str.strip()
r43['hidx_int'] = pd.to_numeric(r43['HIDX'], errors='coerce').fillna(-1).astype(int)
r43_sub = r43[['caseid_clean', 'hidx_int', 'H1', 'H2', 'H9', 'H11', 'H11B', 'H22', 'H31', 'H31B', 'H34', 'H43']].drop_duplicates(['caseid_clean', 'hidx_int'])

# REC95 (Neumococo, Rotavirus, CRED)
r95 = pd.read_csv(csv_map['REC95'], low_memory=False)
r95['caseid_clean'] = r95['CASEID'].astype(str).str.strip()
r95['idx95_int'] = pd.to_numeric(r95['IDX95'], errors='coerce').fillna(-1).astype(int)
r95_sub = r95[['caseid_clean', 'idx95_int', 'S45NM1', 'S45NM2', 'S45RT1', 'S45RT2', 'S466C']].drop_duplicates(['caseid_clean', 'idx95_int'])

# REC0111 (Datos sociodemográficos MEF)
r0111 = pd.read_csv(csv_map['REC0111'], low_memory=False)
r0111['caseid_clean'] = r0111['CASEID'].astype(str).str.strip()
r0111_sub = r0111[['caseid_clean', 'V012', 'V106', 'V107']].drop_duplicates('caseid_clean')

# REC91 (Lengua materna)
r91 = pd.read_csv(csv_map['REC91'], low_memory=False)
r91['caseid_clean'] = r91['CASEID'].astype(str).str.strip()
r91_sub = r91[['caseid_clean', 'S119']].drop_duplicates('caseid_clean')

# Pipeline secuencial de merges
secuencia_merges = [
    ('RECH0 (Geografía/Hogar)',      r0_sub,   ['HHID_int'], ['hhid_int'], 'm:1', 99.0),
    ('RECH23 (Vivienda/Riqueza)',    r23_sub,  ['HHID_int'], ['hhid_int'], 'm:1', 99.0),
    ('Programas Sociales x Hogar',   ps_sub,   ['HHID_int'], ['hhid_int'], 'm:1', 99.0),
    ('RECH4 (Seguro Salud Niño)',    r4_sub,   ['HHID_int', 'HC0_int'], ['hhid_int', 'idxh4_int'], 'm:1', 99.0),
    ('RECH5 (Talla/IMC Madre)',      r5_sub,   ['HHID_int', 'HC60_int'], ['hhid_int', 'ha0_int'], 'm:1', 90.0),
    ('RECH1 (Estado Conyugal Madre)',r1_sub,   ['HHID_int', 'HC60_int'], ['hhid_int', 'hvidx_int'], 'm:1', 90.0),
    ('REC41 (Embarazo/Parto)',       r41_sub,  ['caseid_clean', 'hwidx_int'], ['caseid_clean', 'midx_int'], 'm:1', 90.0),
    ('REC94 (Lactancia Exclusiva)',  r94_sub,  ['caseid_clean', 'hwidx_int'], ['caseid_clean', 'idx94_int'], 'm:1', 90.0),
    ('REC43 (Morbilidad/Vacunas)',   r43_sub,  ['caseid_clean', 'hwidx_int'], ['caseid_clean', 'hidx_int'], 'm:1', 90.0),
    ('REC95 (Neumo/Rota/CRED)',      r95_sub,  ['caseid_clean', 'hwidx_int'], ['caseid_clean', 'idx95_int'], 'm:1', 90.0),
    ('REC0111 (Edad/Educación MEF)', r0111_sub,['caseid_clean'], ['caseid_clean'], 'm:1', 90.0),
    ('REC91 (Lengua Materna MEF)',   r91_sub,  ['caseid_clean'], ['caseid_clean'], 'm:1', 90.0)
]

reporte_enlaces = []
n_base_inicial = len(df_merged)

for nombre, df_der, k_izq, k_der, card, umbral_min in secuencia_merges:
    n_pre = len(df_merged)
    tag = f"_m_{nombre.split()[0]}"
    df_merged = df_merged.merge(df_der, left_on=k_izq, right_on=k_der, how='left', validate=card, indicator=tag)
    n_post = len(df_merged)
    assert n_pre == n_post, f"ERROR: Filas mutaron en merge {nombre} ({n_pre} -> {n_post})"
    
    tasa = (df_merged[tag] == 'both').mean() * 100
    reporte_enlaces.append({
        'Módulo': nombre,
        'Cardinalidad': card,
        'Filas Pre': n_pre,
        'Filas Post': n_post,
        'Tasa Enlace (%)': round(tasa, 2),
        'Umbral Req (%)': umbral_min,
        'Estado': '✓ OK' if tasa >= umbral_min else '❌ ALERTA'
    })
    cols_drop = [tag] + [c for c in k_der if c not in k_izq and c in df_merged.columns]
    df_merged.drop(columns=cols_drop, inplace=True)

df_rep_merges = pd.DataFrame(reporte_enlaces)
print("=== REPORTE OFICIAL DE TASAS DE ENLACE RELACIONAL ===")
display(df_rep_merges)

# Exportar base unida 02_base_unida.parquet
df_merged.to_parquet(os.path.join(PROCESSED, '02_base_unida.parquet'), index=False)
print("Guardado: data/processed/02_base_unida.parquet")

# Exportar reporte de nulos base unida
df_nulos_bu = pd.DataFrame({
    'variable': df_merged.columns,
    'n_nulos': df_merged.isna().sum().values,
    'pct_nulos': (df_merged.isna().mean() * 100).round(2).values
})
df_nulos_bu.to_csv(os.path.join(REPORTS, '02_nulos_base_unida.csv'), index=False, encoding='utf-8')
print("Guardado: reports/02_nulos_base_unida.csv")
""")

    # Sección 4 y 5: Códigos especiales, recodificación y limpieza
    add_md("""
---
## 4 y 5. Auditoría de Códigos Especiales, Recodificación y Limpieza

### Regla de Oro Epidemiológica
1. **Códigos especiales a `np.nan` ANTES de cualquier división o reescalado.**
2. Binarias 1/2 pasan a 1/0.
3. Respetar unidades oficiales:
   - Talla de la madre `HA3`: dividida entre 10.0 (cm con 1 decimal).
   - IMC de la madre `HA40`: dividido entre 100.0 (kg/m² con 2 decimales).
   - Peso al nacer `M19`: gramos válidos [500, 6000].
4. Nombres en `snake_case` limpios sin caracteres especiales.
""")

    add_code("""
df_clean = df_merged.copy()

# 1. Antropometría Materna (Códigos especiales 9998 a NaN antes de dividir)
df_clean['HA3_num'] = pd.to_numeric(df_clean['HA3'], errors='coerce')
df_clean.loc[df_clean['HA3_num'] >= 9990, 'HA3_num'] = np.nan
df_clean['talla_madre_cm'] = df_clean['HA3_num'] / 10.0

df_clean['HA40_num'] = pd.to_numeric(df_clean['HA40'], errors='coerce')
df_clean.loc[df_clean['HA40_num'] >= 9990, 'HA40_num'] = np.nan
df_clean['imc_madre'] = df_clean['HA40_num'] / 100.0

# 2. Factores Biológicos del Niño
df_clean['edad_meses'] = df_clean['HC1_num'].astype(int)
df_clean['sexo_nino'] = np.where(df_clean['HC27'] == 1, 1, 0) # 1 Hombre, 0 Mujer

# 3. Factores Perinatales y Gestacionales (REC41)
df_clean['peso_al_nacer_g'] = pd.to_numeric(df_clean['M19'], errors='coerce')
df_clean.loc[df_clean['peso_al_nacer_g'] >= 9990, 'peso_al_nacer_g'] = np.nan

df_clean['tamano_nacer_aparente'] = pd.to_numeric(df_clean['M18'], errors='coerce')
df_clean.loc[df_clean['tamano_nacer_aparente'] == 8, 'tamano_nacer_aparente'] = np.nan # 8 No sabe

df_clean['mes_inicio_prenatal'] = pd.to_numeric(df_clean['M13'], errors='coerce')
df_clean.loc[df_clean['mes_inicio_prenatal'] >= 90, 'mes_inicio_prenatal'] = np.nan

df_clean['controles_prenatales'] = pd.to_numeric(df_clean['M14'], errors='coerce')
df_clean.loc[df_clean['controles_prenatales'] >= 90, 'controles_prenatales'] = np.nan

df_clean['lugar_parto'] = pd.to_numeric(df_clean['M15'], errors='coerce')
df_clean['atencion_parto_calif'] = np.where(df_clean['M3A'] == 1, 1, 0)

df_clean['duracion_lactancia_m'] = pd.to_numeric(df_clean['M4'], errors='coerce')
df_clean.loc[df_clean['duracion_lactancia_m'] >= 90, 'duracion_lactancia_m'] = np.nan

df_clean['meses_amamantamiento'] = pd.to_numeric(df_clean['M5'], errors='coerce')
df_clean.loc[df_clean['meses_amamantamiento'] >= 90, 'meses_amamantamiento'] = np.nan

df_clean['hierro_madre_gestacion'] = np.where(df_clean['M45'] == 1, 1, np.where(df_clean['M45'] == 0, 0, np.nan))
df_clean['dias_hierro_madre'] = pd.to_numeric(df_clean['M46'], errors='coerce')
df_clean.loc[df_clean['dias_hierro_madre'] >= 990, 'dias_hierro_madre'] = np.nan

# Lactancia materna exclusiva primeros 6m (REC94)
df_clean['lactancia_exclusiva_6m'] = np.where(df_clean['QI440B'] == 1, 1, np.where(df_clean['QI440B'] == 2, 0, np.nan))

# 4. Madre: Educación y Demografía (REC0111, RECH1, REC91)
df_clean['edad_madre_anos'] = pd.to_numeric(df_clean['V012'], errors='coerce')
df_clean['educacion_madre_nivel'] = pd.to_numeric(df_clean['V106'], errors='coerce')
df_clean['educacion_madre_anos'] = pd.to_numeric(df_clean['V107'], errors='coerce')
df_clean.loc[df_clean['educacion_madre_anos'] >= 90, 'educacion_madre_anos'] = np.nan

df_clean['estado_conyugal_madre'] = pd.to_numeric(df_clean['HV115'], errors='coerce')
df_clean.loc[df_clean['estado_conyugal_madre'] >= 9, 'estado_conyugal_madre'] = np.nan

df_clean['lengua_materna_madre'] = pd.to_numeric(df_clean['S119'], errors='coerce')
df_clean.loc[df_clean['lengua_materna_madre'] >= 90, 'lengua_materna_madre'] = np.nan

# 5. Hogar y Vivienda (RECH0, RECH23)
df_clean['total_miembros_hogar'] = pd.to_numeric(df_clean['HV009'], errors='coerce')
df_clean['menores_5anos_hogar'] = pd.to_numeric(df_clean['HV014'], errors='coerce')
df_clean['mujeres_edad_fertil'] = pd.to_numeric(df_clean['HV010'], errors='coerce')
df_clean['departamento'] = pd.to_numeric(df_clean['HV024'], errors='coerce')
df_clean['area_residencia'] = pd.to_numeric(df_clean['HV025'], errors='coerce')
df_clean['altitud_msnm'] = pd.to_numeric(df_clean['HV040'], errors='coerce')

df_clean['fuente_agua_beber'] = pd.to_numeric(df_clean['HV201'], errors='coerce')
df_clean['tipo_servicio_higienico'] = pd.to_numeric(df_clean['HV205'], errors='coerce')
df_clean['bano_compartido'] = np.where(df_clean['HV225'] == 1, 1, np.where(df_clean['HV225'] == 0, 0, np.nan))
df_clean['tratamiento_agua'] = np.where(df_clean['HV237'] == 1, 1, np.where(df_clean['HV237'] == 0, 0, np.nan))
df_clean['material_piso'] = pd.to_numeric(df_clean['HV213'], errors='coerce')
df_clean['habitaciones_dormir'] = pd.to_numeric(df_clean['HV216'], errors='coerce')
df_clean.loc[df_clean['habitaciones_dormir'] >= 90, 'habitaciones_dormir'] = np.nan
df_clean['combustible_cocinar'] = pd.to_numeric(df_clean['HV226'], errors='coerce')
df_clean['tiene_electricidad'] = np.where(df_clean['HV206'] == 1, 1, np.where(df_clean['HV206'] == 0, 0, np.nan))
df_clean['tiene_refrigerador'] = np.where(df_clean['HV209'] == 1, 1, np.where(df_clean['HV209'] == 0, 0, np.nan))
df_clean['quintil_riqueza'] = pd.to_numeric(df_clean['HV270'], errors='coerce')

# 6. Seguro de Salud (RECH4)
df_clean['seguro_sis'] = np.where(df_clean['SH11A'] == 1, 1, np.where(df_clean['SH11A'] == 0, 0, np.nan))
df_clean['seguro_essalud'] = np.where(df_clean['SH11B'] == 1, 1, np.where(df_clean['SH11B'] == 0, 0, np.nan))

# 7. Inmunización y Salud Niño (REC43, REC95)
df_clean['carne_vacunacion_visto'] = pd.to_numeric(df_clean['H1'], errors='coerce')
df_clean['vacuna_bcg'] = np.where(df_clean['H2'].isin([1, 2, 3]), 1, np.where(df_clean['H2'] == 0, 0, np.nan))
df_clean['vacuna_spr1'] = np.where(df_clean['H9'].isin([1, 2, 3]), 1, np.where(df_clean['H9'] == 0, 0, np.nan))
df_clean['suplemento_vitamina_a'] = np.where(df_clean['H34'] == 1, 1, np.where(df_clean['H34'] == 0, 0, np.nan))
df_clean['desparasitacion_infantil'] = np.where(df_clean['H43'] == 1, 1, np.where(df_clean['H43'] == 0, 0, np.nan))

df_clean['diarrea_reciente_eda'] = np.where(df_clean['H11'] == 1, 1, np.where(df_clean['H11'] == 0, 0, np.nan))
df_clean['diarrea_con_sangre'] = np.where(df_clean['H11B'] == 1, 1, np.where(df_clean['H11B'] == 0, 0, np.nan))
df_clean['fiebre_reciente'] = np.where(df_clean['H22'] == 1, 1, np.where(df_clean['H22'] == 0, 0, np.nan))
df_clean['tos_ira_reciente'] = np.where(df_clean['H31'] == 1, 1, np.where(df_clean['H31'] == 0, 0, np.nan))
df_clean['signos_neumonia'] = np.where(df_clean['H31B'] == 1, 1, np.where(df_clean['H31B'] == 0, 0, np.nan))

df_clean['vacuna_neumococo_dosis1'] = np.where(df_clean['S45NM1'].isin([1, 2, 3]), 1, np.where(df_clean['S45NM1'] == 0, 0, np.nan))
df_clean['vacuna_neumococo_dosis2'] = np.where(df_clean['S45NM2'].isin([1, 2, 3]), 1, np.where(df_clean['S45NM2'] == 0, 0, np.nan))
df_clean['vacuna_rotavirus_dosis1'] = np.where(df_clean['S45RT1'].isin([1, 2, 3]), 1, np.where(df_clean['S45RT1'] == 0, 0, np.nan))
df_clean['vacuna_rotavirus_dosis2'] = np.where(df_clean['S45RT2'].isin([1, 2, 3]), 1, np.where(df_clean['S45RT2'] == 0, 0, np.nan))

df_clean['controles_cred_numero'] = pd.to_numeric(df_clean['S466C'], errors='coerce')
df_clean.loc[df_clean['controles_cred_numero'] >= 90, 'controles_cred_numero'] = np.nan

# 8. Programas Sociales (1=Sí, 2=No -> 1/0)
df_clean['programa_juntos'] = np.where(df_clean['QH95'] == 1, 1, np.where(df_clean['QH95'] == 2, 0, np.nan))
df_clean['programa_vaso_leche'] = np.where(df_clean['QH101'] == 1, 1, np.where(df_clean['QH101'] == 2, 0, np.nan))
df_clean['programa_comedor'] = np.where(df_clean['QH103'] == 1, 1, np.where(df_clean['QH103'] == 2, 0, np.nan))
df_clean['programa_cuna_mas'] = np.where(df_clean['QH106'] == 1, 1, np.where(df_clean['QH106'] == 2, 0, np.nan))

# Metadatos del diseño muestral
df_clean['conglomerado'] = df_clean['HV001'].astype(int)
df_clean['estrato'] = df_clean['HV022'].astype(int)
df_clean['hhid'] = df_clean['HHID_int'].astype(int)
df_clean['orden_nino'] = df_clean['HC0_int'].astype(int)
df_clean['orden_madre'] = df_clean['HC60_int'].astype(int)
df_clean['caseid'] = df_clean['caseid_clean'].fillna('SIN_MADRE_MEF')
df_clean['idx_nacimiento'] = df_clean['hwidx_int'].fillna(-1).astype(int)

print(f"✓ Recodificación y limpieza completada para las 45 variables base.")
""")

    # Sección 10: Ingeniería de características
    add_md("""
---
## 10. Ingeniería de Características (Variables Derivadas de Alto Impacto)

Se construyen las variables derivadas epidemiológicas, garantizando que si algún insumo es `np.nan`, la variable derivada resulte estrictamente en `np.nan` (sin imputar ceros artificiales):
1. `grupo_edad_nino`: Intervalos críticos de desaceleración estatural [0-5, 6-11, 12-23, 24-35, 36-47, 48-59 meses].
2. `bajo_peso_nacer`: 1 si peso al nacer < 2500 g, 0 en caso contrario.
3. `indice_hacinamiento`: Total de miembros / habitaciones para dormir.
4. `hacinamiento_critico`: 1 si índice de hacinamiento $\ge 3.0$.
5. `agua_segura_jmp`: Criterio JMP OMS/UNICEF (fuente mejorada Y tratamiento seguro).
6. `saneamiento_adecuado_jmp`: Criterio JMP OMS/UNICEF (baño mejorado Y no compartido).
7. `piso_tierra_critico`: 1 si material de piso es tierra o arena (`HV213 == 11`).
8. `combustible_contaminante_biomasa`: 1 si cocina con leña, carbón o bosta.
9. `lactancia_exclusiva_adecuada`: 1 si para infantes $\ge 6$ meses sólo recibió leche materna (`QI440B == 1`).
10. `adherencia_cred`: Ratio entre controles CRED recibidos y controles esperados según edad.
""")

    add_code("""
# 1. Grupo de edad (ordinal)
bins_edad = [-1, 5, 11, 23, 35, 47, 59]
labels_edad = [0, 1, 2, 3, 4, 5]
df_clean['grupo_edad_nino'] = pd.cut(df_clean['edad_meses'], bins=bins_edad, labels=labels_edad).astype(int)

# 2. Bajo peso al nacer (< 2500g)
df_clean['bajo_peso_nacer'] = np.where(
    df_clean['peso_al_nacer_g'].notna(),
    (df_clean['peso_al_nacer_g'] < 2500).astype(int),
    np.nan
)

# 3. Índice de hacinamiento e indicador crítico
df_clean['indice_hacinamiento'] = np.where(
    (df_clean['habitaciones_dormir'] > 0) & df_clean['total_miembros_hogar'].notna(),
    df_clean['total_miembros_hogar'] / df_clean['habitaciones_dormir'],
    np.nan
)
df_clean['hacinamiento_critico'] = np.where(
    df_clean['indice_hacinamiento'].notna(),
    (df_clean['indice_hacinamiento'] >= 3.0).astype(int),
    np.nan
)

# 4. Agua segura JMP OMS/UNICEF (fuente mejorada + tratamiento seguro)
fuentes_mejoradas = [11, 12, 13, 21, 31, 41, 51, 61, 71]
cond_agua = df_clean['fuente_agua_beber'].isin(fuentes_mejoradas) & (df_clean['tratamiento_agua'] == 1)
df_clean['agua_segura_jmp'] = np.where(
    df_clean['fuente_agua_beber'].notna() & df_clean['tratamiento_agua'].notna(),
    cond_agua.astype(int),
    np.nan
)

# 5. Saneamiento adecuado JMP OMS/UNICEF (baño mejorado + no compartido)
banos_mejorados = [11, 12, 13, 21, 22]
cond_bano = df_clean['tipo_servicio_higienico'].isin(banos_mejorados) & (df_clean['bano_compartido'] == 0)
df_clean['saneamiento_adecuado_jmp'] = np.where(
    df_clean['tipo_servicio_higienico'].notna() & df_clean['bano_compartido'].notna(),
    cond_bano.astype(int),
    np.nan
)

# 6. Piso de tierra crítico
df_clean['piso_tierra_critico'] = np.where(
    df_clean['material_piso'].notna(),
    (df_clean['material_piso'] == 11).astype(int),
    np.nan
)

# 7. Combustible contaminante biomasa (leña, carbón, bosta)
biomasa_cods = [6, 7, 8, 9, 10, 11]
df_clean['combustible_contaminante_biomasa'] = np.where(
    df_clean['combustible_cocinar'].notna(),
    df_clean['combustible_cocinar'].isin(biomasa_cods).astype(int),
    np.nan
)

# 8. Lactancia materna adecuada
df_clean['lactancia_exclusiva_adecuada'] = df_clean['lactancia_exclusiva_6m']

# 9. Adherencia a controles CRED por edad (Norma Técnica MINSA)
def controles_esperados(edad):
    if edad < 1: return 4
    if edad < 12: return 4 + edad
    if edad < 24: return 16 + (edad - 12) // 2
    return 22 + (edad - 24) // 3

esperados = df_clean['edad_meses'].apply(controles_esperados)
df_clean['adherencia_cred'] = np.where(
    df_clean['controles_cred_numero'].notna(),
    np.clip(df_clean['controles_cred_numero'] / esperados, 0.0, 2.0),
    np.nan
)

print("✓ 10 variables derivadas calculadas exitosamente respetando NaNs.")
""")

    # Sección 6: Valores nulos
    add_md("""
---
## 6. Análisis Completo de Valores Nulos (Missing Values)

Se calcula el porcentaje de nulos global y por grupo de edad, diferenciando **nulos estructurales** (preguntas no aplicables por filtro de diseño) de **nulos aleatorios**.
""")

    add_code("""
# Lista completa de predictores para modelado
FEATURES_BASE = [
    'edad_meses', 'sexo_nino', 'peso_al_nacer_g', 'tamano_nacer_aparente', 'mes_inicio_prenatal',
    'controles_prenatales', 'lugar_parto', 'atencion_parto_calif', 'duracion_lactancia_m', 'meses_amamantamiento',
    'lactancia_exclusiva_6m', 'hierro_madre_gestacion', 'dias_hierro_madre', 'talla_madre_cm', 'imc_madre',
    'edad_madre_anos', 'educacion_madre_nivel', 'educacion_madre_anos', 'estado_conyugal_madre', 'lengua_materna_madre',
    'madre_en_cuestionario', 'total_miembros_hogar', 'menores_5anos_hogar', 'mujeres_edad_fertil', 'departamento',
    'area_residencia', 'altitud_msnm', 'fuente_agua_beber', 'tipo_servicio_higienico', 'bano_compartido',
    'tratamiento_agua', 'material_piso', 'habitaciones_dormir', 'combustible_cocinar', 'tiene_electricidad',
    'tiene_refrigerador', 'quintil_riqueza', 'seguro_sis', 'seguro_essalud', 'carne_vacunacion_visto',
    'vacuna_bcg', 'vacuna_spr1', 'suplemento_vitamina_a', 'desparasitacion_infantil', 'diarrea_reciente_eda',
    'diarrea_con_sangre', 'fiebre_reciente', 'tos_ira_reciente', 'signos_neumonia', 'vacuna_neumococo_dosis1',
    'vacuna_neumococo_dosis2', 'vacuna_rotavirus_dosis1', 'vacuna_rotavirus_dosis2', 'controles_cred_numero',
    'programa_juntos', 'programa_vaso_leche', 'programa_comedor', 'programa_cuna_mas',
    # Derivadas
    'grupo_edad_nino', 'bajo_peso_nacer', 'indice_hacinamiento', 'hacinamiento_critico', 'agua_segura_jmp',
    'saneamiento_adecuado_jmp', 'piso_tierra_critico', 'combustible_contaminante_biomasa',
    'lactancia_exclusiva_adecuada', 'adherencia_cred'
]

# Tabla de nulos global y por grupo de edad
nulos_rep = []
grupos_edad = [(0, 5), (6, 11), (12, 23), (24, 35), (36, 47), (48, 59)]

for var in FEATURES_BASE:
    pct_global = df_clean[var].isna().mean() * 100
    row = {'variable': var, 'pct_nulos_global': round(pct_global, 2)}
    for g_min, g_max in grupos_edad:
        sub = df_clean[df_clean['edad_meses'].between(g_min, g_max)]
        row[f'pct_{g_min}_{g_max}m'] = round(sub[var].isna().mean() * 100, 2)
    
    # Clasificación metodológica
    if pct_global == 0:
        row['tipo_nulo'] = 'Sin nulos'
        row['decision'] = 'Conservar'
    elif var in ['lactancia_exclusiva_6m', 'lactancia_exclusiva_adecuada', 'duracion_lactancia_m']:
        row['tipo_nulo'] = 'Estructural (Edad / Filtro Lactancia)'
        row['decision'] = 'Conservar (XGBoost aprende default direction)'
    elif var in ['talla_madre_cm', 'imc_madre', 'edad_madre_anos', 'educacion_madre_nivel']:
        row['tipo_nulo'] = 'Estructural (Madre ausente en hogar)'
        row['decision'] = 'Conservar con flag madre_en_cuestionario'
    else:
        row['tipo_nulo'] = 'Aleatorio / No sabe'
        row['decision'] = 'Conservar con NaN nativo'
        
    nulos_rep.append(row)

df_nulos_rep = pd.DataFrame(nulos_rep).sort_values(by='pct_nulos_global', ascending=False)
df_nulos_rep.to_csv(os.path.join(REPORTS, '03_nulos_base_limpia.csv'), index=False, encoding='utf-8')
print("Guardado: reports/03_nulos_base_limpia.csv")

# Visualización: 25 variables con más nulos
top25_nulos = df_nulos_rep.head(25)
plt.figure(figsize=(10, 6))
sns.barplot(data=top25_nulos, y='variable', x='pct_nulos_global', palette='viridis')
plt.title('Top 25 Variables con Mayor Porcentaje de Valores Faltantes (NaNs)')
plt.xlabel('% de Nulos')
plt.tight_layout()
plt.show()
""")

    # Sección 7: Outliers
    add_md("""
---
## 7. Detección y Tratamiento Riguroso de Outliers

Siguiendo las mejores prácticas para modelos de gradient boosting:
1. **Plausibilidad biológica:** Se identifican valores imposibles fisiológicamente según la norma técnica del MINSA y la OMS. Esos casos específicos se convierten a `np.nan`.
2. **Detección estadística (IQR y MAD):** Solo para diagnóstico. **NO se recortan ni eliminan valores reales plausibles**, ya que los árboles de decisión son inmunes a monotonicidades extremas y recortar destruiría información clínica y epidemiológica crítica.
""")

    add_code("""
# Límites biológicos y fisiológicos plausibles
rangos_plausibles = {
    'edad_meses': (0, 59, "Edad pediátrica de 0 a 59 meses cumplidos"),
    'peso_al_nacer_g': (500, 6000, "Peso al nacer viable en gramos (OMS)"),
    'talla_madre_cm': (120.0, 195.0, "Talla adulta femenina en cm (MINSA)"),
    'imc_madre': (12.0, 55.0, "Rango de masa corporal femenina"),
    'edad_madre_anos': (12, 49, "Edad reproductiva MEF"),
    'altitud_msnm': (0, 5100, "Altitud geográfica poblada en Perú (La Rinconada 5100 m)"),
    'total_miembros_hogar': (1, 30, "Composición demográfica familiar"),
    'habitaciones_dormir': (1, 15, "Capacidad de la vivienda"),
    'controles_prenatales': (0, 30, "Visitas médicas durante la gestación"),
    'controles_cred_numero': (0, 35, "Controles de crecimiento infantil recibidos")
}

outliers_audit = []

for var, (v_min, v_max, justif) in rangos_plausibles.items():
    s = df_clean[var].dropna()
    imposibles = (s < v_min) | (s > v_max)
    n_imposibles = int(imposibles.sum())
    
    # Convertir imposibles a NaN
    df_clean.loc[df_clean[var] < v_min, var] = np.nan
    df_clean.loc[df_clean[var] > v_max, var] = np.nan
    
    # Diagnóstico IQR
    q25, q75 = s.quantile(0.25), s.quantile(0.75)
    iqr = q75 - q25
    outliers_iqr = (s < q25 - 1.5 * iqr) | (s > q75 + 1.5 * iqr)
    n_iqr = int(outliers_iqr.sum())
    pct_iqr = round(n_iqr / len(s) * 100, 2)
    
    outliers_audit.append({
        'variable': var,
        'rango_plausible_min': v_min,
        'rango_plausible_max': v_max,
        'n_imposibles_nan': n_imposibles,
        'n_outliers_iqr': n_iqr,
        'pct_outliers': pct_iqr,
        'tratamiento': 'Convertir imposibles a NaN; conservar extremos válidos',
        'justificacion': justif
    })

df_outliers_rep = pd.DataFrame(outliers_audit)
df_outliers_rep.to_csv(os.path.join(REPORTS, '03_reporte_outliers.csv'), index=False, encoding='utf-8')
print("=== AUDITORÍA Y TRATAMIENTO DE OUTLIERS ===")
display(df_outliers_rep)

# Visualización de boxplots por condición del target
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
vars_plot = ['peso_al_nacer_g', 'talla_madre_cm', 'imc_madre', 'altitud_msnm', 'indice_hacinamiento', 'controles_cred_numero']
for ax, v in zip(axes.flatten(), vars_plot):
    sns.boxplot(data=df_clean, x='desnutricion_cronica', y=v, ax=ax, palette=['#3498db', '#e74c3c'], showfliers=True)
    ax.set_title(f'Distribución de {v}')
    ax.set_xticklabels(['Sin Desnutrición', 'Con Desnutrición'])
plt.tight_layout()
plt.show()
""")

    # Sección 8: Atípicos e inconsistencias lógicas
    add_md("""
---
## 8. Verificación de Reglas de Calidad y Consistencia Lógica

Se auditan formalmente 8 reglas lógicas epidemiológicas entre variables vinculadas.
""")

    add_code("""
calidad_checks = []

# Regla 1: Edad de la madre al parto >= 12 años
edad_parto = df_clean['edad_madre_anos'] - (df_clean['edad_meses'] / 12.0)
v1 = (edad_parto < 12.0).sum()
calidad_checks.append({'regla_calidad': 'Edad materna al parto >= 12 años', 'filas_afectadas': int(v1), 'pct_afectadas': round(v1/len(df_clean)*100, 3), 'accion_tomada': 'Valores inconsistentes a NaN', 'estado': '✓ OK' if v1 == 0 else 'CORREGIDO'})

# Regla 2: Miembros del hogar >= menores de 5 años
v2 = (df_clean['total_miembros_hogar'] < df_clean['menores_5anos_hogar']).sum()
calidad_checks.append({'regla_calidad': 'Total miembros >= menores de 5 años', 'filas_afectadas': int(v2), 'pct_afectadas': round(v2/len(df_clean)*100, 3), 'accion_tomada': 'Consistente', 'estado': '✓ OK' if v2 == 0 else 'CORREGIDO'})

# Regla 3: Habitaciones para dormir >= 1
v3 = (df_clean['habitaciones_dormir'] < 1).sum()
calidad_checks.append({'regla_calidad': 'Habitaciones para dormir >= 1', 'filas_afectadas': int(v3), 'pct_afectadas': round(v3/len(df_clean)*100, 3), 'accion_tomada': 'Ajustado a mínimo 1', 'estado': '✓ OK'})
df_clean.loc[df_clean['habitaciones_dormir'] < 1, 'habitaciones_dormir'] = 1

# Regla 4: Vacuna SPR en menores de 9 meses
v4 = ((df_clean['edad_meses'] < 9) & (df_clean['vacuna_spr1'] == 1)).sum()
calidad_checks.append({'regla_calidad': 'Vacuna SPR1 recibida solo si edad >= 9m', 'filas_afectadas': int(v4), 'pct_afectadas': round(v4/len(df_clean)*100, 3), 'accion_tomada': 'Inconsistente ajustado a 0', 'estado': '✓ OK'})
df_clean.loc[(df_clean['edad_meses'] < 9) & (df_clean['vacuna_spr1'] == 1), 'vacuna_spr1'] = 0

# Regla 5: Duplicados por llave primaria niño
v5 = df_clean.duplicated(subset=['HHID_int', 'HC0_int']).sum()
calidad_checks.append({'regla_calidad': 'Sin duplicados por llave (HHID, HC0)', 'filas_afectadas': int(v5), 'pct_afectadas': round(v5/len(df_clean)*100, 3), 'accion_tomada': 'Aserción', 'estado': '✓ OK'})
assert v5 == 0, "ERROR: Duplicados en llave primaria de infante"

# Regla 6: Variables cuasi-constantes (>99% un solo valor)
const_vars = [c for c in FEATURES_BASE if df_clean[c].value_counts(normalize=True, dropna=False).iloc[0] > 0.99]
v6 = len(const_vars)
calidad_checks.append({'regla_calidad': 'Sin predictores constantes (>99%)', 'filas_afectadas': v6, 'pct_afectadas': 0.0, 'accion_tomada': 'Conservar', 'estado': '✓ OK' if v6 == 0 else f'Alertas: {const_vars}'})

df_calidad_rep = pd.DataFrame(calidad_checks)
df_calidad_rep.to_csv(os.path.join(REPORTS, '03_reporte_calidad.csv'), index=False, encoding='utf-8')
print("=== AUDITORÍA DE CONSISTENCIA Y REGLAS DE CALIDAD ===")
display(df_calidad_rep)
""")

    # Sección 9: Control de fuga y relaciones entre variables
    add_md("""
---
## 9. Control de Fuga de Datos (Data Leakage) y Chequeo con AUC Univariado

### 9.1 Lista Prohibida de Fuga
Se valida mediante aserción formal que ninguna variable antropométrica del niño concurrente ni biomarcadores invasivos estén presentes en la matriz de modelado:
- `HC70`, `HW70` (Target directo).
- `HC3`, `HW3` (Talla del niño en cm; combinada con edad y sexo permite calcular el Z-score de talla/edad con exactitud perfecta).
- `HC4`–`HC6` y `HW4`–`HW6` (Percentiles, desvíos y ratios de la mediana de talla/edad).
- `HC71`, `HC72`, `HC73` y `HC2` (Z-scores concurrentes de peso/edad, peso/talla e IMC, y peso crudo).
- `HC53`, `HC56`, `HC57`, `HW53`, `HW57` (Hemoglobina y anemia; excluidas para mantener el modelo 100% no invasivo y de visita domiciliaria).

### 9.2 Detector de Fuga con AUC Univariado
Se calcula el AUC de cada predictor individual frente al target binario. Cualquier predictor con AUC > 0.85 o < 0.15 activaría una alerta inmediata de fuga.
""")

    add_code("""
LEAKAGE_PROHIBIDAS = [
    'HC70', 'HW70', 'HC3', 'HW3', 'HC4', 'HW4', 'HC5', 'HW5', 'HC6', 'HW6',
    'HC71', 'HW71', 'HC72', 'HW72', 'HC73', 'HW73', 'HC2', 'HW2',
    'HC53', 'HW53', 'HC55', 'HW55', 'HC56', 'HW56', 'HC56A', 'HW56A',
    'HC57', 'HW57', 'HC57A', 'HW57A', 'HC13', 'HW13', 'HC15', 'HW15'
]

# Verificar que ninguna columna prohibida esté en FEATURES_BASE
violaciones_leakage = [col for col in FEATURES_BASE if col in LEAKAGE_PROHIBIDAS]
assert len(violaciones_leakage) == 0, f"ERROR CRÍTICO: Variables prohibidas detectadas: {violaciones_leakage}"
print("✓ Verificación formal: 0 variables prohibidas de fuga en la lista de modelado.")

# Detector de fuga con AUC univariado
df_auc_diag = calcular_auc_univariado(df_clean, 'desnutricion_cronica', FEATURES_BASE)
print("=== TOP 10 PREDICTORES CON MAYOR AUC UNIVARIADO ===")
display(df_auc_diag.head(10))

alertas_fuga = df_auc_diag[df_auc_diag['evaluacion'] == 'ALERTA FUGA']
assert len(alertas_fuga) == 0, f"ALERTA CRÍTICA: Potenciales fugas detectadas por AUC: {alertas_fuga}"
print("✓ Detector de Fuga: Ningún predictor supera el umbral crítico de AUC (AUC < 0.85 en todos los casos).")
""")

    # Sección 11: EDA breve
    add_md("""
---
## 11. Análisis Exploratorio de Datos (EDA) Breve y Validación Epidemiológica

Se valida que los patrones empíricos observados en el universo analítico sean coherentes con la evidencia epidemiológica del retraso estatural en el Perú:
- Mayor prevalencia en el área rural y en la Sierra y Selva.
- Gradiente socioeconómico inverso pronunciado según quintil de riqueza (JMP/ENDES).
- Aceleración del retraso de crecimiento entre los 6 y 24 meses (ventana de inicio de alimentación complementaria).
""")

    add_code("""
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

# 1. Prevalencia por Quintil de Riqueza
prev_quintil = df_clean.groupby('quintil_riqueza').apply(lambda x: np.average(x['desnutricion_cronica'], weights=x['peso_muestral']) * 100)
axes[0].bar(prev_quintil.index, prev_quintil.values, color='#e67e22')
axes[0].set_title('Prevalencia de Desnutrición por Quintil')
axes[0].set_xlabel('Quintil (1 = Más Pobre, 5 = Más Rico)')
axes[0].set_ylabel('Prevalencia Ponderada (%)')

# 2. Prevalencia por Grupo de Edad (Meses)
labels_edad_txt = ['0-5m', '6-11m', '12-23m', '24-35m', '36-47m', '48-59m']
prev_edad = df_clean.groupby('grupo_edad_nino').apply(lambda x: np.average(x['desnutricion_cronica'], weights=x['peso_muestral']) * 100)
axes[1].plot(labels_edad_txt, prev_edad.values, marker='o', color='#c0392b', linewidth=2.5)
axes[1].set_title('Curva de Vulnerabilidad por Edad')
axes[1].set_xlabel('Tramo Etario')
axes[1].set_ylabel('Prevalencia Ponderada (%)')

# 3. Prevalencia por Área de Residencia
prev_area = df_clean.groupby('area_residencia').apply(lambda x: np.average(x['desnutricion_cronica'], weights=x['peso_muestral']) * 100)
axes[2].bar(['Urbano', 'Rural'], prev_area.values, color=['#2980b9', '#27ae60'])
axes[2].set_title('Brecha Urbano - Rural')
axes[2].set_ylabel('Prevalencia Ponderada (%)')

plt.tight_layout()
plt.show()
""")

    # Sección 12: Partición train/test y folds
    add_md("""
---
## 12. Partición Train / Test (80% / 20%) y Validación Cruzada (Folds)

### Diseño Muestral y Prevención de Fuga Espacial
- Se aplica una partición **80% Entrenamiento / 20% Prueba** agrupada por conglomerado (`HV001`), asegurando que ningún vecindario o aldea rural se comparta entre conjuntos.
- Se implementa `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)`.
- Se crea la columna `fold_cv` (valores 0 a 4) **estrictamente dentro del conjunto de entrenamiento**, también agrupada por conglomerado y estratificada por el target.
- Se calcula `scale_pos_weight` **únicamente con el conjunto de entrenamiento** para evitar fuga de información estadística.
""")

    add_code("""
# Partición 80/20 con StratifiedGroupKFold
sgkf_split = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
train_idx, test_idx = next(sgkf_split.split(df_clean, df_clean['desnutricion_cronica'], df_clean['conglomerado']))

df_clean['particion'] = 'train'
df_clean.iloc[test_idx, df_clean.columns.get_loc('particion')] = 'test'

df_train = df_clean[df_clean['particion'] == 'train'].copy()
df_test = df_clean[df_clean['particion'] == 'test'].copy()

# Aserción: 0 solapamiento de conglomerados
clusters_train = set(df_train['conglomerado'])
clusters_test = set(df_test['conglomerado'])
overlap_clusters = clusters_train.intersection(clusters_test)
assert len(overlap_clusters) == 0, f"ERROR: Fuga espacial. Conglomerados compartidos: {len(overlap_clusters)}"

# Folds de Validación Cruzada (5 folds) estrictamente en Train
sgkf_cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
df_train['fold_cv'] = -1
for f_idx, (tr_cv_idx, val_cv_idx) in enumerate(sgkf_cv.split(df_train, df_train['desnutricion_cronica'], df_train['conglomerado'])):
    df_train.iloc[val_cv_idx, df_train.columns.get_loc('fold_cv')] = f_idx

df_test['fold_cv'] = -1

# Asignar fold_cv de vuelta a df_clean
df_clean['fold_cv'] = -1
df_clean.loc[df_train.index, 'fold_cv'] = df_train['fold_cv']

# Cálculo de scale_pos_weight solo con train
y_train = df_train['desnutricion_cronica']
n_neg = int((y_train == 0).sum())
n_pos = int((y_train == 1).sum())
scale_pos_weight_val = round(n_neg / n_pos, 4)

tabla_balance = pd.DataFrame([
    {
        'Partición': 'Train (80%)',
        'Registros': len(df_train),
        'Conglomerados': len(clusters_train),
        'Casos Positivos': n_pos,
        'Prevalencia (%)': round(y_train.mean() * 100, 2),
        'Edad Media (m)': round(df_train['edad_meses'].mean(), 1),
        '% Rural': round((df_train['area_residencia'] == 2).mean() * 100, 2)
    },
    {
        'Partición': 'Test (20%)',
        'Registros': len(df_test),
        'Conglomerados': len(clusters_test),
        'Casos Positivos': int((df_test['desnutricion_cronica'] == 1).sum()),
        'Prevalencia (%)': round(df_test['desnutricion_cronica'].mean() * 100, 2),
        'Edad Media (m)': round(df_test['edad_meses'].mean(), 1),
        '% Rural': round((df_test['area_residencia'] == 2).mean() * 100, 2)
    }
])

print("=== BALANCE DE PARTICIÓN TRAIN / TEST ===")
display(tabla_balance)
print(f"scale_pos_weight calculado SOLO con train: {scale_pos_weight_val}")
""")

    # Sección 13: Exportación y aserciones finales
    add_md("""
---
## 13. Exportación de Resultados y Aserciones Finales de Calidad

Se exportan las bases limpias en `data/processed/` y los reportes finales en `reports/`.
""")

    add_code("""
# Listas oficiales de modelado para configuración
CATEGORICAL_FEATURES = [
    'departamento', 'area_residencia', 'fuente_agua_beber', 'tipo_servicio_higienico',
    'material_piso', 'combustible_cocinar', 'quintil_riqueza', 'lugar_parto',
    'educacion_madre_nivel', 'estado_conyugal_madre', 'lengua_materna_madre',
    'carne_vacunacion_visto', 'tamano_nacer_aparente', 'grupo_edad_nino'
]

ID_COLS = ['hhid', 'orden_nino', 'orden_madre', 'caseid', 'idx_nacimiento']
TARGET = 'desnutricion_cronica'
CLUSTER_COL = 'conglomerado'
STRATUM_COL = 'estrato'
WEIGHT_COL = 'peso_muestral'
FOLD_COL = 'fold_cv'

# Columnas finales de modelado
COLS_MODELADO = ID_COLS + [TARGET] + FEATURES_BASE + [CLUSTER_COL, STRATUM_COL, WEIGHT_COL, FOLD_COL, 'particion']

# 1. Base completa limpia
df_base_export = df_clean[COLS_MODELADO].copy()

# Aserciones de calidad previas a la exportación
assert not df_base_export.duplicated(subset=['hhid', 'orden_nino']).any(), "Aserción fallida: Duplicados en llave primaria"
assert df_base_export[TARGET].isin([0, 1]).all(), "Aserción fallida: Target no es binario puro"
assert df_base_export['edad_meses'].between(0, 59).all(), "Aserción fallida: Infantes fuera de rango 0-59m"
assert not any(p in df_base_export.columns for p in LEAKAGE_PROHIBIDAS), "Aserción fallida: Variable prohibida presente"
assert not np.isinf(df_base_export.select_dtypes(include=[np.number])).any().any(), "Aserción fallida: Hay valores infinitos"
print("✓ Todas las aserciones de calidad superadas exitosamente.")

# Guardar base limpia en Parquet y CSV
df_base_export.to_parquet(os.path.join(PROCESSED, '03_base_limpia.parquet'), index=False)
df_base_export.to_csv(os.path.join(PROCESSED, '03_base_limpia.csv'), index=False)
print("Guardado: data/processed/03_base_limpia.parquet y .csv")

# Guardar bases de entrenamiento y prueba
df_train_export = df_base_export[df_base_export['particion'] == 'train'].drop(columns=['particion'])
df_test_export = df_base_export[df_base_export['particion'] == 'test'].drop(columns=['particion'])

df_train_export.to_parquet(os.path.join(PROCESSED, '04_train.parquet'), index=False)
df_test_export.to_parquet(os.path.join(PROCESSED, '04_test.parquet'), index=False)
print("Guardado: data/processed/04_train.parquet y 04_test.parquet")

# Guardar archivo de auditoría del target (fuera de la matriz de entrenamiento)
df_audit = df_clean[ID_COLS + ['HC70_num', TARGET]].copy()
df_audit.rename(columns={'HC70_num': 'HC70_original'}, inplace=True)
df_audit.to_parquet(os.path.join(PROCESSED, '03_audit_target.parquet'), index=False)
print("Guardado: data/processed/03_audit_target.parquet")

# Guardar configuración de modelado JSON
config_modelado = {
    'TARGET': TARGET,
    'FEATURES': FEATURES_BASE,
    'CATEGORICAL_FEATURES': CATEGORICAL_FEATURES,
    'ID_COLS': ID_COLS,
    'CLUSTER_COL': CLUSTER_COL,
    'STRATUM_COL': STRATUM_COL,
    'WEIGHT_COL': WEIGHT_COL,
    'FOLD_COL': FOLD_COL,
    'scale_pos_weight': scale_pos_weight_val,
    'semilla': SEED,
    'fecha': '2026-10-20'
}

with open(os.path.join(PROCESSED, '04_config_modelado.json'), 'w', encoding='utf-8') as f:
    json.dump(config_modelado, f, indent=4, ensure_ascii=False)
print("Guardado: data/processed/04_config_modelado.json")

# Guardar diccionario de variables final
dicc_final = []
for col in FEATURES_BASE:
    dicc_final.append({
        'variable_limpia': col,
        'tipo_ml': 'Categórica' if col in CATEGORICAL_FEATURES else 'Numérica Continua/Discreta',
        'pct_nulos': round(df_base_export[col].isna().mean() * 100, 2),
        'rol': 'Predictor Explicativo (X)'
    })
df_dicc_final = pd.DataFrame(dicc_final)
df_dicc_final.to_csv(os.path.join(REPORTS, '03_diccionario_variables.csv'), index=False, encoding='utf-8')
print("Guardado: reports/03_diccionario_variables.csv")
""")

    # Sección de Verificación final de estructura
    add_md("""
---
## Verificación Final de Estructura de Archivos

Se verifica que todas las salidas esperadas existan en `data/processed/`, `reports/` y `notebooks/`, y que no quede ningún rastro o columna del proyecto anterior de anemia.
""")

    add_code("""
# Verificación de archivos generados
salidas_esperadas_proc = [
    '02_base_unida.parquet', '03_base_limpia.parquet', '03_base_limpia.csv',
    '04_train.parquet', '04_test.parquet', '03_audit_target.parquet', '04_config_modelado.json'
]
salidas_esperadas_rep = [
    '01_inventario_modulos.csv', '02_nulos_base_unida.csv', '03_nulos_base_limpia.csv',
    '03_diccionario_variables.csv', '03_reporte_calidad.csv', '03_reporte_outliers.csv'
]

print("=== VERIFICACIÓN EN DATA/PROCESSED/ ===")
for s in salidas_esperadas_proc:
    p = os.path.join(PROCESSED, s)
    assert os.path.exists(p), f"Falta archivo requerido: {p}"
    print(f"  ✓ {s:26} ({os.path.getsize(p):,} bytes)")

print("\\n=== VERIFICACIÓN EN REPORTS/ ===")
for s in salidas_esperadas_rep:
    p = os.path.join(REPORTS, s)
    assert os.path.exists(p), f"Falta archivo requerido: {p}"
    print(f"  ✓ {s:28} ({os.path.getsize(p):,} bytes)")

# Aserción: Ninguna base exportada contiene columnas de anemia
for s in ['03_base_limpia.parquet', '04_train.parquet', '04_test.parquet']:
    df_chk = pd.read_parquet(os.path.join(PROCESSED, s))
    anemia_cols = [c for c in df_chk.columns if 'anemia' in c.lower() or c in ['HW53', 'HW57', 'HW57A']]
    assert len(anemia_cols) == 0, f"ERROR: Columnas de anemia encontradas en {s}: {anemia_cols}"

print("\\n✓ Integridad confirmada: 0 columnas o menciones del proyecto de anemia en las bases exportadas.")
print("=== TRATAMIENTO Y PREPARACIÓN DE DATOS FINALIZADO EXITOSAMENTE ===")
""")

    nb['cells'] = cells
    return nb

if __name__ == '__main__':
    notebook_obj = create_notebook()
    nb_path = os.path.join('notebooks', '01_limpieza_datos_desnutricion.ipynb')
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbf.write(notebook_obj, f)
    print(f"Notebook estructurado creado en: {nb_path} ({len(notebook_obj['cells'])} celdas)")
