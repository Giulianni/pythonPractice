import pandas as pd
import numpy as np
from datetime import datetime
import os

archivo2 = 'archivos/codigo_empresas.xlsx'
df2 = pd.read_excel(archivo2)

def EdenorLoanAcumulable(df_actual, archivo_actual):
    dia = archivo_actual[21:23]
    mes = archivo_actual[24:26]
    año = archivo_actual[27:31]

    fecha = f'{año}-{mes}-{dia}'
    mask = (df_actual['FEC_REGISTRO'] >= fecha)
    df_actual = df_actual.loc[mask]
    
    df_actual = df_actual.reset_index(drop=True)

    #----------------UTILIDADES-----------------#
    registros = df_actual.shape[0]
    lista_vacia = [] #Utilizada para varias columnas que deben estar vacías
    for i in range (0, registros):
        lista_vacia.append(np.nan)

    #----------------A - DOCUMENTO-----------------#
    df_a = pd.DataFrame(df_actual['ID_CUENTA'])
    df_a.rename(columns={'ID_CUENTA' : 'DOCUMENTO'}, inplace=True)

    #----------------B,-----------------#
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
    #----------------G - CLIENTE-----------------#
    df2['Código'] = df2['Código'].astype(str)
    lista = os.path.splitext(archivo_actual) #52
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
        'CANTIDAD' : lista
    }
    df_h = pd.DataFrame(dicc)

    #----------------I - BOCA DE PAGO-----------------#
    lista = os.path.splitext(archivo_actual)
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
    doc = list(df_actual['ID_CUENTA']) 
    docu = []
    for i in doc:
        docu.append(int(i))

    fec = list(df_actual['FEC_PAGO']) #fecha de pago
    fechas = []
    for i in fec:
        i = str(i)

        año = i[:4]
        mes = i[5:7]
        dia = i[8:10]
        i = f'{dia}/{mes}/{año}'

        i = i.replace('/', '')
        fechas.append(int(i))

    monto = []
    imp = list(df_actual['MONTO'])
    for i in imp: 
        i = i.replace(',', '.')
        i = float(i)
        monto.append(int(i))

    lista = []
    for i in range(0, registros):
        concatenacion = f'{docu[i]}{fechas[i]}{monto[i]}'
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