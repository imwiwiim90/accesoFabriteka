import openpyxl
import pandas
import os
from datetime import datetime
import time
file_name1='RegistroTarjeta.xlsx'
file_name2='usuarios.xlsx'
files=os.listdir('./')
def entradas_mensuales(cedula, año, mes):
    a=0
    b=0
    if file_name in files:
        rt=pandas.read_excel(file_name)
        if len(rt)==0:
            return None
        else:

            rtc1=rt.set_index('Cedula')
            rtc=rtc1.index
            rtc2=rtc1.keys
            cedula=rtc1.loc[cedula]
            ced=cedula.index.values
            print(cedula)
            fecha=año + '-' + mes
            for f in ced:
                if fecha in cedula.iloc[a][0] and 'Entrada' in cedula.iloc[a][2]:
                    b=b+1
                a=a+1
            print('entradas este mes = '+str(b))

def movimientos_mes(año, mes):
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
                print(b)
                if b > 0:
                    uss=us.loc[u]
                    nombre=uss[0]
                    telefono=uss[1]
                    cliente={
                        'cedula':u,
                        'nombre':nombre,
                        'telefono':telefono,
                        'entradas':b
                    }
                    ob.append(cliente)
            return ob

def movimientos_dia(año, mes, dia):
    a=0
    if file_name1 in files and file_name2 in files:
        rt=pandas.read_excel(file_name1)
        us=pandas.read_excel(file_name2)
        if len(rt)==0:
            return None
        else:
            try:
                fecha=año + '-' + mes + '-' + dia
                usr=us.index.values.tolist()
                rt1=rt.set_index('Fecha')
                rtf=rt1.loc[fecha]
                rti=rt1.index.values.tolist()
                ob=[]
                for u in usr:
                    a=0
                    b=0
                    for f in rti:
                        cc=int(rt.iloc[a][0])
                        fe=str(rt.iloc[a][1])
                        es=str(rt.iloc[a][3])
                        if u==cc and fecha in fe and 'Entrada' in es :
                            uss=us.loc[u]
                            nombre=uss[0]
                            telefono=uss[1]
                            cliente={
                                'cedula':u,
                                'nombre':nombre,
                                'telefono':telefono,
                            }
                            ob.append(cliente)
                        a=a+1
                return ob
            except:
                return None

def duracion(cedula):
    a=0
    b=0
    if file_name in files:
        rt=pandas.read_excel(file_name)
        if len(rt)==0:
            return None
        else:
            rtc1=rt.set_index('Cedula')
            cedula=rtc1.loc[cedula]
            ced=cedula.index.values
            l=len(ced)
            fecha_mes='2018-08'
            if 'Salida' in cedula.iloc[-1][2]:
                entrada=cedula.iloc[-1][0]+' '+cedula.iloc[-1][1]
                salida=cedula.iloc[-1][0]+' '+cedula.iloc[-2][1]
                fentrada=datetime.strptime(entrada,"%Y-%m-%d %H:%M")
                fsalida=datetime.strptime(salida,"%Y-%m-%d %H:%M")
                delta=fentrada-fsalida
                print(delta)
            else:
                print('El usuario no ha salido')

def cambiarEmpleado(cedula, pin):
    em=pandas.read_excel('empleados.xlsx')
    em1=em.set_index('Cedula')
    em1=em1.index.values.tolist()
    ind=em1.index(cedula)
    pin_b=em.index.values[ind]
    nombre=em.iloc[ind][0]
    telefono=em.iloc[ind][1]
    em=em.drop(pin_b)
    em=em.T
    em[pin]=[nombre, telefono, cedula]
    em=em.T
    writer = pandas.ExcelWriter('empleados.xlsx', engine=None)
    em.to_excel(writer, sheet_name='Sheet1')
    writer.save()

# verifica si el pin no existe tanto en empleados como en clientes, retorna True si existe, False si no
def verificarPin(pin):

    files=os.listdir('./')

    if 'PinUsuarios.xlsx' in files:
        df=pandas.read_excel('PinUsuarios.xlsx')

        try:
            fe=df.loc[pin]
            return True
        except KeyError:
            pass


    if 'empleados.xlsx' in files:
        em=pandas.read_excel('empleados.xlsx')

        try:
            em=em.loc[pin]
            return True
        except KeyError:
            return False

    else:
        return False

