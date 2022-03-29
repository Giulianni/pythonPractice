import pandas as pd

#Crudo CP archivo:
def ExtraerMCR(df):
    #-------------Validador--------------#
    titulo = 'Validador de columnas'
    print('')
    print(titulo.center(len(titulo)+70, '-'))

    columnas = df.columns

    columnas_validas = ['Nro Asociado', 'Fecha de Pago']

    for i in columnas:
        if i in columnas_validas:
            columnas_validas.remove(i)

    if not columnas_validas:
        print('Columnas válidas del archivo proveniente de Central de Pagos\n')
    else: 
        print(f'Columnas faltantes: {columnas_validas}\n')

    col1 = df['Nro Asociado']

    contador = 0
    lista = []
    for nombre, contenido in col1.items():
        contenido = str(contenido)
        if 'MCR' in contenido:
            lista.append(contenido)
            contador += 1

    df_final = df[df['Nro Asociado'].str.contains('MCR', case=False, na=False)]

    df_final['Fecha de Pago'] = pd.to_datetime(df_final['Fecha de Pago'])
    df_final['Fecha de Pago'] = pd.to_datetime(df_final['Fecha de Pago'], format="%d/%m/%Y", dayfirst=True)
    df_final['Fecha de Pago'] = df_final['Fecha de Pago'].dt.strftime('%d/%m/%Y')

    try:
        df_final = df_final.to_excel('archivos/CPagosFiltrados/2-067-CPagosMCR.xlsx', index=False)
        print("Archivo '2-067-CPagosMCR.xlsx' creado correctamente")
    except:
        print("Error al crear archivo '2-067-CPagosMCR.xlsx'")