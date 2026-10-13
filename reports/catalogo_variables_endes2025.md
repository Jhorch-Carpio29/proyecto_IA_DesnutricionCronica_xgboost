# Catálogo Exhaustivo de Variables — ENDES 2025 (INEI)

## Análisis de Relevancia, Fuga de Información y Selección para XGBoost

**Proyecto:** Predicción del Riesgo de Anemia en Niños de 6 a 59 meses en el Perú  
**Fuente oficial:** Instituto Nacional de Estadística e Informática (INEI) — ENDES 2025  
**Fecha de generación:** Octubre 2026  

---
## 1. Criterios Metodológicos de Evaluación
Para seleccionar los predictores de forma rigurosa y defendible ante el comité evaluador, se aplicaron cuatro principios fundamentales:
1. **Condición de Entrevista Comunitaria (No Invasivo / Sin Mediciones Clínicas):** El modelo está orientado a salud pública comunitaria para priorizar tamizaje preventivo. Por ende, debe basarse en información que un promotor de salud o enfermera pueda recoger por cuestionario/entrevista, sin requerir equipos clínicos (balanzas calibradas, tallímetros o hemoglobinómetros).
2. **Prevención Estricta de Fuga de Información (Target Leakage):** Se prohíbe el uso de cualquier medición de hemoglobina (cruda o ajustada), clasificaciones previas de anemia o consentimientos médicos, ya que derivan directamente del análisis bioquímico.
3. **Prevención de Causalidad Inversa:** Variables de intervenciones farmacológicas dirigidas al niño (ej. jarabe de hierro o tratamiento terapéutico de anemia en `REC94`) implican que el niño ya fue diagnosticado y tratado; incluirlas como predictores engañaría al modelo confundiéndolo con causalidad.
4. **Respeto al Diseño Muestral Complejo:** Las variables de conglomerado (`HV001`), estrato (`HV022`) y factor de ponderación (`HV005`) deben conservarse intactas en la base depurada para garantizar validación cruzada agrupada y estimaciones poblacionales insesgadas.

---
## 2. Resumen Ejecutivo del Inventario de Datos

| Módulo | Archivo CSV | Registros | Columnas | Descripción del Módulo | Rol Principal en el Proyecto |
|:---|:---|---:|---:|:---|:---|
| `RECH6` | `RECH6_2025.csv` | 19,298 | 43 | Cuestionario de Hogar: Niños menores de 5 años evaluados en hemoglobina y antropometría. | **Módulo Núcleo: TARGET + Niño** |
| `REC44` | `REC44_2025.csv` | 18,841 | 34 | Cuestionario Individual de Mujeres: Evaluación de hijos nacidos en los últimos 5 años. | Módulo Niño (Cuest. Individual) |
| `RECH5` | `RECH5_2025.csv` | 37,679 | 40 | Evaluación de anemia y estado nutricional de mujeres de 15 a 49 años. | Módulo Descartado (No núcleo) |
| `RECH0` | `RECH0_2025.csv` | 37,331 | 44 | Identificación del hogar, ubicación territorial, conglomerados y factores de ponderación. | **Diseño Muestral + Geografía** |
| `RECH4` | `RECH4_2025.csv` | 131,929 | 22 | Cobertura de seguro de salud (SIS, EsSalud, Privado) para los integrantes del hogar. | Seguro SIS del Hogar |
| `RECH1` | `RECH1_2025.csv` | 131,929 | 36 | Relación de parentesco, sexo, edad y educación de los miembros habituales del hogar. | Módulo Descartado (No núcleo) |
| `RECHM` | `RECHM_2025.csv` | 2,714 | 8 | Registro de miembros ausentes o migraciones recientes. | Módulo Descartado (No núcleo) |
| `RECH23` | `RECH23_2025.csv` | 37,331 | 130 | Materiales de construcción, abastecimiento de agua, saneamiento e índice de riqueza. | **Vivienda, Agua y Riqueza** |
| `REC41` | `REC41_2025.csv` | 18,841 | 147 | Historial gestacional, controles prenatales, peso al nacer y prácticas de lactancia materna. | **Gestación y Lactancia** |
| `REC94` | `REC94_2025.csv` | 18,841 | 61 | Consumo de gotas/jarabe de hierro, tamizaje de anemia y tratamientos infantiles. | Suplementación (Dudosa) |

---
## 3. Catálogo Detallado de Variables por Archivo CSV

### 📁 Archivo: `RECH6_2025.csv` — Módulo 1638: Evaluación Antropométrica y Anemia del Niño (RECH6)
**Total de columnas:** 43 | **Total de filas en origen:** 19,298  

