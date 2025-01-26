import streamlit as st
from datetime import datetime
import pandas as pd
import pickle
import os

# Mapeos para las EPS
eps_dict = {1: 'AIC EPSIC', 3: 'ALIANSALUD', 4: 'ALIANSALUD EPS S.A', 5: 'AMBUQ CONTRIBUTIVO', 6: 'AMBUQ ESS', 7: 'ANAS WAYUU EPSI', 
 8: 'ANAS WAYUU EPSIC', 9: 'ARL FONDO DE RIESGOS LABORALES', 10: 'ARL SURA', 11: 'ASEGURADORA DE VIDA COLSEGUROS', 12: 'ASMESSALUD DE NARIÑO ESSC', 
 13: 'ASMET SALUD ESS', 14: 'ASMET SALUD ESSC', 15: 'ASOCIACIÓN MUTUAL SER EMPRESA SOLIDARIA DE SALUD E.S.S', 16: 'ASOCIACIÓN MUTUAL BARRIOS UNIDOS DE QUIBDÓ (AMBUQ EPS)', 
 17: 'ASOCIACIÓN MUTUAL SER EMPRESA SOLIDARIA DE SALUD - MUTUAL SER EPS', 18: 'BBVA SEGUROS DE VIDA COLOMBIA S A', 19: 'CAFESALUD EPS SA', 
 20: 'CAFESALUD MEDICINA PREPAGADA S A', 21: 'CAFESALUD SUBSIDIADO', 22: 'CAJA COMPENSACION COMFENALCO', 23: 'CAJACOPI ATLANTICO - CCFC', 
 24: 'CAJACOPI CCF055', 25: 'CAMACOL', 26: 'CAPITAL SALUD EPS-S', 27: 'CAPITAL SALUD EPSC34', 28: 'CAPRESOCA EPS', 29: 'CCF COMFACUNDI', 
 30: 'CCF COMFAMILIAR CARTAGENA', 31: 'CCF COMFAMILIAR DE LA GUAJIRA', 32: 'CCF COMFAMILIAR HUILA', 33: 'CCF COMFAMILIAR RISARALDA', 34: 'CCF COMFAORIENTE', 
 35: 'CCF COMFASUCRE', 36: 'CCF COMPENSAR', 37: 'CCF DE NARIÑO', 38: 'CIA DE SEGUROS BOLIVAR S A', 39: 'COLMENA SA MEDICINA PREPAGADA', 40: 'COLPATRIA EPS', 
 41: 'COLPATRIA SA MEDICINA PREPAGADA', 42: 'COLSANITAS', 43: 'COLSEGUROS EPS', 44: 'COMFACHOCO CCF', 45: 'COMFACHOCO-CCFC', 46: 'COMFACOR CCF015', 
 47: 'COMFAMILIAR DE LA GUAJIRA EPS-CCF', 48: 'COMFASUCRE CCFC', 49: 'COMFENALCO ANTIOQUIA', 50: 'COMFENALCO VALLE EPS', 51: 'COMFENALCO VALLE EPSS', 52: 'COMPARTA', 
 53: 'COMPARTA ESSC', 54: 'COMPAÑIA AGRICOLA DE SEGUROS DE VIDA S A', 55: 'COMPAÑIA CENTRAL DE SEGUROS DE VIDA SA', 56: 'COMPAÑIA DE SEGUROS DE VIDA AURORA', 
 57: 'COMPAÑIA MUNDIAL DE SEGUROS SA', 58: 'COMPAÑIA SURAMERICANA', 59: 'COMPAÑIA SURAMERICANA DE SEGUROS SA', 60: 'COMPAÑIA SURAMERICANA PREPAGADA', 61: 'COMPENSAR EPS', 
 62: 'CONVIDA EPS', 63: 'COOMEVA EPS SA', 64: 'COOMEVA EPSS', 65: 'COOMEVA MEDICINA PREPAGADA S A', 66: 'COOSALUD ESS EPS-S', 67: 'COOSALUD ESSC', 68: 'CRUZ BLANCA EPS SA', 
 69: 'CRUZ BLANCA EPSS', 70: 'CAJA DE COMPENSACIÓN FAMILIAR DEL ORIENTE COLOMBIANO (COMFAORIENTE)', 71: 'COLPATRIA MEDICINA PREPAGADA S.A.', 72: 'COLSEGURO', 
 73: 'COMPAÑÍA SURAMERICANA DE SEGUROS', 74: 'COMPENSAR EPS', 75: 'COOMEVA MEDICINA PREPAGADA S.A.', 76: 'COOSALUD EPS S.A.', 
 77: 'DEPARTAMENTO MEDICO Y ODONTOLOGICO DEL MUNICIPIO DE MEDELLIN', 78: 'DIRECCION DEPARTAMENTAL DE SALUD DE ANTIOQUIA', 79: 'DIRECCION DEPARTAMENTAL DE SALUD DE ARAUCA', 
 80: 'DIRECCION DEPARTAMENTAL DE SALUD DE BOLIVAR', 81: 'DIRECCION DEPARTAMENTAL DE SALUD DE BOYACA', 82: 'DIRECCION DEPARTAMENTAL DE SALUD DE CALDAS', 
 83: 'DIRECCION DEPARTAMENTAL DE SALUD DE CAQUETA', 84: 'DIRECCION DEPARTAMENTAL DE SALUD DE CASANARE', 85: 'DIRECCION DEPARTAMENTAL DE SALUD DE CAUCA', 
 86: 'DIRECCION DEPARTAMENTAL DE SALUD DE CESAR', 87: 'DIRECCION DEPARTAMENTAL DE SALUD DE CHOCO', 88: 'DIRECCION DEPARTAMENTAL DE SALUD DE CORDOBA', 
 89: 'DIRECCION DEPARTAMENTAL DE SALUD DE CUNDINAMARCA', 90: 'DIRECCION DEPARTAMENTAL DE SALUD DE GUAJIRA', 91: 'DIRECCION DEPARTAMENTAL DE SALUD DE HUILA', 
 92: 'DIRECCION DEPARTAMENTAL DE SALUD DE MAGDALENA', 93: 'DIRECCION DEPARTAMENTAL DE SALUD DE META', 94: 'DIRECCION DEPARTAMENTAL DE SALUD DE NORTE DE SANTANDER', 
 95: 'DIRECCION DEPARTAMENTAL DE SALUD DE PUTUMAYO', 96: 'DIRECCION DEPARTAMENTAL DE SALUD DE QUINDIO', 97: 'DIRECCION DEPARTAMENTAL DE SALUD DE RISARALDA', 
 98: 'DIRECCION DEPARTAMENTAL DE SALUD DE SANTANDER', 99: 'DIRECCION DEPARTAMENTAL DE SALUD DE SUCRE', 100: 'DIRECCION DEPARTAMENTAL DE SALUD DE TOLIMA', 
 101: 'DIRECCION DEPARTAMENTAL DE SALUD DE VALLE', 102: 'DIRECCION DISTRITAL DE SALUD DE BOGOTA', 103: 'DIRECCION GENERAL DE SANIDAD MILITAR', 
 104: 'DIRECCION SANIDAD POLICIA NACIONAL', 105: 'DIVISION DE SALUD DE LA UNIVERSIDAD DE ANTIOQUIA', 
 106: 'DIVISION DE SERVICIOS MEDICO ASISTENCIAL DE LA CORPORACION ELECTRICA DE LA COSTA ATLANTICA CORELCA', 107: 'DUSAKAWI EPSI', 108: 'DUSAKAWI ESS', 
 109: 'DIRECCIÓN DEPARTAMENTAL DE SALUD DE ANTIOQUIA', 110: 'DIRECCIÓN DEPARTAMENTAL DE SALUD DE ATLANTICO', 111: 'DIRECCIÓN DEPARTAMENTAL DE SALUD DE ANTIOQUIA', 
 112: 'DIRECCIÓN DEPARTAMENTAL DE SALUD DE ATLÁNTICO', 113: 'DIRECCIÓN DEPARTAMENTAL DE SALUD DE CALDAS', 114: 'DIRECCIÓN DEPARTAMENTAL DE SALUD DE CALDAS', 
 115: 'DIRECCIÓN DEPARTAMENTAL DE SALUD DE CESAR', 116: 'DIRECCIÓN DEPARTAMENTAL DE SALUD DE CHOCÓ', 117: 'DIRECCIÓN DEPARTAMENTAL DE SALUD DE HUILA', 
 118: 'DIRECCIÓN DEPARTAMENTAL DE SALUD DE LA GUAJIRA', 119: 'DIRECCIÓN DEPARTAMENTAL DE SALUD DE NORTE DE SANTANDER', 120: 'DIRECCIÓN DEPARTAMENTAL DE SALUD DE QUINDÍO', 
 121: 'DIRECCIÓN DEPARTAMENTAL DE SALUD DE RISARALDA', 122: 'DIRECCIÓN DEPARTAMENTAL DE SALUD DE SANTANDER', 123: 'DIRECCIÓN DEPARTAMENTAL DE SALUD DE SUCRE', 
 124: 'DIRECCIÓN MUNICIPAL DE SALUD DE ABEJORRAL', 125: 'E.P.S. SANITAS S.A.', 126: 'ECOOPSOS ESS', 127: 'ECOOPSOS ESSC', 128: 'ECOPETROL', 129: 'EMDISALUD ESS', 
 130: 'EMERGENCIA MÉDICA INTEGRAL EMI ANTIOQUIA SA SERVICIO DE AMBULANCIA PREPAGADO', 131: 'EMPRESAS PUBLICAS DE MEDELLIN DEPARTAMENTO MEDICO', 132: 'EMSSANAR ESS', 
 133: 'ESS COOPERATIVA VILLASALUD LTD', 134: 'EMPRESA MUTUAL PARA EL DESARROLLO INTEGRAL DE LA SALUD (EMDISALUD ESS-EPS-S)', 135: 'FAMISANAR EPS LTDA', 
 136: 'FAMISANAR EPSS', 137: 'FERROCARRILES NACIONALES DE COLOMBIA', 138: 'FIDUPREVISORA  SA REMG', 139: 'FIDUPREVISORA SA RES', 
 140: 'FONDO DE SOLIDARIDAD Y GARANTIA MINISTERIO DE SALUD', 141: 'FUERZAS MILITARES', 142: 'FUNDACIÓN SALUD MÍA EPS', 
 143: 'GENERALI COLOMBIA-SEGUROS GENERALES SA', 144: 'GENERALI COLOMBIA-SEGUROS GENERALES S.A.', 145: 'INPEC', 
 146: 'LA EQUIDAD SEGUROS DE VIDA ORGANISMO COOPERATIVO -LA EQUIDAD VIDA-', 147: 'LA INTERAMERICANA COMPAÑIA DE SEGUROS GENERALES SA', 
 148: 'LA PREVISORA SA COMPAÑIA DE SEGUROS', 149: 'LIBERTY SEGUROS DE VIDA SA', 150: 'LIBERTY SEGUROS SA', 151: 'LA PREVISORA S.A', 152: 'LIBERTY SEGUROS', 
 153: 'MALLAMAS EPSI', 154: 'MALLAMAS EPSIC', 155: 'MAPFRE COLOMBIA VIDA SEGUROS SA', 156: 'MAPFRE SEGUROS GENERALES DE COLOMBIA SA', 157: 'MEDIMAS EPS CONTRIBUTIVO', 
 158: 'MEDIMAS EPS MOVILIDAD CONTRIBUTIVO', 159: 'MEDIMAS EPS MOVILIDAD SUBSIDIADO', 160: 'MEDIMAS EPS SUBSIDIADO', 161: 'MEDISALUD COMPAÑIA COLOMBIANA DE MEDICINA PREPAGADA SA', 162: 'MEDISANITAS SA PREPAGADA', 
 163: 'MUNDIAL DE SEGUROS DE VIDA SA', 164: 'MUTUAL SER ESS', 165: 'MUNDIAL DE SEGUROS', 166: 'NUEVA EPS', 167: 'NUEVA EPS CONTRIBUTIVO', 168: 'NUEVA EPS SA SUBSIDIADO', 
 169: 'NUEVA EPSS', 170: 'OTRA', 171: 'PANAMERICANA DE COLOMBIA COMPAÑIA DE SEGUROS DE VIDA SA', 172: 'PIJAOS SALUD EPSI', 173: 'PIJAOSALUD EPSIC', 174: 'POLICIA NACIONAL', 
 175: 'POSITIVA COMPAÑIA DE SEGUROS - LA PREVISORA VIDA', 176: 'PROGRAMA DE SALUD UNIVERSIDAD DE ANTIOQUIA', 177: 'QBE SEGUROS SA', 178: 'RES FONDO PRESTACION SOCIAL CO', 
 179: 'RIESGOS PROFESIONALES COLMENA SA COMPAÑIA DE SEGUROS DE VIDA', 180: 'RISARALDA LTDA EN LIQUIDACION EPS', 181: 'ROYAL & SUN ALLIANCE SEGUROS (COLOMBIA) SA', 
 182: 'SALUD TOTAL SA EPS', 183: 'SALUD TOTAL SA SUBSIDIADO', 184: 'SALUD VIDA EPS', 185: 'SALUD VIDA SA ENTIDAD PROMOTORA DE SALUD', 186: 'SALUDCOLOMBIA ENTIDAD PROMOTORA DE SALUD SA', 
 187: 'SALUDVIDA', 188: 'SALUDVIDA EPS SA', 189: 'SANITAS EPS SA', 190: 'SAVIA SALUD', 191: 'SAVIA SALUD EPS', 192: 'SEGUROS COLPATRIA S.A.', 193: 'SEGUROS COMERCIALES BOLIVAR SA', 
 194: 'SEGUROS DE VIDA ALFA SA', 195: 'SEGUROS DE VIDA COLPATRIA S A', 196: 'SEGUROS DE VIDA DEL ESTADO SA', 197: 'SEGUROS DEL ESTADO SA', 198: 'SERVICIO NACIONAL DE APRENDIZAJE - SENA', 
 199: 'SOLSALUD EPS SA', 200: 'SOS EPS', 201: 'SOS EPSS', 202: 'SURA EPS', 203: 'SEGUROS DEL ESTADO', 204: 'UISALUD', 205: 'UNISALUD EAS', 206: 'UNISALUD RES', 207: 'UNISALUD REUE', 208: 'UNIVERSIDAD DE ANTIOQUIA', 
 209: 'UNIVERSIDAD DEL CAUCA UNIDAD DE SALUD', 210: 'UNIVERSIDAD DEL VALLE SERVICIO DE SALUD', 211: 'UNIVERSIDAD DE CÓRDOBA', 212: 'UNIVERSIDAD DE NARIÑO'}

