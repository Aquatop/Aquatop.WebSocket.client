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

PASSOS_POR_ROTACAO = 512

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


def alimentar(number_aqua):
    global conta
    conta = 0
    
    print("Entrou Alimentar: ", conta)
    
    flag = 0
    if(number_aqua == 1):
        print("Entrou if: ", conta)
        while(wiringpi.digitalRead(FDC1) != 0):
            sentidoHorario()
            conta += 1
            # print("Conta Alimentar: ", conta)
        while(conta >= 0):
            sentidoAntiHorario()
            conta -= 1
            if(flag == 0):
                flag = 1 
                print("AAAAAAAAAAAAAAAAA Alimentar: ", conta)
    elif(number_aqua == 2):
        while(wiringpi.digitalRead(FDC2) != 0):
            sentidoAntiHorario()
            conta += 1
        while(conta >= 0):
            sentidoHorario()
            conta -= 1


def fuso(number_aqua = 2):
    print("Entrou Fuso: ", conta)
    if number_aqua == 1:
        print("Entrou IF", conta)
        while(conta < 3 * PASSOS_POR_ROTACAO ):
            print("Conta Fuso: ", conta)
        while(conta >= 3 * PASSOS_POR_ROTACAO ):
            gira_fuso2()
            print("Conta Fuso: ", conta)
    else:
        while(conta > 0 and conta <= 2 * PASSOS_POR_ROTACAO):
            pass
        while(conta >= 2 * PASSOS_POR_ROTACAO and conta <= 4 * PASSOS_POR_ROTACAO):
            gira_fuso2()


def feed_fishes(number_aqua):
    wiringpi.wiringPiSetup()

    wiringpi.pinMode(FDC1, wiringpi.INPUT)
    wiringpi.pinMode(FDC2, wiringpi.INPUT)
    wiringpi.pullUpDnControl(FDC1, wiringpi.PUD_DOWN)
    wiringpi.pullUpDnControl(FDC2, wiringpi.PUD_DOWN)

    wiringpi.pinMode(IN1, wiringpi.OUTPUT)
    wiringpi.pinMode(IN2, wiringpi.OUTPUT)
    wiringpi.pinMode(IN3, wiringpi.OUTPUT)
    wiringpi.pinMode(IN4, wiringpi.OUTPUT)

    wiringpi.pinMode(FS11, wiringpi.OUTPUT)
    wiringpi.pinMode(FS12, wiringpi.OUTPUT)
    wiringpi.pinMode(FS13, wiringpi.OUTPUT)
    wiringpi.pinMode(FS14, wiringpi.OUTPUT)

    wiringpi.pinMode(FS21, wiringpi.OUTPUT)
    wiringpi.pinMode(FS22, wiringpi.OUTPUT)
    wiringpi.pinMode(FS23, wiringpi.OUTPUT)
    wiringpi.pinMode(FS24, wiringpi.OUTPUT)

    # global conta
    # conta = 0

    time.sleep(1)

    thread1 = threading.Thread(target=alimentar, args=[number_aqua])
    thread1.start()

    time.sleep(1)

    thread2 = threading.Thread(target=fuso, args=[number_aqua])
    thread2.start()

    thread1.join()

    print('Aquario alimentado: ', number_aqua)
