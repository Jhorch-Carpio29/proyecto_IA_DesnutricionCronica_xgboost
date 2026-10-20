# DICCIONARIO DE VARIABLES CUESTIONARIO INDIVIDUAL (REC0111)

**ENCUESTA DEMOGRÁFICA Y DE SALUD FAMILIAR ENDES**  
*Módulo:* `1031-mef` | *Archivo fuente:* `Diccionario - REC0111.pdf` | *Páginas originales:* 7

| Nº | VARIABLE | DESCRIPCIÓN DE LAS VARIABLES | TIPO DE CARÁCTER | LONGITUD | RANGO DE VARIACIÓN | VALORES | DESCRIPCIÓN DE LAS ALTERNATIVAS | OBS |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 1 | ID1 | Año | N | 4 |  |  |  |  |
| 2 | CASEID | Identificación Cuestionario Individual | A | 18 |  |  |  | Variable (Llave de identificación) |
| 3 | HHID | Identificación Cuestionario del Hogar | A | 15 |  |  |  |  |
| 4 | V000 | Código y fase del país | A | 3 | PE6 |  |  |  |
| 5 | V001 | Conglomerado | N | 8 | 1:3175 |  |  |  |
| 6 | V002 | Número de vivienda | N | 4 | 1:9998 |  |  |  |
| 7 | V003 | Número de línea de entrevistada | N | 3 | 1:15 |  |  |  |
| 8 | V004 | Unidad de área final | N | 4 | 1:3175 |  |  |  |
| 9 | V007 | Año de la entrevista | N | 4 | 1986:2025 |  |  |  |
| 10 | V008 | Fecha de la entrevista, Codificación centenaria de meses (CMC) | N | 4 |  |  |  |  |
| 11 | Q105DD | Dia de nacimeinto de la entrevistada | N | 2 | 1:31,98 | 98 | No sabe el dia |  |
| 12 | V009 | Mes de nacimiento de la entrevistada | N | 2 | 1:12 |  |  |  |
| 13 | V010 | Año de nacimiento de la entrevistada | N | 4 | 1975:2014 |  |  |  |
| 14 | V011 | Fecha de nacimiento, Codificación centenaria de meses (CMC) | N | 4 |  |  |  |  |
| 15 | V012 | Edad actual - entrevistada | N | 2 | 12:49 |  |  |  |
| 16 | V013 | Edad actual por grupos de 5 años | N | 1 | 1:7 | 0 | De 12 a 14 años de edad |  |
|  |  |  |  |  |  | 1 | De 15 a 19 años de edad |  |
|  |  |  |  |  |  | 2 | De 20 a 24 años de edad |  |
|  |  |  |  |  |  | 3 | De 25 a 29 años de edad |  |
|  |  |  |  |  |  | 4 | De 30 a 34 años de edad |  |
|  |  |  |  |  |  | 5 | De 35 a 39 años de edad |  |
|  |  |  |  |  |  | 6 | De 40 a 44 años de edad |  |
|  |  |  |  |  |  | 7 | De 45 a 49 años de edad |  |
| 17 | V014 | Integridad de la información para la fecha de nacimiento | N | 1 | 1:8 | 1 | Mes y año |  |
|  |  |  |  |  |  | 2 | Mes y edad - año imputado |  |
|  |  |  |  |  |  | 3 | Año y edad - mes imputado |  |
|  |  |  |  |  |  | 4 | Año y edad - año ignorado supera el año de entrevista |  |
|  |  |  |  |  |  | 5 | Año - edad y mes imputados |  |
|  |  |  |  |  |  | 6 | Edad - año y mes imputados |  |
|  |  |  |  |  |  | 7 | Mes - edad y año imputados |  |
|  |  |  |  |  |  | 8 | Ninguno - edad, mes y año imputados |  |
| 18 | V015 | Resultado entrevista individual | N | 1 | 1:7 | 1 | Completa |  |
|  |  |  |  |  |  | 2 | Ausente |  |
|  |  |  |  |  |  | 3 | Aplazada |  |
|  |  |  |  |  |  | 4 | Rechazada |  |
|  |  |  |  |  |  | 5 | Incompleta |  |
|  |  |  |  |  |  | 6 | Discapacitada |  |
|  |  |  |  |  |  | 7 | Otra |  |
| 19 | V017 | Inicio del calendario, Codificación centenaria de mesesl CMC | N | 4 |  |  |  |  |
| 20 | V018 | Columna del mes de la entrevista | N | 2 | 0, 9:18 | 0 | Sin calendario |  |
| 21 | V019 | Duración del calendario | N | 2 | 0, 63:72 | 0 | Sin calendario |  |
| 22 | V019A | Número de columnas de calendario | N | 1 | 0, 4 |  |  |  |
| 23 | V020 | Muestra alguna vez casada | N | 1 | 0:1 | 0 | Toda la mujer muestra |  |
|  |  |  |  |  |  | 1 | Alguna muestra casada |  |
| 24 | V021 | Unidad de muestreo primario - conglomerado | N | 4 | 1:3175 |  |  |  |
| 25 | V023 | Dominio de ejemplo - Departamento | N | 2 | 1:25 | 1 | Amazonas |  |
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
| 26 | V024 | Región | N | 2 | 1:25 | 1 | Amazonas |  |
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
| 27 | V025 | Tipo de lugar de residencia | N | 1 | 1:2 | 1 | Urbano |  |
|  |  |  |  |  |  | 2 | Rural |  |
| 28 | V026 | El lugar de residencia en el que se entrevistó - De Facto | N | 1 | 0:3 | 0 | Capital, gran ciudad |  |
|  |  |  |  |  |  | 1 | Pequeña ciudad |  |
|  |  |  |  |  |  | 2 | Pueblo |  |
|  |  |  |  |  |  | 3 | Campo |  |
| 29 | V027 | Número de visitas | N | 1 | 1:9 |  |  |  |
| 30 | V028 | Identificación del entrevistador | N | 3 | 0:62 |  |  |  |
| 31 | V029 | Identificador del digitador | N | 2 | 0:11 |  |  |  |
| 32 | V030 | Supervisor de campo | N | 3 | 0:62 |  |  |  |
| 33 | V031 | Editor de campo | N | 3 |  |  |  |  |
| 34 | V032 | Editor de la oficina | N | 2 | 0 |  |  |  |
| 35 | V033 | Selección final del área de probabilidad | N | 8 |  |  |  |  |
| 36 | V034 | Número de orden del esposo | N | 2 | 0:16 | 0 | El esposo no está en el hogar |  |
| 37 | V040 | Altitud del conglomerado en metros | N | 4 | 0:5500 |  |  |  |
| 38 | V042 | Selección de hogar para hemoglobina | N | 1 | 0:1 | 0 | No sabeleccionado |  |
|  |  |  |  |  |  | 1 | Seleccionado |  |
| 39 | V043 | Selección para módulo de estatus de mujeres | N | 1 | 0:1 | 0 | Mujer No sabeleccionada |  |
|  |  |  |  |  |  | 1 | Mujer seleccionada |  |
| 40 | V044 | Selección para módulo de violencia domestica | N | 1 | 0:3 | 0 | Mujer No sabeleccionada |  |
|  |  |  |  |  |  | 1 | Mujer seleccionada y entrevistada |  |
|  |  |  |  |  |  | 2 | Mujer seleccionada, pero la privacidad no es posible |  |
|  |  |  |  |  |  | 3 | Mujer seleccionada, pero no entrevistada |  |
| 41 | V101 | Región | N | 2 | 1:25 | 1 | Amazonas |  |
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
| 42 | V102 | Tipo de lugar de residencia | N | 1 | 1:2 | 1 | Urbano |  |
|  |  |  |  |  |  | 2 | Rural |  |
| 43 | V103 | Lugar de residencia de la infancia | N | 1 | 0:4 | 0 | Capital, gran ciudad |  |
|  |  |  |  |  |  | 1 | Ciudad |  |
|  |  |  |  |  |  | 2 | Pueblo |  |
|  |  |  |  |  |  | 3 | Campo |  |
|  |  |  |  |  |  | 4 | En el extranjero |  |
| 44 | V104 | Cuanto tiempo tiene viviendo continuamente en el lugar de residencia actual | N | 2 | 0:49, 95:96 | 95 | Siempre |  |
|  |  |  |  |  |  | 96 | Visitante |  |
|  |  |  |  |  |  | 97 | Inconsistente |  |
|  |  |  |  |  |  | 98 | No sabe |  |
| 45 | V105 | Tipo de lugar de residencia anteriormente | N | 1 | 0:4 | 0 | Capital, gran ciudad |  |
|  |  |  |  |  |  | 1 | Ciudad |  |
|  |  |  |  |  |  | 2 | Pueblo |  |
|  |  |  |  |  |  | 3 | Campo |  |
|  |  |  |  |  |  | 4 | En el extranjero |  |
| 46 | V106 | Nivel educativo más alto | N | 1 | 0:3 | 0 | Sin educación |  |
|  |  |  |  |  |  | 1 | Primario |  |
|  |  |  |  |  |  | 2 | Secundario |  |
|  |  |  |  |  |  | 3 | Superior |  |
| 47 | V107 | Año/grado de educación más alto aprobado | N | 2 | 0:6 |  |  |  |
| 48 | V113 | Fuente principal de abasteciemiento de agua potable que utilizan en su hogar para tomar<br>o beber | N | 2 | 11:13, 21:22, 41:43, 51, 61, 71, 96 | 11 | Dentro de la vivienda |  |
|  |  |  |  |  |  | 12 | Fuera de la vivienda, pero dentro del edificio |  |
|  |  |  |  |  |  | 13 | Pilón/Grifo público |  |
|  |  |  |  |  |  | 21 | Pozo en la casa/patio/lote |  |
|  |  |  |  |  |  | 22 | Pozo Público |  |
|  |  |  |  |  |  | :97 41 | Manantial (puquio) |  |
|  |  |  |  |  |  | 43 | Río/Acequia/Laguna |  |
|  |  |  |  |  |  | 51 | Agua de lluvia |  |
|  |  |  |  |  |  | 61 | Camión tanque/Aguatero |  |
|  |  |  |  |  |  | 71 | Agua embotellada |  |
|  |  |  |  |  |  | 96 | Otro |  |
|  |  |  |  |  |  | 97 | No es residente habitual |  |
| 49 | V115 | Tiempo para llegar a la fuente de agua | N | 3 | 1:240, 996:998 | 996 | En los lugares |  |
|  |  |  |  |  |  | 997 | No residente de jure |  |
| 50 | V116 | Tipo de instalación sanitaria | N | 2 | 11:12, 21:24, 31:32, 96:97 | 11 | Vivienda interior |  |
|  |  |  |  |  |  | 12 | Vivienda exterior |  |
|  |  |  |  |  |  | 21 | Letrina ventilada |  |
|  |  |  |  |  |  | 22 | Pozo séptico |  |
|  |  |  |  |  |  | 23 | Latrina (ciego o negro) |  |
|  |  |  |  |  |  | 24 | Latrina sobre el río/lago |  |
|  |  |  |  |  |  | 31 | Río, canal |  |
|  |  |  |  |  |  | 32 | Sin servicio |  |
|  |  |  |  |  |  | 96 | Otro |  |
|  |  |  |  |  |  | 97 | No es residente habitual |  |
| 51 | V119 | En su hogar tiene: electricidad | N | 1 | 0:1, 7 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 7 | No es residente habitual |  |
| 52 | V120 | En su hogar tiene: radio | N | 1 | 0:1, 7 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 7 | No es residente habitual |  |
| 53 | V121 | En su hogar tiene: televisión | N | 1 | 0:1, 7 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 7 | No es residente habitual |  |
| 54 | V122 | En su hogar tiene: refrigerador | N | 1 | 0:1, 7 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 7 | No es residente habitual |  |
| 55 | V123 | En su hogar tiene: bicicleta | N | 1 | 0:1, 7 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 7 | No es residente habitual |  |
| 56 | V124 | En su hogar tiene: motocicleta/motocar | N | 1 | 0:1, 7 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 7 | No es residente habitual |  |
| 57 | V125 | En su hogar tiene: coche/camión | N | 1 | 0:1, 7 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 7 | No es residente habitual |  |
| 58 | V127 | Material predominante del piso de la vivienda | N | 2 | 11, 21, 31:34, 96:97 | 11 | Tierra/arena |  |
|  |  |  |  |  |  | 21 | Madera (entablados) |  |
|  |  |  |  |  |  | 31 | Parquet o madera pulida |  |
|  |  |  |  |  |  | 32 | Làminas asfálticas, vinílicos o similares |  |
|  |  |  |  |  |  | 33 | Losetas, terrazos o similares |  |
|  |  |  |  |  |  | 34 | Cemento/ladrillo |  |
|  |  |  |  |  |  | 96 | Pona |  |
|  |  |  |  |  |  | 97 | Otro(pona) |  |
| 59 | V128 | Material predominante de las paredes exteriores de la vivienda | N | 2 | 11:13, 21:24, 31:33, 41, 96:97 | 11 | Tablones/madera |  |
|  |  |  |  |  |  | 12 | Estera |  |
|  |  |  |  |  |  | 13 | Caña/bambu/pona/palma/troncos/tabique |  |
|  |  |  |  |  |  | 21 | Adobe o tapia tarrajeados |  |
|  |  |  |  |  |  | 22 | Quincha (caña con barro) |  |
|  |  |  |  |  |  | 23 | Piedra con barro |  |
|  |  |  |  |  |  | 24 | Cartón |  |
|  |  |  |  |  |  | 31 | Ladrillo o /Bloques de cemento |  |
|  |  |  |  |  |  | 32 | Piedra o sillar con cal o cemento |  |
|  |  |  |  |  |  | 33 | Tripley |  |
|  |  |  |  |  |  | 41 | Sin paredes |  |
|  |  |  |  |  |  | 96 | Otro |  |
|  |  |  |  |  |  | 97 | No es residente habitual |  |
| 60 | V129 | Material predominante del techo de la vivienda | N | 2 | 11:12, 21:22, 31:34, 41, 96:97 | 11 | Paja, hojas de palmera etc. |  |
|  |  |  |  |  |  | 12 | Estera |  |
|  |  |  |  |  |  | 21 | Caña o estera con torta de barro |  |
|  |  |  |  |  |  | 22 | Cartón |  |
|  |  |  |  |  |  | 31 | Concreto armado |  |
|  |  |  |  |  |  | 32 | Madera |  |
|  |  |  |  |  |  | 33 | Tejas |  |
|  |  |  |  |  |  | 34 | Plancha de calamina, fibra de cemento o similares |  |
|  |  |  |  |  |  | 41 | Sin techo |  |
|  |  |  |  |  |  | 96 | Otro |  |
|  |  |  |  |  |  | 97 | No es residente habitual |  |
| 61 | V130 | Religión | N | 2 |  |  |  |  |
| 62 | V131 | Etnicidad | N | 2 | 1:12 | 1 | Quechua |  |
|  |  |  |  |  |  | 2 | Aimara |  |
|  |  |  |  |  |  | 3 | Ashaninka |  |
|  |  |  |  |  |  | 4 | Awajún/Aguaruna |  |
|  |  |  |  |  |  | 5 | Shipibo/Konibo |  |
|  |  |  |  |  |  | 6 | Shawi/Chayahuita |  |
|  |  |  |  |  |  | 7 | Matsigenka/ Machiguenga |  |
|  |  |  |  |  |  | 8 | Achuar |  |
|  |  |  |  |  |  | 9 | Otra lengua nativa u originaria |  |
|  |  |  |  |  |  | 10 | Castellano |  |
|  |  |  |  |  |  | 11 | Portugués |  |
|  |  |  |  |  |  | 12 | Otra lengua extranjera |  |
| 63 | V133 | Educación en años simples | N | 2 | 0:18 | 97 | Inconsistente |  |
| 64 | V134 | El lugar en el que se realizó la entrevista De-facto | N | 1 | 0:3 | 0 | Capital, ciudad grande |  |
|  |  |  |  |  |  | 1 | Ciudad pequeña |  |
|  |  |  |  |  |  | 2 | Pueblo |  |
|  |  |  |  |  |  | 3 | Campo |  |
| 65 | V135 | Residente habitual o visitante | N | 1 | 1:2 | 1 | Residente habitual |  |
|  |  |  |  |  |  | 2 | Visitante |  |
| 66 | V136 | Número de miembros del hogar | N | 2 | 1:24 |  |  |  |
| 67 | V137 | Número de niños de 6 años de edad | N | 2 | 0:10 |  |  |  |
| 68 | V138 | Número de mujeres de 15 a 49 años de edad elegibles en el hogar | N | 2 | 1:24 |  |  |  |
|  |  |  |  |  |  | 0 | En el extranjero |  |
| 69 | V139 | Región, residencia habitual De-jure | N | 2 | 0:25, 97 | 1 | Amazonas |  |
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
|  |  |  |  |  |  | 97 | No es residente habitual |  |
| 70 | V140 | Tipo de área de residencia De-jure | N | 1 | 1:2, 7 | 1 | Área urbana |  |
|  |  |  |  |  |  | 2 | Área rural |  |
|  |  |  |  |  |  | 7 | No es residente habitual |  |
| 71 | V141 | Lugar de residencia De-jure | N | 1 | 0:3, 7 | 0 | Capital, ciudad grande |  |
|  |  |  |  |  |  | 1 | Ciudad pequeña |  |
|  |  |  |  |  |  | 2 | Pueblo |  |
|  |  |  |  |  |  | 3 | Campo |  |
|  |  |  |  |  |  | 7 | No es residente habitual |  |
| 72 | V149 | Logro educativo | N | 1 | 0:5 | 0 | Sin educación |  |
|  |  |  |  |  |  | 1 | Primaria incompleta |  |
|  |  |  |  |  |  | 2 | Primaria completa |  |
|  |  |  |  |  |  | 3 | Secundaria incompleta |  |
|  |  |  |  |  |  | 4 | Secundaria completa |  |
|  |  |  |  |  |  | 5 | Superior |  |
| 73 | V150 | Relación con el jefe del hogar | N | 2 | 1:12, 15, 98 | 1 | Jefe del hogar |  |
|  |  |  |  |  |  | 2 | Esposa/esposo |  |
|  |  |  |  |  |  | 3 | Hijo/Hija |  |
|  |  |  |  |  |  | 4 | Yerno/Nuera |  |
|  |  |  |  |  |  | 5 | Nieto/Nieta |  |
|  |  |  |  |  |  | 6 | Padre/Madre |  |
|  |  |  |  |  |  | 7 | Suegro/Suegra |  |
|  |  |  |  |  |  | 8 | Hermano/a |  |
|  |  |  |  |  |  | 9 | Conviviente |  |
|  |  |  |  |  |  | 10 | Otro pariente |  |
|  |  |  |  |  |  | 11 | Hijo adoptado/hijo de crianza |  |
|  |  |  |  |  |  | 12 | Sin parentesco |  |
|  |  |  |  |  |  | 15 | Empleada domésdtica |  |
|  |  |  |  |  |  | 98 | No sabe |  |
| 74 | V151 | Sexo del Jefe del Hogar | N | 1 | 1:2 | 1 | Hombre |  |
|  |  |  |  |  |  | 2 | Mujer |  |
| 75 | V152 | Edad del jefe del hogar | N | 2 | 15:98 | 97 | 97+ |  |
|  |  |  |  |  |  | 98 | NS |  |
| 76 | V153 | En su hogar tiene: teléfono | N | 1 | 0:1, 7 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 7 | No es residente habitual |  |
| 77 | AWFACTT | Factor todas las mujeres - total | N | 5 | 100 |  |  |  |
| 78 | AWFACTU | Factor todas las mujeres - urbano/rural | N | 5 | 100 |  |  |  |
| 79 | AWFACTR | Factor todas las mujeres - regional | N | 5 | 100 |  |  |  |
| 80 | AWFACTE | Factor todas las mujeres - educación | N | 5 | 100 |  |  |  |
| 81 | AWFACTW | Factor todas las mujeres - índice de riqueza | N | 5 | 100 |  |  |  |
| 82 | V155 | Alfabetización | N | 1 | 0:4 | 0 | No puede leer |  |
|  |  |  |  |  |  | 1 | Puede leer sólo parte de la frase |  |
|  |  |  |  |  |  | 2 | Puede leer la frase |  |
|  |  |  |  |  |  | 3 | No hay tarjeta en el idioma requerido |  |
|  |  |  |  |  |  | 4 | Ciega/problemas visuales |  |
| 83 | V156 | Alguna vez participó en un programa de alfabetización (no incluyendo la escuela<br>primaria) | N | 1 | 0:1 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
| 84 | V157 | Frecuencia de lectura de un periódico o revista | N | 1 | 0:3 | 0 | Nunca |  |
|  |  |  |  |  |  | 1 | De vez en cuando |  |
|  |  |  |  |  |  | 2 | Una vez por semana |  |
|  |  |  |  |  |  | 3 | Casi todos los días |  |
| 85 | V158 | Frecuencia de escuchar radio | N | 1 | 0:3 | 0 | Nunca |  |
|  |  |  |  |  |  | 1 | De vez en cuando |  |
|  |  |  |  |  |  | 2 | Una vez por semana |  |
|  |  |  |  |  |  | 3 | Casi todos los días |  |
| 86 | V159 | Frecuencia de ver televisión | N | 1 | 0:3 | 0 | Nunca |  |
|  |  |  |  |  |  | 1 | De vez en cuando |  |
|  |  |  |  |  |  | 2 | Una vez por semana |  |
|  |  |  |  |  |  | 3 | Casi todos los días |  |
| 87 | V160 | Baño compartido con otros hogares | N | 1 | 0:1, 7 | 0 | No |  |
|  |  |  |  |  |  | 1 | Si |  |
|  |  |  |  |  |  | 7 | No es residente habitual |  |
| 88 | V161 | Tipo de combustible para cocinar | N | 2 | 1:11, 95:97 | 1 | Electricidad |  |
|  |  |  |  |  |  | 2 | Gas Licuado (GLP) |  |
|  |  |  |  |  |  | 3 | Gas natural(Tuberia) |  |
|  |  |  |  |  |  | 5 | Kerosene |  |
|  |  |  |  |  |  | 6 | Carbón mineral |  |
|  |  |  |  |  |  | 7 | Carbon vegetal |  |
|  |  |  |  |  |  | 8 | Leña |  |
|  |  |  |  |  |  | 9 | Cañas/Arbustos (secos) |  |
|  |  |  |  |  |  | 10 | Residuos agricolas |  |
|  |  |  |  |  |  | 11 | Bosta |  |
|  |  |  |  |  |  | 95 | No cocina |  |
|  |  |  |  |  |  | 96 | Otro |  |
|  |  |  |  |  |  | 97 | No es residente habitual |  |
| 89 | V166 | Resultados de la prueba del yodo en la sal | N | 3 | 0, 7, 15, 30, 994:995, 997 | 0 | Sin coloración - 0 ppm (sin yodo) |  |
|  |  |  |  |  |  | 7 | Coloración tenue - 7 ppm |  |
|  |  |  |  |  |  | 15 | Coloración azul o morado - 15 ppm |  |
|  |  |  |  |  |  | 30 | Coloración morado oscuro - 30 ppm a más |  |
|  |  |  |  |  |  | 994 | No se pudo realizar la prueba |  |
|  |  |  |  |  |  | 995 | No hay sal en el hogar |  |
| 90 | V167 | Número de viajes en los últimos 12 meses | N | 2 |  |  |  |  |
| 91 | V168 | Afuera más de un mes en los últimos 12 meses | N | 1 |  |  |  |  |
| 92 | ML101 | Tipo de mosquitero que utilizo para dormir última noche | N | 1 |  |  |  |  |
| 93 | QD333_1 | Alguna dificultad o limitación permanente para ver, aún usando anteojos | N | 1 | 1:2 | 1 | Si |  |
|  |  |  |  |  |  | 2 | No |  |
| 94 | QD333_2 | Alguna dificultad o limitación permanente para oir, aún usando audífonos | N | 1 | 1:2 | 1 | Si |  |
|  |  |  |  |  |  | 2 | No |  |
| 95 | QD333_3 | Alguna dificultad o limitación permanente para hablar o comunicarse, aún usando la<br>lengua de señas u otro | N | 1 | 1:2 | 1 | Si |  |
|  |  |  |  |  |  | 2 | No |  |
| 96 | QD333_4 | Alguna dificultad o limitación permanente para moverse o caminar para usar brazos y/o<br>piernas | N | 1 | 1:2 | 1 | Si |  |
|  |  |  |  |  |  | 2 | No |  |
| 97 | QD333_5 | Alguna dificultad o limitación permanente para entender o aprender (concentrarse y<br>recordarse) | N | 1 | 1:2 | 1 | Si |  |
|  |  |  |  |  |  | 2 | No |  |
| 98 | QD333_6 | Alguna dificultad o limitación permanente para relacionarse con los demás, por sus<br>pensamientos, sentimientos, emociones o conductas | N | 1 | 1:2 | 1 | Si |  |
|  |  |  |  |  |  | 2 | No |  |
| 99 | UBIGEO | Código de Ubicación Gegráfica | A | 6 |  |  |  |  |
| 100 | V022 | Estratos | N | 8 | 1:250 |  |  |  |
| 101 | V005 | Factor de ponderacion | N | 8 |  |  |  |  |
| 102 | V190 | Índice de riqueza | N | 1 | 1:5 | 1 | El más pobre |  |
|  |  |  |  |  |  | 2 | Pobrer |  |
|  |  |  |  |  |  | 3 | Medio |  |
|  |  |  |  |  |  | 4 | Rico |  |
|  |  |  |  |  |  | 5 | Más rico |  |
| 103 | V191 | Factor de puntuación del índice de riqueza (5 decimales) | N | 8 |  |  |  |  |
| 104 | mujeres12a49 | Mujeres de 12 a 49 años de edad | N | 8 | 0:2 | 0 | Mujeres de 12 a 14 de edad, nunca embarazadas |  |
|  |  |  |  |  |  | 1 | Mujeres de 12 a 49 de edad, alguna vez emabrazadas |  |
|  |  |  |  |  |  | 2 | Mujeres de 15 a 49 años de edad |  |