# Mapeos para las IPS
prestadores_dict  = {
 50010212604: 'AUNA CENTRO MÉDICO LAS AMÉRICAS SEDE ARKADIA',
 50010217854: 'CENTRO DE SALUD SANTO DOMINGO',
 50010211001: 'CLINICA CARDIO VID',
 50010909923: 'CLINICA CENTRAL FUNDADORES',
 50010329301: 'CLINICA DE CIRUGIA AMBULATORIA CONQUISTADORES',
 50010464802: 'CLINICA DEL PRADO CIUDAD DEL RIO',
 50010209201: 'CLINICA EL ROSARIO SEDE CENTRO',
 50010209202: 'CLINICA EL ROSARIO SEDE EL TESORO',
 50010217203: 'CLINICA MEDELLIN OCCIDENTE',
 50010217202: 'CLINICA MEDELLIN POBLADO',
 50010217201: 'CLINICA MEDELLIN S.A',
 50010344803: 'CLINICA UNIVERSITARIA BOLIVARIANA',
 50010218601: 'CLINISANITAS MEDELLIN',
 50010212601: 'CLÍNICA LAS AMERICAS',
 50010420901: 'COOPERATIVA DE SALUD SAN ESTEBAN',
 50011313101: 'CORPORACIÓN HOSPITAL INFANTIL CONCEJO DE MEDELLÍN',
 50010212401: 'CORPORACIÓN PARA ESTUDIOS EN SALUD CLINICA CES',
 50010608601: 'E.S.E. HOSPITAL LA MARIA',
 50011930101: 'ENDOGINE IPS SAS',
 50010558607: 'FUNDACION COLOMBIANA DE CANCEROLOGIA CLINICA VIDA',
 50010217501: 'FUNDACION HOSPITALARIA SAN VICENTE DE PAUL',
 50010115001: 'FUNDACIÓN INSTITUTO NEUROLOGICO DE COLOMBIA',
 50010214401: 'HOSPITAL GENERAL DE MEDELLÍN LUZ CASTRO DE GUT',
 50010210401: 'HOSPITAL PABLO TOBON URIBE',
 50010212001: 'INVERSIONES MEDICAS DE ANTIOQUIA S.A. CLINICA',
 50010425919: 'IPS SURA INDUSTRIALES MEDELLIN',
 50010425930: 'IPS SURA LAS VEGAS MEDELLIN',
 50010425925: 'IPS SURA LOS MOLINOS MEDELLIN',
 50010425936: 'IPS SURA SAN DIEGO',
 50011174601: 'NUEVA CLINICA SAGRADO CORAZON S.A.S',
 50010558603: 'OTRA',
 50010217801: 'SEDE ADMINISTRATIVA EDIFICIO SACATIN',
 50010590903: 'SEDE PRINCIPAL HOSPITAL ALMA MÁTER DE ANTIOQUIA',
 50010210101: 'SOCIEDAD MEDICA ANTIOQUEÑA S.A. SOMA',
 50011679101: 'TRAUMACENTRO S.A.A',
 50010217862: 'UNIDAD DE SALUD MENTAL',
 50010217802: 'UNIDAD HOSPITALARIA DE BELEN HECTOR ABAD GOMEZ',
 50010217808: 'UNIDAD HOSPITALARIA DE CASTILLA JAIME TOBON AR',
 50010217804: 'UNIDAD HOSPITALARIA DE MANRRIQUE HERMENEGILDO',
 50010217807: 'UNIDAD HOSPITALARIA DOCE DE OCTUBRE LUIS CARLO',
 50010217861: 'UNIDAD HOSPITALARIA NUEVO OCCIDENTE',
 50010217811: 'UNIDAD HOSPITALARIA SAN ANTONIO DE PRADO DIEGO',
 50010217810: 'UNIDAD HOSPITALARIA SAN CRISTOBAL LEONARDO BET',
 50010217809: 'UNIDAD HOSPITALARIA SAN JAVIER JESÚS PELÁEZ BO',
 50010217857: 'UNIDAD HOSPITALARIA SANTA CRUZ VÍCTOR CÁRDENAS',
 50011427607: 'VIRREY SOLIS I.P.S S.A SAN DIEGO',
 50011427609: 'VIRREY SOLIS IPS FLORIDA',
 50011427610: 'VIRREY SOLÍS IPS. S.A TRANVÍA PLAZA'
 }