#retorna 1 si tiene un pin asignado, 2 si la cedula ya existe en el sistema y 3 si es una cedula nueva
def verificarCedulaCliente(cedula):

        files=os.listdir('./')
        cedula=int(cedula)

        if 'PinUsuarios.xlsx' in files:
            us=pandas.read_excel('PinUsuarios.xlsx')
            us2=us.set_index('Cedula')

            try:
                us2.loc[cedula]
                return 1
            except KeyError:
                pass

        if 'usuarios.xlsx' in files:
            df=pandas.read_excel('usuarios.xlsx')

            try:
                pn=df.loc[cedula]
                return 2
            except KeyError:
                return 3

        else:
            return 3

#Se Borra Pin con su respectivo registro y retorna True, si n oexiste el pin retorna False
def borrarPinCliente(pin):
    files=os.listdir('./')
    pin=str(pin)

    if 'PinUsuarios.xlsx' in files:
        try:
            df=pandas.read_excel('PinUsuarios.xlsx')
            fe=df.loc[pin]
            cedula=fe[0]
            df1=df.drop(pin)
            writer = pandas.ExcelWriter('PinUsuarios.xlsx', engine=None)
            df1.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            fecha=datetime.now()
            hora=fecha.strftime("%H:%M")
            fecha=fecha.strftime("%Y-%m-%d")
            rg=pandas.read_excel('RegistroTarjeta.xlsx')
            rg_t=rg.T
            col=rg_t.columns
            l=len(col)
            rg_t[l]=[cedula, fecha, hora, 'Salida']
            rg=rg_t.T
            writer = pandas.ExcelWriter('RegistroTarjeta.xlsx', engine=None)
            rg.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            return True
        except KeyError:
            return False
    else:
        return False

#Retorna lista con datos de el dueño del pin[cliente/empleado,nombre,telefono,correo,cedula], si no existe retorna None
def verificarPinAsignado(pin):

    a=0
    files=os.listdir('./')
    pin=str(pin)

    if 'PinUsuarios.xlsx' in files:
        df=pandas.read_excel('PinUsuarios.xlsx')

        try:
            fe=df.loc[pin]
            cedula=fe[0]
            reg=pandas.read_excel('usuarios.xlsx')
            us=reg.loc[cedula]
            a=1
            datos=['cliente',us[0], us[1], us[2], cedula]
            return datos
        except KeyError:
            pass

    if a==0 :

        if 'empleados.xlsx' in files:
            em=pandas.read_excel('empleados.xlsx')
            try:
                em=em.loc[pin]
                datos=['empleado',em[0], em[1], em[2], em[3]]
                return datos
            except KeyError:
                pass

        else:
            return None
#Se agrega nuevo PinUsuarios y su resectivo registro de tarjeta,retorna True si guardo, False si no se pudo
def nuevoPinCliente(pin, cedula):

    files=os.listdir('./')
    pin=str(pin)
    cedula=int(cedula)
    if 'PinUsuarios.xlsx' in files: #Se agrega el nuevo usuario
        df=pandas.read_excel('PinUsuarios.xlsx')
        df_t=df.T
        fecha=datetime.now()
        hora=fecha.strftime("%H:%M")
        fecha=fecha.strftime("%Y-%m-%d")
        df_t[pin]=[cedula]
        df=df_t.T
        writer = pandas.ExcelWriter('PinUsuarios.xlsx', engine=None)
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        rg=pandas.read_excel('RegistroTarjeta.xlsx')
        rg_t=rg.T
        col=rg_t.columns
        l=len(col)
        rg_t[l]=[cedula, fecha, hora, 'Entrada']
        rg=rg_t.T
        writer = pandas.ExcelWriter('RegistroTarjeta.xlsx', engine=None)
        rg.to_excel(writer, sheet_name='Sheet1')
        writer.save()


    else:#Se crea nuevo documento de usuarios y se guarda usuario actual
        fecha=datetime.now()
        fecha=fecha.strftime("%Y-%m-%d-%H-%M-%f")
        df = pandas.DataFrame({pin: [cedula]})
        df=df.T
        df.columns=['Cedula']
        writer = pandas.ExcelWriter('PinUsuarios.xlsx', engine=None)
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        fecha=datetime.now()
        hora=fecha.strftime("%H:%M")
        fecha=fecha.strftime("%Y-%m-%d")
        rg = pandas.DataFrame({0:[cedula,fecha,hora,'Entrada']})
        rg=rg.T
        rg.columns=['Cedula', 'Fecha', 'Hora', 'Entrada/salida']
        writer = pandas.ExcelWriter('RegistroTarjeta.xlsx', engine=None)
        rg.to_excel(writer, sheet_name='Sheet1')
        writer.save()