| Variable | Descripción Oficial (INEI) | Tipo | % Nulos (Muestra) | Clasificación / Rol | Justificación Metodológica |
|:---|:---|:---|---:|:---|:---|
| `ID1` | Año | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `HHID` | Identificación Cuestionario Individual | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `HC0` | Número de orden en el hogar | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `HC1` | Edad en meses | `int64` | 0.0% | **PREDICTOR RECOMENDADO** | Edad del niño en meses (6 a 59). Factor biológico central de requerimiento de hierro. |
| `HC2` | Peso en kilogramos (1 dec.) | `int64` | 0.0% | **DUDOSA: CLÍNICA** | Medición física clínica (peso, talla, Z-score OMS). Requiere tallímetro/balanza; no se obtiene por simple entrevista. |
| `HC3` | Altura en centímetros (1 dec.) | `int64` | 0.0% | **DUDOSA: CLÍNICA** | Medición física clínica (peso, talla, Z-score OMS). Requiere tallímetro/balanza; no se obtiene por simple entrevista. |
| `HC4` | Talla/Edad percentil | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC5` | Talla/Edad Desviación Estándar | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC6` | Talla/Edad porcentaje de la mediana de referencia | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC7` | Peso/Edad percentil | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC8` | Peso/Edad Desviación Estándar | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC9` | Peso/Edad porcentaje de la mediana de referencia | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC10` | Peso/Talla percentil | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC11` | Peso/Talla Desviación Estándar | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC12` | Peso/Talla Porcentaje de la mediana de referencia | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC13` | Razón por la cual el niño no se midió | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC15` | El niño se midió acostado o de pie | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC16` | Día de nacimiento del niño | `int64` | 0.0% | **DESCARTAR: ADMINISTRATIVA** | Variable operativa de la logística de campo de la encuesta; sin relevancia epidemiológica. |
| `HC19` | Año de la medición | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC27` | Sexo | `int64` | 0.0% | **PREDICTOR RECOMENDADO** | Sexo del niño (1: Hombre, 2: Mujer). Diferencias fisiológicas en la velocidad de crecimiento. |
| `HC30` | Mes de nacimiento del niño | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC31` | Año de nacimiento del niño | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC32` | Fecha de nacimiento (cmc) | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC33` | Fecha de información completa | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC51` | Número de orden del padre o responsable | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC52` | Leyó la declaración de consentimiento | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC53` | Nivel de hemoglobina (g/dl-1 decimal) | `int64` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HC55` | Resultado de medir (hemoglobina) | `int64` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HC56` | Nivel de hemoglobina ajustado por altitud (g/dl-1 decimal) RM 363-2022-MINSA Nivel de hemoglobina ajustada por altitud en g/dl - 1 decimal NUEVA DIRECTRIZ OMS | `int64` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HC56A` | N 2024/RM 251-2024-MINSA | `int64` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HC57` | Nivel de anemia RM 363-2022-MINSA | `int64` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HC57A` | Nivel de Anemia NUEVA DIRECTRIZ OMS 2024/RM 251-2024-MINSA | `int64` | 0.0% | **TARGET** | Variable objetivo oficial según directriz OMS 2024 / RM 251-2024-MINSA (1,2,3 -> Anemia; 4 -> Sin anemia). |
| `HC58` | Está de acuerdo con enviar los datos a un especialista | `str` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HC60` | Número de orden de la madre en el hogar | `int64` | 0.0% | **LLAVE / VÍNCULO** | Número de orden de la madre en el hogar para vincular historia obstétrica. |
| `HC61` | El nivel educativo más alto de la madre | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC62` | El año más alto de educación de la madre | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC63` | Intervalo de los nacimientos anteriores al niño | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC64` | Número de orden de nacimiento | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC68` | Nivel educativo más alto (CS para informe preliminar y final) | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HC70` | Talla/Edad de la Desviación Estándar de la mediana de referencia (según la OMS) | `int64` | 0.0% | **DUDOSA: CLÍNICA** | Medición física clínica (peso, talla, Z-score OMS). Requiere tallímetro/balanza; no se obtiene por simple entrevista. |
| `HC71` | Peso/Edad de la Desviación Estándar de la mediana de referencia (según la OMS) | `int64` | 0.0% | **DUDOSA: CLÍNICA** | Medición física clínica (peso, talla, Z-score OMS). Requiere tallímetro/balanza; no se obtiene por simple entrevista. |
| `HC72` | Peso/Talla Desviación Estándar de la mediana de referencia (según la OMS) | `int64` | 0.0% | **DUDOSA: CLÍNICA** | Medición física clínica (peso, talla, Z-score OMS). Requiere tallímetro/balanza; no se obtiene por simple entrevista. |
| `HC73` | Desviación Estándar del IMC (según la OMS) | `int64` | 0.0% | **DUDOSA: CLÍNICA** | Medición física clínica (peso, talla, Z-score OMS). Requiere tallímetro/balanza; no se obtiene por simple entrevista. |

### 📁 Archivo: `REC44_2025.csv` — Módulo 1638: Peso, Talla y Anemia en Hijos de Mujeres 15-49 (REC44)
**Total de columnas:** 34 | **Total de filas en origen:** 18,841  

| Variable | Descripción Oficial (INEI) | Tipo | % Nulos (Muestra) | Clasificación / Rol | Justificación Metodológica |
|:---|:---|:---|---:|:---|:---|
| `ID1` | Año | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `CASEID` | Identificación de caso | `str` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `HWIDX` | Número de orden de la historia del nacimiento | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `HW1` | Edad en meses | `str` | 0.0% | **PREDICTOR RECOMENDADO** | Edad del niño en meses (6 a 59). Factor biológico central de requerimiento de hierro. |
| `HW2` | Peso en kilogramos (1 decimal) | `str` | 0.0% | **DUDOSA: CLÍNICA** | Medición física clínica (peso, talla, Z-score OMS). Requiere tallímetro/balanza; no se obtiene por simple entrevista. |
| `HW3` | Talla en centímetros (1 decimal) | `str` | 0.0% | **DUDOSA: CLÍNICA** | Medición física clínica (peso, talla, Z-score OMS). Requiere tallímetro/balanza; no se obtiene por simple entrevista. |
| `HW4` | Talla/Edad percentil | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HW5` | Talla/Edad de las Desviación Estándar de la mediana de referencia | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HW6` | Talla/Edad porcentaje de la mediana de referencia | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HW7` | Peso/Edad percentil | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HW8` | Peso/Edad Desviación Estándar de la mediana de referencia | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HW9` | Peso/Edad porcentaje de la mediana de referencia | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HW10` | Peso/Talla percentil | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HW11` | Peso/Talla Desviación Estándar de la mediana de referencia | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HW12` | Peso/Talla porcentaje de la mediana de referencia | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HW13` | Razón por la cual el niño no se midió | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HW15` | El niño se midió acostado o de pie | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HW16` | Día de nacimiento del niño | `str` | 0.0% | **DESCARTAR: ADMINISTRATIVA** | Variable operativa de la logística de campo de la encuesta; sin relevancia epidemiológica. |
| `HW17` | Día de la medición | `str` | 0.0% | **DESCARTAR: ADMINISTRATIVA** | Variable operativa de la logística de campo de la encuesta; sin relevancia epidemiológica. |
| `HW18` | Mes de la medición | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HW19` | Año de la medición | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HW51` | Número de orden del padre o responsable | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HW52` | Leyó la declaración de consentimiento para la medición de hemoglobina | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HW53` | Nivel de hemoglobina (g /dl -1 decimal) | `str` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HW55` | Resultado de la medición (Hemoglobina) | `int64` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HW56` | Nivel de hemoglobina ajustada por altitud en g/dl - 1 decimal RM 363-2022-MINSA Nivel de hemoglobina ajustada por altitud en g/dl - 1 decimal NUEVA DIRECTRIZ OMS | `str` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HW56A` | N 2024/RM 251-2024-MINSA | `str` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HW57` | Nivel de anemia RM 363-2022-MINSA | `str` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HW57A` | Nivel de Anemia NUEVA DIRECTRIZ OMS 2024/RM 251-2024-MINSA | `str` | 0.0% | **TARGET** | Variable objetivo oficial según directriz OMS 2024 / RM 251-2024-MINSA (1,2,3 -> Anemia; 4 -> Sin anemia). |
| `HW58` | Está de acuerdocon enviar los datos a un especialista | `str` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HW70` | Talla/Edad de la Desviación Estándar de la mediana de referencia (según la OMS) | `str` | 0.0% | **DUDOSA: CLÍNICA** | Medición física clínica (peso, talla, Z-score OMS). Requiere tallímetro/balanza; no se obtiene por simple entrevista. |
| `HW71` | Peso/Edad de la Desviación Estándar de la mediana de referencia (según la OMS) | `str` | 0.0% | **DUDOSA: CLÍNICA** | Medición física clínica (peso, talla, Z-score OMS). Requiere tallímetro/balanza; no se obtiene por simple entrevista. |
| `HW72` | Peso/Talla Desviación Estándar de la mediana de referencia (según la OMS) | `str` | 0.0% | **DUDOSA: CLÍNICA** | Medición física clínica (peso, talla, Z-score OMS). Requiere tallímetro/balanza; no se obtiene por simple entrevista. |
| `HW73` | Desviación Estándar del IMC (según la OMS) | `str` | 0.0% | **DUDOSA: CLÍNICA** | Medición física clínica (peso, talla, Z-score OMS). Requiere tallímetro/balanza; no se obtiene por simple entrevista. |

### 📁 Archivo: `RECH5_2025.csv` — Módulo 1638: Mediciones Antropométricas y Hemoglobina en Mujeres 15-49 (RECH5)
**Total de columnas:** 40 | **Total de filas en origen:** 37,679  