# mapeo municipios
municipio_dict_1 = {1.0: 'MEDELLIN',2.0: 'SANTAFE DE BOGOTA D.C.-CHAPINERO', 4.0: 'SANTAFE DE BOGOTA D.C.-SAN CRISTOBAL', 21.0: 'ALEJANDRIA', 30.0: 'AMBALEMA', 31.0: 'AMALFI', 34.0: 'ANDES', 36.0: 'ANDALUCIA', 38.0: 'ANGOSTURA', 40.0: 'ANOLAIMA', 44.0: 'ANZA', 45.0: 'BECERRIL', 51.0: 'ARBOLEDAS', 55.0: 'ARMERO (GUAYABAL)', 59.0: 'ARMENIA', 79.0: 'BARBACOAS', 88.0: 'BELALCAZAR', 86.0: 'BELTRAN', 91.0: 'BETANIA', 93.0: 'BETULIA', 101.0: 'BOLIVAR', 107.0: 'BRICEÑO', 113.0: 'BUGALAGRANDE', 120.0: 'CABRERA', 125.0: 'HATO COROZAL', 129.0: 'CALDAS', 134.0: 'CAMPAMENTO', 138.0: 'CAÑASGORDAS', 142.0: 'CALOTO', 145.0: 'CARAMANTA', 147.0: 'CARTAGO', 148.0: 'CARMEN APICALA', 150.0: 'CASTILLA LA NUEVA', 154.0: 'CARMEN DE CARUPA', 172.0: 'CHINACOTA', 190.0: 'CIRCASIA', 197.0: 'COCORNA', 206.0: 'CONVENCION', 209.0: 'CONFINES', 212.0: 'CORDOBA', 234.0: 'DABEIBA', 237.0: 'DON MATIAS', 240.0: 'CHACHAGUI', 250.0: 'PAZ DE ARIPORO', 264.0: 'ENCINO', 266.0: 'ENCISO', 282.0: 'FREDONIA', 284.0: 'FRONTINO', 1.0: 'MANIZALES', 585.0: 'PURIFICACION', 13.0: 'AGUADAS', 20.0: 'ALCALA', 75.0: 'BAHIA SOLANO (MUTIS)', 77.0: 'BAJO BAUDO (PIZARRO)', 81.0: 'BARRANCABERMEJA', 92.0: 'BETEITIVA', 121.0: 'CABRERA', 132.0: 'CAMPOALEGRE', 152.0: 'CASABIANCA', 160.0: 'CANTAGALLO', 162.0: 'MONTERREY', 167.0: 'CHARALA', 169.0: 'CHARTA', 170.0: 'CHIVOLO', 176.0: 'CHIQUINQUIRA', 179.0: 'CHIPATA', 207.0: 'CONSACA', 211.0: 'CONTRATACION', 217.0: 'COYAIMA', 229.0: 'CURITI', 235.0: 'GALERAS (NUEVA GRANADA)', 245.0: 'EL CARMEN', 255.0: 'EL PLAYON', 271.0: 'FLORIAN', 302.0: 'GENOVA', 318.0: 'GUACARI', 383.0: 'LA GLORIA', 400.0: 'TAMARA', 401.0: 'LA VICTORIA', 440.0: 'VILLANUEVA', 456.0: 'MISTRATO', 470.0: 'MONTENEGRO', 548.0: 'PIENDAMO', 572.0: 'SANTA RITA', 594.0: 'QUETAME', 682.0: 'SAN JOAQUIN', 687.0: 'SAN LORENZO', 690.0: 'SANTA MARIA', 42.0: 'ANSERMA', 306.0: 'GINEBRA', 308.0: 'GIRARDOTA', 310.0: 'GONZALEZ', 313.0: 'GRAMALOTE', 315.0: 'SACAMA', 321.0: 'GUATAPE', 347.0: 'HERVEO', 353.0: 'HISPANIA', 360.0: 'ITAGUI', 361.0: 'ISTMINA', 364.0: 'JAMUNDI', 368.0: 'JESUS MARIA', 376.0: 'LA CEJA', 380.0: 'LA DORADA', 390.0: 'LA TOLA', 411.0: 'LIBANO', 425.0: 'MACARAVITA', 467.0: 'MONTEBELLO', 475.0: 'MURINDO', 480.0: 'MUTISCUA', 483.0: 'NATAGAIMA', 495.0: 'NORCASIA', 490.0: 'OLAYA HERRERA (BOCAS DE SATINGA)', 501.0: 'OLAYA', 541.0: 'PENSILVANIA', 543.0: 'PEQUE', 576.0: 'PUEBLORRICO', 579.0: 'PUERTO BERRIO', 591.0: 'PUERTO RONDON', 604.0: 'REMEDIOS', 607.0: 'RETIRO', 615.0: 'RIONEGRO', 628.0: 'SABANALARGA', 631.0: 'SABANETA', 642.0: 'SALGAR', 647.0: 'SAN ESTANISLAO', 649.0: 'SAN BERNARDO', 652.0: 'SAN FRANCISCO', 656.0: 'SAN JERONIMO', 658.0: 'SAN FRANCISCO', 659.0: 'SAN JUAN DE URABA', 660.0: 'SALAZAR', 664.0: 'SAN JOSE DE PARE', 665.0: 'SAN JOSE', 667.0: 'SAN LUIS DE GACENO', 670.0: 'SAN PEDRO', 674.0: 'SAN VICENTE', 679.0: 'SAN GIL', 686.0: 'SANTA ISABEL', 697.0: 'SANTUARIO', 736.0: 'SEVILLA', 756.0: 'SOLANO', 761.0: 'SOMONDOCO', 789.0: 'TAMESIS', 790.0: 'TASCO', 792.0: 'TARSO', 809.0: 'TIMBIQUI', 819.0: 'TOLEDO', 837.0: 'TUTA', 842.0: 'UMBITA', 847.0: 'URIBIA', 854.0: 'VALLE DE SAN JUAN', 856.0: 'VALPARAISO', 858.0: 'VEGACHI', 861.0: 'VENADILLO', 873.0: 'VILLAMARIA', 885.0: 'VILLAGARZON', 887.0: 'PANA PANA (CAMPO ALEGRE)', 890.0: 'YOTOCO', 893.0: 'YONDO', 895.0: 'ZARZAL', 78.0: 'BARRANCAS', 137.0: 'CALDONO', 141.0: 'CANDELARIA', 296.0: 'GALAN', 372.0: 'JURADO', 421.0: 'LURUACO', 433.0: 'MANZANARES', 436.0: 'MANTA', 520.0: 'PALOCABILDO', 549.0: 'PINCHOTE', 558.0: 'POLO NUEVO', 560.0: 'POTOSI', 573.0: 'PUERTO LEGUIZAMO', 606.0: 'RESTREPO', 634.0: 'SABANAGRANDE', 638.0: 'SACHICA', 675.0: 'SAN ANTONIO', 685.0: 'SAN BERNARDO', 758.0: 'SOPO', 770.0: 'SUAREZ', 832.0: 'TUNUNGUA', 849.0: 'USIACURI', 6.0: 'ACACIAS', 52.0: 'ARJONA', 62.0: 'ARROYOHONDO', 74.0: 'BARRANCO DE LOBA', 140.0: 'CALAMAR', 188.0: 'CICUCO', 222.0: 'CLEMENCIA', 244.0: 'EL COCUY', 248.0: 'EL CERRITO', 268.0: 'ESPINAL', 300.0: 'SABANALARGA', 430.0: 'LA VICTORIA', 442.0: 'MARMATO', 458.0: 'MONTECRISTO', 468.0: 'MOLAGAVITA', 473.0: 'MORROA', 580.0: 'PUERTO LIBERTADOR', 600.0: 'RIOQUITO', 620.0: 'SAN CRISTOBAL', 650.0: 'SAN JUAN DEL CESAR', 654.0: 'SAN JACINTO', 655.0: 'SABANA DE TORRES', 657.0: 'SAN JUAN NEPOMUCENO', 673.0: 'SAN BENITO', 683.0: 'SANDONA', 688.0: 'SANTA ROSA DEL SUR', 744.0: 'SIMITI', 760.0: 'SAN JOSE DE OCUNE', 780.0: 'SURATA', 810.0: 'TIBU', 836.0: 'TURBACO', 838.0: 'TUQUERRES', 894.0: 'ZAMBRANO', 3.0: 'ABREGO', 5.0: 'SANTAFE DE BOGOTA D.C.-USME', 7.0: 'SANTAFE DE BOGOTA D.C.-BOSA', 8.0: 'SANTAFE DE BOGOTA D.C.-KENNEDY', 9.0: 'SANTAFE DE BOGOTA D.C.-FONTIBON', 10.0: 'AGUAZUL', 11.0: 'AGUACHICA', 12.0: 'SANTAFE DE BOGOTA D.C.-BARRIOS UNIDOS', 14.0: 'SANTAFE DE BOGOTA D.C.-MARTIRES', 15.0: 'CALAMAR', 16.0: 'AIPE', 17.0: 'SANTAFE DE BOGOTA D.C.-CANDELARIA', 18.0: 'SANTAFE DE BOGOTA D.C.-RAFAEL URIBE', 19.0: 'ALBAN (SAN JOSE)', 35.0: 'ANAPOIMA', 53.0: 'ARACATACA', 95.0: 'BITUIMA', 99.0: 'BOCHALEMA', 123.0: 'CACHIPAY', 126.0: 'CALIMA (DARIEN)', 151.0: 'CAQUEZA', 168.0: 'CHAPARRAL', 175.0: 'CHIMICHAGUA', 178.0: 'CHIRIGUANA', 181.0: 'CHOACHI', 183.0: 'CHITA', 200.0: 'MIRAFLORES', 214.0: 'COTA', 224.0: 'CUASPUD (CARLOSAMA)', 258.0: 'EL TABLON', 260.0: 'EL TAMBO', 269.0: 'FACATATIVA', 279.0: 'RECETOR', 281.0: 'FOSCA', 286.0: 'FUNZA', 288.0: 'FUNDACION', 290.0: 'FLORENCIA', 293.0: 'GACHANTIVA', 295.0: 'GAMARRA', 297.0: 'GACHETA', 299.0: 'GARAGOA', 307.0: 'GIRON', 312.0: 'GRANADA', 317.0: 'GUACHUCAL', 320.0: 'ORITO', 322.0: 'GUAPOTA', 324.0: 'GUAVATA', 326.0: 'GUATAVITA', 328.0: 'GUAYABAL DE SIQUIMA', 335.0: 'GUAYABETAL', 339.0: 'GUTIERREZ', 377.0: 'LA CUMBRE', 386.0: 'LA MESA', 394.0: 'LA PALMA', 398.0: 'LA PLAYA', 402.0: 'LA VEGA', 407.0: 'LA PEDRERA', 426.0: 'MACHETA', 438.0: 'MEDINA', 486.0: 'NEIRA', 488.0: 'NILO', 489.0: 'NIMAIMA', 491.0: 'NOVITA', 599.0: 'RAGONVALIA', 513.0: 'PACORA', 518.0: 'PAMPLONA', 524.0: 'PALESTINA', 530.0: 'PUERTO ALEGRIA', 535.0: 'PASCA', 592.0: 'PUERTO RICO', 596.0: 'QUIPILE', 612.0: 'RICAURTE', 645.0: 'SAN ANTONIO DEL TEQUENDAMA', 653.0: 'SALAMINA', 662.0: 'SAMANA', 718.0: 'SASAIMA', 740.0: 'SIACHOQUE', 743.0: 'SILOS', 745.0: 'SIMACOTA', 754.0: 'SOACHA', 769.0: 'SUBACHOQUE', 772.0: 'SUESCA', 777.0: 'SUPIA', 779.0: 'SUSA', 781.0: 'SUTATAUSA', 785.0: 'SOLITA', 793.0: 'TAUSA', 797.0: 'TESALIA', 799.0: 'TELLO', 805.0: 'TIBACUY', 807.0: 'TIERRALTA', 815.0: 'TOCAIMA', 817.0: 'TOCANCIPA', 823.0: 'TORO', 839.0: 'TUTASA', 841.0: 'UBAQUE', 843.0: 'UBATE', 845.0: 'ULLOA', 851.0: 'UTICA', 506.0: 'OSPINA', 862.0: 'VERGARA', 867.0: 'VICTORIA', 871.0: 'VILLACARO', 875.0: 'VILLETA', 878.0: 'VIOTA', 26.0: 'ALVARADO', 298.0: 'GAMBITA', 319.0: 'GUAMO', 349.0: 'HONDA', 357.0: 'IQUIRA', 359.0: 'ISNOS (SAN JOSE DE ISNOS)', 378.0: 'LA CRUZ', 396.0: 'LA PLATA', 898.0: 'ZIPACON', 899.0: 'ZIPAQUIRA', 503.0: 'OPORAPA', 551.0: 'PIVIJAY', 668.0: 'SAN AGUSTIN', 676.0: 'SAN MIGUEL DE SEMA', 791.0: 'TARQUI', 801.0: 'TERUEL', 872.0: 'VILLANUEVA', 22.0: 'ALDANA', 47.0: 'AQUITANIA', 87.0: 'BELEN', 90.0: 'DIBULLA', 97.0: 'BOAVITA', 104.0: 'BOYACA', 106.0: 'BRICEÑO', 109.0: 'BUENAVENTURA', 114.0: 'BUSBANZA', 131.0: 'CALDAS', 135.0: 'CANTON DE SAN PABLO (MANAGRU)', 232.0: 'CHIQUIZA', 180.0: 'CHISCAS', 185.0: 'CHITARAQUE', 187.0: 'CHIVATA', 236.0: 'DOLORES', 189.0: 'CIENAGA', 204.0: 'COLOSO (RICAURTE)', 215.0: 'COROZAL', 218.0: 'COVARACHIA', 223.0: 'CUCUTILLA', 226.0: 'CUNDAY', 238.0: 'EL COPEY', 272.0: 'FILADELFIA', 276.0: 'FLORIDABLANCA', 325.0: 'SAN LUIS DE PALENQUE', 332.0: 'GUICAN', 362.0: 'IZA', 367.0: 'JENESANO', 403.0: 'LA VICTORIA', 455.0: 'MIRANDA', 464.0: 'MOGOTES', 466.0: 'MONTELIBANO', 469.0: 'MONIQUIRA', 476.0: 'MOTAVITA', 494.0: 'NUEVO COLON', 500.0: 'OIBA', 507.0: 'OTANCHE', 511.0: 'PACOA', 514.0: 'PAEZ', 516.0: 'PAIPA', 522.0: 'PALMAR', 531.0: 'PAUNA', 533.0: 'PARAMO', 537.0: 'PAZ DEL RIO', 542.0: 'PESCA', 550.0: 'PELAYA', 621.0: 'ROBERTO PAYAN (SAN JOSE)', 632.0: 'SABOYA', 646.0: 'SAMACA', 681.0: 'SAN PABLO DE BORBUR', 693.0: 'SAN PABLO', 696.0: 'SANTA BARBARA (ISCUANDE)', 720.0: 'SANTA HELENA DEL OPON', 723.0: 'SATIVASUR', 753.0: 'SAN VICENTE DEL CAGUAN', 757.0: 'SAN MIGUEL (LA DORADA)', 755.0: 'SAN FRANCISCO', 759.0: 'SOGAMOSO', 762.0: 'SORA', 764.0: 'SORACA', 763.0: 'SOTAQUIRA', 774.0: 'SUSACON', 776.0: 'SUTAMARCHAN', 778.0: 'SUTATENZA', 798.0: 'TARAPACA', 804.0: 'TIBANA', 806.0: 'TIBASOSA', 808.0: 'TINJACA', 814.0: 'TOCA', 816.0: 'TOGUI', 820.0: 'TOLU', 822.0: 'TOTA', 835.0: 'TUMACO', 29.0: 'ALBANIA', 50.0: 'ARANZAZU', 94.0: 'BELEN DE LOS ANDAQUIES', 205.0: 'CONCORDIA', 247.0: 'EL DONCELLO', 256.0: 'EL ROSARIO', 410.0: 'TAURAMENA', 460.0: 'MIRITI-PARANA', 479.0: 'MORELIA', 610.0: 'SAN JOSE DE FRAGUA', 860.0: 'VALPARAISO', 879.0: 'VIRACACHA', 897.0: 'ZETAQUIRA', 32.0: 'ASTREA', 60.0: 'BOSCONIA', 100.0: 'BOLIVAR', 110.0: 'BUENAVISTA', 130.0: 'CANDELARIA', 228.0: 'CURUMANI', 355.0: 'INZA', 392.0: 'LA SIERRA', 397.0: 'LA PAZ', 418.0: 'LOS PALMITOS', 450.0: 'PUERTO CONCORDIA', 517.0: 'PAILITAS', 532.0: 'PATIA (EL BORDO)', 622.0: 'ROLDANILLO', 698.0: 'SANTANDER DE QUILICHAO', 701.0: 'SANTA ROSA', 821.0: 'TORIBIO', 824.0: 'TOTORO', 68.0: 'AYAPEL', 182.0: 'CHINU', 350.0: 'LA MACARENA', 417.0: 'LORICA', 419.0: 'LOS CORDOBAS', 443.0: 'MARIQUITA', 555.0: 'PLANADAS', 570.0: 'PUEBLOVIEJO', 574.0: 'PUERTO ESCONDIDO', 586.0: 'PURISIMA', 614.0: 'RIOSUCIO', 672.0: 'SAN ANTERO', 678.0: 'SAN LUIS', 710.0: 'SAN ALBERTO', 750.0: 'SAN DIEGO', 787.0: 'TADO', 855.0: 'VALLE SAN JOSE', 25.0: 'EL RETORNO', 73.0: 'BAGADO', 413.0: 'LLORO', 800.0: 'TEORAMA', 58.0: 'ARIGUANI (EL DIFICIL)', 98.0: 'DISTRACCION', 161.0: 'CARURU', 420.0: 'LA JAGUA DEL PILAR', 545.0: 'PIJIÑO DEL CARMEN (PIJIÑO)', 874.0: 'VILLA DEL ROSARIO', 83.0: 'BELEN', 124.0: 'CAJAMARCA', 203.0: 'COLON (GENOVA)', 251.0: 'EL CASTILLO', 270.0: 'FALAN', 287.0: 'FUNES', 330.0: 'MESETAS', 370.0: 'JORDAN', 568.0: 'PUERTO ASIS', 577.0: 'PUERTO LLERAS', 590.0: 'PUERTO RICO', 605.0: 'REMOLINO', 680.0: 'SANTIAGO', 689.0: 'SAN VICENTE DE CHUCURI', 692.0: 'SAN SEBASTIAN DE BUENAVISTA', 703.0: 'SAN ZENON', 707.0: 'SANTA ANA', 711.0: 'VISTAHERMOSA', 210.0: 'CONTADERO', 227.0: 'CUMBAL', 233.0: 'DAGUA', 254.0: 'EL PEÑOL', 323.0: 'GUALMATAN', 352.0: 'ICONONZO', 354.0: 'IMUES', 356.0: 'IPIALES', 381.0: 'LA FLORIDA', 385.0: 'LANDAZURI', 399.0: 'LA UNION', 405.0: 'LA CHORRERA', 427.0: 'MAGUI (PAYAN)', 435.0: 'MALLAMA (PIEDRANCHA)', 540.0: 'PUERTO NARIÑO', 565.0: 'PROVIDENCIA', 694.0: 'SAN PEDRO DE CARTAGO', 699.0: 'SANTA CRUZ (GUACHAVES)', 111.0: 'BUGA', 128.0: 'CACHIRA', 174.0: 'CHINCHINA', 239.0: 'DURANIA', 261.0: 'EL ZULIA', 344.0: 'HATO', 498.0: 'OCAMONTE', 553.0: 'PUERTO SANTANDER', 786.0: 'TAMINANGO', 788.0: 'TANGUA', 327.0: 'GUEPSA', 406.0: 'LEBRIJA', 432.0: 'MALAGA', 444.0: 'MARQUETALIA', 502.0: 'ONZAGA', 547.0: 'PIEDRAS', 575.0: 'PUERTO WILCHES', 669.0: 'PUERTO SANTANDER', 684.0: 'SAN JOSE DE MIRANDA', 705.0: 'SANTA BARBARA', 773.0: 'CUMARIBO', 24.0: 'ALPUJARRA', 43.0: 'ANZOATEGUI', 67.0: 'ATACO', 230.0: 'OROCUE', 265.0: 'GUARANDA', 275.0: 'FLORIDA', 283.0: 'FRESNO', 408.0: 'LERIDA', 429.0: 'MAJAGUAL', 508.0: 'OVEJAS', 523.0: 'PALMITO', 702.0: 'SAN JUAN DE BETULIA', 708.0: 'SAN MARCOS', 713.0: 'SAN ONOFRE', 717.0: 'SAN PEDRO', 742.0: 'SINCE', 771.0: 'SUCRE', 41.0: 'ANSERMANUEVO', 54.0: 'ARGELIA', 122.0: 'CAICEDONIA', 243.0: 'EL AGUILA', 246.0: 'EL CAIRO', 449.0: 'MELGAR', 461.0: 'MURILLO', 497.0: 'OBANDO', 504.0: 'ORTEGA', 563.0: 'PRADO', 616.0: 'RISARALDA', 624.0: 'ROVIRA', 671.0: 'SALDAÑA', 870.0: 'VILLAHERMOSA', 65.0: 'ARAUQUITA', 136.0: 'LA SALINA', 139.0: 'MANI', 219.0: 'COLON', 220.0: 'CRAVO NORTE', 225.0: 'NUNCHIA', 263.0: 'EL ENCANTO', 569.0: 'PUERTO CAICEDO', 571.0: 'PUERTO GUZMAN', 749.0: 'SIBUNDOY', 794.0: 'TAME', 828.0: 'TRUJILLO', 834.0: 'TULUA', 863.0: 'VERSALLES', 865.0: 'LA HORMIGA (VALLE DEL GUAMUEZ)', 869.0: 'VIJES', 892.0: 'YUMBO', 343.0: 'BARRANCO MINAS', 536.0: 'PUERTO ARICA', 564.0: 'PROVIDENCIA', 666.0: 'TARAIRA', 883.0: 'SAN FELIPE', 884.0: 'PUERTO COLOMBIA', 886.0: 'CACAHUAL', 888.0: 'MORICHAL (MORICHAL NUEVO)', 889.0: 'YAVARATE', 388.0: 'LA MERCED', 446.0: 'MARULANDA', 877.0: 'VITERBO'}
# Ordenar el diccionario por los valores
municipio_dict = dict(sorted(municipio_dict_1.items(), key=lambda item: item[1]))

