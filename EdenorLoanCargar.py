import pandas as pd
import numpy as np
import os

def EdenorLoanCargar(df_actual, archivo_actual):
    dia = archivo_actual[21:23]
    mes = archivo_actual[24:26]
    año = archivo_actual[27:31]

    fecha = f'{año}-{mes}-{dia}'
    mask = (df_actual['FEC_REGISTRO'] >= fecha)
    df_actual = df_actual.loc[mask]
    
    df_actual = df_actual.reset_index(drop=True)

    #-------------Validador--------------#
    titulo = 'Validador de columnas'
    print('')
    print(titulo.center(len(titulo)+70, '-'))

    columnas = df_actual.columns 
    columnas_validas = ['ID_CUENTA', 'FEC_REGISTRO',
    'FEC_PAGO', 'MONTO']

    for i in columnas:
        if i in columnas_validas:
            columnas_validas.remove(i)

    if not columnas_validas:
        print('Columnas válidas')
    else: 
        print(f'Columnas faltantes: {columnas_validas}')

    #----------------UTILIDADES-----------------#
    registros = df_actual.shape[0]
    lista_vacia = [] #Utilizada para varias columnas que deben estar vacías
    for i in range (0, registros):
        lista_vacia.append(np.nan)

    #----------------A - DOCUMENTO-----------------#
    df_a = df_actual['ID_CUENTA']

    #----------------B NUMEROCONVENIO -----------------#
    dicc = {
        'NUMEROCONVENIO' : lista_vacia,
        'NUMEROOPERACION' : lista_vacia
    }
    df_bc = pd.DataFrame(dicc)

    #----------------D - COMPAÑÍA-----------------#
    lista = os.path.splitext(archivo_actual)
    valor = lista[0][11:14]

    lista = []
    for i in range(0, registros):
        lista.append(int(valor)) 
    df_d = pd.DataFrame({'COMPANIA' : lista})

    #----------------E - FECHAPAGO-----------------#
    df_e = df_actual['FEC_PAGO']
    lista = []
    for i in df_e:
        año = i[:4]
        mes = i[5:7]
        dia = i[8:10]
        i = f'{dia}/{mes}/{año}'
        lista.append(i)
    df_e = pd.DataFrame({'FECHAPAGO' : lista})

    #----------------F - IMPORTECONSOLIDADO-----------------#
    df_f = df_actual['MONTO']
    lista = []
    for i in df_f:
        i = i.replace(',', '.')
        lista.append(float(i))
    df_f = pd.DataFrame({'IMPORTECONSOLIDADO' : lista})

    #----------------G, H, I, J, K-----------------#
    dicc = {
        'IMPORTECAPITAL' : lista_vacia,
        'IMPORTEHONORARIOS' : lista_vacia,
        'IMPORTECOMISIONCANALPAGO' : lista_vacia,
        'OBSERVACION' : lista_vacia,
        'CANALPAGO' : lista_vacia
    }
    df_gk = pd.DataFrame(dicc)

    #----------------L - NUMERORECIBO-----------------#
    lista = []
    for i in range(registros):
        lista.append(i+1)

    dicc = {
        'NUMERORECIBO' : lista
    }
    df_l = pd.DataFrame(dicc)

    #--------------CONCATENAR COLUMNAS-------------#
    df_concat = pd.concat([df_a, df_bc, df_d, df_e, df_f, df_gk, df_l], axis=1)

    #--------------OBTENER EXCEL-------------#
    try:
        df_concat.to_excel('archivos/EmpresaLoanCargar/EdenorLoanCargar.xlsx', index=False)
        print("Archivo 'EdenorLoanCargar' creado correctamente")
    except:
        print("Error al crear el archivo 'EdenorLoanCargar'")