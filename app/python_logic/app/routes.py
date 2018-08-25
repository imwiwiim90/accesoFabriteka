# --*-- coding: utf-8 --*--

from app import app
from flask import request
from modules.accesoFabriteka import *
from modules.modulos import ModuloPuerta, ModuloEntrada
import urlparse
import json
from modules.Datos import *


functions = {
    'verificarPin' : verificarPin,
    'nuevoCliente' : ingresarNuevoCliente,
    'nuevoEmpleado' : ingresarEmpleado,
    'verificarCedulaCliente' : verificarCedulaCliente,
    'borrarEmpleado' : borrarEmpleado,
    'cambiarPinEmpleado' : cambiarEmpleado,
    'cambiarPinCliente' : cambiarCliente,
    'asignarPinCliente' : nuevoPinCliente,
    'desasignarPinCliente' : borrarPinCliente,
    'obtenerPorPin' : verificarPinAsignado,
    'verificarCedulaEmpleado' : verificarCedulaEmpleado,
    'entradasMensuales' : entradas_mensuales,
    'movimientosMes' : movimientos_mes,
    'movimientosDia' : movimientos_dia,
    'duracionConTarjeta' : duracion,
    'usuariosConTarjeta' : usuariosConTarjeta,
}

##### INIT #####

moduloPuerta = ModuloPuerta()
moduloPuerta.test = True
moduloPuerta.start()

moduloEntrada = ModuloEntrada()
moduloEntrada.test = True
moduloEntrada.start()

#################

@app.route('/verificarPin')
@app.route('/nuevoCliente')
@app.route('/verificarCedulaCliente')
@app.route('/nuevoEmpleado')
@app.route('/borrarEmpleado')
@app.route('/cambiarPinEmpleado')
@app.route('/cambiarPinCliente')
@app.route('/asignarPinCliente')
@app.route('/desasignarPinCliente')
@app.route('/obtenerPorPin')
@app.route('/verificarCedulaEmpleado')
@app.route('/entradasMensuales')
@app.route('/movimientosMes')
@app.route('/movimientosDia')
@app.route('/duracionConTarjeta')
@app.route('/usuariosConTarjeta')
def general_routes():
    try:
        query = urlparse.parse_qs(request.query_string)
        path = request.path.replace('/','')
        if 'data[]' in query:
            args = query['data[]']
            return json.dumps(functions[path](*args))
        else:
            return json.dumps(functions[path]())
    except:
        return None

@app.route('/clearModule')
def clearModule():
    print 'clear module'
    moduloEntrada.clear()
    return json.dumps(True)

@app.route('/getPin')
def getPin():
    pin = moduloEntrada.get()
    return json.dumps(pin)

@app.route('/logsInside')
def logsInside():
    query = urlparse.parse_qs(request.query_string)
    users = Usuarios()
    logs  = users.getLogsFromLastEntrance(*query['data[]'])
    return json.dumps(logs)

@app.route('/usersInside')
def usersInside():
    users = Usuarios()
    return json.dumps(users.getInside())




