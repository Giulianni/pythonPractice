import pandas as pd

def ExtraerCredNow(df):
    df_final = df[df['Nro Asociado'].str.contains('CRW', case=False, na=False)]

    df_final['Fecha de Pago'] = pd.to_datetime(df_final['Fecha de Pago'])
    df_final['Fecha de Pago'] = pd.to_datetime(df_final['Fecha de Pago'], format="%d/%m/%Y", dayfirst=True)
    df_final['Fecha de Pago'] = df_final['Fecha de Pago'].dt.strftime('%d/%m/%Y')

    try:
        df_final.to_excel('archivos/CPagosFiltrados/2-100-CPagosCRW.xlsx', index=False)
        print("Archivo '2-100-CPagosCRW.xlsx' creado correctamente")
    except:
        print("Error al crear archivo '2-100-CPagosCRW.xlsx'")