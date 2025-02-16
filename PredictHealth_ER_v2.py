import streamlit as st
from datetime import datetime
import numpy as np
import pandas as pd
import pickle
import os

# mapeo prestadores publico - privado
prestadores_publico_privado_dict = {'CLINICA MEDELLIN OCCIDENTE': 0, 'IPS SURA LAS VEGAS MEDELLIN': 0, 'CLINICA CENTRAL FUNDADORES': 0, 'IPS SURA INDUSTRIALES MEDELLIN': 0, 'UNIDAD HOSPITALARIA SANTA CRUZ VÍCTOR CÁRDENAS JARAMILLO': 1, 'FUNDACION HOSPITALARIA SAN VICENTE DE PAUL': 0, 'HOSPITAL GENERAL DE MEDELLÍN LUZ CASTRO DE GUTIERREZ, EMPRESA SOCIAL DEL ESTADO': 1, 'UNIDAD HOSPITALARIA DE BELEN HECTOR ABAD GOMEZ': 1, 'UNIDAD HOSPITALARIA DE MANRRIQUE HERMENEGILDO DE FEX': 1, 'CLINICA DEL PRADO CIUDAD DEL RIO': 0, 'CENTRO DE SALUD SANTO DOMINGO': 1, 'UNIDAD HOSPITALARIA SAN CRISTOBAL LEONARDO BETANCUR TABORDA': 1, 'UNIDAD HOSPITALARIA SAN JAVIER JESÚS PELÁEZ BOTERO': 1, 'CORPORACIÓN HOSPITAL INFANTIL CONCEJO DE MEDELLÍN': 0, 'CLINICA CARDIO VID': 0, 'UNIDAD HOSPITALARIA NUEVO OCCIDENTE': 1, 'UNIDAD HOSPITALARIA DOCE DE OCTUBRE LUIS CARLOS GALAN SARMIENTO': 1, 'UNIDAD HOSPITALARIA DE CASTILLA JAIME TOBON ARBELAEZ': 1, 'HOSPITAL PABLO TOBON URIBE': 0, 'SEDE PRINCIPAL HOSPITAL ALMA MÁTER DE ANTIOQUIA': 0, 'UNIDAD HOSPITALARIA SAN ANTONIO DE PRADO DIEGO ECHAVARRIA MISAS': 1, 'CORPORACIÓN PARA ESTUDIOS EN SALUD CLINICA CES': 0, 'CLINICA EL ROSARIO SEDE CENTRO': 0, 'NUEVA CLINICA SAGRADO CORAZON S.A.S': 0, 'UNIDAD DE SALUD MENTAL': 1, 'CLINICA MEDELLIN POBLADO': 0, 'CLINICA UNIVERSITARIA BOLIVARIANA': 0, 'CLINICA EL ROSARIO SEDE EL TESORO': 0, 'INVERSIONES MEDICAS DE ANTIOQUIA S.A. CLINICA LAS VEGAS': 0, 'FUNDACIÓN INSTITUTO NEUROLOGICO DE COLOMBIA': 0, 'CLÍNICA LAS AMERICAS': 0, 'TRAUMACENTRO S.A.A': 0, 'FUNDACION COLOMBIANA DE CANCEROLOGIA CLINICA VIDA': 0, 'CLINICA DE CIRUGIA AMBULATORIA CONQUISTADORES': 0, 'E.S.E. HOSPITAL LA MARIA': 1, 'CLINICA MEDELLIN S.A': 0, 'SEDE ADMINISTRATIVA EDIFICIO SACATIN': 1, 'SOCIEDAD MEDICA ANTIOQUEÑA S.A. SOMA': 0, 'COOPERATIVA DE SALUD SAN ESTEBAN': 0, 'AUNA CENTRO MÉDICO LAS AMÉRICAS SEDE ARKADIA': 0, 'VIRREY SOLÍS IPS. S.A TRANVÍA PLAZA': 0, 'CLINISANITAS MEDELLIN': 0, 'IPS SURA LOS MOLINOS MEDELLIN': 0, 'VIRREY SOLIS I.P.S S.A SAN DIEGO': 0, 'VIRREY SOLIS IPS FLORIDA': 0, 'ENDOGINE IPS SAS': 0, 'IPS SURA SAN DIEGO': 0}

# mapeo prestadores
prestadores_dict_HOSPITAL = {'AUNA CENTRO MÉDICO LAS AMÉRICAS SEDE ARKADIA': 0, 'CENTRO DE SALUD SANTO DOMINGO': 0, 'CLINICA CARDIO VID': 0, 'CLINICA CENTRAL FUNDADORES': 0, 'CLINICA DE CIRUGIA AMBULATORIA CONQUISTADORES': 0, 'CLINICA DEL PRADO CIUDAD DEL RIO': 0, 'CLINICA EL ROSARIO SEDE CENTRO': 0, 'CLINICA EL ROSARIO SEDE EL TESORO': 0, 'CLINICA MEDELLIN OCCIDENTE': 0, 'CLINICA MEDELLIN POBLADO': 0, 'CLINICA MEDELLIN S.A': 0, 'CLINICA UNIVERSITARIA BOLIVARIANA': 0, 'CLINISANITAS MEDELLIN': 0, 'CLÍNICA LAS AMERICAS': 0, 'COOPERATIVA DE SALUD SAN ESTEBAN': 0, 'CORPORACIÓN HOSPITAL INFANTIL CONCEJO DE MEDELLÍN': 1, 'CORPORACIÓN PARA ESTUDIOS EN SALUD CLINICA CES': 0, 'E.S.E. HOSPITAL LA MARIA': 1, 'ENDOGINE IPS SAS': 0, 'FUNDACION COLOMBIANA DE CANCEROLOGIA CLINICA VIDA': 0, 'FUNDACION HOSPITALARIA SAN VICENTE DE PAUL': 1, 'FUNDACIÓN INSTITUTO NEUROLOGICO DE COLOMBIA': 0, 'HOSPITAL GENERAL DE MEDELLÍN LUZ CASTRO DE GUTIERREZ, EMPRESA SOCIAL DEL ESTADO': 1, 'HOSPITAL PABLO TOBON URIBE': 1, 'INVERSIONES MEDICAS DE ANTIOQUIA S.A. CLINICA LAS VEGAS': 0, 'IPS SURA INDUSTRIALES MEDELLIN': 0, 'IPS SURA LAS VEGAS MEDELLIN': 0, 'IPS SURA LOS MOLINOS MEDELLIN': 0, 'IPS SURA SAN DIEGO': 0, 'NUEVA CLINICA SAGRADO CORAZON S.A.S': 0, 'SEDE ADMINISTRATIVA EDIFICIO SACATIN': 0, 'SEDE PRINCIPAL HOSPITAL ALMA MÁTER DE ANTIOQUIA': 1, 'SOCIEDAD MEDICA ANTIOQUEÑA S.A. SOMA': 0, 'TRAUMACENTRO S.A.A': 0, 'UNIDAD DE SALUD MENTAL': 0, 'UNIDAD HOSPITALARIA DE BELEN HECTOR ABAD GOMEZ': 1, 'UNIDAD HOSPITALARIA DE CASTILLA JAIME TOBON ARBELAEZ': 1, 'UNIDAD HOSPITALARIA DE MANRRIQUE HERMENEGILDO DE FEX': 1, 'UNIDAD HOSPITALARIA DOCE DE OCTUBRE LUIS CARLOS GALAN SARMIENTO': 1, 'UNIDAD HOSPITALARIA NUEVO OCCIDENTE': 1, 'UNIDAD HOSPITALARIA SAN ANTONIO DE PRADO DIEGO ECHAVARRIA MISAS': 1, 'UNIDAD HOSPITALARIA SAN CRISTOBAL LEONARDO BETANCUR TABORDA': 1, 'UNIDAD HOSPITALARIA SAN JAVIER JESÚS PELÁEZ BOTERO': 1, 'UNIDAD HOSPITALARIA SANTA CRUZ VÍCTOR CÁRDENAS JARAMILLO': 1, 'VIRREY SOLIS I.P.S S.A SAN DIEGO': 0, 'VIRREY SOLIS IPS FLORIDA': 0, 'VIRREY SOLÍS IPS. S.A TRANVÍA PLAZA': 0}

