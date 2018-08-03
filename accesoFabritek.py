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

def popupmsg():
    popup= tk.Tk()
    tmp = PhotoImage(file='boton.gif')


    #buttonStart = Button(frameWb,image=tmp,command=root.quit)
    popup.wm_title("!")
    label = tk.Label(image = tmp)
    #label = ttk.Label(popup, text="Lista Empleados", font=NORM_FONT)
    label.pack()
    B1=ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()
class ventanas(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self,"palmeras.ico")
        tk.Tk.wm_title(self,"Ventanas")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand= True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Empleados",
                                command= lambda:popupmsg())
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=quit)
        menubar.add_cascade(label="Empleados", menu=filemenu)

        tk.Tk.config(self, menu= menubar)

        self.frames = {}
        for F in (StartPage, Entrada, Salida, Pin, Verificar, IngresarEmpleado, PinEmpleado, BorrarEmpleado):

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
        button1=ttk.Button(self,text="Ingresar Empleado",
                command=lambda:controller.show_frame(PinEmpleado))
        button1.pack()
        button1=ttk.Button(self,text="Eliminar Empleado",
                command=lambda:controller.show_frame(BorrarEmpleado))
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
        files=os.listdir('./')
        pin=self.entry_pin.get()
        pin=str(pin)

        if 'usuarios.xlsx' in files:
            df=pandas.read_excel('usuarios.xlsx')

            try:
                pn=df.loc[pin]
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
        files = os.listdir('./')
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
        files=os.listdir('./')
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
        files=os.listdir('./')
        cedula=self.entry2.get()
        cedula=int(cedula)
        ced=self.comprobar_cedula()
        pagePin=self.controller.get_page(Pin)
        pin=pagePin.v
        pin=str(pin)

        if 'usuarios.xlsx' in files: #Se agrega el nuevo usuario
            df=pandas.read_excel('usuarios.xlsx')
            df_t=df.T
            datos=self.guardar_registro(cedula)
            nombre=datos[0]
            fecha=datetime.now()
            fecha=fecha.strftime("%Y-%m-%d-%H-%M-%f")
            print(pin)
            df_t[pin]=[nombre,fecha,cedula]
            df=df_t.T
            writer = pandas.ExcelWriter('usuarios.xlsx', engine=None)
            df.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            messagebox.showinfo("Ingresar Usuario", "Usuario Ingresado Exitosamente")
            self.entry2.delete('0',END)
            self.entry3.delete('0',END)
            self.entry4.delete('0',END)
            self.text1.delete('1.0',END)
            controller.show_frame(StartPage)

        else:#Se crea nuevo documento de usuarios y se guarda usuario actual
            print(pin)
            datos=self.guardar_registro(cedula)
            nombre=datos[0]
            fecha=datetime.now()
            fecha=fecha.strftime("%Y-%m-%d-%H-%M-%f")
            df = pandas.DataFrame({pin: [nombre,fecha,cedula]})
            df=df.T
            writer = pandas.ExcelWriter('usuarios.xlsx', engine=None)
            df.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            messagebox.showinfo("Ingresar Usuario", "Usuario Ingresado Exitosamente")
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
        files=os.listdir('./')
        pin=self.entry1.get()
        pin=str(pin)

        if 'usuarios.xlsx' in files:
            try:
                df=pandas.read_excel('usuarios.xlsx')
                fe=df.loc[pin]
                FechaIngreso=fe[1]
                Ingreso=datetime.strptime(FechaIngreso,"%Y-%m-%d-%H-%M-%f")#Cambiar formato a uno mas amigable en el registro
                Ahora=datetime.now()
                delta=Ahora-Ingreso
                delta = str(delta)
                print(delta)
                df1=df.drop(pin)
                writer = pandas.ExcelWriter('usuarios.xlsx', engine=None)
                df1.to_excel(writer, sheet_name='Sheet1')
                writer.save()
                messagebox.showinfo("Dar Salida a Usuario", "Usuario Borrado Exitosamente, Tiempo de usuario: "+ delta)
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
        files=os.listdir('./')
        pin=self.entry1.get()
        pin=str(pin)

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

