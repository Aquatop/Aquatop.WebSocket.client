import wiringpi
import threading
import time

IN1 = 0
IN2 = 2
IN3 = 3
IN4 = 4

FS11 = 21
FS12 = 22
FS13 = 23
FS14 = 24

FS21 = 26
FS22 = 27
FS23 = 28
FS24 = 29

FDC1 = 6
FDC2 = 25

VEL_MOTOR = 1048
SEQUENCIA = [0x08, 0x0C, 0x04, 0x06, 0x02, 0x03, 0x01, 0x09]

conta = 0
number_aqua = 0
number_tip1 = 0
number_tip2 = 0
passosPorRotacao = 512


def sentidoHorario():
    for i in range(7, 0, -1):
        setOutput(i)
        time.sleep(VEL_MOTOR/1000000.0)


def sentidoAntiHorario():
    for i in range(0, 8, 1):
        setOutput(i)
        time.sleep(VEL_MOTOR/1000000.0)


def gira_fuso1():
    for i in range(7, 0, -1):
        setOutputFuso1(i)
        time.sleep(VEL_MOTOR/1000000.0)


def gira_fuso2():
    for i in range(7, 0, -1):
        setOutputFuso2(i)
        time.sleep(VEL_MOTOR/1000000.0)


def setOutput(out):
    var1 = ((SEQUENCIA[out]) & 0x01)
    var2 = ((SEQUENCIA[out] >> 1) & 0x01)
    var3 = ((SEQUENCIA[out] >> 2) & 0x01)
    var4 = ((SEQUENCIA[out] >> 3) & 0x01)

    wiringpi.digitalWrite(IN1, var1)
    wiringpi.digitalWrite(IN2, var2)
    wiringpi.digitalWrite(IN3, var3)
    wiringpi.digitalWrite(IN4, var4)


def setOutputFuso1(out):
    var1 = ((SEQUENCIA[out]) & 0x01)
    var2 = ((SEQUENCIA[out] >> 1) & 0x01)
    var3 = ((SEQUENCIA[out] >> 2) & 0x01)
    var4 = ((SEQUENCIA[out] >> 3) & 0x01)

    wiringpi.digitalWrite(FS11, var1)
    wiringpi.digitalWrite(FS12, var2)
    wiringpi.digitalWrite(FS13, var3)
    wiringpi.digitalWrite(FS14, var4)


def setOutputFuso2(out):
    var1 = ((SEQUENCIA[out]) & 0x01)
    var2 = ((SEQUENCIA[out] >> 1) & 0x01)
    var3 = ((SEQUENCIA[out] >> 2) & 0x01)
    var4 = ((SEQUENCIA[out] >> 3) & 0x01)

    wiringpi.digitalWrite(FS21, var1)
    wiringpi.digitalWrite(FS22, var2)
    wiringpi.digitalWrite(FS23, var3)
    wiringpi.digitalWrite(FS24, var4)


def alimentar():
    if(number_aqua == 1):
        while(wiringpi.digitalRead(FDC1) != 0):
            sentidoHorario()
            conta += 1
        while(conta >= 0):
            sentidoAntiHorario()
            conta -= 1
    elif(number_aqua == 2):
        while(wiringpi.digitalRead(FDC2) != 0):
            sentidoAntiHorario()
            conta += 1
        while(conta >= 0):
            sentidoHorario()
            conta -= 1
    elif(number_aqua == 3):
        while(wiringpi.digitalRead(FDC1) != 0):
            sentidoHorario()
            conta += 1
        while(conta >= 0):
            sentidoAntiHorario()
            conta -= 1
        while(wiringpi.digitalRead(FDC2) != 0):
            sentidoAntiHorario()
            conta += 1
        while(conta >= 0):
            sentidoHorario()
            conta -= 1


def fuso():
    if(number_tip1 == 1 and number_tip2 == 0):
        if(number_aqua == 1 or number_aqua == 2):
            while(conta > 0 and conta <= 2*passosPorRotacao):
                pass
            while(conta >= 2*passosPorRotacao and conta <= 4*passosPorRotacao):
                gira_fuso1()
    elif(number_tip1 == 2 and number_tip2 == 0):
        if(number_aqua == 1 or number_aqua == 2):
            while(conta > 0 and conta <= 2*passosPorRotacao):
                pass
            while(conta >= 2*passosPorRotacao and conta <= 4*passosPorRotacao):
                gira_fuso2()
    elif(number_aqua == 3):
        while(conta > 0 and conta <= 2*passosPorRotacao):
            pass
        while(conta >= 2*passosPorRotacao and conta <= 4*passosPorRotacao):
            if(number_tip1 == 1):
                gira_fuso1()
            if(number_tip1 == 2):
                gira_fuso2()
        while(conta != 0):
            pass
        time.sleep(1)
        while(conta > 0 and conta <= 2*passosPorRotacao):
            pass
        while(conta >= 2*passosPorRotacao and conta <= 4*passosPorRotacao):
            if(number_tip2 == 1):
                gira_fuso1()
            if(number_tip2 == 2):
                gira_fuso2()


if __name__ == "__main__":
    wiringpi.wiringPiSetup()

    wiringpi.pinMode(FDC1, INPUT)
    wiringpi.pinMode(FDC2, INPUT)
    wiringpi.pullUpDnControl(FDC1, PUD_DOWN)
    wiringpi.pullUpDnControl(FDC2, PUD_DOWN)

    wiringpi.pinMode(IN1, OUTPUT)
    wiringpi.pinMode(IN2, OUTPUT)
    wiringpi.pinMode(IN3, OUTPUT)
    wiringpi.pinMode(IN4, OUTPUT)

    wiringpi.pinMode(FS11, OUTPUT)
    wiringpi.pinMode(FS12, OUTPUT)
    wiringpi.pinMode(FS13, OUTPUT)
    wiringpi.pinMode(FS14, OUTPUT)

    wiringpi.pinMode(FS21, OUTPUT)
    wiringpi.pinMode(FS22, OUTPUT)
    wiringpi.pinMode(FS23, OUTPUT)
    wiringpi.pinMode(FS24, OUTPUT)

    number_aqua = int(input("Qual aquario alimentar 1, 2 ou os dois(3)? "))
    number_tip1 = int(input("Qual ração 1, 2 do aquario 1? "))

    if(number_aqua == 3):
        number_tip2 = int(input("Qual ração 1, 2 do aquario 2? "))

    thread1 = threading.Thread(target=alimentar)
    thread1.start()

    time.sleep(1)

    thread2 = threading.Thread(target=fuso)
    thread2.start()

    thread1.join()

    print('Aquario alimentado: ', number_aqua)
    print('Ração fornecida: ', number_tip1)
