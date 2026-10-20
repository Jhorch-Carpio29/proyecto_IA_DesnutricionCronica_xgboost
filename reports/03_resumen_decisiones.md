# Resumen Ejecutivo de Decisiones Metodológicas y Tratamiento de Datos
## Proyecto: Predicción de Desnutrición Crónica Infantil (Stunting) — ENDES 2025
**Algoritmo Obligatorio:** XGBoost  
**Población:** Menores de 5 años (0 a 59 meses) con medición antropométrica válida  
**Fecha:** 2026-10-20 | **Semilla:** 42

---

### 1. Definición del Universo y Target
- **Fuente Oficial:** `HC70` en `RECH6_2025.csv` (centésimas de desviación estándar OMS 2006).
- **Criterio de Clasificación:** `desnutricion_cronica = 1` si `HC70 < -200` (-2.00 DE), `0` si `HC70 >= -200`.
- **Filtros de Depuración:** Se excluyeron códigos especiales de control antropométrico (`9996` implausible > 6 DE, `9997` inconsistente, `9998` no medido) y valores fuera del rango biológico [-600, 600].
- **Universo Analítico Final:** 18,987 infantes evaluados.
- **Prevalencia Nacional Sin Ponderar:** 11.87%
- **Prevalencia Nacional Ponderada:** 12.04% (consistente con reporte oficial INEI ~11.5 - 12.0%).
- **Brecha Urbano-Rural:** Urbano 7.95% vs. Rural 21.45% (ponderada).
- **Desbalance de Clase en Train:** `scale_pos_weight = 7.426`.

---

### 2. Integración Relacional de Módulos
- **Tabla Base Núcleo:** `RECH6` a nivel de infante.
- **Módulos de Hogar y Vivienda:** `RECH0`, `RECH23`, `Programas Sociales x Hogar` enlazados por `HHID` (tasa de match: 100.0%).
- **Seguro de Salud del Niño:** `RECH4` enlazado por `HHID` y `IDXH4 == HC0` (tasa de match: 100.0%).
- **Antropometría y Estado Conyugal Materno:** `RECH5` y `RECH1` enlazados por `HHID` y `HC60` (tasa de match: 94.78% en base completa; 100% para madres residentes en el hogar).
- **Historia Gestacional, Morbilidad y Vacunas:** `REC41`, `REC94`, `REC43`, `REC95`, `REC0111`, `REC91` enlazados mediante llave intrafamiliar normalizada.
- **Infantes sin madre residente (`HC60 >= 990`):** Se conservan en la muestra analítica con flag binario `madre_en_cuestionario = 0` y variables maternas en `NaN`.

---

### 3. Prevención Estricta de Fuga de Datos (Target Leakage) y Causalidad Inversa
- **Antropometría del Niño Excluida:** Se excluyeron de forma estricta la talla del niño (`HC3`/`HW3`), percentiles (`HC4`/`HW4`), desvíos de la mediana (`HC5`/`HW5`, `HC6`/`HW6`) y Z-scores concurrentes de peso/edad (`HC71`), peso/talla (`HC72`) e IMC (`HC73`).
- **Hemoglobina y Anemia:** Excluidas (`HC53`, `HC56`, `HC57`) para mantener el modelo 100% no invasivo para screening comunitario domiciliario.
- **Control de Causalidad Inversa:** Se excluyeron tratamientos reactivos como Sales de Rehidratación Oral (`H13`), jarabes y antibióticos para diarrea (`H15`), manteniendo únicamente síntomas y profilaxis preventiva universal (`M45`, `M46`).

---

### 4. Tratamiento de Códigos Especiales, Outliers y Nulos (Reglas XGBoost)
- **Códigos Especiales:** Códigos 8, 9, 96, 98, 99, 998, 9998 convertidos a `np.nan` antes de cualquier cálculo.
- **No Imputación:** No se imputó ninguna variable; se preservaron los NaNs para aprovechamiento del split nativo (`default_direction`) de XGBoost.
- **Outliers:** Se definieron rangos biológicamente plausibles (peso al nacer 500-6000g, talla materna 120-195cm, IMC 12-55). Los valores imposibles se convirtieron a `np.nan`; los valores extremos válidos se conservaron.
- **Variables Categóricas:** 14 variables declaradas en `CATEGORICAL_FEATURES` listas para `enable_categorical=True`.

---

### 5. Partición y Validación Cruzada
- **Partición Train/Test (80% / 20%):** Agrupada por conglomerado (`HV001`) con `StratifiedGroupKFold`. Cero solapamiento de comunidades entre train y test.
- **Folds en Entrenamiento:** 5 folds (`fold_cv` 0 a 4) generados estrictamente dentro de train, agrupados por conglomerado y estratificados por target.