| Variable | Descripción Oficial (INEI) | Tipo | % Nulos (Muestra) | Clasificación / Rol | Justificación Metodológica |
|:---|:---|:---|---:|:---|:---|
| `ID1` | Año | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `HHID` | Identificación de caso | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `HA0` | Número de orden en el hogar | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `HA1` | Edad de la mujer en años | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA2` | Peso en kilogramos (1 decimal) | `int64` | 0.0% | **DUDOSA: CLÍNICA** | Medición física clínica (peso, talla, Z-score OMS). Requiere tallímetro/balanza; no se obtiene por simple entrevista. |
| `HA3` | Talla en centímetros (1 decimal) | `int64` | 0.0% | **DUDOSA: CLÍNICA** | Medición física clínica (peso, talla, Z-score OMS). Requiere tallímetro/balanza; no se obtiene por simple entrevista. |
| `HA4` | Talla/Edad percentil en que se encuentra | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA5` | Talla/Edad Desviación Estándar | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA6` | Talla/Edad porcentaje respecto a la mediana de referencia | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA11` | Peso/Talla desvio estándar (DHS) | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA12` | Peso/Talla Porcentaje respecto a la mediana (DHS) | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA12A` | Peso/Talla Porcentaje respecto a la mediana (Foggarty) | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA12B` | Peso/Talla Porcentaje respecto a la mediana (OMS) | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA13` | Resultado de medición de la entrevistada | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA32` | Fecha de nacimiento (cmc) | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA33` | Fecha de información completa | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA35` | En las últimas 24 horas cuantos cigarrillos fumó Ud. | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA40` | Índice de Masa Corporal para la entrevistada | `int64` | 0.0% | **DUDOSA: CLÍNICA** | Medición física clínica (peso, talla, Z-score OMS). Requiere tallímetro/balanza; no se obtiene por simple entrevista. |
| `HA41` | Índice de Rohrer para la entrevistada | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA50` | Grupos de mujeres de 12 a 49 años de edad | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA51` | Número de orden del padre o responsable | `str` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA52` | Leyó la declaración de consentimiento para la medición de hemoglobina | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA53` | Nivel de hemoglobina (g/dl - 1 decimal) | `int64` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HA54` | Actualmente embarazada | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA55` | Resultado de la medición (hemoglobina) | `int64` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HA56` | Nivel de hemoglobina ajustado por la altitud (g/dl - 1 decimal) RM 363-2022-MINSA Nivel de hemoglobina ajustada por altitud en g/dl - 1 decimal NUEVA DIRECTRIZ OMS | `int64` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HA56A` | N 2024/RM 251-2024-MINSA | `str` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HA57` | Nivel de anemia RM 363-2022-MINSA | `int64` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HA57A` | Nivel de Anemia NUEVA DIRECTRIZ OMS 2024/RM 251-2024-MINSA | `int64` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HA58` | Está de acuerdo con enviar los datos a un especialista | `str` | 0.0% | **FUGA DE DATOS** | Medición directa de hemoglobina, nivel previo de anemia o consentimiento médico. Debe excluirse para evitar Target Leakage. |
| `HA60` | Estado civil | `str` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA61` | Lea la declaración de consentimiento (VIH) | `str` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA62` | Número de identificación de la muestra de sangre | `str` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA63` | Resultado de la medición (VIH) | `str` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA64` | Consentimiento para pruebas adicionales | `str` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA65` | Resultado de la entrevista individual a la mujer | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA66` | El nivel educativo más alto aprobado de la mujer | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA67` | El año más alto de educación de la mujer | `str` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA68` | Nivel educativo más alto (CS para el informe preliminar y final) | `int64` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |
| `HA69` | Peso del VIH (6 decimales) | `str` | 0.0% | **DESCARTAR: POBLACIÓN DISTINTA** | Módulo de mujeres 15-49 años. Las características del niño se toman directamente de RECH6. |

### 📁 Archivo: `RECH0_2025.csv` — Módulo 1629: Características del Hogar, Geografía y Muestra (RECH0)
**Total de columnas:** 44 | **Total de filas en origen:** 37,331  

| Variable | Descripción Oficial (INEI) | Tipo | % Nulos (Muestra) | Clasificación / Rol | Justificación Metodológica |
|:---|:---|:---|---:|:---|:---|
| `ID1` | Año | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `HHID` | Identificacion Cuestionario del Hogar | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `HV000` | Código del país | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV001` | Conglomerado | `int64` | 0.0% | **DISEÑO MUESTRAL** | Obligatoria para ponderación poblacional (HV005/1e6) y partición Train/Test por conglomerado (HV001) sin fuga espacial. |
| `HV002` | Vivienda | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV002A` | Hogar | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV003` | Número de orden del Informante del cuestionario del hogar | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV004` | Unidad última de muestreo | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV007` | Año de entrevista | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV008` | Fecha de entrevista meses (CMC) | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV009` | Total de personas en el hogar | `int64` | 0.0% | **PREDICTOR RECOMENDADO** | Composición del hogar (total personas y menores de 5 años; hacinamiento y carga de cuidado). |
| `HV010` | Número de mujeres elegibles para entrevista individual | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV011` | Número de hombres elegibles por hogar | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV012` | Número de miembros de jure (residentes habituales) | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV013` | Número de miembros de facto (personas que durmieron la noche anterior) | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV014` | Número de niños menores de 5 años | `int64` | 0.0% | **PREDICTOR RECOMENDADO** | Composición del hogar (total personas y menores de 5 años; hacinamiento y carga de cuidado). |
| `HV015` | Resultado de la entrevista en el hogar | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV017` | Número de visitas | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV020` | Sin descripción en ficha técnica | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV021` | Unidad de muestreo primario (conglomerado) | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV023` | Dominio | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV024` | Región | `int64` | 0.0% | **PREDICTOR RECOMENDADO** | Región geográfica / Departamento. Captura brechas estructurales y territoriales. |
| `HV025` | Sin descripción en ficha técnica | `int64` | 0.0% | **PREDICTOR RECOMENDADO** | Área de residencia (Urbano / Rural). Determinante socio-sanitario de saneamiento y acceso a salud. |
| `HV026` | Sin descripción en ficha técnica | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV027` | Selección para hombre/esposo | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV028` | Peso de muestra masculino | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV030` | Supervisor de campo | `int64` | 0.0% | **DESCARTAR: ADMINISTRATIVA** | Variable operativa de la logística de campo de la encuesta; sin relevancia epidemiológica. |
| `HV031` | Editor de campo | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV032` | Editor de la oficina | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV033` | Ultimate area selection prob. | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV035` | Número de niños elegibles para altura y peso | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV040` | Altitud del conglomerado en metros | `int64` | 0.0% | **PREDICTOR RECOMENDADO** | Altitud en m.s.n.m. Variable fisiológica ambiental clave de hipoxia y adaptación hematopoyética. |
| `HV041` | Número de mujeres con medición de peso y talla | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV042` | Sin descripción en ficha técnica | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV043` | Sin descripción en ficha técnica | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV044` | Sin descripción en ficha técnica | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `UBIGEO` | Código de Ubicación Gegráfica | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV005` | Factor de ponderación | `int64` | 0.0% | **DISEÑO MUESTRAL** | Obligatoria para ponderación poblacional (HV005/1e6) y partición Train/Test por conglomerado (HV001) sin fuga espacial. |
| `HV022` | Estrato | `int64` | 0.0% | **DISEÑO MUESTRAL** | Obligatoria para ponderación poblacional (HV005/1e6) y partición Train/Test por conglomerado (HV001) sin fuga espacial. |
| `NCONGLOME1` | Número de conglomerado asignado (muestra) | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `CODCCPP` | Codigo de Centro Poblado | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `NOMCCPP` | Nombre del Centro Poblado | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `LONGITUDX` | Longitud del conglomerado | `float64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `LATITUDY` | Latitud del conglomerado | `float64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |

### 📁 Archivo: `RECH4_2025.csv` — Módulo 1629: Salud y Afiliación a Seguros por Miembro (RECH4)
**Total de columnas:** 22 | **Total de filas en origen:** 131,929  