#En caso de que la persona no este en usuarios aqui se haria el registro
def ingresarNuevoCliente(cedula, nombre , telefono, correo):
    files = os.listdir('./')

    if 'usuarios.xlsx' in files and 'PinUsuarios.xlsx' in files:
        us=pandas.read_excel('usuarios.xlsx')
        us_t=us.T
        us_t[cedula]=[nombre,telefono,correo]
        us=us_t.T
        writer = pandas.ExcelWriter('usuarios.xlsx', engine=None)
        us.to_excel(writer, sheet_name='Sheet1')
        writer.save()

    else:
        us = pandas.DataFrame({cedula: [nombre,telefono,correo]})
        us=us.T
        us.columns=['Nombre', 'Telefono','Correo']
        writer = pandas.ExcelWriter('usuarios.xlsx', engine=None)
        us.to_excel(writer, sheet_name='Sheet1')
        writer.save()

#Guarda En usuarios y en registro tarjeta si la cedula ya existe en usuarios
def ingresarClienteExistente(cedula):
    files=os.listdir('./')
    cedula=int(cedula)
    df=pandas.read_excel('usuarios.xlsx')
    us_t=df.T
    pn=df.loc[cedula]
    usuario=df.loc[cedula]
    us_t[cedula]=[usuario[0],usuario[1]]
    us=us_t.T
    writer = pandas.ExcelWriter('usuarios.xlsx', engine=None)
    us.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    fecha=datetime.now()
    hora=fecha.strftime("%H:%M")
    fecha=fecha.strftime("%Y-%m-%d")

#Retorna True si ya existe un empeado com esa cedula, Retorna False si es un cedula nueva
def verificarCedulaEmpleado(cedula):

        files=os.listdir('./')
        cedula=int(cedula)

        if 'empleados.xlsx' in files:
            us=pandas.read_excel('empleados.xlsx')
            us2=us.set_index('Cedula')

            try:
                us2.loc[cedula]
                return True
            except KeyError:
                return False

        else:
            return False

#ingresa un nuevo empleado
def ingresarEmpleado(pin, cedula, nombre, telefono, correo):
    files = os.listdir('./')
    pin=str(pin)
    cedula=int(cedula)

    if 'empleados.xlsx' in files:
        em=pandas.read_excel('empleados.xlsx')
        em_t=em.T
        em_t[pin]=[nombre,telefono,correo,cedula]
        em=em_t.T
        writer = pandas.ExcelWriter('empleados.xlsx', engine=None)
        em.to_excel(writer, sheet_name='Sheet1')
        writer.save()
    else:
        em = pandas.DataFrame({pin: [nombre, telefono, correo, cedula]})
        em=em.T
        em.columns=['Nombre','Telefono','Correo', 'Cedula']
        writer = pandas.ExcelWriter('empleados.xlsx', engine=None)
        em.to_excel(writer, sheet_name='Sheet1')
        writer.save()

#si Borra el empleado retorna True, si no existe retorna False
def borrarEmpleado(pin):
    files=os.listdir('./')
    pin=str(pin)

    if 'empleados.xlsx' in files:
        try:
            df=pandas.read_excel('empleados.xlsx')
            fe=df.loc[pin]
            df1=df.drop(pin)
            writer = pandas.ExcelWriter('empleados.xlsx', engine=None)
            df1.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            return True
        except KeyError:
            return False
    else:
        return False

#Cambia el pi nde un cliente en caso de perdida, recordar hacer verificacion de cedula y pin
def cambiarCliente(cedula, pin):
    cedula=int(cedula)
    df=pandas.read_excel('PinUsuarios.xlsx')
    ced=df.set_index('Cedula')
    c=ced.loc[cedula]
    dt=ced.T
    cee=dt.columns.tolist()
    ind=cee.index(cedula)
    br=df.index
    pin_b=br[ind]
    dff=df.drop(pin_b)
    df_t=dff.T
    df_t[pin]=[cedula]
    df=df_t.T
    writer = pandas.ExcelWriter('PinUsuarios.xlsx', engine=None)
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()

