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


def gira_fuso1():
    pass


def gira_fuso2():
    pass


def alimentar():
    print('Alimentando')


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