| Variable | Descripción Oficial (INEI) | Tipo | % Nulos (Muestra) | Clasificación / Rol | Justificación Metodológica |
|:---|:---|:---|---:|:---|:---|
| `ID1` | Año | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `HHID` | Identificacion Cuestionario del Hogar | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `IDXH4` | Número de orden del listado del hogar | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `SH11A` | Seguro de salud: ESSALUD/IPSS | `int64` | 0.0% | **PREDICTOR RECOMENDADO** | Afiliación a Seguro Integral de Salud (SIS). Acceso a programas preventivos del Estado. |
| `SH11B` | Seguro de salud: Militar | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH11C` | Seguro de salud: Integral | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH11D` | Seguro de salud: Compañía de seguros | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH11E` | Seguro de salud: Seguro privado | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH11Y` | Seguro de salud: No sabe | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH11Z` | Seguro de salud: No tienen | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH12` | Alguno de los seguros está a su nombre | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH13` | Actividad de la ultima semana | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH15N` | Nivel de educación aprobado | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH15Y` | Nivel de educación en años | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH15G` | Nivel de educación en grados | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH18N` | Nivel de educación que actualmente asiste o se matriculó | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH18Y` | Año al que actualmente asiste o se matriculó | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH18G` | Grado al que actualmente asiste o se matriculó | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH20N` | Nivel educativo al que asistió el año pasado | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH20Y` | Año al que asistió el año pasado | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH20G` | Grado al que asistió el año pasado | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH21` | Resultado de la asistencia del año escolar pasado | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |

### 📁 Archivo: `RECH1_2025.csv` — Módulo 1629: Lista de Miembros del Hogar y Parentesco (RECH1)
**Total de columnas:** 36 | **Total de filas en origen:** 131,929  

| Variable | Descripción Oficial (INEI) | Tipo | % Nulos (Muestra) | Clasificación / Rol | Justificación Metodológica |
|:---|:---|:---|---:|:---|:---|
| `ID1` | Año | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `HHID` | Identificación Cuestionario del Hogar | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `HVIDX` | Número de orden | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `HV101` | Relación de parentesco con el jefe del hogar | `int64` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV102` | ¿Vive habitualmente aquí? | `int64` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV103` | ¿Durmió aquí anoche? | `int64` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV104` | Sexo | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV105` | Edad | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV106` | ¿Cuál fue el nivel de estudios más alto que aprobó? | `int64` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV107` | ¿Cuál fue el año o grado más alto que aprobó? | `str` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV108` | Número de años de estudio | `int64` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV109` | Nivel educativo alcanzado | `int64` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV110` | Actualmente ¿Asiste a una escuela o colegio (un instituto superior o universidad)? | `int64` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV111` | ¿Está viva la madre natural? | `str` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV112` | Número de orden de la madre | `str` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV113` | ¿Está vivo el padre natural? | `str` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV114` | Número de orden del padre | `str` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV115` | ¿Cúal es su estado civil o conyugal? | `str` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV116` | Acutalmente, anteriormente o nunca unida | `str` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV117` | Elegibilidad para entrevista individual de mujeres | `int64` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV118` | Elegibilidad para entrevista de hombres | `str` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV120` | Menores de 5 años para medición de peso/talla y hemoglobina | `int64` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV121` | ¿Asistió a una escuela o colegio? en algún momento durante el año actual | `int64` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV122` | ¿A qué nivel asiste o se matriculó? | `int64` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV123` | Año o grado que asiste o se matriculó | `str` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV124` | Número de años de estudio al que asiste o se matriculó durante el año actual | `int64` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV125` | El año pasado ¿estuvo o matriculado en una escuela o colegio (un instituto superior o universidad) | `int64` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV126` | ¿A que nivel asistió o se matriculó el año pasado? | `int64` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV127` | Año o grado que asistió o se matriculó | `str` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV128` | Número de años de estudio al que asiste o se matriculó el año pasado | `int64` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `HV129` | Condición de asistencia a una escuela, colegio, instituto superior o universidad | `str` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `QH21A` | ¿Estudia en una escuela o colegio estatal? | `str` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `QH25A` | ¿Cuál es su nacionalidad? | `str` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `QH25B` | Vive permanentemente en el Perú | `str` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `QH25CM` | Desde qué mes vive en el Perú | `str` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |
| `QH25CA` | Desde qué año vive en el Perú | `str` | 0.0% | **DESCARTAR: NO REQUERIDA** | Variables detalladas de miembros individuales; las características del hogar se toman de RECH0. |

### 📁 Archivo: `RECHM_2025.csv` — Módulo 1629: Migración y Residencia Habitual (RECHM)
**Total de columnas:** 8 | **Total de filas en origen:** 2,714  

| Variable | Descripción Oficial (INEI) | Tipo | % Nulos (Muestra) | Clasificación / Rol | Justificación Metodológica |
|:---|:---|:---|---:|:---|:---|
| `ID1` | Año | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `HHID` | Identificación del caso | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `NRO_ORDEN_ID` | Número de orden | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `QH30M` | Sexo | `int64` | 0.0% | **DESCARTAR: MÓDULO AUXILIAR** | Migración familiar; cobertura restringida (~95% nulos respecto al universo de niños). |
| `QH31M` | A qué edad murió | `int64` | 0.0% | **DESCARTAR: MÓDULO AUXILIAR** | Migración familiar; cobertura restringida (~95% nulos respecto al universo de niños). |
| `QH32M_M` | En qué mes murió | `int64` | 0.0% | **DESCARTAR: MÓDULO AUXILIAR** | Migración familiar; cobertura restringida (~95% nulos respecto al universo de niños). |
| `QH32M_Y` | En qué año murió | `int64` | 0.0% | **DESCARTAR: MÓDULO AUXILIAR** | Migración familiar; cobertura restringida (~95% nulos respecto al universo de niños). |
| `QH33M` | Murió por alguna causa relacionada con el embarazo, parto, sobreparto o por alguna otra causa | `str` | 0.0% | **DESCARTAR: MÓDULO AUXILIAR** | Migración familiar; cobertura restringida (~95% nulos respecto al universo de niños). |

### 📁 Archivo: `RECH23_2025.csv` — Módulo 1630: Características de la Vivienda y Servicios Básicos (RECH23)
**Total de columnas:** 130 | **Total de filas en origen:** 37,331  

| Variable | Descripción Oficial (INEI) | Tipo | % Nulos (Muestra) | Clasificación / Rol | Justificación Metodológica |
|:---|:---|:---|---:|:---|:---|
| `ID1` | Año | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `HHID` | Identificacion Cuestionario del Hogar | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `HV201` | ¿Cuál es la fuente principal de abastecimiento de agua para tomar o beber? | `str` | 0.0% | **PREDICTOR RECOMENDADO** | Fuente principal de agua para beber. Riesgo de infecciones diarreicas agudas y malabsorción. |
| `HV202` | ¿Cuál es la fuente principal de abastecimiento de agua en su hogar? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV204` | ¿Cuánto tiempo se demora en ir, recoger agua y volver? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV205` | ¿Qué tipo de servicio higiénico tiene su hogar? | `str` | 0.0% | **PREDICTOR RECOMENDADO** | Tipo de servicio higiénico / baño. Condición sanitaria y exposición a enteroparásitos. |
| `HV206` | ¿Tiene electricidad en su hogar? | `str` | 0.0% | **PREDICTOR RECOMENDADO** | Disponibilidad de electricidad en la vivienda. Proxy de infraestructura básica y refrigeración. |
| `HV207` | Su hogar ¿tiene radio? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV208` | Su hogar ¿tiene televisor? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV209` | Su hogar ¿tiene refrigeradora /congeladora? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV210` | Algún miembro de su hogar ¿tiene bicleta/triciclo? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV211` | Algún miembro de su hogar ¿tiene motocileta/ motokar? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV212` | Algún miembro de su hogar ¿tiene carro o camión? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV213` | Material predominante del piso de la vivienda | `str` | 0.0% | **PREDICTOR RECOMENDADO** | Material predominante del piso (tierra vs material noble; reservorio de uncinarias y parásitos). |
| `HV214` | Material predominante de las paredes exteriores de la vivienda | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV215` | Material predominante del techo de la vivienda | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV216` | Número de habitaciones utilizadas para dormir | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV217` | Estructura de relaciones en el hogar (composición de los hogares) | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV218` | Número de orden del Jefe del hogar | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV219` | Sexo del jefe de hogar | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV220` | Edad del jefe de hogar | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV221` | Su hogar ¿tiene teléfono? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV225` | ¿El servicio higiénico es compartido con otros hogares? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV226` | ¿Cuál es el combustible que utilizan más frecuentemente en su hogar para cocinar? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV227` | Tiene un mosquitero para dormir | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV228` | Los niños menores de 5 años durmieron bajo mosquiteros anoche | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV234` | Prueba de yodo para sal | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV235` | Ubicación de la fuente de agua | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV236` | Persona que a recoger agua para su hogar | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV237` | Hecho algo al agua para hacerla segura para beber | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV237A` | El agua usualmente es tratada por: hervida | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV237B` | El agua usualmente es tratada por: añadir lejía o cloro | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV237C` | El agua usualmente es tratada por: filtro a través de un paño | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV237D` | El agua usualmente es tratada por: uso de agua filtrada | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV237E` | El agua usualmente es tratada por: desinfección solar | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV237F` | El agua usualmente es tratada por: dejar reposar y asentarse | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV237G` | El agua usualmente es tratada por: CS - agua embotellada | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV237H` | El agua usualmente es tratada por: CS | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV237I` | El agua usualmente es tratada por: CS | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV237J` | El agua usualmente es tratada por: CS | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV237K` | El agua usualmente es tratada por: CS | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV237X` | El agua usualmente es tratada por: otros | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV237Z` | El agua usualmente es tratada por: no sabe | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV238` | Número de hogares que comparten el baño | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV239` | Comida cocinada en estufa o fuego abierto | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV240` | El hogar tiene una chimenea o una campana | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV241` | Comida preparada en la casa, en edificio separado o al aire libre | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV242` | ¿Utilizan un cuarto especialmente para cocinar? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV243A` | ¿Tiene un teléfono móvil (celular)? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV243B` | Tiene un reloj | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV243C` | ¿Tiene un carreta jalada por animales? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV243D` | ¿Tiene un bote a motor? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV244` | ¿Algún miembro del hogar es dueño de tierras agrícolas? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV245` | ¿Cuántas hectáreas de tierras agrícolas le pertenecen? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV246` | ¿Algún miembro del hogar es dueño de ganadería, rebaños o animales de granja? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV246A` | Cantidad de: ganado | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV246B` | Cantidad de: vacas, toros | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV246C` | Cantidad de: caballos, burros, mulas | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV246D` | Cantidad de: cabras | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV246E` | Cantidad de: ovejas | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV246F` | Cantidad de: pollos | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV246G` | Cantidad de: aves de corral | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV246H` | Cantidad de: cuyes/conejos | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV246I` | Cantidad de: cerdos | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV246J` | Cantidad de: otros | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV246K` | CS propio | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV247` | Posee una cuenta bancaria | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV248` | Número de personas enfermas 18-59 | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV249` | Miembro de la HH fallecido los últimos 12 meses | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV250` | Número de miembros que murieron en los últimos 12 meses | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV251` | Número de huérfanos y niños vulnerables | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HML1` | Número de mosquiteros | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HML1A` | Número de mosquiteros con información específica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HML2` | Número de niños menores de edad en la noche anterior | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SHVER` | Versión del cuestionario | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SHREGION` | Región natural | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SHSEMES` | Semestre | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SHPROVIN` | Provincia | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SHDISTRI` | Distrito | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SHTOTH` | Total de hogares en la vivienda | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH42` | El abastecimiento de agua para beber está disponible todo el día | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH43` | Las últimas 2 semanas fueron interrumpidas por un día o más | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH48` | ¿Conserva en un envase o recipiente el agua para beber? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH49` | Tipo de envase o recipiente | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH50` | ¿Lo usa con tapa? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH51` | Pago por el agua? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH52` | Institución de pago de agua | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH56` | Con qué frecuencia se limpia el baño o la letrina? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH58` | Dónde tira la basura? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH59` | Con qué frecuencia se recoge la basura? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH60` | Antes de desechar la basura donde se almacena? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH61A` | ¿Tiene sofá? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH61B` | ¿Tiene vitrina/aparador? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH61C` | ¿Tiene repostero? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH61D` | ¿Tiene cómoda/ropero? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH61E` | ¿Tiene reloj de pared? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH61J` | ¿Tiene televisión por cable? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH61K` | ¿Tiene licuadora? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH61L` | ¿Tiene cocina de gas? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH61M` | ¿Tiene cocina de kerosene? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH61N` | ¿Tiene microondas? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH61O` | ¿Tiene lavadora? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH61P` | ¿Tiene computadora? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH61Q` | ¿Tiene acceso a Internet en casa? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH61R` | ¿Tiene bomba de agua? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH61S` | ¿Tiene generador de electricidad? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH63` | ¿Utiliza otro tipo de combustible para cocinar? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH64` | Otro tipo de combustible utilizado para cocinar | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH66` | ¿La cocina tiene una chimenea o un mecanismo para eliminar el humo? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH69` | El hogar compra combustible para cocinar? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH70` | ¿Qué tipo de alumbrado utiliza el hogar? | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH71` | Número de habitaciones en el hogar | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH72` | Número de habitaciones que usa para dormir | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SXH73` | Tiene una red (No 20011) | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH76A` | La vivienda tiene ventanas | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH76B` | Ventanas con cristal | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH76C` | Ventanas de madera | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH76D` | Ventanas con malla | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH76E` | Ventanas con cortinas/persianas | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH77F` | Otro tipo de transporte (caballos, peque-peque, etc.) | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH78` | Algún miembro de su hogar es dueño de tierras agricolas | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH79` | Cuantas hectareas (1 decimal) | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH224` | Prueba de Yodo | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH225U` | Visualización de la bolsa de sal | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH225` | Marca de sal usada por el hogar | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `SH227` | Prueba de cloro | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `QH227A` | La muestra fue tomada por: | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `QH227B` | La nuestra del agua se extrajo del: | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `HV270` | Índice de riqueza | `str` | 0.0% | **PREDICTOR RECOMENDADO** | Índice de riqueza en quintiles (nivel socioeconómico relativo del hogar). |
| `HV271` | Factor de puntuación del índice de riqueza (5 decimales) | `str` | 0.0% | **PREDICTOR SECUNDARIO** | Puntaje continuo de riqueza (puede usarse en lugar del quintil para evitar discretización). |

### 📁 Archivo: `REC41_2025.csv` — Módulo 1633: Embarazo, Parto, Puerperio y Lactancia (REC41)
**Total de columnas:** 147 | **Total de filas en origen:** 18,841  

| Variable | Descripción Oficial (INEI) | Tipo | % Nulos (Muestra) | Clasificación / Rol | Justificación Metodológica |
|:---|:---|:---|---:|:---|:---|
| `ID1` | Año | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `CASEID` | Identificación Cuestionario Individual | `str` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `MIDX` | Orden de historia de nacimiento | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `M1` | Durante el embarazo cuantas dosis contra el tétano le aplicaron | `str` | 0.0% | **PREDICTOR SECUNDARIO** | Lugar de ocurrencia del parto (institucional vs domiciliario). |
| `M1A` | Antes del embarazo cuantas dosis de la vacuna contra el tétano recibió | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M1B` | Mes última inyección contra el tétano antes del embarazo | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M1C` | Año de la última inyección contra el tétano antes del embarazo | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M1D` | Sin descripción en ficha técnica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M1E` | Última inyección contra el tétano antes del embarazo (CMC) | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M2A` | La chequeó en su control prenatal: Médico | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M2B` | La chequeó en su control prenatal: Enfermera | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M2C` | La chequeó en su control prenatal: Obstetra | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M2D` | La chequeó en su control prenatal: Técnico en enfermería | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M2E` | La chequeó en su control prenatal: Promotor de salud | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M2F` | La chequeó en su control prenatal: Asistente de parto entrenado | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M2G` | La chequeó en su control prenatal: Comadrona/partera | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M2H` | La chequeó en su control prenatal: Relativo (no estándar y rara vez se usa) | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M2I` | La chequeó en su control prenatal: CS otra persona | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M2J` | La chequeó en su control prenatal: CS otra persona | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M2K` | La chequeó en su control prenatal: Otro | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M2L` | La chequeó en su control prenatal: CS otro | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M2M` | La chequeó en su control prenatal: CS otro | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M2N` | La chequeó en su control prenatal: Nadie | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M3A` | La atendió en el parto: Médico | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M3B` | La atendió en el parto: Enfermera | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M3C` | La atendió en el parto: Obstetra | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M3D` | La atendió en el parto: Técnico en enfermería | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M3E` | La atendió en el parto: Promotor de salud | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M3F` | La atendió en el parto: Asistente de parto entrenado | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M3G` | La atendió en el parto: Comadrona/partera | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M3H` | La atendió en el parto: Familiar | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M3I` | La atendió en el parto: CS otra persona | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M3J` | La atendió en el parto: CS otra persona | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M3K` | La atendió en el parto: Otro | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M3L` | La atendió en el parto: CS otro | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M3M` | La atendió en el parto: CS otro | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M3N` | La atendió en el parto: Nadie | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M4` | Duración de la lactancia | `int64` | 0.0% | **PREDICTOR RECOMENDADO** | Duración de la lactancia materna (meses). Fuente primaria de biodisponibilidad férrica. |
| `M5` | Meses de amamantamiento | `int64` | 0.0% | **PREDICTOR RECOMENDADO** | Meses de lactancia materna exclusiva. |
| `M6` | Duración de la amenorrea | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M7` | Meses de amenorrea | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M8` | Duración de la abstinencia | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M9` | Meses de abstinencia | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M10` | Momento que quería quedar embarazada | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M11` | Tiempo que hubiera querido esperar | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M13` | Momento del primer control prenatal | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M14` | Visitas prenatales por embarazo | `str` | 0.0% | **PREDICTOR RECOMENDADO** | Número de controles prenatales recibidos por la madre durante la gestación. |
| `M15` | Lugar del parto | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M17` | Parto por cesárea | `int64` | 0.0% | **PREDICTOR SECUNDARIO** | Asistencia profesional calificada durante el parto (médico/obstetra). |
| `M18` | Tamaño del niño al nacer | `int64` | 0.0% | **PREDICTOR RECOMENDADO** | Mes de inicio del control prenatal (atención temprana vs tardía). |
| `M19` | Peso del niño al nacer (kilos - 3 dec.) | `int64` | 0.0% | **PREDICTOR RECOMENDADO** | Peso al nacer en gramos (reportado por la madre / carné). Indicador de reservas congénitas de hierro. |
| `M19A` | Peso del niño al nacer según recuerda | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M27` | Marca para lactancia | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M28` | Marca para amenorrea | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M29` | Marca para abstinencia | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M34` | Cuando empezó a darle el pecho al niño | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M35` | Cuantas veces le dio pecho durante la noche de ayer | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M36` | Cuantas veces le dio pecho durante el día de ayer | `str` | 0.0% | **DESCARTAR: ADMINISTRATIVA** | Variable operativa de la logística de campo de la encuesta; sin relevancia epidemiológica. |
| `M38` | El día de ayer o noche tomó algo en biberón El día de ayer o durante el dìa o la noche cuantas veces le dio comida sólidas o | `str` | 0.0% | **DESCARTAR: ADMINISTRATIVA** | Variable operativa de la logística de campo de la encuesta; sin relevancia epidemiológica. |
| `M39` | N semisólidas | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M42A` | Durante su embarazo Durante su embarazo en alguno de sus controles: La pesaron | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M42B` | Durante su embarazo en alguno de sus controles: Le midieron la barriga | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M42C` | Durante su embarazo en alguno de sus controles: Le tomaron le presión arterial | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M42D` | Durante su embarazo en alguno de sus controles: Le hicieron examen de orina | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M42E` | Durante su embarazo en alguno de sus controles: Le hicieron examen de sangre | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M43` | Le explicaron acerca de las complicaciones que se pueden presentar en el embarazo | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M44` | Le dijeron dónde acudir si se presentan complicaciones del embarazo | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M45` | Durante el embarazo, le administraron tabletas, jarabe o inyecciones de hierro | `str` | 0.0% | **PREDICTOR RECOMENDADO** | Suplementación con hierro a la madre durante el embarazo (1: Sí, 0: No). |
| `M46` | Por cuantos días tomó hierro y/o cuantas inyecciones recibió | `str` | 0.0% | **PREDICTOR RECOMENDADO** | Días de consumo de hierro por la madre durante el embarazo. |
| `M47` | Durante el embarazo, tuvo dificultad para ver objetos o personas siendo de día | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M48` | Durante el embarazo, tuvo dificultad para ver objetos o personas siendo de noche | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M49A` | Durante el embarazo - tomó fansidar para la malaria | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M49B` | Durante el embarazo - tomó cloroquina para la malaria | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M49C` | Durante el embarazo - tomó medicamento para la malaria | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M49D` | Durante el embarazo: tomó un medicamento específico del país para la malaria | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M49E` | Durante el embarazo: tomó un medicamento específico del país para la malaria | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M49F` | Durante el embarazo: tomó un medicamento específico del país para la malaria | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M49G` | Durante el embarazo: tomó un medicamento específico del país para la malaria | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M49X` | Durante el embarazo - tomó otro medicamento para la malaria | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M49Z` | Durante el embarazo: no tomó medicamento para la malaria | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M51A` | Tiempo en que tuvo control después del parto Durante los primeros 3 días despues del parto, le dieron de tomar: leche, diferente a la | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M54` | Razón principal por la que no recibió atención prenatal | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M55A` | N leche materna | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M55B` | Durante los primeros 3 días despues del parto, le dieron de tomar: agua sola | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M55C` | Durante los primeros 3 días despues del parto, le dieron de tomar: dextrosa glucosada | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M55D` | Durante los primeros 3 días despues del parto, le dieron de tomar: agua | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M55E` | Durante los primeros 3 días despues del parto, le dieron de tomar: agua azucarada | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M55F` | Durante los primeros 3 días despues del parto, le dieron de tomar: jugo de fruta | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M55G` | Durante los primeros 3 días despues del parto, le dieron de tomar: fórmula para bebes | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M55H` | Durante los primeros 3 días despues del parto, le dieron de tomar: té/infusiones | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M55I` | Durante los primeros 3 días despues del parto, le dieron de tomar: miel | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M55J` | Durante los primeros 3 días despues del parto, le dieron de tomar: país específico | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M55K` | Durante los primeros 3 días despues del parto, le dieron de tomar: país específico | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M55L` | Durante los primeros 3 días despues del parto, le dieron de tomar: país específico | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M55M` | Durante los primeros 3 días despues del parto, le dieron de tomar: país específico | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M55N` | Durante los primeros 3 días, le dieron de tomar: país específico | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M55X` | Durante los primeros 3 días despues del parto, le dieron de tomar: otro | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M55Z` | Durante los primeros 3 días despues del parto, le dieron de tomar: nada | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57A` | Control prenatal: Presión arterial tomada | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57B` | Control prenatal: Examen de orina | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57C` | Control prenatal: Muestra de sangre (tamizaje anemia/glucosa) | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57D` | Control prenatal: Prueba de VIH | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57E` | Control prenatal: Prueba rápida de Sífilis (VDRL) | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57F` | Control prenatal: Ecografía obstétrica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57G` | Control prenatal: Examen odontológico | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57H` | Control prenatal: Medición de peso y ganancia ponderal | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57I` | Control prenatal: Medición de altura uterina | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57J` | Control prenatal: Consejería en nutrición y alimentación | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57K` | Control prenatal: Consejería en lactancia materna | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57L` | Control prenatal: Consejería en planificación familiar | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57M` | Control prenatal: Atención psicológica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57N` | Control prenatal: No le realizaron exámenes ni consejerías | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57O` | Sin descripción en ficha técnica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57P` | Sin descripción en ficha técnica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57Q` | Sin descripción en ficha técnica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57R` | Sin descripción en ficha técnica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57S` | Sin descripción en ficha técnica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57T` | Sin descripción en ficha técnica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57U` | Sin descripción en ficha técnica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57V` | Sin descripción en ficha técnica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M57X` | Sin descripción en ficha técnica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M60` | Durante el embarazo tomó medicamentos contra parásitos intestinales | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M61` | N Tiempo que permaneció en el lugar del parto | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M62` | Alguien verificó su salud antes del alta | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M63` | N Cuánto tiempo antes del parto se realizó un control de salud | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M64` | N Quién verificó la salud de los encuestados antes del alta | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M65A` | Atención del parto: Médico | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M65B` | Atención del parto: Obstetra | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M65C` | Atención del parto: Enfermera | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M65D` | Atención del parto: Auxiliar | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M65E` | Atención del parto: Partera | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M65F` | Atención del parto: Otro familiar | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M65G` | Atención del parto: Sola / Nadie | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M65H` | Sin descripción en ficha técnica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M65I` | Sin descripción en ficha técnica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M65J` | Sin descripción en ficha técnica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M65K` | Sin descripción en ficha técnica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M65L` | Sin descripción en ficha técnica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M65X` | Sin descripción en ficha técnica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M66` | Después del parto tuvo algún chequeo o revisiòn médica | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M67` | Cuánto tiempo después del parto se realizó su primer chequeo o revisiòn médica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M68` | Quién le realizó su chequeo o revisión médica después del parto | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M69` | N Donde se chequeo Ud. | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M70` | Durante el primer mes le hicieron al bebe algún control o revisión médica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M71` | N Cuánto tiempo después del parto se realizó el control postnatal | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M72` | Quién realizó el control posnatal | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `M73` | Dónde le hicieron el chequeo o revisión médica al bebé por primera vez | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |

