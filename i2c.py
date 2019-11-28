import wiringpi
from smbus2 import SMBus
from time import sleep
import read_temp_double

LED = 5

INPUT = {
    1: 'temperature',
    2: 'ph',
    3: 'waterLevel',
    4: 'LUMINOSIDADE: ',
    9: 'TROCA DE AGUA: '
}


def returnAngle(pot,slaveAddr):
    response = 0
    bus = SMBus(1)
    bus.write_byte(slaveAddr,pot)
    print('Alice usando lolo - ',pot)
    sleep(0.2)
    response = bus.read_byte(slaveAddr)
    print(response)
    
    
def turnOnLights():
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(LED, wiringpi.OUTPUT)
    wiringpi.digitalWrite(LED,1)

def turnOffLights():
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(LED, wiringpi.OUTPUT)
    wiringpi.digitalWrite(LED,0)

def monitoring(slave_addr, aquarium, sio, RESPONSE):
    response = {}

    bus = SMBus(1)

    for i in range(2, 4):
        bus.write_byte(slave_addr, i)
        sleep(0.1)
        response[INPUT[i]] = bus.read_byte(slave_addr)
        sleep(0.1)

    read_temp_double.read_temp()
    response[INPUT[1]] = float(str(temp[aquarium])

    bus.close()
    
    RESPONSE['body'] = response

    sio.emit('RESPOND_REPORT', RESPONSE, namespace='/monitoring')


def change_water(slave_addr):
    user_input = 9
    payload = 3
    response = 0
    other_response = 0
    bomba2 = 0

    bus = SMBus(1)
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(bomba2, wiringpi.OUTPUT)

    bus.write_byte(slave_addr, user_input)
    sleep(0.5)
    response = bus.read_byte(slave_addr)
    sleep(0.5)

    if(response == 10):
        #payload = 3

        bus.write_byte(slave_addr, payload)
        sleep(0.5)
        other_response = bus.read_byte(slave_addr)
        sleep(0.5)
         
        count = 0
        while(count < 4):
            bus.write_byte(slave_addr, payload)
            sleep(0.5)
            other_response = bus.read_byte(slave_addr)
            print(other_response, ' - ', count)
            sleep(0.5)
            
            if(other_response > 12):
                count += 1
            else:
                count = 0

        payload = 10

        bus.write_byte(slave_addr, payload)
        sleep(0.5)

        payload = 3
        wiringpi.digitalWrite(bomba2, 0)

        bus.write_byte(slave_addr, payload)
        sleep(0.5)
        other_response = bus.read_byte(slave_addr)

        while(other_response > 8):
            bus.write_byte(slave_addr, payload)
            sleep(0.5)
            other_response = bus.read_byte(slave_addr)
            print(other_response)
            sleep(0.5)

        payload = 11
        wiringpi.digitalWrite(bomba2, 1)

        bus.write_byte(slave_addr, payload)
        sleep(0.5)

    bus.close()
