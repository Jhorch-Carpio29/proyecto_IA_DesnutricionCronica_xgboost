# Catálogo Exhaustivo de Variables — Desnutrición Crónica Infantil (ENDES 2025, INEI)
## Prevención de Fuga de Información (Target Leakage), Causalidad Inversa y Selección para XGBoost

**Proyecto:** Predicción del Riesgo de Desnutrición Crónica Infantil (Talla para la Edad < -2 DE OMS) en Menores de 5 Años en el Perú  
**Fuente Oficial:** Instituto Nacional de Estadística e Informática (INEI) — Encuesta Demográfica y de Salud Familiar (ENDES 2025)  
**Población Objetivo:** Niños de 0 a 59 meses cumplidos con medición antropométrica válida en el hogar  
**Fecha de Elaboración:** Octubre 2026  

---

## 1. Criterios Metodológicos Adaptados a Desnutrición Crónica Infantil

A diferencia de la anemia infantil (que es una condición bioquímica transitoria dependiente del balance de hierro y eritropoyesis), la **desnutrición crónica infantil (retraso en el crecimiento lineal o *stunting*)** refleja la **acumulación de privaciones nutricionales, infecciones gastrointestinales/respiratorias recurrentes y enteropatía ambiental** durante la ventana crítica de los **primeros 1,000 días de vida** (desde la concepción hasta los 24 meses).

Para estructurar un modelo predictivo robusto, generalizable y defendible ante un comité académico o de salud pública, se aplican los siguientes seis principios rectores:

1. **Prevención Estricta de Fuga de Información (Target Leakage):**
   - Queda terminantemente prohibido el uso de `HC70` y `HW70` (que constituyen el objetivo directo).
   - Se prohíbe el uso de la **talla en centímetros** (`HC3`, `HW3`), de percentiles (`HC4`, `HW4`), desvíos estándar (`HC5`, `HW5`) y porcentajes de la mediana (`HC6`, `HW6`), ya que un árbol de decisión como XGBoost puede reconstruir matemáticamente el puntaje Z de talla/edad combinando talla, edad (`HC1`) y sexo (`HC27`).
   - Se excluyen por defecto los puntajes antropométricos Z concurrentes (`HC71` Peso/Edad, `HC72` Peso/Talla, `HC73` IMC), por tratarse de subrogados clínicos directos del estado nutricional que no estarían disponibles sin una evaluación antropométrica formal previa.

2. **Condición de Screening Comunitario (No Invasivo / Visita Domiciliaria):**
   - El objetivo operativo del modelo es apoyar a agentes comunitarios de salud, enfermeras del primer nivel y programas sociales (ej. Cuna Más, JUNTOS) en la identificación temprana de niños en alto riesgo de retardo estatural mediante **entrevista domiciliaria verbal**.
   - No se asume la tenencia de tallímetros de madera calibrados, balanzas pediátricas de precisión ni lancetas/hemoglobinómetros en el primer contacto comunitario de screening.

3. **Control Riguroso de Causalidad Inversa:**
   - En encuestas transversales como ENDES, las preguntas sobre medicamentos o tratamientos (ej. antibióticos para diarrea grave, jarabe terapéutico o atención de emergencia por falla de medro en `REC94`/`REC42`) pueden reflejar que el niño **ya fue diagnosticado** y tratado por su retardo estatural o emaciación.
   - Se excluyen las intervenciones terapéuticas reactivas y solo se preservan las medidas estrictamente preventivas (suplementación universal profiláctica materna, vacunas, transferencias condicionadas).

4. **Respeto al Diseño Muestral Complejo de la ENDES:**
   - La ENDES es una encuesta bietápica, probabilística y estratificada. Las variables `HV001` (conglomerado/PSU), `HV022` (estrato de muestreo) y `HV005` (factor de ponderación) deben preservarse intactas como **metadatos de muestreo**.
   - `HV001` debe emplearse como llave de agrupación en `StratifiedGroupKFold` para evitar fuga espacial entre niños del mismo vecindario o aldea.
   - `HV005` (dividido entre 1,000,000) debe integrarse como `sample_weight` en XGBoost para reflejar las probabilidades reales de selección poblacional.

5. **Tratamiento Nativo de NaNs Estructurales:**
   - Múltiples preguntas de la ENDES poseen filtros de pase condicionales (ej. duración de lactancia materna solo si el niño fue amamantado, preguntas de diarrea solo si tuvo síntomas).
   - Se aprovecha la capacidad nativa de XGBoost para aprender divisiones óptimas de valores nulos (`default_direction`), evitando imputaciones sintéticas artificiales (como media o mediana) que distorsionarían la estructura epidemiológica de la no aplicabilidad.

6. **Ajuste por Desbalance de Clase:**
   - Con una prevalencia nacional de desnutrición crónica en torno al 11.5%, la distribución positiva:negativa es de aproximadamente 1:7.7. Se documenta la configuración formal de `scale_pos_weight` y la optimización de métricas orientadas a clases minoritarias (PR-AUC, Recall y F1 con umbral calibrado).

---

## 2. Definición Exacta de la Variable Objetivo ($Y$) y su Construcción Paso a Paso

### 2.1 Criterio Internacional (OMS 2006)
De acuerdo con los estándares de crecimiento infantil de la Organización Mundial de la Salud (OMS 2006), adoptados oficialmente por el Ministerio de Salud del Perú (MINSA), la **desnutrición crónica infantil** se define formalmente como un **Puntaje Z de Talla para la Edad ($Z_{T/E}$) inferior a -2.00 Desviaciones Estándar** respecto a la población de referencia medianamente nutrida.

$$Y_i = \text{desnutricion\_cronica}_i = \begin{cases} 1, & \text{si } Z_{T/E} < -2.00 \text{ DE} \\ 0, & \text{si } Z_{T/E} \ge -2.00 \text{ DE} \end{cases}$$

### 2.2 Fuente Primaria en ENDES 2025: `HC70` en `RECH6`
En el archivo oficial `RECH6_2025.csv` (Cuestionario de Hogar: Niños menores de 5 años evaluados en antropometría y hemoglobina), la variable `HC70` almacena el puntaje Z de talla para la edad según la norma OMS, **expresado en centésimas de desviación estándar** (con dos decimales implícitos).
- Ejemplo: Un valor registrado de `-250` representa un Z-score de **-2.50 DE** (desnutrición crónica).
- Un valor registrado de `-180` representa un Z-score de **-1.80 DE** (eutrófico o sin retardo estatural severo).
- Por consiguiente, el umbral matemático de clasificación es exactamente **`HC70 < -200`**.

### 2.3 Protocolo de Limpieza y Depuración de Casos Inválidos
El diccionario oficial del INEI especifica códigos especiales de control antropométrico que deben ser **eliminados de la muestra analítica antes de definir el target**:
- `9996`: Altura/Talla fuera de rango biológico plausible según la OMS ($Z < -6.00$ DE o $Z > +6.00$ DE; error de instrumento o digitación).
- `9997`: Inconsistencia de fecha de nacimiento o medición.
- `9998`: Caso no medido (niño no presente, madre rechazó la medición o no fue encontrado en el hogar).
- Valores vacíos o `NaN` en `HC70`.

```python
# Algoritmo de Construcción del Target (Python / Pandas):
def construir_target_desnutricion(df_rech6):
    # 1. Descartar códigos de error antropométrico y no medidos
    filtro_validos = (
        df_rech6['HC70'].notna() &
        (~df_rech6['HC70'].isin([9996, 9997, 9998])) &
        (df_rech6['HC70'] >= -600) & (df_rech6['HC70'] <= 600) &
        (df_rech6['HC1'] >= 0) & (df_rech6['HC1'] <= 59)
    )
    df_clean = df_rech6[filtro_validos].copy()
    
    # 2. Asignar variable objetivo binaria (1 = Desnutrición Crónica, 0 = Sin desnutrición crónica)
    df_clean['desnutricion_cronica'] = (df_clean['HC70'] < -200).astype(int)
    return df_clean
```

### 2.4 Verificación Cruzada con `REC44` (`HW70`)
En el archivo `REC44_2025.csv` (Cuestionario Individual de Mujeres), la variable homóloga es `HW70`. Durante el control de calidad, se verifica que para los niños coincidentes por `HHID` y número de orden, se cumpla la paridad `HC70 == HW70`. `RECH6` se mantiene como la fuente canónica por abarcar la muestra censal de todos los niños del hogar.

### 2.5 Desbalance de Clase y Recomendaciones de Modelado
- **Prevalencia esperada:** ~11.5% a nivel nacional (con picos superiores al 25–30% en zonas rurales altoandinas y comunidades nativas de la Selva).
- **Ratio de desbalance:** ~1 caso positivo por cada 7.7 casos negativos.
- **Parametrización XGBoost:** Configurar `scale_pos_weight = 7.7` para penalizar los falsos negativos.
- **Métricas de Evaluación:** Prohibido evaluar únicamente con Accuracy o ROC-AUC por el sesgo de clase mayoritaria. Las métricas prioritarias son **PR-AUC (Área bajo la curva Precision-Recall)**, **Recall / Sensibilidad** (imprescindible para no perder niños desnutridos en screening) y **F1-Score calibrando el umbral de decisión**.
---

## 3. Resumen Ejecutivo del Inventario de Datos (23 Archivos Analizados)

| Módulo | Archivo CSV / PDF | Registros Estimados | Variables | Descripción Oficial del Módulo | Rol en el Proyecto |
|:---|:---|---:|---:|:---|:---|
| `1638` | `RECH6` | 19,298 | 43 | Evaluación antropométrica y hemoglobina en niños < 5 años | **NÚCLEO: TARGET + Niño en Hogar** |
| `1638` | `REC44` | 18,841 | 34 | Salud y antropometría de hijos en cuestionario individual | Auditoría / Verificación cruzada |
| `1638` | `RECH5` | 37,679 | 40 | Evaluación de mujeres de 15 a 49 años (antropometría y anemia) | **Madre: Talla, IMC y Estado Nutricional** |
| `1629` | `RECH0` | 37,331 | 44 | Características del hogar, geografía y diseño muestral | **Diseño Muestral + Geografía + Hogar** |
| `1629` | `RECH1` | 131,929 | 36 | Composición de miembros, parentesco y educación | **Estructura Familiar y Educación de Cuidadores** |
| `1629` | `RECH4` | 131,929 | 21 | Seguro de salud de los integrantes del hogar | **Seguro SIS / Acceso a Servicios** |
| `1629` | `RECHM` | 2,714 | 8 | Mortalidad general en el hogar en los últimos años | Descartado (>98% nulo) |
| `1630` | `RECH23` | 37,331 | 130 | Vivienda, agua, saneamiento y quintil de riqueza | **Agua JMP, Saneamiento, Piso y Riqueza** |
| `1633` | `REC41` | 18,841 | 147 | Embarazo, parto, puerperio y lactancia materna | **Controles Prenatales, Peso Nacer y Lactancia** |
| `1633` | `REC94` | 18,841 | 61 | Suplementación con micronutrientes y tratamientos | Complicaciones Perinatales / Causalidad Inversa |
| `1031` | `REC0111` | 37,679 | 104 | Datos sociodemográficos y reproductivos de la mujer (MEF) | **Edad Materna, Educación, Autonomía y Paridad** |
| `1031` | `REC91` | 37,679 | 343 | Etnicidad, lengua materna y educación ampliada de la madre | **Lengua Materna Indígena y Localización Fina** |
| `1036` | `DIT` | 18,841 | 63 | Desarrollo Infantil Temprano (hitos y estimulación) | **Estimulación Temprana y Entorno Seguro** |
| `1036` | `REC42` | 18,841 | 169 | Salud infantil: Diarrea (EDA), Infecciones (IRA) y Dieta 24h | **CAUSAS INMEDIATAS: Morbilidad y Diversidad Dieta** |
| `1036` | `REC43` | 18,841 | 168 | Registro oficial de vacunas infantiles del carné de salud | **Vacunación Completa: Rotavirus, Neumo, SPR** |
| `1036` | `REC95` | 18,841 | 315 | Controles CRED de crecimiento y salud infantil ampliada | **Adherencia a Controles CRED Infantiles** |
| `1041` | `Programas Sociales x Hogar` | 37,331 | 20 | Cobertura de programas sociales en el hogar (JUNTOS, etc.) | **Programas de Transferencia y Alimentación** |
| `1041` | `PS_COMEDOR` | 62,621 | 10 | Beneficiarios de Comedores Populares a nivel individual | Detalle de subsidio alimentario |
| `1041` | `PS_CUNAMAS_VISITA` | 110,715 | 10 | Acompañamiento a Familias (SAF) de Cuna Más | Cuidado integral y visitas domiciliarias |
| `1041` | `PS_QALIWARMA` | 828,981 | 11 | Programa de alimentación escolar Qali Warma | Alimentación preescolar |
| `1041` | `PS_TRABAJA` | 5,484 | 10 | Programa de empleo temporal Trabaja Perú | Ingreso familiar de emergencia |
| `1041` | `PS_VL VASO DE LECHE` | 394,989 | 10 | Programa municipal del Vaso de Leche (PVL) | Complemento lácteo municipal |
| `1041` | `PS_WAWAWASI` | 35,174 | 10 | Cuna Más Servicio de Cuidado Diurno (Wawa Wasi) | Cuidado diurno y raciones proteicas |

---

## 4. Catálogo Detallado por Archivo (Evaluación Exhaustiva de 1,807 Variables)

> En esta sección se clasifica **cada una de las variables oficiales** existentes en los 23 diccionarios. Se asigna una categoría formal de decisión y un motivo epidemiológico/metodológico específico adaptado a desnutrición crónica infantil.

### 📁 Archivo: `Diccionario - RECH6.pdf` — Módulo: `1638_anemia`
**Total de variables evaluadas:** 43

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Identificador relacional del hogar y número de orden del niño en el hogar. |
| 2 | `HHID` | Identificación Cuestionario Individual | **METADATO / LLAVE** | Identificador relacional del hogar y número de orden del niño en el hogar. |
| 3 | `HC0` | Número de orden en el hogar | **METADATO / LLAVE** | Identificador relacional del hogar y número de orden del niño en el hogar. |
| 4 | `HC1` | Edad en meses | **INCLUIR** | Edad del niño en meses (0 a 59). Factor biológico central del crecimiento lineal y acumulación del retraso estatural. |
| 5 | `HC2` | Peso en kilogramos (1 dec.) | **DUDOSA (CLÍNICA / PROXY)** | Peso en kg (balanza calibrada). Medición física concurrente; riesgo de fuga indirecta de masa corporal y rompe el enfoque no invasivo. |
| 6 | `HC3` | Altura en centímetros (1 dec.) | **EXCLUIR POR LEAKAGE** | Talla directa o tablas de percentiles/desvíos que permiten reconstruir el puntaje Z de talla/edad con la edad del niño. |
| 7 | `HC4` | Talla/Edad percentil | **EXCLUIR POR LEAKAGE** | Talla directa o tablas de percentiles/desvíos que permiten reconstruir el puntaje Z de talla/edad con la edad del niño. |
| 8 | `HC5` | Talla/Edad Desviación Estándar | **EXCLUIR POR LEAKAGE** | Talla directa o tablas de percentiles/desvíos que permiten reconstruir el puntaje Z de talla/edad con la edad del niño. |
| 9 | `HC6` | Talla/Edad porcentaje de la mediana de referencia | **EXCLUIR POR LEAKAGE** | Talla directa o tablas de percentiles/desvíos que permiten reconstruir el puntaje Z de talla/edad con la edad del niño. |
| 10 | `HC7` | Peso/Edad percentil | **EXCLUIR POR LEAKAGE** | Talla directa o tablas de percentiles/desvíos que permiten reconstruir el puntaje Z de talla/edad con la edad del niño. |
| 11 | `HC8` | Peso/Edad Desviación Estándar | **EXCLUIR POR LEAKAGE** | Talla directa o tablas de percentiles/desvíos que permiten reconstruir el puntaje Z de talla/edad con la edad del niño. |
| 12 | `HC9` | Peso/Edad porcentaje de la mediana de referencia | **EXCLUIR POR LEAKAGE** | Talla directa o tablas de percentiles/desvíos que permiten reconstruir el puntaje Z de talla/edad con la edad del niño. |
| 13 | `HC10` | Peso/Talla percentil | **EXCLUIR POR LEAKAGE** | Talla directa o tablas de percentiles/desvíos que permiten reconstruir el puntaje Z de talla/edad con la edad del niño. |
| 14 | `HC11` | Peso/Talla Desviación Estándar | **EXCLUIR POR LEAKAGE** | Talla directa o tablas de percentiles/desvíos que permiten reconstruir el puntaje Z de talla/edad con la edad del niño. |
| 15 | `HC12` | Peso/Talla Porcentaje de la mediana de referencia | **EXCLUIR POR LEAKAGE** | Talla directa o tablas de percentiles/desvíos que permiten reconstruir el puntaje Z de talla/edad con la edad del niño. |
| 16 | `HC13` | Razón por la cual el niño no se midió | **EXCLUIR POR LEAKAGE / OPERATIVA** | Control operativo de medición antropométrica (si se midió acostado o de pie según talla < 85cm o razón de no medición). |
| 17 | `HC15` | El niño se midió acostado o de pie | **EXCLUIR POR LEAKAGE / OPERATIVA** | Control operativo de medición antropométrica (si se midió acostado o de pie según talla < 85cm o razón de no medición). |
| 18 | `HC16` | Día de nacimiento del niño | **EXCLUIR POR IRRELEVANCIA** | Variable administrativa, fecha de visita de campo, código de muestra o consentimiento operativo sin valor predictivo. |
| 19 | `HC19` | Año de la medición | **EXCLUIR POR IRRELEVANCIA** | Variable administrativa, fecha de visita de campo, código de muestra o consentimiento operativo sin valor predictivo. |
| 20 | `HC27` | Sexo | **INCLUIR** | Sexo del niño (1: Hombre, 2: Mujer). Dimorfismo biológico en velocidades de maduración y requerimientos nutricionales. |
| 21 | `HC30` | Mes de nacimiento del niño | **EXCLUIR POR IRRELEVANCIA** | Variable administrativa, fecha de visita de campo, código de muestra o consentimiento operativo sin valor predictivo. |
| 22 | `HC31` | Año de nacimiento del niño | **EXCLUIR POR IRRELEVANCIA** | Variable administrativa, fecha de visita de campo, código de muestra o consentimiento operativo sin valor predictivo. |
| 23 | `HC32` | Fecha de nacimiento (cmc) | **EXCLUIR POR IRRELEVANCIA** | Variable administrativa, fecha de visita de campo, código de muestra o consentimiento operativo sin valor predictivo. |
| 24 | `HC33` | Fecha de información completa | **EXCLUIR POR IRRELEVANCIA** | Variable administrativa, fecha de visita de campo, código de muestra o consentimiento operativo sin valor predictivo. |
| 25 | `HC51` | Número de orden del padre o responsable | **EXCLUIR POR IRRELEVANCIA** | Variable administrativa, fecha de visita de campo, código de muestra o consentimiento operativo sin valor predictivo. |
| 26 | `HC52` | Leyó la declaración de consentimiento | **EXCLUIR POR IRRELEVANCIA** | Variable administrativa, fecha de visita de campo, código de muestra o consentimiento operativo sin valor predictivo. |
| 27 | `HC53` | Nivel de hemoglobina (g/dl-1 decimal) | **DUDOSA (BIOMARCADOR CONCURRENTE)** | Medición de hemoglobina y anemia infantil. Concurrente e invasiva (punción capilar). Evaluar modelo no invasivo vs. clínico. |
| 28 | `HC55` | Resultado de medir (hemoglobina) | **EXCLUIR POR IRRELEVANCIA** | Variable administrativa, fecha de visita de campo, código de muestra o consentimiento operativo sin valor predictivo. |
| 29 | `HC56` | Nivel de hemoglobina ajustado por altitud (g/dl-1 decimal) RM 363-2022-MINSA | **DUDOSA (BIOMARCADOR CONCURRENTE)** | Medición de hemoglobina y anemia infantil. Concurrente e invasiva (punción capilar). Evaluar modelo no invasivo vs. clínico. |
| 30 | `HC56A` | Nivel de hemoglobina ajustada por altitud en g/dl - 1 decimal NUEVA DIRECTRIZ OMS<br>2024/RM 251-2024-MINSA | **DUDOSA (BIOMARCADOR CONCURRENTE)** | Medición de hemoglobina y anemia infantil. Concurrente e invasiva (punción capilar). Evaluar modelo no invasivo vs. clínico. |
| 31 | `HC57` | Nivel de anemia RM 363-2022-MINSA | **DUDOSA (BIOMARCADOR CONCURRENTE)** | Medición de hemoglobina y anemia infantil. Concurrente e invasiva (punción capilar). Evaluar modelo no invasivo vs. clínico. |
| 32 | `HC57A` | Nivel de Anemia NUEVA DIRECTRIZ OMS 2024/RM 251-2024-MINSA | **DUDOSA (BIOMARCADOR CONCURRENTE)** | Medición de hemoglobina y anemia infantil. Concurrente e invasiva (punción capilar). Evaluar modelo no invasivo vs. clínico. |
| 33 | `HC58` | Está de acuerdo con enviar los datos a un especialista | **EXCLUIR POR IRRELEVANCIA** | Variable administrativa, fecha de visita de campo, código de muestra o consentimiento operativo sin valor predictivo. |
| 34 | `HC60` | Número de orden de la madre en el hogar | **METADATO / LLAVE** | Número de orden de la madre en el hogar. Llave relacional imprescindible para cruce con registros maternos. |
| 35 | `HC61` | El nivel educativo más alto de la madre | **INCLUIR** | Nivel educativo y años de estudio de la madre reportados en el cuestionario de hogar. Fuerte determinante socioeconómico. |
| 36 | `HC62` | El año más alto de educación de la madre | **EXCLUIR POR IRRELEVANCIA** | Variable administrativa, fecha de visita de campo, código de muestra o consentimiento operativo sin valor predictivo. |
| 37 | `HC63` | Intervalo de los nacimientos anteriores al niño | **EXCLUIR POR IRRELEVANCIA** | Variable administrativa, fecha de visita de campo, código de muestra o consentimiento operativo sin valor predictivo. |
| 38 | `HC64` | Número de orden de nacimiento | **EXCLUIR POR IRRELEVANCIA** | Variable administrativa, fecha de visita de campo, código de muestra o consentimiento operativo sin valor predictivo. |
| 39 | `HC68` | Nivel educativo más alto (CS para informe preliminar y final) | **INCLUIR** | Nivel educativo y años de estudio de la madre reportados en el cuestionario de hogar. Fuerte determinante socioeconómico. |
| 40 | `HC70` | Talla/Edad de la Desviación Estándar de la mediana de referencia (según la OMS) | **VARIABLE OBJETIVO (TARGET)** | Variable objetivo (Y): Talla/Edad Z-score OMS (< -200 centésimas = 1, >= -200 = 0). Excluida de predictores. |
| 41 | `HC71` | Peso/Edad de la Desviación Estándar de la mediana de referencia (según la OMS) | **EXCLUIR POR LEAKAGE (PROXY TARGET)** | Puntajes antropométricos Z (Peso/Edad, Peso/Talla, IMC) calculados post-medición. Fuga directa y redundancia con estado nutricional. |
| 42 | `HC72` | Peso/Talla Desviación Estándar de la mediana de referencia (según la OMS) | **EXCLUIR POR LEAKAGE (PROXY TARGET)** | Puntajes antropométricos Z (Peso/Edad, Peso/Talla, IMC) calculados post-medición. Fuga directa y redundancia con estado nutricional. |
| 43 | `HC73` | Desviación Estándar del IMC (según la OMS) | **EXCLUIR POR LEAKAGE (PROXY TARGET)** | Puntajes antropométricos Z (Peso/Edad, Peso/Talla, IMC) calculados post-medición. Fuga directa y redundancia con estado nutricional. |


### 📁 Archivo: `Diccionario - REC44.pdf` — Módulo: `1638_anemia`
**Total de variables evaluadas:** 34

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Llave relacional de la madre y orden de nacimiento del niño en el cuestionario individual. |
| 2 | `CASEID` | Identificación de caso | **METADATO / LLAVE** | Llave relacional de la madre y orden de nacimiento del niño en el cuestionario individual. |
| 3 | `HWIDX` | Número de orden de la historia del nacimiento | **METADATO / LLAVE** | Llave relacional de la madre y orden de nacimiento del niño en el cuestionario individual. |
| 4 | `HW1` | Edad en meses | **INCLUIR** | Edad del niño en meses (homólogo a HC1 en cuestionario individual). |
| 5 | `HW2` | Peso en kilogramos (1 decimal) | **DUDOSA (CLÍNICA / PROXY)** | Peso del niño en kilogramos con 1 decimal. Medición clínica con balanza. |
| 6 | `HW3` | Talla en centímetros (1 decimal) | **EXCLUIR POR LEAKAGE** | Antropometría del niño (talla, percentiles, desviaciones estándar, peso/talla). Reconstruye directamente el target. |
| 7 | `HW4` | Talla/Edad percentil | **EXCLUIR POR LEAKAGE** | Antropometría del niño (talla, percentiles, desviaciones estándar, peso/talla). Reconstruye directamente el target. |
| 8 | `HW5` | Talla/Edad de las Desviación Estándar de la mediana de referencia | **EXCLUIR POR LEAKAGE** | Antropometría del niño (talla, percentiles, desviaciones estándar, peso/talla). Reconstruye directamente el target. |
| 9 | `HW6` | Talla/Edad porcentaje de la mediana de referencia | **EXCLUIR POR LEAKAGE** | Antropometría del niño (talla, percentiles, desviaciones estándar, peso/talla). Reconstruye directamente el target. |
| 10 | `HW7` | Peso/Edad percentil | **EXCLUIR POR LEAKAGE** | Antropometría del niño (talla, percentiles, desviaciones estándar, peso/talla). Reconstruye directamente el target. |
| 11 | `HW8` | Peso/Edad Desviación Estándar de la mediana de referencia | **EXCLUIR POR LEAKAGE** | Antropometría del niño (talla, percentiles, desviaciones estándar, peso/talla). Reconstruye directamente el target. |
| 12 | `HW9` | Peso/Edad porcentaje de la mediana de referencia | **EXCLUIR POR LEAKAGE** | Antropometría del niño (talla, percentiles, desviaciones estándar, peso/talla). Reconstruye directamente el target. |
| 13 | `HW10` | Peso/Talla percentil | **EXCLUIR POR LEAKAGE** | Antropometría del niño (talla, percentiles, desviaciones estándar, peso/talla). Reconstruye directamente el target. |
| 14 | `HW11` | Peso/Talla Desviación Estándar de la mediana de referencia | **EXCLUIR POR LEAKAGE** | Antropometría del niño (talla, percentiles, desviaciones estándar, peso/talla). Reconstruye directamente el target. |
| 15 | `HW12` | Peso/Talla porcentaje de la mediana de referencia | **EXCLUIR POR LEAKAGE** | Antropometría del niño (talla, percentiles, desviaciones estándar, peso/talla). Reconstruye directamente el target. |
| 16 | `HW13` | Razón por la cual el niño no se midió | **EXCLUIR POR LEAKAGE / OPERATIVA** | Procedimiento de medición física (acostado/de pie o razón de no medición). |
| 17 | `HW15` | El niño se midió acostado o de pie | **EXCLUIR POR LEAKAGE / OPERATIVA** | Procedimiento de medición física (acostado/de pie o razón de no medición). |
| 18 | `HW16` | Día de nacimiento del niño | **EXCLUIR POR IRRELEVANCIA** | Datos de control de campo, fechas administrativas y consentimientos operativos. |
| 19 | `HW17` | Día de la medición | **EXCLUIR POR IRRELEVANCIA** | Datos de control de campo, fechas administrativas y consentimientos operativos. |
| 20 | `HW18` | Mes de la medición | **EXCLUIR POR IRRELEVANCIA** | Datos de control de campo, fechas administrativas y consentimientos operativos. |
| 21 | `HW19` | Año de la medición | **EXCLUIR POR IRRELEVANCIA** | Datos de control de campo, fechas administrativas y consentimientos operativos. |
| 22 | `HW51` | Número de orden del padre o responsable | **EXCLUIR POR IRRELEVANCIA** | Datos de control de campo, fechas administrativas y consentimientos operativos. |
| 23 | `HW52` | Leyó la declaración de consentimiento para la medición de hemoglobina | **EXCLUIR POR IRRELEVANCIA** | Datos de control de campo, fechas administrativas y consentimientos operativos. |
| 24 | `HW53` | Nivel de hemoglobina (g /dl -1 decimal) | **DUDOSA (BIOMARCADOR CONCURRENTE)** | Hemoglobina y anemia en cuestionario individual. Procedimiento clínico concurrente. |
| 25 | `HW55` | Resultado de la medición (Hemoglobina) | **EXCLUIR POR IRRELEVANCIA** | Datos de control de campo, fechas administrativas y consentimientos operativos. |
| 26 | `HW56` | Nivel de hemoglobina ajustada por altitud en g/dl - 1 decimal RM 363-2022-MINSA | **DUDOSA (BIOMARCADOR CONCURRENTE)** | Hemoglobina y anemia en cuestionario individual. Procedimiento clínico concurrente. |
| 27 | `HW56A` | Nivel de hemoglobina ajustada por altitud en g/dl - 1 decimal NUEVA DIRECTRIZ OMS<br>2024/RM 251-2024-MINSA | **DUDOSA (BIOMARCADOR CONCURRENTE)** | Hemoglobina y anemia en cuestionario individual. Procedimiento clínico concurrente. |
| 28 | `HW57` | Nivel de anemia RM 363-2022-MINSA | **DUDOSA (BIOMARCADOR CONCURRENTE)** | Hemoglobina y anemia en cuestionario individual. Procedimiento clínico concurrente. |
| 29 | `HW57A` | Nivel de Anemia NUEVA DIRECTRIZ OMS 2024/RM 251-2024-MINSA | **DUDOSA (BIOMARCADOR CONCURRENTE)** | Hemoglobina y anemia en cuestionario individual. Procedimiento clínico concurrente. |
| 30 | `HW58` | Está de acuerdocon enviar los datos a un especialista | **EXCLUIR POR IRRELEVANCIA** | Datos de control de campo, fechas administrativas y consentimientos operativos. |
| 31 | `HW70` | Talla/Edad de la Desviación Estándar de la mediana de referencia (según la OMS) | **VARIABLE OBJETIVO (TARGET SECUNDARIO)** | Puntaje Z Talla/Edad OMS en cuestionario individual. Usado como verificación cruzada del target; excluido de X. |
| 32 | `HW71` | Peso/Edad de la Desviación Estándar de la mediana de referencia (según la OMS) | **EXCLUIR POR LEAKAGE** | Antropometría del niño (talla, percentiles, desviaciones estándar, peso/talla). Reconstruye directamente el target. |
| 33 | `HW72` | Peso/Talla Desviación Estándar de la mediana de referencia (según la OMS) | **EXCLUIR POR LEAKAGE** | Antropometría del niño (talla, percentiles, desviaciones estándar, peso/talla). Reconstruye directamente el target. |
| 34 | `HW73` | Desviación Estándar del IMC (según la OMS) | **EXCLUIR POR LEAKAGE** | Antropometría del niño (talla, percentiles, desviaciones estándar, peso/talla). Reconstruye directamente el target. |


