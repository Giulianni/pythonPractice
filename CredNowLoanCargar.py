import pandas as pd
import numpy as np 
import os

def CredNowLoanCargarYComparar(cantidadArchivos, archivo_anterior, archivo_actual, archivo_obtenido_anterior, archivo_obtenido_actual, archivo_filtrado):
    
    #Defino parametros de la función--------------------------------------------------------------
    archivoLectura1 = archivo_anterior
    archivoLectura2 = archivo_actual
    escrituraArchivo1 = archivo_obtenido_anterior
    escrituraArchivo2 = archivo_obtenido_actual
    cantidadArchivos = cantidadArchivos
    #Realizo lectura de archivos ------------------------------------------------------------------
    df = pd.read_excel(archivoLectura1, skiprows=1)
    df2 = pd.read_excel(archivoLectura2, skiprows=1)

    #Borro filas vacias de DataFrame 1 y 2 --------------------------------------------------------
    if len(df.isnull().sum() >= 6): #Detecta última final c/ Total
        df.drop(df.tail(1).index,inplace=True)  
    
    if len(df2.isnull().sum() >= 6): #Detecta última final c/ Total
        df2.drop(df2.tail(1).index,inplace=True)
    
    #Dropeo valores nan en DataFrame(df 1 y 2)----------------------------------------------------
    df= df.dropna(how='all')
    df2= df2.dropna(how='all')
    
    #Validator de columnas -----------------------------------------------------------------------
    titulo = 'Validador de columnas'
    print('')
    print(titulo.center(len(titulo)+70, '-'))
    
    columnas_df = df.columns 
    columnas_df2 = df2.columns 
    
    columnas_validas_df = ['dni', 'Fecha de pago', 'Importe']
    columnas_validas_df2 = ['dni', 'Fecha de pago', 'Importe']
    
    for i in columnas_df:
        if i in  columnas_validas_df:
            columnas_validas_df.remove(i)
        if not columnas_validas_df:
            print('Columnas válidas del Dataframe anterior')
    else: 
            print(f'Columnas faltantes del Dataframe anterior: {columnas_validas_df}')
            
    for i in columnas_df2:
        if i in  columnas_validas_df2:
            columnas_validas_df2.remove(i)
        if not columnas_validas_df2:
            print('Columnas válidas del Dataframe anterior')
    else: 
            print(f'Columnas faltantes del Dataframe anterior: {columnas_validas_df2}')
            
    #df.columns #Para fijarme los nombres de las columnas 
    
    #Utils --------------------------------------------------------------------------------
    columnasVacias = []
    registros_df = df.shape[0]
    registros_df2 = df2.shape[0]
    
    # A - DOCUMENTO -----------------------------------------------------------------------
    df_a1 = pd.DataFrame(df['dni'].astype(int))
    df_a1.rename(columns={'dni' : 'DOCUMENTO'}, inplace=True)
    
    df_a2 = pd.DataFrame(df2['dni'].astype(int))
    df_a2.rename(columns={'dni' : 'DOCUMENTO'}, inplace=True)
    
    # df_a.head(10)
    
   # B,C Columnas vacias-------------------------------------------------------------------
    columnas_bc = {
    'NUMEROCONVENIO' : columnasVacias,
    'NUMEROOPERACION' : columnasVacias
    }
    df_bc = pd.DataFrame(columnas_bc)

    # D - COMPAÑÍA--------------------------------------------------------------------------
    codigoCompania_df = []
    codigoCompaniaArchivo1 = os.path.splitext(archivoLectura1)
    valorArchivo1 = codigoCompaniaArchivo1[0][11:14]
    print('------------------------- valor compania')
    print(valorArchivo1)
    for i in range(0, registros_df):
        codigoCompania_df.append(int(valorArchivo1)) 
    df_d1 = pd.DataFrame({'COMPANIA' : codigoCompania_df})

    codigoCompania_df2 = []
    codigoCompaniaArchivo2 = os.path.splitext(archivoLectura1)
    valorArchivo2 = codigoCompaniaArchivo2[0][11:14]
    print('------------------------- valor compania')
    print(valorArchivo2)
    for i in range(0, registros_df2):
        codigoCompania_df2.append(int(valorArchivo2)) 
    df_d2 = pd.DataFrame({'COMPANIA' : codigoCompania_df2})
    
    #----------------E - FECHAPAGO-------------------------------------------------
    df['Fecha de pago'] = pd.to_datetime(df['Fecha de pago'])
    df['Fecha de pago'] = pd.to_datetime(df['Fecha de pago'], format="%d/%m/%Y", dayfirst=True)
    df['Fecha de pago'] = df['Fecha de pago'].dt.strftime('%d/%m/%Y')

    df_e1 = pd.DataFrame(df['Fecha de pago'])
    df_e1.rename(columns={'Fecha de pago' : 'FECHAPAGO'}, inplace=True)

    df2['Fecha de pago'] = pd.to_datetime(df2['Fecha de pago'])
    df2['Fecha de pago'] = pd.to_datetime(df2['Fecha de pago'], format="%d/%m/%Y", dayfirst=True)
    df2['Fecha de pago'] = df2['Fecha de pago'].dt.strftime('%d/%m/%Y')

    df_e2 = pd.DataFrame(df2['Fecha de pago'])
    df_e2.rename(columns={'Fecha de pago' : 'FECHAPAGO'}, inplace=True)
    
    #----------------F - IMPORTECONSOLIDADO--------------------------------------
    df_f1 = pd.DataFrame(df['Importe'])
    df_f1.rename(columns={'Importe' : 'IMPORTECONSOLIDADO'}, inplace=True)
    
    df_f2 = pd.DataFrame(df2['Importe'])
    df_f2.rename(columns={'Importe' : 'IMPORTECONSOLIDADO'}, inplace=True)
    
    #G, H, I, J, K Columnas vacias----------------------------------------------------
    columnas_vacias_gk = {
        'IMPORTECAPITAL' : columnasVacias,
        'IMPORTEHONORARIOS' : columnasVacias,
        'IMPORTECOMISIONCANALPAGO' : columnasVacias,
        'OBSERVACION' : columnasVacias,
        'CANALPAGO' : columnasVacias
    }
    df_gk = pd.DataFrame(columnas_vacias_gk)

    #L - NUMERORECIBO---------------------------------------------------------------
    listaGuardarRecibos1 = []
    listaGuardarRecibos2 = []
    generadorRecibos1 = np.arange(len(df_a1)) 
    generadorRecibos2 = np.arange(len(df_a2)) 
    
    for i in generadorRecibos1:
        listaGuardarRecibos1.append(i+1)
    
    columnaRecibo1 = {
        'NUMERORECIBO' : listaGuardarRecibos1
    }
    df_l1 = pd.DataFrame(columnaRecibo1) 

    for i in generadorRecibos2:
        listaGuardarRecibos2.append(i+1)
    
    columnaRecibo2 = {
        'NUMERORECIBO' : listaGuardarRecibos2
    }
    df_l2 = pd.DataFrame(columnaRecibo2) 
    
    #CONCATENAR COLUMNAS----------------------------------------------------------------
    df_concat1 = pd.concat([df_a1, df_bc, df_d1, df_e1, df_f1, df_gk, df_l1], axis=1)
    df_concat2 = pd.concat([df_a2, df_bc, df_d2, df_e2, df_f2, df_gk, df_l2], axis=1)
    
    #Escribo ambos archivos ------------------------------------------------------------
    try:
        df_concat1.to_excel(escrituraArchivo1, index=False)
        print("Archivo 1 'CredNowLoanCargar' creado correctamente")
    except:
        print("Error al crear el archivo 1'CredNowLoanCargar'")
        
    try:
        df_concat2.to_excel(escrituraArchivo2, index=False)
        print("Archivo 2 'CredNowLoanCargar' creado correctamente")
    except:
        print("Error al crear el archivo 2'CredNowLoanCargar'")
        

    print('COMPARAR ARCHIVOS----------------------------------------------------------------')

    print('COMPARABLES ----------------------------------')    
    #Comparar Archivos y obtener uno nuevo con la información nueva ------------------
    lecturaComparable1=pd.read_excel(escrituraArchivo1)
    lecturaComparable2=pd.read_excel(escrituraArchivo2)


    print('LECTURA COOOOOMPARABLE --------------------------------')
    print(lecturaComparable1)
    print(lecturaComparable2)

    archivoComparado = pd.merge(lecturaComparable1, lecturaComparable2, how='outer', indicator='Exist')
    archivoComparado = archivoComparado.loc[archivoComparado['Exist'] != 'both']

    archivoComparado.drop('Exist', inplace=True, axis=1)

    #Borro los archivos 1 y 2 con el formato Loan
    os.remove(escrituraArchivo1)
    os.remove(escrituraArchivo2)
    

    #Escribis un tercer archivo solamente con la información nueva ---------------------------------------
    archivoComparado.to_excel(archivo_filtrado, index=False)

    