# mapeo tipo usuario
tipo_usuario_map = {1:"Contributivo", 2:"Subsidiado", 3: "Vinculado", 4:"Particular", 5:"Otro", 6:"Víctima con afiliación al Régimen Contributivo",
                    7:"Víctima con afiliación al Régimen subsidiado", 8:"Víctima no asegurado (Vinculado)"}

# mapeo dia semana
dia_semana_map = {"Lunes": 2, "Martes": 3, "Miércoles": 4, "Jueves": 1, "Viernes": 6, "Sábado": 5, "Domingo": 0}

# mapeo sexo
sexo_map = {1:"Masculino", 0:"Femenino"}  # Asume valores 'M' y 'F' para Masculino y Femenino

causa_externa_map = {1:"Accidente de trabajo", 2:"Accidente de tránsito", 3:"Accidente rábico", 4:"Accidente ofídico",
                     5:"Otro tipo de accidente", 6:"Evento catastrófico", 7:"Lesión por agresión", 8:"Lesión auto infligida",
                     9:"Sospecha de maltrato físico", 10:"Sospecha de abuso sexual", 11:"Sospecha de violencia sexual",
                     12:"Sospecha de maltrato emocional", 13:"Enfermedad general", 14:"Enfermedad laboral", 15: "Otra"}