### 📁 Archivo: `Diccionario - RECH5.pdf` — Módulo: `1638_anemia`
**Total de variables evaluadas:** 40

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Identificador del hogar y número de orden de la mujer en el hogar (cruza con HC60 de RECH6). |
| 2 | `HHID` | Identificación de caso | **METADATO / LLAVE** | Identificador del hogar y número de orden de la mujer en el hogar (cruza con HC60 de RECH6). |
| 3 | `HA0` | Número de orden en el hogar | **METADATO / LLAVE** | Identificador del hogar y número de orden de la mujer en el hogar (cruza con HC60 de RECH6). |
| 4 | `HA1` | Edad de la mujer en años | **EXCLUIR POR IRRELEVANCIA** | Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos. |
| 5 | `HA2` | Peso en kilogramos (1 decimal) | **INCLUIR** | Peso de la madre en kilogramos. Evalúa reserva energética y estado nutricional de la madre. |
| 6 | `HA3` | Talla en centímetros (1 decimal) | **INCLUIR** | Talla de la madre en centímetros con 1 decimal. La talla baja materna (< 150 cm) es uno de los determinantes biológicos y epigenéticos más potentes del retardo estatural del niño. |
| 7 | `HA4` | Talla/Edad percentil en que se encuentra | **EXCLUIR POR IRRELEVANCIA / REDUNDANCIA** | Percentiles y desvíos antropométricos de referencia de la mujer frente a estándares adultos ya sintetizados en el IMC (HA40). |
| 8 | `HA5` | Talla/Edad Desviación Estándar | **EXCLUIR POR IRRELEVANCIA / REDUNDANCIA** | Percentiles y desvíos antropométricos de referencia de la mujer frente a estándares adultos ya sintetizados en el IMC (HA40). |
| 9 | `HA6` | Talla/Edad porcentaje respecto a la mediana de referencia | **EXCLUIR POR IRRELEVANCIA / REDUNDANCIA** | Percentiles y desvíos antropométricos de referencia de la mujer frente a estándares adultos ya sintetizados en el IMC (HA40). |
| 10 | `HA11` | Peso/Talla desvio estándar (DHS) | **EXCLUIR POR IRRELEVANCIA / REDUNDANCIA** | Percentiles y desvíos antropométricos de referencia de la mujer frente a estándares adultos ya sintetizados en el IMC (HA40). |
| 11 | `HA12` | Peso/Talla Porcentaje respecto a la mediana (DHS) | **EXCLUIR POR IRRELEVANCIA / REDUNDANCIA** | Percentiles y desvíos antropométricos de referencia de la mujer frente a estándares adultos ya sintetizados en el IMC (HA40). |
| 12 | `HA12A` | Peso/Talla Porcentaje respecto a la mediana (Foggarty) | **EXCLUIR POR IRRELEVANCIA / REDUNDANCIA** | Percentiles y desvíos antropométricos de referencia de la mujer frente a estándares adultos ya sintetizados en el IMC (HA40). |
| 13 | `HA12B` | Peso/Talla Porcentaje respecto a la mediana (OMS) | **EXCLUIR POR IRRELEVANCIA / REDUNDANCIA** | Percentiles y desvíos antropométricos de referencia de la mujer frente a estándares adultos ya sintetizados en el IMC (HA40). |
| 14 | `HA13` | Resultado de medición de la entrevistada | **EXCLUIR POR IRRELEVANCIA** | Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos. |
| 15 | `HA32` | Fecha de nacimiento (cmc) | **EXCLUIR POR IRRELEVANCIA** | Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos. |
| 16 | `HA33` | Fecha de información completa | **EXCLUIR POR IRRELEVANCIA** | Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos. |
| 17 | `HA35` | En las últimas 24 horas cuantos cigarrillos fumó Ud. | **EXCLUIR POR IRRELEVANCIA** | Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos. |
| 18 | `HA40` | Índice de Masa Corporal para la entrevistada | **INCLUIR** | Índice de Masa Corporal (IMC) e Índice de Rohrer de la madre. Bajo peso materno (IMC < 18.5) se asocia directamente a desnutrición crónica infantil. |
| 19 | `HA41` | Índice de Rohrer para la entrevistada | **INCLUIR** | Índice de Masa Corporal (IMC) e Índice de Rohrer de la madre. Bajo peso materno (IMC < 18.5) se asocia directamente a desnutrición crónica infantil. |
| 20 | `HA50` | Grupos de mujeres de 12 a 49 años de edad | **EXCLUIR POR IRRELEVANCIA** | Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos. |
| 21 | `HA51` | Número de orden del padre o responsable | **EXCLUIR POR IRRELEVANCIA** | Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos. |
| 22 | `HA52` | Leyó la declaración de consentimiento para la medición de hemoglobina | **EXCLUIR POR IRRELEVANCIA** | Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos. |
| 23 | `HA53` | Nivel de hemoglobina (g/dl - 1 decimal) | **DUDOSA (BIOMARCADOR CONCURRENTE)** | Nivel de hemoglobina y anemia de la madre. Puede incluirse como proxy de calidad nutricional y reservas biológicas maternas, pero requiere punción capilar. |
| 24 | `HA54` | Actualmente embarazada | **EXCLUIR POR IRRELEVANCIA** | Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos. |
| 25 | `HA55` | Resultado de la medición (hemoglobina) | **EXCLUIR POR IRRELEVANCIA** | Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos. |
| 26 | `HA56` | Nivel de hemoglobina ajustado por la altitud (g/dl - 1 decimal) RM 363-2022-MINSA | **DUDOSA (BIOMARCADOR CONCURRENTE)** | Nivel de hemoglobina y anemia de la madre. Puede incluirse como proxy de calidad nutricional y reservas biológicas maternas, pero requiere punción capilar. |
| 27 | `HA56A` | Nivel de hemoglobina ajustada por altitud en g/dl - 1 decimal NUEVA DIRECTRIZ OMS<br>2024/RM 251-2024-MINSA | **DUDOSA (BIOMARCADOR CONCURRENTE)** | Nivel de hemoglobina y anemia de la madre. Puede incluirse como proxy de calidad nutricional y reservas biológicas maternas, pero requiere punción capilar. |
| 28 | `HA57` | Nivel de anemia RM 363-2022-MINSA | **DUDOSA (BIOMARCADOR CONCURRENTE)** | Nivel de hemoglobina y anemia de la madre. Puede incluirse como proxy de calidad nutricional y reservas biológicas maternas, pero requiere punción capilar. |
| 29 | `HA57A` | Nivel de Anemia NUEVA DIRECTRIZ OMS 2024/RM 251-2024-MINSA | **DUDOSA (BIOMARCADOR CONCURRENTE)** | Nivel de hemoglobina y anemia de la madre. Puede incluirse como proxy de calidad nutricional y reservas biológicas maternas, pero requiere punción capilar. |
| 30 | `HA58` | Está de acuerdo con enviar los datos a un especialista | **EXCLUIR POR IRRELEVANCIA** | Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos. |
| 31 | `HA60` | Estado civil | **EXCLUIR POR IRRELEVANCIA** | Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos. |
| 32 | `HA61` | Lea la declaración de consentimiento (VIH) | **EXCLUIR POR IRRELEVANCIA** | Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos. |
| 33 | `HA62` | Número de identificación de la muestra de sangre | **EXCLUIR POR IRRELEVANCIA** | Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos. |
| 34 | `HA63` | Resultado de la medición (VIH) | **EXCLUIR POR IRRELEVANCIA** | Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos. |
| 35 | `HA64` | Consentimiento para pruebas adicionales | **EXCLUIR POR IRRELEVANCIA** | Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos. |
| 36 | `HA65` | Resultado de la entrevista individual a la mujer | **EXCLUIR POR IRRELEVANCIA** | Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos. |
| 37 | `HA66` | El nivel educativo más alto aprobado de la mujer | **INCLUIR** | Nivel educativo más alto aprobado y años de educación de la madre. Pilar de capital humano para el cuidado y alimentación del menor. |
| 38 | `HA67` | El año más alto de educación de la mujer | **INCLUIR** | Nivel educativo más alto aprobado y años de educación de la madre. Pilar de capital humano para el cuidado y alimentación del menor. |
| 39 | `HA68` | Nivel educativo más alto (CS para el informe preliminar y final) | **INCLUIR** | Nivel educativo más alto aprobado y años de educación de la madre. Pilar de capital humano para el cuidado y alimentación del menor. |
| 40 | `HA69` | Peso del VIH (6 decimales) | **EXCLUIR POR IRRELEVANCIA** | Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos. |


### 📁 Archivo: `Diccionario - RECH0.pdf` — Módulo: `1629_hogar`
**Total de variables evaluadas:** 44

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Identificador maestro del hogar para unión con todos los módulos. |
| 2 | `HHID` | Identificacion Cuestionario del Hogar | **METADATO / LLAVE** | Identificador maestro del hogar para unión con todos los módulos. |
| 3 | `HV000` | Código del país | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 4 | `HV001` | Conglomerado | **METADATO DEL DISEÑO MUESTRAL** | Conglomerado, estrato y unidades de muestreo complejo. Imprescindibles para GroupKFold y validación sin fuga espacial. |
| 5 | `HV002` | Vivienda | **METADATO DEL DISEÑO MUESTRAL** | Conglomerado, estrato y unidades de muestreo complejo. Imprescindibles para GroupKFold y validación sin fuga espacial. |
| 6 | `HV002A` | Hogar | **METADATO DEL DISEÑO MUESTRAL** | Conglomerado, estrato y unidades de muestreo complejo. Imprescindibles para GroupKFold y validación sin fuga espacial. |
| 7 | `HV003` | Número de orden del Informante del cuestionario del hogar | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 8 | `HV004` | Unidad última de muestreo | **METADATO DEL DISEÑO MUESTRAL** | Conglomerado, estrato y unidades de muestreo complejo. Imprescindibles para GroupKFold y validación sin fuga espacial. |
| 9 | `HV007` | Año de entrevista | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 10 | `HV008` | Fecha de entrevista meses (CMC) | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 11 | `HV009` | Total de personas en el hogar | **INCLUIR** | Número total de personas en el hogar. Indicador de carga de dependencia familiar y hacinamiento potencial. |
| 12 | `HV010` | Número de mujeres elegibles para entrevista individual | **INCLUIR** | Número de mujeres elegibles en edad fértil en el hogar. Red de apoyo materno y capacidad de cuidado infantil. |
| 13 | `HV011` | Número de hombres elegibles por hogar | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 14 | `HV012` | Número de miembros de jure (residentes habituales) | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 15 | `HV013` | Número de miembros de facto (personas que durmieron la noche anterior) | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 16 | `HV014` | Número de niños menores de 5 años | **INCLUIR** | Número de niños menores de 5 años en el hogar. Competencia directa por atención, lactancia y raciones nutricionales. |
| 17 | `HV015` | Resultado de la entrevista en el hogar | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 18 | `HV017` | Número de visitas | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 19 | `HV020` | Muestra de alguna vez en union | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 20 | `HV021` | Unidad de muestreo primario (conglomerado) | **METADATO DEL DISEÑO MUESTRAL** | Conglomerado, estrato y unidades de muestreo complejo. Imprescindibles para GroupKFold y validación sin fuga espacial. |
| 21 | `HV023` | Dominio | **INCLUIR** | Dominio geográfico de residencia (Costa, Sierra, Selva, Lima). Patrones agroecológicos y epidemiológicos. |
| 22 | `HV024` | Región | **INCLUIR** | Departamento de residencia (1 a 25). Captura brechas estructurales de desarrollo regional y servicios de salud. |
| 23 | `HV025` | Área de residencia | **INCLUIR** | Área de residencia (1: Urbano, 2: Rural). Una de las brechas más críticas en desnutrición crónica infantil en el Perú. |
| 24 | `HV026` | Lugar de residencia | **INCLUIR** | Tipo de lugar de residencia (Capital, gran ciudad, ciudad pequeña, pueblo, campo). |
| 25 | `HV027` | Selección para hombre/esposo | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 26 | `HV028` | Peso de muestra masculino | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 27 | `HV030` | Supervisor de campo | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 28 | `HV031` | Editor de campo | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 29 | `HV032` | Editor de la oficina | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 30 | `HV033` | Ultimate area selection prob. | **EXCLUIR POR IRRELEVANCIA** | Variable operativa, de control de campo o sin sustento explicativo. |
| 31 | `HV035` | Número de niños elegibles para altura y peso | **INCLUIR** | Número de mujeres de 15 a 49 años en el hogar. |
| 32 | `HV040` | Altitud del conglomerado en metros | **INCLUIR** | Altitud del conglomerado en msnm. Fuerte asociación fisiológica con retardo estatural andino y ruralidad extrema. |
| 33 | `HV041` | Número de mujeres con medición de peso y talla | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 34 | `HV042` | Selección para medición de hemoglobina | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 35 | `HV043` | Hogares seleccionados para el módulo de mujeres de estado | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 36 | `HV044` | Selección para el módulo de violencia familiar | **EXCLUIR POR IRRELEVANCIA** | Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo. |
| 37 | `UBIGEO` | Código de Ubicación Gegráfica | **EXCLUIR POR IRRELEVANCIA** | Variable operativa, de control de campo o sin sustento explicativo. |
| 38 | `HV005` | Factor de ponderación | **METADATO DEL DISEÑO MUESTRAL** | Factor de ponderación muestral del hogar (dividir entre 1,000,000 para obtener el peso expandido insesgado / sample_weight). |
| 39 | `HV022` | Estrato | **METADATO DEL DISEÑO MUESTRAL** | Conglomerado, estrato y unidades de muestreo complejo. Imprescindibles para GroupKFold y validación sin fuga espacial. |
| 40 | `NCONGLOME` | Número de Conglomerado (proveniente del marco) | **EXCLUIR POR IRRELEVANCIA** | Variable operativa, de control de campo o sin sustento explicativo. |
| 41 | `CODCCPP` | Codigo de Centro Poblado | **EXCLUIR POR IRRELEVANCIA** | Variable operativa, de control de campo o sin sustento explicativo. |
| 42 | `NOMCCPP` | Nombre del Centro Poblado | **EXCLUIR POR IRRELEVANCIA** | Variable operativa, de control de campo o sin sustento explicativo. |
| 43 | `LONGITUDX` | Longitud del conglomerado | **EXCLUIR POR IRRELEVANCIA** | Variable operativa, de control de campo o sin sustento explicativo. |
| 44 | `LATITUDY` | Latitud del conglomerado | **EXCLUIR POR IRRELEVANCIA** | Variable operativa, de control de campo o sin sustento explicativo. |


### 📁 Archivo: `Diccionario - RECH1.pdf` — Módulo: `1629_hogar`
**Total de variables evaluadas:** 36

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Identificador del hogar y número de orden de cada miembro del hogar. |
| 2 | `HHID` | Identificación Cuestionario del Hogar | **METADATO / LLAVE** | Identificador del hogar y número de orden de cada miembro del hogar. |
| 3 | `HVIDX` | Número de orden | **METADATO / LLAVE** | Identificador del hogar y número de orden de cada miembro del hogar. |
| 4 | `HV101` | Relación de parentesco con el jefe del hogar | **INCLUIR** | Parentesco con el jefe del hogar (hijo, nieto, etc.). Estructura familiar y posición del niño. |
| 5 | `HV102` | ¿Vive habitualmente aquí? | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 6 | `HV103` | ¿Durmió aquí anoche? | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 7 | `HV104` | Sexo | **INCLUIR** | Sexo y edad de los miembros del hogar. Caracterización demográfica de los cuidadores. |
| 8 | `HV105` | Edad | **INCLUIR** | Sexo y edad de los miembros del hogar. Caracterización demográfica de los cuidadores. |
| 9 | `HV106` | ¿Cuál fue el nivel de estudios más alto que aprobó? | **INCLUIR** | Nivel educativo y años de estudio alcanzados por el jefe del hogar y cuidadores principales. |
| 10 | `HV107` | ¿Cuál fue el año o grado más alto que aprobó? | **INCLUIR** | Nivel educativo y años de estudio alcanzados por el jefe del hogar y cuidadores principales. |
| 11 | `HV108` | Número de años de estudio | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 12 | `HV109` | Nivel educativo alcanzado | **INCLUIR** | Nivel educativo y años de estudio alcanzados por el jefe del hogar y cuidadores principales. |
| 13 | `HV110` | Actualmente ¿Asiste a una escuela o colegio (un instituto superior o universidad)? | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 14 | `HV111` | ¿Está viva la madre natural? | **INCLUIR / LLAVE** | Madre viva en el hogar y número de orden de la madre en la cartilla. Fundamental para enlazar niño con registros maternos. |
| 15 | `HV112` | Número de orden de la madre | **INCLUIR / LLAVE** | Madre viva en el hogar y número de orden de la madre en la cartilla. Fundamental para enlazar niño con registros maternos. |
| 16 | `HV113` | ¿Está vivo el padre natural? | **INCLUIR / LLAVE** | Padre vivo en el hogar y número de orden del padre en el hogar. |
| 17 | `HV114` | Número de orden del padre | **INCLUIR / LLAVE** | Padre vivo en el hogar y número de orden del padre en el hogar. |
| 18 | `HV115` | ¿Cúal es su estado civil o conyugal? | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 19 | `HV116` | Acutalmente, anteriormente o nunca unida | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 20 | `HV117` | Elegibilidad para entrevista individual de mujeres | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 21 | `HV118` | Elegibilidad para entrevista de hombres | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 22 | `HV120` | Menores de 5 años para medición de peso/talla y hemoglobina | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 23 | `HV121` | ¿Asistió a una escuela o colegio? en algún momento durante el año actual | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 24 | `HV122` | ¿A qué nivel asiste o se matriculó? | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 25 | `HV123` | Año o grado que asiste o se matriculó | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 26 | `HV124` | Número de años de estudio al que asiste o se matriculó durante el año actual | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 27 | `HV125` | El año pasado ¿estuvo o matriculado en una escuela o colegio (un instituto superior o universidad) | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 28 | `HV126` | ¿A que nivel asistió o se matriculó el año pasado? | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 29 | `HV127` | Año o grado que asistió o se matriculó | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 30 | `HV128` | Número de años de estudio al que asiste o se matriculó el año pasado | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 31 | `HV129` | Condición de asistencia a una escuela, colegio, instituto superior o universidad | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 32 | `QH21A` | ¿Estudia en una escuela o colegio estatal? | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 33 | `QH25A` | ¿Cuál es su nacionalidad? | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 34 | `QH25B` | Vive permanentemente en el Perú | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 35 | `QH25CM` | Desde qué mes vive en el Perú | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |
| 36 | `QH25CA` | Desde qué año vive en el Perú | **EXCLUIR POR IRRELEVANCIA** | Control de residencia temporal/de facto o detalles operativos de entrevista. |


### 📁 Archivo: `Diccionario - RECH4.pdf` — Módulo: `1629_hogar`
**Total de variables evaluadas:** 21

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Llaves de identificación del hogar y número de línea de cada integrante. |
| 2 | `HHID` | Identificacion Cuestionario del Hogar | **METADATO / LLAVE** | Llaves de identificación del hogar y número de línea de cada integrante. |
| 3 | `IDXH4` | Número de orden del listado del hogar | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares de registro del seguro o códigos administrativos. |
| 4 | `SH11A` | Seguro de salud: ESSALUD/IPSS | **INCLUIR** | Afiliación al Seguro Integral de Salud (SIS). Subsidio estatal de controles CRED, vacunas y micronutrientes para población vulnerable. |
| 5<br>6 | `SH11B<br>SH11C` | Seguro de salud: Militar<br>Seguro de salud: Integral | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares de registro del seguro o códigos administrativos. |
| 7 | `SH11D` | Seguro de salud: Compañía de seguros | **INCLUIR** | Otras modalidades de seguro de salud (FFAA/Policial, Privado, Universitario, etc.). |
| 8 | `SH11E` | Seguro de salud: Seguro privado | **INCLUIR** | Otras modalidades de seguro de salud (FFAA/Policial, Privado, Universitario, etc.). |
| 9 | `SH11Y` | Seguro de salud: No sabe | **INCLUIR** | Otras modalidades de seguro de salud (FFAA/Policial, Privado, Universitario, etc.). |
| 10 | `SH11Z` | Seguro de salud: No tienen | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares de registro del seguro o códigos administrativos. |
| 11 | `SH12` | Alguno de los seguros está a su nombre | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares de registro del seguro o códigos administrativos. |
| 12 | `SH13` | Actividad de la ultima semana | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares de registro del seguro o códigos administrativos. |
| 13 | `SH15N` | Nivel de educación aprobado | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares de registro del seguro o códigos administrativos. |
| 14 | `SH15Y` | Nivel de educación en años | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares de registro del seguro o códigos administrativos. |
| 15 | `SH15G` | Nivel de educación en grados | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares de registro del seguro o códigos administrativos. |
| 16 | `SH18N` | Nivel de educación que actualmente asiste o se matriculó | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares de registro del seguro o códigos administrativos. |
| 17 | `SH18Y` | Año al que actualmente asiste o se matriculó | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares de registro del seguro o códigos administrativos. |
| 18 | `SH18G` | Grado al que actualmente asiste o se matriculó | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares de registro del seguro o códigos administrativos. |
| 19 | `SH20N` | Nivel educativo al que asistió el año pasado | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares de registro del seguro o códigos administrativos. |
| 20 | `SH20Y` | Año al que asistió el año pasado | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares de registro del seguro o códigos administrativos. |
| 21 | `SH20G` | Grado al que asistió el año pasado | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares de registro del seguro o códigos administrativos. |
| 22 | `SH21` | Resultado de la asistencia del año escolar pasado | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares de registro del seguro o códigos administrativos. |


### 📁 Archivo: `Diccionario - RECHM.pdf` — Módulo: `1629_hogar`
**Total de variables evaluadas:** 8

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Registro de defunciones en el hogar. Base extremadamente pequeña (2,714 filas en toda la ENDES, >98% nula para el universo de niños menores de 5 años). |
| 2 | `HHID` | Identificación del caso | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Registro de defunciones en el hogar. Base extremadamente pequeña (2,714 filas en toda la ENDES, >98% nula para el universo de niños menores de 5 años). |
| 3 | `NRO_ORDEN_ID` | Número de orden | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Registro de defunciones en el hogar. Base extremadamente pequeña (2,714 filas en toda la ENDES, >98% nula para el universo de niños menores de 5 años). |
| 4 | `QH30M` | Sexo | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Registro de defunciones en el hogar. Base extremadamente pequeña (2,714 filas en toda la ENDES, >98% nula para el universo de niños menores de 5 años). |
| 5 | `QH31M` | A qué edad murió | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Registro de defunciones en el hogar. Base extremadamente pequeña (2,714 filas en toda la ENDES, >98% nula para el universo de niños menores de 5 años). |
| 6 | `QH32M_M` | En qué mes murió | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Registro de defunciones en el hogar. Base extremadamente pequeña (2,714 filas en toda la ENDES, >98% nula para el universo de niños menores de 5 años). |
| 7 | `QH32M_Y` | En qué año murió | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Registro de defunciones en el hogar. Base extremadamente pequeña (2,714 filas en toda la ENDES, >98% nula para el universo de niños menores de 5 años). |
| 8 | `QH33M` | Murió por alguna causa relacionada con el embarazo, parto, sobreparto o por alguna otra causa | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Registro de defunciones en el hogar. Base extremadamente pequeña (2,714 filas en toda la ENDES, >98% nula para el universo de niños menores de 5 años). |


### 📁 Archivo: `Diccionario - RECH23.pdf` — Módulo: `1630_vivienda`
**Total de variables evaluadas:** 130

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Llave relacional para vincular la vivienda con el hogar y el niño. |
| 2 | `HHID` | Identificacion Cuestionario del Hogar | **METADATO / LLAVE** | Llave relacional para vincular la vivienda con el hogar y el niño. |
| 3 | `HV201` | ¿Cuál es la fuente principal de abastecimiento de agua para tomar o beber? | **INCLUIR** | Fuente principal de abastecimiento de agua para beber y uso general. Factor crítico de diarreas y enteropatía ambiental. |
| 4 | `HV202` | ¿Cuál es la fuente principal de abastecimiento de agua en su hogar? | **INCLUIR** | Fuente principal de abastecimiento de agua para beber y uso general. Factor crítico de diarreas y enteropatía ambiental. |
| 5 | `HV204` | ¿Cuánto tiempo se demora en ir, recoger agua y volver? | **INCLUIR** | Tiempo en minutos para ir, recoger agua y volver. Proxy de estrés hídrico y precariedad extrema de acceso. |
| 6 | `HV205` | ¿Qué tipo de servicio higiénico tiene su hogar? | **INCLUIR** | Tipo de servicio higiénico. Clasificación JMP OMS/UNICEF de saneamiento mejorado vs. no mejorado (clave en desnutrición). |
| 7 | `HV206` | ¿Tiene electricidad en su hogar? | **INCLUIR** | Disponibilidad de electricidad en la vivienda (0: No, 1: Sí). Permite refrigeración y conservación de alimentos. |
| 8 | `HV207` | Su hogar ¿tiene radio? | **INCLUIR** | Bienes del hogar (radio, televisor, refrigeradora, bicicleta, motocicleta, automóvil). Componentes del nivel socioeconómico. |
| 9 | `HV208` | Su hogar ¿tiene televisor? | **INCLUIR** | Bienes del hogar (radio, televisor, refrigeradora, bicicleta, motocicleta, automóvil). Componentes del nivel socioeconómico. |
| 10 | `HV209` | Su hogar ¿tiene refrigeradora /congeladora? | **INCLUIR** | Bienes del hogar (radio, televisor, refrigeradora, bicicleta, motocicleta, automóvil). Componentes del nivel socioeconómico. |
| 11 | `HV210` | Algún miembro de su hogar ¿tiene bicleta/triciclo? | **INCLUIR** | Bienes del hogar (radio, televisor, refrigeradora, bicicleta, motocicleta, automóvil). Componentes del nivel socioeconómico. |
| 12 | `HV211` | Algún miembro de su hogar ¿tiene motocileta/ motokar? | **INCLUIR** | Bienes del hogar (radio, televisor, refrigeradora, bicicleta, motocicleta, automóvil). Componentes del nivel socioeconómico. |
| 13 | `HV212` | Algún miembro de su hogar ¿tiene carro o camión? | **INCLUIR** | Bienes del hogar (radio, televisor, refrigeradora, bicicleta, motocicleta, automóvil). Componentes del nivel socioeconómico. |
| 14 | `HV213` | Material predominante del piso de la vivienda | **INCLUIR** | Material predominante del piso (tierra/arena = reservorio de parásitos y bacterias), paredes y techo de la vivienda. |
| 15 | `HV214` | Material predominante de las paredes exteriores de la vivienda | **INCLUIR** | Material predominante del piso (tierra/arena = reservorio de parásitos y bacterias), paredes y techo de la vivienda. |
| 16 | `HV215` | Material predominante del techo de la vivienda | **INCLUIR** | Material predominante del piso (tierra/arena = reservorio de parásitos y bacterias), paredes y techo de la vivienda. |
| 17 | `HV216` | Número de habitaciones utilizadas para dormir | **INCLUIR** | Número de habitaciones para dormir. Denominador obligatorio para calcular el índice de hacinamiento del hogar. |
| 18 | `HV217` | Estructura de relaciones en el hogar (composición de los hogares) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 19 | `HV218` | Número de orden del Jefe del hogar | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 20 | `HV219` | Sexo del jefe de hogar | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 21 | `HV220` | Edad del jefe de hogar | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 22 | `HV221` | Su hogar ¿tiene teléfono? | **INCLUIR** | Acceso a teléfono fijo, celular, computadora e internet en el hogar. Conectividad y alfabetismo informacional de la familia. |
| 23 | `HV225` | ¿El servicio higiénico es compartido con otros hogares? | **INCLUIR** | Comparte servicio higiénico con otros hogares (1: Sí, 0: No). Contaminación fecal cruzada y saneamiento no exclusivo. |
| 24 | `HV226` | ¿Cuál es el combustible que utilizan más frecuentemente en su hogar para cocinar? | **INCLUIR** | Tipo de combustible para cocinar (leña, carbón, bosta, gas). Contaminación del aire en interiores e infecciones respiratorias. |
| 25 | `HV227` | Tiene un mosquitero para dormir | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 26 | `HV228` | Los niños menores de 5 años durmieron bajo mosquiteros anoche | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 27 | `HV234` | Prueba de yodo para sal | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 28 | `HV235` | Ubicación de la fuente de agua | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 29 | `HV236` | Persona que a recoger agua para su hogar | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 30 | `HV237` | Hecho algo al agua para hacerla segura para beber | **INCLUIR** | Tratamiento del agua para beber (hervir, clorar, filtrar). Barrera higiénica contra enteropatógenos causantes de retardo de crecimiento. |
| 31 | `HV237A` | El agua usualmente es tratada por: hervida | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 32 | `HV237B` | El agua usualmente es tratada por: añadir lejía o cloro | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 33 | `HV237C` | El agua usualmente es tratada por: filtro a través de un paño | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 34 | `HV237D` | El agua usualmente es tratada por: uso de agua filtrada | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 35 | `HV237E` | El agua usualmente es tratada por: desinfección solar | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 36 | `HV237F` | El agua usualmente es tratada por: dejar reposar y asentarse | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 37 | `HV237G` | El agua usualmente es tratada por: CS - agua embotellada | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 38 | `HV237H` | El agua usualmente es tratada por: CS | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 39 | `HV237I` | El agua usualmente es tratada por: CS | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 40 | `HV237J` | El agua usualmente es tratada por: CS | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 41 | `HV237K` | El agua usualmente es tratada por: CS | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 42 | `HV237X` | El agua usualmente es tratada por: otros | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 43 | `HV237Z` | El agua usualmente es tratada por: no sabe | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 44 | `HV238` | Número de hogares que comparten el baño | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 45 | `HV239` | Comida cocinada en estufa o fuego abierto | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 46 | `HV240` | El hogar tiene una chimenea o una campana | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 47 | `HV241` | Comida preparada en la casa, en edificio separado o al aire libre | **INCLUIR** | Cocina en ambiente separado de los dormitorios (1: Sí, 0: No). Higiene en la preparación de alimentos del infante. |
| 48 | `HV242` | ¿Utilizan un cuarto especialmente para cocinar? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 49 | `HV243A` | ¿Tiene un teléfono móvil (celular)? | **INCLUIR** | Acceso a teléfono fijo, celular, computadora e internet en el hogar. Conectividad y alfabetismo informacional de la familia. |
| 50 | `HV243B` | Tiene un reloj | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 51 | `HV243C` | ¿Tiene un carreta jalada por animales? | **INCLUIR** | Acceso a teléfono fijo, celular, computadora e internet en el hogar. Conectividad y alfabetismo informacional de la familia. |
| 52 | `HV243D` | ¿Tiene un bote a motor? | **INCLUIR** | Acceso a teléfono fijo, celular, computadora e internet en el hogar. Conectividad y alfabetismo informacional de la familia. |
| 53 | `HV244` | ¿Algún miembro del hogar es dueño de tierras agrícolas? | **INCLUIR** | Tenencia de tierras agrícolas, hectáreas y tenencia de animales de cría. Autosuficiencia alimentaria y zoonosis. |
| 54 | `HV245` | ¿Cuántas hectáreas de tierras agrícolas le pertenecen? | **INCLUIR** | Tenencia de tierras agrícolas, hectáreas y tenencia de animales de cría. Autosuficiencia alimentaria y zoonosis. |
| 55 | `HV246` | ¿Algún miembro del hogar es dueño de ganadería, rebaños o animales de granja? | **INCLUIR** | Tenencia de tierras agrícolas, hectáreas y tenencia de animales de cría. Autosuficiencia alimentaria y zoonosis. |
| 56 | `HV246A` | Cantidad de: ganado | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 57 | `HV246B` | Cantidad de: vacas, toros | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 58 | `HV246C` | Cantidad de: caballos, burros, mulas | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 59 | `HV246D` | Cantidad de: cabras | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 60 | `HV246E` | Cantidad de: ovejas | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 61 | `HV246F` | Cantidad de: pollos | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 62 | `HV246G` | Cantidad de: aves de corral | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 63 | `HV246H` | Cantidad de: cuyes/conejos | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 64 | `HV246I` | Cantidad de: cerdos | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 65 | `HV246J` | Cantidad de: otros | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 66 | `HV246K` | CS propio | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 67 | `HV247` | Posee una cuenta bancaria | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 68 | `HV248` | Número de personas enfermas 18-59 | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 69 | `HV249` | Miembro de la HH fallecido los últimos 12 meses | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 70 | `HV250` | Número de miembros que murieron en los últimos 12 meses | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 71 | `HV251` | Número de huérfanos y niños vulnerables | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 72 | `HML1` | Número de mosquiteros | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 73 | `HML1A` | Número de mosquiteros con información específica | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 74 | `HML2` | Número de niños menores de edad en la noche anterior | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 75 | `SHVER` | Versión del cuestionario | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 76 | `SHREGION` | Región natural | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 77 | `SHSEMES` | Semestre | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 78 | `SHPROVIN` | Provincia | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 79 | `SHDISTRI` | Distrito | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 80 | `SHTOTH` | Total de hogares en la vivienda | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 81 | `SH42` | El abastecimiento de agua para beber está disponible todo el día | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 82 | `SH43` | Las últimas 2 semanas fueron interrumpidas por un día o más | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 83 | `SH48` | ¿Conserva en un envase o recipiente el agua para beber? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 84 | `SH49` | Tipo de envase o recipiente | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 85 | `SH50` | ¿Lo usa con tapa? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 86 | `SH51` | Pago por el agua? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 87 | `SH52` | Institución de pago de agua | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 88 | `SH56` | Con qué frecuencia se limpia el baño o la letrina? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 89 | `SH58` | Dónde tira la basura? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 90 | `SH59` | Con qué frecuencia se recoge la basura? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 91 | `SH60` | Antes de desechar la basura donde se almacena? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 92 | `SH61A` | ¿Tiene sofá? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 93 | `SH61B` | ¿Tiene vitrina/aparador? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 94 | `SH61C` | ¿Tiene repostero? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 95 | `SH61D` | ¿Tiene cómoda/ropero? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 96 | `SH61E` | ¿Tiene reloj de pared? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 97 | `SH61J` | ¿Tiene televisión por cable? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 98 | `SH61K` | ¿Tiene licuadora? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 99 | `SH61L` | ¿Tiene cocina de gas? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 100 | `SH61M` | ¿Tiene cocina de kerosene? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 101 | `SH61N` | ¿Tiene microondas? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 102 | `SH61O` | ¿Tiene lavadora? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 103 | `SH61P` | ¿Tiene computadora? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 104 | `SH61Q` | ¿Tiene acceso a Internet en casa? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 105 | `SH61R` | ¿Tiene bomba de agua? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 106 | `SH61S` | ¿Tiene generador de electricidad? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 107 | `SH63` | ¿Utiliza otro tipo de combustible para cocinar? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 108 | `SH64` | Otro tipo de combustible utilizado para cocinar | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 109 | `SH66` | ¿La cocina tiene una chimenea o un mecanismo para eliminar el humo? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 110 | `SH69` | El hogar compra combustible para cocinar? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 111 | `SH70` | ¿Qué tipo de alumbrado utiliza el hogar? | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 112 | `SH71` | Número de habitaciones en el hogar | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 113 | `SH72` | Número de habitaciones que usa para dormir | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 114 | `SXH73` | Tiene una red (No 20011) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 115 | `SH76A` | La vivienda tiene ventanas | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 116 | `SH76B` | Ventanas con cristal | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 117 | `SH76C` | Ventanas de madera | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 118 | `SH76D` | Ventanas con malla | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 119 | `SH76E` | Ventanas con cortinas/persianas | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 120 | `SH77F` | Otro tipo de transporte (caballos, peque-peque, etc.) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 121 | `SH78` | Algún miembro de su hogar es dueño de tierras agricolas | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 122 | `SH79` | Cuantas hectareas (1 decimal) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 123 | `SH224` | Prueba de Yodo | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 124 | `SH225U` | Visualización de la bolsa de sal | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 125 | `SH225` | Marca de sal usada por el hogar | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 126 | `SH227` | Prueba de cloro | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 127 | `QH227A` | La muestra fue tomada por: | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 128 | `QH227B` | La nuestra del agua se extrajo del: | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza. |
| 129 | `HV270` | Índice de riqueza | **INCLUIR** | Quintil de riqueza del hogar (1 a 5) y puntaje factorial continuo de riqueza. Determinante distal de desnutrición. |
| 130 | `HV271` | Factor de puntuación del índice de riqueza (5 decimales) | **INCLUIR** | Quintil de riqueza del hogar (1 a 5) y puntaje factorial continuo de riqueza. Determinante distal de desnutrición. |