#Cambia el pin de un empleado en caso de perdida, recordar hacer verificacion de cedula y pin
def cambiarEmpleado(cedula, pin):
    em=pandas.read_excel('empleados.xlsx')
    em1=em.set_index('Cedula')
    em1=em1.index.values.tolist()
    ind=em1.index(cedula)
    pin_b=em.index.values[ind]
    nombre=em.iloc[ind][0]
    telefono=em.iloc[ind][1]
    correo=em.iloc[ind][2]
    em=em.drop(pin_b)
    em=em.T
    em[pin]=[nombre, telefono, correo, cedula]
    em=em.T
    writer = pandas.ExcelWriter('empleados.xlsx', engine=None)
    em.to_excel(writer, sheet_name='Sheet1')
    writer.save()

#Retorna numero de veces al mes de un usuario en especifico
def entradas_mensuales(cedula, año, mes):
    a=0
    b=0
    if file_name in files:
        rt=pandas.read_excel(file_name)
        if len(rt)==0:
            return None
        else:

            rtc1=rt.set_index('Cedula')
            rtc=rtc1.index
            rtc2=rtc1.keys
            cedula=rtc1.loc[cedula]
            ced=cedula.index.values
            print(cedula)
            fecha=año + '-' + mes
            for f in ced:
                if fecha in cedula.iloc[a][0] and 'Entrada' in cedula.iloc[a][2]:
                    b=b+1
                a=a+1
            print('entradas este mes = '+str(b))

#Restorna lista de diccionario que contiene los usuarios que ingresaron en el mes dado con la siguiente
#estructura : {cedula, nombre , telefono , correo, veces este mes}
def movimientos_mes(año, mes):
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
                print(b)
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

#Restorna lista de diccionario que contiene los usuarios que ingresaron en el dia dado con la siguiente
#estructura : {cedula, nombre , telefono , correo}
def movimientos_dia(año, mes, dia):
    a=0
    if file_name1 in files and file_name2 in files:
        rt=pandas.read_excel(file_name1)
        us=pandas.read_excel(file_name2)
        if len(rt)==0:
            return None
        else:
            try:
                fecha=año + '-' + mes + '-' + dia
                usr=us.index.values.tolist()
                rt1=rt.set_index('Fecha')
                rtf=rt1.loc[fecha]
                rti=rt1.index.values.tolist()
                ob=[]
                for u in usr:
                    a=0
                    b=0
                    for f in rti:
                        cc=int(rt.iloc[a][0])
                        fe=str(rt.iloc[a][1])
                        es=str(rt.iloc[a][3])
                        if u==cc and fecha in fe and 'Entrada' in es :
                            uss=us.loc[u]
                            nombre=uss[0]
                            telefono=uss[1]
                            correo=uss[2]
                            cliente={
                                'cedula':u,
                                'nombre':nombre,
                                'telefono':telefono,
                                'correo':correo,
                            }
                            ob.append(cliente)
                        a=a+1
                return ob
            except:
                return None

#Retorna Duracion con la tarjeta, recordar llamar despues de haber lamado la funcio nde salida.
def duracion(cedula):
    a=0
    b=0
    if file_name in files:
        rt=pandas.read_excel(file_name)
        if len(rt)==0:
            return None
        else:
            rtc1=rt.set_index('Cedula')
            cedula=rtc1.loc[cedula]
            ced=cedula.index.values
            l=len(ced)
            fecha_mes='2018-08'
            if 'Salida' in cedula.iloc[-1][2]:
                entrada=cedula.iloc[-1][0]+' '+cedula.iloc[-1][1]
                salida=cedula.iloc[-1][0]+' '+cedula.iloc[-2][1]
                fentrada=datetime.strptime(entrada,"%Y-%m-%d %H:%M")
                fsalida=datetime.strptime(salida,"%Y-%m-%d %H:%M")
                delta=fentrada-fsalida
                print(delta)
            else:
                print('El usuario no ha salido')

# entradas_mensuales(1088)
# duracion(1088)
cambiarEmpleado(11111,'zzzz')
