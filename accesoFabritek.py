# -*- coding: utf-8 -*-
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import openpyxl
import pandas
import os
from datetime import datetime
import time

LARGE_FONT=("Verdana",12)
NORM_FONT=("Verdana",10)
SMALL_FONT=("Verdana",8)

# verifica si el pin no existe tanto en empleados como en clientes, retorna True si existe, False si no
def verificarPin(pin):

    files=os.listdir('./')

    if '.PinUsuarios.xlsx' in files:
        df=pandas.read_excel('.PinUsuarios.xlsx')

        try:
            fe=df.loc[pin]
            return True
        except KeyError:
            pass


    if '.empleados.xlsx' in files:
        em=pandas.read_excel('.empleados.xlsx')

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

        if '.PinUsuarios.xlsx' in files:
            us=pandas.read_excel('.PinUsuarios.xlsx')
            us2=us.set_index('Cedula')

            try:
                us2.loc[cedula]
                return 1
            except KeyError:
                pass

        if '.usuarios.xlsx' in files:
            df=pandas.read_excel('.usuarios.xlsx')

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

    if '.PinUsuarios.xlsx' in files:
        try:
            df=pandas.read_excel('.PinUsuarios.xlsx')
            fe=df.loc[pin]
            cedula=fe[0]
            df1=df.drop(pin)
            writer = pandas.ExcelWriter('.PinUsuarios.xlsx', engine=None)
            df1.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            fecha=datetime.now()
            hora=fecha.strftime("%H:%M:%S")
            fecha=fecha.strftime("%Y-%m-%d")
            rg=pandas.read_excel('.RegistroTarjeta.xlsx')
            rg_t=rg.T
            col=rg_t.columns
            l=len(col)
            rg_t[l]=[cedula, fecha, hora, 'Salida']
            rg=rg_t.T
            writer = pandas.ExcelWriter('.RegistroTarjeta.xlsx', engine=None)
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

    if '.PinUsuarios.xlsx' in files:
        df=pandas.read_excel('.PinUsuarios.xlsx')

        try:
            fe=df.loc[pin]
            cedula=fe[0]
            reg=pandas.read_excel('.usuarios.xlsx')
            us=reg.loc[cedula]
            a=1
            datos=['cliente',us[0], us[1], us[2], cedula]
            return datos
        except KeyError:
            pass

    if a==0 :

        if '.empleados.xlsx' in files:
            em=pandas.read_excel('.empleados.xlsx')
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
    if '.PinUsuarios.xlsx' in files: #Se agrega el nuevo usuario
        df=pandas.read_excel('.PinUsuarios.xlsx')
        df_t=df.T
        fecha=datetime.now()
        hora=fecha.strftime("%H:%M:%S")
        fecha=fecha.strftime("%Y-%m-%d")
        df_t[pin]=[cedula]
        df=df_t.T
        writer = pandas.ExcelWriter('.PinUsuarios.xlsx', engine=None)
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        rg=pandas.read_excel('.RegistroTarjeta.xlsx')
        rg_t=rg.T
        col=rg_t.columns
        l=len(col)
        rg_t[l]=[cedula, fecha, hora, 'Entrada']
        rg=rg_t.T
        writer = pandas.ExcelWriter('.RegistroTarjeta.xlsx', engine=None)
        rg.to_excel(writer, sheet_name='Sheet1')
        writer.save()


    else:#Se crea nuevo documento de usuarios y se guarda usuario actual

        df = pandas.DataFrame({pin: [cedula]})
        df=df.T
        df.columns=['Cedula']
        writer = pandas.ExcelWriter('.PinUsuarios.xlsx', engine=None)
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        fecha=datetime.now()
        hora=fecha.strftime("%H:%M:%S")
        fecha=fecha.strftime("%Y-%m-%d")
        rg = pandas.DataFrame({0:[cedula,fecha,hora,'Entrada']})
        rg=rg.T
        rg.columns=['Cedula', 'Fecha', 'Hora', 'Entrada/salida']
        writer = pandas.ExcelWriter('.RegistroTarjeta.xlsx', engine=None)
        rg.to_excel(writer, sheet_name='Sheet1')
        writer.save()

    return None

#En caso de que la persona no este en usuarios aqui se haria el registro
def ingresarNuevoCliente(cedula, nombre , telefono, correo):
    files = os.listdir('./')

    if '.usuarios.xlsx' in files:
        us=pandas.read_excel('.usuarios.xlsx')
        us_t=us.T
        us_t[cedula]=[nombre,telefono,correo]
        us=us_t.T
        writer = pandas.ExcelWriter('.usuarios.xlsx', engine=None)
        us.to_excel(writer, sheet_name='Sheet1')
        writer.save()

    else:
        us = pandas.DataFrame({cedula: [nombre,telefono,correo]})
        us=us.T
        us.columns=['Nombre', 'Telefono','Correo']
        writer = pandas.ExcelWriter('.usuarios.xlsx', engine=None)
        us.to_excel(writer, sheet_name='Sheet1')
        writer.save()