### 📁 Archivo: `REC94_2025.csv` — Módulo 1633: Suplementación con Micronutrientes y Descarte (REC94)
**Total de columnas:** 61 | **Total de filas en origen:** 18,841  

| Variable | Descripción Oficial (INEI) | Tipo | % Nulos (Muestra) | Clasificación / Rol | Justificación Metodológica |
|:---|:---|:---|---:|:---|:---|
| `ID1` | Año | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `CASEID` | Identificación Cuestionario Individual | `str` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `IDX94` | Orden de historia de nacimiento | `int64` | 0.0% | **LLAVE / ID** | Identificador relacional para cruce entre módulos o control de duplicados. |
| `S410B` | Cuantos meses de embarazo tenía en la última revisión prenatal | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S411B` | En alguno de sus controles: Le midieron la barriga | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S411F` | En alguno de sus controles: Escucharon los latidos del corazón del bebé | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S411G` | En alguno de sus controles: Le hicieron la prueba para descartar Sífilis | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S411H` | En alguno de sus controles: Le hicieron la prueba para descartar de VIH/SIDA | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S411I` | En alguno de sus controles: Le informaron como alimentarse | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S411J` | En alguno de sus controles: Le informaron sobre sus derechos En alguno de sus controles: Le enseñaron como preparar pezones para lactancia | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S411K` | N materna | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S411L` | En alguno de sus controles: Le enseñaron como darle el pecho a su bebe | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S411BA` | Cuantos meses de embarazo tenía cuando se realizó la primera prueba de orina | `str` | 0.0% | **DUDOSA: INTERVENCIÓN** | Suplementación o tratamiento recibido por el niño. Alto riesgo de causalidad inversa (recibió jarabe porque ya tenía anemia). |
| `S411CA` | Cuantos meses de embarazo tenía cuando se realizó el primer análisis de sangre | `str` | 0.0% | **DUDOSA: INTERVENCIÓN** | Suplementación o tratamiento recibido por el niño. Alto riesgo de causalidad inversa (recibió jarabe porque ya tenía anemia). |
| `S411DA` | Cuantos meses de embarazo tenía cuando se realizó la primera prueba de Sífilis | `str` | 0.0% | **DUDOSA: INTERVENCIÓN** | Suplementación o tratamiento recibido por el niño. Alto riesgo de causalidad inversa (recibió jarabe porque ya tenía anemia). |
| `S411EA` | Cuantos meses de embarazo tenía cuando se realizó la primera prueba de VIH/SIDA | `str` | 0.0% | **DUDOSA: INTERVENCIÓN** | Suplementación o tratamiento recibido por el niño. Alto riesgo de causalidad inversa (recibió jarabe porque ya tenía anemia). |
| `S413` | Durante el embarazo estaba afiliada al SIS | `str` | 0.0% | **DUDOSA: INTERVENCIÓN** | Suplementación o tratamiento recibido por el niño. Alto riesgo de causalidad inversa (recibió jarabe porque ya tenía anemia). |
| `S422I` | Cantidad de inyecciones de hierro recibidas durante el embarazo Razón por qué no acudió a un hospital, centro o puesto de salud del MINSA para dar a | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S426B` | N luz | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S426E` | La cesárea fue programada | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S426FA` | Cuánto tiempo transcurrió hasta llegar al establecimiento para dar a luz Cuanto tiempo transcurrió desde que llegó al establecimeinto hasta que fué examinada | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S426FB` | N por personal de salud. | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S426GA` | Complicaciones de parto: Parto prolongado | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S426GB` | Complicaciones de parto: Sangrado excesivo | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S426GC` | Complicaciones de parto: Fiebre con sangrado vaginal | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S426GD` | Complicaciones de parto: Convulsiones | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S426GE` | Complicaciones de parto: Otras | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S430C` | El niño fue inscrito en la municipalidad/Oficina Registral de la RENIEC | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S430D` | La partida/acta tiene Código Único de Identidad (CUI) | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S431A` | En el establecimiento de salud le dieron algo en biberón al bebe después del nacimiento | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S425A` | Entrevistada era miembro del seguro de salud materna | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S432` | El niño está afiliado al Seguro Integral de Salud | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S432AD` | Day affiliation integral health insurance | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S432AM` | Mes afiliación seguro de salud integral | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S432AY` | Año de afiliación seguro de salud integral | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S427DA` | Complicaciones después del parto: sangrado intenso | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S427DB` | Complicaciones después del parto: pérdida de conciencia | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S427DC` | Complicaciones después del parto: fiebre alta, escalofríos | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S427DD` | Complicaciones después del parto: infección de los senos | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S427DE` | Complicaciones después del parto: dolor al orinar | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S427DF` | Complicaciones después del parto: flujos vaginales | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S427DG` | Complicaciones después del parto: Pérdida involuntaria de orina | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S427F` | Cuando tuvo esas complicaciones recibió atención médica | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S435` | Por qué no le dio pecho al bebé | `str` | 0.0% | **DUDOSA: INTERVENCIÓN** | Suplementación o tratamiento recibido por el niño. Alto riesgo de causalidad inversa (recibió jarabe porque ya tenía anemia). |
| `S436C` | Pusieron al niño en contacto piel a piel con Ud. inmediatamente después del nacimiento | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S440` | Por qué dejo de darle pecho | `str` | 0.0% | **DUDOSA: INTERVENCIÓN** | Suplementación o tratamiento recibido por el niño. Alto riesgo de causalidad inversa (recibió jarabe porque ya tenía anemia). |
| `S441` | Recibió alguna capacitación sobre lactancia materna durante el embarazo | `int64` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S442` | En qué lugar recibió capacitación sobre lactancia materna | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S446AA` | Con cuanto tiempo de anticipación preparó el biberón | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S446AB` | Donde guardó el biberón | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S446A` | Se agregó azúcar a cualquiera de los alimentos del bebé | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S447` | Se agrego azúcar a algun alimento o liquido que comiò o tomò el dìa de ayer | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S448A` | Tiempo entre que terminó de preparar los alimentos del bebé y los sirvió | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `S448B` | Dónde se almacenó la comida | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `QI411_M` | En alguno de sus controles: le hicieron la prueba para descartar Hepatitis B | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `QI411F` | Cuántos meses de embarazo tenía en primera prueba para descartar Hepatitis B | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `QI440B` | Durante primeros 6 meses, solo recibió leche materna Durante el embarazo algún personal de salud le realizó una prueba o análisis para | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `QI422A_A` | N descartar anemia | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `QI422A_B` | Durante el embarazo le diagnosticaron o le dijeron que tenía anemia | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `QI422A_C` | Durante el embarazo le indicaron tratamiento con hierro Durante el embarazo consumió hierro tal como le indicó el personal de salud | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |
| `QI422A_D` | N | `str` | 0.0% | **DESCARTAR: ALTA INCOMPLETITUD / NO APLICA** | Pregunta con filtro condicional muy restrictivo, alta tasa de nulos o fuera del alcance del modelo. |

