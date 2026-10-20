"""
Módulo de utilidades para la preparación de datos de desnutrición crónica infantil
ENDES 2025 (INEI, Perú) - Preparación para XGBoost.
"""

import os
import glob
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score


def to_num(val):
    """
    Convierte valores a numérico de forma robusta.
    Maneja strings con espacios, códigos nulos y convierte a float/int según aplique.
    """
    if pd.isna(val):
        return np.nan
    if isinstance(val, (int, float, np.integer, np.floating)):
        return val
    val_str = str(val).strip()
    if val_str == '' or val_str.lower() in ('nan', 'none', 'null', '.'):
        return np.nan
    try:
        f = float(val_str)
        return int(f) if f.is_integer() else f
    except (ValueError, TypeError):
        return np.nan


def localizar_archivos_csv(root_dir):
    """
    Localiza recursivamente todos los archivos *_2025.csv en el árbol de data/.
    Evita symlinks rotos y reporta la ruta válida, filas y columnas de cada uno.
    Prioridad: data/raw/ si es archivo real válido; de lo contrario la carpeta modular.
    """
    data_dir = os.path.join(root_dir, 'data')
    pattern = os.path.join(data_dir, '**', '*_2025.csv')
    all_csvs = glob.glob(pattern, recursive=True)
    
    file_map = {}
    inventario = []
    
    for p in sorted(all_csvs):
        fname = os.path.basename(p)
        base = fname.replace('_2025.csv', '')
        
        # Verificar si es archivo real y existe (evita symlinks rotos)
        if not (os.path.isfile(p) and os.path.exists(p)):
            continue
            
        is_link = os.path.islink(p)
        is_raw = 'data/raw/' in p.replace('\\', '/')
        
        # Si no está en el mapa, o si está en data/raw/ y no es symlink roto
        if base not in file_map or (is_raw and not is_link):
            file_map[base] = p

    for base, p in sorted(file_map.items()):
        df_head = pd.read_csv(p, nrows=5)
        n_cols = len(df_head.columns)
        with open(p, 'rb') as fp:
            n_rows = sum(1 for _ in fp) - 1
            
        inventario.append({
            'modulo_archivo': base,
            'archivo_csv': os.path.basename(p),
            'ruta_absoluta': p,
            'ruta_relativa': os.path.relpath(p, root_dir),
            'filas': n_rows,
            'columnas': n_cols,
            'tamano_bytes': os.path.getsize(p)
        })
        
    df_inv = pd.DataFrame(inventario)
    return file_map, df_inv


def limpiar_salidas_anemia(root_dir):
    """
    Elimina explícitamente y con control las salidas derivadas del proyecto de anemia.
    Verifica que ninguna ruta a borrar esté en data/raw/ ni en carpetas de módulos.
    """
    archivos_eliminar = [
        os.path.join(root_dir, 'data', 'processed', '02_base_unida.parquet'),
        os.path.join(root_dir, 'data', 'processed', '03_base_limpia.csv'),
        os.path.join(root_dir, 'data', 'processed', '03_base_limpia.parquet'),
        os.path.join(root_dir, 'reports', '01_inventario_modulos.csv'),
        os.path.join(root_dir, 'reports', '02_nulos_base_unida.csv'),
        os.path.join(root_dir, 'reports', '03_diccionario_variables.csv'),
        os.path.join(root_dir, 'reports', '03_nulos_base_limpia.csv'),
        os.path.join(root_dir, 'reports', '03_reporte_calidad.csv')
    ]
    
    resultados = []
    for f in archivos_eliminar:
        norm_path = os.path.normpath(f).replace('\\', '/')
        assert '/data/raw/' not in norm_path, f'Seguridad violada: {f} está en raw'
        assert not any(f'/data/{mod}/' in norm_path for mod in [
            '1031-mef', '1036-inmunizacion', '1041-programasocial',
            '1629_hogar', '1630_vivienda', '1633_embarazo', '1638_anemia'
        ]), f'Seguridad violada: {f} está en módulos'
        
        if os.path.exists(f):
            sz = os.path.getsize(f)
            os.remove(f)
            resultados.append({
                'archivo': os.path.relpath(f, root_dir),
                'tamano_bytes': sz,
                'resultado': 'ELIMINADO'
            })
        else:
            resultados.append({
                'archivo': os.path.relpath(f, root_dir),
                'tamano_bytes': 0,
                'resultado': 'NO EXISTÍA'
            })
            
    return pd.DataFrame(resultados)


def calcular_auc_univariado(df, target_col, feature_cols):
    """
    Calcula el AUC univariado de cada feature frente al target en train.
    Trata los NaNs evaluando el predictor sobre casos válidos.
    Alerta si AUC > 0.85 o AUC < 0.15 (potencial fuga de información).
    """
    res = []
    y = df[target_col].values
    for col in feature_cols:
        s = df[col]
        if s.dtype.name == 'category' or s.dtype == 'object':
            means = df.groupby(col, observed=True)[target_col].mean()
            s_num = df[col].map(means)
        else:
            s_num = pd.to_numeric(s, errors='coerce')
            
        mask = s_num.notna() & df[target_col].notna()
        if mask.sum() < 50 or df.loc[mask, target_col].nunique() < 2:
            auc = np.nan
        else:
            try:
                auc = roc_auc_score(y[mask], s_num[mask])
            except Exception:
                auc = np.nan
                
        alerta = 'ALERTA FUGA' if (pd.notna(auc) and (auc > 0.85 or auc < 0.15)) else 'OK'
        res.append({
            'variable': col,
            'n_validos': int(mask.sum()),
            'pct_validos': round(mask.mean() * 100, 2),
            'auc_univariado': round(auc, 4) if pd.notna(auc) else np.nan,
            'evaluacion': alerta
        })
        
    return pd.DataFrame(res).sort_values(by='auc_univariado', ascending=False, na_position='last')