prestadores_dict_IPS = {'AUNA CENTRO MÉDICO LAS AMÉRICAS SEDE ARKADIA': 0, 'CENTRO DE SALUD SANTO DOMINGO': 0, 'CLINICA CARDIO VID': 0, 'CLINICA CENTRAL FUNDADORES': 0, 'CLINICA DE CIRUGIA AMBULATORIA CONQUISTADORES': 0, 'CLINICA DEL PRADO CIUDAD DEL RIO': 0, 'CLINICA EL ROSARIO SEDE CENTRO': 0, 'CLINICA EL ROSARIO SEDE EL TESORO': 0, 'CLINICA MEDELLIN OCCIDENTE': 0, 'CLINICA MEDELLIN POBLADO': 0, 'CLINICA MEDELLIN S.A': 0, 'CLINICA UNIVERSITARIA BOLIVARIANA': 0, 'CLINISANITAS MEDELLIN': 0, 'CLÍNICA LAS AMERICAS': 0, 'COOPERATIVA DE SALUD SAN ESTEBAN': 0, 'CORPORACIÓN HOSPITAL INFANTIL CONCEJO DE MEDELLÍN': 0, 'CORPORACIÓN PARA ESTUDIOS EN SALUD CLINICA CES': 0, 'E.S.E. HOSPITAL LA MARIA': 0, 'ENDOGINE IPS SAS': 1, 'FUNDACION COLOMBIANA DE CANCEROLOGIA CLINICA VIDA': 0, 'FUNDACION HOSPITALARIA SAN VICENTE DE PAUL': 0, 'FUNDACIÓN INSTITUTO NEUROLOGICO DE COLOMBIA': 0, 'HOSPITAL GENERAL DE MEDELLÍN LUZ CASTRO DE GUTIERREZ, EMPRESA SOCIAL DEL ESTADO': 0, 'HOSPITAL PABLO TOBON URIBE': 0, 'INVERSIONES MEDICAS DE ANTIOQUIA S.A. CLINICA LAS VEGAS': 0, 'IPS SURA INDUSTRIALES MEDELLIN': 1, 'IPS SURA LAS VEGAS MEDELLIN': 1, 'IPS SURA LOS MOLINOS MEDELLIN': 1, 'IPS SURA SAN DIEGO': 1, 'NUEVA CLINICA SAGRADO CORAZON S.A.S': 0, 'SEDE ADMINISTRATIVA EDIFICIO SACATIN': 0, 'SEDE PRINCIPAL HOSPITAL ALMA MÁTER DE ANTIOQUIA': 0, 'SOCIEDAD MEDICA ANTIOQUEÑA S.A. SOMA': 0, 'TRAUMACENTRO S.A.A': 0, 'UNIDAD DE SALUD MENTAL': 0, 'UNIDAD HOSPITALARIA DE BELEN HECTOR ABAD GOMEZ': 0, 'UNIDAD HOSPITALARIA DE CASTILLA JAIME TOBON ARBELAEZ': 0, 'UNIDAD HOSPITALARIA DE MANRRIQUE HERMENEGILDO DE FEX': 0, 'UNIDAD HOSPITALARIA DOCE DE OCTUBRE LUIS CARLOS GALAN SARMIENTO': 0, 'UNIDAD HOSPITALARIA NUEVO OCCIDENTE': 0, 'UNIDAD HOSPITALARIA SAN ANTONIO DE PRADO DIEGO ECHAVARRIA MISAS': 0, 'UNIDAD HOSPITALARIA SAN CRISTOBAL LEONARDO BETANCUR TABORDA': 0, 'UNIDAD HOSPITALARIA SAN JAVIER JESÚS PELÁEZ BOTERO': 0, 'UNIDAD HOSPITALARIA SANTA CRUZ VÍCTOR CÁRDENAS JARAMILLO': 0, 'VIRREY SOLIS I.P.S S.A SAN DIEGO': 1, 'VIRREY SOLIS IPS FLORIDA': 1, 'VIRREY SOLÍS IPS. S.A TRANVÍA PLAZA': 1}