# Cargar el modelo
with open("lgb_model_early_stop_2.pkl", "rb") as file:
    model = pickle.load(file)

# # Cargar el modelo
# with open("/home/ubuntu/TFM2025VIU/lgb_model_early_stop_2.pkl", "rb") as file:
#     model = pickle.load(file)

# Título de la aplicación
st.title("Predicción Destino del Paciente en Urgencias")
st.write("Introduce los datos del paciente para realizar la predicción.")

# Crear entradas para las variables

# Selector de fecha
fecha = st.date_input("Fecha de ingreso del paciente", value=datetime.now().date())
Mes = fecha.month
Dia_del_mes = fecha.day

# Selector de hora
hora = st.time_input("Hora de ingreso del paciente")
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




############################################################################################################################

# Crear una lista desplegable con un mensaje inicial
options = ["Seleccione una IPS"] + list(prestadores_dict.values())
prestador_seleccionado = st.selectbox(
    "Nombre del Prestador",
    options=options
)

# Verificar si el usuario seleccionó una opción válida
if prestador_seleccionado == "Seleccione una IPS":
    st.warning("Por favor, seleccione una IPS válida.")
else:
    # Obtener el código del prestador seleccionado
    CodigoPrestador = [codigo for codigo, nombre in prestadores_dict.items() if nombre == prestador_seleccionado][0]
    st.success(f"Prestador seleccionado correctamente")

