# from w1thermsensor import W1ThermSensor
from rq import use_connection, Queue
from time import sleep
import socketio
import I2C_LCD_driver
import al
import i2c
import read_temp_double

lcdi2c1 = I2C_LCD_driver.lcd(0x23)
lcdi2c2 = I2C_LCD_driver.lcd(0x27)
# sensor = W1ThermSensor()

AQUARIO_1 = 'AQUARIO_1'
AQUARIO_2 = 'AQUARIO_2'

RESPONSE = {
    'params': {'name': AQUARIO_1},
    'body':  {
        'ph': '0',
        'waterLevel': 0,
        'temperature': '0°C',
    }
}
RESPONSE2 = {
    'params': {'name': AQUARIO_2},
    'body':  {
        'ph': '0',
        'waterLevel': 0,
        'temperature': '0°C',
    }
}

slave_addr = 0x0F
slave2_addr = 0xE


def set_lcd_info():
    temp = read_temp_double.read_temp()
    tem_aqua1 = str(temp[1])
    tem_aqua2 = str(temp[0])

    lcdi2c1.lcd_clear()
    lcdi2c1.lcd_display_string(AQUARIO_1, 1, 0)
    lcdi2c1.lcd_display_string(tem_aqua1, 2, 0)

    lcdi2c2.lcd_clear()
    lcdi2c2.lcd_display_string(AQUARIO_2, 1, 0)
    lcdi2c2.lcd_display_string(tem_aqua2, 2, 0)


use_connection()
queue = Queue()

sio = socketio.Client()


@sio.on('connect', namespace='/scheduling')
def scheduling_connect():
    sio.emit('CLIENT_INFO', RESPONSE, namespace="/scheduling")
    sio.emit('CLIENT_INFO', RESPONSE2, namespace="/scheduling")
    print('Conectado ao scheduling')


@sio.on('REQUEST_FEED_FISHES', namespace='/aquarium')
def feed_fishes(data):
    if(AQUARIO_1 == data['aquarium']):
        queue.enqueue(al.feed_fishes, 1)
        print('FEEDIND FISHES AQUARIO 1')

    elif(AQUARIO_2 == data['aquarium']):
        queue.enqueue(al.feed_fishes, 2)
        print('FEEDIND FISHES AQUARIO 2')


@sio.on('REQUEST_FEED_FISHES', namespace='/scheduling')
def feed_fishes(data):
    if(AQUARIO_1 == data['aquarium']):
        queue.enqueue(al.feed_fishes, 1)
        print('FEEDIND FISHES AQUARIO 1')

    elif(AQUARIO_2 == data['aquarium']):
        queue.enqueue(al.feed_fishes, 2)
        print('FEEDIND FISHES AQUARIO 2')


@sio.on('REQUEST_SWAP_WATER', namespace='/aquarium')
def swap_water(data):
    if(AQUARIO_1 == data['aquarium']):
        queue.enqueue_call(func=i2c.change_water, args=(slave_addr,), timeout=900)
        print('SWAPPING WATER AQUARIO 1')

    elif(AQUARIO_2 == data['aquarium']):
        queue.enqueue_call(func=i2c.change_water, args=(slave2_addr,), timeout=900)
        print('SWAPPING WATER AQUARIO 2')


@sio.on('REQUEST_SWAP_WATER', namespace='/scheduling')
def swap_water(data):
    if(AQUARIO_1 == data['aquarium']):
        queue.enqueue(i2c.change_water, slave_addr)
        print('SWAPPING WATER AQUARIO 1')

    elif(AQUARIO_2 == data['aquarium']):
        queue.enqueue(i2c.change_water, slave2_addr)
        print('SWAPPING WATER AQUARIO 2')


@sio.on('REQUEST_TURN_ON_LIGHTS', namespace='/aquarium')
def turn_on_lights(data):
    if(AQUARIO_1 == data['aquarium'] or AQUARIO_2 == data['aquarium']):
        queue.enqueue(i2c.turnOnLights)
        print('TURNING ON LIGHTS')


@sio.on('REQUEST_TURN_ON_LIGHTS', namespace='/scheduling')
def turn_on_lights(data):
    if(AQUARIO_1 == data['aquarium'] or AQUARIO_2 == data['aquarium']):
        queue.enqueue(i2c.turnOnLights)
        print('TURNING ON LIGHTS')


@sio.on('REQUEST_TURN_OFF_LIGHTS', namespace='/aquarium')
def turn_off_lights(data):
    if(AQUARIO_1 == data['aquarium'] or AQUARIO_2 == data['aquarium']):
        queue.enqueue(i2c.turnOffLights)
        print('TURNING OFF LIGHTS')


@sio.on('REQUEST_TURN_OFF_LIGHTS', namespace='/scheduling')
def turn_off_lights(data):
    if(AQUARIO_1 == data['aquarium'] or AQUARIO_2 == data['aquarium']):
        queue.enqueue(i2c.turnOffLights)
        print('TURNING OFF LIGHTS')


@sio.on('connect', namespace='/aquarium')
def aquarium_connect():
    sio.emit('CLIENT_INFO', RESPONSE, namespace="/aquarium")
    sio.emit('CLIENT_INFO', RESPONSE2, namespace="/aquarium")
    print('Conectado ao aquarium')


@sio.on('DISPLAY_PIN', namespace='/aquarium')
def display_pin(data):
    dict(data)
    pin = "PIN: " + data['pin']
    print(pin)
    if(AQUARIO_1 == data['aquarium']):
        lcdi2c1.lcd_clear()
        lcdi2c1.lcd_display_string(AQUARIO_1, 1, 0)
        lcdi2c1.lcd_display_string(pin, 2, 0)
        sleep(20)
        set_lcd_info()
    if(AQUARIO_2 == data['aquarium']):
        lcdi2c2.lcd_clear()
        lcdi2c2.lcd_display_string(AQUARIO_2, 1, 0)
        lcdi2c2.lcd_display_string(pin, 2, 0)
        sleep(20)
        set_lcd_info()


@sio.on('connect', namespace='/monitoring')
def monitoring_connect():
    sio.emit('CLIENT_INFO', RESPONSE, namespace="/monitoring")
    sio.emit('CLIENT_INFO', RESPONSE2, namespace="/monitoring")
    print('Conectado ao monitoring')


@sio.on('REQUEST_REPORT', namespace='/monitoring')
def respond_report(data):
    print('Monitoramento solicitado')
    if(AQUARIO_1 == data['aquarium']):
        queue.enqueue(i2c.monitoring, slave_addr, 0, RESPONSE)

    elif(AQUARIO_2 == data['aquarium']):
        queue.enqueue(i2c.monitoring, slave2_addr, 1, RESPONSE2)


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://104.248.58.252:80', socketio_path='/websocket-server',
            namespaces=['/monitoring', '/aquarium', '/scheduling'])

set_lcd_info()

sio.wait()