# mapeo municipios
municipio_dict_1 = {'ABEJORRAL': 2, 'ABREGO': 0, 'ABRIAQUI': 0, 'ACACIAS': 0, 'ACANDI': 0, 'ACEVEDO': 0, 'ACHI': 0, 'AGRADO': 0, 'AGUA DE DIOS': 0, 'AGUACHICA': 0, 'AGUADA': 0, 'AGUADAS': 0, 'AGUAZUL': 0, 'ALBAN': 0, 'ALBANIA': 0, 'ALCALA': 0, 'ALDANA': 0, 'ALEJANDRIA': 1, 'ALGARROBO': 0, 'ALMEIDA': 0, 'ALPUJARRA': 0, 'ALTAMIRA': 0, 'ALTO BAUDO (PIE DE PATO)': 0, 'ALTOS DEL ROSARIO': 0, 'AMAGA': 2, 'AMALFI': 1, 'ANAPOIMA': 0, 'ANDALUCIA': 0, 'ANDES': 2, 'ANGELOPOLIS': 1, 'ANGOSTURA': 1, 'ANORI': 1, 'ANSERMA': 0, 'ANSERMANUEVO': 0, 'ANTIOQUIA': 1, 'ANZA': 1, 'ANZOATEGUI': 0, 'APARTADO': 2, 'APIA': 0, 'ARACATACA': 0, 'ARAUCA': 0, 'ARAUQUITA': 0, 'ARBOLEDA (BERRUECOS)': 0, 'ARBOLETES': 1, 'ARGELIA': 1, 'ARJONA': 0, 'ARMENIA': 1, 'ARMERO (GUAYABAL)': 0, 'ASTREA': 0, 'ATACO': 0, 'ATRATO': 0, 'AYAPEL': 0, 'BAGADO': 0, 'BAHIA SOLANO (MUTIS)': 1, 'BAJO BAUDO (PIZARRO)': 0, 'BALBOA': 0, 'BARANOA': 0, 'BARBACOAS': 0, 'BARBOSA': 2, 'BARICHARA': 0, 'BARRANCABERMEJA': 1, 'BARRANCAS': 0, 'BARRANCO DE LOBA': 0, 'BARRANQUILLA (DISTRITO ESPECIAL  INDUSTRIAL Y PORTUARIO DE BARRANQUILLA)': 1, 'BECERRIL': 0, 'BELALCAZAR': 0, 'BELEN': 0, 'BELLO': 4, 'BELMIRA': 1, 'BELTRAN': 0, 'BETANIA': 1, 'BETULIA': 1, 'BOAVITA': 0, 'BOCHALEMA': 0, 'BOJACA': 0, 'BOJAYA (BELLAVISTA)': 0, 'BOLIVAR': 1, 'BOSCONIA': 0, 'BOYACA': 0, 'BRICEÑO': 1, 'BUCARAMANGA': 1, 'BUENAVENTURA': 0, 'BUENAVISTA': 0, 'BUENOS AIRES': 0, 'BUESACO': 0, 'BUGA': 0, 'BUGALAGRANDE': 0, 'BURITICA': 1, 'CABRERA': 0, 'CACERES': 1, 'CACHIPAY': 0, 'CAICEDO': 2, 'CAICEDONIA': 0, 'CAIMITO': 0, 'CAJAMARCA': 0, 'CAJICA': 0, 'CALAMAR': 0, 'CALARCA': 0, 'CALDAS': 2, 'CALDONO': 0, 'CALI (SANTIAGO DE CALI)': 1, 'CALIFORNIA': 0, 'CALIMA (DARIEN)': 0, 'CALOTO': 0, 'CAMPAMENTO': 1, 'CAMPO DE LA CRUZ': 0, 'CAMPOHERMOSO': 0, 'CANALETE': 0, 'CANDELARIA': 0, 'CANTAGALLO': 0, 'CANTON DE SAN PABLO (MANAGRU)': 0, 'CAQUEZA': 0, 'CARACOLI': 1, 'CARAMANTA': 1, 'CARCASI': 0, 'CAREPA': 1, 'CARMEN APICALA': 0, 'CARMEN DE CARUPA': 0, 'CARMEN DE VIBORAL': 1, 'CAROLINA': 1, 'CARTAGENA (DISTRITO TURISTICO Y CULTURAL DE CARTAGENA)': 1, 'CARTAGENA DEL CHAIRA': 0, 'CARTAGO': 0, 'CASTILLA LA NUEVA': 0, 'CAUCASIA': 2, 'CAÑASGORDAS': 1, 'CERETE': 0, 'CHALAN': 0, 'CHAPARRAL': 0, 'CHARTA': 0, 'CHIA': 0, 'CHIGORODO': 1, 'CHIMA': 0, 'CHIMICHAGUA': 0, 'CHINACOTA': 0, 'CHINCHINA': 0, 'CHINU': 0, 'CHIPAQUE': 0, 'CHIQUINQUIRA': 0, 'CHIRIGUANA': 0, 'CHITA': 0, 'CHIVOLO': 0, 'CHOACHI': 0, 'CHOCONTA': 0, 'CICUCO': 0, 'CIENAGA': 0, 'CIENAGA DE ORO': 0, 'CIMITARRA': 0, 'CIRCASIA': 0, 'CISNEROS': 1, 'CLEMENCIA': 0, 'COCORNA': 1, 'COGUA': 0, 'COLOMBIA': 0, 'COLON (GENOVA)': 0, 'CONCEPCION': 1, 'CONCORDIA': 1, 'CONDOTO': 0, 'CONVENCION': 0, 'COPACABANA': 2, 'CORDOBA': 0, 'CORINTO': 0, 'COROMORO': 0, 'COROZAL': 0, 'COTA': 0, 'COTORRA': 0, 'CUCUTA': 1, 'CUCUTILLA': 0, 'CUMARAL': 0, 'CUMARIBO': 0, 'CUNDAY': 0, 'CURILLO': 0, 'CURUMANI': 0, 'DABEIBA': 1, 'DAGUA': 0, 'DISTRACCION': 0, 'DON MATIAS': 2, 'DOS QUEBRADAS': 0, 'DUITAMA': 0, 'EBEJICO': 1, 'EL AGUILA': 0, 'EL BAGRE': 1, 'EL BANCO': 0, 'EL CARMEN': 0, 'EL CARMEN DE ATRATO': 1, 'EL CARMEN DE BOLIVAR': 0, 'EL CHARCO': 0, 'EL COLEGIO': 0, 'EL COPEY': 0, 'EL DONCELLO': 0, 'EL DORADO': 0, 'EL ENCANTO': 0, 'EL PASO': 0, 'EL PEÑOL': 0, 'EL PEÑON': 0, 'EL PIÑON': 0, 'EL PLAYON': 0, 'EL RETORNO': 0, 'EL TAMBO': 0, 'EL ZULIA': 0, 'ENCINO': 0, 'ENCISO': 0, 'ENTRERRIOS': 1, 'ENVIGADO': 3, 'ESPINAL': 0, 'FACATATIVA': 0, 'FILADELFIA': 0, 'FLANDES': 0, 'FLORENCIA': 0, 'FLORESTA': 0, 'FLORIDA': 0, 'FLORIDABLANCA': 0, 'FOMEQUE': 0, 'FONSECA': 0, 'FRANCISCO PIZARRO (SALAHONDA)': 0, 'FREDONIA': 1, 'FRESNO': 0, 'FRONTINO': 1, 'FUENTE DE ORO': 0, 'FUNDACION': 0, 'FUNZA': 0, 'FUSAGASUGA': 0, 'GALAPA': 0, 'GALERAS (NUEVA GRANADA)': 0, 'GAMA': 0, 'GAMARRA': 0, 'GARZON': 0, 'GIGANTE': 0, 'GIRALDO': 1, 'GIRARDOT': 0, 'GIRARDOTA': 2, 'GIRON': 0, 'GOMEZ PLATA': 1, 'GRANADA': 1, 'GUACARI': 0, 'GUACHUCAL': 0, 'GUADALUPE': 1, 'GUADUAS': 0, 'GUAITARILLA': 0, 'GUAMAL': 0, 'GUAMO': 0, 'GUARANDA': 0, 'GUARNE': 2, 'GUATAPE': 1, 'GUATAQUI': 0, 'GUATAVITA': 0, 'GUATICA': 0, 'GUAYABAL DE SIQUIMA': 0, 'HATILLO DE LOBA': 0, 'HATONUEVO': 0, 'HELICONIA': 1, 'HISPANIA': 1, 'HONDA': 0, 'IBAGUE': 1, 'INZA': 0, 'IPIALES': 0, 'ISNOS (SAN JOSE DE ISNOS)': 0, 'ISTMINA': 1, 'ITAGUI': 3, 'ITUANGO': 1, 'JAMUNDI': 0, 'JARDIN': 1, 'JERICO': 1, 'JERUSALEN': 0, 'JORDAN': 0, 'JUAN DE ACOSTA': 0, 'JURADO': 0, 'LA APARTADA': 0, 'LA ARGENTINA': 0, 'LA BELLEZA': 0, 'LA CALERA': 0, 'LA CAPILLA': 0, 'LA CEJA': 2, 'LA CELIA': 0, 'LA CUMBRE': 0, 'LA DORADA': 0, 'LA ESTRELLA': 2, 'LA FLORIDA': 0, 'LA GLORIA': 0, 'LA HORMIGA (VALLE DEL GUAMUEZ)': 0, 'LA JAGUA IBIRICO': 0, 'LA MACARENA': 0, 'LA MERCED': 0, 'LA MESA': 0, 'LA MONTAÑITA': 0, 'LA PAZ': 0, 'LA PINTADA': 1, 'LA PLATA': 0, 'LA PLAYA': 0, 'LA SALINA': 0, 'LA SIERRA': 0, 'LA TEBAIDA': 0, 'LA UNION': 1, 'LA VEGA': 0, 'LA VICTORIA': 0, 'LA VIRGINIA': 0, 'LANDAZURI': 0, 'LEBRIJA': 0, 'LEJANIAS': 0, 'LERIDA': 0, 'LETICIA': 0, 'LIBANO': 0, 'LIBORINA': 1, 'LINARES': 0, 'LITORAL DEL BAJO SAN JUAN (SANTA GENOVEVA DE DOCORDO)': 0, 'LLORO': 0, 'LOPEZ (MICAY)': 0, 'LORICA': 0, 'LOS CORDOBAS': 0, 'LOS PALMITOS': 0, 'LOS PATIOS': 0, 'MACANAL': 0, 'MACEO': 1, 'MADRID': 0, 'MAGANGUE': 0, 'MAICAO': 0, 'MAJAGUAL': 0, 'MALAGA': 0, 'MALAMBO': 0, 'MANATI': 0, 'MANAURE (BALCON DEL CESAR)': 0, 'MANI': 0, 'MANIZALES': 1, 'MANTA': 0, 'MANZANARES': 0, 'MARGARITA': 0, 'MARIA LA BAJA': 0, 'MARINILLA': 2, 'MARIQUITA': 0, 'MARMATO': 0, 'MARSELLA': 0, 'MEDELLIN': 4, 'MEDINA': 0, 'MEDIO ATRATO': 0, 'MEDIO BAUDO': 0, 'MELGAR': 0, 'MERCADERES': 0, 'MESETAS': 0, 'MILAN': 0, 'MIRAFLORES': 0, 'MIRANDA': 0, 'MIRITI-PARANA': 0, 'MISTRATO': 0, 'MITU': 0, 'MOCOA': 0, 'MOMIL': 0, 'MOMPOS': 0, 'MONIQUIRA': 0, 'MONTEBELLO': 2, 'MONTECRISTO': 0, 'MONTELIBANO': 1, 'MONTENEGRO': 0, 'MONTERIA': 1, 'MONTERREY': 0, 'MORALES': 0, 'MORROA': 0, 'MOSQUERA': 0, 'MOÑITOS': 0, 'MURINDO': 1, 'MUTATA': 1, 'MUZO': 0, 'NARIÑO': 1, 'NECHI': 1, 'NECOCLI': 1, 'NEIRA': 0, 'NEIVA': 0, 'NILO': 0, 'NORCASIA': 0, 'NOVITA': 0, 'NUQUI': 0, 'OCAMONTE': 0, 'OCAÑA': 0, 'OIBA': 0, 'OLAYA': 1, 'OLAYA HERRERA (BOCAS DE SATINGA)': 0, 'ORITO': 0, 'OVEJAS': 0, 'PACHO': 0, 'PACORA': 0, 'PAEZ (BELALCAZAR)': 0, 'PAILITAS': 0, 'PAJARITO': 0, 'PALERMO': 0, 'PALMAR': 0, 'PALMAS DEL SOCORRO': 0, 'PALMIRA': 0, 'PALMITO': 0, 'PAMPLONA': 0, 'PANA PANA (CAMPO ALEGRE)': 0, 'PARAMO': 0, 'PASTO (SAN JUAN DE PASTO)': 0, 'PAZ DEL RIO': 0, 'PEDRAZA': 0, 'PELAYA': 0, 'PENSILVANIA': 0, 'PEQUE': 1, 'PEREIRA': 1, 'PEÑOL': 1, 'PIAMONTE': 0, 'PIEDECUESTA': 0, 'PIEDRAS': 0, 'PINCHOTE': 0, 'PINILLOS': 0, 'PITAL': 0, 'PITALITO': 0, 'PLANADAS': 0, 'PLANETA RICA': 0, 'PLATO': 0, 'POLICARPA': 0, 'POLO NUEVO': 0, 'POPAYAN': 0, 'PORE': 0, 'POTOSI': 0, 'PRADERA': 0, 'PRADO': 0, 'PROVIDENCIA': 0, 'PUEBLO BELLO': 0, 'PUEBLO NUEVO': 0, 'PUEBLO RICO': 0, 'PUEBLORRICO': 1, 'PUENTE NACIONAL': 0, 'PUERTO ASIS': 0, 'PUERTO BERRIO': 2, 'PUERTO BOYACA': 1, 'PUERTO COLOMBIA': 0, 'PUERTO ESCONDIDO': 0, 'PUERTO GUZMAN': 0, 'PUERTO LIBERTADOR': 0, 'PUERTO LOPEZ': 0, 'PUERTO NARE (LA MAGDALENA)': 1, 'PUERTO NARIÑO': 0, 'PUERTO PARRA': 0, 'PUERTO RICO': 0, 'PUERTO RONDON': 0, 'PUERTO SALGAR': 0, 'PUERTO SANTANDER': 0, 'PUERTO TRIUNFO': 1, 'PUERTO WILCHES': 0, 'PURIFICACION': 0, 'QUETAME': 0, 'QUIBDO (SAN FRANCISCO DE QUIBDO)': 2, 'QUIMBAYA': 0, 'QUINCHIA': 0, 'RAGONVALIA': 0, 'RAMIRIQUI': 0, 'RAQUIRA': 0, 'REGIDOR': 0, 'REMEDIOS': 1, 'REPELON': 0, 'RESTREPO': 0, 'RETIRO': 1, 'RICAURTE': 0, 'RIO DE ORO': 0, 'RIOBLANCO': 0, 'RIOFRIO': 0, 'RIOHACHA': 0, 'RIONEGRO': 2, 'RIOQUITO': 0, 'RIOSUCIO': 0, 'RISARALDA': 0, 'ROBERTO PAYAN (SAN JOSE)': 0, 'ROLDANILLO': 0, 'ROSAS': 0, 'SABANA DE TORRES': 0, 'SABANAGRANDE': 0, 'SABANALARGA': 1, 'SABANETA': 3, 'SAHAGUN': 0, 'SALAMINA': 0, 'SALDAÑA': 0, 'SALENTO': 0, 'SALGAR': 1, 'SAMANA': 0, 'SAMANIEGO': 0, 'SAMPUES': 0, 'SAN AGUSTIN': 0, 'SAN ALBERTO': 0, 'SAN ANDRES': 1, 'SAN ANDRES SOTAVENTO': 0, 'SAN ANTERO': 0, 'SAN ANTONIO': 1, 'SAN ANTONIO DEL TEQUENDAMA': 0, 'SAN BENITO': 0, 'SAN BENITO ABAD': 0, 'SAN BERNARDO': 0, 'SAN BERNARDO DEL VIENTO': 0, 'SAN CALIXTO': 0, 'SAN CARLOS': 1, 'SAN CARLOS DE GUAROA': 0, 'SAN CAYETANO': 0, 'SAN CRISTOBAL': 1, 'SAN DIEGO': 0, 'SAN FELIPE': 0, 'SAN FERNANDO': 0, 'SAN FRANCISCO': 1, 'SAN GIL': 0, 'SAN JACINTO': 0, 'SAN JACINTO DEL CAUCA': 0, 'SAN JERONIMO': 1, 'SAN JOSE': 0, 'SAN JOSE DE FRAGUA': 0, 'SAN JOSE DE LA MONTAÑA': 1, 'SAN JOSE DE MIRANDA': 0, 'SAN JOSE DEL GUAVIARE': 0, 'SAN JOSE DEL PALMAR': 0, 'SAN JUAN DE ARAMA': 0, 'SAN JUAN DE BETULIA': 0, 'SAN JUAN DE URABA': 1, 'SAN JUAN DEL CESAR': 0, 'SAN JUAN NEPOMUCENO': 0, 'SAN LUIS': 1, 'SAN LUIS DE CUBARRAL': 0, 'SAN MARCOS': 0, 'SAN MARTIN': 0, 'SAN MIGUEL': 0, 'SAN MIGUEL DE SEMA': 0, 'SAN ONOFRE': 0, 'SAN PABLO': 0, 'SAN PEDRO': 2, 'SAN PEDRO DE URABA': 1, 'SAN PELAYO': 0, 'SAN RAFAEL': 1, 'SAN ROQUE': 1, 'SAN SEBASTIAN': 0, 'SAN SEBASTIAN DE BUENAVISTA': 0, 'SAN VICENTE': 1, 'SAN VICENTE DEL CAGUAN': 0, 'SANTA ANA': 0, 'SANTA BARBARA': 2, 'SANTA BARBARA (ISCUANDE)': 0, 'SANTA CATALINA': 0, 'SANTA CRUZ (GUACHAVES)': 0, 'SANTA FE DE BOGOTA, D. C.': 2, 'SANTA HELENA DEL OPON': 0, 'SANTA LUCIA': 0, 'SANTA MARIA': 0, 'SANTA MARTA (DISTRITO TURISTICO  CULTURAL E HISTORICODE SANTA MARTA)': 1, 'SANTA RITA': 0, 'SANTA ROSA': 0, 'SANTA ROSA DE CABAL': 0, 'SANTA ROSA DE OSOS': 2, 'SANTA ROSA DE VITERBO': 0, 'SANTA ROSA DEL SUR': 0, 'SANTA ROSALIA': 0, 'SANTAFE DE BOGOTA D.C.-CHAPINERO': 0, 'SANTAFE DE BOGOTA D.C.-CIUDAD BOLIVAR': 0, 'SANTAFE DE BOGOTA D.C.-ENGATIVA': 0, 'SANTAFE DE BOGOTA D.C.-SAN CRISTOBAL': 0, 'SANTAFE DE BOGOTA D.C.-SANTA FE': 0, 'SANTANA': 0, 'SANTANDER DE QUILICHAO': 0, 'SANTIAGO': 0, 'SANTO DOMINGO': 1, 'SANTO TOMAS': 0, 'SANTUARIO': 1, 'SARAVENA': 0, 'SARDINATA': 0, 'SASAIMA': 0, 'SATIVASUR': 0, 'SEGOVIA': 2, 'SEVILLA': 0, 'SILVANIA': 0, 'SILVIA': 0, 'SIMACOTA': 0, 'SIMITI': 0, 'SINCE': 0, 'SINCELEJO': 1, 'SIPI': 0, 'SOACHA': 0, 'SOATA': 0, 'SOGAMOSO': 0, 'SOLANO': 0, 'SOLEDAD': 0, 'SONSON': 1, 'SOPETRAN': 1, 'SOPO': 0, 'SOTAQUIRA': 0, 'SUAZA': 0, 'SUBACHOQUE': 0, 'SUCRE': 0, 'SUPIA': 0, 'SURATA': 0, 'SUTATAUSA': 0, 'TABIO': 0, 'TADO': 0, 'TAMALAMEQUE': 0, 'TAME': 0, 'TAMESIS': 1, 'TARAZA': 1, 'TARSO': 1, 'TEORAMA': 0, 'TIBU': 0, 'TIERRALTA': 0, 'TIMBIO': 0, 'TIQUISIO (PUERTO RICO)': 0, 'TITIRIBI': 1, 'TOCAIMA': 0, 'TOCANCIPA': 0, 'TOLEDO': 1, 'TOLU': 0, 'TOLUVIEJO': 0, 'TOPAIPI': 0, 'TORO': 0, 'TOTORO': 0, 'TRINIDAD': 0, 'TRUJILLO': 0, 'TULUA': 0, 'TUMACO': 0, 'TUNJA': 0, 'TUQUERRES': 0, 'TURBACO': 0, 'TURBO': 2, 'UBATE': 0, 'ULLOA': 0, 'UNGUIA': 0, 'UNION PANAMERICANA': 0, 'URAMITA': 1, 'URIBIA': 0, 'URRAO': 2, 'USIACURI': 0, 'VALDIVIA': 1, 'VALENCIA': 0, 'VALLE DE SAN JUAN': 0, 'VALLE SAN JOSE': 0, 'VALLEDUPAR': 1, 'VALPARAISO': 1, 'VEGACHI': 1, 'VELEZ': 0, 'VENECIA': 1, 'VENECIA (OSPINA PEREZ)': 0, 'VERGARA': 0, 'VERSALLES': 0, 'VICTORIA': 0, 'VIGIA DEL FUERTE': 0, 'VILLA DEL ROSARIO': 0, 'VILLACARO': 0, 'VILLAHERMOSA': 0, 'VILLAMARIA': 0, 'VILLANUEVA': 0, 'VILLAVICENCIO': 1, 'VILLAVIEJA': 0, 'VILLETA': 0, 'VISTAHERMOSA': 0, 'VITERBO': 0, 'YACOPI': 0, 'YALI': 1, 'YARUMAL': 2, 'YOLOMBO': 1, 'YONDO': 1, 'YOPAL': 0, 'YOTOCO': 0, 'YUMBO': 0, 'ZAMBRANO': 0, 'ZAPATOCA': 0, 'ZARAGOZA': 1, 'ZARZAL': 0, 'ZIPAQUIRA': 0}