#CredNowLoanCargarYComparar('Archivos/1-100-CredNow_1102.xlsx', 'Archivos/1-100-CredNow_1502.xlsx', 'Generados/CredNowLoanCargar1.xlsx', 'Generados/CredNowLoanCargar2.xlsx', 'Generados/CredNowLoanFiltrado.xlsx')
#CredNowLoanCargarYComparar('Archivos/1-100-CredNow_1502.xlsx', 'Archivos/1-100-CredNow_2502.xlsx', 'Generados/CredNowLoanCargar3.xlsx', 'Generados/CredNowLoanCargar4.xlsx', 'Generados/CredNowLoanFiltrado2.xlsx')


def CredNowLoanCargar( cantidadArchivos, archivo_actual, archivo_obtenido_Formato_Loan):

    
    #Defino parametros de la función--------------------------------------------------------------
    archivoLectura1 = archivo_actual
    escrituraArchivo1 = archivo_obtenido_Formato_Loan
    cantidadArchivos = cantidadArchivos
    
    #Realizo lectura de archivos ------------------------------------------------------------------
    df = pd.read_excel(archivoLectura1, skiprows=1)

    #Borro filas vacias de DataFrame 1 y 2 --------------------------------------------------------
    if len(df.isnull().sum() >= 6): #Detecta última final c/ Total
        df.drop(df.tail(1).index,inplace=True)  
    
    #Dropeo valores nan en DataFrame(df 1 y 2)----------------------------------------------------
    df= df.dropna(how='all')
    
    #Validator de columnas -----------------------------------------------------------------------
    titulo = 'Validador de columnas'
    print('')
    print(titulo.center(len(titulo)+70, '-'))
    
    columnas_df = df.columns  
    
    columnas_validas_df = ['dni', 'Fecha de pago', 'Importe']
    
    for i in columnas_df:
        if i in  columnas_validas_df:
            columnas_validas_df.remove(i)
        if not columnas_validas_df:
            print('Columnas válidas del Dataframe anterior')
    else: 
            print(f'Columnas faltantes del Dataframe anterior: {columnas_validas_df}')
                    
    #df.columns #Para fijarme los nombres de las columnas 
    
    #Utils --------------------------------------------------------------------------------
    columnasVacias = []
    registros_df = df.shape[0]
    
    # A - DOCUMENTO -----------------------------------------------------------------------
    df_a = pd.DataFrame(df['dni'].astype(int))
    df_a.rename(columns={'dni' : 'DOCUMENTO'}, inplace=True)
    
    
    # df_a.head(10)
    
   # B,C Columnas vacias-------------------------------------------------------------------
    columnas_bc = {
    'NUMEROCONVENIO' : columnasVacias,
    'NUMEROOPERACION' : columnasVacias
    }
    df_bc = pd.DataFrame(columnas_bc)

    # D - COMPAÑÍA--------------------------------------------------------------------------
    codigoCompania_df = []
    codigoCompaniaArchivo1 = os.path.splitext(archivoLectura1)
    valorArchivo1 = codigoCompaniaArchivo1[0][11:14]
    print('------------------------- valor compania')
    print(valorArchivo1)
    for i in range(0, registros_df):
        codigoCompania_df.append(int(valorArchivo1)) 
    df_d = pd.DataFrame({'COMPANIA' : codigoCompania_df})
    
    #----------------E - FECHAPAGO-------------------------------------------------
    df['Fecha de pago'] = pd.to_datetime(df['Fecha de pago'])
    df['Fecha de pago'] = pd.to_datetime(df['Fecha de pago'], format="%d/%m/%Y", dayfirst=True)
    df['Fecha de pago'] = df['Fecha de pago'].dt.strftime('%d/%m/%Y')

    df_e = pd.DataFrame(df['Fecha de pago'])
    df_e.rename(columns={'Fecha de pago' : 'FECHAPAGO'}, inplace=True)
    
    #----------------F - IMPORTECONSOLIDADO--------------------------------------
    df_f = pd.DataFrame(df['Importe'])
    df_f.rename(columns={'Importe' : 'IMPORTECONSOLIDADO'}, inplace=True)
    
    #G, H, I, J, K Columnas vacias----------------------------------------------------
    columnas_vacias_gk = {
        'IMPORTECAPITAL' : columnasVacias,
        'IMPORTEHONORARIOS' : columnasVacias,
        'IMPORTECOMISIONCANALPAGO' : columnasVacias,
        'OBSERVACION' : columnasVacias,
        'CANALPAGO' : columnasVacias
    }
    df_gk = pd.DataFrame(columnas_vacias_gk)

    #L - NUMERORECIBO---------------------------------------------------------------
    listaGuardarRecibos = []
    generadorRecibos = np.arange(len(df_a)) 
 
    for i in generadorRecibos:
        listaGuardarRecibos.append(i+1)
    
    columnaRecibo = {
        'NUMERORECIBO' : listaGuardarRecibos
    }
    df_l = pd.DataFrame(columnaRecibo) 

    #CONCATENAR COLUMNAS----------------------------------------------------------------
    df_concat1 = pd.concat([df_a, df_bc, df_d, df_e, df_f, df_gk, df_l], axis=1)
    
    #Escribo ambos archivos ------------------------------------------------------------
    try:
        df_concat1.to_excel(escrituraArchivo1, index=False)
        print("Archivo 1 'CredNowLoanCargar' creado correctamente")
    except:
        print("Error al crear el archivo 1'CredNowLoanCargar'")


#CredNowLoanCargar('Archivos/1-100-CredNow_1102.xlsx', 'Generados/CredNowLoanCargar1.xlsx')
        