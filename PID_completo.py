import sys
import RPi.GPIO as GPIO
import read_temp_double
import i2c
from time import *


# Aquisição da temperatura
temp = read_temp_double.read_temp()
t1 = float(str(temp[0]))


# Variaveis Inteiras

angle = [0,10,20,110,70,170,30,120]

temp_ref = 24

# Variaveis float e double
kp = 2.0
ki = 0.001
kd = 1000
P = 0
I = 0
D = 0
PID = 0
lastemp = 0
lastprocess = 0
erro = 0
lasterro = 0
slaveAddr = 0x0e

while True:
    temp = read_temp_double.read_temp()
    temperatura = float(str(temp[0]))
    print("temperatura:", temperatura)
#    sleep(300)
    while(temperatura <= 24):
        temp = read_temp_double.read_temp()
        temperatura = float(str(temp[0]))

        # Implementacao PID
        erro = temp_ref - temperatura
        print("erro: ", erro)
        # deltatime = (millis() - lastprocess)/1000.0
        # lastprocess = millis()

        P = erro * kp
        print("P:", P)

        I += (erro * ki)  # deltatime
        print("I: ", I)

        D = ((erro - lasterro) * kd)  # deltatime
        print("D: ", D)

        lastemp = temperatura
        print("LAST TEMP: ", lastemp)
        temperatura = 0

        PID = P + I + D
        print("PID: ", PID)

        if PID < 1:
            pot = angle[7]
            i2c.returnAngle(pot,slaveAddr)
            print("Valor de ângulo (potência): ", pot)
        elif PID < 3460:
            pot = angle[6]
            i2c.returnAngle(pot, slaveAddr)
            print("Valor de ângulo (potência): ", pot)
        elif PID < 6900:
            pot = angle[5]
            i2c.returnAngle(pot,slaveAddr)
            print("Valor de ângulo (potência): ", pot)
        elif PID < 10350:
            pot = angle[4]
            i2c.returnAngle(pot,slaveAddr)
            print("Valor de ângulo (potência): ", pot)
        elif PID < 13800:
            pot = angle[3]
            i2c.returnAngle(pot,slaveAddr)
            print("Valor de ângulo (potência): ", pot)
        elif PID < 17250:
            pot = angle[2]
            i2c.returnAngle(pot,slaveAddr)
            print("Valor de ângulo (potência): ", pot)
        elif PID < 20700:
            pot = angle[1]
            i2c.returnAngle(pot,slaveAddr)
            print("Valor de ângulo (potência): ", pot)
        elif PID < 24100:
            pot = angle[0]
            i2c.returnAngle(pot,slaveAddr)
            print("Valor de ângulo (potência): ", pot)
print("Temperatura acima do setpoint")