### 📁 Archivo: `Diccionario - REC41.pdf` — Módulo: `1633_embarazo`
**Total de variables evaluadas:** 147

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Llaves de identificación de la mujer y orden de la historia de nacimiento del niño. |
| 2 | `CASEID` | Identificación Cuestionario Individual | **METADATO / LLAVE** | Llaves de identificación de la mujer y orden de la historia de nacimiento del niño. |
| 3 | `MIDX` | Orden de historia de nacimiento | **METADATO / LLAVE** | Llaves de identificación de la mujer y orden de la historia de nacimiento del niño. |
| 4 | `M1` | Durante el embarazo cuantas dosis contra el tétano le aplicaron | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 5 | `M1A` | Antes del embarazo cuantas dosis de la vacuna contra el tétano recibió | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 6 | `M1B` | Mes última inyección contra el tétano antes del embarazo | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 7 | `M1C` | Año de la última inyección contra el tétano antes del embarazo | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 8 | `M1D` | Hace cuantos años recibió la última inyección contra el tétano antes del embarazo | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 9 | `M1E` | Última inyección contra el tétano antes del embarazo (CMC) | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 10 | `M2A` | La chequeó en su control prenatal: Médico | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 11 | `M2B` | La chequeó en su control prenatal: Enfermera | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 12 | `M2C` | La chequeó en su control prenatal: Obstetra | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 13 | `M2D` | La chequeó en su control prenatal: Técnico en enfermería | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 14 | `M2E` | La chequeó en su control prenatal: Promotor de salud | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 15 | `M2F` | La chequeó en su control prenatal: Asistente de parto entrenado | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 16 | `M2G` | La chequeó en su control prenatal: Comadrona/partera | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 17 | `M2H` | La chequeó en su control prenatal: Relativo (no estándar y rara vez se usa) | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 18 | `M2I` | La chequeó en su control prenatal: CS otra persona | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 19 | `M2J` | La chequeó en su control prenatal: CS otra persona | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 20 | `M2K` | La chequeó en su control prenatal: Otro | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 21 | `M2L` | La chequeó en su control prenatal: CS otro | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 22 | `M2M` | La chequeó en su control prenatal: CS otro | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 23 | `M2N` | La chequeó en su control prenatal: Nadie | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 24 | `M3A` | La atendió en el parto: Médico | **INCLUIR** | Personal calificado que atendió el parto (médico, obstetra, enfermera). Calidad y seguridad de la atención perinatal. |
| 25 | `M3B` | La atendió en el parto: Enfermera | **INCLUIR** | Personal calificado que atendió el parto (médico, obstetra, enfermera). Calidad y seguridad de la atención perinatal. |
| 26 | `M3C` | La atendió en el parto: Obstetra | **INCLUIR** | Personal calificado que atendió el parto (médico, obstetra, enfermera). Calidad y seguridad de la atención perinatal. |
| 27 | `M3D` | La atendió en el parto: Técnico en enfermería | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 28 | `M3E` | La atendió en el parto: Promotor de salud | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 29 | `M3F` | La atendió en el parto: Asistente de parto entrenado | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 30 | `M3G` | La atendió en el parto: Comadrona/partera | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 31 | `M3H` | La atendió en el parto: Familiar | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 32 | `M3I` | La atendió en el parto: CS otra persona | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 33 | `M3J` | La atendió en el parto: CS otra persona | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 34 | `M3K` | La atendió en el parto: Otro | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 35 | `M3L` | La atendió en el parto: CS otro | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 36 | `M3M` | La atendió en el parto: CS otro | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 37 | `M3N` | La atendió en el parto: Nadie | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 38 | `M4` | Duración de la lactancia | **INCLUIR** | Duración de la lactancia materna en meses. Amamantamiento sostenido protege contra infecciones y desnutrición. |
| 39 | `M5` | Meses de amamantamiento | **INCLUIR** | Meses de lactancia materna exclusiva. Pilar de nutrición óptima en los primeros 6 meses de vida según OMS. |
| 40 | `M6` | Duración de la amenorrea | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 41 | `M7` | Meses de amenorrea | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 42 | `M8` | Duración de la abstinencia | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 43 | `M9` | Meses de abstinencia | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 44 | `M10` | Momento que quería quedar embarazada | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 45 | `M11` | Tiempo que hubiera querido esperar | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 46 | `M13` | Momento del primer control prenatal | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 47 | `M14` | Visitas prenatales por embarazo | **INCLUIR** | Número total de controles prenatales recibidos durante la gestación. Vigilancia oportuna del crecimiento fetal intrauterino. |
| 48 | `M15` | Lugar del parto | **INCLUIR** | Lugar de ocurrencia del parto (hospital, centro de salud, posta, domicilio). Indicador de parto institucional y acceso a salud. |
| 49 | `M17` | Parto por cesárea | **INCLUIR** | Parto por cesárea (1: Sí, 0: No). Vía de nacimiento asociada a morbilidades perinatales. |
| 50 | `M18` | Tamaño del niño al nacer | **INCLUIR** | Mes de gestación en que inició el primer control prenatal. Detección temprana de patologías gestacionales y RCIU. |
| 51 | `M19` | Peso del niño al nacer (kilos - 3 dec.) | **INCLUIR** | Peso al nacer en gramos reportado en carné o memoria. El bajo peso al nacer (< 2,500 g) es el factor etiológico más potente de desnutrición crónica. |
| 52 | `M19A` | Peso del niño al nacer según recuerda | **INCLUIR** | Tamaño del niño al nacer percibido por la madre (muy pequeño, pequeño, promedio, grande). Reporte cualitativo clave cuando no hubo balanza. |
| 53 | `M27` | Marca para lactancia | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 54 | `M28` | Marca para amenorrea | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 55 | `M29` | Marca para abstinencia | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 56 | `M34` | Cuando empezó a darle el pecho al niño | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 57 | `M35` | Cuantas veces le dio pecho durante la noche de ayer | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 58 | `M36` | Cuantas veces le dio pecho durante el día de ayer | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 59 | `M38` | El día de ayer o noche tomó algo en biberón | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 60 | `M39` | El día de ayer o durante el dìa o la noche cuantas veces le dio comida sólidas o<br>semisólidas | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 61 | `M42A` | Durante su embarazo Durante su embarazo en alguno de sus controles: La pesaron | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 62 | `M42B` | Durante su embarazo en alguno de sus controles: Le midieron la barriga | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 63 | `M42C` | Durante su embarazo en alguno de sus controles: Le tomaron le presión arterial | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 64 | `M42D` | Durante su embarazo en alguno de sus controles: Le hicieron examen de orina | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 65 | `M42E` | Durante su embarazo en alguno de sus controles: Le hicieron examen de sangre | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 66 | `M43` | Le explicaron acerca de las complicaciones que se pueden presentar en el embarazo | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 67 | `M44` | Le dijeron dónde acudir si se presentan complicaciones del embarazo | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 68 | `M45` | Durante el embarazo, le administraron tabletas, jarabe o inyecciones de hierro | **INCLUIR** | Madre recibió tabletas o jarabe de hierro durante el embarazo (1: Sí, 0: No). Estado nutricional de la gestante. |
| 69 | `M46` | Por cuantos días tomó hierro y/o cuantas inyecciones recibió | **INCLUIR** | Número de días que la madre consumió suplemento de hierro en la gestación. Adherencia preventiva materna. |
| 70 | `M47` | Durante el embarazo, tuvo dificultad para ver objetos o personas siendo de día | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 71 | `M48` | Durante el embarazo, tuvo dificultad para ver objetos o personas siendo de noche | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 72 | `M49A` | Durante el embarazo - tomó fansidar para la malaria | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 73 | `M49B` | Durante el embarazo - tomó cloroquina para la malaria | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 74 | `M49C` | Durante el embarazo - tomó medicamento para la malaria | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 75 | `M49D` | Durante el embarazo: tomó un medicamento específico del país para la malaria | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 76 | `M49E` | Durante el embarazo: tomó un medicamento específico del país para la malaria | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 77 | `M49F` | Durante el embarazo: tomó un medicamento específico del país para la malaria | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 78 | `M49G` | Durante el embarazo: tomó un medicamento específico del país para la malaria | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 79 | `M49X` | Durante el embarazo - tomó otro medicamento para la malaria | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 80 | `M49Z` | Durante el embarazo: no tomó medicamento para la malaria | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 81 | `M51A` | Tiempo en que tuvo control después del parto | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 82 | `M54` | Recibió una dosis de vitamina A en los primeros 2 meses después del parto | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 83 | `M55A` | Durante los primeros 3 días despues del parto, le dieron de tomar: leche, diferente a la<br>leche materna | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 84 | `M55B` | Durante los primeros 3 días despues del parto, le dieron de tomar: agua sola | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 85 | `M55C` | Durante los primeros 3 días despues del parto, le dieron de tomar: dextrosa glucosada | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 86 | `M55D` | Durante los primeros 3 días despues del parto, le dieron de tomar: agua | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 87 | `M55E` | Durante los primeros 3 días despues del parto, le dieron de tomar: agua azucarada | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 88 | `M55F` | Durante los primeros 3 días despues del parto, le dieron de tomar: jugo de fruta | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 89 | `M55G` | Durante los primeros 3 días despues del parto, le dieron de tomar: fórmula para bebes | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 90 | `M55H` | Durante los primeros 3 días despues del parto, le dieron de tomar: té/infusiones | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 91 | `M55I` | Durante los primeros 3 días despues del parto, le dieron de tomar: miel | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 92 | `M55J` | Durante los primeros 3 días despues del parto, le dieron de tomar: país específico | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 93 | `M55K` | Durante los primeros 3 días despues del parto, le dieron de tomar: país específico | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 94 | `M55L` | Durante los primeros 3 días despues del parto, le dieron de tomar: país específico | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 95 | `M55M` | Durante los primeros 3 días despues del parto, le dieron de tomar: país específico | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 96 | `M55N` | Durante los primeros 3 días, le dieron de tomar: país específico | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 97 | `M55X` | Durante los primeros 3 días despues del parto, le dieron de tomar: otro | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 98 | `M55Z` | Durante los primeros 3 días despues del parto, le dieron de tomar: nada | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 99 | `M57A` | Cuidado prenatal: su hogar | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 100 | `M57B` | Cuidado prenatal: otro hogar | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 101 | `M57C` | Cuidado prenatal: CS hogar | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 102 | `M57D` | Cuidado prenatal: CS hogar | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 103 | `M57E` | Atención prenatal: Hospital MINSA | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 104 | `M57F` | Atención prenatal: Centro de salud MINSA | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 105 | `M57G` | Atención prenatal: Posta médica MINSA | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 106 | `M57H` | Atención prenatal: Clínica móvil | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 107 | `M57I` | Atención prenatal: Hospital ESSALUD | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 108 | `M57J` | Atención prenatal: Hospital FF.AA. y PNP | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 109 | `M57K` | Atención prenatal: Policlínico/centro/posta ESSALUD | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 110 | `M57L` | Atención prenatal: Hospital/Otro de la Municipalidad | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 111 | `M57M` | Atención prenatal: Hospital privado/clínica | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 112 | `M57N` | Atención prenatal: Clínica móvil particular | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 113 | `M57O` | Atención prenatal: Médico particular | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 114 | `M57P` | Atención prenatal: Clínica/Posta de ONG | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 115 | `M57Q` | Atención prenatal: Hospital/Otro de la Iglesia | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 116 | `M57R` | Atención prenatal: Otros privados | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 117 | `M57S` | Atención prenatal: Casa de partera | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 118 | `M57T` | Atención prenatal: Otro CS | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 119 | `M57U` | Atención prenatal: Otro CS | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 120 | `M57V` | Atención prenatal: Otro CS | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 121 | `M57X` | Atención prenatal: Otro | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 122 | `M60` | Durante el embarazo tomó medicamentos contra parásitos intestinales | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 123 | `M61` | Tiempo que permaneció en el lugar del parto | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 124 | `M62` | Alguien verificó su salud antes del alta | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 125 | `M63` | Cuánto tiempo antes del parto se realizó un control de salud | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 126 | `M64` | Quién verificó la salud de los encuestados antes del alta | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 127 | `M65A` | Razón no fue a centro de salud: Cuesta mucho | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 128 | `M65B` | Razón no fue a centro de salud: No está abierto | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 129 | `M65C` | Razón no fue a centro de salud: Muy lejos, no hay transporte | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 130 | `M65D` | Razón no fue a centro de salud: No confía en atención | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 131 | `M65E` | Razón no fue a centro de salud: No había personal femenino | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 132 | `M65F` | Razón no fue a centro de salud: Nsposo, familia no quería | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 133 | `M65G` | Razón no fue a centro de salud: No fue necesario | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 134 | `M65H` | Razón no fue a centro de salud: No acostumbrada | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 135 | `M65I` | Razón no fue a centro de salud: CS | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 136 | `M65J` | Razón no fue a centro de salud: CS | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 137 | `M65K` | Razón no fue a centro de salud: CS | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 138 | `M65L` | Razón no fue a centro de salud: CS | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 139 | `M65X` | Razón no fue a centro de salud: otro | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 140 | `M66` | Después del parto tuvo algún chequeo o revisiòn médica | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 141 | `M67` | Cuánto tiempo después del parto se realizó su primer chequeo o revisiòn médica | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 142 | `M68` | Quién le realizó su chequeo o revisión médica después del parto | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 143 | `M69` | Donde se chequeo Ud. | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 144 | `M70` | Durante el primer mes le hicieron al bebe algún control o revisión médica | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 145 | `M71` | Cuánto tiempo después del parto se realizó el control postnatal | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 146 | `M72` | Quién realizó el control posnatal | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |
| 147 | `M73` | Dónde le hicieron el chequeo o revisión médica al bebé por primera vez | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.). |


### 📁 Archivo: `Diccionario - REC94.pdf` — Módulo: `1633_embarazo`
**Total de variables evaluadas:** 61

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Llaves de enlace relacional del cuestionario individual y del niño. |
| 2 | `CASEID` | Identificación Cuestionario Individual | **METADATO / LLAVE** | Llaves de enlace relacional del cuestionario individual y del niño. |
| 3 | `IDX94` | Orden de historia de nacimiento | **METADATO / LLAVE** | Llaves de enlace relacional del cuestionario individual y del niño. |
| 4 | `S410B` | Cuantos meses de embarazo tenía en la última revisión prenatal | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 5 | `S411B` | En alguno de sus controles: Le midieron la barriga | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 6 | `S411F` | En alguno de sus controles: Escucharon los latidos del corazón del bebé | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 7 | `S411G` | En alguno de sus controles: Le hicieron la prueba para descartar Sífilis | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 8 | `S411H` | En alguno de sus controles: Le hicieron la prueba para descartar de VIH/SIDA | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 9 | `S411I` | En alguno de sus controles: Le informaron como alimentarse | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 10 | `S411J` | En alguno de sus controles: Le informaron sobre sus derechos | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 11 | `S411K` | En alguno de sus controles: Le enseñaron como preparar pezones para lactancia<br>materna | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 12 | `S411L` | En alguno de sus controles: Le enseñaron como darle el pecho a su bebe | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 13 | `S411BA` | Cuantos meses de embarazo tenía cuando se realizó la primera prueba de orina | **DUDOSA (INTERVENCIÓN PRENATAL)** | Mes de embarazo al realizar pruebas específicas. Evaluar completitud y redundancia con inicio de control prenatal (M18). |
| 14 | `S411CA` | Cuantos meses de embarazo tenía cuando se realizó el primer análisis de sangre | **DUDOSA (INTERVENCIÓN PRENATAL)** | Mes de embarazo al realizar pruebas específicas. Evaluar completitud y redundancia con inicio de control prenatal (M18). |
| 15 | `S411DA` | Cuantos meses de embarazo tenía cuando se realizó la primera prueba de Sífilis | **DUDOSA (INTERVENCIÓN PRENATAL)** | Mes de embarazo al realizar pruebas específicas. Evaluar completitud y redundancia con inicio de control prenatal (M18). |
| 16 | `S411EA` | Cuantos meses de embarazo tenía cuando se realizó la primera prueba de VIH/SIDA | **DUDOSA (INTERVENCIÓN PRENATAL)** | Mes de embarazo al realizar pruebas específicas. Evaluar completitud y redundancia con inicio de control prenatal (M18). |
| 17 | `S413` | Durante el embarazo estaba afiliada al SIS | **INCLUIR** | Madre afiliada al SIS durante el embarazo. Acceso a subsidio integral de salud materna y neonatal. |
| 18 | `S422I` | Cantidad de inyecciones de hierro recibidas durante el embarazo | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 19 | `S426B` | Razón por qué no acudió a un hospital, centro o puesto de salud del MINSA para dar a<br>luz | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 20 | `S426E` | La cesárea fue programada | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 21 | `S426FA` | Cuánto tiempo transcurrió hasta llegar al establecimiento para dar a luz | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 22 | `S426FB` | Cuanto tiempo transcurrió desde que llegó al establecimeinto hasta que fué examinada<br>por personal de salud. | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 23 | `S426GA` | Complicaciones de parto: Parto prolongado | **INCLUIR** | Complicaciones severas del parto (parto prolongado, sangrado excesivo, convulsiones). Sufrimiento fetal e hipoxia perinatal. |
| 24 | `S426GB` | Complicaciones de parto: Sangrado excesivo | **INCLUIR** | Complicaciones severas del parto (parto prolongado, sangrado excesivo, convulsiones). Sufrimiento fetal e hipoxia perinatal. |
| 25 | `S426GC` | Complicaciones de parto: Fiebre con sangrado vaginal | **INCLUIR** | Complicaciones severas del parto (parto prolongado, sangrado excesivo, convulsiones). Sufrimiento fetal e hipoxia perinatal. |
| 26 | `S426GD` | Complicaciones de parto: Convulsiones | **INCLUIR** | Complicaciones severas del parto (parto prolongado, sangrado excesivo, convulsiones). Sufrimiento fetal e hipoxia perinatal. |
| 27 | `S426GE` | Complicaciones de parto: Otras | **INCLUIR** | Complicaciones severas del parto (parto prolongado, sangrado excesivo, convulsiones). Sufrimiento fetal e hipoxia perinatal. |
| 28 | `S430C` | El niño fue inscrito en la municipalidad/Oficina Registral de la RENIEC | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 29 | `S430D` | La partida/acta tiene Código Único de Identidad (CUI) | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 30 | `S431A` | En el establecimiento de salud le dieron algo en biberón al bebe después del nacimiento | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 31 | `S425A` | Entrevistada era miembro del seguro de salud materna | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 32 | `S432` | El niño está afiliado al Seguro Integral de Salud | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 33 | `S432AD` | Day affiliation integral health insurance | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 34 | `S432AM` | Mes afiliación seguro de salud integral | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 35 | `S432AY` | Año de afiliación seguro de salud integral | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 36 | `S427DA` | Complicaciones después del parto: sangrado intenso | **EXCLUIR POR ALTA INCOMPLETITUD** | Complicaciones del puerperio con muy baja prevalencia de respuesta afirmativa. |
| 37 | `S427DB` | Complicaciones después del parto: pérdida de conciencia | **EXCLUIR POR ALTA INCOMPLETITUD** | Complicaciones del puerperio con muy baja prevalencia de respuesta afirmativa. |
| 38 | `S427DC` | Complicaciones después del parto: fiebre alta, escalofríos | **EXCLUIR POR ALTA INCOMPLETITUD** | Complicaciones del puerperio con muy baja prevalencia de respuesta afirmativa. |
| 39 | `S427DD` | Complicaciones después del parto: infección de los senos | **EXCLUIR POR ALTA INCOMPLETITUD** | Complicaciones del puerperio con muy baja prevalencia de respuesta afirmativa. |
| 40 | `S427DE` | Complicaciones después del parto: dolor al orinar | **EXCLUIR POR ALTA INCOMPLETITUD** | Complicaciones del puerperio con muy baja prevalencia de respuesta afirmativa. |
| 41 | `S427DF` | Complicaciones después del parto: flujos vaginales | **EXCLUIR POR ALTA INCOMPLETITUD** | Complicaciones del puerperio con muy baja prevalencia de respuesta afirmativa. |
| 42 | `S427DG` | Complicaciones después del parto: Pérdida involuntaria de orina | **EXCLUIR POR ALTA INCOMPLETITUD** | Complicaciones del puerperio con muy baja prevalencia de respuesta afirmativa. |
| 43 | `S427F` | Cuando tuvo esas complicaciones recibió atención médica | **EXCLUIR POR ALTA INCOMPLETITUD** | Complicaciones del puerperio con muy baja prevalencia de respuesta afirmativa. |
| 44 | `S435` | Por qué no le dio pecho al bebé | **EXCLUIR POR CAUSALIDAD INVERSA** | Razones por las que no dio o dejó de dar pecho por enfermedad/indicación médica. Alto riesgo de causalidad inversa con falla de medro. |
| 45 | `S436C` | Pusieron al niño en contacto piel a piel con Ud. inmediatamente después del nacimiento | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 46 | `S440` | Por qué dejo de darle pecho | **EXCLUIR POR CAUSALIDAD INVERSA** | Razones por las que no dio o dejó de dar pecho por enfermedad/indicación médica. Alto riesgo de causalidad inversa con falla de medro. |
| 47 | `S441` | Recibió alguna capacitación sobre lactancia materna durante el embarazo | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 48 | `S442` | En qué lugar recibió capacitación sobre lactancia materna | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 49 | `S446AA` | Con cuanto tiempo de anticipación preparó el biberón | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 50 | `S446AB` | Donde guardó el biberón | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 51 | `S446A` | Se agregó azúcar a cualquiera de los alimentos del bebé | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 52 | `S447` | Se agrego azúcar a algun alimento o liquido que comiò o tomò el dìa de ayer | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 53 | `S448A` | Tiempo entre que terminó de preparar los alimentos del bebé y los sirvió | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 54 | `S448B` | Dónde se almacenó la comida | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 55 | `QI411_M` | En alguno de sus controles: le hicieron la prueba para descartar Hepatitis B | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 56 | `QI411F` | Cuántos meses de embarazo tenía en primera prueba para descartar Hepatitis B | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 57 | `QI440B` | Durante primeros 6 meses, solo recibió leche materna | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 58 | `QI422A_A` | Durante el embarazo algún personal de salud le realizó una prueba o análisis para<br>descartar anemia | **EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD** | Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables. |
| 59 | `QI422A_B` | Durante el embarazo le diagnosticaron o le dijeron que tenía anemia | **DUDOSA (TRATAMIENTO CLÍNICO)** | Diagnóstico e indicación de hierro materno por anemia en el embarazo. Fuerte correlación pero posible causalidad inversa si fue reactivo. |
| 60 | `QI422A_C` | Durante el embarazo le indicaron tratamiento con hierro | **DUDOSA (TRATAMIENTO CLÍNICO)** | Diagnóstico e indicación de hierro materno por anemia en el embarazo. Fuerte correlación pero posible causalidad inversa si fue reactivo. |
| 61 | `QI422A_D` | Durante el embarazo consumió hierro tal como le indicó el personal de salud | **DUDOSA (TRATAMIENTO CLÍNICO)** | Diagnóstico e indicación de hierro materno por anemia en el embarazo. Fuerte correlación pero posible causalidad inversa si fue reactivo. |