# mapeo tipo usuario
tipo_usuario_map = {1:"Contributivo", 2:"Subsidiado", 3: "Vinculado", 4:"Particular", 5:"Otro", 6:"Víctima con afiliación al Régimen Contributivo",
                    7:"Víctima con afiliación al Régimen subsidiado", 8:"Víctima no asegurado (Vinculado)"}

# mapeo dia semana
dia_semana_map = {
    'Lunes': 0, 'Martes': 1, 'Miércoles': 2, 'Jueves': 3, 
    'Viernes': 4, 'Sábado': 5, 'Domingo': 6}


# mapeo sexo
sexo_map = {1:"Masculino", 0:"Femenino"}  # Asume valores 'M' y 'F' para Masculino y Femenino

causa_externa_map = {1:"Accidente de trabajo", 2:"Accidente de tránsito", 3:"Accidente rábico", 4:"Accidente ofídico",
                     5:"Otro tipo de accidente", 6:"Evento catastrófico", 7:"Lesión por agresión", 8:"Lesión auto infligida",
                     9:"Sospecha de maltrato físico", 10:"Sospecha de abuso sexual", 11:"Sospecha de violencia sexual",
                     12:"Sospecha de maltrato emocional", 13:"Enfermedad general", 14:"Enfermedad laboral", 15: "Otra"}

