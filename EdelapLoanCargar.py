from operator import index
import pandas as pd
import numpy as np
import os

def EdelapLoanCargar(df, archivo):
    #-------------Validador--------------#
    titulo = 'Validador de columnas'
    print('')
    print(titulo.center(len(titulo)+70, '-'))

    columnas = df.columns 
    columnas_validas = ['DOCUMENTO', 'NUMEROOPERACION', 'FECHA', 'IMPORTE_COBRADO','IDCOMPANIA']

    for i in columnas:
        if i in columnas_validas:
            columnas_validas.remove(i)

    if not columnas_validas:
        print('Columnas válidas')
    else: 
        print(f'Columnas faltantes: {columnas_validas}')
    #----------------UTILIDADES-----------------#
    registros = df.shape[0]
    lista_vacia = [] #Utilizada para varias columnas que deben estar vacías
    for i in range (0, registros):
        lista_vacia.append(np.nan)

    #----------------A - DOCUMENTO-----------------#
    df_a = df['DOCUMENTO']
    #----------------B NUMEROCONVENIO -----------------#
    dicc = {
        'NUMEROCONVENIO' : lista_vacia,
    }
    df_b = pd.DataFrame(dicc)

    #---------------- C - NUMEROOPERACION -----------------#
    df_c = df['NUMEROOPERACION']
    #----------------D - COMPAÑÍA-----------------#
    df_d = df['IDCOMPANIA']
    lista = []
    for i in df_d:
        lista.append(i)
    df_d = pd.DataFrame({'COMPANIA' : lista})
    #----------------E - FECHAPAGO-----------------#
    df_e = df['FECHA']
    lista = []
    for i in df_e:
        i = str(i)
        año = i[0:4]
        mes = i[5:7]
        dia = i[8:10]
        formato = f'{dia}/{mes}/{año}'
        lista.append(formato)
    df_e = pd.DataFrame({'FECHAPAGO' : lista})
    #----------------F - IMPORTECONSOLIDADO-----------------#
    df_f = df['IMPORTE_COBRADO']
    lista = []
    for i in df_f:
        lista.append((i))
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
    df_concat = pd.concat([df_a, df_b, df_c, df_d, df_e, df_f, df_gk, df_l], axis=1)

    #--------------OBTENER EXCEL-------------#
    try:
        df_concat.to_excel('archivos/EmpresaLoanCargar/EdelapLoanCargar.xlsx', index=False)
        print("Archivo 'EdelapLoanCargar' creado correctamente")
    except:
        print("Error al crear el archivo 'EdelapLoanCargar'")

    