### 📁 Archivo: `Diccionario - REC0111.pdf` — Módulo: `1031-mef`
**Total de variables evaluadas:** 104

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Llaves relacionales de la mujer (MEF) y del hogar. |
| 2 | `CASEID` | Identificación Cuestionario Individual | **METADATO / LLAVE** | Llaves relacionales de la mujer (MEF) y del hogar. |
| 3 | `HHID` | Identificación Cuestionario del Hogar | **METADATO / LLAVE** | Llaves relacionales de la mujer (MEF) y del hogar. |
| 4 | `V000` | Código y fase del país | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 5 | `V001` | Conglomerado | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 6 | `V002` | Número de vivienda | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 7 | `V003` | Número de línea de entrevistada | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 8 | `V004` | Unidad de área final | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 9 | `V007` | Año de la entrevista | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 10 | `V008` | Fecha de la entrevista, Codificación centenaria de meses (CMC) | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 11 | `Q105DD` | Dia de nacimeinto de la entrevistada | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 12 | `V009` | Mes de nacimiento de la entrevistada | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 13 | `V010` | Año de nacimiento de la entrevistada | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 14 | `V011` | Fecha de nacimiento, Codificación centenaria de meses (CMC) | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 15 | `V012` | Edad actual - entrevistada | **INCLUIR** | Edad actual de la madre en años y por grupos quinquenales. Embarazo adolescente o edad materna avanzada. |
| 16 | `V013` | Edad actual por grupos de 5 años | **INCLUIR** | Edad actual de la madre en años y por grupos quinquenales. Embarazo adolescente o edad materna avanzada. |
| 17 | `V014` | Integridad de la información para la fecha de nacimiento | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 18 | `V015` | Resultado entrevista individual | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 19 | `V017` | Inicio del calendario, Codificación centenaria de mesesl CMC | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 20 | `V018` | Columna del mes de la entrevista | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 21 | `V019` | Duración del calendario | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 22 | `V019A` | Número de columnas de calendario | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 23 | `V020` | Muestra alguna vez casada | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 24 | `V021` | Unidad de muestreo primario - conglomerado | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 25 | `V023` | Dominio de ejemplo - Departamento | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 26 | `V024` | Región | **INCLUIR** | Región de residencia habitual De-Jure (departamento 1 a 25). |
| 27 | `V025` | Tipo de lugar de residencia | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 28 | `V026` | El lugar de residencia en el que se entrevistó - De Facto | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 29 | `V027` | Número de visitas | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 30 | `V028` | Identificación del entrevistador | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 31 | `V029` | Identificador del digitador | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 32 | `V030` | Supervisor de campo | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 33 | `V031` | Editor de campo | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 34 | `V032` | Editor de la oficina | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 35 | `V033` | Selección final del área de probabilidad | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 36 | `V034` | Número de orden del esposo | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 37 | `V040` | Altitud del conglomerado en metros | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 38 | `V042` | Selección de hogar para hemoglobina | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 39 | `V043` | Selección para módulo de estatus de mujeres | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 40 | `V044` | Selección para módulo de violencia domestica | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 41 | `V101` | Región | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 42 | `V102` | Tipo de lugar de residencia | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 43 | `V103` | Lugar de residencia de la infancia | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 44 | `V104` | Cuanto tiempo tiene viviendo continuamente en el lugar de residencia actual | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 45 | `V105` | Tipo de lugar de residencia anteriormente | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 46 | `V106` | Nivel educativo más alto | **INCLUIR** | Nivel educativo más alto de la madre y años de educación aprobados. Determinante social de salud infantil. |
| 47 | `V107` | Año/grado de educación más alto aprobado | **INCLUIR** | Nivel educativo más alto de la madre y años de educación aprobados. Determinante social de salud infantil. |
| 48 | `V113` | Fuente principal de abasteciemiento de agua potable que utilizan en su hogar para tomar<br>o beber | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 49 | `V115` | Tiempo para llegar a la fuente de agua | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 50 | `V116` | Tipo de instalación sanitaria | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 51 | `V119` | En su hogar tiene: electricidad | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 52 | `V120` | En su hogar tiene: radio | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 53 | `V121` | En su hogar tiene: televisión | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 54 | `V122` | En su hogar tiene: refrigerador | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 55 | `V123` | En su hogar tiene: bicicleta | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 56 | `V124` | En su hogar tiene: motocicleta/motocar | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 57 | `V125` | En su hogar tiene: coche/camión | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 58 | `V127` | Material predominante del piso de la vivienda | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 59 | `V128` | Material predominante de las paredes exteriores de la vivienda | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 60 | `V129` | Material predominante del techo de la vivienda | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 61 | `V130` | Religión | **INCLUIR** | Religión de la entrevistada (católica, evangélica, etc.). Pautas culturales de crianza y alimentación. |
| 62 | `V131` | Etnicidad | **INCLUIR** | Etnicidad / Autoidentificación étnica de la mujer. Captura desigualdades históricas de pueblos originarios. |
| 63 | `V133` | Educación en años simples | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 64 | `V134` | El lugar en el que se realizó la entrevista De-facto | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 65 | `V135` | Residente habitual o visitante | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 66 | `V136` | Número de miembros del hogar | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 67 | `V137` | Número de niños de 6 años de edad | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 68 | `V138` | Número de mujeres de 15 a 49 años de edad elegibles en el hogar | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 69 | `V139` | Región, residencia habitual De-jure | **INCLUIR** | Región de residencia habitual De-Jure (departamento 1 a 25). |
| 70 | `V140` | Tipo de área de residencia De-jure | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 71 | `V141` | Lugar de residencia De-jure | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 72 | `V149` | Logro educativo | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 73 | `V150` | Relación con el jefe del hogar | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 74 | `V151` | Sexo del Jefe del Hogar | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 75 | `V152` | Edad del jefe del hogar | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 76 | `V153` | En su hogar tiene: teléfono | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 77 | `AWFACTT` | Factor todas las mujeres - total | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 78 | `AWFACTU` | Factor todas las mujeres - urbano/rural | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 79 | `AWFACTR` | Factor todas las mujeres - regional | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 80 | `AWFACTE` | Factor todas las mujeres - educación | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 81 | `AWFACTW` | Factor todas las mujeres - índice de riqueza | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 82 | `V155` | Alfabetización | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 83 | `V156` | Alguna vez participó en un programa de alfabetización (no incluyendo la escuela<br>primaria) | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 84 | `V157` | Frecuencia de lectura de un periódico o revista | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 85 | `V158` | Frecuencia de escuchar radio | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 86 | `V159` | Frecuencia de ver televisión | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 87 | `V160` | Baño compartido con otros hogares | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 88 | `V161` | Tipo de combustible para cocinar | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 89 | `V166` | Resultados de la prueba del yodo en la sal | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 90 | `V167` | Número de viajes en los últimos 12 meses | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 91 | `V168` | Afuera más de un mes en los últimos 12 meses | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 92 | `ML101` | Tipo de mosquitero que utilizo para dormir última noche | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 93 | `QD333_1` | Alguna dificultad o limitación permanente para ver, aún usando anteojos | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 94 | `QD333_2` | Alguna dificultad o limitación permanente para oir, aún usando audífonos | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 95 | `QD333_3` | Alguna dificultad o limitación permanente para hablar o comunicarse, aún usando la<br>lengua de señas u otro | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 96 | `QD333_4` | Alguna dificultad o limitación permanente para moverse o caminar para usar brazos y/o<br>piernas | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 97 | `QD333_5` | Alguna dificultad o limitación permanente para entender o aprender (concentrarse y<br>recordarse) | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 98 | `QD333_6` | Alguna dificultad o limitación permanente para relacionarse con los demás, por sus<br>pensamientos, sentimientos, emociones o conductas | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 99 | `UBIGEO` | Código de Ubicación Gegráfica | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 100 | `V022` | Estratos | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 101 | `V005` | Factor de ponderacion | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |
| 102 | `V190` | Índice de riqueza | **INCLUIR** | Índice de riqueza y factor de puntuación en el cuestionario de MEF. |
| 103 | `V191` | Factor de puntuación del índice de riqueza (5 decimales) | **INCLUIR** | Índice de riqueza y factor de puntuación en el cuestionario de MEF. |
| 104 | `mujeres12a49` | Mujeres de 12 a 49 años de edad | **EXCLUIR POR IRRELEVANCIA** | Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo. |


### 📁 Archivo: `Diccionario - REC91.pdf` — Módulo: `1031-mef`
**Total de variables evaluadas:** 343

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Llaves relacionales de la mujer en el módulo individual ampliado. |
| 2 | `CASEID` | Identificación del caso | **METADATO / LLAVE** | Llaves relacionales de la mujer en el módulo individual ampliado. |
| 3 | `SVER` | Versión del cuestionario | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 4 | `SREGION` | Región natural | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 5 | `SSEMES` | Semestre | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 6 | `SPROVIN` | Provincia | **INCLUIR** | Provincia y distrito de residencia de la mujer (georreferenciación fina). |
| 7 | `SDISTRI` | Distrito | **INCLUIR** | Provincia y distrito de residencia de la mujer (georreferenciación fina). |
| 8 | `S108N` | Nivel educativo aprobado | **INCLUIR** | Nivel y año educativo aprobado detallado. |
| 9 | `S108Y` | El último año de educación aprobado | **INCLUIR** | Nivel y año educativo aprobado detallado. |
| 10 | `S108G` | El último grado de educación aprobado | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 11 | `S111` | Actualmente asiste a la escuela, colegio, instituto o universidad | **INCLUIR** | Madre asiste actualmente a escuela, instituto o universidad. |
| 12 | `S112` | Razón por que dejo de asistir a la escuela | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 13 | `S119` | Idioma o lengua materna que aprendió hablar en su niñez | **INCLUIR** | Idioma o lengua materna que aprendió a hablar en su niñez la madre (Quechua, Aimara, Castellano, etc.). Barrera lingüística y etnicidad. |
| 14 | `S119NA` | Lengua materna de la madre | **INCLUIR** | Lengua materna de la abuela materna. Herencia lingüística indígena intergeneracional. |
| 15 | `S119NB` | Lengua materna su padre | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 16 | `S119D` | Por sus antepasados ​​y costumbres, Ud. Se considera | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 17 | `S229A` | Control del embarazo en: hospital MINSA | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 18 | `S229B` | Control del embarazo en: hospital ESSALUD | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 19 | `S229C` | Control del embarazo en: hospital FFAA & PNP | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 20 | `S229D` | Control del embarazo en: centro de salud MINSA | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 21 | `S229E` | Control del embarazo en: puesto de salud MINSA | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 22 | `S229F` | Control del embarazo en: center/post ESSALUD | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 23 | `S229G` | Control del embarazo en: Hospital/Otro gobierno local. | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 24 | `S229H` | Control del embarazo en: Clínica privada | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 25 | `S229I` | Control del embarazo en: Médico particular | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 26 | `S229J` | Control del embarazo en: casa de partera | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 27 | `S229K` | Control de embarazo en: clínica/posta de ONG | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 28 | `S229L` | Control del embarazo en: hospital/otro de la iglesia | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 29 | `S229X` | Control del embarazo en: otro | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 30 | `S229Y` | Sin control | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 31 | `S229A1` | Meses de embarazo al primer control | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 32 | `S229B1` | Afiliada a seguro de salud (seguro integral) | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 33 | `S229CDAY` | Día de afiliación | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 34 | `S229CM` | Mes de afiliación | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 35 | `S229CY` | Año de afiliación | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 36 | `S229DA` | Conocimiento de Seguro Integral por: TV | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 37 | `S229DB` | Conocimiento del Seguro Integral por: radio | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 38 | `S229DC` | Conocimiento del Seguro Integral por: periódicos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 39 | `S229DD` | Conocimiento del Seguro Integral por: personal de salud | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 40 | `S229DE` | Se hizo consciente de Seguro Integral por: familia/amigos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 41 | `S229DF` | Conocimiento de Seguro Integral por: club de madres | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 42 | `S229DX` | Conocimiento de Seguro Integral por: otros | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 43 | `S239A` | Documento de identificación: Partida de Nacimiento | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 44 | `S239B` | Documento de identificación: Tarjeta de Inscripción | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 45 | `S239C` | Documento de identificación: DNI | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 46 | `S239D` | Documento de identificación: Tarjeta de Votación | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 47 | `S239E` | Documento de identificación: Libreta Militar | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 48 | `S239F` | Documento de identificación: No tiene | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 49 | `S239X` | Documento de identificación: Otro | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 50 | `S314` | Monto de pago de la esterilización incluyendo la consulta | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 51 | `S315B` | Momento que se esterilizó | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 52 | `S317AC` | Marca Vaginales | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 53 | `S317AD` | Marca de inyección | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 54 | `S317C` | Cómo determinar días de fertilidad | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 55 | `S321A` | Primera fuente para el método actual | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 56 | `S325A` | El método actual es el que quería | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 57 | `S325B` | Qué método quería | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 58 | `S325CA` | Problema para obtener el método: el centro de salud no tenía método | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 59 | `S325CB` | Problema para obtener el método: muy costoso | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 60 | `S325CX` | Problema para obtener el método: otro | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 61 | `S325D` | Quién decidió sobre el método actual | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 62 | `S325E` | Por qué aceptó el método actual | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 63 | `S325GA` | Opinión de atención recibida: horas de trabajo | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 64 | `S325GB` | Opinión de la atención recibida: métodos de planificación familiar | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 65 | `S325GC` | Opinión de la atención recibida: método prescrito | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 66 | `S325GD` | Opinión de la atención recibida: sala de espera cómoda | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 67 | `S325GE` | Opinión de la atención recibida: limpieza de la sala de espera | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 68 | `S325GF` | Opinión de la atención recibida: tiempo de espera | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 69 | `S325GG` | Opinión de la atención recibida: tratamiento del personal administrativo | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 70 | `S325GH` | Opinión de la atención recibida: tratamiento del personal de salud | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 71 | `S325GI` | Opinión de la atención recibida: tratamiento del médico | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 72 | `S325GJ` | Opinión de la atención recibida: explicaciones del médico | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 73 | `S325GK` | Opinión de atención recibida: privacidad | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 74 | `S327B` | Ha ido a consulta de control de DIU/IMPLANTES | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 75 | `S327C` | Número de controles de DIU/IMPLANTES en los últimos 12 meses | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 76 | `S481AA` | Llevaría inmediatamente al niño al centro de salud si: no puede beber o lactar | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 77 | `S481AB` | Llevaría inmediatamente al niño al centro de salud si: se pone más enfermo | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 78 | `S481AC` | Llevaría inmediatamente al niño al centro de salud si: le da fiebre/diarrea/vómito | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 79 | `S481AD` | Llevaría inmediatamente al niño al centro de salud si: tiene respiraciones rápidas | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 80 | `S481AE` | Llevaría inmediatamente al niño al centro de salud si: tiene tos/dificultad para respirar | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 81 | `S481AF` | Llevaría inmediatamente al niño al centro de salud si: sangre sobre las heces hace<br>deposiciones con sangre | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 82 | `S481AG` | Llevaría inmediatamente al niño al centro de salud si: come/bebe poco | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 83 | `S481AX` | Llevaría inmediatamente al niño al centro de salud si: Otro | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 84 | `S481AZ` | Llevaría inmediatamente al niño al centro de salud si: no sabe | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 85 | `S484` | Afiliado o incorporado al programa Juntos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 86 | `S484D` | Día de afiliación | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 87 | `S484M` | Mes de afiliación | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 88 | `S484Y` | Año de afiliación | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 89 | `S485` | A oído/escuchado de la prueba del papanicolao | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 90 | `S485A` | Le hicieron una prueba de papanicolaou en los últimos 5 años | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 91 | `S486` | Le hicieron un examen de mama en los últimos 5 años | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 92 | `S486A` | Ud. conoce como hacerse el auto-examen de mama | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 93 | `S486B` | Ud. misma se realizó el examen de mama | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 94 | `S489C` | Cuidaría a parientes si se enfermaran con la TBC | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 95 | `S489D` | Si un miembro de su familia tuviera tuberculosis, mantendría en secreto su enfermedad | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 96 | `S490` | Normalmente, cuántas veces al día se lava las manos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 97 | `S490AA` | Se lava las manos necesariamente después de usar el baño | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 98 | `S490AB` | Se lava las manos necesariamente después de cambiar pañales | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 99 | `S490AC` | Se lava las manos necesariamente antes de preparar la comida | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 100 | `S490AD` | Se lava las manos necesariamente antes de servir la comida | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 101 | `S490AE` | Se lava las manos necesariamente antes de comer | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 102 | `S490AF` | Se lava las manos necesariamente antes de alimentar al niño | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 103 | `S490AG` | Se lava las manos necesariamente en cualquier momento | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 104 | `S490AX` | Se lava las manos necesariamente en otra situación | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 105 | `S490BA` | Normalmente utiliza cuando se lava las manos: Agua de caño o grifo | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 106 | `S490BB` | Normalmente utiliza cuando se lava las manos: Jabón | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 107 | `S490BC` | Normalmente utiliza cuando se lava las manos: Detergente | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 108 | `S490BD` | Normalmente utiliza cuando se lava las manos: Toalla | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 109 | `S490BX` | Normalmente utiliza cuando se lava las manos: Otro | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 110 | `S492A` | Ayer el niño(a) durante el día o la noche bebió: Solo agua | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 111 | `S492B` | Ayer el niño(a) durante el día o la noche bebió: Leche en polvo (NAM,S26, SIMILAC,<br>etc) | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 112 | `S492C` | Ayer el niño(a) durante el día o la noche bebió: Leche materna refrigerada | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 113 | `S492D` | Ayer el niño(a) durante el día o la noche bebió: cualquier otra leche (fresca, evaporada<br>o en polvo) | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 114 | `S492E` | Ayer el niño(a) durante el día o la noche bebió: Zumo de frutas | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 115 | `S492F` | Ayer el niño(a) durante el día o la noche bebió: Té Café | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 116 | `S492G` | Ayer el niño(a) durante el día o la noche bebió: cualquier otro líquido como bebidas<br>gaseosas, caldo | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 117 | `S493A` | Ayer el niño(a) durante el día o la noche comió: harina, pan, fideos, galletas o comida<br>hecha de cereales | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 118 | `S493B` | Ayer el niño(a) durante el día o la noche comió: camote, zapallo, zanahoria | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 119 | `S493C` | Ayer el niño(a) durante el día o la noche comió: habas, frijol, lenteja, soya, pallares,<br>garbanzos, alrvejas | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 120 | `S493D` | Ayer el niño(a) durante el día o la noche comió: comida hecha de tubérculos, raíces<br>(papa, yuca, olluco, oca, mashua) | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 121 | `S493E` | Ayer el niño(a) durante el día o la noche comió: verduras (espinacas, acelgas, etc.) | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 122 | `S493F` | Ayer el niño(a) durante el día o la noche comió: mango, papaya, aguaje | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 123 | `S493G` | Ayer el niño(a) durante el día o la noche comió: naranja, mandarina, maracuyá, toronja,<br>etc. | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 124 | `S493H` | Ayer el niño(a) durante el día o la noche comió: Otras frutas (bananas, manzanas, etc.) | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 125 | `S493I` | Ayer el niño(a) durante el día o la noche comió: carne, pollo, pescado | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 126 | `S493J` | Ayer el niño(a) durante el día o la noche comió: huevos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 127 | `S493K` | Ayer el niño(a) durante el día o la noche comió: queso, yogurt, helado u otros alimentos<br>preparados con leche (leche asada, helados, crema volteada, etc.) | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 128 | `S493L` | Ayer el niño(a) durante el día o la noche comió: cualquier comida hecha alimentos<br>hechos con aceite, manteca, mantequilla, o al que le agregó aceite manteca,<br>mantequilla | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 129 | `S493M` | Ayer el niño(a) durante el día o la noche comió: papilla de programas sociales | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 130 | `S493N` | Ayer el niño(a) durante el día o la noche comió: cualquier otra comida sòlida o<br>semisòlida Otros alimentos sólidos o semisólidos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 131 | `S493O` | Ayer el niño(a) durante el día o la noche comió: Otras frutas secas | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 132 | `S493P` | Ayer el niño(a) durante el día o la noche comió: Cualquier alimento dulce, caramelo,<br>chocolates u otros | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 133 | `S494` | Recibir papilla de los programas sociales | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 134 | `S494A` | Cuántos paquetes tiene | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 135 | `S494B` | Come la papilla de programas sociales | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 136 | `S495A` | Ayer el niño no recibe líquidos o sólidos excepto la leche materna | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 137 | `S496` | Persona que normalmente alimenta al niño | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 138 | `S500A` | Presencia de niñas/os menores de 10 años | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 139 | `S500B` | Presencia del esposo/compañero | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 140 | `S500C` | Presencia de otros hombres | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 141 | `S500D` | Presencia de otras mujeres | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 142 | `S508A` | Principal causa de la ùltima del último divorcio/separación | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 143 | `S512C` | Relación con la primera pareja sexual | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 144 | `S616` | Aprueba, desaprueba que parejas usen métodos de planificación familiar | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 145 | `S618A` | Los últimos 12 meses comentado sobre planificación familiar con: esposo/pareja | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 146 | `S618B` | Los últimos 12 meses comentado sobre planificación familiar con: madre | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 147 | `S618C` | Los últimos 12 meses comentado sobre planificación familiar con: padre | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 148 | `S618D` | Los últimos 12 meses comentado sobre planificación familiar con: hermanas | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 149 | `S618E` | Los últimos 12 meses comentado sobre planificación familiar con: hermanos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 150 | `S618F` | Los últimos 12 meses comentado sobre planificación familiar con: hija | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 151 | `S618G` | Los últimos 12 meses comentado sobre planificación familiar con: hijo | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 152 | `S618H` | Los últimos 12 meses comentado sobre planificación familiar con: suegra | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 153 | `S618I` | Los últimos 12 meses comentado sobre planificación familiar con: suegro | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 154 | `S618J` | Los últimos 12 meses comentado sobre planificación familiar con: novio | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 155 | `S618K` | Los últimos 12 meses comentado sobre planificación familiar con: amigas/vecinas | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 156 | `S618L` | Los últimos 12 meses comentado sobre planificación familiar con: amigos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 157 | `S618M` | Los últimos 12 meses comentado sobre planificación familiar con: otros familiares | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 158 | `S618X` | Los últimos 12 meses comentado sobre planificación familiar con: otros | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 159 | `S621` | Su esposo/compañero aprueba/desaprueba que las parejas usen planificación familiar | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 160 | `S621A` | Frecuencia de los últimos 12 meses habló con su esposo acerca de planificación<br>familiar | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 161 | `S704N` | Nivel educativo del esposo/compañero | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 162 | `S704Y` | Último año aprobado del esposo | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 163 | `S704G` | Último grado aprobado del esposo | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 164 | `S718` | Ingresos de la entrevistada utilizada para gastos familiares | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 165 | `S720A` | Quién cuida de la niña/niño cuando Ud. sale de la casa | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 166 | `S802` | Cree Ud. Que una persona puede hacer algo para prevenir el virus que causa el SIDA<br>(VIH) | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 167 | `S802D` | Cree Ud. que la gente puede contraer el SIDA (VIH) a través de abrazos o caricias a<br>una persona infectada | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 168 | `S802E` | Cree Ud. que la gente puede contraer el SIDA (VIH) a través de utensilios compartidos<br>con una persona infectada | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 169 | `S802F` | Cree Ud. que se pueden contraer el SIDA (VIH) comparten baño, ducha y/o piscinas | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 170 | `S802H` | Cree Ud. que se puede contraer el SIDA (VIH) a través de la brujería | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 171 | `S802I` | Cree Ud. que la gente puede contraer el SIDA (VIH) por el castigo divino | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 172 | `S803AF` | Lugar para hacerse la prueba de VIH SIDA: Hospital/Otros FFAA & PNP | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 173 | `S803AG` | Lugar para hacerse la prueba de VIH SIDA: Hospital/Otros de la Municipalidad | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 174 | `S803AM` | Lugar para hacerse la prueba de VIH SIDA: Hospital/Otro de la Iglesia | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 175 | `S804A` | Cuando fue a realizarse la prueba: recibió asesoramiento antes del examen | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 176 | `S804C` | Cuando le dieron resultados. Le brindaron consejería | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 177 | `S806AX` | En que etapa puede ser transmitido el VIH de la madre al hijo: otro | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 178 | `S806AZ` | En que etapa puede ser transmitido el VIHI de la madre al hijo: No sabe | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 179 | `S807` | Si una niña/niño tiene infección por el virus que causa el SIDA: se debe permitir asistir a<br>la escuela o colegio | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 180 | `S809` | Si una persona tiene la infecciòn por el virus que causa el SIDA: el empleador lo debe<br>despedir por esta causa | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 181 | `S810` | Si un médico tiene la infecciòn por el virus que causa el SIDA: se le debe permitir<br>continuar con su trabajo | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 182 | `S811` | Si una persona tiene el virus que causa el SIDA y necesita ser operada: debe permitirle<br>la operación | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 183 | `S815AA` | Conoce la ETS: sífilis | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 184 | `S815AB` | Conoce la ETS: gonorrea | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 185 | `S815AC` | Conoce la ETS: verrugas genitales/condiloma | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 186 | `S815AD` | Conoce la ETS: Chancro | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 187 | `S815AE` | Conoce la ETS: Herpes | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 188 | `S815AX` | Conoce la ETS: Otros | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 189 | `S815AZ` | Conoce la ETS: No sabe | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 190 | `S816A` | Síntomas de ETS en hombres: dolor abdominal | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 191 | `S816B` | Síntomas de ETS en hombres: secreción/goteos en genitales | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 192 | `S816C` | Síntomas de ETS en hombres: secreción mal oliente | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 193 | `S816D` | Síntomas de ETS en hombres: molestia al orinar | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 194 | `S816E` | Síntomas de ETS en hombres: enrojecimiento/picazón/ardor en genitales | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 195 | `S816F` | Síntomas de ETS en hombres: inflamación/hinchazón /dolor en genitales | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 196 | `S816G` | Síntomas de ETS en hombres: úlceras/llagas genitales | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 197 | `S816H` | Síntomas de ETS en hombres: verrugas genitales | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 198 | `S816I` | Síntomas de ETS en hombres: sangre en la orina | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 199 | `S816J` | Síntomas de ETS en hombres: pérdida de peso | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 200 | `S816K` | Síntomas de ETS en hombres: la impotencia | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 201 | `S816L` | Síntomas de ETS en hombres: los síntomas pueden no estar presentes | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 202 | `S816M` | Síntomas de ETS en hombres: secreción/pus por el pene | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 203 | `S816W` | Síntomas de ETS en hombres: otros | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 204 | `S816Z` | Síntomas de ETS en hombres: no sabe | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 205 | `S816AA` | Síntomas de ETS en mujeres: dolor abdominal | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 206 | `S816AB` | Síntomas de ETS en mujeres: secreción genital de flujo por la vagina | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 207 | `S816AC` | Síntomas de ETS en mujeres: secreción mal oliente | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 208 | `S816AD` | Síntomas de ETS en mujeres: molestias al orinar | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 209 | `S816AE` | Síntomas de ETS en mujeres: enrojecimiento/picazón/ardor en genitales | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 210 | `S816AF` | Síntomas de ETS en mujeres: inflamación/hinchazón /dolor en genitales | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 211 | `S816AG` | Síntomas de ETS en mujeres: úlceras/llagas genitales | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 212 | `S816AH` | Síntomas de ETS en mujeres: verrugas genitales | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 213 | `S816AI` | Síntomas de ETS en mujeres: sangre en la orina | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 214 | `S816AJ` | Síntomas de ETS en mujeres: pérdida de peso | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 215 | `S816AK` | Síntomas de ETS en mujeres: infertilidad/no poder tener hijos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 216 | `S816AL` | Síntomas de ETS en mujeres: los síntomas pueden no estar presentes | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 217 | `S816AW` | Síntomas de ETS en mujeres: otros | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 218 | `S816AZ` | Síntomas de ETS en mujeres: no sabe | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 219 | `S817` | Le han Diagnosticado alguna ETS en los últimos 12 meses | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 220 | `S817GF` | Dónde fue a recibir tratamiento: Hospital/Otros FFAA o PNP | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 221 | `S817GG` | Dónde fue a recibir tratamiento: Hospital/Otro de la Municipalidad | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 222 | `S817GM` | Dónde fue a recibir tratamiento: Hospital/Otro de la Iglesia | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 223 | `S818` | Ha tenido relaciones sexuales por dinero en los últimos 12 meses | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 224 | `S1002A` | En última/actual relación su esposo/compañero: se mostró tierno/cariñoso | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 225 | `S1002B` | En última/actual relación su esposo/compañero: paso tiempo libre con usted | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 226 | `S1002C` | En última/actual relación su esposo/compañero: tomo en cuenta su opinión | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 227 | `S1002D` | En última/actual relación su esposo/compañero: respetó sus deseos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 228 | `S1002E` | En última/actual relación su esposo/compañero: respetó sus derechos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 229 | `S1008AN` | En los últimos 12 meses como resultado de algo que su esposo/compañero le hizo, Ud.<br>tuvo: moretones y/o dolores | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 230 | `S1008BN` | En los últimos 12 meses como resultado de algo que su esposo/compañero le hizo, Ud.<br>tuvo: herida o lesión, huesos y dientes rotos, quemaduras | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 231 | `S1008CN` | En los últimos 12 meses como resultado de algo que su esposo/compañero le hizo, Ud.<br>tuvo: que ir al médico o centro de salud | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 232 | `S1008DN` | En los últimos 12 meses como resultado de algo que su esposo/compañero le hizo, Ud.<br>tuvo: que ir al curandero, huesero u otra persona | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 233 | `S1012B` | Cuando su esposo/compañero la ha agredido o golpeado se encontraba bajo los<br>efectos de licor o drogas | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 234 | `S1012BN` | En los últimos 12 meses con qué frecuencia su esposo/compañero la ha agredido o<br>golpeado bajo los efectos de licor o drogas | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 235 | `S1017` | La persona que le pegó, abofeteó, pateó o la maltrato físicamente con mayor<br>frecuencia, en los últimos 12 meses cuántas veces lo hizo | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 236 | `S1023AA` | Para buscar ayuda acudió a: Comisaría | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 237 | `S1023AB` | Para buscar ayuda acudió a: Juzgado | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 238 | `S1023AC` | Para buscar ayuda acudió a: Fiscalía | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 239 | `S1023AD` | Para buscar ayuda acudió a: Defensoría Municipal (DEMUNA) | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 240 | `S1023AE` | Para buscar ayuda acudió a: Ministerio de la mujer (MIMP)/CEM/MINDES | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 241 | `S1023AF` | Para buscar ayuda acudió a: Defensoría del Pueblo | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 242 | `S1023AG` | Para buscar ayuda acudió a: Establecimiento de salud | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 243 | `S1023AH` | Para buscar ayuda acudió a: Organización privada | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 244 | `S1023AX` | Para buscar ayuda acudió a: Otro | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 245 | `S1023AZ` | No, nunca ha buscado ayuda | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 246 | `S1026` | Conoce el caso de alguna vecina, conocida o familiar que ha muerto por violencia de su<br>pareja o expareja | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 247 | `S1028A` | Reprende o castiga a sus hijas o hijos en el hogar: padre biológico | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 248 | `S1028B` | Reprende o castiga a sus hijas o hijos en el hogar: madre biológica | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 249 | `S1028X` | Reprende o castiga a sus hijas o hijos en el hogar: otros | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 250 | `S1028Y` | Nadie, reprende o castiga a los niños en el hogar | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 251 | `S1030AA` | De qué manera castiga padre biológico a su(s) hija(s)/hijo(s): palmadas | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 252 | `S1030AB` | De qué manera castiga padre biológico a su(s) hija(s)/hijo(s): reprimenda verbal | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 253 | `S1030AC` | De qué manera castiga padre biológico a su(s) hija(s)/hijo(s): prohibición de algo que<br>les gusta | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 254 | `S1030AD` | De qué manera castiga padre biológico a su(s) hija(s)/hijo(s): privarlos de alimentos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 255 | `S1030AE` | De qué manera castiga padre biológico a su(s) hija(s)/hijo(s): golpes y castigos físicos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 256 | `S1030AF` | De qué manera castiga padre biológico a su(s) hija(s)/hijo(s): dejándolos cerrados | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 257 | `S1030AG` | De qué manera castiga padre biológico a su(s) hija(s)/hijo(s): ignorándolos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 258 | `S1030AH` | De qué manera castiga padre biológico a su(s) hija(s)/hijo(s): poniéndoles más trabajo | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 259 | `S1030AI` | De qué manera castiga padre biológico a su(s) hija(s)/hijo(s): dejándolos fuera de la<br>casa | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 260 | `S1030AJ` | De qué manera castiga padre biológico a su(s) hija(s)/hijo(s): echándoles agua | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 261 | `S1030AK` | De qué manera castiga padre biológico a su(s) hija(s)/hijo(s): quitándoles la ropa | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 262 | `S1030AL` | De qué manera castiga padre biológico a su(s) hija(s)/hijo(s): quitándole las<br>pertenencias | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 263 | `S1030AM` | De qué manera castiga padre biológico a su(s) hija(s)/hijo(s): quitándoles el apoyo<br>económico | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 264 | `S1030AX` | De qué manera castiga padre biológico a su(s) hija(s)/hijo(s): otro | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 265 | `S1030BA` | De qué manera castiga Ud. a su(s) hija(s)/hijo(s): palmadas | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 266 | `S1030BB` | De qué manera castiga Ud. a su(s) hija(s)/hijo(s): reprimenda verbal | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 267 | `S1030BC` | De qué manera castiga Ud. a su(s) hija(s)/hijo(s): prohibición de algo que les gusta | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 268 | `S1030BD` | De qué manera castiga Ud. a su(s) hija(s)/hijo(s): privarlos de alimentos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 269 | `S1030BE` | De qué manera castiga Ud. a su(s) hija(s)/hijo(s): golpes y castigos físicos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 270 | `S1030BF` | De qué manera castiga Ud. a su(s) hija(s)/hijo(s): dejándolos cerrados | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 271 | `S1030BG` | De qué manera castiga Ud. a su(s) hija(s)/hijo(s): ignorándolos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 272 | `S1030BH` | De qué manera castiga Ud. a su(s) hija(s)/hijo(s): poniéndoles más trabajo | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 273 | `S1030BI` | De qué manera castiga Ud. a su(s) hija(s)/hijo(s): dejándolos fuera de la casa | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 274 | `S1030BJ` | De qué manera castiga Ud. a su(s) hija(s)/hijo(s): echándoles el agua | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 275 | `S1030BK` | De qué manera castiga Ud. a su(s) hija(s)/hijo(s): quitándoles la ropa | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 276 | `S1030BL` | De qué manera castiga Ud. a su(s) hija(s)/hijo(s): quitándoles las pertenencias | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 277 | `S1030BM` | De qué manera castiga Ud. a su(s) hija(s)/hijo(s): quitándoles el apoyo económico | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 278 | `S1030BX` | De qué manera castiga Ud. a su(s) hija(s)/hijo(s): otro | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 279 | `S1030CA` | De qué manera castiga esa persona a su(s) hija(s)/hijo(s): palmadas | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 280 | `S1030CB` | De qué manera castiga esa persona a su(s) hija(s)/hijo(s): reprimenda verbal | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 281 | `S1030CC` | De qué manera castiga esa persona a su(s) hija(s)/hijo(s): prohibición de algo que les<br>gusta | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 282 | `S1030CD` | De qué manera castiga esa persona a su(s) hija(s)/hijo(s): privarlos de alimentos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 283 | `S1030CE` | De qué manera castiga esa persona a su(s) hija(s)/hijo(s): golpes y castigos físicos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 284 | `S1030CF` | De qué manera castiga esa persona a su(s) hija(s)/hijo(s): dejándolos cerrados | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 285 | `S1030CG` | De qué manera castiga esa persona a su(s) hija(s)/hijo(s): ignorándolos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 286 | `S1030CH` | De qué manera castiga esa persona a su(s) hija(s)/hijo(s): poniéndoles más trabajo<br>ellos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 287 | `S1030CI` | De qué manera castiga esa persona a su(s) hija(s)/hijo(s): dejándolos fuera de la casa | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 288 | `S1030CJ` | De qué manera castiga esa persona a su(s) hija(s)/hijo(s): echándoles agua | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 289 | `S1030CK` | De qué manera castiga esa persona a su(s) hija(s)/hijo(s): quitándoles la ropa | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 290 | `S1030CL` | De qué manera castiga esa persona a su(s) hija(s)/hijo(s): quitándoles las pertenencias | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 291 | `S1030CM` | De qué manera castiga esa persona a su(s) hija(s)/hijo(s): quitándoles el apoyo<br>económico | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 292 | `S1030CX` | De qué manera castiga esa persona a su(s) hija(s)/hijo(s): otro | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 293 | `S1031` | Algunos de sus hijos fueron castigado por su mal comportamiento | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 294 | `S1032A` | De qué manera la castigan o castigaban a Ud. sus padres: palmadas | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 295 | `S1032B` | De qué manera la castigan o castigaban a Ud. sus padres: reprimenda verbal | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 296 | `S1032C` | De qué manera la castigan o castigaban a Ud. sus padres: prohibición de algo que les<br>gusta | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 297 | `S1032D` | De qué manera la castigan o castigaban a Ud. sus padres: privarla de alimentos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 298 | `S1032E` | De qué manera la castigan o castigaban a Ud. sus padres: golpes y castigos físicos | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 299 | `S1032F` | De qué manera la castigan o castigaban a Ud. sus padres: quemándola | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 300 | `S1032G` | De qué manera la castigan o castigaban a Ud. sus padres: dejándola cerrada | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 301 | `S1032H` | De qué manera la castigan o castigaban a Ud. sus padres: ignorándola | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 302 | `S1032I` | De qué manera la castigan o castigaban a Ud. sus padres: ponerle más trabajo | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 303 | `S1032J` | De qué manera la castigan o castigaban a Ud. sus padres: dejándola fuera de la casa | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 304 | `S1032K` | De qué manera la castigan o castigaban a Ud. sus padres: hundiéndola en agua | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 305 | `S1032L` | De qué manera la castigan o castigaban a Ud. sus padres: quitándole la ropa | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 306 | `S1032M` | De qué manera la castigan o castigaban a Ud. sus padres: quitándole sus pertenencias | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 307 | `S1032N` | De qué manera la castigan o castigaban a Ud. sus padres: quitándole el apoyo<br>económico | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 308 | `S1032X` | De qué manera la castigan o castigaban a Ud. sus padres: otro | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 309 | `S1032Y` | No la castigaban/No la castigan | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 310 | `S1033` | Cree Ud. que para la educación de los niños es necesario el castigo físico | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 311 | `S1034A` | Presencia de niños menores de 10 años | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 312 | `S1034B` | Presencia de niños mayores de 10 años | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 313 | `Q479A` | En los últimos 12 meses participó en reuniones o sesiones demostrativas sobre<br>preparación de alimentos por el MINSA | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 314 | `Q479B` | En los últimos 12 meses en cuántas sesiones demostrativas participó | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 315 | `Q479C` | En los últimos 12 meses recibió la visita del MINSA para aconsejarle de la alimentación,<br>nutrición y/o lactancia de su niña(o) | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 316 | `Q479D` | En los últimos 12 meses cuantas visitas recibió | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 317 | `QI479E_A` | ¿Qué síntomas tendría su niña(o) si tuviera anemia.... Cansancio, mucho sueño y<br>palidez? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 318 | `QI479E_B` | ¿Qué síntomas tendría su niña(o) si tuviera anemia... Alteraciones del desarrollo<br>Psicomotor? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 319 | `QI479E_C` | ¿Qué síntomas tendría su niña(o) si tuviera anemia... Pérdida de apetito, bajo peso? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 320 | `QI479E_D` | ¿Qué síntomas tendría su niña(o) si tuviera anemia... Dolor de cabeza, mareos? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 321 | `QI479E_E` | ¿Qué síntomas tendría su niña(o) si tuviera anemia... Piel seca, caida de cabello, uñas<br>quebradas y aplanadas? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 322 | `QI479E_F` | ¿Qué síntomas tendría su niña(o) si tuviera anemia... Comer tierra, hielo, uñas, cabello,<br>pasta de dientes entre otros? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 323 | `QI479E_G` | ¿Qué síntomas tendría su niña(o) si tuviera anemia... Vómitos, diarrea, fiebre, tos? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 324 | `QI479E_H` | ¿Qué síntomas tendría su niña(o) si tuviera anemia... Dolor muscular? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 325 | `QI479E_I` | ¿Qué síntomas tendría su niña(o) si tuviera anemia... Falta de sueño? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 326 | `QI479E_J` | ¿Qué síntomas tendría su niña(o) si tuviera anemia... No tiene síntomas? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 327 | `QI479E_X` | ¿Qué síntomas tendría su niña(o) si tuviera anemia... Otro? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 328 | `QI479E_Y` | ¿No sabe/no recuerda? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 329 | `QI479F_A` | ¿Qué alimentos le ofrecería a su niña(o)......Carnes rojas, visceras, sangrecita? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 330 | `QI479F_B` | ¿Qué alimentos le ofrecería a su niña(o)......Otras carnes y pescados? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 331 | `QI479F_C` | ¿Qué alimentos le ofrecería a su niña(o)......Lentejas y otras menestras? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 332 | `QI479F_D` | ¿Qué alimentos le ofrecería a su niña(o)......Verduras de hojas verdes, alfalfa? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 333 | `QI479F_E` | ¿Qué alimentos le ofrecería a su niña(o)......Jugo de naranja, limonada? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 334 | `QI479F_F` | ¿Qué alimentos le ofrecería a su niña(o)......Fruta? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 335 | `QI479F_G` | ¿Qué alimentos le ofrecería a su niña(o)......Frutas secas? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 336 | `QI479F_H` | ¿Qué alimentos le ofrecería a su niña(o)......Huevo, leche y derivados? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 337 | `QI479F_I` | ¿Qué alimentos le ofrecería a su niña(o)......Arroz y tubérculos? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 338 | `QI479F_J` | ¿Qué alimentos le ofrecería a su niña(o)......Arroz fortificado con hierro? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 339 | `QI479F_K` | ¿Qué alimentos le ofrecería a su niña(o)......Hierro (Sulfato ferroso o similar)? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 340 | `QI479F_L` | ¿Qué alimentos le ofrecería a su niña(o)......Calcio? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 341 | `QI479F_M` | ¿Qué alimentos le ofrecería a su niña(o)......Vitaminas? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 342 | `QI479F_X` | ¿Qué alimentos le ofrecería a su niña(o)......Otro? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |
| 343 | `QI479F_Y` | ¿Qué alimentos le ofrecería a su niña(o)......No sabe/no recuerda? | **EXCLUIR POR IRRELEVANCIA** | Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión. |


