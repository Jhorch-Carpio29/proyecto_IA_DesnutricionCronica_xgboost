#!/usr/bin/env python3
"""
Generador completo del Catálogo Exhaustivo de Variables para Desnutrición Crónica Infantil
ENDES 2025 (INEI, Perú) - Modelo Predictivo XGBoost.
"""

import os
import re

DICT_FILE = "reports/diccionarios_completos_endes2025.md"
OUTPUT_FILE = "reports/catalogo_variables_desnutricion_cronica_endes2025.md"

def load_dict_variables():
    with open(DICT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = re.findall(r'# DICCIONARIO DE VARIABLES .*?\((.*?)\)(.*?)(?=# DICCIONARIO|\Z)', content, re.DOTALL)
    dict_vars = {}
    for code, body in sections:
        code = code.strip()
        dict_vars[code] = []
        for line in body.strip().splitlines():
            if line.startswith('|') and not line.startswith('| Nº') and not line.startswith('|:--'):
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 3 and parts[0] != '':
                    dict_vars[code].append({
                        'num': parts[0],
                        'var': parts[1],
                        'desc': parts[2],
                        'tipo': parts[3] if len(parts) > 3 else '',
                        'longitud': parts[4] if len(parts) > 4 else '',
                        'rango': parts[5] if len(parts) > 5 else '',
                        'valores': parts[6] if len(parts) > 6 else '',
                        'desc_alt': parts[7] if len(parts) > 7 else '',
                        'obs': parts[8] if len(parts) > 8 else ''
                    })
    return dict_vars

def classify_variable(dict_name, var_info):
    v = var_info['var'].upper().strip()
    d = var_info['desc'].strip()
    
    # 1. RECH6 (Niños - Antropometría y Hemoglobina)
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

    # 2. REC44 (Niños Cuestionario Individual)
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

    # 3. RECH0 (Hogar y Muestreo)
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

    # 4. RECH23 (Vivienda, Saneamiento y Riqueza)
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

    # 5. RECH4 (Seguro de Salud)
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

    # 6. RECH1 (Miembros del Hogar)
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

    # 7. RECHM (Mortalidad del Hogar)
    if dict_name == 'RECHM':
        return "EXCLUIR POR IRRELEVANCIA / ALTA INCOMPLETITUD", "Registro de defunciones en el hogar. Base extremadamente pequeña (2,714 filas en toda la ENDES, >98% nula para el universo de niños menores de 5 años)."

    # 8. REC41 (Embarazo, Parto y Lactancia)
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

    # 9. REC94 (Suplementación y Tratamiento Pediátrico)
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

    # 10. RECH5 (Evaluación Antropométrica y Anemia de Mujeres de 15 a 49 años)
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

    return "EXCLUIR POR IRRELEVANCIA", "Variable operativa, duplicada o sin sustento epidemiológico comprobable."

def main():
    dict_vars = load_dict_variables()
    
    # Classify all
    classified = {}
    stats = {
        'INCLUIR': 0,
        'DUDOSA': 0,
        'EXCLUIR_LEAKAGE': 0,
        'EXCLUIR_IRRELEVANTE': 0,
        'METADATO': 0,
        'TARGET': 0
    }
    
    for d_name, vars_list in dict_vars.items():
        classified[d_name] = []
        for item in vars_list:
            dec, mot = classify_variable(d_name, item)
            classified[d_name].append({
                'item': item,
                'decision': dec,
                'motivo': mot
            })
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

    print("Estadísticas de clasificación:")
    for k, v in stats.items():
        print(f"  {k}: {v}")

if __name__ == '__main__':
    main()