# # Cargar el modelo
# with open("lgb_model_early_stop_2.pkl", "rb") as file:
#     model = pickle.load(file)

# Cargar el modelo
with open("best_xgb_07_02.pkl", "rb") as file:
    model = pickle.load(file)

# Crear dos columnas para organizar el logo y el título
t1, t2 = st.columns([1, 5])  # Ajusta la proporción según sea necesario

# Coloca la imagen en la columna de la derecha
with t1:
    st.image("logo.png", width=120)

# Coloca el título en la columna de la izquierda
with t2:
    st.markdown("""
    <h1 style='text-align: left; margin-top: -20px;'>Predicción Destino del Paciente en Urgencias</h1>
    <p style='text-align: left; margin-top: -10px;'>Introduce los datos del paciente para realizar la predicción.</p>
    """, unsafe_allow_html=True)

########################################################################################################

# Configurar valores iniciales en session_state
if "nombre_paciente" not in st.session_state:
    st.session_state["nombre_paciente"] = ""
if "apellido" not in st.session_state:
    st.session_state["apellido"] = ""
# Crear columnas para organizar los campos
col1, col2 = st.columns(2)

with col1:
    st.session_state["nombre_paciente"] = st.text_input(
        "Nombre del paciente", value=st.session_state["nombre_paciente"]
    )
