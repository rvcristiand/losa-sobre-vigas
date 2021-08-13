import numpy as np
from docxtpl import DocxTemplate


doc = DocxTemplate("Losa sobre vigas.docx")

def design(params):
    # datos de entrada

    fc = params['fc'] = params.get('fc', 28)
    fy = 420
    L = params['L'] = params.get('L', 10)
    ancho_de_carril = params['ancho_de_carril'] = params.get('ancho_de_carril', 3.6)
    ancho_de_berma = params['ancho_de_berma'] = params.get('ancho_de_berma', 1)
    ancho_de_anden = params['ancho_de_anden'] = params.get('ancho_de_anden', 0)
    espesor_de_carpeta_asfaltica = params['espesor_de_carpeta_asfaltica'] = params.get('espesor_de_carpeta_asfaltica', 0.1)
    ancho_inferior_de_bordillo = params['ancho_inferior_de_bordillo'] = params.get('ancho_inferior_de_bordillo', 0.2)
    ancho_superior_de_bordillo = params['ancho_superior_de_bordillo'] = params.get('ancho_superior_de_bordillo', 0.2)
    altura_de_bordillo = params['altura_de_bordillo'] = params.get('altura_de_bordillo', 0.3)
    h = params['h'] = params.get('h', 0.22)
    S_entre_vigas = params['S_entre_vigas'] = params.get('S_entre_vigas', 2.55)
    dist_eje_viga_borde = params['dist_eje_vig_borde'] = params.get('dist_eje_vig_borde', 0.9)
    num_carriles = params['num_carriles'] = params.get('num_carriles', 2)
    # TODO: agregar num_carriles params

    ancho_total = params['ancho_total'] = (((ancho_de_carril *num_carriles / 2 )+ ancho_de_berma + ancho_de_anden + ancho_inferior_de_bordillo) * 2)
    
    #Solicitaciones
    #Por carga muerta
    # pesos especificos en kN/m3
    pespecifico_concreto = params['pespecifico_concreto'] = 2.4 * 10
    pespecifico_carpeta_asfaltica = params['pespecifico_carpeta_asfaltica'] = 2.2 * 9.81

    # Cargas distrbuidas muertas
    DC = params['DC'] = pespecifico_concreto * h
    DW = params['DW'] = (pespecifico_carpeta_asfaltica * espesor_de_carpeta_asfaltica)

    #Momentos máximos
    # Cargas Permanentes
    # Unidades en kN/m
    MDC = params['MDC'] = params.get('MDC', 4.68)
    MDW = params['MDW'] = params.get('MDW', 1.94)

    
    #Momento maximo debido a la carga vehicular de diseño con amplificación dinámica (Ver tabla A4 CC-14)

    MLLIMpos =params['MLLIMpos']= params.get('MLLIMpos',30.8)
    
    MLLIMneg = params['MLLIMneg'] = params.get('MLLIMneg',23.12) 
    
    #Diseño a Flexión
    #Factores de modificación de carga 1.3.2
    #Factor relacionado cola ductilidad
    factor_ductilidad = 1

    #Factor relacionado con la redundancia
    factor_redundancia = 1

    #Factor relacionado con la importancia operativa
    factor_imp_operativa = 1

    factor_mod_carga = params['factor_mod_carga'] = factor_ductilidad *  factor_imp_operativa * factor_redundancia
    
    # Momento ultimo positivo
    Mupos = params['Mupos'] = factor_mod_carga * ( 1.25 * MDC + 1.5 * MDW + 1.75 * MLLIMpos )

    # Recubrimiento de armadura principal no protegida Tabla 5.12.3.1
    recub = params['recub'] = params.get('d',0.06)
    # factor phi para diseño a flexión
    phi = 0.9
    d = params['d'] = round(h - recub,3)
    

    cuantia_kN_pos = params['cuantia_kN_pos'] = round(( 1 - ( 1 - ( 2 * Mupos / ( phi * 1 * d ** 2 * 0.85 * fc * 1000 ) ) ) ** 0.5 ) * 0.85 * fc /  fy, 5)  
    
    #Area de refuerzo de la losa en cm2
    As_flexion = params['As_flexion'] = round(cuantia_kN_pos * d * 100 * 100, 2)

    #Para barras #8 As = 5.1 cm2
    As_5 = params['As_5'] = 1.99 # definir al inicio
    No_barras_5_flexion_pos = params['No_barras_5_flexion_pos'] = round(As_flexion / As_5)

    #Espaciamiento Armadura a flexión para momentos positivo
    espac_arm_prin_flexion_pos = params['espac_arm_prin_flexion_pos'] = round (100 / No_barras_5_flexion_pos)

    # Revisión del factor phi = 0.9 para el diseño a flexión para momentos positivo

    a_f_pos = params['a_f_pos'] = round(cuantia_kN_pos * d * fy /( 0.85 * fc), 4)

    #profundidad eje neutro

    betha_1 = 0.85
    c_f_pos = params['c_f_pos'] = round(a_f_pos / betha_1 , 4) 

    #Relacion de  deformaciones en la sección de concreto reforzado

    defor_total_pos = params['defor_total_pos'] = round((d - c_f_pos) * (0.003 / c_f_pos), 4)  

    # Momento ultimo negativo
    Muneg = params['Muneg'] = factor_mod_carga * ( 1.25 * MDC + 1.5 * MDW + 1.75 * MLLIMneg )
   
    cuantia_kN_neg =  params['cuantia_kN_neg'] = round(( 1 - ( 1 - ( 2 * Muneg / ( phi * 1 * d ** 2 * 0.85 * fc * 1000 ) ) ) ** 0.5 ) * 0.85 * fc /  fy, 5)  

    #Area de refuerzo de la losa en cm2
    As_flexion_neg = params['As_flexion_neg'] = round(cuantia_kN_neg * d * 100 * 100, 2)

    #Para barras #8 As = 5.1 cm2

    No_barras_5_flexion_neg = params['No_barras_5_flexion_neg'] = round(As_flexion_neg / As_5)
    
    #Espaciamiento Armadura a flexión para momentos positivo
    espac_arm_prin_flexion_neg = params['espac_arm_prin_flexion_neg'] = round (100 / No_barras_5_flexion_neg)
    

    # Revisión del factor phi = 0.9 para el diseño a flexión para momentos positivo

    a_f_neg = params['a_f_neg'] = round(cuantia_kN_neg * d * fy /( 0.85 * fc), 4)
    
    #profundidad eje neutro

    betha_1 = 0.85
    c_f_neg = params['c_f_neg'] = round(a_f_neg / betha_1 , 4) 

    #Relacion de  deformaciones en la sección de concreto reforzado

    defor_total_neg = params['defor_total_neg'] = round((d - c_f_neg) * (0.003 / c_f_neg), 4)  
    
    #Armadura dedistribución para losas con armadura principal paralela a la dirección del trafico (9.7.3.2)

    Armadura_de_distribucion = params['Armadura_de_distribucion'] = round(3840 / (S_entre_vigas*1000) ** 0.5 / 100, 2 )
    
    if Armadura_de_distribucion > 0.67 :
        Armadura_de_distribucion = 0.67

    As_4 = 1.29
    As_Armadura_de_distribucion = params['As_Armadura_de_distribucion'] = round ( Armadura_de_distribucion * As_flexion , 2)

    No_barras_4_dist = params['No_barras_4_dist'] =  round( As_Armadura_de_distribucion / As_4 )
    
    espac_arm_dist = params['espac_arm_dist'] =  round( 100 / No_barras_4_dist )

    #Armadura minima
    #Modulo de rotura del concreto
    fr = params['fr'] = round(0.62 * fc ** 0.5, 2)
    
    # factor de variacion de l afisuracion por flexion 5.7.3.3.2 
    gamma_1 = params['gamma_1'] = params.get('gamma_1',1.6)

    #relacion entre la reistencia especificada a fluencia y la resistencia ultima atracción del refuerzo
    #refuerzo a706, Grado 60
    gamma_3 = params['gamma_3'] = params.get('gamma_3',0.75)

    #Modulo elastico de la seccion

    Sc = params['Sc'] = round(1 * h ** 2 / 6, 4 )
    
    Mcr = params['Mcr'] = round (gamma_1 ** 2 * gamma_3 * fr * Sc * 1000)
    
    if Mcr > Muneg :
        print ('No cumple Armadura mínima')
    
    # Control de fisuración
    # Factor de exposición clase 1. 5.7.3.4 
    gamma_e = params['gamma_e'] = params.get('gamma_e',1.0)

    #De acuerdo con 5.12.3-1, el espesor de recubrimiento de concreto medido desde la fibra extrema a tracción hasta el centro del refuerzo de flexión mas cercano, para losas vaciadas in situ 25 mm

    d_c = params['d_c'] = params.get('d_c',0.025+0.0159/2)

    if d_c < 0.05 :
        d_cf = 0.05
    params['d_cf'] = d_cf

    #De acuerdo con el Art 5.7.3.4, el coeficiente beta s 
    beta_s = params['beta_s'] = round (1 + d_cf / (0.7 * (h - d_cf)), 3)

    #Calculo de fss: Esfuerzo actuante a tracción en el acero para estado limite de servicio I
    
    #Combinación para el estado limite de servicio tabla 3.4.1
    Msi = params['Msi'] = 1 * (MDC + MDW + MLLIMpos)

    # Modulo de elasticidad del concreto - densidad normal MPa

    E_concreto = params['E_concreto'] = round(0.043 * 2350 ** 1.5 * (fc) ** 0.5, 2)

    # Modulo de elasticidad del acero MPa
    
    E_acero = params['E_acero'] = params.get('E_acero', 200000)

    #Relación modular

    rel_mod = params['rel_mod'] = round(E_acero / E_concreto)

    #Momento de primer orden de la sección  fisurada, de 1m de ancho, con respecto al eje neutro

    #Tomando momentos con respecto al eje neutro de la sección:

    X_cf = params['X_cf'] = round (( -(2 * rel_mod * As_flexion * 10 ** -4) + ((2 * rel_mod * As_flexion * 10 ** -4 ) ** 2 - (4 * 1 * -2 * rel_mod * As_flexion * 10 ** -4 * d )) ** 0.5 ) / (2 * 1), 2)

    # Momento de inercia de la seccion fisurada
    d_ = params['d_'] = (h - d_c)
    I_c = params['I_c'] = round(X_cf ** 3 / 3 + rel_mod * As_flexion * 10 ** -4 * (d_ - X_cf) ** 2, 8)
    

    fss = params['fss'] = round (rel_mod * Msi * (d_ - X_cf) / I_c / 1000, 2)

    # Reemplazando en la ecuación 5.7.3.4.1
    
    espac_control_fisuracion = params['espac_control_fisuracion'] = round((123000 * gamma_e / (beta_s * fss) ) - (2 * d_cf * 1000))

    if espac_control_fisuracion / 100 > espac_arm_prin_flexion_pos :
        print ('No cumple control de fisuración')

    # Separacion centro a centro de barras 
    diametro_barra_8 = 2.54
    espac_libre = params['espac_libre'] = espac_arm_prin_flexion_pos - diametro_barra_8 
    
    # Espaciamiento minimo de la armadura vaciada in situ 5.10.3 
    
    #tamaño agregado 3/4in en cm
    tamaño_agregado = 1.905

    if espac_libre < 1.5 * diametro_barra_8 :
        print ('No cumple espaciamineto minimo 5.10.3')
    if espac_libre < 1.5 * tamaño_agregado :
        print ('No cumple espaciamineto minimo 5.10.3')
    if espac_libre < 3.8 :
        print ('No cumple espaciamineto minimo 5.10.3')

    #Armadura por retraccion de fraguado y temperatura
    As_retytemp = round(750 * ancho_total * h / (2 * (ancho_total + h) * fy) * 1000)

    if 234 > As_retytemp :
        As_retytemp = 234
    if  As_retytemp > 1278:
        print ('No cumple Retraccion y Temperatura') 
    params['As_retytemp'] = As_retytemp
    As_3 = 0.71
    No_barras_3_retytemp = params ['No_barras_3_retytemp'] = round (As_retytemp /100 / As_3, 2) 

    espa_arm_retytemp = params['espa_arm_retytemp'] = round(100 / No_barras_3_retytemp)
    
    h3 = params['h3'] = round(3 * h)
    

    #Franja exterior del puente 
    #De acuerdo con 4.6.2.1.4b 
    dist_aplicacion_P = params['dist_aplicacion_P'] = params.get('dist_aplicacion_P', 0.3) # Según 3.6.1.3.1
    dist_ancho_franja_equiv = params['dist_ancho_franja_equiv'] = dist_eje_viga_borde - ancho_inferior_de_bordillo - dist_aplicacion_P
    
    E_borde = params['E_borde'] = round(1.14 + 0.833 * dist_ancho_franja_equiv , 2)

    #Avaluo de cargas permanentes para la franja exterior
    DC_bordillo = params['DC_bordillo'] = round(altura_de_bordillo * ancho_inferior_de_bordillo * pespecifico_concreto , 2)

    DC_ext = params['DC_ext'] = round(pespecifico_concreto * (h * dist_eje_viga_borde) , 2)

    DC_barrera = params['DC_barrera'] = params.get('DC_barrera',round(0.07 * 9.81 , 2))

    DW_ext = params['DW_ext'] = round(pespecifico_carpeta_asfaltica * espesor_de_carpeta_asfaltica  , 2) 

    #Momentos maximos debidos a cargas permanentes

    MDC_ext = params['MDC_ext'] = round( DC_bordillo * (dist_eje_viga_borde - ancho_inferior_de_bordillo/2) + DC_ext * dist_eje_viga_borde/2 + DC_barrera * (dist_eje_viga_borde - ancho_inferior_de_bordillo), 2)

    MDW_ext = params['MDW_ext'] = round(DW_ext * (dist_eje_viga_borde - ancho_inferior_de_bordillo) ** 2 / 2 , 2)
    
    
    #Momento debido a carga viva
    # Debido a que sobre la franja exterior actua una rueda y no un eje, se dividen las solicitaciones en 2 y en el ancho de la franja exterior
    MLLIM_ext = params['MLLIM_ext'] = round(80 * dist_ancho_franja_equiv * 1.33/ E_borde, 2)

    #Determinacion de armadura a flexion de franja exterior
    
    Mu_ext = params['Mu_ext'] = round((1.25 * MDC_ext + 1.5 * MDW_ext + 1.75 * MLLIM_ext), 2)
    
    #cuantia franja exterior 
    
    cuantia_ext = params['cuantia_ext'] = round(( 1 - ( 1 - ( 2 * Mu_ext / ( phi * 1 * d ** 2 * 0.85 * fc * 1000 ) ) ) ** 0.5 ) * 0.85 * fc /  fy, 4)

    As_flexion_ext = params['As_flexion_ext'] = round(cuantia_ext * d * 100 * 100)

    #Numero de barras #8 flexion franja exterior

    No_barras_5_flexion_ext = params['No_barras_5_flexion_ext'] = round (As_flexion_ext / As_5) 

    #Separacion de barras a flexion franja exterior

    espac_arm_prin_flexion_ext = params['espac_arm_prin_flexion_ext'] = round (100 / No_barras_5_flexion_ext)

    return params


def report(dict):
    string = ''

    def add(key):
        return "{}: {}".format(key, dict[key])

    string += add('nombre') + '\n'
    string += add('L')

    
    return string


if __name__ == "__main__":
    params = {}

    params = design(params)

    doc.render(params)
    doc.save('Memoria de cálculos de la losa sobre vigas.docx')

