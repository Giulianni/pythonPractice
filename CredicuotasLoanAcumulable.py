import pandas as pd
import numpy as np
from datetime import datetime
import os

archivo2 = 'archivos/codigo_empresas.xlsx'
df2 = pd.read_excel(archivo2)

def CredicuotasLoanAcumulable(df, archivo):
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

    #----------------F - IMPORTECONSOLIDADO-----------------#
    df_f = pd.DataFrame(df_final['IMPORTECONSOLIDADO'])

    #----------------G - CLIENTE-----------------#
    df2['Código'] = df2['Código'].astype(str)
    lista = os.path.splitext(archivo) #67
    numero = str(lista[0][11:14])

    valor = df2[df2["Código"].str.contains(numero)]
    valor = valor['Descripción']
    valor = valor.iloc[0]

    lista = []
    for i in range(registros):
        lista.append(valor)

    dicc = {
        'CLIENTE' : lista
    }
    df_g = pd.DataFrame(dicc)

    #----------------H - CANTIDAD-----------------#
    lista = []
    for i in range(registros):
        lista.append(1)

    dicc = {
        'CANTIDAD' : lista
    }
    df_h = pd.DataFrame(dicc)

    #----------------I - BOCA DE PAGO-----------------#
    lista = os.path.splitext(archivo)
    if '1-' in lista[0][9:11]:
        lista = []
        for i in range(registros):
            lista.append('Boca Empresa')
        dicc = {
            'BOCA DE PAGO' : lista
        }
        df_i = pd.DataFrame(dicc)

    elif '2-' in lista[0][9:11]:
        lista = []
        for i in range(registros):
            lista.append('Central de Pagos')
        dicc = {
            'BOCA DE PAGO' : lista
        }
        df_i = pd.DataFrame(dicc)

    elif '3-' in lista[0][9:11]:
        lista = []
        for i in range(registros):
            lista.append('Transferencia')
        dicc = {
            'BOCA DE PAGO' : lista
        }
        df_i = pd.DataFrame(dicc)

    #----------------J - CÓDIGO ÚNICO-----------------#
    doc = list(df_final['DOCUMENTO']) 
    docu = []
    for i in doc:
        docu.append(int(i))

    fec = list(df_final['FECHAPAGO']) #fecha de pago
    fechas = []
    for i in fec:
        i = str(i)
        i = i.replace('/', '')
        fechas.append(int(i))

    imp = list(df_final['IMPORTECONSOLIDADO'].astype(int)) 

    lista = []
    for i in range(0, registros):
        concatenacion = f'{docu[i]}{fechas[i]}{imp[i]}'
        lista.append(concatenacion)

    df_j = pd.DataFrame({'CÓDIGO ÚNICO' : lista})

    #----------------K - FECHAPROCESO-----------------#
    lista = []
    for i in range(registros):
        lista.append(datetime.today().strftime('%d/%m/%Y'))

    dicc = {
        'FECHAPROCESO' : lista
    }
    df_k = pd.DataFrame(dicc)

    #--------------CONCATENAR COLUMNAS-------------#
    df_concat = pd.concat([df_a, df_bc, df_d, df_e, df_f, df_g, df_h, df_i, df_j, df_k], axis=1)

    #--------------OBTENER EXCEL-------------#
    try:
        if os.path.exists('archivos/LoanAcumulable/LoanAcumulable.xlsx'):
            a_concatenar = pd.read_excel('archivos/LoanAcumulable/LoanAcumulable.xlsx')
            df_concat = pd.concat([a_concatenar, df_concat])
            df_concat.to_excel('archivos/LoanAcumulable/LoanAcumulable.xlsx', index=False)
            print("Archivo 'LoanAcumulable' concatenado correctamente")
        else:
            df_concat.to_excel('archivos/LoanAcumulable/LoanAcumulable.xlsx', index=False)
            print("Archivo 'LoanAcumulable' creado correctamente")
    except:
        print("Error al crear el archivo 'LoanAcumulable'")