############################################################################################################################

# prestador_seleccionado = st.selectbox(
#     "Seleccione el prestador",
#     options=list(prestadores_dict.values())  # Mostrar nombres de prestadores
# )
# # Obtener el código del prestador seleccionado
# CodigoPrestador = [codigo for codigo, nombre in prestadores_dict.items() if nombre == prestador_seleccionado][0]

############################################################################################################################

# Crear una lista desplegable con un mensaje inicial
options = ["Seleccione una EPS o Aseguradora"] + list(eps_dict.values())
eps_seleccionada = st.selectbox(
    "Nombre de la EPS o Aseguradora",
    options=options
)

# Verificar si el usuario seleccionó una opción válida
if eps_seleccionada == "Seleccione una EPS o Aseguradora":
    st.warning("Por favor, seleccione una EPS o Aseguradora válida.")
else:
    # Obtener el código del prestador seleccionado
    codigoEPS = [codigo for codigo, nombre in eps_dict.items() if nombre == eps_seleccionada][0]
    st.success(f"EPS o Aseguradora seleccionada correctamente")

############################################################################################################################


# Ingresar Edad
Edad = st.number_input("Edad del paciente(años)", min_value=0, max_value=120)
if Edad < 12:
    Grupo_etario = 3
elif 12 <= Edad < 18:
    Grupo_etario = 0
