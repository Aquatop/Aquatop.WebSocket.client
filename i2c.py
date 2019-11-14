import wiringpi
from smbus2 import SMBus
from time import sleep

INPUT = {
    1: 'PH: ',
    2: 'TEMPERATURA: ',
    3: 'NIVEL: ',
    4: 'LUMINOSIDADE: ',
    9: 'TROCA DE AGUA: '
}

AQUARIUM_NAME = 'AQUARIO_1'


def monitoring(slave_addr):
    response = {}

    bus = SMBus(1)

    for i in range(1, 4):
        bus.write_byte(slave_addr, i)
        sleep(0.1)
        response[INPUT[i]] = bus.read_byte(slave_addr)
        sleep(0.1)

    bus.close()

    print(response)

    return response


def change_water(slave_addr):
    user_input = 9
    payload = 0
    response = 0
    other_response = 0
    bomba2 = 7

    bus = SMBus(1)
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(bomba2, wiringpi.OUTPUT)

    bus.write_byte(slave_addr, user_input)
    sleep(0.2)
    response = bus.read_byte(slave_addr)

    if(response == 10):
        payload = 3

        bus.write_byte(slave_addr, payload)
        sleep(1)
        other_response = bus.read_byte(slave_addr)

        while(other_response < 20):
            bus.write_byte(slave_addr, payload)
            sleep(1)
            other_response = bus.read_byte(slave_addr)
            sleep(1)

        payload = 10

        bus.write_byte(slave_addr, payload)
        sleep(1)

        payload = 3
        wiringpi.digitalWrite(bomba2, 1)

        bus.write_byte(slave_addr, payload)
        sleep(1)
        other_response = bus.read_byte(slave_addr)

        while(other_response > 8):
            bus.write_byte(slave_addr, payload)
            sleep(1)
            other_response = bus.read_byte(slave_addr)
            sleep(1)

        payload = 11
        wiringpi.digitalWrite(bomba2, 0)

        bus.write_byte(slave_addr, payload)
        sleep(1)

    bus.close()


if __name__ == "__main__":
    slave_addr = 0x0F
    slave2_addr = 0xE

    # if(AQUARIUM_NAME == 'AQUARIO_1'):
    #     msp(slave_addr)
    # elif(AQUARIUM_NAME == 'AQUARIO_2'):
    #     msp(slave2_addr)
    # monitoring(slave2_addr)
    change_water(slave2_addr)
