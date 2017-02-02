import json
import requests
import radar
# from timeit import timeit


def receipt_json(secuencia, fecha):
    return {
        "apikey": "0494fed41bfd4ccb9f6f076dfd6fcf23",
        "livemode": False,
        "ambiente": 2,
        "tipo_emision": 1,
        "type": "receipt",
        "pagos": [{
            "medio": "cash",
            "total": 1.00
        }],
        # "22-11-2016",
        "fecha": fecha,
        "guiaremision": None,
        "codigoestablecimiento": "001",
        "codigopuntoventa": "033",
        "secuencia": secuencia,
        "cliente": {
            "tipoidentificacion": "RUC",
            "identificacion": "1050320-1",
            "razonsocial": "Datil",
            "correo": "w@datil.co",
            "direccion": "Carrera 10 Calle 1",
            "telefono": "5712222"
        },
        "items": [{
            "cantidad": 1,
            "codigoprincipal": "ABC",
            "codigoauxiliar": "123",
            "nombre": "Apple",
            "precio": 1.00,
            "descuento": 0.0,
            "codigoiva": 2,
            "codigoice": None,
            "precio_total_sin_impuestos": 0.88,
            "importe_total": 1.00,
            "unidad_medida": "units",
            "impuestos": [{
                "codigo_porcentaje": "2",
                "base_imponible": 0.88,
                "codigo": "2",
                "valor": 0.12,
                "tarifa": 0.12
            }],
            "detalle_adicional": [{
                "descripcion": "Magenta",
                "nombre": "color"
            }, {
                "descripcion": "M",
                "nombre": "size"
            }]
        }],
        "propina": 0.0,
        "informacion_adicional": {
            "Contract Number": "420420"
        },
        "total_impuestos": [{
            "base_imponible": 0.88,
            "codigo": "2",
            "codigo_porcentaje": "2",
            "valor": 0.12
        }],
        "total_sin_impuestos": 0.88,
        "total_descuento": 0.0,
        "importe_total": 1.00
    }


def issue_invoices(n, secuencia=10000):
    print("tiempo estimado: {} s".format(n*11.093875885))
    headers = {'Content-type': 'application/json',
               'Accept': 'application/json'}
    url = 'http://localhost:8000/api/facturar'
    for i in xrange(n):
        # fecha = radar.random_datetime(
        #     start='2017-01-01', stop='2017-01-30').date().strftime('%d-%m-%Y')
        fecha = "02-02-2017"
        invoice = receipt_json(str(secuencia), fecha)
        a = requests.post(url, data=json.dumps(invoice), headers=headers)
        message = "\033[94m" + "\n" + str(fecha) + \
                  " \033[94m" + "secuencia:" + str(secuencia) + \
                  " \033[94m" + str(a)+"\033[0m"
        print(message)
        secuencia += 1
    print("Finalizado.")


def issue_invoice_timed():
    headers = {'Content-type': 'application/json',
               'Accept': 'application/json'}
    url = 'http://localhost:8000/api/facturar'
    fecha = radar.random_datetime(
        start='2017-01-01', stop='2017-01-30').date().strftime('%d-%m-%Y')
    invoice = receipt_json("2033", fecha)
    a = requests.post(url, data=json.dumps(invoice), headers=headers)
    print("\033[94m"+fecha, "\033[94m"+"2033", "\033[94m"+repr(a))
    print("Finalizado.")


n = raw_input("\033[1m"+"cantidad de facturas a generar: ")
sec = raw_input("\033[1m"+"empezar desde secuencia: ")
if sec == '':
    sec = 10000
print("\033[0m")
issue_invoices(int(n), int(sec))

# print(timeit(issue_invoice_timed, number=1))
