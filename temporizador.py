'''
simple programa que ejecuta un temporizador

'''

import sys

from PyQt5 import uic, QtWidgets, QtCore
import uat_rc

qtCreatorFile = "menu.ui" # Nombre del archivo aquí.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #el código fuente va aquí

        # codigo para establecer limites de las horas
        self.sb_horas.setMaximum(12)
        self.sb_horas.setMinimum(0)
        self.sb_horas.setSingleStep(1)
        self.sb_horas.setValue(0)

        # codigo para establecer limites de los minutos
        self.sb_minutos.setMaximum(59)
        self.sb_minutos.setMinimum(0)
        self.sb_minutos.setSingleStep(1)
        self.sb_minutos.setValue(0)

        # codigo para establecer limites de los segundos
        self.sb_segundos.setMaximum(59)
        self.sb_segundos.setMinimum(0)
        self.sb_segundos.setSingleStep(1)
        self.sb_segundos.setValue(0)

        self.segundo = 0
        self.minuto = 0
        self.hora = 0

        self.lcdNumber.setDigitCount(8)
        self.lcdNumber.display("00:00:00")
        self.btn_iniciar.clicked.connect(self.establecer_temporizador)
        self.btn_pausa.clicked.connect(self.pausa)
        self.btn_reiniciar.clicked.connect(self.reiniciar)

        self.btn_reiniciar.setEnabled(False)

        self.tareaAsincrona = QtCore.QTimer()
        self.tareaAsincrona.timeout.connect(self.temporizador)

        self.btn_pausa.setEnabled(False)

    def reiniciar(self):
        self.tareaAsincrona.stop()
        self.establecer_temporizador()

    def pausa(self):
        texto= self.btn_pausa.text()

        if texto == "Pausa":
            self.tareaAsincrona.stop()
            self.btn_pausa.setText("continuar")
        else:
            self.tareaAsincrona.start(10)
            self.btn_pausa.setText("Pausa")

    def establecer_temporizador(self):
        self.segundo = self.sb_segundos.value()
        self.minuto = self.sb_minutos.value()
        self.hora = self.sb_horas.value()

        self.btn_pausa.setEnabled(True)
        self.btn_reiniciar.setEnabled(True)
        self.tareaAsincrona.start(10)

    def temporizador(self):
        '''
        cada iteracion / repeticion del tempo

            1.- decrementar en 1 los segundos
            2.- Si los segundos son -1 o segundos < 0 entonces:
	            decrementar en uno los minutos
	            segundos = 59
            3.- Si los minutos son -1:
	            decrementar en uno las horas
	            minutos = 59
            4.- Si las horas = -1 y todos los valores son 0:
	            detener timer
                :return:
        '''

        valorH = str(self.hora)

        if len(valorH) < 2:
            valorH = "0" + valorH

        valorM = str(self.minuto)

        if len(valorM) < 2:
            valorM = "0" + valorM

        valorS = str(self.segundo)

        if len(valorS) < 2:
            valorS = "0" + valorS

        valor = str(valorH) + ":" + str(valorM) + ":" + str(valorS)

        self.lcdNumber.display(valor)
        self.segundo -= 1

        if self.segundo == -1:
            self.segundo = 59
            self.minuto = self.minuto - 1

        if self.minuto == -1:
            self.minuto = 59
            self.hora = self.hora - 1

        if self.hora == -1:
            self.hora = 0
            self.minuto = 0
            self.segundo = 0
            self.tareaAsincrona.stop()
            self.btn_pausa.setEnabled(False)
            self.btn_reiniciar.setEnabled(False)

if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())