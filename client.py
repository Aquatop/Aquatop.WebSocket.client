from w1thermsensor import W1ThermSensor
import socketio
import I2C_LCD_driver
import time
import al
import i2c
lcdi2c = I2C_LCD_driver.lcd()
sensor = W1ThermSensor()

AQUARIUM_NAME = 'AQUARIO_DU_LERMEN'
slave_addr = 0x0F
slave2_addr = 0xE

sio = socketio.Client()


@sio.on('connect', namespace='/scheduling')
def scheduling_connect():
    sio.emit('CLIENT_INFO', RESPONSE, namespace="/scheduling")


@sio.on('REQUEST_FEED_FISHES', namespace='/aquarium')
def feed_fishes(data):
    if(AQUARIUM_NAME == data['aquarium']):
        al.feed_fishes(1)
        print('FEEDIND FISHES')


@sio.on('REQUEST_FEED_FISHES', namespace='/scheduling')
def feed_fishes(data):
    if(AQUARIUM_NAME == data['aquarium']):
        print('FEEDIND FISHES')


@sio.on('REQUEST_SWAP_WATER', namespace='/aquarium')
def swap_water(data):
    if(AQUARIUM_NAME == data['aquarium']):
        i2c.change_water(slave2_addr)
        print('SWAPPING WATER')


@sio.on('REQUEST_SWAP_WATER', namespace='/scheduling')
def swap_water(data):
    if(AQUARIUM_NAME == data['aquarium']):
        print('SWAPPING WATER')


@sio.on('REQUEST_TURN_ON_LIGHTS', namespace='/aquarium')
def turn_on_lights(data):
    if(AQUARIUM_NAME == data['aquarium']):
        i2c.turnOnLights()
        print('TURNING ON LIGHTS')


@sio.on('REQUEST_TURN_ON_LIGHTS', namespace='/scheduling')
def turn_on_lights(data):
    if(AQUARIUM_NAME == data['aquarium']):
        print('TURNING ON LIGHTS')


@sio.on('REQUEST_TURN_OFF_LIGHTS', namespace='/aquarium')
def turn_off_lights(data):
    if(AQUARIUM_NAME == data['aquarium']):
        i2c.turnOffLights()
        print('TURNING OFF LIGHTS')


@sio.on('REQUEST_TURN_OFF_LIGHTS', namespace='/scheduling')
def turn_off_lights(data):
    if(AQUARIUM_NAME == data['aquarium']):
        print('TURNING OFF LIGHTS')

@sio.on('connect', namespace='/aquarium')
def aquarium_connect():
    sio.emit('CLIENT_INFO', RESPONSE, namespace="/aquarium")

@sio.on('DISPLAY_PIN', namespace='/aquarium')
def display_pin(data):
    if(AQUARIUM_NAME == data['aquarium']):
        lcdi2c.lcd_clear()
        lcdi2c.lcd_display_string("PIN: %d" % data['pin'], 1, 0)
        print('PIN: ', data['pin'])


@sio.on('connect', namespace='/monitoring')
def monitoring_connect():
    file = open('aquario1.txt', 'r')
    RESPONSE = {'params': {'name': AQUARIUM_NAME}}
    RESPONSE['body'] = eval(file.read())
    file.close()

    print(RESPONSE)

    sio.emit('CLIENT_INFO', RESPONSE, namespace="/monitoring")


@sio.on('REQUEST_REPORT', namespace='/monitoring')
def respond_report(data):
    if(AQUARIUM_NAME == data['aquarium']):
        RESPONSE = {'params': {'name': AQUARIUM_NAME}}
        RESPONSE['body'] = i2c.monitoring(slave2_addr)

        print(RESPONSE)

        sio.emit('RESPOND_REPORT', RESPONSE, namespace='/monitoring')


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://192.168.0.55:8080', socketio_path='/websocket-server',
            namespaces=['/monitoring', '/aquarium', '/scheduling'])
sio.wait()