### 📁 Archivo: `Diccionario - DIT.pdf` — Módulo: `1036-inmunizacion`
**Total de variables evaluadas:** 63

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Identificadores relacionales del niño en el módulo de Desarrollo Infantil Temprano. |
| 2 | `CASEID` | Case Identification | **METADATO / LLAVE** | Identificadores relacionales del niño en el módulo de Desarrollo Infantil Temprano. |
| 3 | `BIDX` | Número de orden de nacimeinto | **METADATO / LLAVE** | Identificadores relacionales del niño en el módulo de Desarrollo Infantil Temprano. |
| 4 | `BORD` | Número de orden en la historia de nacimiento | **METADATO / LLAVE** | Identificadores relacionales del niño en el módulo de Desarrollo Infantil Temprano. |
| 5 | `QI478` | Edad en meses | **INCLUIR** | Edad del niño en meses en el módulo DIT. |
| 6 | `QI478A` | Vive con la madre y no tiene discapacidad | **INCLUIR** | Niño vive con la madre y presencia de discapacidad. |
| 7 | `QI478E1` | De estas figuras, Cuál o cuáles de las siguientes acciones generalmente realiza | **DUDOSA (BIDIRECCIONALIDAD)** | Hitos motores gruesos (pararse, caminar). El retardo estatural severo retrasa la deambulación; posible consecuencia en vez de predictor. |
| 8 | `QI478E2` | En el lugar en el cual pasa mayor tiempo, Tiene un espacio sin objetos en el que pueda<br>desplazarse/caminar libremente | **INCLUIR** | Espacio libre para desplazarse y gatear/caminar en el hogar. Estimulación psicomotriz y entorno seguro. |
| 9 | `QI478E3` | Trata de imitar las palabras que escucha | **INCLUIR** | Pautas de estimulación temprana y lenguaje (madre habla, lee o canta al infante). |
| 10 | `QI478E4` | Entiende cuando Ud. le dice NO aunque no le haga caso | **INCLUIR** | Pautas de estimulación temprana y lenguaje (madre habla, lee o canta al infante). |
| 11 | `QI478E5` | Entiende una orden sencilla como por ejemplo "dame" o "toma" | **INCLUIR** | Pautas de estimulación temprana y lenguaje (madre habla, lee o canta al infante). |
| 12 | `QI478E6` | Cuando está con ella/él, Ud. le habla de lo que están haciendo en ese momento | **INCLUIR** | Pautas de estimulación temprana y lenguaje (madre habla, lee o canta al infante). |
| 13 | `QI478E7` | Cuando usted la(o) carga generalmente se tira hacia atrás, se niega a que se le cargue,<br>se pone tiesa(o) o la empuja | **INCLUIR** | Interacción afectiva y apego seguro entre cuidador y niño. |
| 14 | `QI478E8` | Cuando está con Ud., ella (él) generalmente está tensa (o), ansiosa (o), angustiada (o),<br>indiferente o aburrida (o) | **INCLUIR** | Interacción afectiva y apego seguro entre cuidador y niño. |
| 15 | `QI478E9` | Generalmente es impaciente, protesta e insiste a menos que Ud. haga lo que ella (él)<br>quiere | **INCLUIR** | Interacción afectiva y apego seguro entre cuidador y niño. |
| 16 | `QI478E10` | Si llora cuando Ud. está haciendo algo generalmente : qué hace Ud. | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 17 | `QI478F1` | De estas figuras: cuál o cuáles son las que generalmente realiza | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 18 | `QI478F2_A` | En el lugar donde generalmente juega: Hay objetos pesados que le pueden caer encima | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 19 | `QI478F2_B` | En el lugar donde generalmente juega: Hay objetos con los que se puede cortar | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 20 | `QI478F2_C` | En el lugar donde generalmente juega: El lugar donde normalmente juega, está cerca de<br>desperdicios o basura como restos de alimentos | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 21 | `QI478F2_D` | En el lugar donde generalmente juega: En ese lugar hay elementos tóxicos como<br>detergentes, insecticidas al alcance de ella/él | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 22 | `QI478F2_E` | En el lugar donde generalmente juega: Está fuera de la casa y cerca de pistas,<br>carreteras, acequias o abismos | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 23 | `QI478F3` | Cuando ella (él) quiere algo, pide con palabras | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 24 | `QI478F4` | Cuando se le pide a ella (él) que lleve de un lugar a otro un objeto que conoce como<br>alguno de sus juguetes: lo hace | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 25 | `QI478F5` | Cuando se le pide a ella (él) que haga algo sin Ud. mostrarle cómo hacerlo: lo hace | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 26 | `QI478F6` | Cuando está con ella (el) Ud. le habla de lo que están haciendo en ese momento | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 27 | `QI478G1` | Ella (él) Nombra las partes de su cuerpo | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 28 | `QI478G2_A` | Cuando ella (él) habla: usa palabras | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 29 | `QI478G2_B` | Cuando ella (él) habla: Usa palabras que todas las personas entienden | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 30 | `QI478G2_C` | Cuando ella (él) habla: Usa frases de 2 a 4 palabras que todas las personas entienden | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 31 | `QI478G3` | Cuando Ud. le pide a ella (él) que coja un objeto que no está a la vista y que luego lo<br>coloque donde Ud. le indica sin mostrarle cómo hacerlo, lo hace | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 32 | `QI478G4` | Ella (él) generalmente participa en las conversaciones con adultos | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 33 | `QI478H1` | Cuando ella (él) habla dice frases con un sujeto y una acción como “bebé llora” | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 34 | `QI478H2` | Cuando ella (él) habla dice oraciones como “vamos a la casa”, “dónde está la abuela”, “mi<br>mamá es linda” | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 35 | `QI478H3` | Ella (él) entiende palabras que indican la posición de las cosas como dentro y fuera o<br>encima y debajo | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 36 | `QI478H4` | Ella (él) generalmente participa en las conversaciones con adultos | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 37 | `QI478H5` | Cuando ella (él) hace un garabato o dibujo dice lo que dibujó | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 38 | `QI478H6` | Ella (él) imita lo que hace una persona o personaje cuando esta(este) no se encuentra<br>presente | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 39 | `QI478H7` | Ella (él) le habla a sus muñecos o juguetes | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 40 | `QI478H8_A` | En casa ella (él) tiene: materiales especialmente hechos para jugar como una pelota o<br>una muñeca | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 41 | `QI478H8_B` | En casa tella (él) tiene otros materiales con los que puede jugar como bloques, palitos,<br>botellas, lápices o algún tipo de papel | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 42 | `QI478H9` | Ella (él) llora, grita o hace pataleta la mayor parte del tiempo | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 43 | `QI478H10` | Cuando ella (él) quiere algo y Ud. le dice que espere generalmente espera “tranquila(o)” | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 44 | `QI478H11` | Cuando ella (él) quiere algo y Ud. le dice que NO, generalmente se hace daño, agrede a<br>los demás o daña las cosas | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 45 | `QI478H12` | En los ùltimos 15 dìas, cuántas veces Ud. le ha dado un palmazo, le ha jalado de los<br>cabellos o la oreja o le ha golpeado con un objeto en cualquier parte de su cuerpo a ella<br>(él) de 1 a 3 veces, de 4 a 6 veces o más de 6 veces | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 46 | `QI478I1` | Cuando ella (él) dibuja una persona a cuál de estas figuras se parece más su dibujo | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 47 | `QI478I2` | Cuando ella (él) juega dice que las cosas o muñecos tienen emociones o sensaciones,<br>es decir que están contentos, molestos, tienen hambre o frio, etc. | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 48 | `QI478I3` | Ella (él) juega a ser un personaje de televisión, o de cuentos como superhéroes,<br>princesas, el lobo feroz o un animalito | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 49 | `QI478I4_A` | En casa ella (él) tiene Materiales especialmente hechos para jugar como una pelota o<br>una muñeca | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 50 | `QI478I4_B` | En casa ella (él) Tiene otros materiales con los que puede jugar como bloques, palitos,<br>botellas, lápices o algún tipo de papel | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 51 | `QI478I5` | Ella (él) Llora, grita o hace pataletas la mayor parte del tiempo | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 52 | `QI478I6` | Cuando ella (él) quiere algo y Ud. le dice que espere generalmente espera tranquila(o) | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 53 | `QI478I7` | Cuando ella (él) quiere algo y Ud. le dice que NO, generalmente se hace daño, agrede a<br>los demás o daña las cosas | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 54 | `QI478I8` | En los ùltimos 15 dìas, cuántas veces Ud. le ha dado un palmazo, le ha jalado de los<br>cabellos o la oreja o le ha golpeado con un objeto en cualquier parte de su cuerpo, de 1 a<br>3 veces, de 4 a 6 veces o más de 6 veces | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 55 | `QI478J1` | Ella (él) Juega de mentirita, es decir juega con cosas que no tiene en ese momento} | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 56 | `QI478J2` | Cuando ella (él) Juega sola(o), juega a ser otra persona | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 57 | `QI478J3` | Cuando ella (él) juega con otras(os) niñas(os), es un personaje como la mamá, el<br>monstruo o un animalito | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 58 | `QI478J4_A` | En casa ella (él) Tiene materiales especialmente hechos para jugar como una pelota o<br>una muñeca | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 59 | `QI478J4_B` | En casa ella (él) Tiene otros materiales con los que puede jugar como bloques, palitos,<br>botellas, lápices o algún tipo de papel | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 60 | `QI478J5` | Ella (él) Llora, grita o hace pataletas la mayor parte del tiempo | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 61 | `QI478J6` | Cuando ella (él) quiere algo y Ud. le dice que espere generalmente espera tranquila(o) | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 62 | `QI478J7` | Cuando ella (él) quiere algo y Ud. le dice que NO, generalmente se hace daño, agrede a<br>los demás o daña las cosas | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |
| 63 | `QI478J8` | En los ùltimos 15 dìas, cuántas veces Ud. le ha dado un palmazo, le ha jalado de los<br>cabellos o la oreja o le ha golpeado con un objeto en cualquier parte de su cuerpo, de 1 a<br>3 veces, de 4 a 6 veces o más de 6 veces | **EXCLUIR POR IRRELEVANCIA** | Ítems secundarios del test DIT no extrapolables a población menor de 24 meses. |