class PinEmpleado(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller=controller
        label = tk.Label(self,text="Ingresar Pin",font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1=ttk.Button(self,text="Back Home",
                command=lambda:self.volver(controller))
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
        files=os.listdir('./')
        pin=self.entry_pin.get()
        pin=str(pin)
        if 'pinempleados.xlsx' in files:
            df=pandas.read_excel('pinempleados.xlsx')

            try:
                df.loc[pin]
                self.text1.delete('1.0',END)
                self.text1.insert(END,"Este Pin Ya Existe")


            except KeyError:
                print("Pin Valido")
                self.v=str(pin)
                self.entry_pin.delete('0',END)
                self.text1.delete('1.0',END)
                controller.show_frame(IngresarEmpleado)
        else:
            print("Pin Valido")
            self.v=str(pin)
            self.entry_pin.delete('0',END)
            self.text1.delete('1.0',END)
            controller.show_frame(IngresarEmpleado)

    def volver(self, controller):
        self.text1.delete('1.0',END)
        self.entry_pin.delete('0',END)
        controller.show_frame(StartPage)

class IngresarEmpleado(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller=controller
        label = tk.Label(self,text="Ingresar Empleado",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1=ttk.Button(self,text="Back to Home",
                command=lambda:controller.show_frame(StartPage))
        button1.pack()
        label1 = tk.Label(self,text="Nombre",font=LARGE_FONT)
        label1.pack(pady=10,padx=10)
        self.entry1=tk.Entry(self)
        self.entry1.pack()
        label2 = tk.Label(self,text="Cedula",font=LARGE_FONT)
        label2.pack(pady=10,padx=10)
        self.entry2=tk.Entry(self)
        self.entry2.pack()
        label3 = tk.Label(self,text="Telefono",font=LARGE_FONT)
        label3.pack(pady=10,padx=10)
        self.entry3=tk.Entry(self)
        self.entry3.pack()
        button2=ttk.Button(self,text="Ingresar", command=lambda:self.ingresar_empleado(controller))
        button2.pack()
        self.text1=tk.Text(self,height=1,width=40)
        self.text1.pack()
    def ingresar_empleado(self, controller):
        files = os.listdir('./')
        pagePin=self.controller.get_page(PinEmpleado)
        pin=pagePin.v
        pin=str(pin)
        nombre=self.entry1.get()
        cedula=self.entry2.get()
        telefono=self.entry3.get()
        cedula=int(cedula)
        if 'empleados.xlsx' in files:
            em=pandas.read_excel('empleados.xlsx')
            try :
                empleado=em.loc[cedula]
                self.text1.insert(END,"Ya existe un usuario con esta cedula : "+empleado[0]+", con CC: "+ empleado[2])
                self.entry1.delete('0',END)
                self.entry2.delete('0',END)
                self.entry3.delete('0',END)


            except KeyError:
                pn= pandas.read_excel('pinempleados.xlsx')
                em_t=em.T
                em_t[cedula]=[nombre,telefono]
                em=em_t.T
                writer = pandas.ExcelWriter('empleados.xlsx', engine=None)
                em.to_excel(writer, sheet_name='Sheet1')
                writer.save()
                pn_t=pn.T
                pn_t[pin]=[nombre,telefono,cedula]
                pn=pn_t.T
                writer = pandas.ExcelWriter('pinempleados.xlsx', engine=None)
                pn.to_excel(writer, sheet_name='Sheet1')
                writer.save()
                messagebox.showinfo("Ingresar Empleado", "Empleado Ingresado Exitosamente")
                self.entry1.delete('0',END)
                self.entry2.delete('0',END)
                self.entry3.delete('0',END)
                controller.show_frame(StartPage)
        else:
            em = pandas.DataFrame({cedula: [nombre,telefono]})
            em=em.T
            writer = pandas.ExcelWriter('empleados.xlsx', engine=None)
            em.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            pn = pandas.DataFrame({pin: [nombre,telefono,cedula]})
            pn=pn.T
            writer = pandas.ExcelWriter('pinempleados.xlsx', engine=None)
            pn.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            messagebox.showinfo("Ingresar Empleado", "Empleado Ingresado Exitosamente")
            self.entry1.delete('0',END)
            self.entry2.delete('0',END)
            self.entry3.delete('0',END)
            controller.show_frame(StartPage)

class BorrarEmpleado(tk.Frame):



    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        def get_selected_row(event):
            index=self.lista.curselection()
            print(index[0])
            self.v=index[0]
            return(index[0])
        label = tk.Label(self,text="Borrar Empleado",font=LARGE_FONT)
        label.grid(row=0,column=1)
        button1=ttk.Button(self,text="Back to Home",
                command=lambda:self.volver(controller))
        button1.grid(row=0,column=0)
        self.entry_id = StringVar()
        self.entry1=tk.Entry(self,textvariable=self.entry_id)
        self.entry1.grid(row=1,column=1)
        button3=ttk.Button(self,text="Dar Salida",
                command=lambda:self.borrar_pin(controller))
        button3.grid(row=2,column=1)
        self.text1=tk.Text(self,height=1,width=20)
        self.text1.grid(row=3,column=1)
        self.lista=Listbox(self, height=6, width=35)
        self.lista.grid(row=4,column=1)
        self.sb1=Scrollbar(self)
        self.sb1.grid(row=4,column=2)
        self.lista.configure(yscrollcommand=self.sb1.set)
        self.sb1.configure(command=self.lista.yview)
        self.lista.bind('<<ListboxSelect>>',get_selected_row)
        button1=ttk.Button(self,text="llenar", command=lambda:self.llenar(controller))
        button1.grid(row=5,column=1)
        button1=ttk.Button(self,text="borrar", command=lambda:self.borrar(controller))
        button1.grid(row=6,column=1)


    def get_selected_row(self,event):
        index=self.lista.curselection()
        return(index[0])
    def borrar(self,controller):
        df=pandas.read_excel('empleados.xlsx')
        df_t=df.T
        d=df_t.columns
        print(self.v)
        row=int(self.v)-1

        em=df.iloc[row]


        el=d[row]
        df1=df.drop(d[row])
        df1_t=df1.T
        d=df1_t.columns
        a=len(d)
        b=0
        self.lista.delete('0',END)
        texto=str('Cedula    Nombre    Telefono')
        self.lista.insert(END,texto)
        while(b<a):
            em=df1.iloc[b]
            texto=str(d[b])+'    '+str(em[0])+'    '+str(em[1])
            self.lista.insert(END,texto)
            b=b+1


    def borrar_pin(self, controller):
        files=os.listdir('./')
        pin=self.entry1.get()
        pin=str(pin)

        if 'pinempleados.xlsx' in files:
            try:
                df=pandas.read_excel('pinempleados.xlsx')
                dfe=pandas.read_excel('empleados.xlsx')
                ce=df.loc[pin]
                cedula=ce[2]
                cedula=int(cedula)
                em=dfe.loc[cedula]
                dfe1=dfe.drop(cedula)
                df1=df.drop(pin)
                writer = pandas.ExcelWriter('pinempleados.xlsx', engine=None)
                df1.to_excel(writer, sheet_name='Sheet1')
                writer.save()
                writer = pandas.ExcelWriter('empleados.xlsx', engine=None)
                dfe1.to_excel(writer, sheet_name='Sheet1')
                writer.save()
                messagebox.showinfo("Borrar Empleado", "El empleado: "+ce[0]+", Ha sido borrado exitosamente")
                self.entry1.delete('0',END)
                controller.show_frame(StartPage)
            except KeyError:
                print("Este pin no existe")
                self.text1.delete('1.0',END)
                self.text1.insert(END,'este pin no existe')

        else:
            print("este pin no existe")
            self.text1.delete('1.0',END)
            self.text1.insert(END,'este pin no existe')
            self.entry1.delete('0',END)

    def volver(self, controller):
        self.text1.delete('1.0',END)
        self.entry1.delete('0',END)
        controller.show_frame(StartPage)

    def llenar(self, controller):
        df=pandas.read_excel('empleados.xlsx')
        df_t=df.T
        d=df_t.columns
        a=len(d)
        b=0
        self.lista.delete('0',END)
        texto=str('Cedula    Nombre    Telefono')
        self.lista.insert(END,texto)
        while(b<a):
            em=df.iloc[b]
            texto=str(d[b])+'    '+str(em[0])+'    '+str(em[1])
            self.lista.insert(END,texto)
            b=b+1


app=ventanas()
app.geometry("720x320")
app.mainloop()