#Retorna True si ya existe un empeado com esa cedula, Retorna False si es un cedula nueva
def verificarCedulaEmpleado(cedula):

        files=os.listdir('./')
        cedula=int(cedula)

        if '.empleados.xlsx' in files:
            us=pandas.read_excel('.empleados.xlsx')
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

    if '.empleados.xlsx' in files:
        em=pandas.read_excel('.empleados.xlsx')
        em_t=em.T
        em_t[pin]=[nombre,telefono,correo,cedula]
        em=em_t.T
        writer = pandas.ExcelWriter('.empleados.xlsx', engine=None)
        em.to_excel(writer, sheet_name='Sheet1')
        writer.save()
    else:
        em = pandas.DataFrame({pin: [nombre, telefono, correo, cedula]})
        em=em.T
        em.columns=['Nombre','Telefono','Correo', 'Cedula']
        writer = pandas.ExcelWriter('.empleados.xlsx', engine=None)
        em.to_excel(writer, sheet_name='Sheet1')
        writer.save()

#si Borra el empleado retorna True, si no existe retorna False
def borrarEmpleado(pin):
    files=os.listdir('./')
    pin=str(pin)

    if '.empleados.xlsx' in files:
        try:
            df=pandas.read_excel('.empleados.xlsx')
            fe=df.loc[pin]
            df1=df.drop(pin)
            writer = pandas.ExcelWriter('.empleados.xlsx', engine=None)
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
    df=pandas.read_excel('.PinUsuarios.xlsx')
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
    writer = pandas.ExcelWriter('.PinUsuarios.xlsx', engine=None)
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()

#Cambia el pin de un empleado en caso de perdida, recordar hacer verificacion de cedula y pin
def cambiarEmpleado(cedula, pin):
    em=pandas.read_excel('.empleados.xlsx')
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
    writer = pandas.ExcelWriter('.empleados.xlsx', engine=None)
    em.to_excel(writer, sheet_name='Sheet1')
    writer.save()

#Retorna numero de veces al mes de un usuario en especifico
def entradas_mensuales(cedula, año, mes):
    a=0
    b=0
    file_name='.RegistroTarjeta.xlsx'
    files=os.listdir('./')
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
            fecha=año + '-' + mes
            for f in ced:
                if fecha in cedula.iloc[a][0] and 'Entrada' in cedula.iloc[a][2]:
                    b=b+1
                a=a+1
            return b


#Restorna lista de diccionario que contiene los usuarios que ingresaron en el mes dado con la siguiente
#estructura : {cedula, nombre , telefono , correo, veces este mes}
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

#Restorna lista de diccionario que contiene los usuarios que ingresaron en el dia dado con la siguiente
#estructura : {cedula, nombre , telefono , correo}
def movimientos_dia(año, mes, dia):
    a=0
    file_name1='.RegistroTarjeta.xlsx'
    file_name2='.usuarios.xlsx'
    files=os.listdir('./')
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
    file_name='.RegistroTarjeta.xlsx'
    files=os.listdir('./')
    if file_name in files:
        rt=pandas.read_excel(file_name)
        if len(rt)==0:
            return None
        else:
            rtc1=rt.set_index('Cedula')
            cedula=rtc1.loc[cedula]
            ced=cedula.index.values
            l=len(ced)
            if 'Salida' in cedula.iloc[-1][2]:
                entrada=cedula.iloc[-1][0]+' '+cedula.iloc[-1][1]
                salida=cedula.iloc[-1][0]+' '+cedula.iloc[-2][1]
                fentrada=datetime.strptime(entrada,"%Y-%m-%d %H:%M:%S")
                fsalida=datetime.strptime(salida,"%Y-%m-%d %H:%M:%S")
                delta=fentrada-fsalida
            else:
                pass

# retorna todos los datos del usuario en una lista
def usuarioCedula(cedula):
    us=pandas.read_excel('.usuarios.xlsx')
    usu=us.loc[cedula]
    datos=[usu[0], usu[1], usu[2]]
    return datos

#Retorna Numero de usuarios con tarjeta asignada
def usuariosConTarjeta():
    uct=0
    filename1 = '.RegistroTarjeta.xlsx'
    filename2 = '.usuarios.xlsx'
    files = os.listdir('./')
    if filename1 in files:
        us=pandas.read_excel(filename2)
        us_cedula=us.index.values.tolist()
        rg=pandas.read_excel(filename1)
        rg=rg.set_index('Cedula')
        for f in us_cedula:
            try:
                rg_f=rg.loc[f]
                if type(rg_f) == pandas.core.series.Series:
                    if rg_f.iloc[-1]=='Entrada':
                        uct=uct+1
                else:
                    if rg_f.iloc[-1][2]=='Entrada':
                        uct=uct+1
            except:
                pass
        return uct
#Exporta excel con movimientos en todos los meses anteriores 
def exportarDatos(path):
    filename1 = '.usuarios.xlsx'
    filename2 = '.RegistroTarjeta.xlsx'
    fecha_ant = ' '
    us=pandas.read_excel(filename1)
    writer = pandas.ExcelWriter(path, engine=None)
    us.to_excel(writer, sheet_name='Información de Usuarios')

    rg=pandas.read_excel(filename2)
    rg_f=rg.set_index('Fecha')
    rg_f=rg_f.index.values.tolist()

    for f in rg_f:
        a=0
        fecha=datetime.strptime(f,"%Y-%m-%d")
        fecha_mes=fecha.strftime("%Y-%m")
        año=fecha.strftime("%Y")
        mes=fecha.strftime("%m")
        año_mes=fecha.strftime("%Y-%B")
        if fecha_ant not in f:
            mm=movimientos_mes(año, mes)
            m1=mm[0]
            rr = pandas.DataFrame({ a : [m1['cedula'],m1['nombre'],m1['telefono'],m1['correo'],m1['entradas']]})
            try:
                mm=mm[1:]
                for m in mm:
                    a=a+1
                    rr[a] = [m['cedula'],m['nombre'],m['telefono'],m['correo'],m['entradas']]
            except:
                pass
            rr=rr.T
            rr.columns=['Cedula','Nombre', 'Telefono', 'Correo', 'Entradas este mes']
            rr.to_excel(writer, sheet_name=año_mes)
        fecha_ant=fecha_mes
    writer.save()
