import pandas as pd
import numpy as np
from datetime import datetime
import os

archivo2 = 'archivos/codigo_empresas.xlsx'
df2 = pd.read_excel(archivo2)

def FertilLoanAcumulable(df_anterior, df_actual, nArchivo_actual):
    
    df_concat = pd.concat([df_anterior, df_actual])
    df_concat = df_concat.drop_duplicates(keep=False) #Elimino los valores duplicados
    df_concat.drop(['Unnamed: 7'], axis=1, inplace=True)

    df_concat = df_concat.reset_index(drop=True)

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
    # df['Fecha_Pago'] = pd.to_datetime(df['Fecha_Pago'])
    # df['Fecha_Pago'] = pd.to_datetime(df['Fecha_Pago'], format="%d/%m/%Y", dayfirst=True)
    # df['Fecha_Pago'] = df['Fecha_Pago'].dt.strftime('%d/%m/%Y')

    df_e = pd.DataFrame(df_concat['FECHA'])
    df_e.rename(columns={'FECHA' : 'FECHAPAGO'}, inplace=True)

    #----------------F - IMPORTECONSOLIDADO-----------------#
    df_f = pd.DataFrame(df_concat['IMPORTE'])
    df_f.rename(columns={'IMPORTE' : 'IMPORTECONSOLIDADO'}, inplace=True)

    #----------------G - CLIENTE-----------------#
    df2['Código'] = df2['Código'].astype(str)
    lista = os.path.splitext(nArchivo_actual) #Valor de 2 cifras o 3
    numero = str(lista[0][12:14])

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
        'CANTIDAD': lista
    }
    df_h = pd.DataFrame(dicc)

    #----------------I - BOCA DE PAGO-----------------#
    lista = os.path.splitext(nArchivo_actual)
    if '1-' in lista[0][9:11]:
        lista = []
        for i in range(registros):
            lista.append('Boca Empresa')
        dicc = {
            'BOCA DE PAGO': lista
        }
        df_i = pd.DataFrame(dicc)

    elif '2-' in lista[0][9:11]:
        lista = []
        for i in range(registros):
            lista.append('Central de Pagos')
        dicc = {
            'BOCA DE PAGO': lista
        }
        df_i = pd.DataFrame(dicc)

    elif '3-' in lista[0][9:11]:
        lista = []
        for i in range(registros):
            lista.append('Transferencia')
        dicc = {
            'BOCA DE PAGO': lista
        }
        df_i = pd.DataFrame(dicc)

    #----------------J - CÓDIGO ÚNICO-----------------#
    doc = list(df_concat['DNI ']) 
    docu = []
    for i in doc:
        i = str(i)
        p1 = i[2:-1]
        docu.append(int(p1))
        
    fec = list(df_concat['FECHA']) #fecha de pago
    fechas = []
    for i in fec:
        i = i.replace('/', '')
        fechas.append(int(i))

    imp = list(df_concat['IMPORTE'].astype(int)) 

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
        'FECHAPROCESO': lista
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