from operator import index
import pandas as pd
import numpy as np
import os

def CredicuotasLoanCargar(df, archivo):
    #-------------Validador--------------#
    titulo = 'Validador de columnas'
    print('')
    print(titulo.center(len(titulo)+70, '-'))

    columnas = df.columns 
    columnas_validas = ['f_valor', 'DNI', 'Importe']

    for i in columnas:
        if i in columnas_validas:
            columnas_validas.remove(i)

    if not columnas_validas:
        print('Columnas válidas')
    else: 
        print(f'Columnas faltantes: {columnas_validas}')

    #Filtro de Los registros que Se liquida
    col1 = df['Liq']
    df_final = df[~df['Liq'].str.contains('No se liquida', case=False, na=False)]

    df_final = df_final.drop(['IdCredito', 'Origen', 'Liq', 'Convenio'], axis=1)

    df_final.rename(columns={'f_valor' : 'FECHAPAGO',
                             'Importe' : 'IMPORTECONSOLIDADO',
                             'DNI': 'DOCUMENTO'}, inplace=True)

    df_final = df_final[['DOCUMENTO', 'FECHAPAGO', 'IMPORTECONSOLIDADO']]

    df_final = df_final.reset_index(drop=True)

    #----------------UTILIDADES-----------------#
    registros = df_final.shape[0]
    lista_vacia = [] #Utilizada para varias columnas que deben estar vacías
    for i in range (0, registros):
        lista_vacia.append(np.nan)

    #----------------A - DOCUMENTO-----------------#
    df_a = df_final['DOCUMENTO']

    #----------------B,C-----------------#
    dicc = {
        'NUMEROCONVENIO' : lista_vacia,
        'NUMEROOPERACION' : lista_vacia
    }
    df_bc = pd.DataFrame(dicc)

    #----------------D - COMPAÑÍA-----------------#
    lista = os.path.splitext(archivo)
    valor = lista[0][11:14]

    lista = []
    for i in range(0, registros):
        lista.append(int(valor)) 
    df_d = pd.DataFrame({'COMPANIA' : lista})

    #----------------E - FECHAPAGO-----------------#
    df_final['FECHAPAGO'] = pd.to_datetime(df_final['FECHAPAGO'])
    df_final['FECHAPAGO'] = pd.to_datetime(df_final['FECHAPAGO'], format="%d/%m/%Y", dayfirst=True)
    df_final['FECHAPAGO'] = df_final['FECHAPAGO'].dt.strftime('%d/%m/%Y')

    df_e = pd.DataFrame(df_final['FECHAPAGO'])
    #df_e.rename(columns={'f_valor' : 'FECHAPAGO'}, inplace=True)

    #----------------F - IMPORTECONSOLIDADO-----------------#
    df_f = pd.DataFrame(df_final['IMPORTECONSOLIDADO'])
    #df_f.rename(columns={'Importe' : 'IMPORTECONSOLIDADO'}, inplace=True)

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
        df_concat.to_excel('archivos/EmpresaLoanCargar/CredicuotasLoanCargar.xlsx', index=False)
        print("Archivo 'CredicuotasLoanCargar' creado correctamente")
    except:
        print("Error al crear el archivo 'CredicuotasLoanCargar'")

    