# --*-- coding: utf-8 --*--
import os
import pandas

def verificarPin(pin):
    a=0
    files=os.listdir('./')

    if 'PinUsuarios.xlsx' in files:
        df=pandas.read_excel('PinUsuarios.xlsx')
        try:
            fe=df.loc[pin]
            a=1
            return True

        except KeyError:
            pass

    if a==0 :
        if 'empleados.xlsx' in files:
            em=pandas.read_excel('empleados.xlsx')
            try:
                em=em.loc[pin]
                return True

            except KeyError:
                return False

        else:
            return False
'''
def cedula_siguiente(cedula,pin):
    a=0
    files=os.listdir('./')
    cedula=int(cedula)
    pin=str(pin)

    if 'PinUsuarios.xlsx' in files:
        us=pandas.read_excel('PinUsuarios.xlsx')

        us2=us.set_index('Cedula')
        print(us2.index)
        try:
            us2.loc[cedula]
            self.text1.delete('1.0',END)
            self.text1.insert(END,"Esta usuario ya tiene un Pin asignado")
            a=1

        except KeyError:
            print("Cedula valida")


    if 'usuarios.xlsx' in files:
        df=pandas.read_excel('usuarios.xlsx')
        us_t=df.T
        try:
            pn=df.loc[cedula]
            print(cedula)

            if a==0:
                self.entry_ced.delete('0',END)
                self.text1.delete('1.0',END)
                usuario=df.loc[cedula]

                usuario[2]=usuario[2]+1

                us_t[cedula]=[usuario[0],usuario[1],usuario[2]]
                us=us_t.T
                writer = pandas.ExcelWriter('usuarios.xlsx', engine=None)
                us.to_excel(writer, sheet_name='Sheet1')
                writer.save()
                fecha=datetime.now()
                hora=fecha.strftime("%H:%M")
                fecha=fecha.strftime("%Y-%m-%d")

                df = pandas.DataFrame({pin: [cedula]})
                df=df.T
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
                messagebox.showinfo("Ingresar Usuario", "El Usuario "+ usuario[0]
                                            +" Ha sido ingresado Exitosamente")
                controller.show_frame(StartPage)
            else:
                print("paila")

        except KeyError:
            print("Cedula Nueva")
            self.c=cedula
            self.entry_ced.delete('0',END)
            self.text1.delete('1.0',END)
            controller.show_frame(Entrada)
    else:
        print("Cedula Nueva")
        self.c=cedula
        self.entry_ced.delete('0',END)
        self.text1.delete('1.0',END)
        controller.show_frame(Entrada)
'''