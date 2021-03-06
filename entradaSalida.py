from tkinter import *
import tkinter as tk
from tkinter import ttk
import openpyxl
import pandas
import os
from datetime import datetime
import time
LARGE_FONT=("Verdana",12)

class ventanas(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self,"palmeras.ico")
        tk.Tk.wm_title(self,"Ventanas")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand= True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Entrada, Salida, Pin, Verificar):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()
    def get_page(self, page_class):
        return self.frames[page_class]

class StartPage(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Start Page",font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1=ttk.Button(self,text="Entrada",
                command=lambda:controller.show_frame(Pin))
        button1.pack()
        button1=ttk.Button(self,text="Salida",
                command=lambda:controller.show_frame(Salida))
        button1.pack()
        button1=ttk.Button(self,text="Verificar",
                command=lambda:controller.show_frame(Verificar))
        button1.pack()

class Pin(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller=controller
        label = tk.Label(self,text="Ingresar Pin",font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1=ttk.Button(self,text="Back Home",
                command=lambda:controller.show_frame(StartPage))
        button1.pack()
        self.entry_pin=tk.Entry(self)
        self.entry_pin.pack()
        button3=ttk.Button(self,text="Ingresar pin",
                command=lambda:self.pin_siguiente(controller))
        button3.pack()
        self.text1=tk.Text(self,height=1,width=40)
        self.text1.pack()

        self.v=StringVar()

    def pin_siguiente(self,controller):
        files=os.listdir()
        pin=self.entry_pin.get()
        pin=int(pin)
        if 'usuarios.xlsx' in files:
            df=pandas.read_excel('usuarios.xlsx')

            try:
                df.loc[pin]
                self.text1.delete('1.0',END)
                self.text1.insert(END,"Este Pin Ya Existe")


            except KeyError:
                print("Pin Valido")
                self.v=str(pin)
                self.entry_pin.delete('0',END)
                self.text1.delete('1.0',END)
                controller.show_frame(Entrada)
        else:
            print("Pin Valido")
            self.v=str(pin)
            self.entry_pin.delete('0',END)
            self.text1.delete('1.0',END)
            controller.show_frame(Entrada)

class Entrada(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller=controller
        label = tk.Label(self,text="Dar Entrada",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1=ttk.Button(self,text="Back to Home",
                command=lambda:controller.show_frame(StartPage))
        button1.pack()

        self.entry2=tk.Entry(self)
        self.entry2.pack()
        button3=ttk.Button(self,text="Ingresar cedula",
                command=self.comprobar_cedula)
        button3.pack()
        label1 = tk.Label(self,text="Nombre",font=LARGE_FONT)
        label1.pack(pady=10,padx=10)
        self.entry3=tk.Entry(self)
        self.entry3.pack()
        label1 = tk.Label(self,text="Telefono",font=LARGE_FONT)
        label1.pack(pady=10,padx=10)

        self.entry4=tk.Entry(self)
        self.entry4.pack()
        button5=ttk.Button(self,text="Ingresar Usuario",
                    command=lambda:self.ingresar_usuario(controller))
        button5.pack()
        self.text1=tk.Text(self,height=1,width=20)
        self.text1.pack()


    def guardar_registro(self,cedula):
        files = os.listdir()
        if 'registro.xlsx' in files:
            us=pandas.read_excel('registro.xlsx')
            us_t=us.T
            try:
                usuario=us.loc[cedula]
                usuario[2]=usuario[2]+1
                us_t[cedula]=[usuario[0],usuario[1],usuario[2]]
                us=us_t.T
                writer = pandas.ExcelWriter('registro.xlsx', engine=None)
                us.to_excel(writer, sheet_name='Sheet1')
                writer.save()
                datos=[usuario[0],usuario[1]]
                return datos
            except KeyError:
                nombre=self.entry3.get()
                telefono=self.entry4.get()
                us_t[cedula]=[nombre,telefono,1]
                us=us_t.T
                writer = pandas.ExcelWriter('registro.xlsx', engine=None)
                us.to_excel(writer, sheet_name='Sheet1')
                writer.save()
                datos=[nombre,telefono]
                return datos

        else:
            nombre=self.entry3.get()
            telefono=self.entry4.get()
            us = pandas.DataFrame({cedula: [nombre,telefono,1]})
            us=us.T
            writer = pandas.ExcelWriter('registro.xlsx', engine=None)
            us.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            datos=[nombre,telefono]
            return datos
    def comprobar_cedula(self):
        files=os.listdir()
        cedula=self.entry2.get()
        cedula=int(cedula)
        if 'registro.xlsx' in files:
            df=pandas.read_excel('registro.xlsx')

            try:
                us=df.loc[cedula]
                print("ya se ha ingresado esta cedula")
                self.entry3.delete('0',END)
                self.entry4.delete('0',END)
                self.entry3.insert(END,us[0])
                self.entry4.insert(END,us[1])

            except KeyError:
                print("Cedula Valida")

        else:

            print("Cedula Valida")
    def ingresar_usuario(self,controller):
        files=os.listdir()
        cedula=self.entry2.get()
        cedula=int(cedula)
        ced=self.comprobar_cedula()
        pagePin=self.controller.get_page(Pin)
        pin=pagePin.v
        pin=int(pin)

        if 'usuarios.xlsx' in files: #Se agrega el nuevo usuario
            df=pandas.read_excel('usuarios.xlsx')
            df_t=df.T
            datos=self.guardar_registro(cedula)
            nombre=datos[0]
            fecha=datetime.now()
            fecha=fecha.strftime("%Y-%m-%d-%H-%M-%f")
            df_t[pin]=[nombre,fecha,cedula]
            df=df_t.T
            writer = pandas.ExcelWriter('usuarios.xlsx', engine=None)
            df.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            self.entry2.delete('0',END)
            self.entry3.delete('0',END)
            self.entry4.delete('0',END)
            self.text1.delete('1.0',END)
            controller.show_frame(StartPage)

        else:#Se crea nuevo documento de usuarios y se guarda usuario actual
            datos=self.guardar_registro(cedula)
            nombre=datos[0]
            fecha=datetime.now()
            fecha=fecha.strftime("%Y-%m-%d-%H-%M-%f")
            df = pandas.DataFrame({pin: [nombre,fecha,cedula]})
            df=df.T
            writer = pandas.ExcelWriter('usuarios.xlsx', engine=None)
            df.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            self.entry2.delete('0',END)
            self.entry3.delete('0',END)
            self.entry4.delete('0',END)
            self.text1.delete('1.0',END)
            controller.show_frame(StartPage)

class Salida(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self,text="Dar Salida",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1=ttk.Button(self,text="Back to Home",
                command=lambda:controller.show_frame(StartPage))
        button1.pack()
        self.entry_id = StringVar()
        self.entry1=tk.Entry(self,textvariable=self.entry_id)
        self.entry1.pack()
        button3=ttk.Button(self,text="Dar Salida",
                command=lambda:self.borrar_pin(controller))
        button3.pack()
        self.text1=tk.Text(self,height=1,width=20)
        self.text1.pack()

    def borrar_pin(self, controller):
        files=os.listdir()
        pin=self.entry1.get()
        pin=int(pin)

        if 'usuarios.xlsx' in files:
            try:
                df=pandas.read_excel('usuarios.xlsx')
                fe=df.loc[pin]
                FechaIngreso=fe[1]
                Ingreso=datetime.strptime(FechaIngreso,"%Y-%m-%d-%H-%M-%f")#Cambiar formato a uno mas amigable en el registro
                Ahora=datetime.now()
                delta=Ahora-Ingreso
                print(delta)
                df1=df.drop(pin)
                writer = pandas.ExcelWriter('usuarios.xlsx', engine=None)
                df1.to_excel(writer, sheet_name='Sheet1')
                writer.save()
                print("este pin ha sido borrado")
                self.entry1.delete('0',END)
                controller.show_frame(StartPage)
            except KeyError:
                print("Este pin no existe")

        else:
            print("este pin no existe")
            self.entry1.delete('0',END)

class Verificar(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self,text="Verificar Pin",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1=ttk.Button(self,text="Back to Home",
                command=lambda:self.volver(controller))
        button1.pack()

        self.entry1=tk.Entry(self)
        self.entry1.pack()
        button2=ttk.Button(self,text="Verificar",
                command=self.verificar_pin)
        button2.pack()
        self.text1=tk.Text(self,height=1,width=40)
        self.text1.pack()

    def verificar_pin(self):
        files=os.listdir()
        pin=self.entry1.get()
        pin=int(pin)

        if 'usuarios.xlsx' in files:
            df=pandas.read_excel('usuarios.xlsx')
            try:
                fe=df.loc[pin]
                cedula=fe[2]
                reg=pandas.read_excel('registro.xlsx')
                us=reg.loc[cedula]
                self.text1.delete('1.0',END)
                self.text1.insert(END,"este pin pertenece a: "+us[0])
                print("este pin pertenece a: "+us[0])
                self.entry1.delete('0',END)
            except KeyError:
                self.text1.delete('1.0',END)
                self.text1.insert(END,"este pin no esta registrado")

        else:
            print("este pin no existe")
            self.entry1.delete('0',END)
    def volver(self, controller):
        self.text1.delete('1.0',END)
        controller.show_frame(StartPage)

app=ventanas()
app.mainloop()
