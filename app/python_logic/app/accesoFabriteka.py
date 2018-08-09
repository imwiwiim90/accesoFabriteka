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
            print('nn')

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