nombre_paciente = st.session_state["nombre_paciente"]

# Campo de texto para el apellido en la segunda columna
with col2:
    st.session_state["apellido"] = st.text_input(
        "Apellido del paciente", value=st.session_state["apellido"]
    )
apellido = st.session_state["apellido"]

########################################################################################################

############################################################################################################################

# Crear entradas para las variables

# Crear columnas para organizar los campos
col3, col4 = st.columns(2)
# Selector de fecha
with col3:
    fecha = st.date_input("Fecha de ingreso", value=datetime.now().date())
    Mes = fecha.month
    # Mes = 9
    # Aplicar transformación cíclica
    Mes_sin_f = np.sin(2 * np.pi * Mes / 12) 
    Mes_cos_f = np.cos(2 * np.pi * Mes / 12)
    # Mes_sin_f = -1
    # Mes_cos_f = -1.84
    Dia_del_mes = fecha.day
    anio = fecha.year

# Selector de hora
with col4:
    hora = st.time_input("Hora de ingreso")
    HoraIngreso = hora.hour

#Selector día de la semana
# Obtener el día de la semana en español
dias_semana = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

# Convertir fecha a día de la semana en español
Dia_de_la_semana_nombre = dias_semana[pd.Timestamp(fecha).day_name()]

# Mapear el día de la semana al número según el diccionario
Dia_de_la_semana = dia_semana_map[Dia_de_la_semana_nombre]

######################################################################################

if "Edad" not in st.session_state:
    st.session_state["Edad"] = ""

# Crear columnas para organizar los campos
col5, col6 = st.columns(2)

with col5:
# Ingresar Edad
    st.session_state["Edad"] = st.text_input(
    "Edad (años)", value=st.session_state["Edad"]
    )
    Edad = st.session_state["Edad"]

    try:
        Edad = int(Edad)
            # Edad = st.number_input("Edad (años)", min_value=0, max_value=120)
        if Edad < 12:
            Grupo_etario = 3
        elif 12 <= Edad < 18:
            Grupo_etario = 0
        elif 18 <= Edad < 60:
            Grupo_etario = 1
        else:
            Grupo_etario = 2
    except:
        st.warning("Por favor, introduce una edad válida (un número entero).")
############################################################################################################################

# if "Sexo" not in st.session_state:
#     st.session_state["Sexo"] = ""

with col6:
    
#     # Crear las opciones del selector
#     options = ["Seleccione el sexo del paciente"] + list(sexo_map.values())
#     sexo_seleccionado = st.selectbox(
#         "Sexo",
#         options=options
#     )

#     # Inicializar codigo_sexo como None
#     codigo_sexo = None

