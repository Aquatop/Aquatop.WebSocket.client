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

if __name__ == "__main__":
    slave_addr = 0x0F
    user_input = 1
    payload = 0
    response = 0
    other_response = 0
    bomba2 = 7

    bus = SMBus(1)
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(bomba2, wiringpi.OUTPUT)

    while(user_input != 0):
        user_input = int(input('Qual ação deseja realizar? '))

        bus.write_byte_data(slave_addr, 0, user_input)
        sleep(1.5)
        response = bus.read_byte_data(slave_addr, 0)

        print(INPUT[user_input], response)

        if(user_input == 9):
            if(response == 10):
                payload = 3

                bus.write_byte_data(slave_addr, 0, payload)
                sleep(1.5)
                other_response = bus.read_byte_data(slave_addr, 0)

                while(other_response < 20):
                    bus.write_byte_data(slave_addr, 0, payload)
                    sleep(1.5)
                    other_response = bus.read_byte_data(slave_addr, 0)
                    sleep(1.5)

                payload = 10

                bus.write_byte_data(slave_addr, 0, payload)
                sleep(1.5)

                payload = 3
                wiringpi.digitalWrite(bomba2, 1)

                bus.write_byte_data(slave_addr, 0, payload)
                sleep(1.5)
                other_response = bus.read_byte_data(slave_addr, 0)

                while(other_response > 8):
                    bus.write_byte_data(slave_addr, 0, payload)
                    sleep(1.5)
                    other_response = bus.read_byte_data(slave_addr, 0)
                    sleep(1.5)

                payload = 11
                wiringpi.digitalWrite(bomba2, 0)

                bus.write_byte_data(slave_addr, 0, payload)
                sleep(1.5)

    bus.close()