---
## 4. Síntesis y Matriz de Decisión para el Modelo XGBoost

### 4.1 Variables Seleccionadas para la Matriz Explicativa ($X$)
Estas variables son 100% compatibles con la entrevista comunitaria preventiva (no requieren exámenes clínicos ni balanza/tallímetro):

| Variable Limpia | Variable Origen | Módulo | Categoría | Tipo en ML | Justificación Epidemiológica y de Negocio |
|:---|:---|:---|:---|:---|:---|
| `edad_meses` | `HC1` | RECH6 | Niño | Continua / Discreta | Factor biológico de agotamiento de depósitos fetales y transición a dieta complementaria. |
| `sexo_nino` | `HC27` | RECH6 | Niño | Binaria (0/1) | Variabilidad metabólica y ritmo de ganancia de masa corporal. |
| `departamento` | `HV024` | RECH0 | Geografía | Categórica Nominal | Brechas estructurales y epidemiológicas interdepartamentales. |
| `area_residencia` | `HV025` | RECH0 | Geografía | Binaria (Urbano/Rural) | Acceso diferencial a agua potable, saneamiento y centros asistenciales. |
| `altitud_msnm` | `HV040` | RECH0 | Geografía | Continua | Factor fisiológico de hipoxia ambiental que demanda mayor eritropoyesis. |
| `total_miembros` | `HV009` | RECH0 | Hogar | Discreta | Densidad de convivencia y asignación presupuestaria familiar. |
| `menores_5anos` | `HV014` | RECH0 | Hogar | Discreta | Competencia de cuidados intrahogar y demanda de atención materna. |
| `tiene_sis` | `SH11A` | RECH4 | Salud | Binaria (0/1) | Cobertura de subsidio estatal para control de crecimiento y tamizaje. |
| `fuente_agua` | `HV201` | RECH23 | Vivienda | Categórica Nominal | Riesgo microbiológico de diarrea aguda y síndrome de malabsorción. |
| `tipo_bano` | `HV205` | RECH23 | Vivienda | Categórica Nominal | Nivel de saneamiento básico e higiene del entorno. |
| `tiene_electricidad` | `HV206` | RECH23 | Vivienda | Binaria (0/1) | Capacidad de refrigeración y conservación adecuada de alimentos cárnicos. |
| `material_piso` | `HV213` | RECH23 | Vivienda | Categórica Nominal | Suelo de tierra asociado a transmisión de geohelmintos (uncinariasis/anemia). |
| `quintil_riqueza` | `HV270` | RECH23 | Socioeconómica | Ordinal (1 a 5) | Poder adquisitivo y seguridad alimentaria del hogar. |
| `controles_prenatales` | `M14` | REC41 | Gestación | Discreta | Oportunidad de detección temprana de complicaciones maternas. |
| `mes_inicio_prenatal` | `M18` | REC41 | Gestación | Continua / Discreta | Adherencia oportuna al paquete de atención integral gestacional. |
| `peso_al_nacer_g` | `M19` | REC41 | Nacimiento | Continua | Peso al nacer reportado por la madre; reserva congénita de hierro del neonato. |
| `duracion_lactancia` | `M4` | REC41 | Lactancia | Continua / Discreta | Meses acumulados de amamantamiento. |
| `lactancia_exclusiva`| `M5` | REC41 | Lactancia | Continua / Discreta | Práctica de lactancia exclusiva hasta los 6 meses de vida. |
| `hierro_madre_gest` | `M45` | REC41 | Gestación | Binaria (0/1) | Transferencia placentaria de hierro durante el último trimestre. |
| `dias_hierro_madre` | `M46` | REC41 | Gestación | Continua / Discreta | Dosis acumulada de suplemento consumida por la madre durante el embarazo. |