#     # Validar si el usuario seleccionó una opción válida
#     if sexo_seleccionado != "Seleccione el sexo del paciente":
#         # Buscar el código correspondiente al sexo seleccionado
#         for codigo, nombre in sexo_map.items():
#             if nombre == sexo_seleccionado:
#                 codigo_sexo = codigo
#                 break


########

    # Inicializar el valor del sexo seleccionado en session_state
    if "sexo_seleccionado" not in st.session_state:
        st.session_state["sexo_seleccionado"] = "Seleccione el sexo del paciente"

    # Crear las opciones del selector
    options = ["Seleccione el sexo del paciente"] + list(sexo_map.values())

    # Selector con estado gestionado
    st.session_state["sexo_seleccionado"] = st.selectbox(
        "Sexo",
        options=options,
        index=options.index(st.session_state["sexo_seleccionado"]),
    )

    # Obtener el sexo seleccionado desde session_state
    sexo_seleccionado = st.session_state["sexo_seleccionado"]

    # Inicializar codigo_sexo como None
    codigo_sexo = None

    # Validar si el usuario seleccionó una opción válida
    if sexo_seleccionado != "Seleccione el sexo del paciente":
        # Buscar el código correspondiente al sexo seleccionado
        for codigo, nombre in sexo_map.items():
            if nombre == sexo_seleccionado:
                codigo_sexo = codigo
                break
    
        # Mostrar el resultado (opcional)
    if codigo_sexo is not None:
        st.success(f"Sexo seleccionado correctamente")
    else:
        st.warning("Por favor, selecciona una opción válida.")


############################################################################################################################


# # Crear una lista desplegable con solo las claves (nombres de los municipios)
# options = ["Seleccione un municipio"] + list(municipio_dict_1.keys())
# municipio_seleccionado = st.selectbox(
#     "Nombre del municipio donde reside",
#     options=options
# )

# # Verificar si el usuario seleccionó una opción válida
# if municipio_seleccionado == "Seleccione un municipio":
#     st.warning("Por favor, seleccione un municipio válido.")
# else:
#     # Obtener el código del municipio seleccionado usando el diccionario
#     CodigoMunicipio = municipio_dict_1[municipio_seleccionado]
#     st.success(f"Municipio seleccionado correctamente")

# Inicializar el valor de municipio_seleccionado en session_state
if "municipio_seleccionado" not in st.session_state:
    st.session_state["municipio_seleccionado"] = "Seleccione un municipio"

# Crear una lista desplegable con solo las claves (nombres de los municipios)
options = ["Seleccione un municipio"] + list(municipio_dict_1.keys())

# Selector con estado gestionado
st.session_state["municipio_seleccionado"] = st.selectbox(
    "Nombre del municipio donde reside",
    options=options,
    index=options.index(st.session_state["municipio_seleccionado"]),
)

# Obtener el municipio seleccionado desde session_state
municipio_seleccionado = st.session_state["municipio_seleccionado"]

# Verificar si el usuario seleccionó una opción válida
if municipio_seleccionado == "Seleccione un municipio":
    st.warning("Por favor, seleccione un municipio válido.")
else:
    # Obtener el código del municipio seleccionado usando el diccionario
    CodigoMunicipio = municipio_dict_1[municipio_seleccionado]
    st.success(f"Municipio seleccionado correctamente")


#######################################################################################-------------------------------------------------------------

# col7, col8 = st.columns(2)
# with col7:
#     # # Crear una lista desplegable con un mensaje inicial
#     # options = ["Seleccione una opción"] + list(tipo_usuario_map.values())
#     # tipo_seleccionado = st.selectbox(
#     #     "Tipo de aseguramiento",
#     #     options=options
#     # )

#     # # Verificar si el usuario seleccionó una opción válida
#     # if tipo_seleccionado == "Seleccione una opción":
#     #     st.warning("Por favor, seleccione una opción válida.")
#     # else:
#     #     # Obtener el código del prestador seleccionado
#     #     codigo_tipo_usuario = [codigo for codigo, nombre in tipo_usuario_map.items() if nombre == tipo_seleccionado][0]
#     #     st.success(f"Opción seleccionada correctamente")

#     # Inicializar el valor de tipo_seleccionado en session_state
#     if "tipo_seleccionado" not in st.session_state:
#         st.session_state["tipo_seleccionado"] = "Seleccione una opción"

#     # Crear una lista desplegable con un mensaje inicial
#     options = ["Seleccione una opción"] + list(tipo_usuario_map.values())

#     # Selector con estado gestionado
#     st.session_state["tipo_seleccionado"] = st.selectbox(
#         "Tipo de aseguramiento",
#         options=options,
#         index=options.index(st.session_state["tipo_seleccionado"]),
#     )

#     # Obtener el tipo de aseguramiento seleccionado desde session_state
#     tipo_seleccionado = st.session_state["tipo_seleccionado"]

#     # Validar si el usuario seleccionó una opción válida
#     if tipo_seleccionado == "Seleccione una opción":
#         st.warning("Por favor, seleccione una opción válida.")
#     else:
#         # Obtener el código correspondiente al tipo de aseguramiento
#         codigo_tipo_usuario = [
#             codigo for codigo, nombre in tipo_usuario_map.items() if nombre == tipo_seleccionado
#         ][0]
#         st.success(f"Opción seleccionada correctamente")



# #############################################################################################################################

# with col8:
#     # Inicializar el valor de causa_externa_seleccionada en session_state
#     if "causa_externa_seleccionada" not in st.session_state:
#         st.session_state["causa_externa_seleccionada"] = "Seleccione una causa externa"

#     # Crear una lista desplegable con las opciones
#     options = ["Seleccione una causa externa"] + list(causa_externa_map.values())

#     # Selector con estado gestionado
#     st.session_state["causa_externa_seleccionada"] = st.selectbox(
#         "Motivo de ingreso a urgencias",
#         options=options,
#         index=options.index(st.session_state["causa_externa_seleccionada"]),
#     )

#     # Obtener la causa externa seleccionada desde session_state
#     causa_externa_seleccionada = st.session_state["causa_externa_seleccionada"]

#     # Validar si el usuario seleccionó una opción válida
#     if causa_externa_seleccionada == "Seleccione una causa externa":
#         st.warning("Por favor, seleccione un motivo válido.")
#     else:
#         # Obtener el código de la causa externa desde el diccionario
#         codigo_causa_externa = None
#         for codigo, nombre in causa_externa_map.items():
#             if nombre == causa_externa_seleccionada:
#                 codigo_causa_externa = codigo
#                 break

#         # Validar si se encontró un código válido
#         if codigo_causa_externa is not None:
#             st.success(f"Motivo seleccionado correctamente")
#         else:
#             st.warning("Por favor, seleccione una opción válida.")


#######################################################################################-------------------------------------------------------------

