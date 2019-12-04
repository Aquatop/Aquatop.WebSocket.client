import wiringpi
from smbus2 import SMBus
from time import sleep
# import read_temp_double
import socketio

LED = 5
bomba2 = 1
wiringpi.wiringPiSetup()
wiringpi.pinMode(bomba2, wiringpi.OUTPUT)
wiringpi.digitalWrite(bomba2, 1)

INPUT = {
    1: 'temperature',
    2: 'ph',
    3: 'waterLevel',
    4: 'LUMINOSIDADE: ',
    9: 'TROCA DE AGUA: '
}


def returnAngle(pot, slaveAddr):
    response = 0
    bus = SMBus(1)
    bus.write_byte(slaveAddr, pot)
    print('Alice usando lolo - ', pot)
    sleep(0.2)
    response = bus.read_byte(slaveAddr)
    print(response)


def turnOnLights():
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(LED, wiringpi.OUTPUT)
    wiringpi.digitalWrite(LED, 1)


def turnOffLights():
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(LED, wiringpi.OUTPUT)
    wiringpi.digitalWrite(LED, 0)


def monitoring(slave_addr, aquarium, RESPONSE):
    print("entrou")

    response = {}

    bus = SMBus(1)

    for i in range(2, 4):
        bus.write_byte(slave_addr, i)
        sleep(0.1)
        response[INPUT[i]] = bus.read_byte(slave_addr)
        sleep(0.1)

    # temp = read_temp_double.read_temp()
    # response[INPUT[1]] = float(str(temp[aquarium]))
    
    response[INPUT[1]] = 25.5

    bus.close()

    print(response)

    RESPONSE['body'] = response

    sio = socketio.Client()
    sio.connect('http://104.248.58.252:80',
                socketio_path='/websocket-server', namespaces=['/monitoring'])

    @sio.on('connect', namespace='/monitoring')
    def monitoring_connect():
        sio.emit('RESPOND_REPORT', RESPONSE, namespace='/monitoring')
        print('Enviou: ', RESPONSE)
        sio.disconnect()
    
    sio.wait()


def change_water(slave_addr):
    user_input = 9
    payload = 3
    response = 0
    other_response = 0
    bomba2 = 1

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
        while(count < 10):
            try:
				bus.write_byte(slave_addr, payload)
				sleep(0.5)
				other_response = bus.read_byte(slave_addr)
            except:
				other_response = 0
            
            print(other_response, ' - ', count)
            sleep(0.5)

            if(other_response > 17):
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

        count = 0
        while(count < 10):
			try:
				bus.write_byte(slave_addr, payload)
				sleep(0.5)
				other_response = bus.read_byte(slave_addr)
            except:
				other_response = 0
            
            print(other_response, ' - ', count)
            sleep(0.5)

            if(other_response < 17):
                count += 1
            else:
                count = 0

        payload = 11
        wiringpi.digitalWrite(bomba2, 1)

        bus.write_byte(slave_addr, payload)
        sleep(0.5)

    bus.close()

# change_water(0xf)