# class ventanas(tk.Tk):
#
#     def __init__(self, *args, **kwargs):
#
#         tk.Tk.__init__(self, *args, **kwargs)
#
#         tk.Tk.iconbitmap(self,"palmeras.ico")
#         tk.Tk.wm_title(self,"Ventanas")
#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand= True)
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)
#
#         menubar = tk.Menu(container)
#         filemenu = tk.Menu(menubar, tearoff=0)
#         filemenu.add_command(label="Añadir Empleado",
#                                 command= lambda:self.show_frame(PinEmpleado))
#         filemenu.add_command(label="Borrar Empleado",
#                                 command= lambda:self.show_frame(BorrarEmpleado))
#         filemenu.add_command(label="Cambiar Pin",
#                                 command= lambda:self.show_frame(BorrarEmpleado))
#         filemenu.add_separator()
#         filemenu.add_command(label="Salir", command=quit)
#         menubar.add_cascade(label="Empleados", menu=filemenu)
#
#
#
#
#         filemenu2 = tk.Menu(menubar, tearoff=0)
#         filemenu2.add_command(label="Cambiar Pin",
#                                 command= lambda:self.show_frame(CedulaCambiar))
#
#         filemenu2.add_separator()
#         filemenu2.add_command(label="Salir", command=quit)
#         menubar.add_cascade(label="Clientes", menu=filemenu2)
#         tk.Tk.config(self, menu= menubar)
#
#         self.frames = {}
#         for F in (StartPage, Entrada, Salida, Pin, Verificar, IngresarEmpleado,
#                             PinEmpleado, BorrarEmpleado, Cedula, CedulaCambiar, CambiarCliente):
#
#             frame = F(container, self)
#
#             self.frames[F] = frame
#
#             frame.grid(row=0,column=0,sticky="nsew")
#
#         self.show_frame(StartPage)
#
#     def show_frame(self,cont):
#         frame=self.frames[cont]
#         frame.tkraise()
#     def get_page(self, page_class):
#         return self.frames[page_class]
#
# class StartPage(tk.Frame):
#
#     def __init__(self,parent,controller):
#         tk.Frame.__init__(self,parent)
#         label = tk.Label(self,text="Start Page",font=LARGE_FONT)
#         label.pack(pady=10,padx=10)
#
#         button1=ttk.Button(self,text="Entrada",
#                 command=lambda:controller.show_frame(Pin))
#         button1.pack()
#         button1=ttk.Button(self,text="Salida",
#                 command=lambda:controller.show_frame(Salida))
#         button1.pack()
#         button1=ttk.Button(self,text="Verificar",
#                 command=lambda:controller.show_frame(Verificar))
#         button1.pack()
#
# class Pin(tk.Frame):
#
#     def __init__(self,parent,controller):
#         tk.Frame.__init__(self,parent)
#         self.controller=controller
#         label = tk.Label(self,text="Ingresar Pin",font=LARGE_FONT)
#         label.pack(pady=10,padx=10)
#
#         button1=ttk.Button(self,text="Back Home",
#                 command=lambda:self.volver(controller))
#         button1.pack()
#         self.entry_pin=tk.Entry(self)
#         self.entry_pin.pack()
#         button3=ttk.Button(self,text="Ingresar pin",
#                 command=lambda:self.pin_siguiente(controller))
#         button3.pack()
#         self.text1=tk.Text(self,height=1,width=40)
#         self.text1.pack()
#
#         self.v=StringVar()
#
#     def pin_siguiente(self,controller):
#         files=os.listdir('./')
#         pin=self.entry_pin.get()
#         pin=str(pin)
#         if verificarPin(pin):
#             self.text1.delete('1.0',END)
#             self.text1.insert(END,"Este Pin Ya Existe")
#         else:
#             self.v=str(pin)
#             self.entry_pin.delete('0',END)
#             self.text1.delete('1.0',END)
#             controller.show_frame(Cedula)
#
#         '''
#         if '.usuarios.xlsx' in files:
#             df=pandas.read_excel('usuarios.xlsx')
#         '''
#
#     def volver(self, controller):
#         self.text1.delete('1.0',END)
#         self.entry_pin.delete('0',END)
#         controller.show_frame(StartPage)
#
# class Cedula(tk.Frame):
#
#     def __init__(self,parent,controller):
#         tk.Frame.__init__(self,parent)
#         self.controller=controller
#         label = tk.Label(self,text="Ingresar Cedula",font=LARGE_FONT)
#         label.pack(pady=10,padx=10)
#
#         button1=ttk.Button(self,text="Back Home",
#                 command=lambda:self.volver(controller))
#         button1.pack()
#         self.entry_ced=tk.Entry(self)
#         self.entry_ced.pack()
#         button3=ttk.Button(self,text="Ingresar Cedula",
#                 command=lambda:self.cedula_siguiente(controller))
#         button3.pack()
#         self.text1=tk.Text(self,height=1,width=40)
#         self.text1.pack()
#
#         self.c=StringVar()
#
#     def cedula_siguiente(self,controller):
#         a=0
#         files=os.listdir('./')
#         cedula=self.entry_ced.get()
#         cedula=int(cedula)
#         pagePin=self.controller.get_page(Pin)
#         pin=pagePin.v
#         pin=str(pin)
#
#         if '.PinUsuarios.xlsx' in files:
#             us=pandas.read_excel('.PinUsuarios.xlsx')
#
#             us2=us.set_index('Cedula')
#             print(us2.index)
#             try:
#                 us2.loc[cedula]
#                 self.text1.delete('1.0',END)
#                 self.text1.insert(END,"Esta usuario ya tiene un Pin asignado")
#                 a=1
#
#             except KeyError:
#                 print("Cedula valida")
#
#
#         if '.usuarios.xlsx' in files:
#             df=pandas.read_excel('.usuarios.xlsx')
#             us_t=df.T
#             try:
#                 pn=df.loc[cedula]
#                 print(cedula)
#
#                 if a==0:
#                     self.entry_ced.delete('0',END)
#                     self.text1.delete('1.0',END)
#                     usuario=df.loc[cedula]
#
#                     usuario[2]=usuario[2]+1
#
#                     us_t[cedula]=[usuario[0],usuario[1],usuario[2]]
#                     us=us_t.T
#                     writer = pandas.ExcelWriter('.usuarios.xlsx', engine=None)
#                     us.to_excel(writer, sheet_name='Sheet1')
#                     writer.save()
#                     fecha=datetime.now()
#                     hora=fecha.strftime("%H:%M")
#                     fecha=fecha.strftime("%Y-%m-%d")
#                     type(pin)
#                     df = pandas.DataFrame({pin: [cedula]})
#                     df=df.T
#                     writer = pandas.ExcelWriter('.PinUsuarios.xlsx', engine=None)
#                     df.to_excel(writer, sheet_name='Sheet1')
#                     writer.save()
#                     rg=pandas.read_excel('.RegistroTarjeta.xlsx')
#                     rg_t=rg.T
#                     col=rg_t.columns
#                     l=len(col)
#                     rg_t[l]=[cedula, fecha, hora, 'Entrada']
#                     rg=rg_t.T
#                     writer = pandas.ExcelWriter('.RegistroTarjeta.xlsx', engine=None)
#                     rg.to_excel(writer, sheet_name='Sheet1')
#                     writer.save()
#                     messagebox.showinfo("Ingresar Usuario", "El Usuario "+ usuario[0]
#                                                 +" Ha sido ingresado Exitosamente")
#                     controller.show_frame(StartPage)
#                 else:
#                     print("paila")
#
#             except KeyError:
#                 print("Cedula Nueva")
#                 self.c=cedula
#                 self.entry_ced.delete('0',END)
#                 self.text1.delete('1.0',END)
#                 controller.show_frame(Entrada)
#         else:
#             print("Cedula Nueva")
#             self.c=cedula
#             self.entry_ced.delete('0',END)
#             self.text1.delete('1.0',END)
#             controller.show_frame(Entrada)
#
#     def volver(self, controller):
#         self.text1.delete('1.0',END)
#         self.entry_ced.delete('0',END)
#         controller.show_frame(StartPage)
#
# class Entrada(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller=controller
#
#         label = tk.Label(self,text="Dar Entrada",font=LARGE_FONT)
#         label.pack(pady=10,padx=10)
#         button1=ttk.Button(self,text="Back to Home",
#                 command=lambda:controller.show_frame(StartPage))
#         button1.pack()
#
#         label1 = tk.Label(self,text="Nombre",font=LARGE_FONT)
#         label1.pack(pady=10,padx=10)
#         self.entry3=tk.Entry(self)
#         self.entry3.pack()
#         label1 = tk.Label(self,text="Telefono",font=LARGE_FONT)
#         label1.pack(pady=10,padx=10)
#
#         self.entry4=tk.Entry(self)
#         self.entry4.pack()
#         button5=ttk.Button(self,text="Ingresar Usuario",
#                     command=lambda:self.ingresar_usuario(controller))
#         button5.pack()
#         self.text1=tk.Text(self,height=1,width=20)
#         self.text1.pack()
#
#
#     def guardar_registro(self,cedula):
#         files = os.listdir('./')
#         if '.usuarios.xlsx' in files:
#             us=pandas.read_excel('.usuarios.xlsx')
#             us_t=us.T
#             try:
#                 usuario=us.loc[cedula]
#                 usuario[2]=usuario[2]+1
#                 us_t[cedula]=[usuario[0],usuario[1],usuario[2]]
#                 us=us_t.T
#
#                 writer = pandas.ExcelWriter('.usuarios.xlsx', engine=None)
#                 us.to_excel(writer, sheet_name='Sheet1')
#                 writer.save()
#                 datos=[usuario[0],usuario[1]]
#                 return datos
#             except KeyError:
#                 nombre=self.entry3.get()
#                 telefono=int(self.entry4.get())
#                 us_t[cedula]=[nombre,telefono,1]
#                 us=us_t.T
#
#                 writer = pandas.ExcelWriter('.usuarios.xlsx', engine=None)
#                 us.to_excel(writer, sheet_name='Sheet1')
#                 writer.save()
#                 datos=[nombre,telefono]
#                 return datos
#
#         else:
#             nombre=self.entry3.get()
#             telefono=int(self.entry4.get())
#             us = pandas.DataFrame({cedula: [nombre,telefono,1]})
#             us=us.T
#             us.columns=['Nombre', 'Telefono', 'Recurrencia']
#             writer = pandas.ExcelWriter('.usuarios.xlsx', engine=None)
#             us.to_excel(writer, sheet_name='Sheet1')
#             writer.save()
#
#             datos=[nombre,telefono]
#             return datos
#
#     def ingresar_usuario(self,controller):
#         files=os.listdir('./')
#         pageCed=self.controller.get_page(Cedula)
#         cedula=int(pageCed.c)
#         # cedula=self.entry2.get()
#         # cedula=int(cedula)
#         # ced=self.comprobar_cedula()
#         pagePin=self.controller.get_page(Pin)
#         pin=pagePin.v
#         pin=str(pin)
#
#         if '.PinUsuarios.xlsx' in files: #Se agrega el nuevo usuario
#             df=pandas.read_excel('.PinUsuarios.xlsx')
#             df_t=df.T
#             datos=self.guardar_registro(cedula)
#             nombre=datos[0]
#             fecha=datetime.now()
#             hora=fecha.strftime("%H:%M")
#             fecha=fecha.strftime("%Y-%m-%d")
#             print(type(pin))
#             df_t[pin]=[cedula]
#             df=df_t.T
#             writer = pandas.ExcelWriter('.PinUsuarios.xlsx', engine=None)
#             df.to_excel(writer, sheet_name='Sheet1')
#             writer.save()
#
#             rg=pandas.read_excel('.RegistroTarjeta.xlsx')
#             rg_t=rg.T
#             col=rg_t.columns
#             l=len(col)
#             rg_t[l]=[cedula, fecha, hora, 'Entrada']
#             rg=rg_t.T
#             writer = pandas.ExcelWriter('.RegistroTarjeta.xlsx', engine=None)
#             rg.to_excel(writer, sheet_name='Sheet1')
#             writer.save()
#             messagebox.showinfo("Ingresar Usuario", "Usuario Ingresado Exitosamente")
#
#             self.entry3.delete('0',END)
#             self.entry4.delete('0',END)
#             self.text1.delete('1.0',END)
#             controller.show_frame(StartPage)
#
#         else:#Se crea nuevo documento de usuarios y se guarda usuario actual
#             print(pin)
#             datos=self.guardar_registro(cedula)
#             nombre=datos[0]
#             fecha=datetime.now()
#             fecha=fecha.strftime("%Y-%m-%d-%H-%M-%f")
#             print(type(pin))
#             df = pandas.DataFrame({pin: [cedula]})
#             df=df.T
#             df.columns=['Cedula']
#             writer = pandas.ExcelWriter('.PinUsuarios.xlsx', engine=None)
#             df.to_excel(writer, sheet_name='Sheet1')
#             writer.save()
#             fecha=datetime.now()
#             hora=fecha.strftime("%H:%M")
#             fecha=fecha.strftime("%Y-%m-%d")
#             rg = pandas.DataFrame({0:[cedula,fecha,hora,'Entrada']})
#             rg=rg.T
#             rg.columns=['Cedula', 'Fecha', 'Hora', 'Entrada/salida']
#             writer = pandas.ExcelWriter('.RegistroTarjeta.xlsx', engine=None)
#             rg.to_excel(writer, sheet_name='Sheet1')
#             writer.save()
#             messagebox.showinfo("Ingresar Usuario", "Usuario Ingresado Exitosamente")
#
#             self.entry3.delete('0',END)
#             self.entry4.delete('0',END)
#             self.text1.delete('1.0',END)
#             controller.show_frame(StartPage)
#
# class Salida(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self,text="Dar Salida",font=LARGE_FONT)
#         label.pack(pady=10,padx=10)
#         button1=ttk.Button(self,text="Back to Home",
#                 command=lambda:self.volver(controller))
#         button1.pack()
#         self.entry_id = StringVar()
#         self.entry1=tk.Entry(self)
#         self.entry1.pack()
#         button3=ttk.Button(self,text="Dar Salida",
#                 command=lambda:self.borrar_pin(controller))
#         button3.pack()
#         self.text1=tk.Text(self,height=1,width=20)
#         self.text1.pack()
#
#     def borrar_pin(self, controller):
#         files=os.listdir('./')
#         pin=self.entry1.get()
#         pin=str(pin)
#
#         if '.PinUsuarios.xlsx' in files:
#             try:
#                 df=pandas.read_excel('.PinUsuarios.xlsx')
#                 fe=df.loc[pin]
#                 cedula=fe[0]
#                 #FechaIngreso=fe[1]
#                 #Ingreso=datetime.strptime(FechaIngreso,"%Y-%m-%d-%H-%M-%f")#Cambiar formato a uno mas amigable en el registro
#                 #Ahora=datetime.now()
#                 #delta=Ahora-Ingreso
#                 #delta = str(delta)
#                 #print(delta)
#                 df1=df.drop(pin)
#                 writer = pandas.ExcelWriter('PinUsuarios.xlsx', engine=None)
#                 df1.to_excel(writer, sheet_name='Sheet1')
#                 writer.save()
#                 fecha=datetime.now()
#                 hora=fecha.strftime("%H:%M")
#                 fecha=fecha.strftime("%Y-%m-%d")
#                 rg=pandas.read_excel('RegistroTarjeta.xlsx')
#                 rg_t=rg.T
#                 col=rg_t.columns
#                 l=len(col)
#                 rg_t[l]=[cedula, fecha, hora, 'Salida']
#                 rg=rg_t.T
#                 writer = pandas.ExcelWriter('RegistroTarjeta.xlsx', engine=None)
#                 rg.to_excel(writer, sheet_name='Sheet1')
#                 writer.save()
#                 messagebox.showinfo("Dar Salida a Usuario", "Usuario Borrado Exitosamente")
#                 self.entry1.delete('0',END)
#                 self.text1.delete('1.0',END)
#                 controller.show_frame(StartPage)
#             except KeyError:
#                 self.text1.insert(END,"Este pin no existe")
#                 self.entry1.delete('0',END)
#         else:
#             self.text1.insert(END,"Este pin no existe")
#             self.entry1.delete('0',END)
#
#     def volver(self, controller):
#         self.text1.delete('1.0',END)
#         self.entry1.delete('0',END)
#         controller.show_frame(StartPage)
#
# class Verificar(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self,text="Verificar Pin",font=LARGE_FONT)
#         label.pack(pady=10,padx=10)
#         button1=ttk.Button(self,text="Back to Home",
#                 command=lambda:self.volver(controller))
#         button1.pack()
#
#         self.entry1=tk.Entry(self)
#         self.entry1.pack()
#         button2=ttk.Button(self,text="Verificar",
#                 command=self.verificar_pin)
#         button2.pack()
#         self.text1=tk.Text(self,height=1,width=40)
#         self.text1.pack()
#
#
#     def verificar_pin(self):
#         a=0
#         files=os.listdir('./')
#         pin=self.entry1.get()
#         pin=str(pin)
#
#         if 'PinUsuarios.xlsx' in files:
#             df=pandas.read_excel('PinUsuarios.xlsx')
#             try:
#                 fe=df.loc[pin]
#                 cedula=fe[0]
#                 reg=pandas.read_excel('usuarios.xlsx')
#                 us=reg.loc[cedula]
#                 self.text1.delete('1.0',END)
#                 self.text1.insert(END,"este pin pertenece al cliente : "+us[0])
#                 print("este pin pertenece a: "+us[0])
#                 self.entry1.delete('0',END)
#                 a=1
#             except KeyError:
#                 self.text1.delete('1.0',END)
#                 self.text1.insert(END,"este pin no esta registrado")
#
#         if a==0 :
#             if 'empleados.xlsx' in files:
#                 em=pandas.read_excel('empleados.xlsx')
#                 try:
#                     em=em.loc[pin]
#                     cedula=em[2]
#
#                     self.text1.delete('1.0',END)
#                     self.text1.insert(END,"este pin pertenece al empleado : "+em[0])
#
#                     self.entry1.delete('0',END)
#
#                 except KeyError:
#                     self.text1.delete('1.0',END)
#                     self.text1.insert(END,"este pin no esta registrado")
#
#             else:
#                 self.text1.delete('1.0',END)
#                 self.text1.insert(END,"este pin no esta registrado")
#
#     def volver(self, controller):
#         self.text1.delete('1.0',END)
#         self.entry1.delete('0',END)
#         controller.show_frame(StartPage)
#
# class PinEmpleado(tk.Frame):
#
#     def __init__(self,parent,controller):
#         tk.Frame.__init__(self,parent)
#         self.controller=controller
#         label = tk.Label(self,text="Ingresar Pin",font=LARGE_FONT)
#         label.pack(pady=10,padx=10)
#
#         button1=ttk.Button(self,text="Back Home",
#                 command=lambda:self.volver(controller))
#         button1.pack()
#         self.entry_pin=tk.Entry(self)
#         self.entry_pin.pack()
#         button3=ttk.Button(self,text="Ingresar pin",
#                 command=lambda:self.pin_siguiente(controller))
#         button3.pack()
#         self.text1=tk.Text(self,height=1,width=40)
#         self.text1.pack()
#
#         self.v=StringVar()
#
#     def pin_siguiente(self,controller):
#         files=os.listdir('./')
#         pin=self.entry_pin.get()
#         pin=str(pin)
#         if verificarPin(pin):
#             self.text1.delete('1.0',END)
#             self.text1.insert(END,"Este Pin Ya Existe")
#         else:
#             self.v=str(pin)
#             self.entry_pin.delete('0',END)
#             self.text1.delete('1.0',END)
#             controller.show_frame(IngresarEmpleado)
#
#     def volver(self, controller):
#         self.text1.delete('1.0',END)
#         self.entry_pin.delete('0',END)
#         controller.show_frame(StartPage)
#
# class IngresarEmpleado(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller=controller
#         label = tk.Label(self,text="Ingresar Empleado",font=LARGE_FONT)
#         label.pack(pady=10,padx=10)
#         button1=ttk.Button(self,text="Back to Home",
#                 command=lambda:self.volver(controller))
#         button1.pack()
#         label1 = tk.Label(self,text="Nombre",font=LARGE_FONT)
#         label1.pack(pady=10,padx=10)
#         self.entry1=tk.Entry(self)
#         self.entry1.pack()
#         label2 = tk.Label(self,text="Cedula",font=LARGE_FONT)
#         label2.pack(pady=10,padx=10)
#         self.entry2=tk.Entry(self)
#         self.entry2.pack()
#         label3 = tk.Label(self,text="Telefono",font=LARGE_FONT)
#         label3.pack(pady=10,padx=10)
#         self.entry3=tk.Entry(self)
#         self.entry3.pack()
#         button2=ttk.Button(self,text="Ingresar", command=lambda:self.ingresar_empleado(controller))
#         button2.pack()
#         self.text1=tk.Text(self,height=1,width=40)
#         self.text1.pack()
#     def ingresar_empleado(self, controller):
#         files = os.listdir('./')
#         pagePin=self.controller.get_page(PinEmpleado)
#         pin=pagePin.v
#         pin=str(pin)
#         nombre=self.entry1.get()
#         cedula=self.entry2.get()
#         telefono=self.entry3.get()
#         cedula=int(cedula)
#         if 'empleados.xlsx' in files:
#             em=pandas.read_excel('empleados.xlsx')
#             em1=em.set_index('Cedula')
#             print(em1)
#             try :
#                 em1.loc[cedula]
#                 self.text1.insert(END,"Ya existe un pin asociado a este empleado ")
#                 self.entry1.delete('0',END)
#                 self.entry2.delete('0',END)
#                 self.entry3.delete('0',END)
#
#
#             except KeyError:
#
#                 em_t=em.T
#                 em_t[pin]=[nombre,telefono,cedula]
#                 em=em_t.T
#                 writer = pandas.ExcelWriter('empleados.xlsx', engine=None)
#                 em.to_excel(writer, sheet_name='Sheet1')
#                 writer.save()
#
#                 messagebox.showinfo("Ingresar Empleado", "Empleado Ingresado Exitosamente")
#                 self.entry1.delete('0',END)
#                 self.entry2.delete('0',END)
#                 self.entry3.delete('0',END)
#                 self.text1.delete('1.0',END)
#                 controller.show_frame(StartPage)
#         else:
#             em = pandas.DataFrame({pin: [nombre, telefono, cedula]})
#             em=em.T
#             em.columns=['Nombre','Telefono', 'Cedula']
#             writer = pandas.ExcelWriter('empleados.xlsx', engine=None)
#             em.to_excel(writer, sheet_name='Sheet1')
#             writer.save()
#             messagebox.showinfo("Ingresar Empleado", "Empleado Ingresado Exitosamente")
#             self.entry1.delete('0',END)
#             self.entry2.delete('0',END)
#             self.entry3.delete('0',END)
#             controller.show_frame(StartPage)
#
#     def volver(self, controller):
#         self.text1.delete('1.0',END)
#         self.entry1.delete('0',END)
#         self.entry2.delete('0',END)
#         self.entry3.delete('0',END)
#         controller.show_frame(StartPage)
#
# class BorrarEmpleado(tk.Frame):
#
#     def __init__(self, parent, controller):
#
#         tk.Frame.__init__(self, parent)
#         def get_selected_row(event):
#             index=self.lista.curselection()
#             print(index[0])
#             self.v=index[0]
#             return(index[0])
#         label = tk.Label(self,text="Borrar Empleado",font=LARGE_FONT)
#         label.grid(row=0,column=1)
#         button1=ttk.Button(self,text="Back to Home",
#                 command=lambda:self.volver(controller))
#         button1.grid(row=0,column=0)
#         self.entry_id = StringVar()
#
#         self.lista=Listbox(self, height=6, width=35)
#         self.lista.grid(row=4,column=1)
#         self.sb1=Scrollbar(self)
#         self.sb1.grid(row=4,column=2)
#         self.lista.configure(yscrollcommand=self.sb1.set)
#         self.sb1.configure(command=self.lista.yview)
#         self.lista.bind('<<ListboxSelect>>',get_selected_row)
#         button1=ttk.Button(self,text="llenar", command=lambda:self.llenar(controller))
#         button1.grid(row=5,column=1)
#         button1=ttk.Button(self,text="borrar", command=lambda:self.borrar(controller))
#         button1.grid(row=6,column=1)
#
#
#     def get_selected_row(self,event):
#         index=self.lista.curselection()
#         return(index[0])
#     def borrar(self,controller):
#         df=pandas.read_excel('empleados.xlsx')
#         df_t=df.T
#         d=df_t.columns
#         print(self.v)
#         row=int(self.v)-1
#         em=df.iloc[row]
#         el=d[row]
#         df1=df.drop(d[row])
#         df1_t=df1.T
#         d=df1_t.columns
#         writer = pandas.ExcelWriter('empleados.xlsx', engine=None)
#         df1.to_excel(writer, sheet_name='Sheet1')
#         writer.save()
#         a=len(d)
#         b=0
#         self.lista.delete('0',END)
#         texto=str('Pin    Nombre    Telefono    Cedula')
#         self.lista.insert(END,texto)
#         while(b<a):
#             em=df1.iloc[b]
#             texto=str(d[b])+'    '+str(em[0])+'    '+str(em[1])+ '    '+str (em[2])
#             self.lista.insert(END,texto)
#             b=b+1
#
#
#     def volver(self, controller):
#
#         self.lista.delete('0',END)
#         controller.show_frame(StartPage)
#
#     def llenar(self, controller):
#         df=pandas.read_excel('empleados.xlsx')
#         df_t=df.T
#         d=df_t.columns
#         a=len(d)
#         b=0
#         self.lista.delete('0',END)
#         texto=str('Pin    Nombre    Telefono    Cedula')
#         self.lista.insert(END,texto)
#         while(b<a):
#             em=df.iloc[b]
#             texto=str(d[b])+'    '+str(em[0])+'    '+str(em[1])+'    '+str(em[2])
#             self.lista.insert(END,texto)
#             b=b+1
#
# class CedulaCambiar(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller=controller
#         label = tk.Label(self,text="Cambiar Pin Cliente",font=LARGE_FONT)
#         label.pack(pady=10,padx=10)
#         button1=ttk.Button(self,text="Back to Home",
#                 command=lambda:self.volver(controller))
#         button1.pack()
#         label = tk.Label(self,text="Cedula",font=LARGE_FONT)
#         label.pack(pady=10,padx=10)
#         self.entry1=tk.Entry(self)
#         self.entry1.pack()
#         button2=ttk.Button(self,text="Cambiar",
#                 command=lambda:self.verificar_cedula(controller))
#         button2.pack()
#         self.text1=tk.Text(self,height=1,width=40)
#         self.text1.pack()
#
#
#     def verificar_cedula(self,controller):
#         a=0
#         files=os.listdir('./')
#         cedula=self.entry1.get()
#         cedula=int(cedula)
#
#         if 'PinUsuarios.xlsx' in files:
#             df=pandas.read_excel('PinUsuarios.xlsx')
#             ced=df.set_index('Cedula')
#             try:
#                 ced.loc[cedula]
#                 self.cc=cedula
#                 self.text1.delete('1.0',END)
#                 self.entry1.delete('0',END)
#                 controller.show_frame(CambiarCliente)
#             except KeyError:
#                 self.text1.delete('1.0',END)
#                 self.text1.insert(END,"este usuario no tiene un pin asignado")
#
#
#
#     def volver(self, controller):
#         self.text1.delete('1.0',END)
#         self.entry1.delete('0',END)
#         controller.show_frame(StartPage)
#
# class CambiarCliente(tk.Frame):
#
#     def __init__(self,parent,controller):
#         tk.Frame.__init__(self,parent)
#         self.controller=controller
#         label = tk.Label(self,text="Ingresar Pin",font=LARGE_FONT)
#         label.pack(pady=10,padx=10)
#
#         button1=ttk.Button(self,text="Back Home",
#                 command=lambda:self.volver(controller))
#         button1.pack()
#         self.entry_pin=tk.Entry(self)
#         self.entry_pin.pack()
#         button3=ttk.Button(self,text="Cambiar Pin",
#                 command=lambda:self.cambiar(controller))
#         button3.pack()
#         self.text1=tk.Text(self,height=1,width=40)
#         self.text1.pack()
#
#         self.c=StringVar()
#
#     def cambiar(self,controller):
#
#         files=os.listdir('./')
#         pin=self.entry_pin.get()
#         pin=str(pin)
#         if verificarPin(pin):
#             self.text1.delete('1.0',END)
#             self.entry_pin.delete('0',END)
#             self.text1.insert(END,'Ya existe este Pin')
#
#         else:
#             pageCedula=self.controller.get_page(CedulaCambiar)
#             cedula=pageCedula.cc
#             cedula=int(cedula)
#             df=pandas.read_excel('PinUsuarios.xlsx')
#             ced=df.set_index('Cedula')
#             c=ced.loc[cedula]
#             dt=ced.T
#             cee=dt.columns.tolist()
#             ind=cee.index(cedula)
#             br=df.index
#
#             pin_b=br[ind]
#             print(pin_b)
#             dff=df.drop(pin_b)
#             df_t=dff.T
#             df_t[pin]=[cedula]
#             df=df_t.T
#             writer = pandas.ExcelWriter('PinUsuarios.xlsx', engine=None)
#             df.to_excel(writer, sheet_name='Sheet1')
#             writer.save()
#             self.text1.delete('1.0',END)
#             self.entry_pin.delete('0',END)
#             messagebox.showinfo("Cambiar Pn Cliente", "Se ha cambiado el pin exitosamente")
#             controller.show_frame(StartPage)
#
#
#
#     def volver(self, controller):
#         self.text1.delete('1.0',END)
#         self.entry_pin.delete('0',END)
#         controller.show_frame(StartPage)

# app=ventanas()
# app.geometry("720x320")
# app.mainloop()
cedula=1233444
pin='bbbb'
nombre='coc34co'
correo='coo@ooo'
telefono=310
if verificarPin(pin):
    borrarPinCliente(pin)
    print(duracion(cedula))
    print('Ok')
else:
    if verificarCedulaCliente(cedula)==2:
        nuevoPinCliente(pin, cedula)
        print('2')
    if verificarCedulaCliente(cedula)==3:
        ingresarNuevoCliente(cedula, nombre, telefono, correo)
        nuevoPinCliente(pin, cedula)
        print('3')
    elif verificarCedulaCliente(cedula)==1:
        print('ya esta registrado')
print(usuariosConTarjeta())
