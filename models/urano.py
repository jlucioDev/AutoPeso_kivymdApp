from logging import raiseExceptions
import serial
import time
import random

class Urano:
    
    
    def __init__(self, porta, simulado):
        self.simular = simulado
        self.porta = porta
        try:
            # try:
            #     serial.Serial(self.porta, 9600).close()
            # except:
            #     pass
            if self.simular == False:
                self.ser = serial.Serial(self.porta, 9600, timeout=0.5, parity=serial.PARITY_NONE, rtscts=0)
            else:
                pass
        except serial.SerialException as e:
            print("Erro ao iniciar Porta Serial", e)
            #serial.Serial(self.porta, 9600).close()
            raiseExceptions("Erro ao iniciar Porta Serial", e)
            
    def capturaPeso(self):
        data = "0.00"
        
        try:
        
            # if not self.ser.is_open():
            if self.simular == False:
                try:
                    self.ser.open()
                except:
                    pass
                
                self.ser.write(b'\x04')
                time.sleep(0.5)
                data = self.ser.readline()
                data = str(data).split(" ")[23]
                self.ser.close()
            else:
                valor = round(random.uniform(0.150, 0.750), 3)
                data = f'DATA:  00/00/00 VALID.: 00/00/00      TARA:   0.000kg       PESO L:  {valor}kg      R$/kg:      0.00      TOTAL R$:      0.00200000000000'
                #data = f'DATA:  00/00/00 VALID.: 00/00/00      TARA:   0.000kg       PESO L:  0.266kg      R$/kg:      0.00      TOTAL R$:      0.00200000000000'
                data = str(data).split(" ")[23]
                
        except serial.SerialException as e:
            print("Erro ao enviar comando à balança.", e)
        
        finally:
            return data[0:5]

    def FecharPorta(self):
        try:
            if not self.simular:
                self.ser.close()
        except serial.SerialException as e:
            print("Erro ao fechar porta serial: ", e)