elif 18 <= Edad < 60:
    Grupo_etario = 1
else:
    Grupo_etario = 2

############################################################################################################################

# Crear una lista desplegable con un mensaje inicial
options = ["Seleccione una opción"] + list(tipo_usuario_map.values())
tipo_seleccionado = st.selectbox(
    "Tipo de usuario",
    options=options
)

# Verificar si el usuario seleccionó una opción válida
if tipo_seleccionado == "Seleccione una opción":
    st.warning("Por favor, seleccione una opción válida.")
else:
    # Obtener el código del prestador seleccionado
    codigo_tipo_usuario = [codigo for codigo, nombre in tipo_usuario_map.items() if nombre == tipo_seleccionado][0]
    st.success(f"Opción seleccionada correctamente")

############################################################################################################################

# Crear una lista desplegable con un mensaje inicial
options = ["Seleccione un municipio"] + list(municipio_dict.values())
municipio_seleccionado = st.selectbox(
    "Nombre del municipio donde reside el paciente",
    options=options
)

# Verificar si el usuario seleccionó una opción válida
if municipio_seleccionado == "Seleccione un municipio":
    st.warning("Por favor, seleccione un municipio válido.")
else:
    # Obtener el código del prestador seleccionado
    CodigoMunicipio = [codigo for codigo, nombre in municipio_dict.items() if nombre == municipio_seleccionado][0]
    st.success(f"Municipio seleccionado correctamente")