### 4.2 Variables Dudosas: Justificación y Decisión Requerida
Existen dos conjuntos de variables que tu compañero utilizó en `v1`, pero que presentan riesgos metodológicos formales:

#### Grupo A: Mediciones Antropométricas Clínicas (`HC70`, `HC71`, `HC72`)
- **Variables:** Z-score Talla/Edad (Desnutrición crónica), Z-score Peso/Edad (Desnutrición global), Z-score Peso/Talla (Desnutrición aguda).
- **Argumento a Favor:** Están fuertemente asociadas a la nutrición infantil y aportan poder discriminante al modelo.
- **Argumento en Contra:** **Rompen la regla de evaluación no invasiva por entrevista.** Para calcular un Z-score se necesita pesar y tallar al niño con balanza y tallímetro calibrados por personal técnico; un promotor comunitario no cuenta con estos datos en una primera visita domiciliaria de tamizaje.

#### Grupo B: Suplementación y Tratamiento Pediátrico en `REC94` (`S411BA`, `S411CA`, `S440`)
- **Variables:** Consumo de gotas de hierro, jarabe de hierro y haber recibido tratamiento médico para la anemia.
- **Argumento en Contra (Causalidad Inversa Crítica):** La variable `S440` (*¿Recibió tratamiento para la anemia?*) se le receta al niño **porque ya le diagnosticaron anemia**. Usarla para predecir si el niño tiene anemia genera un sesgo circular: el algoritmo no aprende vulnerabilidad biológica, sino si el niño ya visitó el centro de salud y fue medicado.

### 4.3 Variables Excluidas Estrictamente por Fuga de Datos (Leakage)
- `HC53` / `HW53`: Nivel de hemoglobina bruta (g/dL).
- `HC56` / `HW56`: Hemoglobina ajustada por altitud según norma RM 363-2022.
- `HC56A` / `HW56A`: Hemoglobina ajustada por altitud según norma OMS 2024 / RM 251-2024.
- `HC57` / `HW57`: Diagnóstico de anemia según norma RM 363-2022 (norma desactualizada).
- `HC55` / `HW55`: Resultado del procedimiento de punción capilar.

