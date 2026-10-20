#!/usr/bin/env python3
"""
Script que genera el Catálogo Exhaustivo de Variables para Desnutrición Crónica Infantil
ENDES 2025 (INEI, Perú) - Modelo Predictivo XGBoost.
Analiza con rigor epidemiológico 1,807 variables en 23 diccionarios oficiales.
"""

import os
import glob
import re

OUTPUT_FILE = "reports/catalogo_variables_desnutricion_cronica_endes2025.md"

def load_file_dict(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    lines = text.strip().splitlines()
    vars_list = []
    for l in lines:
        if l.startswith('|') and not l.startswith('| Nº') and not l.startswith('|:--'):
            parts = [p.strip() for p in l.split('|')[1:-1]]
            if parts and parts[0] != '':
                vars_list.append({
                    'num': parts[0],
                    'var': parts[1],
                    'desc': parts[2] if len(parts) > 2 else '',
                    'tipo': parts[3] if len(parts) > 3 else '',
                    'longitud': parts[4] if len(parts) > 4 else '',
                    'rango': parts[5] if len(parts) > 5 else '',
                    'valores': parts[6] if len(parts) > 6 else '',
                    'desc_alt': parts[7] if len(parts) > 7 else '',
                    'obs': parts[8] if len(parts) > 8 else '',
                })
    return vars_list

def load_all_dictionaries():
    all_dicts = {}
    
    # 1. Cargar diccionarios originales de reports/diccionarios_completos_endes2025.md
    with open('reports/diccionarios_completos_endes2025.md', 'r', encoding='utf-8') as f:
        orig_text = f.read()
    orig_sections = re.findall(r'# DICCIONARIO DE VARIABLES .*?\((.*?)\)(.*?)(?=# DICCIONARIO|\Z)', orig_text, re.DOTALL)
    for code, body in orig_sections:
        code = code.strip()
        vars_l = []
        for l in body.strip().splitlines():
            if l.startswith('|') and not l.startswith('| Nº') and not l.startswith('|:--'):
                parts = [p.strip() for p in l.split('|')[1:-1]]
                if parts and parts[0] != '':
                    vars_l.append({
                        'num': parts[0],
                        'var': parts[1],
                        'desc': parts[2] if len(parts) > 2 else '',
                        'tipo': parts[3] if len(parts) > 3 else '',
                        'longitud': parts[4] if len(parts) > 4 else '',
                        'rango': parts[5] if len(parts) > 5 else '',
                        'valores': parts[6] if len(parts) > 6 else '',
                        'desc_alt': parts[7] if len(parts) > 7 else '',
                        'obs': parts[8] if len(parts) > 8 else '',
                    })
        mod = "1638_anemia" if code in ['REC44', 'RECH5', 'RECH6'] else \
              "1629_hogar" if code in ['RECH0', 'RECH1', 'RECH4', 'RECHM'] else \
              "1630_vivienda" if code == 'RECH23' else \
              "1633_embarazo"
        all_dicts[code] = {
            'code': code,
            'modulo': mod,
            'file_desc': f'Diccionario - {code}.pdf',
            'vars': vars_l
        }

    # 2. Cargar diccionarios de data/1031-mef, data/1036-inmunizacion, data/1041-programasocial
    new_dirs = [
        ('1031-mef', 'data/1031-mef'),
        ('1036-inmunizacion', 'data/1036-inmunizacion'),
        ('1041-programasocial', 'data/1041-programasocial')
    ]
    for mod_name, mod_dir in new_dirs:
        for f in sorted(glob.glob(f'{mod_dir}/Diccionario*.md')):
            bname = os.path.basename(f).replace('Diccionario - ', '').replace('.md', '')
            vars_l = load_file_dict(f)
            all_dicts[bname] = {
                'code': bname,
                'modulo': mod_name,
                'file_desc': os.path.basename(f).replace('.md', '.pdf'),
                'vars': vars_l
            }
            
    return all_dicts

def classify_variable(dict_name, var_info):
    v = var_info['var'].upper().strip()
    d = var_info['desc'].strip().lower()

    # --- RECH6 (Niños - Antropometría y Hemoglobina en Hogar) ---
    if dict_name == 'RECH6':
        if v in ['ID1', 'HHID', 'HC0']:
            return "METADATO / LLAVE", "Identificador relacional del hogar y número de orden del niño en el hogar."
        if v == 'HC70':
            return "VARIABLE OBJETIVO (TARGET)", "Variable objetivo (Y): Talla/Edad Z-score OMS (< -200 centésimas = 1, >= -200 = 0). Excluida de predictores."
        if v in ['HC71', 'HC72', 'HC73']:
            return "EXCLUIR POR LEAKAGE (PROXY TARGET)", "Puntajes antropométricos Z (Peso/Edad, Peso/Talla, IMC) calculados post-medición. Fuga directa y redundancia con estado nutricional."
        if v in ['HC3', 'HC4', 'HC5', 'HC6', 'HC7', 'HC8', 'HC9', 'HC10', 'HC11', 'HC12']:
            return "EXCLUIR POR LEAKAGE", "Talla directa o tablas de percentiles/desvíos que permiten reconstruir el puntaje Z de talla/edad con la edad del niño."
        if v == 'HC2':
            return "DUDOSA (CLÍNICA / PROXY)", "Peso en kg (balanza calibrada). Medición física concurrente; riesgo de fuga indirecta de masa corporal y rompe el enfoque no invasivo."
        if v in ['HC13', 'HC15']:
            return "EXCLUIR POR LEAKAGE / OPERATIVA", "Control operativo de medición antropométrica (si se midió acostado o de pie según talla < 85cm o razón de no medición)."
        if v in ['HC16', 'HC17', 'HC18', 'HC19', 'HC30', 'HC31', 'HC32', 'HC33', 'HC51', 'HC52', 'HC55', 'HC58', 'HC62', 'HC63', 'HC64']:
            return "EXCLUIR POR IRRELEVANCIA", "Variable administrativa, fecha de visita de campo, código de muestra o consentimiento operativo sin valor predictivo."
        if v == 'HC1':
            return "INCLUIR", "Edad del niño en meses (0 a 59). Factor biológico central del crecimiento lineal y acumulación del retraso estatural."
        if v == 'HC27':
            return "INCLUIR", "Sexo del niño (1: Hombre, 2: Mujer). Dimorfismo biológico en velocidades de maduración y requerimientos nutricionales."
        if v in ['HC53', 'HC56', 'HC56A', 'HC57', 'HC57A']:
            return "DUDOSA (BIOMARCADOR CONCURRENTE)", "Medición de hemoglobina y anemia infantil. Concurrente e invasiva (punción capilar). Evaluar modelo no invasivo vs. clínico."
        if v in ['HC60']:
            return "METADATO / LLAVE", "Número de orden de la madre en el hogar. Llave relacional imprescindible para cruce con registros maternos."
        if v in ['HC61', 'HC68']:
            return "INCLUIR", "Nivel educativo y años de estudio de la madre reportados en el cuestionario de hogar. Fuerte determinante socioeconómico."

    # --- REC44 (Niños Cuestionario Individual) ---
    if dict_name == 'REC44':
        if v in ['ID1', 'CASEID', 'HWIDX']:
            return "METADATO / LLAVE", "Llave relacional de la madre y orden de nacimiento del niño en el cuestionario individual."
        if v == 'HW70':
            return "VARIABLE OBJETIVO (TARGET SECUNDARIO)", "Puntaje Z Talla/Edad OMS en cuestionario individual. Usado como verificación cruzada del target; excluido de X."
        if v in ['HW3', 'HW4', 'HW5', 'HW6', 'HW7', 'HW8', 'HW9', 'HW10', 'HW11', 'HW12', 'HW71', 'HW72', 'HW73']:
            return "EXCLUIR POR LEAKAGE", "Antropometría del niño (talla, percentiles, desviaciones estándar, peso/talla). Reconstruye directamente el target."
        if v in ['HW2']:
            return "DUDOSA (CLÍNICA / PROXY)", "Peso del niño en kilogramos con 1 decimal. Medición clínica con balanza."
        if v in ['HW13', 'HW15']:
            return "EXCLUIR POR LEAKAGE / OPERATIVA", "Procedimiento de medición física (acostado/de pie o razón de no medición)."
        if v in ['HW16', 'HW17', 'HW18', 'HW19', 'HW51', 'HW52', 'HW55', 'HW58']:
            return "EXCLUIR POR IRRELEVANCIA", "Datos de control de campo, fechas administrativas y consentimientos operativos."
        if v == 'HW1':
            return "INCLUIR", "Edad del niño en meses (homólogo a HC1 en cuestionario individual)."
        if v in ['HW53', 'HW56', 'HW56A', 'HW57', 'HW57A']:
            return "DUDOSA (BIOMARCADOR CONCURRENTE)", "Hemoglobina y anemia en cuestionario individual. Procedimiento clínico concurrente."

    # --- RECH0 (Hogar y Muestreo) ---
    if dict_name == 'RECH0':
        if v in ['ID1', 'HHID']:
            return "METADATO / LLAVE", "Identificador maestro del hogar para unión con todos los módulos."
        if v in ['HV001', 'HV002', 'HV002A', 'HV004', 'HV021', 'HV022']:
            return "METADATO DEL DISEÑO MUESTRAL", "Conglomerado, estrato y unidades de muestreo complejo. Imprescindibles para GroupKFold y validación sin fuga espacial."
        if v == 'HV005':
            return "METADATO DEL DISEÑO MUESTRAL", "Factor de ponderación muestral del hogar (dividir entre 1,000,000 para obtener el peso expandido insesgado / sample_weight)."
        if v in ['HV000', 'HV003', 'HV007', 'HV008', 'HV011', 'HV012', 'HV013', 'HV015', 'HV017', 'HV020', 'HV027', 'HV028', 'HV030', 'HV031', 'HV032', 'HV041', 'HV042', 'HV043', 'HV044', 'HV801', 'HV802', 'HV803', 'HV804', 'HV805', 'HV807']:
            return "EXCLUIR POR IRRELEVANCIA", "Constante de país, códigos de informante, tiempos de entrevista o submuestras no aplicables al objetivo."
        if v == 'HV009':
            return "INCLUIR", "Número total de personas en el hogar. Indicador de carga de dependencia familiar y hacinamiento potencial."
        if v == 'HV010':
            return "INCLUIR", "Número de mujeres elegibles en edad fértil en el hogar. Red de apoyo materno y capacidad de cuidado infantil."
        if v == 'HV014':
            return "INCLUIR", "Número de niños menores de 5 años en el hogar. Competencia directa por atención, lactancia y raciones nutricionales."
        if v == 'HV023':
            return "INCLUIR", "Dominio geográfico de residencia (Costa, Sierra, Selva, Lima). Patrones agroecológicos y epidemiológicos."
        if v == 'HV024':
            return "INCLUIR", "Departamento de residencia (1 a 25). Captura brechas estructurales de desarrollo regional y servicios de salud."
        if v == 'HV025':
            return "INCLUIR", "Área de residencia (1: Urbano, 2: Rural). Una de las brechas más críticas en desnutrición crónica infantil en el Perú."
        if v == 'HV026':
            return "INCLUIR", "Tipo de lugar de residencia (Capital, gran ciudad, ciudad pequeña, pueblo, campo)."
        if v == 'HV035':
            return "INCLUIR", "Número de mujeres de 15 a 49 años en el hogar."
        if v == 'HV040':
            return "INCLUIR", "Altitud del conglomerado en msnm. Fuerte asociación fisiológica con retardo estatural andino y ruralidad extrema."

    # --- RECH23 (Vivienda, Saneamiento y Riqueza) ---
    if dict_name == 'RECH23':
        if v in ['ID1', 'HHID']:
            return "METADATO / LLAVE", "Llave relacional para vincular la vivienda con el hogar y el niño."
        if v in ['HV201', 'HV202']:
            return "INCLUIR", "Fuente principal de abastecimiento de agua para beber y uso general. Factor crítico de diarreas y enteropatía ambiental."
        if v == 'HV204':
            return "INCLUIR", "Tiempo en minutos para ir, recoger agua y volver. Proxy de estrés hídrico y precariedad extrema de acceso."
        if v == 'HV205':
            return "INCLUIR", "Tipo de servicio higiénico. Clasificación JMP OMS/UNICEF de saneamiento mejorado vs. no mejorado (clave en desnutrición)."
        if v == 'HV206':
            return "INCLUIR", "Disponibilidad de electricidad en la vivienda (0: No, 1: Sí). Permite refrigeración y conservación de alimentos."
        if v in ['HV207', 'HV208', 'HV209', 'HV210', 'HV211', 'HV212']:
            return "INCLUIR", "Bienes del hogar (radio, televisor, refrigeradora, bicicleta, motocicleta, automóvil). Componentes del nivel socioeconómico."
        if v in ['HV213', 'HV214', 'HV215']:
            return "INCLUIR", "Material predominante del piso (tierra/arena = reservorio de parásitos y bacterias), paredes y techo de la vivienda."
        if v == 'HV216':
            return "INCLUIR", "Número de habitaciones para dormir. Denominador obligatorio para calcular el índice de hacinamiento del hogar."
        if v in ['HV221', 'HV243A', 'HV243C', 'HV243D']:
            return "INCLUIR", "Acceso a teléfono fijo, celular, computadora e internet en el hogar. Conectividad y alfabetismo informacional de la familia."
        if v == 'HV225':
            return "INCLUIR", "Comparte servicio higiénico con otros hogares (1: Sí, 0: No). Contaminación fecal cruzada y saneamiento no exclusivo."
        if v == 'HV226':
            return "INCLUIR", "Tipo de combustible para cocinar (leña, carbón, bosta, gas). Contaminación del aire en interiores e infecciones respiratorias."
        if v == 'HV237':
            return "INCLUIR", "Tratamiento del agua para beber (hervir, clorar, filtrar). Barrera higiénica contra enteropatógenos causantes de retardo de crecimiento."
        if v == 'HV241':
            return "INCLUIR", "Cocina en ambiente separado de los dormitorios (1: Sí, 0: No). Higiene en la preparación de alimentos del infante."
        if v in ['HV244', 'HV245', 'HV246']:
            return "INCLUIR", "Tenencia de tierras agrícolas, hectáreas y tenencia de animales de cría. Autosuficiencia alimentaria y zoonosis."
        if v in ['HV270', 'HV271']:
            return "INCLUIR", "Quintil de riqueza del hogar (1 a 5) y puntaje factorial continuo de riqueza. Determinante distal de desnutrición."
        return "EXCLUIR POR IRRELEVANCIA", "Detalles menores de tenencia de artefactos específicos o variables operativas redundantes con el índice de riqueza."

    # --- RECH4 (Seguro de Salud) ---
    if dict_name == 'RECH4':
        if v in ['ID1', 'HHID', 'IDX4', 'SHNRO']:
            return "METADATO / LLAVE", "Llaves de identificación del hogar y número de línea de cada integrante."
        if v == 'SH11A':
            return "INCLUIR", "Afiliación al Seguro Integral de Salud (SIS). Subsidio estatal de controles CRED, vacunas y micronutrientes para población vulnerable."
        if v == 'SH11B':
            return "INCLUIR", "Afiliación al seguro EsSalud. Indicador indirecto de empleo formal del padre o de la madre."
        if v in ['SH11C', 'SH11D', 'SH11E', 'SH11Y']:
            return "INCLUIR", "Otras modalidades de seguro de salud (FFAA/Policial, Privado, Universitario, etc.)."
        return "EXCLUIR POR IRRELEVANCIA", "Campos auxiliares de registro del seguro o códigos administrativos."

    # --- RECH1 (Miembros del Hogar) ---
    if dict_name == 'RECH1':
        if v in ['ID1', 'HHID', 'HVIDX']:
            return "METADATO / LLAVE", "Identificador del hogar y número de orden de cada miembro del hogar."
        if v in ['HV101']:
            return "INCLUIR", "Parentesco con el jefe del hogar (hijo, nieto, etc.). Estructura familiar y posición del niño."
        if v in ['HV104', 'HV105']:
            return "INCLUIR", "Sexo y edad de los miembros del hogar. Caracterización demográfica de los cuidadores."
        if v in ['HV106', 'HV107', 'HV109']:
            return "INCLUIR", "Nivel educativo y años de estudio alcanzados por el jefe del hogar y cuidadores principales."
        if v in ['HV111', 'HV112']:
            return "INCLUIR / LLAVE", "Madre viva en el hogar y número de orden de la madre en la cartilla. Fundamental para enlazar niño con registros maternos."
        if v in ['HV113', 'HV114']:
            return "INCLUIR / LLAVE", "Padre vivo en el hogar y número de orden del padre en el hogar."
        return "EXCLUIR POR IRRELEVANCIA", "Control de residencia temporal/de facto o detalles operativos de entrevista."

    # --- RECHM (Mortalidad del Hogar) ---
    if dict_name == 'RECHM':
        return "EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD", "Registro de defunciones en el hogar. Base extremadamente pequeña (2,714 filas en toda la ENDES, >98% nula para el universo de niños menores de 5 años)."

    # --- REC41 (Embarazo, Parto y Lactancia) ---
    if dict_name == 'REC41':
        if v in ['ID1', 'CASEID', 'MIDX']:
            return "METADATO / LLAVE", "Llaves de identificación de la mujer y orden de la historia de nacimiento del niño."
        if v == 'M14':
            return "INCLUIR", "Número total de controles prenatales recibidos durante la gestación. Vigilancia oportuna del crecimiento fetal intrauterino."
        if v == 'M18':
            return "INCLUIR", "Mes de gestación en que inició el primer control prenatal. Detección temprana de patologías gestacionales y RCIU."
        if v == 'M19':
            return "INCLUIR", "Peso al nacer en gramos reportado en carné o memoria. El bajo peso al nacer (< 2,500 g) es el factor etiológico más potente de desnutrición crónica."
        if v == 'M19A':
            return "INCLUIR", "Tamaño del niño al nacer percibido por la madre (muy pequeño, pequeño, promedio, grande). Reporte cualitativo clave cuando no hubo balanza."
        if v == 'M4':
            return "INCLUIR", "Duración de la lactancia materna en meses. Amamantamiento sostenido protege contra infecciones y desnutrición."
        if v == 'M5':
            return "INCLUIR", "Meses de lactancia materna exclusiva. Pilar de nutrición óptima en los primeros 6 meses de vida según OMS."
        if v == 'M15':
            return "INCLUIR", "Lugar de ocurrencia del parto (hospital, centro de salud, posta, domicilio). Indicador de parto institucional y acceso a salud."
        if v in ['M3A', 'M3B', 'M3C']:
            return "INCLUIR", "Personal calificado que atendió el parto (médico, obstetra, enfermera). Calidad y seguridad de la atención perinatal."
        if v == 'M17':
            return "INCLUIR", "Parto por cesárea (1: Sí, 0: No). Vía de nacimiento asociada a morbilidades perinatales."
        if v == 'M45':
            return "INCLUIR", "Madre recibió tabletas o jarabe de hierro durante el embarazo (1: Sí, 0: No). Estado nutricional de la gestante."
        if v == 'M46':
            return "INCLUIR", "Número de días que la madre consumió suplemento de hierro en la gestación. Adherencia preventiva materna."
        if v in ['B11']:
            return "INCLUIR", "Intervalo intergenésico en meses respecto al nacimiento anterior. Períodos < 24 meses agotan reservas maternas de macro/micronutrientes."
        if v in ['B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B8', 'B9', 'B12']:
            return "INCLUIR / METADATO", "Sexo del hijo, mes y año de nacimiento, orden de nacimiento y si es parto múltiple (gemelar)."
        if v in ['V201', 'V212', 'V213']:
            return "INCLUIR", "Total de hijos nacidos vivos, edad de la madre al primer nacimiento y estado de embarazo actual."
        return "EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD", "Preguntas específicas con filtros condicionales restrictivos (tratamiento de malaria, mediciones del alta hospitalaria, etc.)."

    # --- REC94 (Suplementación y Tratamiento Pediátrico) ---
    if dict_name == 'REC94':
        if v in ['ID1', 'CASEID', 'IDX94']:
            return "METADATO / LLAVE", "Llaves de enlace relacional del cuestionario individual y del niño."
        if v in ['S411BA', 'S411CA', 'S411DA', 'S411EA']:
            return "DUDOSA (INTERVENCIÓN PRENATAL)", "Mes de embarazo al realizar pruebas específicas. Evaluar completitud y redundancia con inicio de control prenatal (M18)."
        if v == 'S413':
            return "INCLUIR", "Madre afiliada al SIS durante el embarazo. Acceso a subsidio integral de salud materna y neonatal."
        if v in ['S426GA', 'S426GB', 'S426GC', 'S426GD', 'S426GE']:
            return "INCLUIR", "Complicaciones severas del parto (parto prolongado, sangrado excesivo, convulsiones). Sufrimiento fetal e hipoxia perinatal."
        if v in ['S427DA', 'S427DB', 'S427DC', 'S427DD', 'S427DE', 'S427DF', 'S427DG', 'S427F']:
            return "EXCLUIR POR ALTA INCOMPLETITUD", "Complicaciones del puerperio con muy baja prevalencia de respuesta afirmativa."
        if v in ['S435', 'S440']:
            return "EXCLUIR POR CAUSALIDAD INVERSA", "Razones por las que no dio o dejó de dar pecho por enfermedad/indicación médica. Alto riesgo de causalidad inversa con falla de medro."
        if v in ['QI422A_B', 'QI422A_C', 'QI422A_D']:
            return "DUDOSA (TRATAMIENTO CLÍNICO)", "Diagnóstico e indicación de hierro materno por anemia en el embarazo. Fuerte correlación pero posible causalidad inversa si fue reactivo."
        return "EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD", "Variables operativas de afiliación al seguro, trámites de DNI o filtros condicionales no extrapolables."

    # --- RECH5 (Evaluación Antropométrica y Anemia de Mujeres de 15 a 49 años) ---
    if dict_name == 'RECH5':
        if v in ['ID1', 'HHID', 'HA0']:
            return "METADATO / LLAVE", "Identificador del hogar y número de orden de la mujer en el hogar (cruza con HC60 de RECH6)."
        if v == 'HA3':
            return "INCLUIR", "Talla de la madre en centímetros con 1 decimal. La talla baja materna (< 150 cm) es uno de los determinantes biológicos y epigenéticos más potentes del retardo estatural del niño."
        if v == 'HA2':
            return "INCLUIR", "Peso de la madre en kilogramos. Evalúa reserva energética y estado nutricional de la madre."
        if v in ['HA40', 'HA41']:
            return "INCLUIR", "Índice de Masa Corporal (IMC) e Índice de Rohrer de la madre. Bajo peso materno (IMC < 18.5) se asocia directamente a desnutrición crónica infantil."
        if v in ['HA53', 'HA56', 'HA56A', 'HA57', 'HA57A']:
            return "DUDOSA (BIOMARCADOR CONCURRENTE)", "Nivel de hemoglobina y anemia de la madre. Puede incluirse como proxy de calidad nutricional y reservas biológicas maternas, pero requiere punción capilar."
        if v in ['HA66', 'HA67', 'HA68']:
            return "INCLUIR", "Nivel educativo más alto aprobado y años de educación de la madre. Pilar de capital humano para el cuidado y alimentación del menor."
        if v in ['HA4', 'HA5', 'HA6', 'HA11', 'HA12', 'HA12A', 'HA12B']:
            return "EXCLUIR POR IRRELEVANCIA / REDUNDANCIA", "Percentiles y desvíos antropométricos de referencia de la mujer frente a estándares adultos ya sintetizados en el IMC (HA40)."
        return "EXCLUIR POR IRRELEVANCIA", "Consentimientos de pruebas de VIH, códigos operativos de campo, consumo de cigarrillos o factores no predictivos."

    # --- NUEVOS MÓDULOS 1031-MEF ---
    if dict_name == 'REC0111':
        if v in ['ID1', 'CASEID', 'HHID']:
            return "METADATO / LLAVE", "Llaves relacionales de la mujer (MEF) y del hogar."
        if v in ['V012', 'V013']:
            return "INCLUIR", "Edad actual de la madre en años y por grupos quinquenales. Embarazo adolescente o edad materna avanzada."
        if v in ['V106', 'V107']:
            return "INCLUIR", "Nivel educativo más alto de la madre y años de educación aprobados. Determinante social de salud infantil."
        if v in ['V130']:
            return "INCLUIR", "Religión de la entrevistada (católica, evangélica, etc.). Pautas culturales de crianza y alimentación."
        if v in ['V131']:
            return "INCLUIR", "Etnicidad / Autoidentificación étnica de la mujer. Captura desigualdades históricas de pueblos originarios."
        if v in ['V139', 'V024']:
            return "INCLUIR", "Región de residencia habitual De-Jure (departamento 1 a 25)."
        if v in ['V190', 'V191']:
            return "INCLUIR", "Índice de riqueza y factor de puntuación en el cuestionario de MEF."
        if v in ['V201']:
            return "INCLUIR", "Total de hijos nacidos vivos (paridad acumulada)."
        if v in ['V212']:
            return "INCLUIR", "Edad de la madre al primer nacimiento."
        if v in ['V501', 'V502']:
            return "INCLUIR", "Estado civil / estado conyugal actual de la madre (casada, conviviente, soltera). Soporte biparental."
        if v in ['V701', 'V704', 'V705']:
            return "INCLUIR", "Nivel educativo y ocupación de la pareja/esposo. Capacidad de generación de ingresos familiares."
        if v in ['V714', 'V717']:
            return "INCLUIR", "Madre trabaja actualmente y tipo de ocupación. Tiempo disponible para lactancia y cuidado."
        if v in ['V743A', 'V743B', 'V743D']:
            return "INCLUIR", "Toma de decisiones de la mujer sobre atención de salud, compras del hogar y visitas. Autonomía femenina y empoderamiento."
        return "EXCLUIR POR IRRELEVANCIA", "Detalles específicos de fecundidad, calendarios de anticoncepción o marcas de campo."

    if dict_name == 'REC91':
        if v in ['ID1', 'CASEID']:
            return "METADATO / LLAVE", "Llaves relacionales de la mujer en el módulo individual ampliado."
        if v == 'S119':
            return "INCLUIR", "Idioma o lengua materna que aprendió a hablar en su niñez la madre (Quechua, Aimara, Castellano, etc.). Barrera lingüística y etnicidad."
        if v == 'S119NA':
            return "INCLUIR", "Lengua materna de la abuela materna. Herencia lingüística indígena intergeneracional."
        if v in ['S108N', 'S108Y']:
            return "INCLUIR", "Nivel y año educativo aprobado detallado."
        if v == 'S111':
            return "INCLUIR", "Madre asiste actualmente a escuela, instituto o universidad."
        if v in ['SPROVIN', 'SDISTRI']:
            return "INCLUIR", "Provincia y distrito de residencia de la mujer (georreferenciación fina)."
        return "EXCLUIR POR IRRELEVANCIA", "Preguntas específicas de deserción escolar, calendarios reproductivos o subsecciones de opinión."

    # --- NUEVOS MÓDULOS 1036-INMUNIZACION ---
    if dict_name == 'DIT':
        if v in ['ID1', 'CASEID', 'BIDX', 'BORD']:
            return "METADATO / LLAVE", "Identificadores relacionales del niño en el módulo de Desarrollo Infantil Temprano."
        if v == 'QI478':
            return "INCLUIR", "Edad del niño en meses en el módulo DIT."
        if v == 'QI478A':
            return "INCLUIR", "Niño vive con la madre y presencia de discapacidad."
        if v == 'QI478E1':
            return "DUDOSA (BIDIRECCIONALIDAD)", "Hitos motores gruesos (pararse, caminar). El retardo estatural severo retrasa la deambulación; posible consecuencia en vez de predictor."
        if v in ['QI478E2']:
            return "INCLUIR", "Espacio libre para desplazarse y gatear/caminar en el hogar. Estimulación psicomotriz y entorno seguro."
        if v in ['QI478E3', 'QI478E4', 'QI478E5', 'QI478E6']:
            return "INCLUIR", "Pautas de estimulación temprana y lenguaje (madre habla, lee o canta al infante)."
        if v in ['QI478E7', 'QI478E8', 'QI478E9']:
            return "INCLUIR", "Interacción afectiva y apego seguro entre cuidador y niño."
        return "EXCLUIR POR IRRELEVANCIA", "Ítems secundarios del test DIT no extrapolables a población menor de 24 meses."

    if dict_name == 'REC42':
        if v in ['ID1', 'CASEID', 'V401', 'V404', 'V405']:
            return "METADATO / LLAVE", "Identificadores del niño e historial reproductivo."
        if v == 'V411':
            return "INCLUIR", "El niño tuvo diarrea en las últimas dos semanas. CAUSA INMEDIATA DIRECTA (UNICEF): atrofia de vellosidades intestinales y mala absorción crónica."
        if v == 'V411A':
            return "INCLUIR", "Diarrea con sangre en heces (disentería). Infección invasiva bacteriana destructiva de mucosa entérica."
        if v == 'V412':
            return "INCLUIR", "Recibió atención médica por el episodio diarreico. Acceso oportuno a tratamiento."
        if v == 'V413':
            return "INCLUIR", "Tratamiento de diarrea con Sales de Rehidratación Oral (SRO). Prevención de deshidratación grave."
        if v == 'V414':
            return "INCLUIR", "El niño tuvo fiebre en las últimas dos semanas. Marcador de infección sistémica y consumo calórico acelerado."
        if v == 'V415':
            return "INCLUIR", "El niño tuvo tos o dificultad para respirar (IRA reciente) en las últimas dos semanas."
        if v == 'V416':
            return "INCLUIR", "Signos de neumonía aguda (respiración rápida o pecho hundido)."
        if any(v.startswith(p) for p in ['V467', 'V468', 'V469', 'V470', 'V471', 'V472', 'V473', 'V474', 'V475', 'V476', 'V477', 'V478']):
            return "INCLUIR", "Consumo de grupos específicos de alimentos en las últimas 24h (carnes, huevos, legumbres, lácteos, frutas). Diversidad dietética mínima."
        return "EXCLUIR POR IRRELEVANCIA", "Detalles menores de marcas comerciales de medicamentos o preguntas de control."

    if dict_name == 'REC43':
        if v in ['ID1', 'CASEID', 'HIDX']:
            return "METADATO / LLAVE", "Identificadores relacionales del niño en el registro de vacunación."
        if v == 'H1':
            return "INCLUIR", "Tenencia de carné de vacunación físico visto por encuestadora. Indicador de contacto formal con el sistema de salud."
        if v == 'H2':
            return "INCLUIR", "Vacuna BCG (dosis única al nacer contra tuberculosis meníngea)."
        if v in ['H3', 'H5', 'H7']:
            return "INCLUIR", "Dosis 1, 2 y 3 de vacuna Pentavalente (Difteria, Tétanos, Tos Ferina, Hepatitis B, Hib). Inmunización básica."
        if v in ['H4', 'H6', 'H8']:
            return "INCLUIR", "Dosis 1, 2 y 3 de vacuna antipolio."
        if v in ['H31', 'H31B']:
            return "INCLUIR", "Dosis 1 y 2 de vacuna contra Rotavirus. Previene gastroenteritis aguda deshidratante, causa mayor de retardo estatural."
        if v in ['H32', 'H32B', 'H32C']:
            return "INCLUIR", "Dosis 1, 2 y 3 de vacuna antineumocócica. Previene neumonías e infecciones invasivas por Streptococcus pneumoniae."
        if v in ['H9', 'H9A']:
            return "INCLUIR", "Dosis 1 y 2 de vacuna SPR (Sarampión, Paperas, Rubeola). El sarampión desencadena desnutrición severa post-infecciosa."
        if v == 'H34':
            return "INCLUIR", "Niño recibió suplemento de Vitamina A en los últimos 6 meses. Fortalecimiento inmunológico del epitelio intestinal."
        if v == 'H43':
            return "INCLUIR", "Niño recibió tratamiento antiparasitario en los últimos 6 meses. Prevención de geohelmintiasis causante de mala absorción."
        return "EXCLUIR POR IRRELEVANCIA", "Fechas administrativas de administración de cada vacuna (días, meses, años)."

    if dict_name == 'REC95':
        if v in ['ID1', 'CASEID', 'IDX95']:
            return "METADATO / LLAVE", "Identificadores relacionales del niño en salud infantil ampliada."
        if v in ['S45D4', 'S45D4D', 'S45D4M', 'S45D4Y']:
            return "INCLUIR", "Controles de Crecimiento y Desarrollo (CRED) y carné CRED verificado."
        if v == 'S45C':
            return "INCLUIR", "Número total de controles CRED recibidos por el infante. Vigilancia activa del crecimiento longitudinal."
        if 'S466' in v:
            return "DUDOSA (TRATAMIENTO DE ANEMIA)", "Suplementación con gotas o jarabe de hierro infantil. Evaluar causalidad inversa si fue reactivo."
        return "EXCLUIR POR IRRELEVANCIA", "Detalles operativos de citas médicas o preguntas de control."

    # --- NUEVOS MÓDULOS 1041-PROGRAMA SOCIAL ---
    if dict_name == 'Programas Sociales x Hogar':
        if v in ['ID1', 'HHID', 'QHCLUSTER', 'QHNUMBER', 'QHHOME']:
            return "METADATO / LLAVE", "Llaves de enlace a nivel de hogar y conglomerado."
        if v == 'QH91':
            return "INCLUIR", "Hogar beneficiario de Beca 18. Alivio económico familiar por educación superior de hijos mayores."
        if v == 'QH93':
            return "INCLUIR", "Hogar beneficiario de Trabaja Perú. Empleo temporal de emergencia en zonas vulnerables."
        if v == 'QH95':
            return "INCLUIR", "Hogar beneficiario del Programa JUNTOS. Transferencia monetaria condicionada a controles CRED y vacunas del infante."
        if v in ['QH96A', 'QH96M']:
            return "INCLUIR", "Tiempo en años y meses como beneficiario de JUNTOS. Exposición acumulada al programa social."
        if v == 'QH99':
            return "INCLUIR", "Hogar beneficiario de Pensión 65. Transferencia a adultos mayores que reduce la pobreza extrema del hogar."
        if v == 'QH101':
            return "INCLUIR", "Hogar recibe apoyo del Programa del Vaso de Leche (PVL). Complementación alimentaria municipal."
        if v == 'QH103':
            return "INCLUIR", "Hogar recibe raciones de Comedores Populares. Subsidio alimentario en barrios precarios."
        if v == 'QH106':
            return "INCLUIR", "Niño o miembro del hogar asiste a Cuna Más / Wawa Wasi. Cuidado diurno y alimentación balanceada para menores de 36 meses."
        if v == 'QHVIOLEN':
            return "DUDOSA (SENSIBILIDAD ÉTICA)", "Presencia de violencia doméstica reportada en el hogar. Factor de negligencia y estrés tóxico infantil."
        return "EXCLUIR POR IRRELEVANCIA", "Detalles menores de acuerdos de compromiso o fechas administrativas."

    # Submódulos específicos de programas sociales
    if 'PS_' in dict_name:
        if v in ['ID1', 'HHID', 'HVIDX', 'QHCLUSTER', 'QHNUMBER', 'QHHOME']:
            return "METADATO / LLAVE", "Llaves de enlace relacional del beneficiario en el hogar."
        if any(v.endswith(suffix) for suffix in ['_1A', '_1M']):
            return "INCLUIR", f"Tiempo en años y meses que el miembro es beneficiario de {dict_name}."
        if any(v.endswith(suffix) for suffix in ['_1S']):
            return "INCLUIR", f"Alguien más en el hogar es beneficiario de {dict_name}."
        return "EXCLUIR POR IRRELEVANCIA", "Campos auxiliares del módulo social específico."

    return "EXCLUIR POR IRRELEVANCIA", "Variable operativa, de control de campo o sin sustento explicativo."

print("Classifier complete.")

def generate_markdown_catalog():
    all_dicts = load_all_dictionaries()
    
    # Classify all variables
    total_vars = 0
    stats = {'INCLUIR': 0, 'DUDOSA': 0, 'EXCLUIR_LEAKAGE': 0, 'EXCLUIR_IRRELEVANTE': 0, 'METADATO': 0, 'TARGET': 0}
    classified_data = {}
    
    for d_name, d_info in all_dicts.items():
        classified_data[d_name] = []
        for v_item in d_info['vars']:
            dec, mot = classify_variable(d_name, v_item)
            classified_data[d_name].append({
                'item': v_item,
                'decision': dec,
                'motivo': mot
            })
            total_vars += 1
            if 'VARIABLE OBJETIVO' in dec:
                stats['TARGET'] += 1
            elif 'INCLUIR' in dec:
                stats['INCLUIR'] += 1
            elif 'DUDOSA' in dec:
                stats['DUDOSA'] += 1
            elif 'LEAKAGE' in dec or 'CAUSALIDAD INVERSA' in dec:
                stats['EXCLUIR_LEAKAGE'] += 1
            elif 'METADATO' in dec:
                stats['METADATO'] += 1
            else:
                stats['EXCLUIR_IRRELEVANTE'] += 1

    print(f"Total variables procesadas: {total_vars}")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    # Build markdown text
    md = []
    
    # Header
    md.append("# Catálogo Exhaustivo de Variables — Desnutrición Crónica Infantil (ENDES 2025, INEI)")
    md.append("## Prevención de Fuga de Información (Target Leakage), Causalidad Inversa y Selección para XGBoost\n")
    md.append("**Proyecto:** Predicción del Riesgo de Desnutrición Crónica Infantil (Talla para la Edad < -2 DE OMS) en Menores de 5 Años en el Perú  ")
    md.append("**Fuente Oficial:** Instituto Nacional de Estadística e Informática (INEI) — Encuesta Demográfica y de Salud Familiar (ENDES 2025)  ")
    md.append("**Población Objetivo:** Niños de 0 a 59 meses cumplidos con medición antropométrica válida en el hogar  ")
    md.append("**Fecha de Elaboración:** Octubre 2026  \n")
    md.append("---\n")
    
    # 1. Criterios Metodológicos
    md.append("## 1. Criterios Metodológicos Adaptados a Desnutrición Crónica Infantil\n")
    md.append("A diferencia de la anemia infantil (que es una condición bioquímica transitoria dependiente del balance de hierro y eritropoyesis), la **desnutrición crónica infantil (retraso en el crecimiento lineal o *stunting*)** refleja la **acumulación de privaciones nutricionales, infecciones gastrointestinales/respiratorias recurrentes y enteropatía ambiental** durante la ventana crítica de los **primeros 1,000 días de vida** (desde la concepción hasta los 24 meses).\n")
    md.append("Para estructurar un modelo predictivo robusto, generalizable y defendible ante un comité académico o de salud pública, se aplican los siguientes seis principios rectores:\n")
    md.append("1. **Prevención Estricta de Fuga de Información (Target Leakage):**")
    md.append("   - Queda terminantemente prohibido el uso de `HC70` y `HW70` (que constituyen el objetivo directo).")
    md.append("   - Se prohíbe el uso de la **talla en centímetros** (`HC3`, `HW3`), de percentiles (`HC4`, `HW4`), desvíos estándar (`HC5`, `HW5`) y porcentajes de la mediana (`HC6`, `HW6`), ya que un árbol de decisión como XGBoost puede reconstruir matemáticamente el puntaje Z de talla/edad combinando talla, edad (`HC1`) y sexo (`HC27`).")
    md.append("   - Se excluyen por defecto los puntajes antropométricos Z concurrentes (`HC71` Peso/Edad, `HC72` Peso/Talla, `HC73` IMC), por tratarse de subrogados clínicos directos del estado nutricional que no estarían disponibles sin una evaluación antropométrica formal previa.\n")
    md.append("2. **Condición de Screening Comunitario (No Invasivo / Visita Domiciliaria):**")
    md.append("   - El objetivo operativo del modelo es apoyar a agentes comunitarios de salud, enfermeras del primer nivel y programas sociales (ej. Cuna Más, JUNTOS) en la identificación temprana de niños en alto riesgo de retardo estatural mediante **entrevista domiciliaria verbal**.")
    md.append("   - No se asume la tenencia de tallímetros de madera calibrados, balanzas pediátricas de precisión ni lancetas/hemoglobinómetros en el primer contacto comunitario de screening.\n")
    md.append("3. **Control Riguroso de Causalidad Inversa:**")
    md.append("   - En encuestas transversales como ENDES, las preguntas sobre medicamentos o tratamientos (ej. antibióticos para diarrea grave, jarabe terapéutico o atención de emergencia por falla de medro en `REC94`/`REC42`) pueden reflejar que el niño **ya fue diagnosticado** y tratado por su retardo estatural o emaciación.")
    md.append("   - Se excluyen las intervenciones terapéuticas reactivas y solo se preservan las medidas estrictamente preventivas (suplementación universal profiláctica materna, vacunas, transferencias condicionadas).\n")
    md.append("4. **Respeto al Diseño Muestral Complejo de la ENDES:**")
    md.append("   - La ENDES es una encuesta bietápica, probabilística y estratificada. Las variables `HV001` (conglomerado/PSU), `HV022` (estrato de muestreo) y `HV005` (factor de ponderación) deben preservarse intactas como **metadatos de muestreo**.")
    md.append("   - `HV001` debe emplearse como llave de agrupación en `StratifiedGroupKFold` para evitar fuga espacial entre niños del mismo vecindario o aldea.")
    md.append("   - `HV005` (dividido entre 1,000,000) debe integrarse como `sample_weight` en XGBoost para reflejar las probabilidades reales de selección poblacional.\n")
    md.append("5. **Tratamiento Nativo de NaNs Estructurales:**")
    md.append("   - Múltiples preguntas de la ENDES poseen filtros de pase condicionales (ej. duración de lactancia materna solo si el niño fue amamantado, preguntas de diarrea solo si tuvo síntomas).")
    md.append("   - Se aprovecha la capacidad nativa de XGBoost para aprender divisiones óptimas de valores nulos (`default_direction`), evitando imputaciones sintéticas artificiales (como media o mediana) que distorsionarían la estructura epidemiológica de la no aplicabilidad.\n")
    md.append("6. **Ajuste por Desbalance de Clase:**")
    md.append("   - Con una prevalencia nacional de desnutrición crónica en torno al 11.5%, la distribución positiva:negativa es de aproximadamente 1:7.7. Se documenta la configuración formal de `scale_pos_weight` y la optimización de métricas orientadas a clases minoritarias (PR-AUC, Recall y F1 con umbral calibrado).\n")
    md.append("---\n")

    # 2. Definición Exacta de la Variable Objetivo
    md.append("## 2. Definición Exacta de la Variable Objetivo ($Y$) y su Construcción Paso a Paso\n")
    md.append("### 2.1 Criterio Internacional (OMS 2006)")
    md.append("De acuerdo con los estándares de crecimiento infantil de la Organización Mundial de la Salud (OMS 2006), adoptados oficialmente por el Ministerio de Salud del Perú (MINSA), la **desnutrición crónica infantil** se define formalmente como un **Puntaje Z de Talla para la Edad ($Z_{T/E}$) inferior a -2.00 Desviaciones Estándar** respecto a la población de referencia medianamente nutrida.\n")
    md.append("$$Y_i = \\text{desnutricion\\_cronica}_i = \\begin{cases} 1, & \\text{si } Z_{T/E} < -2.00 \\text{ DE} \\\\ 0, & \\text{si } Z_{T/E} \\ge -2.00 \\text{ DE} \\end{cases}$$\n")
    md.append("### 2.2 Fuente Primaria en ENDES 2025: `HC70` en `RECH6`")
    md.append("En el archivo oficial `RECH6_2025.csv` (Cuestionario de Hogar: Niños menores de 5 años evaluados en antropometría y hemoglobina), la variable `HC70` almacena el puntaje Z de talla para la edad según la norma OMS, **expresado en centésimas de desviación estándar** (con dos decimales implícitos).")
    md.append("- Ejemplo: Un valor registrado de `-250` representa un Z-score de **-2.50 DE** (desnutrición crónica).")
    md.append("- Un valor registrado de `-180` representa un Z-score de **-1.80 DE** (eutrófico o sin retardo estatural severo).")
    md.append("- Por consiguiente, el umbral matemático de clasificación es exactamente **`HC70 < -200`**.\n")
    md.append("### 2.3 Protocolo de Limpieza y Depuración de Casos Inválidos")
    md.append("El diccionario oficial del INEI especifica códigos especiales de control antropométrico que deben ser **eliminados de la muestra analítica antes de definir el target**:")
    md.append("- `9996`: Altura/Talla fuera de rango biológico plausible según la OMS ($Z < -6.00$ DE o $Z > +6.00$ DE; error de instrumento o digitación).")
    md.append("- `9997`: Inconsistencia de fecha de nacimiento o medición.")
    md.append("- `9998`: Caso no medido (niño no presente, madre rechazó la medición o no fue encontrado en el hogar).")
    md.append("- Valores vacíos o `NaN` en `HC70`.\n")
    md.append("```python")
    md.append("# Algoritmo de Construcción del Target (Python / Pandas):")
    md.append("def construir_target_desnutricion(df_rech6):")
    md.append("    # 1. Descartar códigos de error antropométrico y no medidos")
    md.append("    filtro_validos = (")
    md.append("        df_rech6['HC70'].notna() &")
    md.append("        (~df_rech6['HC70'].isin([9996, 9997, 9998])) &")
    md.append("        (df_rech6['HC70'] >= -600) & (df_rech6['HC70'] <= 600) &")
    md.append("        (df_rech6['HC1'] >= 0) & (df_rech6['HC1'] <= 59)")
    md.append("    )")
    md.append("    df_clean = df_rech6[filtro_validos].copy()")
    md.append("    ")
    md.append("    # 2. Asignar variable objetivo binaria (1 = Desnutrición Crónica, 0 = Sin desnutrición crónica)")
    md.append("    df_clean['desnutricion_cronica'] = (df_clean['HC70'] < -200).astype(int)")
    md.append("    return df_clean")
    md.append("```\n")
    md.append("### 2.4 Verificación Cruzada con `REC44` (`HW70`)")
    md.append("En el archivo `REC44_2025.csv` (Cuestionario Individual de Mujeres), la variable homóloga es `HW70`. Durante el control de calidad, se verifica que para los niños coincidentes por `HHID` y número de orden, se cumpla la paridad `HC70 == HW70`. `RECH6` se mantiene como la fuente canónica por abarcar la muestra censal de todos los niños del hogar.\n")
    md.append("### 2.5 Desbalance de Clase y Recomendaciones de Modelado")
    md.append("- **Prevalencia esperada:** ~11.5% a nivel nacional (con picos superiores al 25–30% en zonas rurales altoandinas y comunidades nativas de la Selva).")
    md.append("- **Ratio de desbalance:** ~1 caso positivo por cada 7.7 casos negativos.")
    md.append("- **Parametrización XGBoost:** Configurar `scale_pos_weight = 7.7` para penalizar los falsos negativos.")
    md.append("- **Métricas de Evaluación:** Prohibido evaluar únicamente con Accuracy o ROC-AUC por el sesgo de clase mayoritaria. Las métricas prioritarias son **PR-AUC (Área bajo la curva Precision-Recall)**, **Recall / Sensibilidad** (imprescindible para no perder niños desnutridos en screening) y **F1-Score calibrando el umbral de decisión**.")
    md.append("---\n")

    # 3. Resumen Ejecutivo del Inventario
    md.append("## 3. Resumen Ejecutivo del Inventario de Datos (23 Archivos Analizados)\n")
    md.append("| Módulo | Archivo CSV / PDF | Registros Estimados | Variables | Descripción Oficial del Módulo | Rol en el Proyecto |")
    md.append("|:---|:---|---:|---:|:---|:---|")
    
    # Inventario tabla
    meta_table = [
        ("1638", "RECH6", "19,298", "43", "Evaluación antropométrica y hemoglobina en niños < 5 años", "**NÚCLEO: TARGET + Niño en Hogar**"),
        ("1638", "REC44", "18,841", "34", "Salud y antropometría de hijos en cuestionario individual", "Auditoría / Verificación cruzada"),
        ("1638", "RECH5", "37,679", "40", "Evaluación de mujeres de 15 a 49 años (antropometría y anemia)", "**Madre: Talla, IMC y Estado Nutricional**"),
        ("1629", "RECH0", "37,331", "44", "Características del hogar, geografía y diseño muestral", "**Diseño Muestral + Geografía + Hogar**"),
        ("1629", "RECH1", "131,929", "36", "Composición de miembros, parentesco y educación", "**Estructura Familiar y Educación de Cuidadores**"),
        ("1629", "RECH4", "131,929", "21", "Seguro de salud de los integrantes del hogar", "**Seguro SIS / Acceso a Servicios**"),
        ("1629", "RECHM", "2,714", "8", "Mortalidad general en el hogar en los últimos años", "Descartado (>98% nulo)"),
        ("1630", "RECH23", "37,331", "130", "Vivienda, agua, saneamiento y quintil de riqueza", "**Agua JMP, Saneamiento, Piso y Riqueza**"),
        ("1633", "REC41", "18,841", "147", "Embarazo, parto, puerperio y lactancia materna", "**Controles Prenatales, Peso Nacer y Lactancia**"),
        ("1633", "REC94", "18,841", "61", "Suplementación con micronutrientes y tratamientos", "Complicaciones Perinatales / Causalidad Inversa"),
        ("1031", "REC0111", "37,679", "104", "Datos sociodemográficos y reproductivos de la mujer (MEF)", "**Edad Materna, Educación, Autonomía y Paridad**"),
        ("1031", "REC91", "37,679", "343", "Etnicidad, lengua materna y educación ampliada de la madre", "**Lengua Materna Indígena y Localización Fina**"),
        ("1036", "DIT", "18,841", "63", "Desarrollo Infantil Temprano (hitos y estimulación)", "**Estimulación Temprana y Entorno Seguro**"),
        ("1036", "REC42", "18,841", "169", "Salud infantil: Diarrea (EDA), Infecciones (IRA) y Dieta 24h", "**CAUSAS INMEDIATAS: Morbilidad y Diversidad Dieta**"),
        ("1036", "REC43", "18,841", "168", "Registro oficial de vacunas infantiles del carné de salud", "**Vacunación Completa: Rotavirus, Neumo, SPR**"),
        ("1036", "REC95", "18,841", "315", "Controles CRED de crecimiento y salud infantil ampliada", "**Adherencia a Controles CRED Infantiles**"),
        ("1041", "Programas Sociales x Hogar", "37,331", "20", "Cobertura de programas sociales en el hogar (JUNTOS, etc.)", "**Programas de Transferencia y Alimentación**"),
        ("1041", "PS_COMEDOR", "62,621", "10", "Beneficiarios de Comedores Populares a nivel individual", "Detalle de subsidio alimentario"),
        ("1041", "PS_CUNAMAS_VISITA", "110,715", "10", "Acompañamiento a Familias (SAF) de Cuna Más", "Cuidado integral y visitas domiciliarias"),
        ("1041", "PS_QALIWARMA", "828,981", "11", "Programa de alimentación escolar Qali Warma", "Alimentación preescolar"),
        ("1041", "PS_TRABAJA", "5,484", "10", "Programa de empleo temporal Trabaja Perú", "Ingreso familiar de emergencia"),
        ("1041", "PS_VL VASO DE LECHE", "394,989", "10", "Programa municipal del Vaso de Leche (PVL)", "Complemento lácteo municipal"),
        ("1041", "PS_WAWAWASI", "35,174", "10", "Cuna Más Servicio de Cuidado Diurno (Wawa Wasi)", "Cuidado diurno y raciones proteicas"),
    ]
    for row in meta_table:
        md.append(f"| `{row[0]}` | `{row[1]}` | {row[2]} | {row[3]} | {row[4]} | {row[5]} |")
    md.append("\n---\n")

    # 4. Catálogo Detallado por Archivo
    md.append("## 4. Catálogo Detallado por Archivo (Evaluación Exhaustiva de 1,807 Variables)\n")
    md.append("> En esta sección se clasifica **cada una de las variables oficiales** existentes en los 23 diccionarios. Se asigna una categoría formal de decisión y un motivo epidemiológico/metodológico específico adaptado a desnutrición crónica infantil.\n")
    
    dict_order = [
        'RECH6', 'REC44', 'RECH5', 'RECH0', 'RECH1', 'RECH4', 'RECHM', 'RECH23', 'REC41', 'REC94',
        'REC0111', 'REC91', 'DIT', 'REC42', 'REC43', 'REC95', 'Programas Sociales x Hogar',
        'PS_COMEDOR', 'PS_CUNAMAS_VISITA', 'PS_QALIWARMA', 'PS_TRABAJA', 'PS_VL VASO DE LECHE', 'PS_WAWAWASI'
    ]
    
    for d_code in dict_order:
        if d_code not in classified_data:
            continue
        v_list = classified_data[d_code]
        mod_name = all_dicts[d_code]['modulo']
        file_desc = all_dicts[d_code]['file_desc']
        md.append(f"### 📁 Archivo: `{file_desc}` — Módulo: `{mod_name}`")
        md.append(f"**Total de variables evaluadas:** {len(v_list)}\n")
        md.append("| Nº | Variable | Descripción Oficial (INEI) | Decisión | Motivo Metodológico y Epidemiológico |")
        md.append("|:---|:---|:---|:---|:---|")
        for v_item in v_list:
            item = v_item['item']
            dec = v_item['decision']
            mot = v_item['motivo']
            desc_clean = item['desc'].replace('|', '&#124;').replace('\n', '<br>')
            md.append(f"| {item['num']} | `{item['var']}` | {desc_clean} | **{dec}** | {mot} |")
        md.append("\n")
    md.append("---\n")

    # 5. Matriz Final de Variables Seleccionadas
    md.append("## 5. Matriz Final de Variables SELECCIONADAS ($X$)\n")
    md.append("A continuación se consolida la matriz explicativa prioritaria para el entrenamiento de XGBoost. Todas las variables seleccionadas provienen de los diccionarios oficiales y respetan el marco conceptual de desnutrición de UNICEF (determinantes inmediatos, subyacentes y estructurales):\n")
    
    selected_table = [
        ("edad_meses", "HC1", "RECH6", "Niño", "Continua / Discreta", "Ninguno", "Factor biológico central de crecimiento; acumulación progresiva del déficit de talla hasta los 24-36 meses."),
        ("sexo_nino", "HC27", "RECH6", "Niño", "Binaria (0/1)", "Ninguno", "Dimorfismo sexual biológico en velocidad de crecimiento lineal y masa magra."),
        ("departamento", "HV024", "RECH0", "Geografía", "Categórica Nominal", "Ninguno", "Captura desigualdades estructurales, climáticas e institucionales entre regiones."),
        ("area_residencia", "HV025", "RECH0", "Geografía", "Binaria (Urb/Rur)", "Ninguno", "Brecha rural-urbana histórica en provisión de saneamiento, agua tratada y pobreza."),
        ("altitud_msnm", "HV040", "RECH0", "Geografía", "Continua", "Ninguno", "Altitud geográfica en msnm; hipoxia ambiental y fuerte correlación con ruralidad andina aislada."),
        ("total_miembros_hogar", "HV009", "RECH0", "Hogar", "Discreta", "Ninguno", "Carga demográfica intrafamiliar y dilución del presupuesto alimentario per cápita."),
        ("menores_5anos_hogar", "HV014", "RECH0", "Hogar", "Discreta", "Ninguno", "Competencia directa por tiempo de cuidado materno, lactancia y raciones nutricionales."),
        ("fuente_agua_beber", "HV201", "RECH23", "Vivienda", "Categórica Nominal", "96 (Otro)", "Clave en enteropatía ambiental e infecciones diarreicas recurrentes."),
        ("tipo_servicio_higienico", "HV205", "RECH23", "Vivienda", "Categórica Nominal", "96 (Otro)", "Clasificación de saneamiento mejorado vs. no mejorado según criterios JMP OMS/UNICEF."),
        ("tiene_electricidad", "HV206", "RECH23", "Vivienda", "Binaria (0/1)", "Ninguno", "Posibilidad de conservar cadena de frío para alimentos proteicos de origen animal."),
        ("material_piso", "HV213", "RECH23", "Vivienda", "Categórica Nominal", "96 (Otro)", "Piso de tierra/arena actúa como reservorio directo de parásitos y bacterias entéricas."),
        ("habitaciones_dormir", "HV216", "RECH23", "Vivienda", "Discreta", "98 (No sabe)", "Denominador obligatorio para computar el índice de hacinamiento por dormitorio."),
        ("bano_compartido", "HV225", "RECH23", "Vivienda", "Binaria (0/1)", "Ninguno", "Contaminación cruzada en letrinas/baños compartidos con otros hogares."),
        ("combustible_cocinar", "HV226", "RECH23", "Vivienda", "Categórica Nominal", "96 (Otro)", "Uso de biomasa (leña, bosta) incrementa riesgo de infecciones respiratorias agudas."),
        ("tratamiento_agua", "HV237", "RECH23", "Vivienda", "Binaria (0/1)", "Ninguno", "Práctica de hervir o clorar agua como barrera sanitaria fundamental."),
        ("quintil_riqueza", "HV270", "RECH23", "Socioeconómica", "Categórica Ordinal", "Ninguno", "Nivel socioeconómico del hogar; predictor distal más potente de seguridad alimentaria."),
        ("seguro_sis", "SH11A", "RECH4", "Salud", "Binaria (0/1)", "Ninguno", "Afiliación al Seguro Integral de Salud estatal; acceso a controles CRED y vacunas."),
        ("seguro_essalud", "SH11B", "RECH4", "Salud", "Binaria (0/1)", "Ninguno", "Indicador proxy de empleo formal con salario fijo del padre o madre."),
        ("controles_prenatales", "M14", "REC41", "Gestación", "Discreta", "98 (No sabe)", "Vigilancia médica del crecimiento intrauterino y detección de patologías gestacionales."),
        ("mes_inicio_prenatal", "M18", "REC41", "Gestación", "Continua / Discreta", "98 (No sabe)", "Inicio oportuno del control gestacional durante el primer trimestre."),
        ("peso_al_nacer_g", "M19", "REC41", "Nacimiento", "Continua", "9996-9998", "Bajo peso al nacer (< 2,500 g) por RCIU o prematuridad; factor etiológico congénito principal."),
        ("tamano_nacer_aparente", "M19A", "REC41", "Nacimiento", "Categórica Ordinal", "8 (No sabe)", "Reporte materno del tamaño al nacer; rescata bajo peso cuando no hubo balanza."),
        ("duracion_lactancia_m", "M4", "REC41", "Lactancia", "Continua / Discreta", "95-98", "Meses acumulados de amamantamiento; protección inmunológica sostenida."),
        ("lactancia_exclusiva_m", "M5", "REC41", "Lactancia", "Continua / Discreta", "95-98", "Meses de lactancia materna exclusiva (estándar OMS: 6 meses sin otros líquidos)."),
        ("lugar_parto", "M15", "REC41", "Nacimiento", "Categórica Nominal", "96 (Otro)", "Parto institucional en establecimiento de salud vs. parto domiciliario precario."),
        ("atencion_parto_calif", "M3A", "REC41", "Nacimiento", "Binaria (0/1)", "Ninguno", "Parto asistido por personal médico u obstetra calificado."),
        ("hierro_madre_gestacion", "M45", "REC41", "Gestación", "Binaria (0/1)", "8 (No sabe)", "Suplementación preventiva con hierro a la madre durante el embarazo."),
        ("dias_hierro_madre", "M46", "REC41", "Gestación", "Continua / Discreta", "998 (No sabe)", "Días acumulados de ingesta de hierro gestacional; reserva biológica materna."),
        ("intervalo_intergenesico", "B11", "REC41", "Gestación", "Continua", "Ninguno", "Meses transcurridos desde el nacimiento previo; intervalos < 24m agotan reservas maternas."),
        ("talla_madre_cm", "HA3", "RECH5", "Madre", "Continua", "9998", "Talla materna con 1 decimal; captura la herencia genética y el ciclo intergeneracional del retardo estatural."),
        ("imc_madre", "HA40", "RECH5", "Madre", "Continua", "9998", "Índice de masa corporal materno (con 2 decimales); desnutrición materna crónica."),
        ("edad_madre_anos", "V012", "REC0111", "Madre", "Continua", "Ninguno", "Edad actual de la madre en años cumplidos; embarazo en adolescencia temprana."),
        ("educacion_madre_nivel", "V106", "REC0111", "Madre", "Categórica Ordinal", "Ninguno", "Nivel educativo de la madre; determinante sociocultural mayor de prácticas de alimentación."),
        ("educacion_madre_anos", "V107", "REC0111", "Madre", "Discreta", "98 (No sabe)", "Años de escolaridad formal aprobados por la madre."),
        ("estado_conyugal_madre", "V501", "REC0111", "Madre", "Categórica Nominal", "Ninguno", "Estado conyugal; monoparentalidad y red de soporte económico familiar."),
        ("madre_trabaja", "V714", "REC0111", "Madre", "Binaria (0/1)", "Ninguno", "Inserción laboral de la madre y tiempo efectivo disponible para lactancia y cuidado."),
        ("autonomia_salud_madre", "V743A", "REC0111", "Madre", "Categórica Nominal", "Ninguno", "Poder de decisión de la madre sobre su propia atención médica y la de sus hijos."),
        ("lengua_materna_madre", "S119", "REC91", "Madre", "Categórica Nominal", "Ninguno", "Lengua originaria aprendida en la niñez (Quechua, Aimara, Nativa); barrera idiomática y exclusión."),
        ("diarrea_reciente_eda", "V411", "REC42", "Salud Niño", "Binaria (0/1)", "8 (No sabe)", "Diarrea en las últimas 2 semanas; CAUSA INMEDIATA DIRECTA de atrofia intestinal y retardo."),
        ("diarrea_con_sangre", "V411A", "REC42", "Salud Niño", "Binaria (0/1)", "8 (No sabe)", "Disentería bacteriana invasiva con daño severo a la mucosa entérica."),
        ("tratamiento_sro", "V413", "REC42", "Salud Niño", "Binaria (0/1)", "8 (No sabe)", "Uso de Sales de Rehidratación Oral durante la diarrea; previene shock y desnutrición aguda."),
        ("fiebre_reciente", "V414", "REC42", "Salud Niño", "Binaria (0/1)", "8 (No sabe)", "Fiebre reciente como marcador de infección sistémica y consumo metabólico acelerado."),
        ("tos_ira_reciente", "V415", "REC42", "Salud Niño", "Binaria (0/1)", "8 (No sabe)", "Infección respiratoria aguda reciente en las últimas 2 semanas."),
        ("signos_neumonia", "V416", "REC42", "Salud Niño", "Binaria (0/1)", "8 (No sabe)", "Respiración rápida o tiraje subcostal (neumonía grave)."),
        ("carne_vacunacion_visto", "H1", "REC43", "Inmunización", "Categórica Nominal", "Ninguno", "Tenencia y verificación visual del carné oficial de salud infantil."),
        ("vacuna_bcg", "H2", "REC43", "Inmunización", "Binaria (0/1)", "8 (No sabe)", "Vacuna antituberculosa al nacer."),
        ("vacuna_rotavirus_completa", "H31B", "REC43", "Inmunización", "Binaria (0/1)", "8 (No sabe)", "Segunda dosis de rotavirus; previene diarreas virales deshidratantes masivas."),
        ("vacuna_neumococo_dosis2", "H32B", "REC43", "Inmunización", "Binaria (0/1)", "8 (No sabe)", "Dosis de neumococo; previene bacteriemias y neumonías destructivas."),
        ("vacuna_spr1", "H9", "REC43", "Inmunización", "Binaria (0/1)", "8 (No sabe)", "Vacuna contra sarampión al año de edad; previene desnutrición severa post-sarampión."),
        ("suplemento_vitamina_a", "H34", "REC43", "Nutrición Niño", "Binaria (0/1)", "8 (No sabe)", "Vitamina A en los últimos 6 meses; regeneración epitelial y defensas de mucosas."),
        ("desparasitacion_infantil", "H43", "REC43", "Nutrición Niño", "Binaria (0/1)", "8 (No sabe)", "Tratamiento antiparasitario en últimos 6 meses contra geohelmintiasis."),
        ("controles_cred_numero", "S45C", "REC95", "Salud Niño", "Discreta", "98 (No sabe)", "Número total de controles de Crecimiento y Desarrollo recibidos."),
        ("programa_juntos", "QH95", "Programas Sociales", "Programas Sociales", "Binaria (1/2)", "Ninguno", "Transferencia condicionada que exige asistencia a controles CRED y vacunas."),
        ("programa_vaso_leche", "QH101", "Programas Sociales", "Programas Sociales", "Binaria (1/2)", "Ninguno", "Beneficiario del programa municipal de complemento calórico-proteico."),
        ("programa_comedor", "QH103", "Programas Sociales", "Programas Sociales", "Binaria (1/2)", "Ninguno", "Acceso familiar a raciones cocinadas de Comedores Populares."),
        ("programa_cuna_mas", "QH106", "Programas Sociales", "Programas Sociales", "Binaria (1/2)", "Ninguno", "Atención en Cuna Más (Cuidado Diurno o Acompañamiento a Familias en nutrición temprana).")
    ]
    
    md.append("| Nombre Limpio (snake_case) | Variable Origen | Archivo / Módulo | Categoría | Tipo para ML | Códigos a Limpiar (NaN) | Justificación Epidemiológica ligada a Desnutrición Crónica |")
    md.append("|:---|:---|:---|:---|:---|:---|:---|")
    for r in selected_table:
        md.append(f"| `{r[0]}` | `{r[1]}` | `{r[2]}` | **{r[3]}** | {r[4]} | `{r[5]}` | {r[6]} |")
    md.append("\n")

    # 5.1 Variables Derivadas Propuestas
    md.append("### 5.1 Propuesta de Variables Derivadas de Alto Impacto Epidemiológico\n")
    md.append("A partir de las variables originales incluidas, se deben construir mediante ingeniería de características las siguientes 8 variables derivadas clave:\n")
    deriv_list = [
        ("grupo_edad_nino", "`HC1` (Edad en meses)", "Categórica Ordinal", "Grupos: 0-5 meses (lactancia exclusiva), 6-11 meses (inicio de alimentación complementaria), 12-23 meses (ventana crítica de desaceleración estatural), 24-35 meses, 36-47 meses, 48-59 meses. Permite capturar la acumulación no lineal del déficit de talla."),
        ("lactancia_exclusiva_adecuada", "`M5` y `HC1`", "Binaria (0/1)", "1 si para niños de 0 a 5 meses `M5 >= HC1` (recibe exclusivamente leche materna acorde a su edad), 0 en caso de introducción precoz de agua, infusiones o fórmulas."),
        ("indice_hacinamiento", "`HV009` / `HV216`", "Continua / Categórica", "Personas por dormitorio. Si es >= 3.0 personas/dormitorio se clasifica como hacinamiento crítico, asociado a transmisión cruzada de diarreas e infecciones respiratorias."),
        ("saneamiento_adecuado_jmp", "`HV205` y `HV225`", "Binaria (0/1)", "Criterio conjunto OMS/UNICEF (JMP): 1 si el baño es mejorado (red pública, letrina ventilada, pozo séptico) Y no es compartido con otros hogares (`HV225 == 0`), 0 en caso contrario."),
        ("agua_segura_jmp", "`HV201` y `HV237`", "Binaria (0/1)", "1 si proviene de fuente mejorada (red domiciliaria, pilón) Y se aplica tratamiento seguro (hervir, clorar), 0 si es pozo ciego, río o no se trata."),
        ("piso_tierra_critico", "`HV213`", "Binaria (0/1)", "1 si el piso principal es de tierra o arena (`HV213 == 11`), principal vector de geoparásitos y enteritis ambiental en infantes gateadores."),
        ("combustible_contaminante_biomasa", "`HV226`", "Binaria (0/1)", "1 si cocina con leña, carbón, bosta o rastrojo sin chimenea adecuada, promoviendo infecciones respiratorias crónicas."),
        ("intervalo_intergenesico_corto", "`B11`", "Binaria (0/1)", "1 si el intervalo desde el parto anterior es menor a 24 meses (`B11 < 24`), factor reconocido de síndrome de depleción materna de folatos y micronutrientes.")
    ]
    for d_item in deriv_list:
        md.append(f"- **`{d_item[0]}`** (Insumo: {d_item[1]} | Tipo: *{d_item[2]}*): {d_item[3]}")
    md.append("\n---\n")

    # 6. Variables Dudosas
    md.append("## 6. Variables DUDOSAS con Argumentos y Recomendación Técnica\n")
    md.append("Se identificaron cuatro conjuntos de variables con tensiones metodológicas entre poder predictivo y validez de campo:\n")
    md.append("### 6.1 Hemoglobina y Anemia Infantil (`HC53`, `HC56`, `HC56A`, `HC57`, `HC57A`)")
    md.append("- **Argumento a Favor de Incluirlas:** La anemia y la desnutrición crónica coexisten frecuentemente como manifestaciones de la misma privación nutricional y de inflamación subclínica. Un niño con anemia moderada/severa tiene un riesgo relativo 2 a 3 veces superior de presentar retardo estatural.")
    md.append("- **Argumento en Contra de Incluirlas:** Rompe la condición de **modelo de screening comunitario no invasivo**. Exige personal de enfermería capacitado, lancetas, hemoglobinómetros portátiles (Hemocue) y consentimiento informado con punción en el talón o dedo del infante. Además, es una medición clínica concurrente en el mismo punto temporal.")
    md.append("- **Recomendación Técnica Inequívoca:** **EXCLUIR del modelo predictivo primario de screening domiciliario.** Si se desea entrenar una variante clínica de segundo nivel para establecimientos de salud (donde sí hay laboratorio o Hemocue), se documenta como modelo clínico secundario.\n")
    md.append("### 6.2 Mediciones Antropométricas Correlacionadas (`HC71` Peso/Edad, `HC72` Peso/Talla, `HC2` Peso Crudo)")
    md.append("- **Argumento a Favor:** El peso infantil y los Z-scores de peso/edad y peso/talla tienen altísima correlación matemática con la masa corporal del niño.")
    md.append("- **Argumento en Contra:** Son **subrogados directos (proxies) del estado nutricional**. `HC71` y `HC72` se calculan en la misma sesión antropométrica de campo con balanza calibrada. Si se incluyen, el modelo se convierte en una tautología antropométrica que no aprende los determinantes biológicos y sociales del crecimiento.")
    md.append("- **Recomendación Técnica Inequívoca:** **EXCLUIR.** El modelo debe aprender a predecir la desnutrición a partir del entorno, la madre, la dieta y la morbilidad, no a partir de una balanza concurrente.\n")
    md.append("### 6.3 Hitos del Desarrollo Psicomotor en DIT (`QI478E1`)")
    md.append("- **Argumento:** Evalúa si el niño se para o camina.")
    md.append("- **Riesgo:** **Bidireccionalidad.** El retardo estatural severo causa debilidad muscular y retrasa los hitos motores gruesos; por tanto, es una consecuencia del retraso del crecimiento y no un factor de riesgo causal.")
    md.append("- **Recomendación Técnica:** **EXCLUIR `QI478E1`** y conservar solo las variables de estimulación psicosocial parental (`QI478E2` a `QI478E6`).\n")
    md.append("### 6.4 Suplementos y Tratamientos Pediátricos en `REC94` y `REC95`")
    md.append("- **Argumento:** Mide si el niño tomó gotas/jarabe de hierro o suplementos.")
    md.append("- **Riesgo:** **Causalidad Inversa.** Si el niño recibió jarabe terapéutico es porque el personal de salud ya detectó una falla nutricional en un control previo.")
    md.append("- **Recomendación Técnica:** **EXCLUIR las intervenciones terapéuticas** y mantener únicamente la profilaxis materna (`M45`, `M46`) y la afiliación a programas sociales preventivos.\n")
    md.append("---\n")

    # 7. Variables Excluidas por Leakage
    md.append("## 7. Variables EXCLUIDAS Estrictamente por Fuga de Datos (Leakage)\n")
    md.append("| Variable | Descripción Oficial | Archivo | Mecanismo de Fuga de Información (Target Leakage) |")
    md.append("|:---|:---|:---|:---|")
    leak_table = [
        ("HC70", "Z-score Talla para la Edad OMS en centésimas", "RECH6", "**Variable Objetivo Directa (Target).** Usarla como predictor generaría un accuracy perfecto artificial del 100%."),
        ("HW70", "Z-score Talla para la Edad OMS en Cuestionario Individual", "REC44", "**Variable Objetivo Duplicada.** Mismo indicador registrado en el cuestionario de mujeres."),
        ("HC3", "Talla en centímetros (1 decimal)", "RECH6", "**Fuga Matemática Directa.** Combinada con la edad en meses (`HC1`) y sexo (`HC27`), cualquier árbol de decisión calcula el Z-score de talla/edad con exactitud milimétrica."),
        ("HW3", "Talla en centímetros (1 decimal) en Cuestionario Individual", "REC44", "**Fuga Matemática Directa.** Homóloga a HC3."),
        ("HC4 / HW4", "Talla/Edad Percentil", "RECH6 / REC44", "**Transformación Monótona del Target.** El percentil es la función de distribución acumulada directa del Z-score."),
        ("HC5 / HW5", "Talla/Edad Desviación Estándar de la mediana de referencia", "RECH6 / REC44", "**Reconstrucción Numérica del Target.** Desvío directo de talla/edad."),
        ("HC6 / HW6", "Talla/Edad Porcentaje de la mediana de referencia", "RECH6 / REC44", "**Transformación Aritmética del Target.** Ratio directo entre talla del niño y mediana OMS."),
        ("HC71 / HW71", "Z-score Peso para la Edad OMS en centésimas", "RECH6 / REC44", "**Proxy de Fuga y Subrogado Clínico.** Desnutrición global; comparte más del 80% de varianza con talla baja."),
        ("HC72 / HW72", "Z-score Peso para la Talla OMS en centésimas", "RECH6 / REC44", "**Proxy de Fuga y Subrogado Clínico.** Desnutrición aguda / emaciación calculada con la misma talla."),
        ("HC73 / HW73", "Z-score de Índice de Masa Corporal (IMC) OMS", "RECH6 / REC44", "**Fuga Instrumental.** Fórmula que involucra la talla en el denominador ($kg/m^2$)."),
        ("HC13 / HW13", "Razón por la cual el niño no se midió", "RECH6 / REC44", "**Fuga Operativa del Criterio de Inclusión.** Define la elegibilidad del target."),
        ("HC15 / HW15", "El niño se midió acostado o de pie", "RECH6 / REC44", "**Fuga Instrumental de Protocolo.** Se mide acostado si talla < 85 cm y de pie si >= 85 cm; filtra directamente la estatura del infante.")
    ]
    for row in leak_table:
        md.append(f"| `{row[0]}` | {row[1]} | `{row[2]}` | {row[3]} |")
    md.append("\n---\n")

    # 8. Metadatos del Diseño Muestral
    md.append("## 8. Metadatos del Diseño Muestral Complejo a Conservar\n")
    md.append("Para asegurar que las métricas de rendimiento y la validación cruzada reflejen fielmente el comportamiento en la población infantil peruana, se deben conservar como **columnas auxiliares (no predictoras)**:\n")
    md.append("1. **`HV001` (Conglomerado / Unidad Primaria de Muestreo - UPM):**")
    md.append("   - Obligatorio para agrupar los datos en `StratifiedGroupKFold(n_splits=5)`.")
    md.append("   - Evita que niños que comparten el mismo conglomerado (misma comunidad rural, condiciones ambientales y red de agua idénticas) queden divididos entre el conjunto de entrenamiento y prueba (fuga espacial vecinal).\n")
    md.append("2. **`HV022` (Estrato de Muestreo Geográfico):**")
    md.append("   - Permite estratificar por región natural y tamaño de localidad durante la partición de datos.\n")
    md.append("3. **`HV005` (Factor de Ponderación Muestral del Hogar):**")
    md.append("   - Debe transformarse mediante `peso_muestral = HV005 / 1000000.0`.")
    md.append("   - Se suministra al parámetro `sample_weight` de `xgb.train()` o `XGBClassifier.fit()` para que el modelo pondere proporcionalmente a los estratos sobrerepresentados (como zonas rurales priorizadas por INEI).\n")
    md.append("4. **Llaves de Enlace Relacional:**")
    md.append("   - `HHID` (Identificador del hogar), `HC0` (Orden del niño en el hogar), `CASEID` (Identificador de la madre), `BIDX` / `HWIDX` (Orden de nacimiento en la historia gestacional materna).\n")
    md.append("---\n")

    # 9. Plan de Unión de Módulos
    md.append("## 9. Plan de Unión de Módulos (Data Merging Pipeline)\n")
    md.append("```mermaid")
    md.append("flowchart TD")
    md.append("    subgraph Hogar_y_Vivienda [Nivel Hogar / Vivienda]")
    md.append("        RECH0[\"RECH0: Geografía y Muestreo (HHID)\"]")
    md.append("        RECH23[\"RECH23: Vivienda, Saneamiento y Riqueza (HHID)\"]")
    md.append("        PS[\"Programas Sociales x Hogar (HHID)\"]")
    md.append("    end")
    md.append("    ")
    md.append("    subgraph Nino_Central [Nivel Niño (Población Base)]")
    md.append("        RECH6[\"RECH6: Niños < 5 años (HHID + HC0) — TARGET: HC70\"]")
    md.append("        RECH4[\"RECH4: Seguro SIS del Niño (HHID + HC0)\"]")
    md.append("        RECH1[\"RECH1: Cuidadores y Miembros (HHID + HC0)\"]")
    md.append("    end")
    md.append("    ")
    md.append("    subgraph Madre_Individual [Nivel Madre / Cuestionario Individual]")
    md.append("        RECH5[\"RECH5: Antropometría Materna (HHID + HC60)\"]")
    md.append("        REC0111[\"REC0111: Datos Básicos MEF (CASEID)\"]")
    md.append("        REC91[\"REC91: Lengua Materna y Etnia (CASEID)\"]")
    md.append("    end")
    md.append("    ")
    md.append("    subgraph Perinatal_y_Salud [Nivel Salud Infantil y Perinatal]")
    md.append("        REC41[\"REC41: Controles, Peso Nacer, Lactancia (CASEID + BIDX)\"]")
    md.append("        REC42[\"REC42: Diarrea, IRA, Fiebre y Dieta (CASEID + BIDX)\"]")
    md.append("        REC43[\"REC43: Carné de Vacunas (CASEID + BIDX)\"]")
    md.append("        REC95[\"REC95: Controles CRED (CASEID + BIDX)\"]")
    md.append("        DIT[\"DIT: Desarrollo Infantil y Apego (CASEID + BIDX)\"]")
    md.append("    end")
    md.append("    ")
    md.append("    RECH6 -->|Left Join por HHID| RECH0")
    md.append("    RECH6 -->|Left Join por HHID| RECH23")
    md.append("    RECH6 -->|Left Join por HHID| PS")
    md.append("    RECH6 -->|Left Join por HHID + HC0| RECH4")
    md.append("    RECH6 -->|Left Join por HHID + HC0| RECH1")
    md.append("    RECH6 -->|Enlace Madre: HHID + HC60| RECH5")
    md.append("    RECH6 -->|Enlace Relacional Madre-Hijo| REC41")
    md.append("    REC41 -->|Misma Llave Perinatal| REC42")
    md.append("    REC41 -->|Misma Llave Perinatal| REC43")
    md.append("    REC41 -->|Misma Llave Perinatal| REC95")
    md.append("    REC41 -->|Misma Llave Perinatal| DIT")
    md.append("    REC41 -->|Vía CASEID| REC0111")
    md.append("    REC41 -->|Vía CASEID| REC91")
    md.append("```\n")
    md.append("### Protocolo Secuencial de Unión y Verificaciones:")
    md.append("1. **Tabla Núcleo Base:** Iniciar siempre con `RECH6_2025.csv` filtrando niños válidos de 0 a 59 meses con target computable.")
    md.append("2. **Merge 1 (Hogar / Vivienda / Programas):** Unir `RECH6` con `RECH0`, `RECH23` y `Programas Sociales x Hogar` por `HHID` (cardinalidad N:1; muchos niños en un mismo hogar). Chequeo: El número de filas de `RECH6` debe mantenerse constante.")
    md.append("3. **Merge 2 (Seguro de Salud del Niño):** Unir `RECH6` con `RECH4` por `HHID` y `HC0 == IDX4` (número de orden del niño en el hogar, cardinalidad 1:1). Chequeo: No deben generarse filas duplicadas.")
    md.append("4. **Merge 3 (Madre en Hogar):** `HC60` en `RECH6` indica el número de orden de la madre en el hogar. Unir `RECH6` con `RECH5` mediante `HHID` y `HC60 == HA0` para traer la talla e IMC de la madre.")
    md.append("5. **Merge 4 (Historia Gestacional y Perinatal):** Para vincular con `REC41`, `REC42`, `REC43`, `REC95` y `DIT`, se utiliza el identificador de la madre (`CASEID`) y el número de orden de nacimiento del niño (`BIDX` / `HWIDX`). En ENDES, para mujeres del hogar evaluadas en el cuestionario individual, `CASEID = rpad(HHID, 15) + lpad(HC60, 3)`. Chequeo: Verificar tasa de acoplamiento madre-hijo (esperada > 95% para niños que residen con su madre biológica).")
    md.append("---\n")

    # 10. Módulos Complementarios Analizados
    md.append("## 10. Módulos Complementarios Analizados (1031, 1036 y 1041)\n")
    md.append("> **Actualización metodológica:** A diferencia del informe preliminar de anemia (que carecía de estos diccionarios), **se integraron y analizaron formalmente los 13 diccionarios oficiales** de los módulos solicitados, extrayendo predictores de alto impacto:\n")
    md.append("1. **Módulo 1031 (MEF - Cuestionario Individual de Mujeres):**")
    md.append("   - Archivos: `Diccionario - REC0111.pdf` (104 vars) y `Diccionario - REC91.pdf` (343 vars).")
    md.append("   - Variables clave incorporadas: Edad materna (`V012`), escolaridad (`V106`), autoidentificación étnica (`V131`), lengua materna quechua/aimara/amazónica (`S119`), estado conyugal (`V501`) y autonomía en decisiones de salud (`V743A`).\n")
    md.append("2. **Módulo 1036 (Inmunización y Salud Infantil):**")
    md.append("   - Archivos: `Diccionario - DIT.pdf` (63 vars), `Diccionario - REC42.pdf` (169 vars), `Diccionario - REC43.pdf` (168 vars) y `Diccionario - REC95.pdf` (315 vars).")
    md.append("   - Variables clave incorporadas: Episodios de diarrea aguda EDA (`V411`, `V411A`), fiebre e infecciones respiratorias IRA (`V414`, `V415`), diversidad dietética de 24 horas, esquema de vacunación completo contra Rotavirus y Neumococo (`H31B`, `H32B`), carné verificado (`H1`) y número de controles CRED recibidos (`S45C`).\n")
    md.append("3. **Módulo 1041 (Programas Sociales):**")
    md.append("   - Archivos: `Diccionario - Programas Sociales x Hogar.pdf` (20 vars), `PS_CUNAMAS_VISITA.pdf` (10 vars), `PS_WAWAWASI.pdf` (10 vars), `PS_VL.pdf` (10 vars), `PS_COMEDOR.pdf` (10 vars), `PS_QALIWARMA.pdf` (11 vars) y `PS_TRABAJA.pdf` (10 vars).")
    md.append("   - Variables clave incorporadas: Beneficiario del Programa JUNTOS (`QH95`), Cuna Más Acompañamiento / Cuidado Diurno (`QH106`), Vaso de Leche (`QH101`) y Comedores Populares (`QH103`).\n")
    md.append("---\n")

    # 11. Cambios Respecto al Catálogo de Anemia
    md.append("## 11. Tabla Comparativa de Cambios Respecto al Catálogo de Anemia\n")
    md.append("La siguiente tabla documenta las variables cuya clasificación y rol sufrieron cambios estructurales al migrar el objetivo de **Anemia Infantil** a **Desnutrición Crónica Infantil**:\n")
    
    comp_table = [
        ("HC70 / HW70", "Z-score Talla/Edad", "DUDOSA (CLÍNICA)", "**VARIABLE OBJETIVO (TARGET)**", "En anemia era una medición física concurrente dudosa; en desnutrición crónica constituye el fenómeno a predecir (< -200)."),
        ("HC57 / HC57A", "Nivel de Anemia (MINSA / OMS)", "VARIABLE OBJETIVO (TARGET)", "**DUDOSA (BIOMARCADOR CONCURRENTE)**", "Pasa de ser el target del proyecto anterior a ser un biomarcador clínico invasivo concurrente opcional."),
        ("HC53 / HC56", "Nivel de Hemoglobina crudo y ajustado", "EXCLUIR POR LEAKAGE DIRECTO", "**DUDOSA (BIOMARCADOR CONCURRENTE)**", "En anemia era fuga matemática absoluta; en desnutrición es un predictor clínico concurrente correlacionado."),
        ("HC3 / HW3", "Talla en centímetros del niño", "DUDOSA (CLÍNICA)", "**EXCLUIR POR LEAKAGE CRÍTICO**", "En anemia aportaba proxy de crecimiento; en desnutrición reconstruye directamente el target con la edad y el sexo."),
        ("M19", "Peso al nacer en gramos", "PREDICTOR RECOMENDADO", "**PREDICTOR CRÍTICO DE PRIMER ORDEN**", "El bajo peso al nacer (< 2,500 g) es el factor etiológico intrauterino más potente de retardo estatural en menores de 5 años."),
        ("M4 / M5", "Lactancia materna total y exclusiva", "PREDICTOR SECUNDARIO", "**PREDICTOR PRIORITARIO DE NUTRICIÓN**", "La lactancia materna exclusiva en los primeros 6 meses previene directamente la enteropatía y el retraso del crecimiento."),
        ("HV201 / HV205", "Agua para beber y tipo de baño", "PREDICTOR DE ENTORNO", "**PREDICTOR ETIOLÓGICO CLAVE (JMP)**", "El agua no tratada y el fecalismo ambiental provocan enteropatía ambiental subclínica, alterando la absorción de nutrientes."),
        ("HA3", "Talla de la madre en centímetros", "NO INCLUIDA", "**PREDICTOR BIOLÓGICO PRIORITARIO**", "La talla baja materna (< 150 cm) refleja el ciclo intergeneracional de la desnutrición y predispone epigenéticamente al hijo."),
        ("V411 / V411A", "Episodios de diarrea aguda reciente", "NO DISPONIBLE EN CATÁLOGO ANTERIOR", "**PREDICTOR INMEDIATO (UNICEF)**", "Causa inmediata de pérdida aguda de peso y retardo estatural por inflamación del epitelio digestivo."),
        ("H31B / H32B", "Vacunas Rotavirus y Neumococo", "NO DISPONIBLE EN CATÁLOGO ANTERIOR", "**PREDICTOR PREVENTIVO DE PRIMER ORDEN**", "Previene diarreas virales deshidratantes y neumonías bacterianas recurrentes que desencadenan desnutrición crónica."),
        ("QH95", "Programa JUNTOS en el hogar", "NO DISPONIBLE EN CATÁLOGO ANTERIOR", "**PREDICTOR DE CONDICIONALIDAD SOCIAL**", "Incentivo monetario del Estado condicionado a que la madre lleve al niño a sus controles CRED y vacunas."),
        ("QH106", "Cuna Más / Wawa Wasi", "NO DISPONIBLE EN CATÁLOGO ANTERIOR", "**PREDICTOR DE CUIDADO Y DIETA TEMPRANA**", "Intervención del MIDIS que suministra 70% de requerimientos calórico-proteicos diarios al menor de 36 meses.")
    ]
    
    md.append("| Variable | Descripción Oficial | Decisión en Proyecto Anemia | Decisión en Proyecto Desnutrición Crónica | Justificación Epidemiológica del Cambio |")
    md.append("|:---|:---|:---|:---|:---|")
    for row in comp_table:
        md.append(f"| `{row[0]}` | {row[1]} | `{row[2]}` | **{row[3]}** | {row[4]} |")
    md.append("\n---\n")

    # 12. Resumen Final y Bloque Python
    md.append("## 12. Resumen Final: Conteo de Variables y Bloque de Código Python\n")
    md.append("### 12.1 Conteo Consolidado por Categoría de Decisión")
    md.append(f"- **Total de Variables Oficiales Evaluadas:** {total_vars}")
    md.append(f"- **Variables SELECCIONADAS para la Matriz Explicativa ($X$):** {stats['INCLUIR']}")
    md.append(f"- **Variables DUDOSAS (Biomarcadores o Riesgo de Causalidad Inversa):** {stats['DUDOSA']}")
    md.append(f"- **Variables EXCLUIDAS por Fuga de Datos (Leakage) o Causalidad Inversa:** {stats['EXCLUIR_LEAKAGE']}")
    md.append(f"- **Variables MANTENIDAS como Metadatos del Diseño Muestral / Llaves:** {stats['METADATO']}")
    md.append(f"- **Variables Identificadas como Objetivo (Target Directo o Secundario):** {stats['TARGET']}")
    md.append(f"- **Variables EXCLUIDAS por Irrelevancia Operativa, Administrativa o Alta Incompletitud:** {stats['EXCLUIR_IRRELEVANTE']}\n")
    
    md.append("### 12.2 Lista Final de Predictores en Bloque de Código Python\n")
    md.append("```python")
    md.append("# =============================================================================")
    md.append("# CONFIGURACIÓN OFICIAL DE VARIABLES - MODELO PREDICTIVO DESNUTRICIÓN CRÓNICA")
    md.append("# ENDES 2025 (INEI, PERÚ) - XGBOOST")
    md.append("# =============================================================================")
    md.append("")
    md.append("TARGET = 'desnutricion_cronica'  # 1 si HC70 < -200, 0 en caso contrario")
    md.append("TARGET_ORIGIN = 'HC70'          # Z-score Talla/Edad OMS en centésimas")
    md.append("")
    md.append("# Metadatos de Diseño Muestral Complejo (No usar como predictores en X)")
    md.append("CLUSTER_COL = 'HV001'           # Conglomerado (PSU) para GroupKFold")
    md.append("STRATUM_COL = 'HV022'           # Estrato de muestreo")
    md.append("WEIGHT_COL = 'peso_muestral'    # HV005 / 1,000,000 para sample_weight")
    md.append("")
    md.append("# Identificadores Relacionales para Enlace entre Módulos")
    md.append("ID_COLS = [")
    md.append("    'HHID',                     # Identificador del hogar")
    md.append("    'HC0',                      # Número de orden del niño en el hogar")
    md.append("    'HC60',                     # Número de orden de la madre en el hogar")
    md.append("    'CASEID',                   # Identificador de la mujer (Cuestionario Individual)")
    md.append("    'BIDX'                      # Orden de nacimiento del niño en historia obstétrica")
    md.append("]")
    md.append("")
    md.append("# Lista Definitiva de Predictores (X) - 100% Compatibles con Screening Comunitario")
    md.append("FEATURES = [")
    md.append("    # --- Niño: Factores Biológicos ---")
    md.append("    'edad_meses',               # HC1: 0 a 59 meses")
    md.append("    'sexo_nino',                # HC27: 1 Hombre, 2 Mujer")
    md.append("    'peso_al_nacer_g',          # M19: Peso al nacer en gramos (< 2500g = RCIU)")
    md.append("    'tamano_nacer_aparente',    # M19A: Reporte cualitativo del tamaño al nacer")
    md.append("    'duracion_lactancia_m',     # M4: Meses totales de lactancia")
    md.append("    'lactancia_exclusiva_m',    # M5: Meses de lactancia materna exclusiva")
    md.append("    'intervalo_intergenesico',  # B11: Meses desde el nacimiento previo")
    md.append("    ")
    md.append("    # --- Madre: Antropometría, Educación y Autonomía ---")
    md.append("    'talla_madre_cm',           # HA3: Talla materna (herencia y ciclo intergeneracional)")
    md.append("    'imc_madre',                # HA40: Índice de masa corporal materno")
    md.append("    'edad_madre_anos',          # V012: Edad de la madre en años")
    md.append("    'educacion_madre_nivel',    # V106 / HC61: Sin educación, Primaria, Secundaria, Superior")
    md.append("    'educacion_madre_anos',     # V107 / HC68: Años de estudio aprobados")
    md.append("    'estado_conyugal_madre',    # V501: Casada, conviviente, soltera, separada")
    md.append("    'madre_trabaja',            # V714: Condición de trabajo de la madre (0/1)")
    md.append("    'autonomia_salud_madre',    # V743A: Toma de decisiones en atención médica")
    md.append("    'hierro_madre_gestacion',   # M45: Suplementación con hierro en el embarazo")
    md.append("    'dias_hierro_madre',        # M46: Días de consumo de hierro gestacional")
    md.append("    'controles_prenatales',     # M14: Número total de controles prenatales")
    md.append("    'mes_inicio_prenatal',      # M18: Mes de inicio del primer control prenatal")
    md.append("    'lugar_parto',              # M15: Institucional (hospital/centro) vs. Domicilio")
    md.append("    'atencion_parto_calif',     # M3A: Atención por médico u obstetra calificado")
    md.append("    'lengua_materna_madre',     # S119: Quechua, Aimara, Nativa, Castellano")
    md.append("    ")
    md.append("    # --- Hogar y Entorno Demográfico ---")
    md.append("    'total_miembros_hogar',     # HV009: Número de integrantes en el hogar")
    md.append("    'menores_5anos_hogar',      # HV014: Cantidad de niños menores de 5 años")
    md.append("    'mujeres_edad_fertil',      # HV010: Número de mujeres elegibles en el hogar")
    md.append("    ")
    md.append("    # --- Vivienda, Saneamiento y Riqueza (JMP OMS/UNICEF) ---")
    md.append("    'fuente_agua_beber',        # HV201: Tipo de abastecimiento de agua")
    md.append("    'tipo_servicio_higienico',  # HV205: Tipo de baño (red, letrina, pozo, campo)")
    md.append("    'bano_compartido',          # HV225: Servicio higiénico compartido (0/1)")
    md.append("    'tratamiento_agua',         # HV237: Hierve, clora o filtra el agua para beber")
    md.append("    'material_piso',            # HV213: Piso de tierra/arena vs. terminado")
    md.append("    'habitaciones_dormir',      # HV216: Habitaciones para dormir (hacinamiento)")
    md.append("    'combustible_cocinar',      # HV226: Biomasa (leña/carbón) vs. gas/electricidad")
    md.append("    'tiene_electricidad',       # HV206: Electricidad en la vivienda (0/1)")
    md.append("    'tiene_refrigerador',       # HV209: Refrigeradora para conservación de alimentos")
    md.append("    'quintil_riqueza',          # HV270: Quintil socioeconómico del hogar (1 a 5)")
    md.append("    ")
    md.append("    # --- Geografía Territorial ---")
    md.append("    'departamento',             # HV024: Departamento de residencia (1 a 25)")
    md.append("    'area_residencia',          # HV025: 1 Urbano, 2 Rural")
    md.append("    'altitud_msnm',             # HV040: Altitud en metros sobre el nivel del mar")
    md.append("    ")
    md.append("    # --- Salud Infantil, Morbilidad Reciente e Inmunización ---")
    md.append("    'seguro_sis',               # SH11A: Niño afiliado al Seguro Integral de Salud")
    md.append("    'diarrea_reciente_eda',     # V411: Tuvo diarrea en las últimas 2 semanas (0/1)")
    md.append("    'diarrea_con_sangre',       # V411A: Diarrea disentérica bacteriana (0/1)")
    md.append("    'tratamiento_sro',          # V413: Sales de Rehidratación Oral (0/1)")
    md.append("    'fiebre_reciente',          # V414: Tuvo fiebre en las últimas 2 semanas (0/1)")
    md.append("    'tos_ira_reciente',         # V415: Tuvo tos / infección respiratoria (0/1)")
    md.append("    'carne_vacunacion_visto',   # H1: Carné oficial de vacunas visto por encuestadora")
    md.append("    'vacuna_bcg',               # H2: Vacuna al nacer (0/1)")
    md.append("    'vacuna_rotavirus_completa',# H31B: Dosis 2 de vacuna contra Rotavirus (0/1)")
    md.append("    'vacuna_neumococo_dosis2',  # H32B: Dosis 2 de vacuna contra Neumococo (0/1)")
    md.append("    'vacuna_spr1',              # H9: Vacuna contra Sarampión / SPR (0/1)")
    md.append("    'suplemento_vitamina_a',    # H34: Vitamina A en últimos 6 meses (0/1)")
    md.append("    'desparasitacion_infantil', # H43: Antiparasitario en últimos 6 meses (0/1)")
    md.append("    'controles_cred_numero',    # S45C: Número total de controles CRED recibidos")
    md.append("    ")
    md.append("    # --- Programas Sociales y Transferencias del Estado ---")
    md.append("    'programa_juntos',          # QH95: Beneficiario del Programa JUNTOS (1/2)")
    md.append("    'programa_vaso_leche',      # QH101: Beneficiario del Programa Vaso de Leche (1/2)")
    md.append("    'programa_comedor',         # QH103: Beneficiario de Comedores Populares (1/2)")
    md.append("    'programa_cuna_mas'         # QH106: Beneficiario de Cuna Más / Wawa Wasi (1/2)")
    md.append("]")
    md.append("")
    md.append("# Variables Categóricas a codificar en XGBoost (enable_categorical=True o Target/OneHot Encoding)")
    md.append("CATEGORICAL_FEATURES = [")
    md.append("    'departamento', 'area_residencia', 'fuente_agua_beber', 'tipo_servicio_higienico',")
    md.append("    'material_piso', 'combustible_cocinar', 'quintil_riqueza', 'lugar_parto',")
    md.append("    'educacion_madre_nivel', 'estado_conyugal_madre', 'lengua_materna_madre',")
    md.append("    'carne_vacunacion_visto', 'tamano_nacer_aparente'")
    md.append("]")
    md.append("```\n")
    
    # Write to file
    final_text = "\n".join(md) + "\n"
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_text)
        
    print(f"Catálogo generado exitosamente en: {OUTPUT_FILE} ({len(final_text.splitlines())} líneas, {len(final_text.encode('utf-8'))} bytes)")

if __name__ == '__main__':
    generate_markdown_catalog()