### 📁 Archivo: `Diccionario - REC42.pdf` — Módulo: `1036-inmunizacion`
**Total de variables evaluadas:** 169

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Identificadores del niño e historial reproductivo. |
| 2 | `CASEID` | Identificación Cuestionario Individual | **METADATO / LLAVE** | Identificadores del niño e historial reproductivo. |
| 3 | `V401` | Último parto por cesárea | **METADATO / LLAVE** | Identificadores del niño e historial reproductivo. |
| 4 | `V404` | Actualmente amamantando | **METADATO / LLAVE** | Identificadores del niño e historial reproductivo. |
| 5 | `V405` | Actualmente amenorreico | **METADATO / LLAVE** | Identificadores del niño e historial reproductivo. |
| 6 | `V406` | Actualmente abstinencia | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 7 | `V407` | Veces que amamanta durante la noche | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 8 | `V408` | Veces que amamanta durante el día | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 9 | `V409` | Ayer durante el dìa o la noche dio agua sola al niño | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 10 | `V409A` | Ayer durante el dìa o la noche dio agua azucarada | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 11 | `V410` | Ayer durante el dìa o la noche dio jugo de fruta al niño | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 12 | `V410A` | Ayer durante el dìa o la noche dio al niño té o café | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 13 | `V411` | Ayer durante el dìa o la noche dio al niño leche materna refrigerada/conservada | **INCLUIR** | El niño tuvo diarrea en las últimas dos semanas. CAUSA INMEDIATA DIRECTA (UNICEF): atrofia de vellosidades intestinales y mala absorción crónica. |
| 14 | `V411A` | Ayer durante el dìa o la noche dio al niño leche en polvo (NAM, S26, SIMILAC etc.) | **INCLUIR** | Diarrea con sangre en heces (disentería). Infección invasiva bacteriana destructiva de mucosa entérica. |
| 15 | `V412` | Ayer durante el dìa o la noche dio al niño otra leche fresca, evaporada o en polvo | **INCLUIR** | Recibió atención médica por el episodio diarreico. Acceso oportuno a tratamiento. |
| 16 | `V412A` | Ayer durante el dìa o la noche dio al niño cereales para bebés | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 17 | `V412B` | Ayer durante el dìa o la noche dio al niño otros cereales | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 18 | `V413` | Ayer durante el dìa o la noche dio al niño otro líquido como bebidas gaseosas, caldo | **INCLUIR** | Tratamiento de diarrea con Sales de Rehidratación Oral (SRO). Prevención de deshidratación grave. |
| 19 | `V413A` | Ayer durante el dìa o la noche dio líquido CS infantil | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 20 | `V413B` | Ayer durante el dìa o la noche dio líquido CS infantil | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 21 | `V413C` | Ayer durante el dìa o la noche dio líquido CS infantil | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 22 | `V413D` | Ayer durante el dìa o la noche dio líquido CS infantil | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 23 | `V414A` | Ayer durante el dìa o la noche dio al niño naranjas mandarina, lima, maracuyá, toronja | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 24 | `V414B` | Ayer durante el dìa o la noche dio al niño papillas de programas sociales | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 25 | `V414C` | Ayer durante el dìa o la noche dio al niño frutas secas | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 26 | `V414D` | Ayer durante el dìa o la noche dio alimentos CS para niños | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 27 | `V414E` | Ayer durante el dìa o la noche dio al niño harina, pan, fideos, galletas u cualquier comida<br>hecha de cereales | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 28 | `V414F` | Ayer durante el dìa o la noche dio al niño comida hecha de tubérculos o raíces (papas,<br>yuca, olluco, oca, mashua) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 29 | `V414G` | Ayer durante el dìa o la noche dio al niño huevos | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 30 | `V414H` | Ayer durante el dìa o la noche dio al niño carne de res, pollo, pescado, mariscos, otras<br>carnes, hígado, mondongo, otras vísceras | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 31 | `V414I` | Ayer durante el dìa o la noche dio al niño camote, zanahorias, zapallo | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 32 | `V414J` | Ayer durante el dìa o la noche dio al niño cualquier vegetal de hoja verde oscuro<br>(espinaca, acelga etc.) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 33 | `V414K` | Ayer durante el dìa o la noche dio al niño mango, papaya aguaje y otras frutas de<br>vitamina A | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 34 | `V414L` | Ayer durante el dìa o la noche dio al niño otras frutas (plátano de isla, plátano de seda,<br>maduro, manzana, palta etc.) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 35 | `V414M` | Ayer durante el dìa o la noche dio hígado, corazón y otros órganos al niño | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 36 | `V414N` | Ayer durante el dìa o la noche dio al niño pescado o mariscos | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 37 | `V414O` | Ayer durante el dìa o la noche dio al niño habas, frijol, lenteja, soya, pallares, garbanzo,<br>arvejas | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 38 | `V414P` | Ayer durante el dìa o la noche dio al niño queso, yogurt u otros productos lácteos (leche<br>asada, helados, crema volteada, etc.) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 39 | `V414Q` | Ayer durante el dìa o la noche dio al niño comida hecha con aceite, grasas, mantequilla,<br>productos hechos de ellos | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 40 | `V414R` | Ayer durante el dìa o la noche dio al niño alimento azucarado como chocolates,<br>caramelos u otros | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 41 | `V414S` | Ayer durante el dìa o la noche dio al niño otro alimento sólido-semisólido | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 42 | `V414T` | Ayer durante el dìa o la noche dio alimentos CS para niños | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 43 | `V414U` | Ayer durante el dìa o la noche dio alimentos CS para niños | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 44 | `V414H1` | Ayer durante el dìa o la noche dio al niño carne de res, hígado, otras vísceras | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 45 | `V414H2` | Ayer durante el dìa o la noche dio al niño carne de pollo, pescado, mariscos, mondongo,<br>otras carnes | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 46 | `V415` | El día de ayer o anoche tomó algo en biberón | **INCLUIR** | El niño tuvo tos o dificultad para respirar (IRA reciente) en las últimas dos semanas. |
| 47 | `V416` | Ha oído hablar de las Sales de Rehidratación Oral/Bolsa salvadora o del frutiflex,<br>electrolite u otro similar | **INCLUIR** | Signos de neumonía aguda (respiración rápida o pecho hundido). |
| 48 | `V417` | Ingreso en la tabla de maternidad | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 49 | `V418` | Ingreso en la tabla de salud | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 50 | `V419` | Ingreso en la tabla de altura/peso | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 51 | `V420` | Código de registrador | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 52 | `V421` | Código de asistente de registrador | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 53 | `V426` | Cuando empezó a darle el pecho al niño | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 54 | `V437` | Peso de entrevistada (kilos-1d) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 55 | `V438` | Talla de entrevistada (cms-1d) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 56 | `V439` | T/E Percentil (ent) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 57 | `V440` | T/E Desviación Estándar (ent) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 58 | `V441` | T/E Porcentaje ref. mediana (ent) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 59 | `V442` | P/T Porcentaje ref. mediana (DHS | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 60 | `V443` | P/T Porcentaje ref. mediana (Fog) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 61 | `V444` | P/T Porcentaje ref. mediana (WHO) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 62 | `V444A` | P/T Desviación estandar (ent) DHS | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 63 | `V445` | Índice de masa corporal para la MEF | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 64 | `V446` | Índice de Rohrer para la MEF | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 65 | `V447` | Resultado de la medición de la MEF | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 66 | `V447A` | Edad de mujer en años del reporte de hogar | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 67 | `V452A` | Menores de 18 años (informe HH) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 68 | `V452B` | Nº de orden de padre-apoderado | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 69 | `V452C` | Leyó declaración de consentimiento | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 70 | `V453` | Nivel de hemoglobina (g/dl - 1 decimal) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 71 | `V454` | Actualmente embarazada (informe del hogar) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 72 | `V455` | Resultado de medir (hemoglobina) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 73 | `V456` | Nivel de hemoglobina ajustado por altitud (g/dl - 1 decimal) RM 363-2022-MINSA | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 74 | `V456A` | Nivel de hemoglobina ajustada por altitud en g/dl - 1 decimal NUEVA DIRECTRIZ OMS<br>2024/RM 251-2024-MINSA | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 75 | `V457` | Nivel de anemia RM 363-2022-MINSA | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 76 | `V457A` | Nivel de Anemia NUEVA DIRECTRIZ OMS 2024/RM 251-2024-MINSA | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 77 | `V458` | De acuerdo con la referencia | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 78 | `V459` | Tener mosquiteros para dormir (informe del hogar) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 79 | `V460` | Los niños menores de 5 dormían bajo el mosquitero anoche (informe HH) | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 80 | `V461` | La MEF durmió debajo de mosquitero | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 81 | `V462` | Se lavaron las manos antes de preparar la última comida | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 82 | `V463A` | Fuma cigarrillos | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 83 | `V463B` | Pipa de humo | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 84 | `V463C` | Mascando tabaco | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 85 | `V463D` | Utiliza tabaco | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 86 | `V463E` | Fuma específico del país | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 87 | `V463F` | Fuma específico del país | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 88 | `V463G` | Fuma específico del país | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 89 | `V463X` | Fuma otro | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 90 | `V463Z` | No fuma | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 91 | `V464` | Número de cigarrillos que fumó en las últimas 24 horas | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 92 | `V465` | Eliminación de las heces de su niña(o) cuando no usa el baño | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 93 | `V466` | Cuando el niño está gravemente enfermo, Ud. puede decidir de llevarlo a tratamiento<br>médico | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 94 | `V467A` | Cuando Ud. se enferma es un gran problema: saber a dónde ir | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 95 | `V467B` | Cuando Ud. se enferma es un gran problema: conseguir permiso para ir | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 96 | `V467C` | Cuando Ud. se enferma es un gran problema: conseguir el dinero para el tratamiento | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 97 | `V467D` | Cuando Ud. se enferma es un gran problema: lejanía de servicios de salud | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 98 | `V467E` | Obtener ayuda médica para uno mismo: conseguir transporte | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 99 | `V467F` | Cuando Ud. se enferma es un gran problema: no querer ir sola | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 100 | `V467G` | Cuando Ud. se enferma es un gran problema: tal vez no haya personal femenino | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 101 | `V467H` | Cuando Ud. se enferma es un gran problema: tal vez no haya personal de salud | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 102 | `V467I` | Cuando Ud. se enferma es un gran problema: tal vez no haya medicamentos | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 103 | `V467J` | Cuando Ud. se enferma es un gran problema: CS | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 104 | `V467K` | Cuando Ud. se enferma es un gran problema: CS | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 105 | `V467L` | Cuando Ud. se enferma es un gran problema: CS | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 106 | `V467M` | Cuando Ud. se enferma es un gran problema: CS | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 107 | `V468` | Columnas usadas solo para variables del último nacimiento | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 108 | `V471A` | La madre tenía leche enlatada, en polvo o fresca | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 109 | `V471B` | La madre tenía té o café | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 110 | `V471C` | La madre tenía cualquier otro líquido | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 111 | `V471D` | La madre tenía líquido CS | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 112 | `V471E` | La madre tenía líquido CS | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 113 | `V471F` | La madre tenía líquido CS | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 114 | `V471G` | La madre tenía líquido CS | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 115 | `V472A` | La madre tenía alimentos CS | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 116 | `V472B` | La madre tenía alimentos CS | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 117 | `V472C` | La madre tenía alimentos CS | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 118 | `V472D` | La madre tenía alimentos CS | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 119 | `V472E` | La madre tenía pan, fideos, otros hechos de granos | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 120 | `V472F` | La madre tenía papas, cassaves u otros tubérculos | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 121 | `V472G` | La madre tenía huevos | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 122 | `V472H` | La madre tenía carne (ternera, cerdo, cordero, pollo, etc.) | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 123 | `V472I` | La madre tenía pumpink, zanahorias, squash (amarillo o naranja en el interior) | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 124 | `V472J` | La madre tenía verduras de hoja verde oscuro | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 125 | `V472K` | La madre tenía mangos, papayas y otras frutas con vitamina A | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 126 | `V472L` | La madre tenía otros fuits | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 127 | `V472M` | La madre tenía hígado, corazón y otros órganos | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 128 | `V472N` | La madre tenía pescado o marisco | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 129 | `V472O` | La madre tenía comida hecha de frijoles, guisantes, lentis, nueces | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 130 | `V472P` | La madre tenía queso, yogur y otros productos lácteos | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 131 | `V472Q` | La madre tenía aceite, grasas, mantequilla, productos hechos de ellos | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 132 | `V472R` | La madre tenía chocolates, dulces, dulces, pasteles, etc. | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 133 | `V472S` | La madre tenía otros alimentos sólidos semisólidos | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 134 | `V472T` | La madre tenía alimentos CS | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 135 | `V472U` | La madre tenía alimentos CS | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 136 | `V473A` | Leyó declaración de consentimiento (VIH) | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 137 | `V473B` | Resultado de medir (VIH) | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 138 | `V474` | Escuchó sobre la Tuberculosis o TBC | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 139 | `V474A` | La tuberculosis es transmitida de una persona a otra: a través del aire al toser/estornudar | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 140 | `V474B` | La tuberculosis es transmitida de una persona a otra: al compartir utensilios | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 141 | `V474C` | La tuberculosis es transmitida de una persona a otra: tocando a una persona con TBC | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 142 | `V474D` | La tuberculosis es transmitida de una persona a otra: a través de los alimentos | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 143 | `V474E` | La tuberculosis es transmitida de una persona a otra: por contacto sexual | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 144 | `V474F` | La tuberculosis es transmitida de una persona a otra: por picadura de mosquito | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 145 | `V474G` | La tuberculosis es transmitida de una persona a otra: CS | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 146 | `V474H` | La tuberculosis es transmitida de una persona a otra: CS | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 147 | `V474I` | La tuberculosis es transmitida de una persona a otra: CS | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 148 | `V474J` | La tuberculosis es transmitida de una persona a otra: CS | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 149 | `V474X` | La tuberculosis es transmitida de una persona a otra: otro | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 150 | `V474Z` | La tuberculosis es transmitida de una persona a otra: No sabe | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 151 | `V475` | Puede curarse la tuberculosis | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 152 | `V476` | Guardaría en secreto si un familiar tuviera TBC | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 153 | `V477` | Número de inyecciones en los últimos 12 meses | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 154 | `V478` | Inyecciones administradas por un trabajador de salud | **INCLUIR** | Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima. |
| 155 | `V479` | Fuente para inyección por el trabajador de salud | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 156 | `V480` | Jeringa y aguja de un paquete nuevo sin abrir | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 157 | `V481` | Cobertura de seguro de salud | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 158 | `V481A` | Tipo de seguro de salud: organización mutual/comunitaria | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 159 | `V481B` | Tipo de seguro de salud: proporcionado por el empleador | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 160 | `V481C` | Tipo de seguro de salud: seguridad social | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 161 | `V481D` | Tipo de seguro de salud: privado | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 162 | `V481E` | Tipo de seguro de salud: ESSALUD/IPSS | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 163 | `V481F` | Tipo de seguro de salud: fuerzas armadas/policiales | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 164 | `V481G` | Tipo de seguro de salud: Seguro Integral de Salud | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 165 | `V481H` | Tipo de seguro de salud: entidad prestadora de salud | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 166 | `V481X` | Tipo de seguro de salud: otro | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 167 | `V482A` | Organice el cuidado de niños biológicos menores de 18 años | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 168 | `V482B` | Cuidado principal de hijos menores de 18 años | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |
| 169 | `V482C` | Organizar el cuidado de niños no biológicos menores 18 | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de marcas comerciales de medicamentos o preguntas de control. |


### 📁 Archivo: `Diccionario - REC43.pdf` — Módulo: `1036-inmunizacion`
**Total de variables evaluadas:** 168

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Identificadores relacionales del niño en el registro de vacunación. |
| 2 | `CASEID` | Identificación Cuestionario Individual | **METADATO / LLAVE** | Identificadores relacionales del niño en el registro de vacunación. |
| 3 | `HIDX` | Nro. orden de historia de nacimiento | **METADATO / LLAVE** | Identificadores relacionales del niño en el registro de vacunación. |
| 4 | `H1` | Tiene el carné de atención integral de la niña(o) | **INCLUIR** | Tenencia de carné de vacunación físico visto por encuestadora. Indicador de contacto formal con el sistema de salud. |
| 5 | `H2` | Recibió vacuna BCG | **INCLUIR** | Vacuna BCG (dosis única al nacer contra tuberculosis meníngea). |
| 6 | `H2D` | Día Vacuna BCG | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 7 | `H2M` | Mes Vacuna BCG | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 8 | `H2Y` | Año Vacuna BCG | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 9 | `H3` | Recibió vacuna DPT 1ra. dosis | **INCLUIR** | Dosis 1, 2 y 3 de vacuna Pentavalente (Difteria, Tétanos, Tos Ferina, Hepatitis B, Hib). Inmunización básica. |
| 10 | `H3D` | Vacuna DPT 1ra. dosis día | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 11 | `H3M` | Vacuna DPT 1ra. dosis mes | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 12 | `H3Y` | Vacuna DPT 1ra. dosis año | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 13 | `H4` | Recibió vacuna POLIO 1ra. dosis | **INCLUIR** | Dosis 1, 2 y 3 de vacuna antipolio. |
| 14 | `H4D` | Vacuna POLIO 1ra. dosis día | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 15 | `H4M` | Vacuna POLIO 1ra. dosis mes | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 16 | `H4Y` | Vacuna POLIO 1ra. dosis año | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 17 | `H5` | Recibió vacuna DPT 2da. dosis | **INCLUIR** | Dosis 1, 2 y 3 de vacuna Pentavalente (Difteria, Tétanos, Tos Ferina, Hepatitis B, Hib). Inmunización básica. |
| 18 | `H5D` | Vacuna DPT 2da. dosis día | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 19 | `H5M` | Vacuna DPT 2da. dosis mes | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 20 | `H5Y` | Vacuna DPT 2da. dosis año | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 21 | `H6` | Recibió vacuna POLIO 2da. dosis | **INCLUIR** | Dosis 1, 2 y 3 de vacuna antipolio. |
| 22 | `H6D` | Vacuna POLIO 2da. dosis día | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 23 | `H6M` | Vacuna POLIO 2da. dosis mes | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 24 | `H6Y` | Vacuna POLIO 2da. dosis año | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 25 | `H7` | Vacuna DPT Recibió 3 | **INCLUIR** | Dosis 1, 2 y 3 de vacuna Pentavalente (Difteria, Tétanos, Tos Ferina, Hepatitis B, Hib). Inmunización básica. |
| 26 | `H7D` | Vacuna DPT 3ra. dosis día | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 27 | `H7M` | Vacuna DPT 3ra. dosis mes | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 28 | `H7Y` | Vacuna DPT 3ra. dosis año | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 29 | `H8` | Recibió vacuna POLIO 3ra. dosis | **INCLUIR** | Dosis 1, 2 y 3 de vacuna antipolio. |
| 30 | `H8D` | Vacuna POLIO 3ra. dosis día | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 31 | `H8M` | Vacuna POLIO 3ra. dosis mes | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 32 | `H8Y` | Vacuna POLIO 3ra. dosis año | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 33 | `H9` | Recibió vacuna contra el SARAMPIÓN | **INCLUIR** | Dosis 1 y 2 de vacuna SPR (Sarampión, Paperas, Rubeola). El sarampión desencadena desnutrición severa post-infecciosa. |
| 34 | `H9D` | Vacuna SARAMPIÓN día | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 35 | `H9M` | Vacuna SARAMPIÓN mes | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 36 | `H9Y` | Vacuna SARAMPIÓN año | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 37 | `H0` | Recibió vacuna POLIO 0 | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 38 | `H0D` | Vacuna POLIO 0 día | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 39 | `H0M` | Vacuna POLIO 0 mes | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 40 | `H0Y` | Vacuna POLIO 0 año | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 41 | `H10` | Alguna vez tuvo vacunación | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 42 | `H11` | En los últimos 14 dìas, ha tenido diarrea la niña(o) | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 43 | `H11B` | Había sangre en las deposiciones de la niña(o) | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 44 | `H12A` | Busco D97:D148 para la diarrea: hospital MINSA | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 45 | `H12B` | Busco tratamiento para la diarrea: centro de salud MINSA | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 46 | `H12C` | Busco tratamiento para la diarrea: puesto de salud MINSA | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 47 | `H12D` | Busco tratamiento para la diarrea: clínica móvil | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 48 | `H12E` | Busco tratamiento para la diarrea: promotor de salud | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 49 | `H12F` | Busco tratamiento para la diarrea: hospital ESSALUD | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 50 | `H12G` | Busco tratamiento para la diarrea: hospital FF.AA. - P.N.P. | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 51 | `H12H` | Busco tratamiento para la diarrea: policlìnico/centro/posta ESSALUD | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 52 | `H12I` | Busco tratamiento para la diarrea: hospital/otro de la Municipalidad | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 53 | `H12J` | Busco tratamiento para la diarrea: clínica particular | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 54 | `H12K` | Busco tratamiento para la diarrea: farmacia/botica | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 55 | `H12L` | Busco tratamiento para la diarrea: consultorio médico particular | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 56 | `H12M` | Busco tratamiento para la diarrea: clínica móvil privado | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 57 | `H12N` | Busco tratamiento para la diarrea: trabajador de la salud | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 58 | `H12O` | Busco tratamiento para la diarrea: botiquín popular | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 59 | `H12P` | Busco tratamiento para la diarrea: clínica/Posta de ONG | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 60 | `H12Q` | Busco tratamiento para la diarrea: hospital/Otro de la iglesia | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 61 | `H12R` | Busco tratamiento para la diarrea: otra | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 62 | `H12S` | Busco tratamiento para la diarrea: comprar | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 63 | `H12T` | Busco tratamiento para la diarrea: curandero | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 64 | `H12U` | Busco tratamiento para la diarrea: amigo/pariente | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 65 | `H12V` | Busco tratamiento para la diarrea: CS oth.priv sector | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 66 | `H12W` | Busco tratamiento para la diarrea: CS oth.priv sector | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 67 | `H12X` | Busco tratamiento para la diarrea: Otro | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 68 | `H12Y` | Busco tratamiento para la diarrea: sin tratamiento | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 69 | `H12Z` | Busco tratamiento para la diarrea: tratamiento médico | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 70 | `H13` | Dio al niño sales de rehidratación oral | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 71 | `H13B` | Le dio: frutiflex/electrolite | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 72 | `H14` | Le dio: suero casero | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 73 | `H15` | Que más le dieron para tratar la diarrea: antibióticos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 74 | `H15A` | Que más le dieron para tratar la diarrea: jarabe para la diarrea | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 75 | `H15B` | Que más le dieron para tratar la diarrea: inyección de antibiótico | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 76 | `H15C` | Que más le dieron para tratar la diarrea: suero intravenoso | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 77 | `H15D` | Que más le dieron para tratar la diarrea: remedios caseros, hierbas medicinales. | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 78 | `H15E` | Que más le dieron para tratar la diarrea: pastillas zinc | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 79 | `H15F` | Que más le dieron para tratar la diarrea: otro (no antibiótico, antimotilidad, zinc) | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 80 | `H15G` | Que más le dieron para tratar la diarrea: pastilla o jarabe desconocido | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 81 | `H15H` | Que más le dieron para tratar la diarrea: inyección no antibiótica | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 82 | `H15I` | Que más le dieron para tratar la diarrea: inyección desconocida | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 83 | `H15J` | Que más le dieron para tratar la diarrea: agua y arroz (panetela) | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 84 | `H15K` | Que más le dieron para tratar la diarrea: CS | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 85 | `H15L` | Que más le dieron para tratar la diarrea: CS | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 86 | `H15M` | Que más le dieron para tratar la diarrea: CS | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 87 | `H20` | Que más le dieron para tratar la diarrea: otro tratamiento | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 88 | `H21A` | Sin tratamiento | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 89 | `H21` | Recibió cualquier tratamiento | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 90 | `H22` | Ha tenido fiebre en las últimas dos semanas | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 91 | `H31` | Ha tenido tos en las últimas dos semanas | **INCLUIR** | Dosis 1 y 2 de vacuna contra Rotavirus. Previene gastroenteritis aguda deshidratante, causa mayor de retardo estatural. |
| 92 | `H31B` | Cuando estuvo enfermo con tos, respiraba más rápido con respiraciones cortas y rápidas | **INCLUIR** | Dosis 1 y 2 de vacuna contra Rotavirus. Previene gastroenteritis aguda deshidratante, causa mayor de retardo estatural. |
| 93 | `H31C` | La respiración rápida o difícil era por un problema en el pecho o porque tenía la nariz<br>tupida | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 94 | `H31D` | Le dió usted la misma cantidad de bebidas que antes de la fiebre o tos, más bebidas o<br>menos bebidas | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 95 | `H31E` | Le dió la misma cantidad de comida que antes de la fiebre o tos, le dio más o le dio<br>menos comida | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 96 | `H32A` | Dónde buscó tratamiento para la Fiebre/tos: Hospital MINSA | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 97 | `H32B` | Dónde buscó tratamiento para la Fiebre/tos: Centro de salud MINSA | **INCLUIR** | Dosis 1, 2 y 3 de vacuna antineumocócica. Previene neumonías e infecciones invasivas por Streptococcus pneumoniae. |
| 98 | `H32C` | Dónde buscó tratamiento para la Fiebre/tos: Puesto de salud MINSA | **INCLUIR** | Dosis 1, 2 y 3 de vacuna antineumocócica. Previene neumonías e infecciones invasivas por Streptococcus pneumoniae. |
| 99 | `H32D` | Dónde buscó tratamiento para la Fiebre/tos: Clínica móvil | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 100 | `H32E` | Dónde buscó tratamiento para la Fiebre/tos: Promotor de salud | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 101 | `H32F` | Dónde buscó tratamiento para la Fiebre/tos: Hospital ESSALUD | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 102 | `H32G` | Dónde buscó tratamiento para la Fiebre/tos: Hospital FF.A. y PNP. | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 103 | `H32H` | Dónde buscó tratamiento para la Fiebre/tos: Posta ESSALUD | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 104 | `H32I` | Dónde buscó tratamiento para la Fiebre/tos: Hospital/otro de la Municipalidad | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 105 | `H32J` | Dónde buscó tratamiento para la Fiebre/tos: Hospital/clínica particular | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 106 | `H32K` | Dónde buscó tratamiento para la Fiebre/tos: Farmacia/botica | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 107 | `H32L` | Dónde buscó tratamiento para la Fiebre/tos: Consultorio médico particular | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 108 | `H32M` | Dónde buscó tratamiento para la Fiebre/tos: Móvil privado | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 109 | `H32N` | Dónde buscó tratamiento para la Fiebre/tos: Trabajador de salud | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 110 | `H32O` | Dónde buscó tratamiento para la Fiebre/tos: Botiquin popular | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 111 | `H32P` | Dónde buscó tratamiento para la Fiebre/tos: Clínica/posta de ONG | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 112 | `H32Q` | Dónde buscó tratamiento para la Fiebre/tos: Hospital/otro de la Iglesia | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 113 | `H32R` | Dónde buscó tratamiento para la Fiebre/tos: Otro médico privado | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 114 | `H32S` | Dónde buscó tratamiento para la Fiebre/tos: Comprar | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 115 | `H32T` | Dónde buscó tratamiento para la Fiebre/tos: Curandero | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 116 | `H32U` | Dónde buscó tratamiento para la Fiebre/tos: Amigo/pariente | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 117 | `H32V` | Dónde buscó tratamiento para la Fiebre/tos: CS Otros | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 118 | `H32W` | Dónde buscó tratamiento para la Fiebre/tos: CS Otros | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 119 | `H32X` | Dónde buscó tratamiento para la Fiebre/tos: Otros | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 120 | `H32Y` | Dónde buscó tratamiento para la Fiebre/tos: Sin tratamiento | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 121 | `H32Z` | Dónde buscó tratamiento para la Fiebre/tos: Tratamiento médico | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 122 | `H33` | Recibió vitamina A1 (más reciente) | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 123 | `H33D` | Vitamina A1 día | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 124 | `H33M` | Vitamina A1 mes | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 125 | `H33Y` | Vitamina A1 año | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 126 | `H34` | Vitamina A en los últimos 6 meses | **INCLUIR** | Niño recibió suplemento de Vitamina A en los últimos 6 meses. Fortalecimiento inmunológico del epitelio intestinal. |
| 127 | `H35` | Cualquier vacuna en los últimos 2 años forma parte de la campaña | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 128 | `H36A` | Vacunado durante la Campaña A | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 129 | `H36B` | Vacunado durante la Campaña B | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 130 | `H36C` | Vacunado durante la Campaña C | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 131 | `H36D` | Vacunado durante la Campaña D | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 132 | `H36E` | Vacunado durante la Campaña E | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 133 | `H36F` | Vacunado durante la Campaña F | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 134 | `H37A` | Tomó FanSIDAr para la fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 135 | `H37B` | Tomó Cloroquina para fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 136 | `H37C` | Tomó Amodiaquina para fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 137 | `H37D` | Tomó Quinina para la fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 138 | `H37E` | Tomó artemisinina para la fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 139 | `H37F` | Tomó Antihistanimico para la fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 140 | `H37G` | Tomó Antibiótico para la fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 141 | `H37H` | Tomó Otro antipalúdico para fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 142 | `H37I` | Tomó Pastillas/jarabe para fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 143 | `H37J` | Inyección para fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 144 | `H37K` | Tomó Aspirina para la fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 145 | `H37L` | Tomó Acetaminofeno para fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 146 | `H37M` | Tomó Ibuprofeno para la fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 147 | `H37N` | Tomó remedio casero para fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 148 | `H37O` | Tomó Analgésico, antinflamatorio para fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 149 | `H37P` | CS otro para fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 150 | `H37X` | Tomó otro para fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 151 | `H37Y` | No tomó nada para fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 152 | `H37Z` | Tomó algo para fiebre/tos: No sabe | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 153 | `H38` | Le dió usted la misma cantidad de bebidas que antes de la diarrea, màs bebidas o menos<br>bebidas | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 154 | `H39` | Le dió usted la misma cantidad de comida que antes de la diarrea, le dio màs o le dio<br>menos comida | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 155 | `H40` | Recibió Vitamina A (2da más reciente) | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 156 | `H40D` | Día de la vitamina A2 | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 157 | `H40M` | Vitamina A2 mes | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 158 | `H40Y` | Vitamina A2 año | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 159 | `H41A` | Recibió vitamina A después de la tarjeta más reciente | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 160 | `H41B` | Alguna vez recibió la dosis de vitamina A | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 161 | `H42` | Tomando píldoras de hierro, jarabe | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 162 | `H43` | Medicamentos para parásitos intestinales en los últimos 12 meses | **INCLUIR** | Niño recibió tratamiento antiparasitario en los últimos 6 meses. Prevención de geohelmintiasis causante de mala absorción. |
| 163 | `H44A` | Primer lugar buscado tratamiento para la diarrea | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 164 | `H44B` | Cuántos días después de que la diarrea buscó consejo o tratamiento | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 165 | `H44C` | Todavía tiene diarrea | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 166 | `H45` | Veces que le dieron zinc | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 167 | `H46A` | Lugar en el que se busca el tratamiento para la fiebre | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |
| 168 | `H46B` | Días después de que la fiebre buscara consejo o tratamiento | **EXCLUIR POR IRRELEVANCIA** | Fechas administrativas de administración de cada vacuna (días, meses, años). |


### 📁 Archivo: `Diccionario - REC95.pdf` — Módulo: `1036-inmunizacion`
**Total de variables evaluadas:** 315

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Identificadores relacionales del niño en salud infantil ampliada. |
| 2 | `CASEID` | Identificación Cuestionario Individual | **METADATO / LLAVE** | Identificadores relacionales del niño en salud infantil ampliada. |
| 3 | `IDX95` | Índice de historia de nacimiento | **METADATO / LLAVE** | Identificadores relacionales del niño en salud infantil ampliada. |
| 4 | `S45D4` | Recibió 1er. refuerzo DPT | **INCLUIR** | Controles de Crecimiento y Desarrollo (CRED) y carné CRED verificado. |
| 5 | `S45D4D` | 1er. Refuerzo DPT - día | **INCLUIR** | Controles de Crecimiento y Desarrollo (CRED) y carné CRED verificado. |
| 6 | `S45D4M` | 1er. Refuerzo DPT - mes | **INCLUIR** | Controles de Crecimiento y Desarrollo (CRED) y carné CRED verificado. |
| 7 | `S45D4Y` | 1er. Refuerzo DPT - año | **INCLUIR** | Controles de Crecimiento y Desarrollo (CRED) y carné CRED verificado. |
| 8 | `S45D5` | Recibió 2do. refuerzo DPT | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 9 | `S45D5D` | 2do. Refuerzo DPT - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 10 | `S45D5M` | 2do. Refuerzo DPT - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 11 | `S45D5Y` | 2do. Refuerzo DPT - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 12 | `S45P4` | Recibió 1er. refuerzo Polio | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 13 | `S45P4D` | 1er. Refuerzo Polio - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 14 | `S45P4M` | 1er. Refuerzo Polio - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 15 | `S45P4Y` | 1er. Refuerzo Polio - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 16 | `S45P5` | Recibió 2do. refuerzo Polio | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 17 | `S45P5D` | 2do. Refuerzo Polio - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 18 | `S45P5M` | 2do. Refuerzo Polio - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 19 | `S45P5Y` | 2do. Refuerzo Polio - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 20 | `S45B0` | Recibió la vacuna Antihepatitis B recién nacido | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 21 | `S45B0D` | Antihepatitis B recién nacido día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 22 | `S45B0M` | Antihepatitis B recién nacido mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 23 | `S45B0Y` | Antihepatitis B recién nacido año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 24 | `S45B1` | Recibió la vacuna Antihepatitis B 1ra. dosis | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 25 | `S45B1D` | Antihepatitis B 1ra. dosis - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 26 | `S45B1M` | Antihepatitis B 1ra. dosis - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 27 | `S45B1Y` | Antihepatitis B 1ra. dosis - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 28 | `S45B2` | Recibió la vacuna Antihepatitis B 2da. dosis | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 29 | `S45B2D` | Antihepatitis B 2da. dosis - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 30 | `S45B2M` | Antihepatitis B 2da. dosis - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 31 | `S45B2Y` | Antihepatitis B 2da. dosis - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 32 | `S45B3` | Recibió la vacuna Antihepatitis B 3ra. dosis | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 33 | `S45B3D` | Antihepatitis B 3ra. dosis - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 34 | `S45B3M` | Antihepatitis B 3ra. dosis - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 35 | `S45B3Y` | Antihepatitis B 3ra. dosis - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 36 | `S45F1` | Recibió vacuna Antihaemophilus 1ra. dosis | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 37 | `S45F1D` | Antihaemophilus 1ra. dosis - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 38 | `S45F1M` | Antihaemophilus 1ra. dosis - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 39 | `S45F1Y` | Antihaemophilus 1ra. dosis - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 40 | `S45F2` | Recibió vacuna Antihaemophilus 2da. dosis | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 41 | `S45F2D` | Antihaemophilus 2da. dosis - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 42 | `S45F2M` | Antihaemophilus 2da. dosis - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 43 | `S45F2Y` | Antihaemophilus 2da. dosis - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 44 | `S45F3` | Recibió Antihaemophilus 3ra. dosis | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 45 | `S45F3D` | Antihaemophilus 3ra. dosis - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 46 | `S45F3M` | Antihaemophilus 3ra. dosis - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 47 | `S45F3Y` | Antihaemophilus 3ra. dosis - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 48 | `S45PV1` | Recibió vacuna Pentavalente 1ra. dosis | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 49 | `S45PV1D` | Pentavalente 1ra. dosis - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 50 | `S45PV1M` | Pentavalente 1ra. dosis - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 51 | `S45PV1Y` | Pentavalente 1ra. dosis - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 52 | `S45PV2` | Recibió vacuna Pentavalente 2da. dosis | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 53 | `S45PV2D` | Pentavalente 2da. dosis - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 54 | `S45PV2M` | Pentavalente 2da. dosis - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 55 | `S45PV2Y` | Pentavalente 2da. dosis - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 56 | `S45PV3` | Recibió vacuna Pentavalente 3ra. dosis | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 57 | `S45PV3D` | Pentavalente 3ra. dosis - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 58 | `S45PV3M` | Pentavalente 3ra. dosis - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 59 | `S45PV3Y` | Pentavalente 3ra. dosis - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 60 | `S45TT` | Recibió vacuna Tetravalente | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 61 | `S45TTD` | Tetravalente día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 62 | `S45TTM` | Tetravalente mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 63 | `S45TTY` | Tetravalente año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 64 | `S45ML` | Recibió vacuna Antiamarílica | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 65 | `S45MLD` | Antiamarílica día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 66 | `S45MLM` | Antiamarílica mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 67 | `S45MLY` | Antiamarílica año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 68 | `S45SP1` | Recibió vacuna Antisarampionosa/SPR 1ra. dosis (triple viral) | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 69 | `S45SP1D` | Antisarampionosa/SPR 1ra. dosis - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 70 | `S45SP1M` | Antisarampionosa/SPR 1ra. dosis - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 71 | `S45SP1Y` | Antisarampionosa/SPR 1ra. dosis - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 72 | `S45SP2` | Recibió vacuna Antisarampionosa/SPR 2da. dosis (triple viral) | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 73 | `S45SP2D` | Antisarampionosa/SPR 2da. dosis - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 74 | `S45SP2M` | Antisarampionosa/SPR 2da. dosis - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 75 | `S45SP2Y` | Antisarampionosa/SPR 2da. dosis - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 76 | `S45SR` | Recibió vacuna SR 1ra. dosis (doble viral) | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 77 | `S45SRD` | SR día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 78 | `S45SRM` | SR mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 79 | `S45SRY` | SR año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 80 | `S45NM1` | Recibió vacuna Neumococo 1ra. dosis | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 81 | `S45NM1D` | Neumococo 1ra. dosis - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 82 | `S45NM1M` | Neumococo 1ra. dosis - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 83 | `S45NM1Y` | Neumococo 1ra. dosis - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 84 | `S45NM2` | Recibió vacuna Neumococo 2da. dosis | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 85 | `S45NM2D` | Neumococo 2da. dosis - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 86 | `S45NM2M` | Neumococo 2da. dosis - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 87 | `S45NM2Y` | Neumococo 2da. dosis - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 88 | `S45NM3` | Recibió vacuna Neumococo 3ra. dosis | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 89 | `S45NM3D` | Neumococo 3ra. dosis - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 90 | `S45NM3M` | Neumococo 3ra. dosis - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 91 | `S45NM3Y` | Neumococo 3ra. dosis - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 92 | `QI461G` | Recibió la vacuna Antineumocócica (Reportada por la madre) | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 93 | `QI461H` | Recibió la vacuna Antineumocócica ¿Cuántas veces? (Reportada por la<br>madre) | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 94 | `S45RT1` | Recibió vacuna Rotavirus 1ra. dosis | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 95 | `S45RT1D` | Rotavirus 1ra. dosis - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 96 | `S45RT1M` | Rotavirus 1ra. dosis - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 97 | `S45RT1Y` | Rotavirus 1ra. dosis - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 98 | `S45RT2` | Recibió vacuna rotavirus 2da. dosis | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 99 | `S45RT2D` | Rotavirus 2da. dosis - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 100 | `S45RT2M` | Rotavirus 2da. dosis - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 101 | `S45RT2Y` | Rotavirus 2da. dosis - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 102 | `QI461I` | Recibió la vacuna Rotavirus (Reportada por la madre) | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 103 | `QI461J` | Recibió la vacuna Rotavirus ¿Cuántas veces? (Reportada por la madre): | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 104 | `S45IF1` | Recibió vacuna Influenza 1ra. dosis | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 105 | `S45IF1D` | Influenza 1ra. dosis - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 106 | `S45IF1M` | Influenza 1ra. dosis - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 107 | `S45IF1Y` | Influenza 1ra. dosis - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 108 | `S45IF2` | Recibió vacuna Influenza 2da. dosis | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 109 | `S45IF2D` | Influenza 2da. dosis - día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 110 | `S45IF2M` | Influenza 2da. dosis - mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 111 | `S45IF2Y` | Influenza 2da. dosis - año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 112 | `S45VA3` | Recibió Vitamina A 3 | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 113 | `S45VA3D` | Vitamina A 3 día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 114 | `S45VA3M` | Vitamina A 3 mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 115 | `S45VA3Y` | Vitamina A 3 año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 116 | `S45V` | Recibió la vacuna de Varicela | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 117 | `S45VD` | Varicela - Día | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 118 | `S45VM` | Varicela - Mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 119 | `S45VY` | Varicela - Año | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 120 | `S459B` | Cuando se administró la primera dosis de hepatitis | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 121 | `S462E` | Número de vacunas con vitamina A | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 122 | `S466` | Le hicieron algún control de crecimiento y desarrollo | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 123 | `S466AA` | El control de crecimiento y desarrollo lo realizó: doctor | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 124 | `S466AB` | El control de crecimiento y desarrollo lo realizó: obstetra | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 125 | `S466AC` | El control de crecimiento y desarrollo lo realizó: enfermera | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 126 | `S466AD` | El control de crecimiento y desarrollo lo realizó: técnico en enfermería | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 127 | `S466AE` | El control de crecimiento y desarrollo lo realizó: promotor de salud | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 128 | `S466AX` | El control de crecimiento y desarrollo lo realizó: otro | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 129 | `S466B` | Dónde le realizaron el control de crecimiento y desarrollo | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 130 | `S466C` | Cantidad de controles de crecimiento de control | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 123 | `QI_CTRL_DIA_01` | DIA.01 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 132 | `QI_CTRL_MES_01` | MES.01 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 133 | `QI_CTRL_ANIO_01` | Año.01 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 134 | `QI_CTRL_PESO_01` | PESO.01 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 135 | `QI_CTRL_TALLA_01` | TALLA.01 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 136 | `QI_CTRL_DIA_02` | DIA.02 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 137 | `QI_CTRL_MES_02` | MES.02 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 138 | `QI_CTRL_ANIO_02` | Año.02 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 139 | `QI_CTRL_PESO_02` | PESO.02 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 140 | `QI_CTRL_TALLA_02` | TALLA.02 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 141 | `QI_CTRL_DIA_03` | DIA.03 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 142 | `QI_CTRL_MES_03` | MES.03 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 143 | `QI_CTRL_ANIO_03` | Año.03 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 144 | `QI_CTRL_PESO_03` | PESO.03 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 145 | `QI_CTRL_TALLA_03` | TALLA.03 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 146 | `QI_CTRL_DIA_04` | DIA.04 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 147 | `QI_CTRL_MES_04` | MES.04 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 148 | `QI_CTRL_ANIO_04` | Año.04 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 149 | `QI_CTRL_PESO_04` | PESO.04 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 150 | `QI_CTRL_TALLA_04` | TALLA.04 - CRED menor de un mes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 151 | `S466DC1` | Día - Control 1 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 152 | `S466MC1` | Mes - Control 1 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 153 | `S466YC1` | Año - Control 1 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 154 | `S466WC1` | Peso en gramos de control 1 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 155 | `S466HC1` | Talla en centímetros de control 1 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 156 | `S466DC2` | Día - Control 2 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 157 | `S466MC2` | Mes - Control 2 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 158 | `S466YC2` | Año - Control 2 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 159 | `S466WC2` | Peso en gramos de control 2 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 160 | `S466HC2` | Talla en centímetros de control 2 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 161 | `S466DC3` | Día - Control 3 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 162 | `S466MC3` | Mes - Control 3 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 163 | `S466YC3` | Año - Control 3 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 164 | `S466WC3` | Peso en gramos de control 3 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 165 | `S466HC3` | Talla en centímetros de control 3 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 166 | `S466DC4` | Día - Control 4 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 167 | `S466MC4` | Mes - Control 4 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 168 | `S466YC4` | Año - Control 4 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 169 | `S466WC4` | Peso en gramos de control 4 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 170 | `S466HC4` | Talla en centímetros control 4 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 171 | `S466DC5` | Día - Control 5 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 172 | `S466MC5` | Mes - Control 5 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 173 | `S466YC5` | Año - Control 5 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 174 | `S466WC5` | Peso en gramos de control 5 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 175 | `S466HC5` | Talla en centímetros de control 5 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 176 | `S466DC6` | Día - Control 6 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 177 | `S466MC6` | Mes - Control 6 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 178 | `S466YC6` | Año - Control 6 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 179 | `S466WC6` | Peso en gramos de control 6 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 180 | `S466HC6` | Talla en centímetros de control 6 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 181 | `S466DC7` | Día - Control 7 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 182 | `S466MC7` | Mes - Control 7 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 183 | `S466YC7` | Año - Control 7 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 184 | `S466WC7` | Peso en gramos de control 7 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 185 | `S466HC7` | Talla en centímetros de control 7 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 186 | `S466DC8` | Día - Control 8 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 187 | `S466MC8` | Mes - Control 8 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 188 | `S466YC8` | Año - Control 8 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 189 | `S466WC8` | Peso en gramos de control 8 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 190 | `S466HC8` | Talla en centímetros de control 8 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 191 | `S466DC9` | Día - Control 9 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 192 | `S466MC9` | Control del mes 9 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 193 | `S466YC9` | Año - Control 9 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 194 | `S466WC9` | Peso en gramos de control 9 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 195 | `S466HC9` | Talla en centímetros de control 9 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 196 | `S466DC10` | Día - Control 10 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 197 | `S466MC10` | Mes - Control 10 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 198 | `S466YC10` | Año - Control 10 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 199 | `S466WC10` | Peso en gramos de control 10 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 200 | `S466HC10` | Talla en centímetros de control 10 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 201 | `S466DC11` | Día - Control 11 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 202 | `S466MC11` | Control del mes 11 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 203 | `S466YC11` | Año - Control 11 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 204 | `S466WC11` | Peso en gramos de control 11 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 205 | `S466HC11` | Talla en centímetros de control 11 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 206 | `S466DC12` | Día - Control 12 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 207 | `S466MC12` | Mes - Control 12 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 208 | `S466YC12` | Año - Control 12 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 209 | `S466WC12` | Peso en gramos de control 12 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 210 | `S466HC12` | Talla en centímetros de control 12 | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 211 | `S466GA` | Practicaste cómo amamantar | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 212 | `S466GB` | Practicaste cómo preparar comida | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 213 | `S466GC` | Practicaste cómo bañar | **DUDOSA (TRATAMIENTO DE ANEMIA)** | Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo. |
| 214 | `S470` | Por qué no acudió a un centro de salud cuando estuvo enfermo con<br>fiebre/tos | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 215 | `S471` | Está aun con fiebre o tos | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 216 | `S471CA` | Cuándo enfermo Ud. tenía en casa: antihestamínico | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 217 | `S471CB` | Cuándo enfermo Ud. tenía en casa: antibióticos | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 218 | `S471CC` | Cuándo enfermo Ud. tenía en casa: antimaláricos | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 219 | `S471CD` | Cuándo enfermo Ud. tenía en casa: jarabe para la tos | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 220 | `S471CE` | Cuándo enfermo Ud. tenía en casa: analgésico antiinflamatorio | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 221 | `S471CF` | No tenía ninguno en casa | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 222 | `S472AA` | Durante la diarrea tuvo síntomas o dolencias como: Intranquilo | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 223 | `S472AB` | Durante la diarrea tuvo síntomas o dolencias como: Sediento | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 224 | `S472AC` | Durante la diarrea tuvo síntomas o dolencias como: Lloraba sin lágrimas | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 225 | `S472AD` | Durante la diarrea tuvo síntomas o dolencias como: Piel reseca | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 226 | `S472B` | Cantidad de deposiciones en el peor día de diarrea | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 227 | `S473DA` | Le dieron para tratar la diarrea: pastillas de zinc | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 228 | `S473DB` | Le dieron para tratar la diarrea: jarabe de zinc | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 229 | `S473F` | Cuántas veces recibió tabletas de zinc | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 230 | `S475` | Por qué no acudió a un establecimiento de salud cuando estuvo<br>enfermo con diarrea | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 231 | `S476AN1` | Tuvo deposiciones líquidas y/o semilíquidas ayer | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 232 | `S476AS1` | Presentó sangrado ayer | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 233 | `S476AT1` | Tuvo tos ayer | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 234 | `S476AR1` | Tuvo dificultad para respirar ayer | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 235 | `S476AN2` | Tuvo deposiciones líquidas y/o semilíquidas hace dos días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 236 | `S476AS2` | Presentó sangrado hace dos días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 237 | `S476AT2` | Tuvo tos hace dos días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 238 | `S476AR2` | Tuvo dificultad para respirar hace dos días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 239 | `S476AN3` | Tuvo deposiciones líquidas y/o semilíquidas hace tres días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 240 | `S476AS3` | Presentó sangrado hace tres días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 241 | `S476AT3` | Tuvo tos hace tres días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 242 | `S476AR3` | Tuvo dificultad para respirar hace tres días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 243 | `S476AN4` | Tuvo deposiciones líquidas y/o semilíquidas hace cuatro días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 244 | `S476AS4` | Presentó sangrado hace cuatro días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 245 | `S476AT4` | Tuvo tos hace cuatro días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 246 | `S476AR4` | Tuvo dificultad para respirar hace cuatro días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 247 | `S476AN5` | Tuvo deposiciones líquidas y/o semilíquidas hace cinco días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 248 | `S476AS5` | Presentó sangrado hace cinco días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 249 | `S476AT5` | Tuvo tos hace cinco días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 250 | `S476AR5` | Tuvo dificultad para respirar hace cinco días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 251 | `S476AN6` | Tuvo deposiciones líquidas y/o semilíquidas hace seis días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 252 | `S476AS6` | Presentó sangrado hace seis días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 253 | `S476AT6` | Tuvo tos hace seis días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 254 | `S476AR6` | Tuvo dificultad para respirar hace seis días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 255 | `S476AN7` | Tuvo deposiciones líquidas y/o semilíquidas hace siete días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 256 | `S476AS7` | Presentó sangrado hace siete días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 257 | `S476AT7` | Tuvo tos hace siete días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 258 | `S476AR7` | Tuvo dificultad para respirar hace siete días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 259 | `S465EA` | En los últimos 7 días tomo hierro en jarabe | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 260 | `S465EB` | En los Últimos 7 días tomo hierro en polvo como Micronutrientes -<br>(chispitas, estrellitas o NUTRIMIX) | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 261 | `S465EC` | En los Últimos 7 días tomo hierro en gotas | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 262 | `S465ED` | En los Últimos 7 día tomo hierro en otra presentación | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 263 | `S465DB_A` | En los últimos 12 meses recibió del MINSA para prevenir la anemia:<br>Hierro en jarabe | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 264 | `S465DB_B` | En los últimos 12 meses recibió del MINSA para prevenir la anemia:<br>Hierro en gotas | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 265 | `S465DB_C` | En los últimos 12 meses recibió del MINSA para prevenir la anemia:<br>Hierro en polvo como Micronutrientes (chispita o / estrellitas /<br>NUTRIMIX) | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 266 | `S465DB_D` | En los últimos 12 meses recibió del MINSA para prevenir la anemia:<br>Hierro en alguna otra presentación | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 267 | `S465DD_AR` | En los últimos 12 meses cuántos frascos recibió de hierro en jarabe | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 268 | `S465DD_AC` | En los últimos 12 meses cuántos frascos consumió de hierro en jarabe | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 269 | `S465DD_BR` | En los últimos 12 meses cuántos frascos recibió de hierro en gotas | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 270 | `S465DD_BC` | En los últimos 12 meses cuántos frascos consumió de hierro en gotas | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 271 | `S465DD_CR` | En los últimos 12 meses cuántos sobres recibió de chispitas o estrellitas | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 272 | `S465DD_CC` | En los últimos 12 meses cuántos sobres consumió de chispitas o | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 273 | `S465DD_DR` | En los últimos 12 meses cuántas unidades recibió de otra presentación<br>de hierro | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 274 | `S465DD_DC` | En los últimos 12 meses cuántas unidades consumió de otra<br>presentación de hierro | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 275 | `Q452` | Número de orden en la historia de nacimiento | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 276 | `Q465DF` | Cuál es la razón por la cual no recibió hierro de parte del Ministerio de<br>Salud | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 277 | `Q465DH` | De qué forma consume los Micronutrientes<br>(chispitas/estrellitas/NUTRIMIX) | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 278 | `Q465DJ` | Cuál es la razón por la cual no consumió los Micronutrientes, jarabe o<br>gotas de hierro que recibió | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 279 | `Q465EB_A8` | De que forma consumió los Micronutrientes en estos últimos 7 días | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 280 | `Q465EC_A9` | Entrega de multimicronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 281 | `Q465EC_D1` | Día 1ra entrega de micronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 282 | `Q465EC_M1` | Mes 1ra entrega de micronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 283 | `Q465EC_Y1` | Año 1ra entrega de micronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 284 | `Q465EC_D2` | Día 2da entrega de micronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 285 | `Q465EC_M2` | Mes 2da entrega de micronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 286 | `Q645EC_Y2` | Año 2da entrega de micronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 287 | `Q465EC_D3` | Día 3ra entrega de micronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 288 | `Q465EC_M3` | Mes 3ra entrega de micronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 289 | `Q465EC_Y3` | Año 3ra entrega de micronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 290 | `Q465EC_D4` | Día 4ta entrega de micronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 291 | `Q465EC_M4` | Mes 4ta entrega de micronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 292 | `Q465EC_Y4` | Año 4ta entrega de micronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 293 | `Q465EC_D5` | Día 5ta entrega de micronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 294 | `Q465EC_M5` | Mes 5ta entrega de micronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 295 | `Q465EC_Y5` | Año 5ta entrega de micronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 296 | `Q465EC_D6` | Día 6ta entrega de micronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 297 | `Q465EC_M6` | Mes 6ta entrega de micronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 298 | `Q465EC_Y6` | Año 6ta entrega de micronutrientes | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 299 | `QI465ED_CC_A` | Alguna vez, un personal de salud le realizó una prueba o análisis para<br>descartar anemia | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 300 | `QI465ED_CC_A1` | Hace cuanto tiempo le realizaron la última prueba | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 301 | `QI465ED_CC_A1_D` | Hace cuantos Dias le realizaron la última prueba | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 302 | `QI465ED_CC_A1_M` | Hace cuantos Meses le realizaron la última prueba | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 303 | `QI465ED_CC_B` | Le diagnosticaron o le dijeron que tenia anemia | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 304 | `QI465ED_CC_B1` | Cuál fue el resultado | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 305 | `QI465ED_CC_B1_1` | Resultado según carné | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 306 | `QI465ED_CC_B1_2` | Resultado según recuerda | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 307 | `QI465ED_CC_C` | Le indicaron tratamiento con hierro | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 308 | `QI465ED_CC_D` | Consumió el hierro tal como le indicó el personal de salud | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 309 | `QIEDAD_GEST` | Edad Gestacional en semanas | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 310 | `QI456_1A` | Documento de donde registro información de vacunas: Carné de<br>Atención Integral de Salud | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 311 | `QI456_1B` | Documento de donde registro información de vacunas: Carné de<br>Crecimiento Neonatal | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 312 | `QI456_1X` | Documento de donde registro información de vacunas: Otro | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 313 | `QI466E_1A` | Documento de donde registro información de controles: Carné de<br>Atención Integral de Salud | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 314 | `QI466E_1B` | Documento de donde registro información de controles: Carné de<br>Crecimiento Neonatal | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |
| 315 | `QI466E_1X` | Documento de donde registro información de controles: Otro | **EXCLUIR POR IRRELEVANCIA** | Detalles operativos de citas médicas o preguntas de control. |


### 📁 Archivo: `Diccionario - Programas Sociales x Hogar.pdf` — Módulo: `1041-programasocial`
**Total de variables evaluadas:** 20

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Llaves de enlace a nivel de hogar y conglomerado. |
| 2 | `HHID` | Identificacion Cuestionario del Hogar | **METADATO / LLAVE** | Llaves de enlace a nivel de hogar y conglomerado. |
| 3 | `QHCLUSTER` | Conglomerado | **METADATO / LLAVE** | Llaves de enlace a nivel de hogar y conglomerado. |
| 4 | `QHNUMBER` | Vivienda seleccionada | **METADATO / LLAVE** | Llaves de enlace a nivel de hogar y conglomerado. |
| 5 | `QHHOME` | Hogar seleccionado | **METADATO / LLAVE** | Llaves de enlace a nivel de hogar y conglomerado. |
| 6 | `QH91` | Algun miembro es beneficiario de BECA 18? | **INCLUIR** | Hogar beneficiario de Beca 18. Alivio económico familiar por educación superior de hijos mayores. |
| 7 | `QH93` | Algun miembro es beneficiario de TRABAJA PERÚ? | **INCLUIR** | Hogar beneficiario de Trabaja Perú. Empleo temporal de emergencia en zonas vulnerables. |
| 8 | `QH95` | Algun miembro es beneficiario de JUNTOS? | **INCLUIR** | Hogar beneficiario del Programa JUNTOS. Transferencia monetaria condicionada a controles CRED y vacunas del infante. |
| 9 | `QH96` | Número de orden | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de acuerdos de compromiso o fechas administrativas. |
| 10 | `QH96A` | Hace cuanto tiempo es beneficiario: Años | **INCLUIR** | Tiempo en años y meses como beneficiario de JUNTOS. Exposición acumulada al programa social. |
| 11 | `QH96M` | Hace cuanto tiempo es beneficiario: Meses | **INCLUIR** | Tiempo en años y meses como beneficiario de JUNTOS. Exposición acumulada al programa social. |
| 12 | `QH96AC` | Muestra acuerdo de compromiso | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de acuerdos de compromiso o fechas administrativas. |
| 13 | `QH97D` | Día de afiliación | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de acuerdos de compromiso o fechas administrativas. |
| 14 | `QH97M` | Mes de afiliación | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de acuerdos de compromiso o fechas administrativas. |
| 15 | `QH97A` | Año de afiliación | **EXCLUIR POR IRRELEVANCIA** | Detalles menores de acuerdos de compromiso o fechas administrativas. |
| 16 | `QH99` | Algun miembro es beneciario de PENSIÓN 65? | **INCLUIR** | Hogar beneficiario de Pensión 65. Transferencia a adultos mayores que reduce la pobreza extrema del hogar. |
| 17 | `QH101` | Algun miembro recibe ayuda de VASO DE LECHE? | **INCLUIR** | Hogar recibe apoyo del Programa del Vaso de Leche (PVL). Complementación alimentaria municipal. |
| 18 | `QH103` | Algun miembro recibe ayuda del COMEDOR POPULAR? | **INCLUIR** | Hogar recibe raciones de Comedores Populares. Subsidio alimentario en barrios precarios. |
| 19 | `QH106` | Algun miembro recibe ayuda de WAWA WASI/ CUNA MAS? | **INCLUIR** | Niño o miembro del hogar asiste a Cuna Más / Wawa Wasi. Cuidado diurno y alimentación balanceada para menores de 36 meses. |
| 20 | `QHVIOLEN` | Numero de mujer para violencia domestica | **DUDOSA (SENSIBILIDAD ÉTICA)** | Presencia de violencia doméstica reportada en el hogar. Factor de negligencia y estrés tóxico infantil. |


### 📁 Archivo: `Diccionario - PS_COMEDOR.pdf` — Módulo: `1041-programasocial`
**Total de variables evaluadas:** 10

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 2 | `HHID` | Identificacion Cuestionario del Hogar | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 3 | `HVIDX` | Número de Orden en el Hogar | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 4 | `QHCLUSTER` | Conglomerado | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 5 | `QHNUMBER` | Vivienda seleccionada | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 6 | `QHHOME` | Hogar seleccionado | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 7 | `PS104_1A` | Hace cuanto tiempo es beneficiario: Años | **INCLUIR** | Tiempo en años y meses que el miembro es beneficiario de PS_COMEDOR. |
| 8 | `PS104_1M` | Hace cuanto tiempo es beneficiario: Meses | **INCLUIR** | Tiempo en años y meses que el miembro es beneficiario de PS_COMEDOR. |
| 9 | `PS104_1S` | Alguien más es beneficiario | **INCLUIR** | Alguien más en el hogar es beneficiario de PS_COMEDOR. |
| 10 | `PS5` | Número de Orden | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares del módulo social específico. |


### 📁 Archivo: `Diccionario - PS_CUNAMAS_VISITA.pdf` — Módulo: `1041-programasocial`
**Total de variables evaluadas:** 10

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 2 | `HHID` | Identificacion Cuestionario del Hogar | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 3 | `HVIDX` | Número de Orden en el Hogar | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 4 | `QHCLUSTER` | Conglomerado | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 5 | `QHNUMBER` | Vivienda seleccionada | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 6 | `QHHOME` | Hogar seleccionado | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 7 | `PS100C1_A` | Hace cuanto tiempo es beneficiario: Años | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares del módulo social específico. |
| 8 | `PS100C1_M` | Hace cuanto tiempo es beneficiario: Meses | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares del módulo social específico. |
| 9 | `PS100C_1S` | Alguien más es beneficiario | **INCLUIR** | Alguien más en el hogar es beneficiario de PS_CUNAMAS_VISITA. |
| 10 | `PS8` | Número de Orden | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares del módulo social específico. |


### 📁 Archivo: `Diccionario - PS_QALIWARMA.pdf` — Módulo: `1041-programasocial`
**Total de variables evaluadas:** 11

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 2 | `HHID` | Identificacion Cuestionario del Hogar | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 3 | `HVIDX` | Número de Orden en el Hogar | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 4 | `QHCLUSTER` | Conglomerado | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 5 | `QHNUMBER` | Vivienda seleccionada | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 6 | `QHHOME` | Hogar seleccionado | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 7 | `PS109_1R` | Recibió desayuno y/o almuerzo del programa nacional de alimentación escolar QALIWARMA | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares del módulo social específico. |
| 8 | `PS109_1A` | Hace cuanto tiempo es beneficiario: Años | **INCLUIR** | Tiempo en años y meses que el miembro es beneficiario de PS_QALIWARMA. |
| 9 | `PS109_1M` | Hace cuanto tiempo es beneficiario: Meses | **INCLUIR** | Tiempo en años y meses que el miembro es beneficiario de PS_QALIWARMA. |
| 10 | `PS109_1S` | Alguien más es beneficiario | **INCLUIR** | Alguien más en el hogar es beneficiario de PS_QALIWARMA. |
| 11 | `PS7` | Número de Orden | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares del módulo social específico. |


### 📁 Archivo: `Diccionario - PS_TRABAJA.pdf` — Módulo: `1041-programasocial`
**Total de variables evaluadas:** 10

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 2 | `HHID` | Identificacion Cuestionario del Hogar | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 3 | `HVIDX` | Número de Orden en el Hogar | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 4 | `QHCLUSTER` | Conglomerado | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 5 | `QHNUMBER` | Vivienda seleccionada | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 6 | `QHHOME` | Hogar seleccionado | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 7 | `PS94_1A` | Hace cuanto tiempo es beneficiario: Años | **INCLUIR** | Tiempo en años y meses que el miembro es beneficiario de PS_TRABAJA. |
| 8 | `PS94_1M` | Hace cuanto tiempo es beneficiario: Meses | **INCLUIR** | Tiempo en años y meses que el miembro es beneficiario de PS_TRABAJA. |
| 9 | `PS94_1S` | Alguien más es beneficiario | **INCLUIR** | Alguien más en el hogar es beneficiario de PS_TRABAJA. |
| 10 | `PS2` | Número de Orden | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares del módulo social específico. |


### 📁 Archivo: `Diccionario - PS_VL VASO DE LECHE.pdf` — Módulo: `1041-programasocial`
**Total de variables evaluadas:** 10

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 2 | `HHID` | Identificacion Cuestionario del Hogar | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 3 | `HVIDX` | Número de Orden en el Hogar | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 4 | `QHCLUSTER` | Conglomerado | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 5 | `QHNUMBER` | Vivienda seleccionada | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 6 | `QHHOME` | Hogar seleccionado | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 7 | `PS102_1A` | Hace cuanto tiempo es beneficiario: Años | **INCLUIR** | Tiempo en años y meses que el miembro es beneficiario de PS_VL VASO DE LECHE. |
| 8 | `PS102_1M` | Hace cuanto tiempo es beneficiario: Meses | **INCLUIR** | Tiempo en años y meses que el miembro es beneficiario de PS_VL VASO DE LECHE. |
| 9 | `PS102_1S` | Alguien más es beneficiario | **INCLUIR** | Alguien más en el hogar es beneficiario de PS_VL VASO DE LECHE. |
| 10 | `PS4` | Número de Orden | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares del módulo social específico. |


### 📁 Archivo: `Diccionario - PS_WAWAWASI.pdf` — Módulo: `1041-programasocial`
**Total de variables evaluadas:** 10

| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |
|:---|:---|:---|:---|:---|
| 1 | `ID1` | Año | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 2 | `HHID` | Identificacion Cuestionario del Hogar | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 3 | `HVIDX` | Número de Orden en el Hogar | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 4 | `QHCLUSTER` | Conglomerado | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 5 | `QHNUMBER` | Vivienda seleccionada | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 6 | `QHHOME` | Hogar seleccionado | **METADATO / LLAVE** | Llaves de enlace relacional del beneficiario en el hogar. |
| 7 | `PS107_1A` | Hace cuanto tiempo es beneficiario: Años | **INCLUIR** | Tiempo en años y meses que el miembro es beneficiario de PS_WAWAWASI. |
| 8 | `PS107_1M` | Hace cuanto tiempo es beneficiario: Meses | **INCLUIR** | Tiempo en años y meses que el miembro es beneficiario de PS_WAWAWASI. |
| 9 | `PS107_1S` | Alguien más es beneficiario | **INCLUIR** | Alguien más en el hogar es beneficiario de PS_WAWAWASI. |
| 10 | `PS6` | Número de Orden | **EXCLUIR POR IRRELEVANCIA** | Campos auxiliares del módulo social específico. |


---

## 5. Matriz Final de Variables SELECCIONADAS ($X$)

A continuación se consolida la matriz explicativa prioritaria para el entrenamiento de XGBoost. Todas las variables seleccionadas provienen de los diccionarios oficiales y respetan el marco conceptual de desnutrición de UNICEF (determinantes inmediatos, subyacentes y estructurales):

| Nombre Limpio (snake_case) | Variable Origen | Archivo / Módulo | Categoría | Tipo para ML | Códigos a Limpiar (NaN) | Justificación Epidemiológica ligada a Desnutrición Crónica |
|:---|:---|:---|:---|:---|:---|:---|
| `edad_meses` | `HC1` | `RECH6` | **Niño** | Continua / Discreta | `Ninguno` | Factor biológico central de crecimiento; acumulación progresiva del déficit de talla hasta los 24-36 meses. |
| `sexo_nino` | `HC27` | `RECH6` | **Niño** | Binaria (0/1) | `Ninguno` | Dimorfismo sexual biológico en velocidad de crecimiento lineal y masa magra. |
| `departamento` | `HV024` | `RECH0` | **Geografía** | Categórica Nominal | `Ninguno` | Captura desigualdades estructurales, climáticas e institucionales entre regiones. |
| `area_residencia` | `HV025` | `RECH0` | **Geografía** | Binaria (Urb/Rur) | `Ninguno` | Brecha rural-urbana histórica en provisión de saneamiento, agua tratada y pobreza. |
| `altitud_msnm` | `HV040` | `RECH0` | **Geografía** | Continua | `Ninguno` | Altitud geográfica en msnm; hipoxia ambiental y fuerte correlación con ruralidad andina aislada. |
| `total_miembros_hogar` | `HV009` | `RECH0` | **Hogar** | Discreta | `Ninguno` | Carga demográfica intrafamiliar y dilución del presupuesto alimentario per cápita. |
| `menores_5anos_hogar` | `HV014` | `RECH0` | **Hogar** | Discreta | `Ninguno` | Competencia directa por tiempo de cuidado materno, lactancia y raciones nutricionales. |
| `fuente_agua_beber` | `HV201` | `RECH23` | **Vivienda** | Categórica Nominal | `96 (Otro)` | Clave en enteropatía ambiental e infecciones diarreicas recurrentes. |
| `tipo_servicio_higienico` | `HV205` | `RECH23` | **Vivienda** | Categórica Nominal | `96 (Otro)` | Clasificación de saneamiento mejorado vs. no mejorado según criterios JMP OMS/UNICEF. |
| `tiene_electricidad` | `HV206` | `RECH23` | **Vivienda** | Binaria (0/1) | `Ninguno` | Posibilidad de conservar cadena de frío para alimentos proteicos de origen animal. |
| `material_piso` | `HV213` | `RECH23` | **Vivienda** | Categórica Nominal | `96 (Otro)` | Piso de tierra/arena actúa como reservorio directo de parásitos y bacterias entéricas. |
| `habitaciones_dormir` | `HV216` | `RECH23` | **Vivienda** | Discreta | `98 (No sabe)` | Denominador obligatorio para computar el índice de hacinamiento por dormitorio. |
| `bano_compartido` | `HV225` | `RECH23` | **Vivienda** | Binaria (0/1) | `Ninguno` | Contaminación cruzada en letrinas/baños compartidos con otros hogares. |
| `combustible_cocinar` | `HV226` | `RECH23` | **Vivienda** | Categórica Nominal | `96 (Otro)` | Uso de biomasa (leña, bosta) incrementa riesgo de infecciones respiratorias agudas. |
| `tratamiento_agua` | `HV237` | `RECH23` | **Vivienda** | Binaria (0/1) | `Ninguno` | Práctica de hervir o clorar agua como barrera sanitaria fundamental. |
| `quintil_riqueza` | `HV270` | `RECH23` | **Socioeconómica** | Categórica Ordinal | `Ninguno` | Nivel socioeconómico del hogar; predictor distal más potente de seguridad alimentaria. |
| `seguro_sis` | `SH11A` | `RECH4` | **Salud** | Binaria (0/1) | `Ninguno` | Afiliación al Seguro Integral de Salud estatal; acceso a controles CRED y vacunas. |
| `seguro_essalud` | `SH11B` | `RECH4` | **Salud** | Binaria (0/1) | `Ninguno` | Indicador proxy de empleo formal con salario fijo del padre o madre. |
| `controles_prenatales` | `M14` | `REC41` | **Gestación** | Discreta | `98 (No sabe)` | Vigilancia médica del crecimiento intrauterino y detección de patologías gestacionales. |
| `mes_inicio_prenatal` | `M18` | `REC41` | **Gestación** | Continua / Discreta | `98 (No sabe)` | Inicio oportuno del control gestacional durante el primer trimestre. |
| `peso_al_nacer_g` | `M19` | `REC41` | **Nacimiento** | Continua | `9996-9998` | Bajo peso al nacer (< 2,500 g) por RCIU o prematuridad; factor etiológico congénito principal. |
| `tamano_nacer_aparente` | `M19A` | `REC41` | **Nacimiento** | Categórica Ordinal | `8 (No sabe)` | Reporte materno del tamaño al nacer; rescata bajo peso cuando no hubo balanza. |
| `duracion_lactancia_m` | `M4` | `REC41` | **Lactancia** | Continua / Discreta | `95-98` | Meses acumulados de amamantamiento; protección inmunológica sostenida. |
| `lactancia_exclusiva_m` | `M5` | `REC41` | **Lactancia** | Continua / Discreta | `95-98` | Meses de lactancia materna exclusiva (estándar OMS: 6 meses sin otros líquidos). |
| `lugar_parto` | `M15` | `REC41` | **Nacimiento** | Categórica Nominal | `96 (Otro)` | Parto institucional en establecimiento de salud vs. parto domiciliario precario. |
| `atencion_parto_calif` | `M3A` | `REC41` | **Nacimiento** | Binaria (0/1) | `Ninguno` | Parto asistido por personal médico u obstetra calificado. |
| `hierro_madre_gestacion` | `M45` | `REC41` | **Gestación** | Binaria (0/1) | `8 (No sabe)` | Suplementación preventiva con hierro a la madre durante el embarazo. |
| `dias_hierro_madre` | `M46` | `REC41` | **Gestación** | Continua / Discreta | `998 (No sabe)` | Días acumulados de ingesta de hierro gestacional; reserva biológica materna. |
| `intervalo_intergenesico` | `B11` | `REC41` | **Gestación** | Continua | `Ninguno` | Meses transcurridos desde el nacimiento previo; intervalos < 24m agotan reservas maternas. |
| `talla_madre_cm` | `HA3` | `RECH5` | **Madre** | Continua | `9998` | Talla materna con 1 decimal; captura la herencia genética y el ciclo intergeneracional del retardo estatural. |
| `imc_madre` | `HA40` | `RECH5` | **Madre** | Continua | `9998` | Índice de masa corporal materno (con 2 decimales); desnutrición materna crónica. |
| `edad_madre_anos` | `V012` | `REC0111` | **Madre** | Continua | `Ninguno` | Edad actual de la madre en años cumplidos; embarazo en adolescencia temprana. |
| `educacion_madre_nivel` | `V106` | `REC0111` | **Madre** | Categórica Ordinal | `Ninguno` | Nivel educativo de la madre; determinante sociocultural mayor de prácticas de alimentación. |
| `educacion_madre_anos` | `V107` | `REC0111` | **Madre** | Discreta | `98 (No sabe)` | Años de escolaridad formal aprobados por la madre. |
| `estado_conyugal_madre` | `V501` | `REC0111` | **Madre** | Categórica Nominal | `Ninguno` | Estado conyugal; monoparentalidad y red de soporte económico familiar. |
| `madre_trabaja` | `V714` | `REC0111` | **Madre** | Binaria (0/1) | `Ninguno` | Inserción laboral de la madre y tiempo efectivo disponible para lactancia y cuidado. |
| `autonomia_salud_madre` | `V743A` | `REC0111` | **Madre** | Categórica Nominal | `Ninguno` | Poder de decisión de la madre sobre su propia atención médica y la de sus hijos. |
| `lengua_materna_madre` | `S119` | `REC91` | **Madre** | Categórica Nominal | `Ninguno` | Lengua originaria aprendida en la niñez (Quechua, Aimara, Nativa); barrera idiomática y exclusión. |
| `diarrea_reciente_eda` | `V411` | `REC42` | **Salud Niño** | Binaria (0/1) | `8 (No sabe)` | Diarrea en las últimas 2 semanas; CAUSA INMEDIATA DIRECTA de atrofia intestinal y retardo. |
| `diarrea_con_sangre` | `V411A` | `REC42` | **Salud Niño** | Binaria (0/1) | `8 (No sabe)` | Disentería bacteriana invasiva con daño severo a la mucosa entérica. |
| `tratamiento_sro` | `V413` | `REC42` | **Salud Niño** | Binaria (0/1) | `8 (No sabe)` | Uso de Sales de Rehidratación Oral durante la diarrea; previene shock y desnutrición aguda. |
| `fiebre_reciente` | `V414` | `REC42` | **Salud Niño** | Binaria (0/1) | `8 (No sabe)` | Fiebre reciente como marcador de infección sistémica y consumo metabólico acelerado. |
| `tos_ira_reciente` | `V415` | `REC42` | **Salud Niño** | Binaria (0/1) | `8 (No sabe)` | Infección respiratoria aguda reciente en las últimas 2 semanas. |
| `signos_neumonia` | `V416` | `REC42` | **Salud Niño** | Binaria (0/1) | `8 (No sabe)` | Respiración rápida o tiraje subcostal (neumonía grave). |
| `carne_vacunacion_visto` | `H1` | `REC43` | **Inmunización** | Categórica Nominal | `Ninguno` | Tenencia y verificación visual del carné oficial de salud infantil. |
| `vacuna_bcg` | `H2` | `REC43` | **Inmunización** | Binaria (0/1) | `8 (No sabe)` | Vacuna antituberculosa al nacer. |
| `vacuna_rotavirus_completa` | `H31B` | `REC43` | **Inmunización** | Binaria (0/1) | `8 (No sabe)` | Segunda dosis de rotavirus; previene diarreas virales deshidratantes masivas. |
| `vacuna_neumococo_dosis2` | `H32B` | `REC43` | **Inmunización** | Binaria (0/1) | `8 (No sabe)` | Dosis de neumococo; previene bacteriemias y neumonías destructivas. |
| `vacuna_spr1` | `H9` | `REC43` | **Inmunización** | Binaria (0/1) | `8 (No sabe)` | Vacuna contra sarampión al año de edad; previene desnutrición severa post-sarampión. |
| `suplemento_vitamina_a` | `H34` | `REC43` | **Nutrición Niño** | Binaria (0/1) | `8 (No sabe)` | Vitamina A en los últimos 6 meses; regeneración epitelial y defensas de mucosas. |
| `desparasitacion_infantil` | `H43` | `REC43` | **Nutrición Niño** | Binaria (0/1) | `8 (No sabe)` | Tratamiento antiparasitario en últimos 6 meses contra geohelmintiasis. |
| `controles_cred_numero` | `S45C` | `REC95` | **Salud Niño** | Discreta | `98 (No sabe)` | Número total de controles de Crecimiento y Desarrollo recibidos. |
| `programa_juntos` | `QH95` | `Programas Sociales` | **Programas Sociales** | Binaria (1/2) | `Ninguno` | Transferencia condicionada que exige asistencia a controles CRED y vacunas. |
| `programa_vaso_leche` | `QH101` | `Programas Sociales` | **Programas Sociales** | Binaria (1/2) | `Ninguno` | Beneficiario del programa municipal de complemento calórico-proteico. |
| `programa_comedor` | `QH103` | `Programas Sociales` | **Programas Sociales** | Binaria (1/2) | `Ninguno` | Acceso familiar a raciones cocinadas de Comedores Populares. |
| `programa_cuna_mas` | `QH106` | `Programas Sociales` | **Programas Sociales** | Binaria (1/2) | `Ninguno` | Atención en Cuna Más (Cuidado Diurno o Acompañamiento a Familias en nutrición temprana). |


### 5.1 Propuesta de Variables Derivadas de Alto Impacto Epidemiológico

A partir de las variables originales incluidas, se deben construir mediante ingeniería de características las siguientes 8 variables derivadas clave:

- **`grupo_edad_nino`** (Insumo: `HC1` (Edad en meses) | Tipo: *Categórica Ordinal*): Grupos: 0-5 meses (lactancia exclusiva), 6-11 meses (inicio de alimentación complementaria), 12-23 meses (ventana crítica de desaceleración estatural), 24-35 meses, 36-47 meses, 48-59 meses. Permite capturar la acumulación no lineal del déficit de talla.
- **`lactancia_exclusiva_adecuada`** (Insumo: `M5` y `HC1` | Tipo: *Binaria (0/1)*): 1 si para niños de 0 a 5 meses `M5 >= HC1` (recibe exclusivamente leche materna acorde a su edad), 0 en caso de introducción precoz de agua, infusiones o fórmulas.
- **`indice_hacinamiento`** (Insumo: `HV009` / `HV216` | Tipo: *Continua / Categórica*): Personas por dormitorio. Si es >= 3.0 personas/dormitorio se clasifica como hacinamiento crítico, asociado a transmisión cruzada de diarreas e infecciones respiratorias.
- **`saneamiento_adecuado_jmp`** (Insumo: `HV205` y `HV225` | Tipo: *Binaria (0/1)*): Criterio conjunto OMS/UNICEF (JMP): 1 si el baño es mejorado (red pública, letrina ventilada, pozo séptico) Y no es compartido con otros hogares (`HV225 == 0`), 0 en caso contrario.
- **`agua_segura_jmp`** (Insumo: `HV201` y `HV237` | Tipo: *Binaria (0/1)*): 1 si proviene de fuente mejorada (red domiciliaria, pilón) Y se aplica tratamiento seguro (hervir, clorar), 0 si es pozo ciego, río o no se trata.
- **`piso_tierra_critico`** (Insumo: `HV213` | Tipo: *Binaria (0/1)*): 1 si el piso principal es de tierra o arena (`HV213 == 11`), principal vector de geoparásitos y enteritis ambiental en infantes gateadores.
- **`combustible_contaminante_biomasa`** (Insumo: `HV226` | Tipo: *Binaria (0/1)*): 1 si cocina con leña, carbón, bosta o rastrojo sin chimenea adecuada, promoviendo infecciones respiratorias crónicas.
- **`intervalo_intergenesico_corto`** (Insumo: `B11` | Tipo: *Binaria (0/1)*): 1 si el intervalo desde el parto anterior es menor a 24 meses (`B11 < 24`), factor reconocido de síndrome de depleción materna de folatos y micronutrientes.

---

## 6. Variables DUDOSAS con Argumentos y Recomendación Técnica

Se identificaron cuatro conjuntos de variables con tensiones metodológicas entre poder predictivo y validez de campo:

### 6.1 Hemoglobina y Anemia Infantil (`HC53`, `HC56`, `HC56A`, `HC57`, `HC57A`)
- **Argumento a Favor de Incluirlas:** La anemia y la desnutrición crónica coexisten frecuentemente como manifestaciones de la misma privación nutricional y de inflamación subclínica. Un niño con anemia moderada/severa tiene un riesgo relativo 2 a 3 veces superior de presentar retardo estatural.
- **Argumento en Contra de Incluirlas:** Rompe la condición de **modelo de screening comunitario no invasivo**. Exige personal de enfermería capacitado, lancetas, hemoglobinómetros portátiles (Hemocue) y consentimiento informado con punción en el talón o dedo del infante. Además, es una medición clínica concurrente en el mismo punto temporal.
- **Recomendación Técnica Inequívoca:** **EXCLUIR del modelo predictivo primario de screening domiciliario.** Si se desea entrenar una variante clínica de segundo nivel para establecimientos de salud (donde sí hay laboratorio o Hemocue), se documenta como modelo clínico secundario.

### 6.2 Mediciones Antropométricas Correlacionadas (`HC71` Peso/Edad, `HC72` Peso/Talla, `HC2` Peso Crudo)
- **Argumento a Favor:** El peso infantil y los Z-scores de peso/edad y peso/talla tienen altísima correlación matemática con la masa corporal del niño.
- **Argumento en Contra:** Son **subrogados directos (proxies) del estado nutricional**. `HC71` y `HC72` se calculan en la misma sesión antropométrica de campo con balanza calibrada. Si se incluyen, el modelo se convierte en una tautología antropométrica que no aprende los determinantes biológicos y sociales del crecimiento.
- **Recomendación Técnica Inequívoca:** **EXCLUIR.** El modelo debe aprender a predecir la desnutrición a partir del entorno, la madre, la dieta y la morbilidad, no a partir de una balanza concurrente.

### 6.3 Hitos del Desarrollo Psicomotor en DIT (`QI478E1`)
- **Argumento:** Evalúa si el niño se para o camina.
- **Riesgo:** **Bidireccionalidad.** El retardo estatural severo causa debilidad muscular y retrasa los hitos motores gruesos; por tanto, es una consecuencia del retraso del crecimiento y no un factor de riesgo causal.
- **Recomendación Técnica:** **EXCLUIR `QI478E1`** y conservar solo las variables de estimulación psicosocial parental (`QI478E2` a `QI478E6`).

### 6.4 Suplementos y Tratamientos Pediátricos en `REC94` y `REC95`
- **Argumento:** Mide si el niño tomó gotas/jarabe de hierro o suplementos.
- **Riesgo:** **Causalidad Inversa.** Si el niño recibió jarabe terapéutico es porque el personal de salud ya detectó una falla nutricional en un control previo.
- **Recomendación Técnica:** **EXCLUIR las intervenciones terapéuticas** y mantener únicamente la profilaxis materna (`M45`, `M46`) y la afiliación a programas sociales preventivos.

---

## 7. Variables EXCLUIDAS Estrictamente por Fuga de Datos (Leakage)

| Variable | Descripción Oficial | Archivo | Mecanismo de Fuga de Información (Target Leakage) |
|:---|:---|:---|:---|
| `HC70` | Z-score Talla para la Edad OMS en centésimas | `RECH6` | **Variable Objetivo Directa (Target).** Usarla como predictor generaría un accuracy perfecto artificial del 100%. |
| `HW70` | Z-score Talla para la Edad OMS en Cuestionario Individual | `REC44` | **Variable Objetivo Duplicada.** Mismo indicador registrado en el cuestionario de mujeres. |
| `HC3` | Talla en centímetros (1 decimal) | `RECH6` | **Fuga Matemática Directa.** Combinada con la edad en meses (`HC1`) y sexo (`HC27`), cualquier árbol de decisión calcula el Z-score de talla/edad con exactitud milimétrica. |
| `HW3` | Talla en centímetros (1 decimal) en Cuestionario Individual | `REC44` | **Fuga Matemática Directa.** Homóloga a HC3. |
| `HC4 / HW4` | Talla/Edad Percentil | `RECH6 / REC44` | **Transformación Monótona del Target.** El percentil es la función de distribución acumulada directa del Z-score. |
| `HC5 / HW5` | Talla/Edad Desviación Estándar de la mediana de referencia | `RECH6 / REC44` | **Reconstrucción Numérica del Target.** Desvío directo de talla/edad. |
| `HC6 / HW6` | Talla/Edad Porcentaje de la mediana de referencia | `RECH6 / REC44` | **Transformación Aritmética del Target.** Ratio directo entre talla del niño y mediana OMS. |
| `HC71 / HW71` | Z-score Peso para la Edad OMS en centésimas | `RECH6 / REC44` | **Proxy de Fuga y Subrogado Clínico.** Desnutrición global; comparte más del 80% de varianza con talla baja. |
| `HC72 / HW72` | Z-score Peso para la Talla OMS en centésimas | `RECH6 / REC44` | **Proxy de Fuga y Subrogado Clínico.** Desnutrición aguda / emaciación calculada con la misma talla. |
| `HC73 / HW73` | Z-score de Índice de Masa Corporal (IMC) OMS | `RECH6 / REC44` | **Fuga Instrumental.** Fórmula que involucra la talla en el denominador ($kg/m^2$). |
| `HC13 / HW13` | Razón por la cual el niño no se midió | `RECH6 / REC44` | **Fuga Operativa del Criterio de Inclusión.** Define la elegibilidad del target. |
| `HC15 / HW15` | El niño se midió acostado o de pie | `RECH6 / REC44` | **Fuga Instrumental de Protocolo.** Se mide acostado si talla < 85 cm y de pie si >= 85 cm; filtra directamente la estatura del infante. |

---

## 8. Metadatos del Diseño Muestral Complejo a Conservar

Para asegurar que las métricas de rendimiento y la validación cruzada reflejen fielmente el comportamiento en la población infantil peruana, se deben conservar como **columnas auxiliares (no predictoras)**:

1. **`HV001` (Conglomerado / Unidad Primaria de Muestreo - UPM):**
   - Obligatorio para agrupar los datos en `StratifiedGroupKFold(n_splits=5)`.
   - Evita que niños que comparten el mismo conglomerado (misma comunidad rural, condiciones ambientales y red de agua idénticas) queden divididos entre el conjunto de entrenamiento y prueba (fuga espacial vecinal).

2. **`HV022` (Estrato de Muestreo Geográfico):**
   - Permite estratificar por región natural y tamaño de localidad durante la partición de datos.

3. **`HV005` (Factor de Ponderación Muestral del Hogar):**
   - Debe transformarse mediante `peso_muestral = HV005 / 1000000.0`.
   - Se suministra al parámetro `sample_weight` de `xgb.train()` o `XGBClassifier.fit()` para que el modelo pondere proporcionalmente a los estratos sobrerepresentados (como zonas rurales priorizadas por INEI).

4. **Llaves de Enlace Relacional:**
   - `HHID` (Identificador del hogar), `HC0` (Orden del niño en el hogar), `CASEID` (Identificador de la madre), `BIDX` / `HWIDX` (Orden de nacimiento en la historia gestacional materna).

---

## 9. Plan de Unión de Módulos (Data Merging Pipeline)

```mermaid
flowchart TD
    subgraph Hogar_y_Vivienda [Nivel Hogar / Vivienda]
        RECH0["RECH0: Geografía y Muestreo (HHID)"]
        RECH23["RECH23: Vivienda, Saneamiento y Riqueza (HHID)"]
        PS["Programas Sociales x Hogar (HHID)"]
    end
    
    subgraph Nino_Central [Nivel Niño (Población Base)]
        RECH6["RECH6: Niños < 5 años (HHID + HC0) — TARGET: HC70"]
        RECH4["RECH4: Seguro SIS del Niño (HHID + HC0)"]
        RECH1["RECH1: Cuidadores y Miembros (HHID + HC0)"]
    end
    
    subgraph Madre_Individual [Nivel Madre / Cuestionario Individual]
        RECH5["RECH5: Antropometría Materna (HHID + HC60)"]
        REC0111["REC0111: Datos Básicos MEF (CASEID)"]
        REC91["REC91: Lengua Materna y Etnia (CASEID)"]
    end
    
    subgraph Perinatal_y_Salud [Nivel Salud Infantil y Perinatal]
        REC41["REC41: Controles, Peso Nacer, Lactancia (CASEID + BIDX)"]
        REC42["REC42: Diarrea, IRA, Fiebre y Dieta (CASEID + BIDX)"]
        REC43["REC43: Carné de Vacunas (CASEID + BIDX)"]
        REC95["REC95: Controles CRED (CASEID + BIDX)"]
        DIT["DIT: Desarrollo Infantil y Apego (CASEID + BIDX)"]
    end
    
    RECH6 -->|Left Join por HHID| RECH0
    RECH6 -->|Left Join por HHID| RECH23
    RECH6 -->|Left Join por HHID| PS
    RECH6 -->|Left Join por HHID + HC0| RECH4
    RECH6 -->|Left Join por HHID + HC0| RECH1
    RECH6 -->|Enlace Madre: HHID + HC60| RECH5
    RECH6 -->|Enlace Relacional Madre-Hijo| REC41
    REC41 -->|Misma Llave Perinatal| REC42
    REC41 -->|Misma Llave Perinatal| REC43
    REC41 -->|Misma Llave Perinatal| REC95
    REC41 -->|Misma Llave Perinatal| DIT
    REC41 -->|Vía CASEID| REC0111
    REC41 -->|Vía CASEID| REC91
```

### Protocolo Secuencial de Unión y Verificaciones:
1. **Tabla Núcleo Base:** Iniciar siempre con `RECH6_2025.csv` filtrando niños válidos de 0 a 59 meses con target computable.
2. **Merge 1 (Hogar / Vivienda / Programas):** Unir `RECH6` con `RECH0`, `RECH23` y `Programas Sociales x Hogar` por `HHID` (cardinalidad N:1; muchos niños en un mismo hogar). Chequeo: El número de filas de `RECH6` debe mantenerse constante.
3. **Merge 2 (Seguro de Salud del Niño):** Unir `RECH6` con `RECH4` por `HHID` y `HC0 == IDX4` (número de orden del niño en el hogar, cardinalidad 1:1). Chequeo: No deben generarse filas duplicadas.
4. **Merge 3 (Madre en Hogar):** `HC60` en `RECH6` indica el número de orden de la madre en el hogar. Unir `RECH6` con `RECH5` mediante `HHID` y `HC60 == HA0` para traer la talla e IMC de la madre.
5. **Merge 4 (Historia Gestacional y Perinatal):** Para vincular con `REC41`, `REC42`, `REC43`, `REC95` y `DIT`, se utiliza el identificador de la madre (`CASEID`) y el número de orden de nacimiento del niño (`BIDX` / `HWIDX`). En ENDES, para mujeres del hogar evaluadas en el cuestionario individual, `CASEID = rpad(HHID, 15) + lpad(HC60, 3)`. Chequeo: Verificar tasa de acoplamiento madre-hijo (esperada > 95% para niños que residen con su madre biológica).
---

## 10. Módulos Complementarios Analizados (1031, 1036 y 1041)

> **Actualización metodológica:** A diferencia del informe preliminar de anemia (que carecía de estos diccionarios), **se integraron y analizaron formalmente los 13 diccionarios oficiales** de los módulos solicitados, extrayendo predictores de alto impacto:

1. **Módulo 1031 (MEF - Cuestionario Individual de Mujeres):**
   - Archivos: `Diccionario - REC0111.pdf` (104 vars) y `Diccionario - REC91.pdf` (343 vars).
   - Variables clave incorporadas: Edad materna (`V012`), escolaridad (`V106`), autoidentificación étnica (`V131`), lengua materna quechua/aimara/amazónica (`S119`), estado conyugal (`V501`) y autonomía en decisiones de salud (`V743A`).

2. **Módulo 1036 (Inmunización y Salud Infantil):**
   - Archivos: `Diccionario - DIT.pdf` (63 vars), `Diccionario - REC42.pdf` (169 vars), `Diccionario - REC43.pdf` (168 vars) y `Diccionario - REC95.pdf` (315 vars).
   - Variables clave incorporadas: Episodios de diarrea aguda EDA (`V411`, `V411A`), fiebre e infecciones respiratorias IRA (`V414`, `V415`), diversidad dietética de 24 horas, esquema de vacunación completo contra Rotavirus y Neumococo (`H31B`, `H32B`), carné verificado (`H1`) y número de controles CRED recibidos (`S45C`).

3. **Módulo 1041 (Programas Sociales):**
   - Archivos: `Diccionario - Programas Sociales x Hogar.pdf` (20 vars), `PS_CUNAMAS_VISITA.pdf` (10 vars), `PS_WAWAWASI.pdf` (10 vars), `PS_VL.pdf` (10 vars), `PS_COMEDOR.pdf` (10 vars), `PS_QALIWARMA.pdf` (11 vars) y `PS_TRABAJA.pdf` (10 vars).
   - Variables clave incorporadas: Beneficiario del Programa JUNTOS (`QH95`), Cuna Más Acompañamiento / Cuidado Diurno (`QH106`), Vaso de Leche (`QH101`) y Comedores Populares (`QH103`).

---

## 11. Tabla Comparativa de Cambios Respecto al Catálogo de Anemia

La siguiente tabla documenta las variables cuya clasificación y rol sufrieron cambios estructurales al migrar el objetivo de **Anemia Infantil** a **Desnutrición Crónica Infantil**:

| Variable | Descripción Oficial | Decisión en Proyecto Anemia | Decisión en Proyecto Desnutrición Crónica | Justificación Epidemiológica del Cambio |
|:---|:---|:---|:---|:---|
| `HC70 / HW70` | Z-score Talla/Edad | `DUDOSA (CLÍNICA)` | ****VARIABLE OBJETIVO (TARGET)**** | En anemia era una medición física concurrente dudosa; en desnutrición crónica constituye el fenómeno a predecir (< -200). |
| `HC57 / HC57A` | Nivel de Anemia (MINSA / OMS) | `VARIABLE OBJETIVO (TARGET)` | ****DUDOSA (BIOMARCADOR CONCURRENTE)**** | Pasa de ser el target del proyecto anterior a ser un biomarcador clínico invasivo concurrente opcional. |
| `HC53 / HC56` | Nivel de Hemoglobina crudo y ajustado | `EXCLUIR POR LEAKAGE DIRECTO` | ****DUDOSA (BIOMARCADOR CONCURRENTE)**** | En anemia era fuga matemática absoluta; en desnutrición es un predictor clínico concurrente correlacionado. |
| `HC3 / HW3` | Talla en centímetros del niño | `DUDOSA (CLÍNICA)` | ****EXCLUIR POR LEAKAGE CRÍTICO**** | En anemia aportaba proxy de crecimiento; en desnutrición reconstruye directamente el target con la edad y el sexo. |
| `M19` | Peso al nacer en gramos | `PREDICTOR RECOMENDADO` | ****PREDICTOR CRÍTICO DE PRIMER ORDEN**** | El bajo peso al nacer (< 2,500 g) es el factor etiológico intrauterino más potente de retardo estatural en menores de 5 años. |
| `M4 / M5` | Lactancia materna total y exclusiva | `PREDICTOR SECUNDARIO` | ****PREDICTOR PRIORITARIO DE NUTRICIÓN**** | La lactancia materna exclusiva en los primeros 6 meses previene directamente la enteropatía y el retraso del crecimiento. |
| `HV201 / HV205` | Agua para beber y tipo de baño | `PREDICTOR DE ENTORNO` | ****PREDICTOR ETIOLÓGICO CLAVE (JMP)**** | El agua no tratada y el fecalismo ambiental provocan enteropatía ambiental subclínica, alterando la absorción de nutrientes. |
| `HA3` | Talla de la madre en centímetros | `NO INCLUIDA` | ****PREDICTOR BIOLÓGICO PRIORITARIO**** | La talla baja materna (< 150 cm) refleja el ciclo intergeneracional de la desnutrición y predispone epigenéticamente al hijo. |
| `V411 / V411A` | Episodios de diarrea aguda reciente | `NO DISPONIBLE EN CATÁLOGO ANTERIOR` | ****PREDICTOR INMEDIATO (UNICEF)**** | Causa inmediata de pérdida aguda de peso y retardo estatural por inflamación del epitelio digestivo. |
| `H31B / H32B` | Vacunas Rotavirus y Neumococo | `NO DISPONIBLE EN CATÁLOGO ANTERIOR` | ****PREDICTOR PREVENTIVO DE PRIMER ORDEN**** | Previene diarreas virales deshidratantes y neumonías bacterianas recurrentes que desencadenan desnutrición crónica. |
| `QH95` | Programa JUNTOS en el hogar | `NO DISPONIBLE EN CATÁLOGO ANTERIOR` | ****PREDICTOR DE CONDICIONALIDAD SOCIAL**** | Incentivo monetario del Estado condicionado a que la madre lleve al niño a sus controles CRED y vacunas. |
| `QH106` | Cuna Más / Wawa Wasi | `NO DISPONIBLE EN CATÁLOGO ANTERIOR` | ****PREDICTOR DE CUIDADO Y DIETA TEMPRANA**** | Intervención del MIDIS que suministra 70% de requerimientos calórico-proteicos diarios al menor de 36 meses. |

---

## 12. Resumen Final: Conteo de Variables y Bloque de Código Python

### 12.1 Conteo Consolidado por Categoría de Decisión
- **Total de Variables Oficiales Evaluadas:** 1807
- **Variables SELECCIONADAS para la Matriz Explicativa ($X$):** 220
- **Variables DUDOSAS (Biomarcadores o Riesgo de Causalidad Inversa):** 98
- **Variables EXCLUIDAS por Fuga de Datos (Leakage) o Causalidad Inversa:** 32
- **Variables MANTENIDAS como Metadatos del Diseño Muestral / Llaves:** 93
- **Variables Identificadas como Objetivo (Target Directo o Secundario):** 2
- **Variables EXCLUIDAS por Irrelevancia Operativa, Administrativa o Alta Incompletitud:** 1362

### 12.2 Lista Final de Predictores en Bloque de Código Python

```python
# =============================================================================
# CONFIGURACIÓN OFICIAL DE VARIABLES - MODELO PREDICTIVO DESNUTRICIÓN CRÓNICA
# ENDES 2025 (INEI, PERÚ) - XGBOOST
# =============================================================================

TARGET = 'desnutricion_cronica'  # 1 si HC70 < -200, 0 en caso contrario
TARGET_ORIGIN = 'HC70'          # Z-score Talla/Edad OMS en centésimas

# Metadatos de Diseño Muestral Complejo (No usar como predictores en X)
CLUSTER_COL = 'HV001'           # Conglomerado (PSU) para GroupKFold
STRATUM_COL = 'HV022'           # Estrato de muestreo
WEIGHT_COL = 'peso_muestral'    # HV005 / 1,000,000 para sample_weight

# Identificadores Relacionales para Enlace entre Módulos
ID_COLS = [
    'HHID',                     # Identificador del hogar
    'HC0',                      # Número de orden del niño en el hogar
    'HC60',                     # Número de orden de la madre en el hogar
    'CASEID',                   # Identificador de la mujer (Cuestionario Individual)
    'BIDX'                      # Orden de nacimiento del niño en historia obstétrica
]

# Lista Definitiva de Predictores (X) - 100% Compatibles con Screening Comunitario
FEATURES = [
    # --- Niño: Factores Biológicos ---
    'edad_meses',               # HC1: 0 a 59 meses
    'sexo_nino',                # HC27: 1 Hombre, 2 Mujer
    'peso_al_nacer_g',          # M19: Peso al nacer en gramos (< 2500g = RCIU)
    'tamano_nacer_aparente',    # M19A: Reporte cualitativo del tamaño al nacer
    'duracion_lactancia_m',     # M4: Meses totales de lactancia
    'lactancia_exclusiva_m',    # M5: Meses de lactancia materna exclusiva
    'intervalo_intergenesico',  # B11: Meses desde el nacimiento previo
    
    # --- Madre: Antropometría, Educación y Autonomía ---
    'talla_madre_cm',           # HA3: Talla materna (herencia y ciclo intergeneracional)
    'imc_madre',                # HA40: Índice de masa corporal materno
    'edad_madre_anos',          # V012: Edad de la madre en años
    'educacion_madre_nivel',    # V106 / HC61: Sin educación, Primaria, Secundaria, Superior
    'educacion_madre_anos',     # V107 / HC68: Años de estudio aprobados
    'estado_conyugal_madre',    # V501: Casada, conviviente, soltera, separada
    'madre_trabaja',            # V714: Condición de trabajo de la madre (0/1)
    'autonomia_salud_madre',    # V743A: Toma de decisiones en atención médica
    'hierro_madre_gestacion',   # M45: Suplementación con hierro en el embarazo
    'dias_hierro_madre',        # M46: Días de consumo de hierro gestacional
    'controles_prenatales',     # M14: Número total de controles prenatales
    'mes_inicio_prenatal',      # M18: Mes de inicio del primer control prenatal
    'lugar_parto',              # M15: Institucional (hospital/centro) vs. Domicilio
    'atencion_parto_calif',     # M3A: Atención por médico u obstetra calificado
    'lengua_materna_madre',     # S119: Quechua, Aimara, Nativa, Castellano
    
    # --- Hogar y Entorno Demográfico ---
    'total_miembros_hogar',     # HV009: Número de integrantes en el hogar
    'menores_5anos_hogar',      # HV014: Cantidad de niños menores de 5 años
    'mujeres_edad_fertil',      # HV010: Número de mujeres elegibles en el hogar
    
    # --- Vivienda, Saneamiento y Riqueza (JMP OMS/UNICEF) ---
    'fuente_agua_beber',        # HV201: Tipo de abastecimiento de agua
    'tipo_servicio_higienico',  # HV205: Tipo de baño (red, letrina, pozo, campo)
    'bano_compartido',          # HV225: Servicio higiénico compartido (0/1)
    'tratamiento_agua',         # HV237: Hierve, clora o filtra el agua para beber
    'material_piso',            # HV213: Piso de tierra/arena vs. terminado
    'habitaciones_dormir',      # HV216: Habitaciones para dormir (hacinamiento)
    'combustible_cocinar',      # HV226: Biomasa (leña/carbón) vs. gas/electricidad
    'tiene_electricidad',       # HV206: Electricidad en la vivienda (0/1)
    'tiene_refrigerador',       # HV209: Refrigeradora para conservación de alimentos
    'quintil_riqueza',          # HV270: Quintil socioeconómico del hogar (1 a 5)
    
    # --- Geografía Territorial ---
    'departamento',             # HV024: Departamento de residencia (1 a 25)
    'area_residencia',          # HV025: 1 Urbano, 2 Rural
    'altitud_msnm',             # HV040: Altitud en metros sobre el nivel del mar
    
    # --- Salud Infantil, Morbilidad Reciente e Inmunización ---
    'seguro_sis',               # SH11A: Niño afiliado al Seguro Integral de Salud
    'diarrea_reciente_eda',     # V411: Tuvo diarrea en las últimas 2 semanas (0/1)
    'diarrea_con_sangre',       # V411A: Diarrea disentérica bacteriana (0/1)
    'tratamiento_sro',          # V413: Sales de Rehidratación Oral (0/1)
    'fiebre_reciente',          # V414: Tuvo fiebre en las últimas 2 semanas (0/1)
    'tos_ira_reciente',         # V415: Tuvo tos / infección respiratoria (0/1)
    'carne_vacunacion_visto',   # H1: Carné oficial de vacunas visto por encuestadora
    'vacuna_bcg',               # H2: Vacuna al nacer (0/1)
    'vacuna_rotavirus_completa',# H31B: Dosis 2 de vacuna contra Rotavirus (0/1)
    'vacuna_neumococo_dosis2',  # H32B: Dosis 2 de vacuna contra Neumococo (0/1)
    'vacuna_spr1',              # H9: Vacuna contra Sarampión / SPR (0/1)
    'suplemento_vitamina_a',    # H34: Vitamina A en últimos 6 meses (0/1)
    'desparasitacion_infantil', # H43: Antiparasitario en últimos 6 meses (0/1)
    'controles_cred_numero',    # S45C: Número total de controles CRED recibidos
    
    # --- Programas Sociales y Transferencias del Estado ---
    'programa_juntos',          # QH95: Beneficiario del Programa JUNTOS (1/2)
    'programa_vaso_leche',      # QH101: Beneficiario del Programa Vaso de Leche (1/2)
    'programa_comedor',         # QH103: Beneficiario de Comedores Populares (1/2)
    'programa_cuna_mas'         # QH106: Beneficiario de Cuna Más / Wawa Wasi (1/2)
]

# Variables Categóricas a codificar en XGBoost (enable_categorical=True o Target/OneHot Encoding)
CATEGORICAL_FEATURES = [
    'departamento', 'area_residencia', 'fuente_agua_beber', 'tipo_servicio_higienico',
    'material_piso', 'combustible_cocinar', 'quintil_riqueza', 'lugar_parto',
    'educacion_madre_nivel', 'estado_conyugal_madre', 'lengua_materna_madre',
    'carne_vacunacion_visto', 'tamano_nacer_aparente'
]
```

