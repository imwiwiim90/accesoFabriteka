import openpyxl
import pandas
import os
from datetime import datetime
import time

def imprimirExcel():
    us=pandas.read_excel('.PinUsuarios.xlsx')
    print(us)
def movimientos_mes(año, mes):
    file_name1='.RegistroTarjeta.xlsx'
    file_name2='.usuarios.xlsx'
    files=os.listdir('./')
    a=0
    if file_name1 in files and file_name2 in files:
        rt=pandas.read_excel(file_name1)
        us=pandas.read_excel(file_name2)
        if len(rt)==0:
            return None
        else:
            fecha=año + '-' + mes
            usr=us.index.values.tolist()
            rtf=rt.index.values.tolist()
            ob=[]
            for u in usr:
                a=0
                b=0
                for f in rtf:
                    cc=int(rt.iloc[a][0])
                    fe=str(rt.iloc[a][1])
                    es=str(rt.iloc[a][3])
                    if u==cc and fecha in fe and 'Entrada' in es :
                        b=b+1
                    a=a+1
                if b > 0:
                    uss=us.loc[u]
                    nombre=uss[0]
                    telefono=uss[1]
                    correo=uss[2]
                    cliente={
                        'cedula':u,
                        'nombre':nombre,
                        'telefono':telefono,
                        'correo': correo,
                        'entradas':b
                    }
                    ob.append(cliente)
            return ob

def exportarDatos():
    filename1 = '.usuarios.xlsx'
    filename2 = '.RegistroTarjeta.xlsx'
    filename_export = 'ExportarDatosClientes.xlsx'
    fecha_ant = ' '
    us=pandas.read_excel(filename1)
    writer = pandas.ExcelWriter(filename_export, engine=None)
    us.to_excel(writer, sheet_name='Información de Usuarios')

    rg=pandas.read_excel(filename2)
    rg_f=rg.set_index('Fecha')
    rg_f=rg_f.index.values.tolist()

    for f in rg_f:
        fecha=datetime.strptime(f,"%Y-%m-%d")
        fecha_mes=fecha.strftime("%Y-%m")
        año=fecha.strftime("%Y")
        mes=fecha.strftime("%m")
        año_mes=fecha.strftime("%Y-%B")
        if fecha_ant not in f:
            mm=movimientos_mes(año, mes)
            m1=mm[0]
            rr = pandas.DataFrame({m1['cedula']: [m1['nombre'],m1['telefono'],m1['correo'],m1['entradas']]})
            try:
                mm=mm[1:]
                for m in mm:
                    rr[m['cedula']] = [m['nombre'],m['telefono'],m['correo'],m['entradas']]
            except:
                pass
            rr=rr.T
            rr.columns=['Nombre', 'Telefono', 'Correo', 'Entradas']
            rr.to_excel(writer, sheet_name=año_mes)
        fecha_ant=fecha_mes
    writer.save()





exportarDatos()
