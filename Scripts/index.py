import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from datetime import datetime
from PyQt5.QtGui import QFont as QF
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


class Principal(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.info = list()
        uic.loadUi("../Ventanas/principal.ui", self)
        self.bt_cedula.clicked.connect(self.informacion)
        self.bt_factura.clicked.connect(self.factura)

    def showEvent(self, event):
        fecha = datetime.now().strftime("%d-%m-%Y")
        self.lb_fecha.setText(fecha)
        self.lb_fecha.setFont(QF("Times", 10, QF.Bold))

    def informacion(self):
        path = 'D:\Independiente\Acueducto\Informacion\DATOS FACTURACION CORRALA P. ALTA.xlsx'
        inf = pd.read_excel(path, engine='openpyxl', sheet_name='CORRALA P. ALTA')
        cedula = self.ln_cedula.text()
        datos = inf[inf.Cc == int(cedula)]
        tam_datos = len(datos)
        print("tamaño de datos", tam_datos)
        print(datos['Cod. Suscriptor'])
        if tam_datos != 0:
            self.info.append(datos)
            for indice in datos['Cod. Suscriptor'].index:
                print(indice)
                self.tb_informacion.insertRow(0)
                nombre = datos['Suscriptor'][indice]
                nombre = QTableWidgetItem(nombre)
                codigo = QTableWidgetItem(datos['Cod. Suscriptor'][indice])
                factura = QTableWidgetItem(datos['Factura No'][indice])
                dir = QTableWidgetItem(datos['Direccion o vereda'][indice])
                tel = QTableWidgetItem(str(datos['Telefono'][indice]))
                pagar = '   $ ' + str(int(datos['TOTAL A PAGAR:'][indice]))
                pagar = QTableWidgetItem(pagar)
                self.tb_informacion.setItem(0, 0, nombre)
                self.tb_informacion.setItem(0, 1, codigo)
                self.tb_informacion.setItem(0, 2, factura)
                self.tb_informacion.setItem(0, 3, tel)
                self.tb_informacion.setItem(0, 4, dir)
                self.tb_informacion.setItem(0, 5, pagar)

        else:
            print("sin datos")

    def factura(self):
        cliente = self.info[0]
        for indice in cliente['Cod. Suscriptor'].index:
            w, h = A4  # Ancho y alto
            print("w= ", w)
            print("h= ", h)
            path = r'D:\Independiente\Acueducto\Facturas'
            path_img = r'D:\Independiente\Acueducto\img'
            nombre = '\prueba.pdf'
            img_logo = path_img + '\logo.png'
            img_super = path_img + '\super.png'

            path_abs = path + nombre
            c = canvas.Canvas(path_abs)  # Crear pdf en ruta especifica

            y = h - 20
            x = 20
            w_info = 365.2
            h_info = 198

            c.rect(x, y - h_info, w_info - x, h_info)  # Cuadro con la informacón de la empresa

            text = c.beginText(x + 10, y - 15)  # Posicion del texto
            text.setFont("Times-Roman", 10)  # Fuente del texto
            text.textLine("    ASOCIACION DE USUARIOS DEL ACUEDUCTO MULTIVEREDAL")
            text.textLine("             CORRALA, CORRALITA, Y CORRALA PARTE BAJA")
            c.drawText(text)

            text1 = c.beginText(x + 120, y - 36)
            text1.setFont("Times-Roman", 9)
            text1.textLine(" Nit: 811.020.040-2 ")
            c.drawText(text1)

            text2 = c.beginText(x + 60, y - 48)
            text2.setFont("Times-Roman", 9)
            text2.textLine("Carrera 50 No. 129 sur - 37, local 202, Caldas, tel: 306 46 52 32 ")
            c.drawText(text2)

            # -------- Dos imagenes, no factura, mes, fecha limite de pago
            xlist = [w_info, w_info + 110, w - 20]
            ylist = [y, y - 80, y - 120, y - 140, y - 170, y - h_info]
            c.grid(xlist, ylist)

            # Dos imagenes y texto de la primera imagen
            text3 = c.beginText(w_info + 5, y - 10)
            text3.setFont("Times-Roman", 8)
            text3.textLine("VIGILADA POR:")
            c.drawText(text3)

            c.drawImage(img_super, w_info + 10, y - 70, width=90, height=56)
            c.drawImage(img_logo, w_info + 115, y - 70, width=90, height=56)

            # String Factura No y su valor
            txt4 = c.beginText(w_info + 25, y - 103)
            txt4.setFont("Times-Roman", 11)
            texto = "Factura No                     " + str(cliente['Factura No'][indice])
            txt4.textLine(texto)
            c.drawText(txt4)

            # Mes
            text3 = c.beginText(w_info + 145, y - 133)
            text3.setFont("Times-Roman", 10)
            text3.textLine(cliente['Mes  facturado:'][indice])
            c.drawText(text3)

            # Fecha limite de pago
            text5 = c.beginText(w_info + 10, y - 160)
            text5.setFont("Times-Roman", 10)
            texto = "Fecha limite de pago         " + cliente['Fecha limite pago '][indice]
            text5.textLine(texto)
            c.drawText(text5)

            # -----------------------------------------------------------------
            ref_h = y - h_info
            # ---- Cod Suscripto, valor, string Servicio de Acueducto---------------------------
            xlist2 = [x, 139 + x, 139 + 70 + x, w - 20]
            ylist2 = [ref_h, ref_h - 20]
            c.grid(xlist2, ylist2)

            text6 = c.beginText(x + 10, ref_h - 13)
            text6.setFont("Times-Roman", 10)
            texto = "Cod. Suscriptor: " + 35 * " " + cliente['Cod. Suscriptor'][
                indice] + 65 * " " + "Servicio de Acueducto"
            text6.textLine(texto)
            c.drawText(text6)

            # -----------------------------------------------------------------

            # Suscriptor, cedula, direccion, telefono
            xlist3 = [x, x + 70]
            ylist3 = [ref_h - 20, ref_h - 50, ref_h - 70, ref_h - 90, ref_h - 110]
            c.grid(xlist3, ylist3)

            txt7 = c.beginText(x +10, ref_h - 40)
            txt7.setFont("Times-Roman", 10)
            texto = "Suscriptor " + 20*" " + cliente['Suscriptor'][indice]
            txt7.textLine(texto)
            c.drawText(txt7)

            # -----------------------------------------------------------------

            # nombre suscriptor
            c.rect(x + 70, ref_h - 50, -x + w_info - 70, 30)

            # lectura actual, lectura anterior, consumo mes
            xlist4 = [w_info, w_info + 110, w - 20]
            ylist4 = [ref_h - 20, ref_h - 50, ref_h - 70, ref_h - 90]
            c.grid(xlist4, ylist4)

            # numero cedula, no medidor, valor del medidor
            xlist5 = [x + 70, x + 147, w_info - 74, w_info]
            ylist5 = [ref_h - 50, ref_h - 70]
            c.grid(xlist5, ylist5)

            # valor de direccion
            c.rect(x + 70, ref_h - 90, w_info - 90, 20)

            # valor telefono, estrato
            xlist6 = [x + 70, w_info - 90, w_info]
            ylist6 = [ref_h - 90, ref_h - 110]
            c.grid(xlist6, ylist6)

            # cuadro vacio
            c.rect(w_info, ref_h - 110, 210, 20)

            c.drawImage(img_logo, 0, 0, width=72, height=50)
            c.drawImage(img_super, 500, 0, width=72, height=50)

            c.showPage()
            c.save()


"""

       # c.drawString(50, h - 50, "¡Hola pdf!") #copiar string
        x = 50
        y = h - 50
     #   c.line(x, y, x + 200, y)       # lineas
        c.rect(50, h - 300, 300, 200)  # Rectangulos
        text = c.beginText(50, h -50)   # Posicion del texto
        text.setFont("Times-Roman", 9)        # Fuente del texto
        text.textLine("ASOCIACION DE USUARIOS DEL ACUEDUCTO MULTIVEREDAL")
        text.textLine("CORRALA, CORRALITA, Y CORRALA PARTE BAJA")
       # c.drawText(text)
        img_logo = path_img + '\logo.png'
        img_super = path_img + '\super.png'

        #imagenes
#        c.drawImage(img_logo, 0, 0, width=72, height=72)
#        c.drawImage(img_super, 500, 0, width=72, height=72)

        #tablas
        xlist = [10, 20, 110, 160]
        ylist = [h- 10, h -60, h - 110, h - 160]
#        c.grid(xlist, ylist)
        c.showPage()"""

#       c.drawImage(img_logo, 0, 0, width=72, height=72)

if __name__ == "__main__":
    print("dentro")
    app = QApplication(sys.argv)
    principal = Principal()
    principal.show()
    app.exec_()
