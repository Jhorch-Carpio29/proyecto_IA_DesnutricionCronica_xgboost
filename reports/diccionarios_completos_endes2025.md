# DICCIONARIOS DE VARIABLES — ENDES 2025 (INEI)

> **Compilación oficial completa en formato Markdown de todos los diccionarios técnicos de la Encuesta Demográfica y de Salud Familiar (ENDES 2025) del INEI.**  
> Todos los nombres de variables, descripciones, tipos de carácter, longitudes, rangos de variación, códigos de alternativas y observaciones se han preservado íntegramente de los documentos PDF oficiales.

## Índice de Diccionarios

- [Diccionario - RECH0 (1629_hogar)](#diccionario---rech0)
- [Diccionario - RECH1 (1629_hogar)](#diccionario---rech1)
- [Diccionario - RECH4 (1629_hogar)](#diccionario---rech4)
- [Diccionario - RECHM (1629_hogar)](#diccionario---rechm)
- [Diccionario - RECH23 (1630_vivienda)](#diccionario---rech23)
- [Diccionario - REC41 (1633_embarazo)](#diccionario---rec41)
- [Diccionario - REC94 (1633_embarazo)](#diccionario---rec94)
- [Diccionario - REC44 (1638_anemia)](#diccionario---rec44)
- [Diccionario - RECH5 (1638_anemia)](#diccionario---rech5)
- [Diccionario - RECH6 (1638_anemia)](#diccionario---rech6)

---

# DICCIONARIO DE VARIABLES CUESTIONARIO DEL HOGAR (RECH0)

**ENCUESTA DEMOGRÁFICA Y DE SALUD FAMILIAR ENDES**  
*Módulo:* `1629_hogar` | *Archivo fuente:* `Diccionario - RECH0.pdf` | *Páginas originales:* 2

| Nº | VARIABLE | DESCRIPCIÓN DE LAS VARIABLES | TIPO DE CARÁCTER | LONGITUD | RANGO DE VARIACIÓN | VALORES | DESCRIPCIÓN DE LAS ALTERNATIVAS | OBS |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 1 | ID1 | Año | N | 4 |  |  |  |  |
| 2 | HHID | Identificacion Cuestionario del Hogar | A | 15 |  |  |  | Variable (Llave de identificaci'on) |
| 3 | HV000 | Código del país | A | 3 | PE6 |  |  |  |
| 4 | HV001 | Conglomerado | N | 8 | 1:3175 |  |  |  |
| 5 | HV002 | Vivienda | N | 4 | 1:9998 |  |  |  |
| 6 | HV002A | Hogar | N | 3 | 1:5 |  |  |  |
| 7 | HV003 | Número de orden del Informante del cuestionario del hogar | N | 3 | 1:15 |  |  |  |
| 8 | HV004 | Unidad última de muestreo | N | 4 | 1:3175 |  |  |  |
| 9 | HV007 | Año de entrevista | N | 4 |  |  |  |  |
| 10 | HV008 | Fecha de entrevista meses (CMC) | N | 4 |  |  |  |  |
| 11 | HV009 | Total de personas en el hogar | N | 2 | 1:25 |  |  |  |
| 12 | HV010 | Número de mujeres elegibles para entrevista individual | N | 2 | 1:25 |  |  |  |
| 13 | HV011 | Número de hombres elegibles por hogar | N | 2 |  |  |  |  |
| 14 | HV012 | Número de miembros de jure (residentes habituales) | N | 2 | 0:25 |  |  |  |
| 15 | HV013 | Número de miembros de facto (personas que durmieron la noche anterior) | N | 2 | 0:25 |  |  |  |
| 16 | HV014 | Número de niños menores de 5 años | N | 2 | 0:24 |  |  |  |
| 17 | HV015 | Resultado de la entrevista en el hogar | N | 2 | 1:9 | 1 | Completo |  |
|  |  |  |  |  |  | 2 | Hogar presente pero entrevistado ausente |  |
|  |  |  |  |  |  | 3 | Hogar ausente |  |
|  |  |  |  |  |  | 4 | Aplazada |  |
|  |  |  |  |  |  | 5 | Rechazada |  |
|  |  |  |  |  |  | 6 | Vivienda desocupada o no es vivienda |  |
|  |  |  |  |  |  | 7 | Vivienda destruida |  |
|  |  |  |  |  |  | 8 | Vivienda no encontrada |  |
|  |  |  |  |  |  | 9 | Otro |  |
| 18 | HV017 | Número de visitas | N | 1 | 1:9 |  |  |  |
| 19 | HV020 | Muestra de alguna vez en union | N | 1 | 0:1 | 0 | Muestra todas las mujeres |  |
|  |  |  |  |  |  | 1 | Muestra alguna vez casado |  |
| 20 | HV021 | Unidad de muestreo primario (conglomerado) | N | 4 | 1:3175 |  |  |  |
| 21 | HV023 | Dominio | N | 2 | 1:25 | 1 | Amazonas |  |
|  |  |  |  |  |  | 2 | Ancash |  |
|  |  |  |  |  |  | 3 | Apurimac |  |
|  |  |  |  |  |  | 4 | Arequipa |  |
|  |  |  |  |  |  | 5 | Ayacucho |  |
|  |  |  |  |  |  | 6 | Cajamarca |  |
|  |  |  |  |  |  | 7 | Callao |  |
|  |  |  |  |  |  | 8 | Cusco |  |
|  |  |  |  |  |  | 9 | Huancavelica |  |
|  |  |  |  |  |  | 10 | Huanuco |  |
|  |  |  |  |  |  | 11 | Ica |  |
|  |  |  |  |  |  | 12 | Junin |  |
|  |  |  |  |  |  | 13 | La Libertad |  |
|  |  |  |  |  |  | 14 | Lambayeque |  |
|  |  |  |  |  |  | 15 | Lima |  |
|  |  |  |  |  |  | 16 | Loreto |  |
|  |  |  |  |  |  | 17 | Madre de Dios |  |
|  |  |  |  |  |  | 18 | Moquegua |  |
|  |  |  |  |  |  | 19 | Pasco |  |
|  |  |  |  |  |  | 20 | Piura |  |
|  |  |  |  |  |  | 21 | Puno |  |
|  |  |  |  |  |  | 22 | San Martin |  |
|  |  |  |  |  |  | 23 | Tacna |  |
|  |  |  |  |  |  | 24 | Tumbes |  |
|  |  |  |  |  |  | 25 | Ucayali |  |
| 22 | HV024 | Región | N | 2 | 1:25 | 1 | Amazonas |  |
|  |  |  |  |  |  | 2 | Ancash |  |
|  |  |  |  |  |  | 3 | Apurimac |  |
|  |  |  |  |  |  | 4 | Arequipa |  |
|  |  |  |  |  |  | 5 | Ayacucho |  |
|  |  |  |  |  |  | 6 | Cajamarca |  |
|  |  |  |  |  |  | 7 | Callao |  |
|  |  |  |  |  |  | 8 | Cusco |  |
|  |  |  |  |  |  | 9 | Huancavelica |  |
|  |  |  |  |  |  | 10 | Huanuco |  |
|  |  |  |  |  |  | 11 | Ica |  |
|  |  |  |  |  |  | 12 | Junin |  |
|  |  |  |  |  |  | 13 | La Libertad |  |
|  |  |  |  |  |  | 14 | Lambayeque |  |
|  |  |  |  |  |  | 15 | Lima |  |
|  |  |  |  |  |  | 16 | Loreto |  |
|  |  |  |  |  |  | 17 | Madre de Dios |  |
|  |  |  |  |  |  | 18 | Moquegua |  |
|  |  |  |  |  |  | 19 | Pasco |  |
|  |  |  |  |  |  | 20 | Piura |  |
|  |  |  |  |  |  | 21 | Puno |  |
|  |  |  |  |  |  | 22 | San Martin |  |
|  |  |  |  |  |  | 23 | Tacna |  |
|  |  |  |  |  |  | 24 | Tumbes |  |
|  |  |  |  |  |  | 25 | Ucayali |  |
| 23 | HV025 | Área de residencia | N | 1 | 1:2 | 1 | Urbano |  |
|  |  |  |  |  |  | 2 | Rural |  |
| 24 | HV026 | Lugar de residencia | N | 1 | 0:3 | 0 | Capital, gran ciudad |  |
|  |  |  |  |  |  | 1 | Pequeña ciudad |  |
|  |  |  |  |  |  | 2 | Pueblo |  |
|  |  |  |  |  |  | 3 | Campo |  |
| 25 | HV027 | Selección para hombre/esposo | N | 1 | 0:2 | 0 | No seleccionado |  |
|  |  |  |  |  |  | 1 | Encuesta de hombres |  |
|  |  |  |  |  |  | 2 | Encuesta del esposo |  |
| 26 | HV028 | Peso de muestra masculino | N | 8 |  |  |  |  |
| 27 | HV030 | Supervisor de campo | N | 3 |  |  |  |  |
| 28 | HV031 | Editor de campo | N | 3 |  |  |  |  |
| 29 | HV032 | Editor de la oficina | N | 2 |  |  |  |  |
| 30 | HV033 | Ultimate area selection prob. | N | 8 |  |  |  |  |
| 31 | HV035 | Número de niños elegibles para altura y peso | N | 2 | 0:24 |  |  |  |
| 32 | HV040 | Altitud del conglomerado en metros | N | 4 | -24:5100 |  |  |  |
| 33 | HV041 | Número de mujeres con medición de peso y talla | N | 2 | 0:24 |  |  |  |
| 34 | HV042 | Selección para medición de hemoglobina | N | 1 | 0:1 | 0 | No seleccionado |  |
|  |  |  |  |  |  | 1 | Seleccionado |  |
| 35 | HV043 | Hogares seleccionados para el módulo de mujeres de estado | N | 1 | 0:1 | 0 | Hogar no seleccionado |  |
|  |  |  |  |  |  | 1 | Hogar seleccionado |  |
| 36 | HV044 | Selección para el módulo de violencia familiar | N | 1 | 0:1 | 0 | Hogar no seleccionado |  |
|  |  |  |  |  |  | 1 | Hogar seleccionado |  |
| 37 | UBIGEO | Código de Ubicación Gegráfica | A | 6 |  |  |  |  |
| 38 | HV005 | Factor de ponderación | N | 8 |  |  |  |  |
| 39 | HV022 | Estrato | N | 8 | 1:250 |  |  |  |
| 40 | NCONGLOME | Número de Conglomerado (proveniente del marco) | A | 7 |  |  |  |  |
| 41 | CODCCPP | Codigo de Centro Poblado | A | 4 |  |  |  |  |
| 42 | NOMCCPP | Nombre del Centro Poblado | A | 49 |  |  |  |  |
| 43 | LONGITUDX | Longitud del conglomerado | N | 8 |  |  |  |  |
| 44 | LATITUDY | Latitud del conglomerado | N | 8 |  |  |  |  |


---

# DICCIONARIO DE VARIABLES CUESTIONARIO DEL HOGAR (RECH1)

**ENCUESTA DEMOGRÁFICA Y DE SALUD FAMILIAR ENDES**  
*Módulo:* `1629_hogar` | *Archivo fuente:* `Diccionario - RECH1.pdf` | *Páginas originales:* 2

| Nº | VARIABLE | DESCRIPCIÓN DE LAS VARIABLES | TIPO DE CARÁCTER | LONGITUD | RANGO DE VARIACIÓN | VALORES | DESCRIPCIÓN DE LAS ALTERNATIVAS | OBS |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 1 | ID1 | Año | N | 4 |  |  |  |  |
| 2 | HHID | Identificación Cuestionario del Hogar | A | 15 |  |  |  | Variable (Llave de identificación) |
| 3 | HVIDX | Número de orden | N | 2 |  |  |  | Variable (Llave de identificación) |
| 4 | HV101 | Relación de parentesco con el jefe del hogar | N | 2 | 1:15 | 1 | Jefe del Hogar |  |
|  |  |  |  |  |  | 2 | Esposa o esposo |  |
|  |  |  |  |  |  | 3 | Hijo/Hija |  |
|  |  |  |  |  |  | 4 | Yerno/Nuera |  |
|  |  |  |  |  |  | 5 | Nieto |  |
|  |  |  |  |  |  | 6 | Padre |  |
|  |  |  |  |  |  | 7 | Suegro |  |
|  |  |  |  |  |  | 8 | Hermano/Hermana |  |
|  |  |  |  |  |  | 10 | Otro pariente |  |
|  |  |  |  |  |  | 11 | Hijo adoptado |  |
|  |  |  |  |  |  | 12 | Sin parentesco |  |
|  |  |  |  |  |  | 15 | Empleada doméstica |  |
| 5 | HV102 | ¿Vive habitualmente aquí? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 6 | HV103 | ¿Durmió aquí anoche? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 7 | HV104 | Sexo | N | 1 | 1:2 | 1 | Hombre |  |
|  |  |  |  |  |  | 2 | Mujer |  |
| 8 | HV105 | Edad | N | 2 | 1:98 | 97 | Mayores de 96 |  |
|  |  |  |  |  |  | 98 | No sabe |  |
| 9 | HV106 | ¿Cuál fue el nivel de estudios más alto que aprobó? | N | 1 | 0:3, 8 | 0 | Sin educación, preescolar |  |
|  |  |  |  |  |  | 1 | Primario |  |
|  |  |  |  |  |  | 2 | Secundario |  |
|  |  |  |  |  |  | 3 | Superior |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 10 | HV107 | ¿Cuál fue el año o grado más alto que aprobó? | N | 2 | 0:8, 98 | 98 | No sabe |  |
| 11 | HV108 | Número de años de estudio | N | 2 | 0:21, 98 | 98 | No sabe |  |
| 12 | HV109 | Nivel educativo alcanzado | N | 1 | 0:5, 8 | 0 | Sin educación |  |
|  |  |  |  |  |  | 1 | Primaria incompleta |  |
|  |  |  |  |  |  | 2 | Primaria completa |  |
|  |  |  |  |  |  | 3 | Secundaria incompleta |  |
|  |  |  |  |  |  | 4 | Secundaria completa |  |
|  |  |  |  |  |  | 5 | Superior |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 13 | HV110 | Actualmente ¿Asiste a una escuela o colegio (un instituto superior o universidad)? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 14 | HV111 | ¿Está viva la madre natural? | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 15 | HV112 | Número de orden de la madre | N | 2 | 0:20 | 0 | Madre no en HH |  |
| 16 | HV113 | ¿Está vivo el padre natural? | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 17 | HV114 | Número de orden del padre | N | 2 | 0:25 | 0 | Padre no en HH |  |
| 18 | HV115 | ¿Cúal es su estado civil o conyugal? | N | 1 | 0:5 | 0 | Soltero(a) |  |
|  |  |  |  |  |  | 1 | Casado(a) |  |
|  |  |  |  |  |  | 2 | Conviviente |  |
|  |  |  |  |  |  | 3 | Viudo(a) |  |
|  |  |  |  |  |  | 4 | Divorciado(a) |  |
|  |  |  |  |  |  | 5 | Separado(a) |  |
| 19 | HV116 | Acutalmente, anteriormente o nunca unida | N | 1 | 0:2 | 0 | Soltero(a) |  |
|  |  |  |  |  |  | 1 | Actualmente casado(a) o conviviendo |  |
|  |  |  |  |  |  | 2 | Anteriormente/alguna vez casado(a) o conviviendo |  |
| 20 | HV117 | Elegibilidad para entrevista individual de mujeres | N | 1 | 0:1 | 0 | No elegible |  |
|  |  |  |  |  |  | 1 | Elegible |  |
| 21 | HV118 | Elegibilidad para entrevista de hombres | N | 1 | 0:1 | 0 | No elegible |  |
|  |  |  |  |  |  | 1 | Elegible |  |
| 22 | HV120 | Menores de 5 años para medición de peso/talla y hemoglobina | N | 1 | 0:1 | 0 | No elegible |  |
|  |  |  |  |  |  | 1 | Elegible |  |
| 23 | HV121 | ¿Asistió a una escuela o colegio? en algún momento durante el año actual | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Actualmente asistiendo |  |
| 24 | HV122 | ¿A qué nivel asiste o se matriculó? | N | 1 | 0:3, 8 | 0 | Inicial/Pre-escolar |  |
|  |  |  |  |  |  | 1 | Primario |  |
|  |  |  |  |  |  | 2 | Secundario |  |
|  |  |  |  |  |  | 3 | Superior |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 25 | HV123 | Año o grado que asiste o se matriculó | N | 2 | 1:6, 98 | 98 | No sabe |  |
| 26 | HV124 | Número de años de estudio al que asiste o se matriculó durante el año actual | N | 2 | 0:21, 98 | 97 | Inconsistente |  |
|  |  |  |  |  |  | 98 | No Sabe |  |
| 27 | HV125 | El año pasado ¿estuvo o matriculado en una escuela o colegio (un instituto superior o universidad) | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 28 | HV126 | ¿A que nivel asistió o se matriculó el año pasado? | N | 1 | 0:3, 8 | 0 | Inicial/Pre-escolar |  |
|  |  |  |  |  |  | 1 | Primario |  |
|  |  |  |  |  |  | 2 | Secundario |  |
|  |  |  |  |  |  | 3 | Superior |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 29 | HV127 | Año o grado que asistió o se matriculó | N | 2 | 1:6, 98 | 98 | NS |  |
| 30 | HV128 | Número de años de estudio al que asiste o se matriculó el año pasado | N | 2 | 0:21, 98 | 97 | Inconsistente |  |
|  |  |  |  |  |  | 98 | No Sabe |  |
| 31 | HV129 | Condición de asistencia a una escuela, colegio, instituto superior o universidad | N | 1 | 0:5 | 0 | Nunca asistió |  |
|  |  |  |  |  |  | 1 | Ingresado a la escuela |  |
|  |  |  |  |  |  | 2 | Avanzado |  |
|  |  |  |  |  |  | 3 | Repitiendo |  |
|  |  |  |  |  |  | 4 | Abandonó |  |
|  |  |  |  |  |  | 5 | Dejo el colegio hace más de 2 años |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 32 | QH21A | ¿Estudia en una escuela o colegio estatal? | N | 1 | 1:2 | 1 | Sí |  |
|  |  |  |  |  |  | 2 | No |  |
| 33 | QH25A | ¿Cuál es su nacionalidad? | A | 100 |  |  |  |  |
| 34 | QH25B | Vive permanentemente en el Perú | N | 1 | 1:2 | 1 | Sí |  |
|  |  |  |  |  |  | 2 | No |  |
| 35 | QH25CM | Desde qué mes vive en el Perú | N | 2 |  |  |  |  |
| 36 | QH25CA | Desde qué año vive en el Perú | N | 4 |  |  |  |  |


---

# DICCIONARIO DE VARIABLES CUESTIONARIO DEL HOGAR (RECH4)

**ENCUESTA DEMOGRÁFICA Y DE SALUD FAMILIAR ENDES**  
*Módulo:* `1629_hogar` | *Archivo fuente:* `Diccionario - RECH4.pdf` | *Páginas originales:* 1

| Nº | VARIABLE | DESCRIPCIÓN DE LAS VARIABLES | TIPO DE CARÁCTER | LONGITUD | RANGO DE VARIACIÓN | VALORES | DESCRIPCIÓN DE LAS ALTERNATIVAS | OBS |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 1 | ID1 | Año | N | 4 |  |  |  |  |
| 2 | HHID | Identificacion Cuestionario del Hogar | A | 15 |  |  |  | Variable (Llave de identificación) |
| 3 | IDXH4 | Número de orden del listado del hogar | N | 2 | 1:25 |  |  | Variable (Llave de identificación) |
| 4 | SH11A | Seguro de salud: ESSALUD/IPSS | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 5<br>6 | SH11B<br>SH11C | Seguro de salud: Militar<br>Seguro de salud: Integral | N<br>N | 1<br>1 | 0:1<br>0:1 | 0 | No |  |
|  |  |  |  |  |  | 1<br>0 | Si<br>No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 7 | SH11D | Seguro de salud: Compañía de seguros | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 8 | SH11E | Seguro de salud: Seguro privado | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 9 | SH11Y | Seguro de salud: No sabe | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 10 | SH11Z | Seguro de salud: No tienen | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 11 | SH12 | Alguno de los seguros está a su nombre | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 12 | SH13 | Actividad de la ultima semana | N | 2 | 1:8, 96, 98 | 1 | Trabajó menos de una hora |  |
|  |  |  |  |  |  | 2 | Realizó alguna tarea o cachuelo |  |
|  |  |  |  |  |  | 3 | No trabajó pero tenia trabajo |  |
|  |  |  |  |  |  | 4 | Estuvo ayudando en la chacra, tienda o negocio de<br>un familiar, sin pago alguno |  |
|  |  |  |  |  |  | 5 | Buscó trabajo |  |
|  |  |  |  |  |  | 6 | Estudiaba |  |
|  |  |  |  |  |  | 7 | Realizó los queaceres del hogar |  |
|  |  |  |  |  |  | 8 | Es jubilado/ pensionista |  |
|  |  |  |  |  |  | 96 | Otro |  |
|  |  |  |  |  |  | 98 | No sabe |  |
| 13 | SH15N | Nivel de educación aprobado | N | 1 | 0:5, 8 | 0 | Inicial/ Pre-escolar |  |
|  |  |  |  |  |  | 1 | Primario |  |
|  |  |  |  |  |  | 2 | Secundario |  |
|  |  |  |  |  |  | 3 | Superior, no universitario |  |
|  |  |  |  |  |  | 4 | Superior universitario |  |
|  |  |  |  |  |  | 5 | Posgrado |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 14 | SH15Y | Nivel de educación en años | N | 1 | 0:8 | 7 | Educación dada en grados |  |
|  |  |  |  |  |  | 8 | No lo sé |  |
| 15 | SH15G | Nivel de educación en grados | N | 1 | 1:6, 8 | 8 | No lo sé |  |
| 16 | SH18N | Nivel de educación que actualmente asiste o se matriculó | N | 1 | 0:5, 8 | 0 | Inicial/ Pre-escolar |  |
|  |  |  |  |  |  | 1 | Primario |  |
|  |  |  |  |  |  | 2 | Secundario |  |
|  |  |  |  |  |  | 3 | Superior, no universitario |  |
|  |  |  |  |  |  | 4 | Superior universitario |  |
|  |  |  |  |  |  | 5 | Posgrado |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 17 | SH18Y | Año al que actualmente asiste o se matriculó | N | 1 | 0:8 | 7 | Educación dada en grados |  |
|  |  |  |  |  |  | 8 | No lo sé |  |
| 18 | SH18G | Grado al que actualmente asiste o se matriculó | N | 1 | 1:6, 8 | 8 | No lo sé |  |
| 19 | SH20N | Nivel educativo al que asistió el año pasado | N | 1 | 0:5, 8 | 0 | Inicial/ Pre-escolar |  |
|  |  |  |  |  |  | 1 | Primario |  |
|  |  |  |  |  |  | 2 | Secundario |  |
|  |  |  |  |  |  | 3 | Superior, no universitario |  |
|  |  |  |  |  |  | 4 | Superior universitario |  |
|  |  |  |  |  |  | 5 | Posgrado |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 20 | SH20Y | Año al que asistió el año pasado | N | 1 | 0:8 | 7 | Educación dada en grados |  |
|  |  |  |  |  |  | 8 | No lo sé |  |
| 21 | SH20G | Grado al que asistió el año pasado | N | 1 | 1:6, 8 | 8 | No lo sé |  |
| 22 | SH21 | Resultado de la asistencia del año escolar pasado | N | 1 | 1:4 | 1 | Aprobó |  |
|  |  |  |  |  |  | 2 | Desaprobó |  |
|  |  |  |  |  |  | 3 | Se retiró |  |
|  |  |  |  |  |  | 4 | Otro |  |


---

# DICCIONARIO DE VARIABLES CUESTIONARIO DEL HOGAR (RECHM)

**ENCUESTA DEMOGRÁFICA Y DE SALUD FAMILIAR ENDES**  
*Módulo:* `1629_hogar` | *Archivo fuente:* `Diccionario - RECHM.pdf` | *Páginas originales:* 1

| Nº | VARIABLE | DESCRIPCIÓN DE LAS VARIABLES | TIPO DE CARÁCTER | LONGITUD | RANGO DE VARIACIÓN | VALORES | DESCRIPCIÓN DE LAS ALTERNATIVAS | OBS |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 1 | ID1 | Año | N | 4 |  |  |  |  |
| 2 | HHID | Identificación del caso | A | 15 |  |  |  | Variable (Llave de identificación) |
| 3 | NRO_ORDEN_ID | Número de orden | N | 2 | 1:10 |  |  | Variable (Llave de identificación) |
| 4 | QH30M | Sexo | N | 1 | 1:2 | 1 | Hombre |  |
|  |  |  |  |  |  | 2 | Mujer |  |
| 5 | QH31M | A qué edad murió | N | 3 | 0:110 |  |  |  |
| 6 | QH32M_M | En qué mes murió | N | 2 | 1:12, 97 | 1 | Enero |  |
|  |  |  |  |  |  | 2 | Febrero |  |
|  |  |  |  |  |  | 3 | Marzo |  |
|  |  |  |  |  |  | 4 | Abril |  |
|  |  |  |  |  |  | 5 | Mayo |  |
|  |  |  |  |  |  | 6 | Junio |  |
|  |  |  |  |  |  | 7 | Julio |  |
|  |  |  |  |  |  | 8 | Agosto |  |
|  |  |  |  |  |  | 9 | Setiembre |  |
|  |  |  |  |  |  | 1 0 | Octubre |  |
|  |  |  |  |  |  | 1 1 | Noviembre |  |
|  |  |  |  |  |  | 1 2 | Diciembre |  |
|  |  |  |  |  |  | 9 7 | No sabe |  |
| 7 | QH32M_Y | En qué año murió | N | 4 |  |  |  |  |
| 8 | QH33M | Murió por alguna causa relacionada con el embarazo, parto, sobreparto o por alguna otra causa | N | 1 | 1:4 | 1 | Embarazo |  |
|  |  |  |  |  |  | 2 | Parto |  |
|  |  |  |  |  |  | 3 | Sobreparto |  |
|  |  |  |  |  |  | 4 | Otra causa |  |


---

# DICCIONARIO DE VARIABLES CUESTIONARIO DEL HOGAR (RECH23)

**ENCUESTA DEMOGRÁFICA Y DE SALUD FAMILIAR ENDES**  
*Módulo:* `1630_vivienda` | *Archivo fuente:* `Diccionario - RECH23.pdf` | *Páginas originales:* 7

| Nº | VARIABLE | DESCRIPCIÓN DE LAS VARIABLES | TIPO DE CARÁCTER | LONGITUD | RANGO DE VARIACIÓN | VALORES | DESCRIPCIÓN DE LAS ALTERNATIVAS | OBS |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 1 | ID1 | Año | N | 4 |  |  |  |  |
| 2 | HHID | Identificacion Cuestionario del Hogar | A | 15 |  |  |  | Variable (Llave de identificación) |
| 3 | HV201 | ¿Cuál es la fuente principal de abastecimiento de agua para tomar o beber? | N | 2 | 11:13, 21:22, 41, 43, 51, 61, 71, 96 | 11 | Dentro de la vivienda |  |
|  |  |  |  |  |  | 12 | Fuera de la vivienda, pero dentro del edificio |  |
|  |  |  |  |  |  | 13 | Pilón/Grifo público |  |
|  |  |  |  |  |  | 21 | Pozo en la vivineda/patio/lote |  |
|  |  |  |  |  |  | 22 | Pozo público |  |
|  |  |  |  |  |  | 41 | Manantial (puquio) |  |
|  |  |  |  |  |  | 43 | Río/acequia/laguna |  |
|  |  |  |  |  |  | 51 | Agua de lluvia |  |
|  |  |  |  |  |  | 61 | Camión cisterna |  |
|  |  |  |  |  |  | 71 | Agua embotellada |  |
|  |  |  |  |  |  | 96 | Otro |  |
| 4 | HV202 | ¿Cuál es la fuente principal de abastecimiento de agua en su hogar? | N | 2 | 11:13, 21:22, 41, 43, 51, 61, 96 | 11 | Dentro de la vivienda |  |
|  |  |  |  |  |  | 12 | Fuera de la vivienda, pero dentro del edificio |  |
|  |  |  |  |  |  | 13 | Pilón/Grifo público |  |
|  |  |  |  |  |  | 21 | Pozo en la vivineda/patio/lote |  |
|  |  |  |  |  |  | 22 | Pozo público |  |
|  |  |  |  |  |  | 41 | Manantial (puquio) |  |
|  |  |  |  |  |  | 43 | Río/acequia/laguna |  |
|  |  |  |  |  |  | 51 | Agua de lluvia |  |
|  |  |  |  |  |  | 61 | Camión cisterna |  |
|  |  |  |  |  |  | 96 | Otro |  |
| 5 | HV204 | ¿Cuánto tiempo se demora en ir, recoger agua y volver? | N | 3 | 0:300, 996, 998 | 996 | En las instalaciones |  |
|  |  |  |  |  |  | 998 | No sabe |  |
| 6 | HV205 | ¿Qué tipo de servicio higiénico tiene su hogar? | N | 2 | 11:12, 21:24, 31, 32, 96 | 11 | Dentro de la vivienda |  |
|  |  |  |  |  |  | 12 | Fuera de la vivienda, pero dentro del edificio |  |
|  |  |  |  |  |  | 21 | Letrina mejorada ventilada |  |
|  |  |  |  |  |  | 22 | Pozo séptico |  |
|  |  |  |  |  |  | 23 | Latrina (pozo ciego o negro) |  |
|  |  |  |  |  |  | 24 | Latrina mejorada colgada/flotante |  |
|  |  |  |  |  |  | 31 | Río, acequia o canal |  |
|  |  |  |  |  |  | 32 | Sin servicio (matorral/campo) |  |
|  |  |  |  |  |  | 96 | Otro |  |
| 7 | HV206 | ¿Tiene electricidad en su hogar? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 8 | HV207 | Su hogar ¿tiene radio? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 9 | HV208 | Su hogar ¿tiene televisor? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 10 | HV209 | Su hogar ¿tiene refrigeradora /congeladora? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 11 | HV210 | Algún miembro de su hogar ¿tiene bicleta/triciclo? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 12 | HV211 | Algún miembro de su hogar ¿tiene motocileta/ motokar? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 13 | HV212 | Algún miembro de su hogar ¿tiene carro o camión? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 14 | HV213 | Material predominante del piso de la vivienda | N | 2 | 11, 21, 31:34, 96 | 11 | Tierra/arena |  |
|  |  |  |  |  |  | 21 | Madera |  |
|  |  |  |  |  |  | 31 | Parquet o madera pulida |  |
|  |  |  |  |  |  | 32 | Láminas asfálticas, vinílicos o similares |  |
|  |  |  |  |  |  | 33 | Losetas, terrazos o similares |  |
|  |  |  |  |  |  | 34 | Cemento/ladrillo |  |
|  |  |  |  |  |  | 96 | Otro |  |
| 15 | HV214 | Material predominante de las paredes exteriores de la vivienda | N | 2 | 11, 21, 31:34, 96 | 11 | Tablones/Madera |  |
|  |  |  |  |  |  | 12 | Estera |  |
|  |  |  |  |  |  | 13 | Caña/Bambu/Pona/Palma/Troncos/Tabique |  |
|  |  |  |  |  |  | 21 | Adobe o tapia |  |
|  |  |  |  |  |  | 22 | Quincha (caña con barro) |  |
|  |  |  |  |  |  | 23 | Piedra con barro |  |
|  |  |  |  |  |  | 24 | Cartón |  |
|  |  |  |  |  |  | 31 | Ladrillo o bloques de cemento |  |
|  |  |  |  |  |  | 32 | Piedra o sillar con cal o cemento |  |
|  |  |  |  |  |  | 33 | Tripley |  |
|  |  |  |  |  |  | 41 | Sin paredes |  |
|  |  |  |  |  |  | 96 | Otro |  |
| 16 | HV215 | Material predominante del techo de la vivienda | N | 2 | 11:12, 21:22, 31:34, 41, 96 | 11 | Paja, hojas de palmera etc. |  |
|  |  |  |  |  |  | 12 | Estera |  |
|  |  |  |  |  |  | 21 | Caña o estera en torta de barro |  |
|  |  |  |  |  |  | 22 | Cartón |  |
|  |  |  |  |  |  | 31 | Concreto armado |  |
|  |  |  |  |  |  | 32 | Madera |  |
|  |  |  |  |  |  | 33 | Tejas |  |
|  |  |  |  |  |  | 34 | Plancha de calamina, fibra de cemento o similares |  |
|  |  |  |  |  |  | 41 | Sin techo |  |
|  |  |  |  |  |  | 96 | Otro |  |
| 17 | HV216 | Número de habitaciones utilizadas para dormir | N | 2 | 0:15 |  |  |  |
| 18 | HV217 | Estructura de relaciones en el hogar (composición de los hogares) | N | 1 | 1:5 | 1 | Un adulto |  |
|  |  |  |  |  |  | 2 | Dos adultos, diferente sexo |  |
|  |  |  |  |  |  | 3 | Dos adultos, del mismo sexo |  |
|  |  |  |  |  |  | 4 | Tres o más adultos con algún grado de parentesco |  |
|  |  |  |  |  |  | 5 | Adultos sin grado de parentesco |  |
| 19 | HV218 | Número de orden del Jefe del hogar | N | 2 | 1 |  |  |  |
| 20 | HV219 | Sexo del jefe de hogar | N | 1 | 1:2 | 1 | Masculino |  |
|  |  |  |  |  |  | 2 | Femenino |  |
| 21 | HV220 | Edad del jefe de hogar | N | 2 | 12:98 | 97 | 97 y más |  |
|  |  |  |  |  |  | 98 | No Sabe |  |
| 22 | HV221 | Su hogar ¿tiene teléfono? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 23 | HV225 | ¿El servicio higiénico es compartido con otros hogares? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 24 | HV226 | ¿Cuál es el combustible que utilizan más frecuentemente en su hogar para cocinar? | N | 2 | 1:11, 95, 96 | 1 | Electricidad |  |
|  |  |  |  |  |  | 2 | GLP |  |
|  |  |  |  |  |  | 3 | Gas natural |  |
|  |  |  |  |  |  | 5 | Kerosene |  |
|  |  |  |  |  |  | 6 | Carbón vegetal |  |
|  |  |  |  |  |  | 7 | Carbón mineral |  |
|  |  |  |  |  |  | 8 | Leña |  |
|  |  |  |  |  |  | 9 | Caña/Arbustos secos |  |
|  |  |  |  |  |  | 10 | Residuos agrícolas |  |
|  |  |  |  |  |  | 11 | Bosta |  |
|  |  |  |  |  |  | 95 | No cocina |  |
|  |  |  |  |  |  | 96 | Otro |  |
| 25 | HV227 | Tiene un mosquitero para dormir | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 26 | HV228 | Los niños menores de 5 años durmieron bajo mosquiteros anoche | N | 1 | 0:3 | 0 | No |  |
|  |  |  |  |  |  | 1 | Todos los niños |  |
|  |  |  |  |  |  | 2 | Algunos niños |  |
|  |  |  |  |  |  | 3 | No mosquitero en el hogar |  |
| 27 | HV234 | Prueba de yodo para sal | N | 3 | 0, 7, 15, 30, 994, 995 | 0 | 0 PPM (sin yodo) |  |
|  |  |  |  |  |  | 7 | 7 PPM |  |
|  |  |  |  |  |  | 15 | 15 PPM |  |
|  |  |  |  |  |  | 30 | 30 PPM |  |
|  |  |  |  |  |  | 994 | No se realizó la prueba |  |
|  |  |  |  |  |  | 995 | No hay sal en el hogar |  |
| 28 | HV235 | Ubicación de la fuente de agua | N | 1 | 1:3 | 1 | En vivienda propia |  |
|  |  |  |  |  |  | 2 | En patio o parcela propia |  |
|  |  |  |  |  |  | 3 | Otro lugar |  |
| 29 | HV236 | Persona que a recoger agua para su hogar | N | 1 | 1:4, 6 | 1 | Mujer adulta |  |
|  |  |  |  |  |  | 2 | Hombre adulto |  |
|  |  |  |  |  |  | 3 | Niño menor de 15 años |  |
|  |  |  |  |  |  | 4 | Niños menores de 15 años |  |
|  |  |  |  |  |  | 6 | Otro |  |
| 30 | HV237 | Hecho algo al agua para hacerla segura para beber | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 31 | HV237A | El agua usualmente es tratada por: hervida | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 32 | HV237B | El agua usualmente es tratada por: añadir lejía o cloro | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 33 | HV237C | El agua usualmente es tratada por: filtro a través de un paño | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 34 | HV237D | El agua usualmente es tratada por: uso de agua filtrada | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 35 | HV237E | El agua usualmente es tratada por: desinfección solar | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 36 | HV237F | El agua usualmente es tratada por: dejar reposar y asentarse | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 37 | HV237G | El agua usualmente es tratada por: CS - agua embotellada | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 38 | HV237H | El agua usualmente es tratada por: CS | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 39 | HV237I | El agua usualmente es tratada por: CS | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 40 | HV237J | El agua usualmente es tratada por: CS | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 41 | HV237K | El agua usualmente es tratada por: CS | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 42 | HV237X | El agua usualmente es tratada por: otros | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 43 | HV237Z | El agua usualmente es tratada por: no sabe | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 44 | HV238 | Número de hogares que comparten el baño | N | 2 |  | 95 | 10 o más hogares |  |
|  |  |  |  |  |  | 98 | No sabe |  |
| 45 | HV239 | Comida cocinada en estufa o fuego abierto | N | 1 | 1:3, 6 | 1 | Abran fuego |  |
|  |  |  |  |  |  | 2 | Estufa abierta |  |
|  |  |  |  |  |  | 3 | Estufa cerrada con chimenea |  |
|  |  |  |  |  |  | 6 | Otro |  |
| 46 | HV240 | El hogar tiene una chimenea o una campana | N | 1 | 0:2 | 0 | Ni chimenea ni campana |  |
|  |  |  |  |  |  | 1 | Tubo de lámpara |  |
|  |  |  |  |  |  | 2 | capucha |  |
| 47 | HV241 | Comida preparada en la casa, en edificio separado o al aire libre | N | 1 | 1:3, 6 | 1 | En la casa |  |
|  |  |  |  |  |  | 2 | En un edificio separado |  |
|  |  |  |  |  |  | 3 | Al aire libre |  |
|  |  |  |  |  |  | 6 | Otro |  |
| 48 | HV242 | ¿Utilizan un cuarto especialmente para cocinar? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 49 | HV243A | ¿Tiene un teléfono móvil (celular)? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 50 | HV243B | Tiene un reloj | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 51 | HV243C | ¿Tiene un carreta jalada por animales? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 52 | HV243D | ¿Tiene un bote a motor? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 53 | HV244 | ¿Algún miembro del hogar es dueño de tierras agrícolas? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 54 | HV245 | ¿Cuántas hectáreas de tierras agrícolas le pertenecen? | N | 2 | 0:96, 98 | 95 | Más de 95 |  |
|  |  |  |  |  |  | 96 | Superficie que no sea hectárea |  |
|  |  |  |  |  |  | 98 | No sabe |  |
| 55 | HV246 | ¿Algún miembro del hogar es dueño de ganadería, rebaños o animales de granja? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 56 | HV246A | Cantidad de: ganado | N | 2 | 0:95, 98 | 0 | Ninguna |  |
|  |  |  |  |  |  | 95 | Más de 95 |  |
|  |  |  |  |  |  | 98 | Desconocido |  |
| 57 | HV246B | Cantidad de: vacas, toros | N | 2 | 0:95, 98 | 0 | Ninguna |  |
|  |  |  |  |  |  | 95 | Más de 95 |  |
|  |  |  |  |  |  | 98 | Desconocido |  |
| 58 | HV246C | Cantidad de: caballos, burros, mulas | N | 2 | 0:95, 98 | 0 | Ninguna |  |
|  |  |  |  |  |  | 95 | Más de 95 |  |
|  |  |  |  |  |  | 98 | Desconocido |  |
| 59 | HV246D | Cantidad de: cabras | N | 2 | 0:95, 98 | 0 | Ninguna |  |
|  |  |  |  |  |  | 95 | Más de 95 |  |
|  |  |  |  |  |  | 98 | Desconocido |  |
| 60 | HV246E | Cantidad de: ovejas | N | 2 | 0:95, 98 | 0 | Ninguna |  |
|  |  |  |  |  |  | 95 | Más de 95 |  |
|  |  |  |  |  |  | 98 | Desconocido |  |
| 61 | HV246F | Cantidad de: pollos | N | 2 | 0:95, 98 | 0 | Ninguna |  |
|  |  |  |  |  |  | 95 | Más de 95 |  |
|  |  |  |  |  |  | 98 | Desconocido |  |
| 62 | HV246G | Cantidad de: aves de corral | N | 2 | 0:95, 98 | 0 | Ninguna |  |
|  |  |  |  |  |  | 95 | Más de 95 |  |
|  |  |  |  |  |  | 98 | Desconocido |  |
| 63 | HV246H | Cantidad de: cuyes/conejos | N | 2 | 0:95, 98 | 0 | Ninguna |  |
|  |  |  |  |  |  | 95 | Más de 95 |  |
|  |  |  |  |  |  | 98 | Desconocido |  |
| 64 | HV246I | Cantidad de: cerdos | N | 2 | 0:95, 98 | 0 | Ninguna |  |
|  |  |  |  |  |  | 95 | Más de 95 |  |
|  |  |  |  |  |  | 98 | Desconocido |  |
| 65 | HV246J | Cantidad de: otros | N | 2 | 0:95, 98 | 0 | Ninguna |  |
|  |  |  |  |  |  | 95 | Más de 95 |  |
|  |  |  |  |  |  | 98 | Desconocido |  |
| 66 | HV246K | CS propio | N | 2 | 0:95, 98 | 0 | Ninguna |  |
|  |  |  |  |  |  | 95 | Más de 95 |  |
|  |  |  |  |  |  | 98 | Desconocido |  |
| 67 | HV247 | Posee una cuenta bancaria | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 68 | HV248 | Número de personas enfermas 18-59 | N | 2 |  |  |  |  |
| 69 | HV249 | Miembro de la HH fallecido los últimos 12 meses | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 70 | HV250 | Número de miembros que murieron en los últimos 12 meses | N | 2 |  | 8 | NS |  |
| 71 | HV251 | Número de huérfanos y niños vulnerables | N | 2 |  |  |  |  |
| 72 | HML1 | Número de mosquiteros | N | 2 |  | 98 | No Sabe |  |
| 73 | HML1A | Número de mosquiteros con información específica | N | 1 |  |  |  |  |
| 74 | HML2 | Número de niños menores de edad en la noche anterior | N | 2 |  |  |  |  |
| 75 | SHVER | Versión del cuestionario | N | 1 |  |  |  |  |
| 76 | SHREGION | Región natural | N | 2 | 1:4 | 1 | Lima metropolitana |  |
|  |  |  |  |  |  | 2 | Resto Costa |  |
|  |  |  |  |  |  | 3 | Sierra |  |
|  |  |  |  |  |  | 4 | Selva |  |
| 77 | SHSEMES | Semestre | N | 2 |  |  |  |  |
| 78 | SHPROVIN | Provincia | N | 2 |  |  |  |  |
| 79 | SHDISTRI | Distrito | N | 2 |  |  |  |  |
| 80 | SHTOTH | Total de hogares en la vivienda | N | 2 |  |  |  |  |
| 81 | SH42 | El abastecimiento de agua para beber está disponible todo el día | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 82 | SH43 | Las últimas 2 semanas fueron interrumpidas por un día o más | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 83 | SH48 | ¿Conserva en un envase o recipiente el agua para beber? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 84 | SH49 | Tipo de envase o recipiente | N | 2 | 1:4, 96 | 1 | Olla, tetera |  |
|  |  |  |  |  |  | 2 | Balde |  |
|  |  |  |  |  |  | 3 | Jarra |  |
|  |  |  |  |  |  | 4 | Bidón |  |
|  |  |  |  |  |  | 96 | Otro |  |
| 85 | SH50 | ¿Lo usa con tapa? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 86 | SH51 | Pago por el agua? | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 87 | SH52 | Institución de pago de agua | N | 1 | 1:6 | 1 | Agencia pública / empresa |  |
|  |  |  |  |  |  | 2 | Agencia privada / empresa |  |
|  |  |  |  |  |  | 3 | Otras provisiones privadas de agua |  |
|  |  |  |  |  |  | 4 | JASS |  |
|  |  |  |  |  |  | 6 | Otro |  |
| 88 | SH56 | Con qué frecuencia se limpia el baño o la letrina? | N | 1 | 1:6 | 1 | Varias veces durante el |  |
|  |  |  |  |  |  | 2 | Diariamente |  |
|  |  |  |  |  |  | 3 | Varias veces durante el |  |
|  |  |  |  |  |  | 4 | Semanal |  |
|  |  |  |  |  |  | 5 | 8 días |  |
|  |  |  |  |  |  | 6 | Nunca |  |
| 89 | SH58 | Dónde tira la basura? | N | 2 | 11:15, 21:24, 31, 41:44, 51, 61, 71, 81, 96,<br>98 | 11 | Elegido en casa por el gobierno |  |
|  |  |  |  |  |  | 12 | Elegido en el hogar por municipio |  |
|  |  |  |  |  |  | 13 | Elegido en casa por la comunidad |  |
|  |  |  |  |  |  | 14 | Elegido en casa por la empresa privada |  |
|  |  |  |  |  |  | 15 | Elegido en casa por Otro |  |
|  |  |  |  |  |  | 21 | Tirar en contenedores del gobierno |  |
|  |  |  |  |  |  | 22 | Lanzar en el municipio containe |  |
|  |  |  |  |  |  | 23 | Tirar en contenedores comunitarios |  |
|  |  |  |  |  |  | 24 | Tirar en compañía privada |  |
|  |  |  |  |  |  | 31 | Lanzar en un espacio abierto |  |
|  |  |  |  |  |  | 41 | Tirar en un lugar lejano |  |
|  |  |  |  |  |  | 42 | Tirar en las calles |  |
|  |  |  |  |  |  | 43 | Tirar en yarda / parcela |  |
|  |  |  |  |  |  | 44 | Río |  |
|  |  |  |  |  |  | 51 | Quemar |  |
|  |  |  |  |  |  | 61 | Enterrar |  |
|  |  |  |  |  |  | 71 | Hacer abono |  |
|  |  |  |  |  |  | 81 | Uso para alimentar a los animales |  |
|  |  |  |  |  |  | 96 | Otro |  |
|  |  |  |  |  |  | 98 | No sabe |  |
| 90 | SH59 | Con qué frecuencia se recoge la basura? | N | 2 | 1:6 | 1 | Diariamente |  |
|  |  |  |  |  |  | 2 | Varias veces durante la semana |  |
|  |  |  |  |  |  | 3 | Semanal |  |
|  |  |  |  |  |  | 4 | Cualquier otra semana |  |
|  |  |  |  |  |  | 5 | Una vez al mes |  |
|  |  |  |  |  |  | 6 | Tiempo irregular |  |
| 91 | SH60 | Antes de desechar la basura donde se almacena? | N | 1 | 1:6 | 1 | Contenedor / contenedor de la cubierta |  |
|  |  |  |  |  |  | 2 | Descubrir receptivo / contener |  |
|  |  |  |  |  |  | 3 | Bolsas de plástico |  |
|  |  |  |  |  |  | 4 | Bolsas de papel |  |
|  |  |  |  |  |  | 5 | No tiene destinatario |  |
|  |  |  |  |  |  | 6 | Otro |  |
| 92 | SH61A | ¿Tiene sofá? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 93 | SH61B | ¿Tiene vitrina/aparador? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 94 | SH61C | ¿Tiene repostero? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 95 | SH61D | ¿Tiene cómoda/ropero? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 96 | SH61E | ¿Tiene reloj de pared? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 97 | SH61J | ¿Tiene televisión por cable? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 98 | SH61K | ¿Tiene licuadora? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 99 | SH61L | ¿Tiene cocina de gas? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 100 | SH61M | ¿Tiene cocina de kerosene? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 101 | SH61N | ¿Tiene microondas? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 102 | SH61O | ¿Tiene lavadora? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 103 | SH61P | ¿Tiene computadora? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 104 | SH61Q | ¿Tiene acceso a Internet en casa? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 105 | SH61R | ¿Tiene bomba de agua? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 106 | SH61S | ¿Tiene generador de electricidad? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 107 | SH63 | ¿Utiliza otro tipo de combustible para cocinar? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 108 | SH64 | Otro tipo de combustible utilizado para cocinar | N | 2 | 1:11, 96 | 1 | Electricidad |  |
|  |  |  |  |  |  | 2 | GLP |  |
|  |  |  |  |  |  | 3 | Gas natural |  |
|  |  |  |  |  |  | 5 | Kerosene |  |
|  |  |  |  |  |  | 6 | Carbón vegetal |  |
|  |  |  |  |  |  | 7 | Carbón mineral |  |
|  |  |  |  |  |  | 8 | Leña |  |
|  |  |  |  |  |  | 9 | Caña arbustos secos |  |
|  |  |  |  |  |  | 10 | Residuos agrícolas |  |
|  |  |  |  |  |  | 11 | Bosta |  |
|  |  |  |  |  |  | 96 | Otro |  |
| 109 | SH66 | ¿La cocina tiene una chimenea o un mecanismo para eliminar el humo? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 110 | SH69 | El hogar compra combustible para cocinar? | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 111 | SH70 | ¿Qué tipo de alumbrado utiliza el hogar? | N | 2 | 1:6, 96 | 1 | Electricidad |  |
|  |  |  |  |  |  | 2 | GLP |  |
|  |  |  |  |  |  | 3 | Gas natural |  |
|  |  |  |  |  |  | 4 | Kerosene |  |
|  |  |  |  |  |  | 5 | Velas |  |
|  |  |  |  |  |  | 6 | Batería |  |
|  |  |  |  |  |  | 96 | Otro |  |
| 112 | SH71 | Número de habitaciones en el hogar | N | 2 | 1:25 |  |  |  |
| 113 | SH72 | Número de habitaciones que usa para dormir | N | 2 | 1:25 |  |  |  |
| 114 | SXH73 | Tiene una red (No 20011) | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 115 | SH76A | La vivienda tiene ventanas | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 116 | SH76B | Ventanas con cristal | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 117 | SH76C | Ventanas de madera | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 118 | SH76D | Ventanas con malla | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 119 | SH76E | Ventanas con cortinas/persianas | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 120 | SH77F | Otro tipo de transporte (caballos, peque-peque, etc.) | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 121 | SH78 | Algún miembro de su hogar es dueño de tierras agricolas | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 122 | SH79 | Cuantas hectareas (1 decimal) | N | 4 | 0:5010, 9996, 9998 | 0 | Menos de 0.1 hectáreas |  |
|  |  |  |  |  |  | 5010 | 501+ |  |
|  |  |  |  |  |  | 9996 | Área dada en otras unidades |  |
|  |  |  |  |  |  | 9998 | No sabe |  |
| 123 | SH224 | Prueba de Yodo | N | 1 | 1:5, 9 | 1 | Sin coloracion (valor "0") |  |
|  |  |  |  |  |  | 2 | Coloracion tenue (valor "7") |  |
|  |  |  |  |  |  | 3 | Coloracion azul o morado (valor "15") |  |
|  |  |  |  |  |  | 4 | Coloracion morado oscuro (valor "30") |  |
|  |  |  |  |  |  | 5 | No hay sal en el hogar |  |
|  |  |  |  |  |  | 9 | No se pudo realizar la prueba |  |
| 124 | SH225U | Visualización de la bolsa de sal | N | 1 | 1:2 | 1 | Vista |  |
|  |  |  |  |  |  | 2 | No vista |  |
| 125 | SH225 | Marca de sal usada por el hogar | N | 2 | 1:37, 96, 98 | 1 | Blanquita |  |
|  |  |  |  |  |  | 2 | Brisal |  |
|  |  |  |  |  |  | 3 | Chavelita |  |
|  |  |  |  |  |  | 4 | Chinita |  |
|  |  |  |  |  |  | 5 | Cholisal |  |
|  |  |  |  |  |  | 6 | Costeñita |  |
|  |  |  |  |  |  | 7 | ElChalandelNorte |  |
|  |  |  |  |  |  | 8 | Elita |  |
|  |  |  |  |  |  | 9 | Elitasal |  |
|  |  |  |  |  |  | 10 | Emsal |  |
|  |  |  |  |  |  | 11 | Esal |  |
|  |  |  |  |  |  | 12 | Extrasal |  |
|  |  |  |  |  |  | 13 | Finita |  |
|  |  |  |  |  |  | 14 | LaCocinera |  |
|  |  |  |  |  |  | 15 | Liberteña |  |
|  |  |  |  |  |  | 16 | Marina |  |
|  |  |  |  |  |  | 17 | Marisal |  |
|  |  |  |  |  |  | 18 | Marsal |  |
|  |  |  |  |  |  | 19 | Mipurita |  |
|  |  |  |  |  |  | 20 | Norsal |  |
|  |  |  |  |  |  | 21 | Norteño |  |
|  |  |  |  |  |  | 22 | Premium |  |
|  |  |  |  |  |  | 23 | Prodesmi |  |
|  |  |  |  |  |  | 24 | Purasal |  |
|  |  |  |  |  |  | 25 | Ricanorteñita |  |
|  |  |  |  |  |  | 26 | Sabrosita |  |
|  |  |  |  |  |  | 29 | SalerinNorteño |  |
|  |  |  |  |  |  | 30 | SaliSal |  |
|  |  |  |  |  |  | 31 | Salimar |  |
|  |  |  |  |  |  | 32 | Salina |  |
|  |  |  |  |  |  | 33 | Supersaladita |  |
|  |  |  |  |  |  | 34 | Suprema |  |
|  |  |  |  |  |  | 35 | Varsal |  |
|  |  |  |  |  |  | 36 | Viva |  |
|  |  |  |  |  |  | 37 | Emsal Marina |  |
|  |  |  |  |  |  | 96 | Otros |  |
|  |  |  |  |  |  | 98 | No sabe |  |
| 126 | SH227 | Prueba de cloro | N | 1 | 1:5, 9 | 1 | Mayor o Igual a 0.5 mg/Lt. | . |
|  |  |  |  |  |  | 2 | De 0.1 mg/Lt. A menos de 0.5 mg/Lt. |  |
|  |  |  |  |  |  | 3 | 0.0 mg/Lt. |  |
|  |  |  |  |  |  | 4 | La toman tal como viene del: Rio, Acequia, Pozo, etc |  |
|  |  |  |  |  |  | 5 | Toman agua embotellada |  |
|  |  |  |  |  |  | 9 | No se pudo realizar la Prueba |  |
| 127 | QH227A | La muestra fue tomada por: | N | 1 | 1:2 | 1 | El funcionario de la encuesta |  |
|  |  |  |  |  |  | 2 | El informante |  |
| 128 | QH227B | La nuestra del agua se extrajo del: | N | 1 | 1:7 | 1 | Grifo o caño |  |
|  |  |  |  |  |  | 2 | Cilindro de metal |  |
|  |  |  |  |  |  | 3 | Balde o batea de plástico |  |
|  |  |  |  |  |  | 4 | Tanque (sin filtro) |  |
|  |  |  |  |  |  | 5 | Tanque (con filtro) |  |
|  |  |  |  |  |  | 7 | Otro |  |
| 129 | HV270 | Índice de riqueza | N | 1 | 1:5 | 1 | Los más pobres |  |
|  |  |  |  |  |  | 2 | Pobre |  |
|  |  |  |  |  |  | 3 | Medio |  |
|  |  |  |  |  |  | 4 | Rico |  |
|  |  |  |  |  |  | 5 | Más rico |  |
| 130 | HV271 | Factor de puntuación del índice de riqueza (5 decimales) | N | 8 |  |  |  |  |


---

# DICCIONARIO DE VARIABLES CUESTIONARIO INDIVIDUAL (REC41)

**ENCUESTA DEMOGRÁFICA Y DE SALUD FAMILIAR ENDES**  
*Módulo:* `1633_embarazo` | *Archivo fuente:* `Diccionario - REC41.pdf` | *Páginas originales:* 8

| Nº | VARIABLE | DESCRIPCIÓN DE LAS VARIABLES | TIPO DE CARÁCTER | LONGITUD | RANGO DE VARIACIÓN | VALORES | DESCRIPCIÓN DE LAS ALTERNATIVAS | OBS |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 1 | ID1 | Año | N | 4 |  |  |  |  |
| 2 | CASEID | Identificación Cuestionario Individual | A | 18 |  |  |  | Variable (Llave de identificación) |
| 3 | MIDX | Orden de historia de nacimiento | N | 1 |  |  |  | Variable (Llave de identificación) |
| 4 | M1 | Durante el embarazo cuantas dosis contra el tétano le aplicaron | N | 1 |  | 0 | No Recibió |  |
|  |  |  |  |  |  | 7 | 7 ó más |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 5 | M1A | Antes del embarazo cuantas dosis de la vacuna contra el tétano recibió | N | 1 | 0:8 | 0 | No Recibió |  |
|  |  |  |  |  |  | 7 | 7 ó más |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 6 | M1B | Mes última inyección contra el tétano antes del embarazo | N | 2 |  | 98 | No sabe el mes |  |
| 7 | M1C | Año de la última inyección contra el tétano antes del embarazo | N | 4 |  | 9998 | No sabe año |  |
| 8 | M1D | Hace cuantos años recibió la última inyección contra el tétano antes del embarazo | N | 2 |  | 98 | No sabe |  |
| 9 | M1E | Última inyección contra el tétano antes del embarazo (CMC) | N | 4 |  | 9996 | No sabe puede determinar |  |
| 10 | M2A | La chequeó en su control prenatal: Médico | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 11 | M2B | La chequeó en su control prenatal: Enfermera | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 12 | M2C | La chequeó en su control prenatal: Obstetra | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 13 | M2D | La chequeó en su control prenatal: Técnico en enfermería | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 14 | M2E | La chequeó en su control prenatal: Promotor de salud | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 15 | M2F | La chequeó en su control prenatal: Asistente de parto entrenado | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 16 | M2G | La chequeó en su control prenatal: Comadrona/partera | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 17 | M2H | La chequeó en su control prenatal: Relativo (no estándar y rara vez se usa) | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 18 | M2I | La chequeó en su control prenatal: CS otra persona | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 19 | M2J | La chequeó en su control prenatal: CS otra persona | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 20 | M2K | La chequeó en su control prenatal: Otro | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 21 | M2L | La chequeó en su control prenatal: CS otro | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 22 | M2M | La chequeó en su control prenatal: CS otro | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 23 | M2N | La chequeó en su control prenatal: Nadie | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 24 | M3A | La atendió en el parto: Médico | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 25 | M3B | La atendió en el parto: Enfermera | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 26 | M3C | La atendió en el parto: Obstetra | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 27 | M3D | La atendió en el parto: Técnico en enfermería | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 28 | M3E | La atendió en el parto: Promotor de salud | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 29 | M3F | La atendió en el parto: Asistente de parto entrenado | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 30 | M3G | La atendió en el parto: Comadrona/partera | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 31 | M3H | La atendió en el parto: Familiar | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 32 | M3I | La atendió en el parto: CS otra persona | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 33 | M3J | La atendió en el parto: CS otra persona | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 34 | M3K | La atendió en el parto: Otro | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 35 | M3L | La atendió en el parto: CS otro | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 36 | M3M | La atendió en el parto: CS otro | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 37 | M3N | La atendió en el parto: Nadie | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 38 | M4 | Duración de la lactancia | N | 2 |  | 94 | Nunca amamantó |  |
|  |  |  |  |  |  | 95 | Aún amamantando |  |
|  |  |  |  |  |  | 98 | No sabe |  |
| 39 | M5 | Meses de amamantamiento | N | 2 |  | 94 | Nunca amamantó |  |
|  |  |  |  |  |  | 98 | No sabe |  |
| 40 | M6 | Duración de la amenorrea | N | 2 |  | 96 | Período no volvió |  |
|  |  |  |  |  |  | 97 | Inconsistente |  |
|  |  |  |  |  |  | 98 | No sabe |  |
| 41 | M7 | Meses de amenorrea | N | 2 |  | 97 | Inconsistente |  |
|  |  |  |  |  |  | 98 | No sabe |  |
| 42 | M8 | Duración de la abstinencia | N | 2 |  | 96 | Aún absteniéndose |  |
|  |  |  |  |  |  | 98 | No sabe |  |
| 43 | M9 | Meses de abstinencia | N | 2 |  | 97 | Inconsistente |  |
|  |  |  |  |  |  | 98 | No sabe |  |
| 44 | M10 | Momento que quería quedar embarazada | N | 1 | 1:3 | 1 | Entonces |  |
|  |  |  |  |  |  | 2 | Esperar más |  |
|  |  |  |  |  |  | 3 | No quería más |  |
| 45 | M11 | Tiempo que hubiera querido esperar | N | 3 |  | 998 | No sabe |  |
| 46 | M13 | Momento del primer control prenatal | N | 2 |  | 98 | No sabe |  |
| 47 | M14 | Visitas prenatales por embarazo | N | 2 |  | 0 | Sin visitas prenatales |  |
|  |  |  |  |  |  | 98 | No sabe |  |
| 48 | M15 | Lugar del parto | N | 2 | 11:12, 21:27, 31:32, 41:42, 96 | 11 | Su domicilio |  |
|  |  |  |  |  |  | 12 | Casa de la partera |  |
|  |  |  |  |  |  | 21 | Hospital MINSA |  |
|  |  |  |  |  |  | 22 | Hospital ESSALUD |  |
|  |  |  |  |  |  | 23 | Hospital FF. AA. PNP |  |
|  |  |  |  |  |  | 24 | Centro de salud MINSA |  |
|  |  |  |  |  |  | 25 | Puesto de salud MINSA |  |
|  |  |  |  |  |  | 26 | Center/Posta ESSALUD |  |
|  |  |  |  |  |  | 27 | Hospital/otro de la Municipalidad |  |
|  |  |  |  |  |  | 31 | Clínica privada |  |
|  |  |  |  |  |  | 32 | Consultorio médico privado |  |
|  |  |  |  |  |  | 41 | Clínica/Posta ONG |  |
|  |  |  |  |  |  | 42 | Hospital/Otro de la Iglesia |  |
|  |  |  |  |  |  | 96 | Otro |  |
| 49 | M17 | Parto por cesárea | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 50 | M18 | Tamaño del niño al nacer | N | 1 | 1:5, 8 | 1 | Muy grande |  |
|  |  |  |  |  |  | 2 | Grande |  |
|  |  |  |  |  |  | 3 | Mediano (normal) |  |
|  |  |  |  |  |  | 4 | Pequeño |  |
|  |  |  |  |  |  | 5 | Muy pequeño |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 51 | M19 | Peso del niño al nacer (kilos - 3 dec.) | N | 4 |  | 9996 | No se pesó al nacer |  |
|  |  |  |  |  |  | 9998 | No sabe |  |
| 52 | M19A | Peso del niño al nacer según recuerda | N | 1 | 0:2, 8, 9 | 0 | No se pesó |  |
|  |  |  |  |  |  | 1 | De la tarjeta |  |
|  |  |  |  |  |  | 2 | Lo que recuerda |  |
|  |  |  |  |  |  | 8 | No sabe |  |
|  |  |  |  |  |  | 9 | Respuesta especial |  |
| 53 | M27 | Marca para lactancia | N | 1 | 0:4 | 0 | Sin bandera |  |
|  |  |  |  |  |  | 1 | > intervalo |  |
|  |  |  |  |  |  | 2 | > intervalo en 1 mes |  |
|  |  |  |  |  |  | 3 | > edad al morir |  |
|  |  |  |  |  |  | 4 | Durante embarazo |  |
| 54 | M28 | Marca para amenorrea | N | 1 | 0:4 | 0 | Sin bandera |  |
|  |  |  |  |  |  | 1 | > intervalo |  |
|  |  |  |  |  |  | 2 | > intervalo en 1 mes |  |
|  |  |  |  |  |  | 4 | Durante embarazo |  |
| 55 | M29 | Marca para abstinencia | N | 1 |  | 0 | Sin bandera |  |
|  |  |  |  |  |  | 1 | > intervalo |  |
|  |  |  |  |  |  | 2 | > intervalo en 1 mes |  |
|  |  |  |  |  |  | 4 | Durante embarazo |  |
| 56 | M34 | Cuando empezó a darle el pecho al niño | N | 3 |  | 0 | Inmediatamente |  |
|  |  |  |  |  |  | 101 | 1 horas: 1 |  |
|  |  |  |  |  |  | 201 | 1 días: 1 |  |
| 57 | M35 | Cuantas veces le dio pecho durante la noche de ayer | N | 2 | 0:36 | 96 | Lo que demanda |  |
| 58 | M36 | Cuantas veces le dio pecho durante el día de ayer | N | 2 | 0:36 | 96 | Lo que demanda |  |
| 59 | M38 | El día de ayer o noche tomó algo en biberón | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 60 | M39 | El día de ayer o durante el dìa o la noche cuantas veces le dio comida sólidas o<br>semisólidas | N | 1 | 0:8 | 0 | Ninguna |  |
|  |  |  |  |  |  | 7 | 7 ó más |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 61 | M42A | Durante su embarazo Durante su embarazo en alguno de sus controles: La pesaron | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 62 | M42B | Durante su embarazo en alguno de sus controles: Le midieron la barriga | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 63 | M42C | Durante su embarazo en alguno de sus controles: Le tomaron le presión arterial | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 64 | M42D | Durante su embarazo en alguno de sus controles: Le hicieron examen de orina | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 65 | M42E | Durante su embarazo en alguno de sus controles: Le hicieron examen de sangre | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 66 | M43 | Le explicaron acerca de las complicaciones que se pueden presentar en el embarazo | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 67 | M44 | Le dijeron dónde acudir si se presentan complicaciones del embarazo | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 68 | M45 | Durante el embarazo, le administraron tabletas, jarabe o inyecciones de hierro | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 69 | M46 | Por cuantos días tomó hierro y/o cuantas inyecciones recibió | N | 3 | 0:360, 998 | 998 | No sabe |  |
| 70 | M47 | Durante el embarazo, tuvo dificultad para ver objetos o personas siendo de día | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 71 | M48 | Durante el embarazo, tuvo dificultad para ver objetos o personas siendo de noche | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 72 | M49A | Durante el embarazo - tomó fansidar para la malaria | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 73 | M49B | Durante el embarazo - tomó cloroquina para la malaria | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 74 | M49C | Durante el embarazo - tomó medicamento para la malaria | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 75 | M49D | Durante el embarazo: tomó un medicamento específico del país para la malaria | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 76 | M49E | Durante el embarazo: tomó un medicamento específico del país para la malaria | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 77 | M49F | Durante el embarazo: tomó un medicamento específico del país para la malaria | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 78 | M49G | Durante el embarazo: tomó un medicamento específico del país para la malaria | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 79 | M49X | Durante el embarazo - tomó otro medicamento para la malaria | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 80 | M49Z | Durante el embarazo: no tomó medicamento para la malaria | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 81 | M51A | Tiempo en que tuvo control después del parto | N | 3 | 100:350, 995, 998 | 100 | La misma hora |  |
|  |  |  |  |  |  | 101 | 1 hora |  |
|  |  |  |  |  |  | 201 | 1 día |  |
|  |  |  |  |  |  | 301 | 1 semana |  |
|  |  |  |  |  |  | 995 | No tuve un chequeo |  |
|  |  |  |  |  |  | 998 | No sabe |  |
| 82 | M54 | Recibió una dosis de vitamina A en los primeros 2 meses después del parto | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 83 | M55A | Durante los primeros 3 días despues del parto, le dieron de tomar: leche, diferente a la<br>leche materna | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 84 | M55B | Durante los primeros 3 días despues del parto, le dieron de tomar: agua sola | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 85 | M55C | Durante los primeros 3 días despues del parto, le dieron de tomar: dextrosa glucosada | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 86 | M55D | Durante los primeros 3 días despues del parto, le dieron de tomar: agua | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 87 | M55E | Durante los primeros 3 días despues del parto, le dieron de tomar: agua azucarada | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 88 | M55F | Durante los primeros 3 días despues del parto, le dieron de tomar: jugo de fruta | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 89 | M55G | Durante los primeros 3 días despues del parto, le dieron de tomar: fórmula para bebes | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 90 | M55H | Durante los primeros 3 días despues del parto, le dieron de tomar: té/infusiones | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 91 | M55I | Durante los primeros 3 días despues del parto, le dieron de tomar: miel | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 92 | M55J | Durante los primeros 3 días despues del parto, le dieron de tomar: país específico | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 93 | M55K | Durante los primeros 3 días despues del parto, le dieron de tomar: país específico | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 94 | M55L | Durante los primeros 3 días despues del parto, le dieron de tomar: país específico | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 95 | M55M | Durante los primeros 3 días despues del parto, le dieron de tomar: país específico | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 96 | M55N | Durante los primeros 3 días, le dieron de tomar: país específico | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 97 | M55X | Durante los primeros 3 días despues del parto, le dieron de tomar: otro | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 98 | M55Z | Durante los primeros 3 días despues del parto, le dieron de tomar: nada | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 99 | M57A | Cuidado prenatal: su hogar | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 100 | M57B | Cuidado prenatal: otro hogar | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 101 | M57C | Cuidado prenatal: CS hogar | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 102 | M57D | Cuidado prenatal: CS hogar | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 103 | M57E | Atención prenatal: Hospital MINSA | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 104 | M57F | Atención prenatal: Centro de salud MINSA | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 105 | M57G | Atención prenatal: Posta médica MINSA | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 106 | M57H | Atención prenatal: Clínica móvil | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 107 | M57I | Atención prenatal: Hospital ESSALUD | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 108 | M57J | Atención prenatal: Hospital FF.AA. y PNP | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 109 | M57K | Atención prenatal: Policlínico/centro/posta ESSALUD | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 110 | M57L | Atención prenatal: Hospital/Otro de la Municipalidad | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 111 | M57M | Atención prenatal: Hospital privado/clínica | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 112 | M57N | Atención prenatal: Clínica móvil particular | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 113 | M57O | Atención prenatal: Médico particular | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 114 | M57P | Atención prenatal: Clínica/Posta de ONG | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 115 | M57Q | Atención prenatal: Hospital/Otro de la Iglesia | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 116 | M57R | Atención prenatal: Otros privados | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 117 | M57S | Atención prenatal: Casa de partera | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 118 | M57T | Atención prenatal: Otro CS | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 119 | M57U | Atención prenatal: Otro CS | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 120 | M57V | Atención prenatal: Otro CS | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 121 | M57X | Atención prenatal: Otro | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 122 | M60 | Durante el embarazo tomó medicamentos contra parásitos intestinales | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 123 | M61 | Tiempo que permaneció en el lugar del parto | N | 3 | 100:350, 998 | 100 | Horas cero |  |
|  |  |  |  |  |  | 201 | Un día |  |
|  |  |  |  |  |  | 301 | Una semana |  |
|  |  |  |  |  |  | 998 | No sabe |  |
| 124 | M62 | Alguien verificó su salud antes del alta | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 125 | M63 | Cuánto tiempo antes del parto se realizó un control de salud | N | 3 | 100:350, 998 | 100 | Horas cero |  |
|  |  |  |  |  |  | 201 | Un día |  |
|  |  |  |  |  |  | 301 | Una semana |  |
|  |  |  |  |  |  | 998 | No sabe |  |
| 126 | M64 | Quién verificó la salud de los encuestados antes del alta | N | 2 | 10:15, 20:22, 96 | 10 | Personal Sanitario |  |
|  |  |  |  |  |  | 11 | Doctor |  |
|  |  |  |  |  |  | 12 | Obstetriz |  |
|  |  |  |  |  |  | 13 | enfermera |  |
|  |  |  |  |  |  | 14 | Sanitario |  |
|  |  |  |  |  |  | 15 | Trabajador de la salud |  |
|  |  |  |  |  |  | 20 | Otra persona |  |
|  |  |  |  |  |  | 21 | Partera tradicional |  |
|  |  |  |  |  |  | 22 | Trabajador de salud de la comunidad/pueblo |  |
|  |  |  |  |  |  | 96 | Otro |  |
| 127 | M65A | Razón no fue a centro de salud: Cuesta mucho | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 128 | M65B | Razón no fue a centro de salud: No está abierto | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 129 | M65C | Razón no fue a centro de salud: Muy lejos, no hay transporte | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 130 | M65D | Razón no fue a centro de salud: No confía en atención | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 131 | M65E | Razón no fue a centro de salud: No había personal femenino | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 132 | M65F | Razón no fue a centro de salud: Nsposo, familia no quería | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 133 | M65G | Razón no fue a centro de salud: No fue necesario | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 134 | M65H | Razón no fue a centro de salud: No acostumbrada | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 135 | M65I | Razón no fue a centro de salud: CS | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 136 | M65J | Razón no fue a centro de salud: CS | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 137 | M65K | Razón no fue a centro de salud: CS | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 138 | M65L | Razón no fue a centro de salud: CS | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 139 | M65X | Razón no fue a centro de salud: otro | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 140 | M66 | Después del parto tuvo algún chequeo o revisiòn médica | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
| 141 | M67 | Cuánto tiempo después del parto se realizó su primer chequeo o revisiòn médica | N | 3 | 100:350, 998 | 100 | Horas cero |  |
|  |  |  |  |  |  | 201 | Un día |  |
|  |  |  |  |  |  | 301 | Una semana |  |
|  |  |  |  |  |  | 998 | No sabe |  |
| 142 | M68 | Quién le realizó su chequeo o revisión médica después del parto | N | 2 |  | 11 | Médico |  |
|  |  |  |  |  |  | 12 | Obstetra |  |
|  |  |  |  |  |  | 13 | Enfermera |  |
|  |  |  |  |  |  | 14 | Técnico en enfermería |  |
|  |  |  |  |  |  | 15 | Promotor de la salud |  |
|  |  |  |  |  |  | 21 | Comadrona/partera |  |
|  |  |  |  |  |  | 96 | Otro |  |
|  |  |  |  |  |  | 11 | Su domicilio |  |
|  |  |  |  |  |  | 12 | Casa de partera |  |
|  |  |  |  |  |  | 21 | Hospital MINSA |  |
|  |  |  |  |  |  | 22 | Hospital ESSALUD |  |
|  |  |  |  |  |  | 23 | Hospital FF. AA. PNP |  |
| 143 | M69 | Donde se chequeo Ud. | N | 2 | 11:12, 20:27, 30:32, 41:42, 96 | 24 | Centro de salud MINSA |  |
|  |  |  |  |  |  | 25 | Puesto de salud MINSA |  |
|  |  |  |  |  |  | 26 | Policlínico/Centro/Posta ESSALUD |  |
|  |  |  |  |  |  | 27 | Hospital/Otro de la Municipalidad |  |
|  |  |  |  |  |  | 31 | Clínica particular |  |
|  |  |  |  |  |  | 32 | Consultorio médico particular |  |
|  |  |  |  |  |  | 41 | Clínica/Posta de ONG |  |
|  |  |  |  |  |  | 42 | Hospital/Otro de la Iglesia |  |
|  |  |  |  |  |  | 96 | Otro |  |
| 144 | M70 | Durante el primer mes le hicieron al bebe algún control o revisión médica | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 145 | M71 | Cuánto tiempo después del parto se realizó el control postnatal | N | 3 | 100:350, 998 | 100 | Horas cero |  |
|  |  |  |  |  |  | 201 | Un día |  |
|  |  |  |  |  |  | 301 | Una semana |  |
|  |  |  |  |  |  | 998 | No sabe |  |
| 146 | M72 | Quién realizó el control posnatal | N | 2 | 10:15, 20:22, 96 | 11 | Médico |  |
|  |  |  |  |  |  | 12 | Obstetra |  |
|  |  |  |  |  |  | 13 | Enfermera |  |
|  |  |  |  |  |  | 14 | Técnico en enfermería |  |
|  |  |  |  |  |  | 15 | Promotor de la salud |  |
|  |  |  |  |  |  | 21 | Comadrona/partera |  |
|  |  |  |  |  |  | 96 | Otro |  |
| 147 | M73 | Dónde le hicieron el chequeo o revisión médica al bebé por primera vez | N | 2 | 10:12, 20:27, 30:32, 41:42, 96 | 11 | Su domicilio |  |
|  |  |  |  |  |  | 12 | Casa de partera |  |
|  |  |  |  |  |  | 21 | Hospital MINSA |  |
|  |  |  |  |  |  | 22 | Hospital ESSALUD |  |
|  |  |  |  |  |  | 23 | Hospital FF. AA. PNP |  |
|  |  |  |  |  |  | 24 | Centro de salud MINSA |  |
|  |  |  |  |  |  | 25 | Puesto de salud MINSA |  |
|  |  |  |  |  |  | 26 | Policlínico/Centro/Posta ESSALUD |  |
|  |  |  |  |  |  | 27 | Hospital/Otro de la Municipalidad |  |
|  |  |  |  |  |  | 31 | Clínica particular |  |
|  |  |  |  |  |  | 32 | Consultorio médico particular |  |
|  |  |  |  |  |  | 41 | Clínica/Posta de ONG |  |
|  |  |  |  |  |  | 42 | Hospital/Otro de la Iglesia |  |
|  |  |  |  |  |  | 96 | Otro |  |


---

# DICCIONARIO DE VARIABLES CUESTIONARIO INDIVIDUAL (REC94)

**ENCUESTA DEMOGRÁFICA Y DE SALUD FAMILIAR ENDES**  
*Módulo:* `1633_embarazo` | *Archivo fuente:* `Diccionario - REC94.pdf` | *Páginas originales:* 4

| Nº | VARIABLE | DESCRIPCIÓN DE LAS VARIABLES | TIPO DE CARÁCTER | LONGITUD | RANGO DE VARIACIÓN | VALORES | DESCRIPCIÓN DE LAS ALTERNATIVAS | OBS |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 1 | ID1 | Año | N | 4 |  |  |  |  |
| 2 | CASEID | Identificación Cuestionario Individual | A | 18 |  |  |  | Variable (Llave de identificación) |
| 3 | IDX94 | Orden de historia de nacimiento | N | 1 | 1:5 |  |  | Variable (Llave de identificación) |
| 4 | S410B | Cuantos meses de embarazo tenía en la última revisión prenatal | N | 2 | 1:9, 98 | 98 | No sabe |  |
| 5 | S411B | En alguno de sus controles: Le midieron la barriga | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 6 | S411F | En alguno de sus controles: Escucharon los latidos del corazón del bebé | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 7 | S411G | En alguno de sus controles: Le hicieron la prueba para descartar Sífilis | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 8 | S411H | En alguno de sus controles: Le hicieron la prueba para descartar de VIH/SIDA | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 9 | S411I | En alguno de sus controles: Le informaron como alimentarse | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 10 | S411J | En alguno de sus controles: Le informaron sobre sus derechos | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 11 | S411K | En alguno de sus controles: Le enseñaron como preparar pezones para lactancia<br>materna | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 12 | S411L | En alguno de sus controles: Le enseñaron como darle el pecho a su bebe | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 13 | S411BA | Cuantos meses de embarazo tenía cuando se realizó la primera prueba de orina | N | 2 | 0:9, 98 | 98 | No sabe el mes |  |
| 14 | S411CA | Cuantos meses de embarazo tenía cuando se realizó el primer análisis de sangre | N | 2 | 0:9, 98 | 98 | No sabe el mes |  |
| 15 | S411DA | Cuantos meses de embarazo tenía cuando se realizó la primera prueba de Sífilis | N | 2 | 0:9, 98 | 98 | No sabe el mes |  |
| 16 | S411EA | Cuantos meses de embarazo tenía cuando se realizó la primera prueba de VIH/SIDA | N | 2 | 0:9, 98 | 98 | No sabe el mes |  |
| 17 | S413 | Durante el embarazo estaba afiliada al SIS | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 18 | S422I | Cantidad de inyecciones de hierro recibidas durante el embarazo | N | 2 | 0:90, 98 | 98 | No sabe |  |
| 19 | S426B | Razón por qué no acudió a un hospital, centro o puesto de salud del MINSA para dar a<br>luz | N | 2 | 11:25, 98 | 11 | No existe en la localidad |  |
|  |  |  |  |  |  | 12 | Quedaba muy lejos |  |
|  |  |  |  |  |  | 13 | No había personal |  |
|  |  |  |  |  |  | 14 | Estaba afiliada a otro servicio de salud |  |
|  |  |  |  |  |  | 15 | Personal daba malos tratos |  |
|  |  |  |  |  |  | 16 | No había privacidad en atención |  |
|  |  |  |  |  |  | 17 | Esposo/Familiar se opuso |  |
|  |  |  |  |  |  | 18 | Por tradición |  |
|  |  |  |  |  |  | 19 | No era higiénico |  |
|  |  |  |  |  |  | 20 | No confia en la atención |  |
|  |  |  |  |  |  | 21 | Personal es descuidado |  |
|  |  |  |  |  |  | 22 | Congestión del servicio |  |
|  |  |  |  |  |  | 23 | No tenía dinero |  |
|  |  |  |  |  |  | 24 | No la quisieron atender |  |
|  |  |  |  |  |  | 25 | Iba camino a establecimiento/Parto se adelantó |  |
|  |  |  |  |  |  | 96 | Otro |  |
| 20 | S426E | La cesárea fue programada | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 21 | S426FA | Cuánto tiempo transcurrió hasta llegar al establecimiento para dar a luz | N | 3 | 100:101, 200:201, 300:301, 99 | 100 | Cero horas |  |
|  |  |  |  |  |  | 101 | Una hora |  |
|  |  |  |  |  |  | 200 | Cero días |  |
|  |  |  |  |  |  | 8 201 | Un día |  |
|  |  |  |  |  |  | 300 | Cero semanas |  |
|  |  |  |  |  |  | 301 | Una semana |  |
|  |  |  |  |  |  | 998 | No sabe |  |
| 22 | S426FB | Cuanto tiempo transcurrió desde que llegó al establecimeinto hasta que fué examinada<br>por personal de salud. | N | 3 | 100:101, 200:201, 300:301, 99 | 100 | Cero horas |  |
|  |  |  |  |  |  | 101 | Una hora |  |
|  |  |  |  |  |  | 200 | Cero días |  |
|  |  |  |  |  |  | 8 201 | Un día |  |
|  |  |  |  |  |  | 300 | Cero semanas |  |
|  |  |  |  |  |  | 301 | Una semana |  |
|  |  |  |  |  |  | 998 | No sabe |  |
| 23 | S426GA | Complicaciones de parto: Parto prolongado | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 24 | S426GB | Complicaciones de parto: Sangrado excesivo | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 25 | S426GC | Complicaciones de parto: Fiebre con sangrado vaginal | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 26 | S426GD | Complicaciones de parto: Convulsiones | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 27 | S426GE | Complicaciones de parto: Otras | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 28 | S430C | El niño fue inscrito en la municipalidad/Oficina Registral de la RENIEC | N | 1 | 0:2, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Sí, muestra partida de nacimiento/DNI |  |
|  |  |  |  |  |  | 2 | Sí, no muestra partida de nacimiento/DNI |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 29 | S430D | La partida/acta tiene Código Único de Identidad (CUI) | N | 1 | 0:1 | 0 | No tiene |  |
|  |  |  |  |  |  | 1 | Si tiene Nro. CIU: DNI |  |
|  |  |  |  |  |  | 2 | Si tiene Nro. CIU: Partida/Acta de nacimiento |  |
| 30 | S431A | En el establecimiento de salud le dieron algo en biberón al bebe después del nacimiento | N | 1 |  | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 31 | S425A | Entrevistada era miembro del seguro de salud materna | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 32 | S432 | El niño está afiliado al Seguro Integral de Salud | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 33 | S432AD | Day affiliation integral health insurance | N | 2 |  | 98 | Otras respuestas |  |
| 34 | S432AM | Mes afiliación seguro de salud integral | N | 2 |  | 98 | Otras respuestas |  |
| 35 | S432AY | Año de afiliación seguro de salud integral | N | 4 |  | 9998 | Otras respuestas |  |
| 36 | S427DA | Complicaciones después del parto: sangrado intenso | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 37 | S427DB | Complicaciones después del parto: pérdida de conciencia | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 38 | S427DC | Complicaciones después del parto: fiebre alta, escalofríos | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 39 | S427DD | Complicaciones después del parto: infección de los senos | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 40 | S427DE | Complicaciones después del parto: dolor al orinar | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 41 | S427DF | Complicaciones después del parto: flujos vaginales | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 42 | S427DG | Complicaciones después del parto: Pérdida involuntaria de orina | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 43 | S427F | Cuando tuvo esas complicaciones recibió atención médica | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 44 | S435 | Por qué no le dio pecho al bebé | N | 2 | 1:8, 96 | 1 | Madre enferma/débil |  |
|  |  |  |  |  |  | 2 | Niña(o) enfermo/débil |  |
|  |  |  |  |  |  | 3 | Niña(o) murió |  |
|  |  |  |  |  |  | 4 | Niña(o) tiene problemas succión |  |
|  |  |  |  |  |  | 5 | Problema de succión pezón |  |
|  |  |  |  |  |  | 6 | No tenía leche |  |
|  |  |  |  |  |  | 7 | Madre trabajando |  |
|  |  |  |  |  |  | 8 | Niña(o) rehusó |  |
|  |  |  |  |  |  | 96 | No sabe |  |
| 45 | S436C | Pusieron al niño en contacto piel a piel con Ud. inmediatamente después del nacimiento | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 46 | S440 | Por qué dejo de darle pecho | N | 2 | 1:12, 96 | 1 | Madre enferma/débil |  |
|  |  |  |  |  |  | 2 | Niña(o) enfermo/débil |  |
|  |  |  |  |  |  | 3 | Niña(o) murió |  |
|  |  |  |  |  |  | 4 | Niña(o) tiene problemas succión |  |
|  |  |  |  |  |  | 5 | Problema de succión pezón |  |
|  |  |  |  |  |  | 6 | No tenía leche |  |
|  |  |  |  |  |  | 7 | Madre trabajaba/estudiaba |  |
|  |  |  |  |  |  | 8 | Niña(o) rehusó |  |
|  |  |  |  |  |  | 9 | Edad de destete |  |
|  |  |  |  |  |  | 10 | Quedó embarazada |  |
|  |  |  |  |  |  | 11 | Comenzó a usar anticonceptivos |  |
|  |  |  |  |  |  | 12 | Niña(o) solo quería pecho |  |
|  |  |  |  |  |  | 96 | No sabe |  |
| 47 | S441 | Recibió alguna capacitación sobre lactancia materna durante el embarazo | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 21 | Hospital MINSA |  |
|  |  |  |  |  |  | 22 | Hospital ESSALUD |  |
|  |  |  |  |  |  | 23 | Hospital FFAA y PNP |  |
|  |  |  |  |  |  | 24 | Centro de salud MINSA |  |
|  |  |  |  |  |  | 25 | Puesto de salud MINSA |  |
| 48 | S442 | En qué lugar recibió capacitación sobre lactancia materna | N | 2 | 21:27, 31:33, 41:42, 96 | 26 | policlínico/Centro/Posta ESSALUD |  |
|  |  |  |  |  |  | 27 | Hospital/Otro de la Municipalidad |  |
|  |  |  |  |  |  | 31 | Clínica particular |  |
|  |  |  |  |  |  | 32 | Consultorio médico particular |  |
|  |  |  |  |  |  | 33 | Casa de partera |  |
|  |  |  |  |  |  | 41 | Clinica/Posta ONG |  |
|  |  |  |  |  |  | 42 | Hospital/Otro de la Iglesia |  |
|  |  |  |  |  |  | 96 | Otro |  |
| 49 | S446AA | Con cuanto tiempo de anticipación preparó el biberón | N | 3 |  | 0 | Inmediatamente |  |
|  |  |  |  |  |  | 100 | Cero minutos |  |
|  |  |  |  |  |  | 101 | Un minuto |  |
|  |  |  |  |  |  | 200 | Cero horas |  |
|  |  |  |  |  |  | 201 | Una hora |  |
|  |  |  |  |  |  | 998 | No sabe |  |
| 50 | S446AB | Donde guardó el biberón | N | 1 |  | 1 | Refrigerador |  |
|  |  |  |  |  |  | 2 | Congelador |  |
|  |  |  |  |  |  | 6 | Otro |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 51 | S446A | Se agregó azúcar a cualquiera de los alimentos del bebé | N | 1 |  | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 52 | S447 | Se agrego azúcar a algun alimento o liquido que comiò o tomò el dìa de ayer | N | 1 | 0:1, 8 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 53 | S448A | Tiempo entre que terminó de preparar los alimentos del bebé y los sirvió | N | 3 |  | 0 | Inmediatamente |  |
|  |  |  |  |  |  | 100 | Cero minutos |  |
|  |  |  |  |  |  | 101 | Un minuto |  |
|  |  |  |  |  |  | 200 | Cero horas |  |
|  |  |  |  |  |  | 201 | Una hora |  |
|  |  |  |  |  |  | 998 | No sabe |  |
| 54 | S448B | Dónde se almacenó la comida | N | 1 |  | 1 | Refrigerador |  |
|  |  |  |  |  |  | 2 | Congelador |  |
|  |  |  |  |  |  | 6 | Otro |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 55 | QI411_M | En alguno de sus controles: le hicieron la prueba para descartar Hepatitis B | N | 1 | 1:2, 8 | 1 | Si |  |
|  |  |  |  |  |  | 2 | No |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 56 | QI411F | Cuántos meses de embarazo tenía en primera prueba para descartar Hepatitis B | N | 2 | 1:9, 98 | 98 | No sabe |  |
| 57 | QI440B | Durante primeros 6 meses, solo recibió leche materna | N | 1 | 1:2, 8, 96 | 1 | Si |  |
|  |  |  |  |  |  | 2 | No |  |
|  |  |  |  |  |  | 8 | No sabe |  |
|  |  |  |  |  |  | 96 | Otro |  |
| 58 | QI422A_A | Durante el embarazo algún personal de salud le realizó una prueba o análisis para<br>descartar anemia | N | 1 | 1:2, 8 | 1 | SI |  |
|  |  |  |  |  |  | 2 | No |  |
|  |  |  |  |  |  | 8 | No sabe/No responde |  |
| 59 | QI422A_B | Durante el embarazo le diagnosticaron o le dijeron que tenía anemia | N | 1 | 1:2, 8 | 1 | SI |  |
|  |  |  |  |  |  | 2 | No |  |
|  |  |  |  |  |  | 8 | No sabe/No responde |  |
| 60 | QI422A_C | Durante el embarazo le indicaron tratamiento con hierro | N | 1 | 1:2, 8 | 1 | SI |  |
|  |  |  |  |  |  | 2 | No |  |
|  |  |  |  |  |  | 8 | No sabe/No responde |  |
| 61 | QI422A_D | Durante el embarazo consumió hierro tal como le indicó el personal de salud | N | 1 | 1:2, 8 | 1 | SI |  |
|  |  |  |  |  |  | 2 | No |  |
|  |  |  |  |  |  | 8 | No sabe/No responde |  |


---

# DICCIONARIO DE VARIABLES CUESTIONARIO INDIVIDUAL (REC44)

**ENCUESTA DEMOGRÁFICA Y DE SALUD FAMILIAR ENDES**  
*Módulo:* `1638_anemia` | *Archivo fuente:* `Diccionario - REC44.pdf` | *Páginas originales:* 2

| Nº | VARIABLE | DESCRIPCIÓN DE LAS VARIABLES | TIPO DE CARÁCTER | LONGITUD | RANGO DE VARIACIÓN | VALORES | DESCRIPCIÓN DE LAS ALTERNATIVAS | OBS |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 1 | ID1 | Año | N | 4 |  |  |  |  |
| 2 | CASEID | Identificación de caso | A | 18 |  |  |  | Variable (Llave de identificación) |
| 3 | HWIDX | Número de orden de la historia del nacimiento | N | 1 | 1:10 |  |  | Variable (Llave de identificación) |
| 4 | HW1 | Edad en meses | N | 2 | 0:59 |  |  |  |
| 5 | HW2 | Peso en kilogramos (1 decimal) | N | 3 | 15:500 |  |  |  |
| 6 | HW3 | Talla en centímetros (1 decimal) | N | 4 | 400:1500 |  |  |  |
| 7 | HW4 | Talla/Edad percentil | N | 4 | 0:9998 | 9998 | Casos marcados |  |
| 8 | HW5 | Talla/Edad de las Desviación Estándar de la mediana de referencia | N | 4 | 0:9998 | 9998 | Casos marcados |  |
| 9 | HW6 | Talla/Edad porcentaje de la mediana de referencia | N | 5 | 0:99998 | 99998 | Casos marcados |  |
| 10 | HW7 | Peso/Edad percentil | N | 4 | 0:9998 | 9998 | Casos marcados |  |
| 11 | HW8 | Peso/Edad Desviación Estándar de la mediana de referencia | N | 4 | 0:9998 | 9998 | Casos marcados |  |
| 12 | HW9 | Peso/Edad porcentaje de la mediana de referencia | N | 5 | 0:99998 | 99998 | Casos marcados |  |
| 13 | HW10 | Peso/Talla percentil | N | 4 | 0:9998 | 9998 | Casos marcados |  |
| 14 | HW11 | Peso/Talla Desviación Estándar de la mediana de referencia | N | 4 | 0:9998 | 9998 | Casos marcados |  |
| 15 | HW12 | Peso/Talla porcentaje de la mediana de referencia | N | 5 | 0:99998 | 99998 | Casos marcados |  |
| 16 | HW13 | Razón por la cual el niño no se midió | N | 1 | 0:7 | 0 | Medido |  |
|  |  |  |  |  |  | 1 | Muerto |  |
|  |  |  |  |  |  | 2 | Enfermo |  |
|  |  |  |  |  |  | 3 | No presente |  |
|  |  |  |  |  |  | 4 | Rechazó |  |
|  |  |  |  |  |  | 5 | Madre rechazó |  |
|  |  |  |  |  |  | 6 | Otro |  |
|  |  |  |  |  |  | 7 | Ninguna medida encontrada en HH |  |
| 17 | HW15 | El niño se midió acostado o de pie | N | 1 | 1:2 | 1 | Acostado |  |
|  |  |  |  |  |  | 2 | De pie |  |
| 18 | HW16 | Día de nacimiento del niño | N | 2 | 1:31 | 97 | Inconsistente |  |
|  |  |  |  |  |  | 98 | No sabe |  |
| 19 | HW17 | Día de la medición | N | 2 | 1:31 |  |  |  |
| 20 | HW18 | Mes de la medición | N | 2 | 1:12 |  |  |  |
| 21 | HW19 | Año de la medición | N | 4 | 2017 |  |  |  |
| 22 | HW51 | Número de orden del padre o responsable | N | 2 | 1:20 | 0 | No en el hogar |  |
| 23 | HW52 | Leyó la declaración de consentimiento para la medición de hemoglobina | N | 1 | 1:2 | 1 | Aceptó |  |
|  |  |  |  |  |  | 2 | Rechazó/Otro |  |
| 24 | HW53 | Nivel de hemoglobina (g /dl -1 decimal) | N | 3 | 45:175 |  |  |  |
| 25 | HW55 | Resultado de la medición (Hemoglobina) | N | 1 | 0:1, 3:4, 6:7 | 0 | Medido |  |
|  |  |  |  |  |  | 1 | Muerto |  |
|  |  |  |  |  |  | 3 | No presente |  |
|  |  |  |  |  |  | 4 | Rechazó |  |
|  |  |  |  |  |  | 6 | Otro |  |
|  |  |  |  |  |  | 7 | Ninguna medida encontrada en HH |  |
| 26 | HW56 | Nivel de hemoglobina ajustada por altitud en g/dl - 1 decimal RM 363-2022-MINSA | N | 4 | 45:175 |  |  |  |
| 27 | HW56A | Nivel de hemoglobina ajustada por altitud en g/dl - 1 decimal NUEVA DIRECTRIZ OMS<br>2024/RM 251-2024-MINSA | N | 4 | 45:175 |  |  |  |
| 28 | HW57 | Nivel de anemia RM 363-2022-MINSA | N | 1 | 1:4 | 1 | Grave |  |
|  |  |  |  |  |  | 2 | Moderado |  |
|  |  |  |  |  |  | 3 | Leve |  |
|  |  |  |  |  |  | 4 | Sin anemia |  |
| 29 | HW57A | Nivel de Anemia NUEVA DIRECTRIZ OMS 2024/RM 251-2024-MINSA | N | 1 | 1:4 | 1 | Grave |  |
|  |  |  |  |  |  | 2 | Moderado |  |
|  |  |  |  |  |  | 3 | Leve |  |
|  |  |  |  |  |  | 4 | Sin anemia |  |
| 30 | HW58 | Está de acuerdocon enviar los datos a un especialista | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 31 | HW70 | Talla/Edad de la Desviación Estándar de la mediana de referencia (según la OMS) | N | 4 | -450:500 | 9996 | Altura fuera de los límites plausibles. |  |
|  |  |  |  |  |  | 9997 | Edad en días fuera de límites plausibles |  |
|  |  |  |  |  |  | 9998 | Casos marcados |  |
| 32 | HW71 | Peso/Edad de la Desviación Estándar de la mediana de referencia (según la OMS) | N | 4 | -450:500 | 9996 | Altura fuera de los límites plausibles. |  |
|  |  |  |  |  |  | 9997 | Edad en días fuera de límites plausibles |  |
|  |  |  |  |  |  | 9998 | Casos marcados |  |
| 33 | HW72 | Peso/Talla Desviación Estándar de la mediana de referencia (según la OMS) | N | 4 | -450:500 | 9996 | Altura fuera de los límites plausibles. |  |
|  |  |  |  |  |  | 9997 | Edad en días fuera de límites plausibles |  |
|  |  |  |  |  |  | 9998 | Casos marcados |  |
| 34 | HW73 | Desviación Estándar del IMC (según la OMS) | N | 4 | -450:500 | 9996 | Altura fuera de los límites plausibles. |  |
|  |  |  |  |  |  | 9997 | Edad en días fuera de límites plausibles |  |
|  |  |  |  |  |  | 9998 | Casos marcados |  |


---

# DICCIONARIO DE VARIABLES CUESTIONARIO INDIVIDUAL (RECH5)

**ENCUESTA DEMOGRÁFICA Y DE SALUD FAMILIAR ENDES**  
*Módulo:* `1638_anemia` | *Archivo fuente:* `Diccionario - RECH5.pdf` | *Páginas originales:* 2

| Nº | VARIABLE | DESCRIPCIÓN DE LAS VARIABLES | TIPO DE CARÁCTER | LONGITUD | RANGO DE VARIACIÓN | VALORES | DESCRIPCIÓN DE LAS ALTERNATIVAS | OBS |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 1 | ID1 | Año | N | 4 |  |  |  |  |
| 2 | HHID | Identificación de caso | N | 15 |  |  |  | Variable (Llave de identificación) |
| 3 | HA0 | Número de orden en el hogar | N | 2 | 1:24 |  |  | Variable (Llave de identificación) |
| 4 | HA1 | Edad de la mujer en años | N | 2 | 12:49 |  |  |  |
| 5 | HA2 | Peso en kilogramos (1 decimal) | N | 4 | 15:500 |  |  |  |
| 6 | HA3 | Talla en centímetros (1 decimal) | N | 4 | 400:1500 |  |  |  |
| 7 | HA4 | Talla/Edad percentil en que se encuentra | N | 4 | 0:9998 | 9998 | Casos marcados |  |
| 8 | HA5 | Talla/Edad Desviación Estándar | N | 4 | 0:9998 | 9998 | Casos marcados |  |
| 9 | HA6 | Talla/Edad porcentaje respecto a la mediana de referencia | N | 5 | 0:99998 | 99998 | Casos marcados |  |
| 10 | HA11 | Peso/Talla desvio estándar (DHS) | N | 4 | 0:9998 | 9998 | Casos marcados |  |
| 11 | HA12 | Peso/Talla Porcentaje respecto a la mediana (DHS) | N | 5 | 0:99998 | 99998 | Casos marcados |  |
| 12 | HA12A | Peso/Talla Porcentaje respecto a la mediana (Foggarty) | N | 5 | 0:99998 | 99998 | Casos marcados |  |
| 13 | HA12B | Peso/Talla Porcentaje respecto a la mediana (OMS) | N | 5 | 0:99998 | 99998 | Casos marcados |  |
| 14 | HA13 | Resultado de medición de la entrevistada | N | 1 | 0, 3:6 | 0 | Medida |  |
|  |  |  |  |  |  | 3 | No presente |  |
|  |  |  |  |  |  | 4 | Rechazó |  |
|  |  |  |  |  |  | 5 | Parcialmente medida |  |
|  |  |  |  |  |  | 6 | Otro |  |
| 15 | HA32 | Fecha de nacimiento (cmc) | N | 4 | 800:1300 |  |  |  |
| 16 | HA33 | Fecha de información completa | N | 1 | 1:8 | 1 | Mes y año |  |
|  |  |  |  |  |  | 2 | Mes y edad |  |
|  |  |  |  |  |  | 3 | Año y edad |  |
|  |  |  |  |  |  | 4 | Año |  |
|  |  |  |  |  |  | 6 | Edad |  |
|  |  |  |  |  |  | 7 | Mes |  |
|  |  |  |  |  |  | 8 | Ninguno |  |
| 17 | HA35 | En las últimas 24 horas cuantos cigarrillos fumó Ud. | N | 2 | 0:25 | 0 | No fuma |  |
| 18 | HA40 | Índice de Masa Corporal para la entrevistada | N | 4 | 1200:6000, 9998 | 9998 | Casos marcados |  |
| 19 | HA41 | Índice de Rohrer para la entrevistada | N | 4 | 800:4500, 9998 | 9998 | Casos marcados |  |
| 20 | HA50 | Grupos de mujeres de 12 a 49 años de edad | N | 1 | 1:2 | 1 | De 12 a 17 años de edad |  |
|  |  |  |  |  |  | 2 | De 18 a 49 años de edad |  |
| 21 | HA51 | Número de orden del padre o responsable | N | 2 | 0:15 | 0 | No es miembro del hogar |  |
| 22 | HA52 | Leyó la declaración de consentimiento para la medición de hemoglobina | N | 1 | 1:2 | 1 | Aceptó |  |
|  |  |  |  |  |  | 2 | Padre/Otro responsable, rechazó |  |
| 23 | HA53 | Nivel de hemoglobina (g/dl - 1 decimal) | N | 3 | 50:250 |  |  |  |
| 24 | HA54 | Actualmente embarazada | N | 1 | 0:1 | 0 | No/No sé |  |
|  |  |  |  |  |  | 1 | Si |  |
| 25 | HA55 | Resultado de la medición (hemoglobina) | N | 1 | 0, 3:6 | 0 | Medida |  |
|  |  |  |  |  |  | 3 | No presente |  |
|  |  |  |  |  |  | 4 | Rechazó |  |
|  |  |  |  |  |  | 5 | Parcialmente medida |  |
|  |  |  |  |  |  | 6 | Otro |  |
| 26 | HA56 | Nivel de hemoglobina ajustado por la altitud (g/dl - 1 decimal) RM 363-2022-MINSA | N | 3 | 40:210 |  |  |  |
| 27 | HA56A | Nivel de hemoglobina ajustada por altitud en g/dl - 1 decimal NUEVA DIRECTRIZ OMS<br>2024/RM 251-2024-MINSA | N | 3 | 40:210 |  |  |  |
| 28 | HA57 | Nivel de anemia RM 363-2022-MINSA | N | 1 | 1:4 | 1 | Grave |  |
|  |  |  |  |  |  | 2 | Moderado |  |
|  |  |  |  |  |  | 3 | Leve |  |
|  |  |  |  |  |  | 4 | Sin anemia |  |
| 29 | HA57A | Nivel de Anemia NUEVA DIRECTRIZ OMS 2024/RM 251-2024-MINSA | N | 1 | 1:4 | 1 | Grave |  |
|  |  |  |  |  |  | 2 | Moderado |  |
|  |  |  |  |  |  | 3 | Leve |  |
|  |  |  |  |  |  | 4 | Sin anemia |  |
| 30 | HA58 | Está de acuerdo con enviar los datos a un especialista | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 31 | HA60 | Estado civil | N | 1 | 1:2 | 1 | Nunca en unión |  |
|  |  |  |  |  |  | 2 | Otro |  |
| 32 | HA61 | Lea la declaración de consentimiento (VIH) | N | 1 | 1:4 | 1 | Aceptó |  |
|  |  |  |  |  |  | 2 | Padre/Otro responsable rechazó |  |
|  |  |  |  |  |  | 3 | Entrevistada rechazó |  |
|  |  |  |  |  |  | 4 | Muestra no probada/perdida/no suficiente DBS |  |
| 33 | HA62 | Número de identificación de la muestra de sangre | A | 5 |  |  |  |  |
| 34 | HA63 | Resultado de la medición (VIH) | N | 1 | 1:6 | 1 | Muestra de sangre tomada |  |
|  |  |  |  |  |  | 2 | No presente |  |
|  |  |  |  |  |  | 3 | Rechazo |  |
|  |  |  |  |  |  | 4 | Muestra no probada/perdida |  |
|  |  |  |  |  |  | 5 | No hay suficiente DBS para completar el protocolo |  |
|  |  |  |  |  |  | 6 | Otro |  |
| 35 | HA64 | Consentimiento para pruebas adicionales | N | 1 | 1:3 | 1 | Aceptada |  |
|  |  |  |  |  |  | 2 | Padres/Otro responsable rechazó |  |
|  |  |  |  |  |  | 3 | Entrevistada rechazó |  |
| 36 | HA65 | Resultado de la entrevista individual a la mujer | N | 1 | 1:7 | 1 | Completa |  |
|  |  |  |  |  |  | 2 | Ausente |  |
|  |  |  |  |  |  | 3 | Aplazada |  |
|  |  |  |  |  |  | 4 | Rechada |  |
|  |  |  |  |  |  | 5 | Incompleta |  |
|  |  |  |  |  |  | 6 | Incapacitada |  |
|  |  |  |  |  |  | 7 | Otro |  |
| 37 | HA66 | El nivel educativo más alto aprobado de la mujer | N | 1 | 0:3, 8 | 0 | Sin educación |  |
|  |  |  |  |  |  | 1 | Primaria |  |
|  |  |  |  |  |  | 2 | Secundaria |  |
|  |  |  |  |  |  | 3 | Superior |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 38 | HA67 | El año más alto de educación de la mujer | N | 2 | 0:6, 98 | 98 | No sabe |  |
| 39 | HA68 | Nivel educativo más alto (CS para el informe preliminar y final) | N | 1 | 0:3, 8 | 0 | Sin educación |  |
|  |  |  |  |  |  | 1 | Primaria |  |
|  |  |  |  |  |  | 2 | Secundaria |  |
|  |  |  |  |  |  | 3 | Superior |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 40 | HA69 | Peso del VIH (6 decimales) | N | 8 |  |  |  |  |


---

# DICCIONARIO DE VARIABLES CUESTIONARIO INDIVIDUAL (RECH6)

**ENCUESTA DEMOGRÁFICA Y DE SALUD FAMILIAR ENDES**  
*Módulo:* `1638_anemia` | *Archivo fuente:* `Diccionario - RECH6.pdf` | *Páginas originales:* 2

| Nº | VARIABLE | DESCRIPCIÓN DE LAS VARIABLES | TIPO DE CARÁCTER | LONGITUD | RANGO DE VARIACIÓN | VALORES | DESCRIPCIÓN DE LAS ALTERNATIVAS | OBS |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 1 | ID1 | Año | N | 4 |  |  |  |  |
| 2 | HHID | Identificación Cuestionario Individual | A | 15 |  |  |  | Variable (Llave de identificación) |
| 3 | HC0 | Número de orden en el hogar | N | 2 |  |  |  | Variable (Llave de identificación) |
| 4 | HC1 | Edad en meses | N | 2 | 0:59 |  |  |  |
| 5 | HC2 | Peso en kilogramos (1 dec.) | N | 4 | 15:500 |  |  |  |
| 6 | HC3 | Altura en centímetros (1 dec.) | N | 4 | 400:1500 |  |  |  |
| 7 | HC4 | Talla/Edad percentil | N | 4 |  | 9998 | Casos marcados |  |
| 8 | HC5 | Talla/Edad Desviación Estándar | N | 4 |  | 9998 | Casos marcados |  |
| 9 | HC6 | Talla/Edad porcentaje de la mediana de referencia | N | 5 |  | 9998 | Casos marcados |  |
| 10 | HC7 | Peso/Edad percentil | N | 4 |  | 9998 | Casos marcados |  |
| 11 | HC8 | Peso/Edad Desviación Estándar | N | 4 |  | 9998 | Casos marcados |  |
| 12 | HC9 | Peso/Edad porcentaje de la mediana de referencia | N | 5 |  | 9998 | Casos marcados |  |
| 13 | HC10 | Peso/Talla percentil | N | 4 |  | 9998 | Casos marcados |  |
| 14 | HC11 | Peso/Talla Desviación Estándar | N | 4 |  | 9998 | Casos marcados |  |
| 15 | HC12 | Peso/Talla Porcentaje de la mediana de referencia | N | 5 |  | 9998 | Casos marcados |  |
| 16 | HC13 | Razón por la cual el niño no se midió | N | 1 | 0, 3:6 | 0 | Medido |  |
|  |  |  |  |  |  | 3 | No presente |  |
|  |  |  |  |  |  | 4 | Rechazó |  |
|  |  |  |  |  |  | 5 | Parcialmente medido |  |
|  |  |  |  |  |  | 6 | Otro |  |
| 17 | HC15 | El niño se midió acostado o de pie | N | 1 | 1:2 | 1 | Acostado |  |
|  |  |  |  |  |  | 2 | De pie |  |
| 18 | HC16 | Día de nacimiento del niño | N | 2 | 1:31 |  |  |  |
| 19 | HC19 | Año de la medición | N | 4 | 2018:2025 |  |  |  |
| 20 | HC27 | Sexo | N | 1 | 1:2 | 1 | Hombre |  |
|  |  |  |  |  |  | 2 | Mujer |  |
| 21 | HC30 | Mes de nacimiento del niño | N | 2 | 1:12;97;98 | 97 | Inconsistente |  |
|  |  |  |  |  |  | 98 | NS |  |
| 22 | HC31 | Año de nacimiento del niño | N | 4 | 2018:2023;9997,9998 | 9997 | Inconsistente |  |
|  |  |  |  |  |  | 9998 | NS |  |
| 23 | HC32 | Fecha de nacimiento (cmc) | N | 4 |  |  |  |  |
| 24 | HC33 | Fecha de información completa | N | 1 |  | 1 | Mes y año |  |
|  |  |  |  |  |  | 2 | Mes y edad |  |
|  |  |  |  |  |  | 3 | Año y edad |  |
|  |  |  |  |  |  | 4 | Año |  |
|  |  |  |  |  |  | 6 | Edad |  |
|  |  |  |  |  |  | 7 | Mes |  |
|  |  |  |  |  |  | 8 | Ninguno |  |
| 25 | HC51 | Número de orden del padre o responsable | N | 2 | 0:20 | 0 | No en el hogar |  |
| 26 | HC52 | Leyó la declaración de consentimiento | N | 1 | 1:2 | 1 | Aceptó |  |
|  |  |  |  |  |  | 2 | Rechazó/otro |  |
| 27 | HC53 | Nivel de hemoglobina (g/dl-1 decimal) | N | 3 |  |  |  |  |
| 28 | HC55 | Resultado de medir (hemoglobina) | N | 1 | 0, 3:4, 6 | 0 | Medido |  |
|  |  |  |  |  |  | 3 | No presente |  |
|  |  |  |  |  |  | 4 | Rechazó |  |
|  |  |  |  |  |  | 6 | Otro |  |
| 29 | HC56 | Nivel de hemoglobina ajustado por altitud (g/dl-1 decimal) RM 363-2022-MINSA | N | 3 |  |  |  |  |
| 30 | HC56A | Nivel de hemoglobina ajustada por altitud en g/dl - 1 decimal NUEVA DIRECTRIZ OMS<br>2024/RM 251-2024-MINSA | N | 3 |  |  |  |  |
| 31 | HC57 | Nivel de anemia RM 363-2022-MINSA | N | 1 | 1:4 | 1 | Grave |  |
|  |  |  |  |  |  | 2 | Moderar |  |
|  |  |  |  |  |  | 3 | Leve |  |
|  |  |  |  |  |  | 4 | Sin anemia |  |
| 32 | HC57A | Nivel de Anemia NUEVA DIRECTRIZ OMS 2024/RM 251-2024-MINSA | N | 1 | 1:4 | 1 | Grave |  |
|  |  |  |  |  |  | 2 | Moderar |  |
|  |  |  |  |  |  | 3 | Leve |  |
|  |  |  |  |  |  | 4 | Sin anemia |  |
| 33 | HC58 | Está de acuerdo con enviar los datos a un especialista | N | 1 |  | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 34 | HC60 | Número de orden de la madre en el hogar | N | 3 | 1:20, 993:995 | 993 | Madre no de facto (MEF que no durmieron la noche anterior) |  |
|  |  |  |  |  |  | 994 | Entrevista incompleta de la MEF |  |
|  |  |  |  |  |  | 995 | Madre no vive en el hogar |  |
| 35 | HC61 | El nivel educativo más alto de la madre | N | 1 | 0:3, 8 | 0 | Sin educación |  |
|  |  |  |  |  |  | 1 | Primaria |  |
|  |  |  |  |  |  | 2 | Secundaria |  |
|  |  |  |  |  |  | 3 | Superior |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 36 | HC62 | El año más alto de educación de la madre | N | 2 | 0:6 |  |  |  |
| 37 | HC63 | Intervalo de los nacimientos anteriores al niño | N | 3 |  |  |  |  |
| 38 | HC64 | Número de orden de nacimiento | N | 2 |  |  |  |  |
| 39 | HC68 | Nivel educativo más alto (CS para informe preliminar y final) | N | 1 | 0:3, 8 | 0 | Sin educación |  |
|  |  |  |  |  |  | 1 | Primaria |  |
|  |  |  |  |  |  | 2 | Secundaria |  |
|  |  |  |  |  |  | 3 | Superior |  |
|  |  |  |  |  |  | 8 | No sabe |  |
| 40 | HC70 | Talla/Edad de la Desviación Estándar de la mediana de referencia (según la OMS) | N | 4 | -450:500 | 9996 | Altura fuera de los límites plausibles. |  |
|  |  |  |  |  |  | 9997 | Edad en días fuera de límites plausibles |  |
|  |  |  |  |  |  | 9998 | Casos marcados |  |
| 41 | HC71 | Peso/Edad de la Desviación Estándar de la mediana de referencia (según la OMS) | N | 4 | -450:500 | 9996 | Altura fuera de los límites plausibles. |  |
|  |  |  |  |  |  | 9997 | Edad en días fuera de límites plausibles |  |
|  |  |  |  |  |  | 9998 | Casos marcados |  |
| 42 | HC72 | Peso/Talla Desviación Estándar de la mediana de referencia (según la OMS) | N | 4 | -450:500 | 9996 | Altura fuera de los límites plausibles. |  |
|  |  |  |  |  |  | 9997 | Edad en días fuera de límites plausibles |  |
|  |  |  |  |  |  | 9998 | Casos marcados |  |
| 43 | HC73 | Desviación Estándar del IMC (según la OMS) | N | 4 | -450:500 | 9996 | Altura fuera de los límites plausibles. |  |
|  |  |  |  |  |  | 9997 | Edad en días fuera de límites plausibles |  |
|  |  |  |  |  |  | 9998 | Casos marcados |  |


---