############################################################################################################################

# Dia_del_mes = st.number_input("Día del mes", min_value=1, max_value=31, step=1)
# Nombre_asegurador = st.text_input("Nombre del Asegurador")
# HoraIngreso = st.text_input("Hora de Ingreso (HH:MM)")
# Mes = st.number_input("Mes", min_value=1, max_value=12, step=1)
# TipoUsuario = st.text_input("Tipo de Usuario")
# Dia_de_la_semana = st.text_input("Día de la semana")
# CodigoMunicipio = st.number_input("Código Municipio", min_value=1, step=1)
# Crear una lista desplegable con un mensaje inicial

options = ["Seleccione una causa externa"] + list(causa_externa_map.values())
causa_externa_seleccionada = st.selectbox(
    "Causa Externa",
    options=options
)

# Verificar si el usuario seleccionó una opción válida
if causa_externa_seleccionada == "Seleccione una causa externa":
    st.warning("Por favor, seleccione una causa externa válida.")
else:
    # Obtener el código del prestador seleccionado
    codigo_causa_externa = [codigo for codigo, nombre in causa_externa_map.items() if nombre == causa_externa_seleccionada][0]
    st.success(f"Causa externa seleccionada correctamente")

# CausaExterna = st.text_input("Causa Externa")
# Grupo_etario = st.text_input("Grupo Etario")
############################################################################################################################

if 0 <= HoraIngreso < 6:
    Rango_horario_ingreso = 0 #"Madrugada"
elif 6 <= HoraIngreso < 12:
    Rango_horario_ingreso = 1 #"Mañana"
elif 12 <= HoraIngreso < 18:
    Rango_horario_ingreso = 3 #"Tarde"
else:
    Rango_horario_ingreso = 2 #"Noche"

############################################################################################################################

options = ["Seleccione el sexo del paciente"] + list(sexo_map.values())
sexo_seleccionado = st.selectbox(
    "Sexo",
    options=options
)

# Verificar si el usuario seleccionó una opción válida
if sexo_seleccionado == "Seleccione el sexo del paciente":
    st.warning("Por favor, seleccione una opción válida.")
else:
    # Obtener el código del prestador seleccionado
    codigo_sexo = [codigo for codigo, nombre in sexo_map.items() if nombre == sexo_seleccionado][0]
    st.success(f"Sexo seleccionado correctamente")

############################################################################################################################

# Botón para predecir
if st.button("Predecir"):

    try:
        # Procesar las variables que requieren conversión
        CodigoPrestador = int(CodigoPrestador)
        HoraIngreso = int(HoraIngreso)
        Edad = int(Edad)
        Dia_del_mes = int(Dia_del_mes)
        Mes = int(Mes)
        CodigoMunicipio = int(CodigoMunicipio)
        CausaExterna = int(codigo_causa_externa)
        Grupo_etario = int(Grupo_etario)
        Rango_horario_ingreso = int(Rango_horario_ingreso)
        codigoEPS = int(codigoEPS)
        TipoUsuario = int(codigo_tipo_usuario)
        Dia_de_la_semana = int(Dia_de_la_semana)

        # Convertir variables categóricas
        # TipoUsuario = tipo_usuario_map.get(codigo_tipo_usuario, 0)  # Valor por defecto 0 si no se encuentra
        # Dia_de_la_semana = dia_semana_map.get(Dia_del_mes, 0)
        Sexo = int(codigo_sexo)

        # Asume que otras variables categóricas ya están codificadas o agrega mapeos adicionales

        # Procesar HoraIngreso (convertir a número entero de horas)
        # HoraIngreso_horas = int(HoraIngreso.split(":")[0]) if ":" in HoraIngreso else 0

        # Crear un DataFrame con los datos procesados
        input_data = pd.DataFrame({
            "CodigoPrestador": [CodigoPrestador],
            "Edad": [Edad],
            "Día del mes": [Dia_del_mes],
            "Nombre asegurador": [codigoEPS],  # Asume 0 como placeholder (requiere codificación real)
            "HoraIngreso": [HoraIngreso],
            "Mes": [Mes],
            "TipoUsuario": [TipoUsuario],
            "Día de la semana": [Dia_de_la_semana],
            "CódigoMunicipio": [CodigoMunicipio],
            "CausaExterna": [CausaExterna],  # Asume 0 como placeholder
            "Grupo etario": [Grupo_etario],  # Asume 0 como placeholder
            "Rango horario ingreso": [Rango_horario_ingreso],  # Asume 0 como placeholder
            "Sexo": [Sexo]
        })

        print(CodigoPrestador)
        print(Edad)
        print(Dia_del_mes)
        print(codigoEPS)
        print(HoraIngreso)
        print(Mes)
        print(TipoUsuario)
        print(Dia_de_la_semana)
        print(CodigoMunicipio)
        print(CausaExterna)
        print(Grupo_etario)
        print(Rango_horario_ingreso)
        print(Sexo)

        # Realizar la predicción
        prediction = model.predict(input_data)[0]
        if prediction == 1:
            prediction = 'Dado de alta de urgencias'
        
        elif prediction == 2:
            prediction = 'Remitido a otro nivel de complejidad'
        
        else:
            prediction = 'Hospitalizado'    


        # Mostrar el resultado
        st.success(f"El paciente tiene una alta probabilidad de ser: {prediction}")

    except Exception as e:
        st.error(f"Hubo un error al procesar los datos: {e}")
