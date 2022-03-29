import pandas as pd
import numpy as np 
import os 

def FertilLoanCargar(df_anterior, df_actual, nArchivo_actual):
    #-------------Validador--------------#
    titulo = 'Validador de columnas'
    print('')
    print(titulo.center(len(titulo)+70, '-'))

    columnas_df1 = df_anterior.columns 
    columnas_df2 = df_actual.columns 

    columnas_validas1 = ['FECHA', 'DNI ', 'IMPORTE']
    columnas_validas2 = ['FECHA', 'DNI ', 'IMPORTE']

    for i in columnas_df1:
        if i in columnas_validas1:
            columnas_validas1.remove(i)

    if not columnas_validas1:
        print('Columnas válidas del Dataframe anterior')
    else: 
        print(f'Columnas faltantes del Dataframe anterior: {columnas_validas1}')

    for i in columnas_df2:
        if i in columnas_validas2:
            columnas_validas2.remove(i)

    if not columnas_validas2:
        print('Columnas válidas del Dataframe actual')
    else: 
        print(f'Columnas faltantes del Dataframe actual: {columnas_validas2}')

    df_concat = pd.concat([df_anterior, df_actual])
    df_concat = df_concat.drop_duplicates(keep=False) #Elimino los valores duplicados
    df_concat.drop(['Unnamed: 7'], axis=1, inplace=True) #Elimino la última columna con el total por mes
    df_concat = df_concat.reset_index(drop=True) #Reseteo de index

    #----------------UTILIDADES-----------------#
    registros = df_concat.shape[0]
    lista_vacia = [] #Utilizada para varias columnas que deben estar vacías
    for i in range (0, registros):
        lista_vacia.append(np.nan)

    #----------------A - DOCUMENTO-----------------#
    df_a = pd.DataFrame(df_concat['DNI '])
    df_a.rename(columns={'DNI ':'DOCUMENTO'}, inplace=True)

    #----------------B,C-----------------#
    dicc = {
        'NUMEROCONVENIO' : lista_vacia,
        'NUMEROOPERACION' : lista_vacia
    }
    df_bc = pd.DataFrame(dicc)

    #----------------D - COMPAÑÍA-----------------#
    lista = os.path.splitext(nArchivo_actual)
    valor = lista[0][11:14]

    lista = []
    for i in range(0, registros):
        lista.append(int(valor)) 
    df_d = pd.DataFrame({'COMPANIA' : lista})

    #----------------E - FECHAPAGO-----------------#
    # df_concat['FECHA'] = pd.to_datetime(df_concat['FECHA'], format="%d/%m/%Y", dayfirst=True)
    # df_concat['FECHA'] = df_concat['FECHA'].dt.strftime('%d/%m/%Y')

    df_e = pd.DataFrame(df_concat['FECHA'])
    df_e.rename(columns={'FECHA' : 'FECHAPAGO'}, inplace=True)

    #----------------F - IMPORTECONSOLIDADO-----------------#
    df_f = pd.DataFrame(df_concat['IMPORTE'])
    df_f.rename(columns={'IMPORTE' : 'IMPORTECONSOLIDADO'}, inplace=True)

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

    dicc = { 'NUMERORECIBO' : lista }
    df_l = pd.DataFrame(dicc)

    #--------------CONCATENAR COLUMNAS-------------#
    df_concat = pd.concat([df_a, df_bc, df_d, df_e, df_f, df_gk, df_l], axis=1)

    #--------------OBTENER EXCEL-------------#
    try:
        df_concat.to_excel('archivos/EmpresaLoanCargar/FertilLoanCargar.xlsx', index=False)
        print("Archivo 'FertilLoanCargar' creado correctamente")
    except:
        print("Error al crear el archivo 'FertilLoanCargar'")