# Estado inicial del selector
if "prestador_seleccionado" not in st.session_state:
    st.session_state["prestador_seleccionado"] = "Seleccione una IPS"

# Crear una lista desplegable con un mensaje inicial
options = ["Seleccione una IPS"] + list(prestadores_dict_HOSPITAL.keys())

# Selector con estado gestionado
st.session_state["prestador_seleccionado"] = st.selectbox(
    "Nombre del Prestador (Institución que atiende el paciente)",
    options=options,
    index=options.index(st.session_state["prestador_seleccionado"]),
)

# Obtener el prestador seleccionado desde session_state
prestador_seleccionado = st.session_state["prestador_seleccionado"]

# Validar si el usuario seleccionó una opción válida
if prestador_seleccionado == "Seleccione una IPS":
    st.warning("Por favor, seleccione una IPS válida.")
else:
    # Obtener el valor del diccionario público/privado
    Prestador_publica_privada = prestadores_publico_privado_dict.get(prestador_seleccionado)
    
    # Definir si es HOSPITAL o IPS
    Tipo_Prestador_IPS = prestadores_dict_IPS.get(prestador_seleccionado)
    # Definir si es HOSPITAL o IPS
    Tipo_Prestador_HOSPITAL = prestadores_dict_HOSPITAL.get(prestador_seleccionado)
    # Mostrar los valores en la interfaz
    st.success("Prestador seleccionado correctamente.")
    # st.write(f"**Prestador:** {prestador_seleccionado}")
    # st.write(f"**Tipo Prestador IPS:** {Tipo_Prestador_IPS}")
    # st.write(f"**Tipo Prestador HOSPITAL:** {Tipo_Prestador_HOSPITAL}")
    # st.write(f"**Prestador Público o Privado:** {Prestador_publica_privada}")


############################################################################################################################



# Hora de ingreso

if 0 <= HoraIngreso < 6:
    Rango_horario_ingreso = 0 #"Madrugada"
elif 6 <= HoraIngreso < 12:
    Rango_horario_ingreso = 1 #"Mañana"
elif 12 <= HoraIngreso < 18:
    Rango_horario_ingreso = 3 #"Tarde"
else:
    Rango_horario_ingreso = 2 #"Noche"

############################################################################################################################

# Botón para predecir
bot1, bot2 = st.columns([1,1])

with bot1:
    if st.button("Predecir"):

        try:
            # Procesar las variables que requieren conversión

            Edad = int(Edad)
            Dia_del_mes = int(Dia_del_mes)
            HoraIngreso = int(HoraIngreso)
            CodigoMunicipio = int(CodigoMunicipio)
            anio = int(anio)
            Tipo_Prestador_HOSPITAL = int(Tipo_Prestador_HOSPITAL)
            Tipo_Prestador_IPS = int(Tipo_Prestador_IPS)
            Mes_sin = float(Mes_sin_f)
            Mes_cos = float(Mes_cos_f)
            Dia_de_la_semana = int(Dia_de_la_semana)
            Prestador_publica_privada = int(Prestador_publica_privada)
            Grupo_etario = int(Grupo_etario)           

            # Convertir variables categóricas
            # TipoUsuario = tipo_usuario_map.get(codigo_tipo_usuario, 0)  # Valor por defecto 0 si no se encuentra
            # Dia_de_la_semana = dia_semana_map.get(Dia_del_mes, 0)
            Sexo = int(codigo_sexo)

            # Asume que otras variables categóricas ya están codificadas o agrega mapeos adicionales

            # Procesar HoraIngreso (convertir a número entero de horas)
            # HoraIngreso_horas = int(HoraIngreso.split(":")[0]) if ":" in HoraIngreso else 0

            # Crear un DataFrame con los datos procesados
            input_data = pd.DataFrame({
                # "CodigoPrestador": [CodigoPrestador],
                "Edad": [Edad],
                "Día del mes": [Dia_del_mes],
                "HoraIngreso": [HoraIngreso],
                "Clasificación casos municipio_int": [CodigoMunicipio],
                "Año": [anio],
                "Tipo Prestador_HOSPITAL": [Tipo_Prestador_HOSPITAL],
                "Mes_sin":[Mes_sin],
                "Mes_cos": [Mes_cos],
                "Día de la semana_int": [Dia_de_la_semana],
                "Prestador:1.publica/0.privada": [Prestador_publica_privada],
                "Tipo Prestador_IPS": [Tipo_Prestador_IPS],
                "Grupo_etario_int": [Grupo_etario]
            })

            print(f"Corecta ejecución paciente {nombre_paciente} {apellido}")
            print(f'Edad: {Edad}')
            print(f'Dia_del_mes: {Dia_del_mes}')
            print(f'HoraIngreso: {HoraIngreso}')
            print(f'CodigoMunicipio: {CodigoMunicipio}')
            print(f'anio:{anio}')
            print(f'Tipo_Prestador_HOSPITAL: {Tipo_Prestador_HOSPITAL}')
            print(f'Mes_sin: {Mes_sin}')
            print(f'Mes_cos: {Mes_cos}')
            print(f'Dia_de_la_semana: {Dia_de_la_semana}')
            print(f'Prestador_publica_privada: {Prestador_publica_privada}')
            print(f'Tipo_Prestador_IPS: {Tipo_Prestador_IPS}')
            print(f'Grupo_etario: {Grupo_etario}')
            # Realizar la predicción
            prediction = model.predict(input_data)[0]
            if prediction == 0:
                prediction = 'Dado de alta de urgencias'
            
            elif prediction == 1:
                prediction = 'Remitido a otro nivel de complejidad'
            
            else:
                prediction = 'Hospitalizado'    


            # Mostrar el resultado
            st.success(f"El paciente {nombre_paciente} {apellido} tiene una alta probabilidad de ser: {prediction}")

        except Exception as e:
            st.error(f"Hubo un error al procesar los datos: {e}")

with bot2:
    if st.button("Nueva predicción"):
        # Reiniciar los valores manualmente
        st.session_state["nombre_paciente"] = ""
        st.session_state["apellido"] = ""
        st.session_state["Edad"] = ""
        st.session_state["sexo_seleccionado"] = "Seleccione el sexo del paciente"
        st.session_state["municipio_seleccionado"] = "Seleccione un municipio"
        st.session_state["tipo_seleccionado"] = "Seleccione una opción"
        st.session_state["causa_externa_seleccionada"] = "Seleccione una causa externa"
        st.session_state["prestador_seleccionado"] = "Seleccione una IPS"
        st.session_state["eps_seleccionada"] = "Seleccione una EPS o Aseguradora"

        # Forzar la recarga de la aplicación para reflejar los cambios
        st.markdown('<meta http-equiv="refresh" content="0; url=/" />', unsafe_allow_html=True)

        

        


        
        




