import pandas as pd
pd.options.mode.chained_assignment = None
#Funciones de Empresa
#---------------MCR---------------#
from MejorCreditoRecovery.MCRLoanCargar import MCRLoanCargar
from MejorCreditoRecovery.MCRLoanAcumulable import MCRLoanAcumulable
from MejorCreditoRecovery.ExtraerMCR import ExtraerMCR

#---------------Credicuotas---------------#
from Credicuotas.CredicuotasLoanCargar import CredicuotasLoanCargar
from Credicuotas.CredicuotasLoanAcumulable import CredicuotasLoanAcumulable

#---------------Cordial---------------#
from Cordial.CordialLoanCargar import CordialLoanCargar
from Cordial.CordialLoanAcumulable import CordialLoanAcumulable
from Cordial.ExtraerCordial import ExtraerCordial

#---------------Qida---------------#
from Qida.QidaLoanCargar import QidaLoanCargar #Necesita el anterior
from Qida.QidaLoanAcumulable import QidaLoanAcumulable
from Qida.ExtraerQida import ExtraerQida

#---------------CredNow---------------#
from CredNow.CredNowLoanCargar import CredNowLoanCargar #Necesita el anterior
from CredNow.CredNowLoanAcumulable import CredNowLoanAcumulable
from CredNow.ExtraerCredNow import ExtraerCredNow

#---------------Fertil---------------#
from Fertil.FertilLoanCargar import FertilLoanCargar
from Fertil.FertilLoanAcumulable import FertilLoanAcumulable

#---------------Edelap---------------#
from Edelap.EdelapLoanCargar import EdelapLoanCargar
from Edelap.EdelapLoanAcumulable import EdelapLoanAcumulable

#---------------Edemsa---------------#
from Edemsa.EdemsaLoanCargar import EdemsaLoanCargar
from Edemsa.EdemsaLoanAcumulable import EdemsaLoanAcumulable

#---------------Edenor---------------#
from Edenor.EdenorLoanCargar import EdenorLoanCargar
from Edenor.EdenorLoanAcumulable import EdenorLoanAcumulable

#---------------Edesur---------------#
# from Edesur.EdesurLoanCargar import EdesurLoanCargar

import os 

#--------------LECTURA DE ARCHIVO-------------#
#(Edenor y Edesur archivo .txt)
#Edesur compara 2 archivos
# archivo_actual = 'archivos/1-052-Edenor21_02_2022.txt'
# df_actual = pd.read_csv(archivo_actual, sep='\t')
# df_anterior = ''

#---------------------------------------------#
archivo_actual = 'archivos/1-095-Edemsa_2502.xlsx'
df_actual = pd.read_excel(archivo_actual)
df_anterior = ''
lista = os.path.splitext(archivo_actual)

#---------------------------------------------#
#2 archivos: QIDA, CREDNOW, FERTIL
# archivo_anterior = 'archivos/1-049-Fertil_1102.xlsx'
# archivo_actual = 'archivos/1-049-Fertil_2102.xlsx'

# df_anterior = pd.read_excel(archivo_anterior)
# df_actual = pd.read_excel(archivo_actual)

lista = os.path.splitext(archivo_actual)
#---------------------------------------------#
if '1-' in lista[0][9:11]:
    print('-----------------------------------------------------------------')
    # if '045-' in lista[0][11:15]:
    #     EdesurLoanCargar(df_anterior, df_actual, archivo_actual)
        
    if '049-' in lista[0][11:15]:
        FertilLoanCargar(df_anterior, df_actual, archivo_actual)
        FertilLoanAcumulable(df_anterior, df_actual, archivo_actual)

    elif '052-' in lista[0][11:15]:
        EdenorLoanCargar(df_actual,archivo_actual)
        EdenorLoanAcumulable(df_actual, archivo_actual)

    elif '060-' in lista[0][11:15]:
        QidaLoanCargar(df_anterior, df_actual, archivo_actual)
        #QidaLoanAcumulable(df_anterior, df_actual, archivo_actual)

    elif '063-' in lista[0][11:15]:
        CordialLoanCargar(df_actual,archivo_actual)
        CordialLoanAcumulable(df_actual, archivo_actual)

    elif '067-' in lista[0][11:15]:
        MCRLoanCargar(df_actual, archivo_actual)
        MCRLoanAcumulable(df_actual, archivo_actual)

    elif '094-' in lista[0][11:15]:
        EdelapLoanCargar(df_actual, archivo_actual)
        EdelapLoanAcumulable(df_actual, archivo_actual)

    elif '095-' in lista[0][11:15]:
        EdemsaLoanCargar(df_actual, archivo_actual)
        EdemsaLoanAcumulable(df_actual, archivo_actual)

    elif '100-' in lista[0][11:15]:
        CredNowLoanCargar(df_anterior, df_actual, archivo_actual)
        #CredNowLoanAcumulable(df_anterior, df_actual, archivo_actual)

    elif '103-' in lista[0][11:15]:
        CredicuotasLoanCargar(df_actual,archivo_actual)
        CredicuotasLoanAcumulable(df_actual, archivo_actual)

    else:
        print('El archivo no contiene un código de empresa')
    print('-----------------------------------------------------------------')

elif '2-' in lista[0][9:11]:
    print('-----------------------------------------------------------------')
    if '060-' in lista[0][11:15]:
        ExtraerQida(df_actual)
        if os.path.exists('archivos/CPagosFiltrados/2-060-CPagosQID.xlsx'):
            from Qida.QidaCPLoanCargar import QidaCPLoanCargar
            from Qida.QidaCPLoanAcumulable import QidaCPLoanAcumulable
            from Qida.QidaMacro import QidaMacro
            QidaCPLoanCargar()
            QidaCPLoanAcumulable(archivo_actual)
            QidaMacro(archivo_actual)
    
    elif '063-' in lista[0][11:15]:
        ExtraerCordial(df_actual)
        if os.path.exists('archivos/CPagosFiltrados/2-063-CPagosCOR.xlsx'):
            from Cordial.CordialCPLoanCargar import CordialCPLoanCargar
            from Cordial.CordialCPLoanAcumulable import CordialCPLoanAcumulable
            from Cordial.CordialMacro import CordialMacro
            CordialCPLoanCargar()
            CordialCPLoanAcumulable(archivo_actual)
            CordialMacro(archivo_actual)

    elif '067-' in lista[0][11:15]:
        ExtraerMCR(df_actual)
        if os.path.exists('archivos/CPagosFiltrados/2-067-CPagosMCR.xlsx'):
            from MejorCreditoRecovery.CPagosLoanCargar import CPagosLoanCargar
            from MejorCreditoRecovery.CPagosLoanAcumulable import CPagosLoanAcumulable
            from MejorCreditoRecovery.CPagosMacro import CPagosMacro
            CPagosLoanCargar()
            CPagosLoanAcumulable(archivo_actual)
            CPagosMacro(archivo_actual)

    elif '100-' in lista[0][11:15]:
        ExtraerCredNow(df_actual)
        if os.path.exists('archivos/CPagosFiltrados/2-100-CPagosCRW.xlsx'):
            from CredNow.CredNowCPLoanCargar import CredNowCPLoanCargar
            from CredNow.CredNowCPLoanAcumulable import CredNowCPLoanAcumulable
            from CredNow.CredNowMacro import CredNowMacro
            CredNowCPLoanCargar()
            CredNowCPLoanAcumulable(archivo_actual)
            CredNowMacro(archivo_actual)

    else:
        print('El archivo no contiene un código de empresa')
    print('-----------------------------------------------------------------')
