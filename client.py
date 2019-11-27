#from w1thermsensor import W1ThermSensor
import socketio
#import I2C_LCD_driver
import time
#import al
#import i2c
#lcdi2c = I2C_LCD_driver.lcd()
#sensor = W1ThermSensor() 

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

sio = socketio.Client()


@sio.on('connect', namespace='/scheduling')
def scheduling_connect():
    sio.emit('CLIENT_INFO', RESPONSE, namespace="/scheduling")
    sio.emit('CLIENT_INFO', RESPONSE2, namespace="/scheduling")
    print('Conectado ao scheduling')


@sio.on('REQUEST_FEED_FISHES', namespace='/aquarium')
def feed_fishes(data):
    if(AQUARIO_1 == data['aquarium']):
        al.feed_fishes(1)
        print('FEEDIND FISHES AQUARIO 1')
    
    elif(AQUARIO_2 == data['aquarium']):
        al.feed_fishes(2)
        print('FEEDIND FISHES AQUARIO 2')


@sio.on('REQUEST_FEED_FISHES', namespace='/scheduling')
def feed_fishes(data):
    if(AQUARIO_1 == data['aquarium']):
        al.feed_fishes(1)
        print('FEEDIND FISHES AQUARIO 1')
    
    elif(AQUARIO_2 == data['aquarium']):
        al.feed_fishes(2)
        print('FEEDIND FISHES AQUARIO 2')


@sio.on('REQUEST_SWAP_WATER', namespace='/aquarium')
def swap_water(data):
    if(AQUARIO_1 == data['aquarium']):
        i2c.change_water(slave_addr)
        print('SWAPPING WATER AQUARIO 1')
    
    elif(AQUARIO_2 == data['aquarium']):
        i2c.change_water(slave2_addr)
        print('SWAPPING WATER AQUARIO 2')


@sio.on('REQUEST_SWAP_WATER', namespace='/scheduling')
def swap_water(data):
    if(AQUARIO_1 == data['aquarium']):
        i2c.change_water(slave_addr)
        print('SWAPPING WATER AQUARIO 1')
    
    elif(AQUARIO_2 == data['aquarium']):
        i2c.change_water(slave2_addr)
        print('SWAPPING WATER AQUARIO 2')


@sio.on('REQUEST_TURN_ON_LIGHTS', namespace='/aquarium')
def turn_on_lights(data):
    if(AQUARIO_1 == data['aquarium'] or AQUARIO_2 == data['aquarium']):
        i2c.turnOnLights()
        print('TURNING ON LIGHTS')


@sio.on('REQUEST_TURN_ON_LIGHTS', namespace='/scheduling')
def turn_on_lights(data):
    if(AQUARIO_1 == data['aquarium'] or AQUARIO_2 == data['aquarium']):
        i2c.turnOnLights()
        print('TURNING ON LIGHTS')


@sio.on('REQUEST_TURN_OFF_LIGHTS', namespace='/aquarium')
def turn_off_lights(data):
    if(AQUARIO_1 == data['aquarium'] or AQUARIO_2 == data['aquarium']):
        i2c.turnOffLights()
        print('TURNING OFF LIGHTS')


@sio.on('REQUEST_TURN_OFF_LIGHTS', namespace='/scheduling')
def turn_off_lights(data):
    if(AQUARIO_1 == data['aquarium'] or AQUARIO_2 == data['aquarium']):
        i2c.turnOffLights()
        print('TURNING OFF LIGHTS')


@sio.on('connect', namespace='/aquarium')
def aquarium_connect():
    sio.emit('CLIENT_INFO', RESPONSE, namespace="/aquarium")
    sio.emit('CLIENT_INFO', RESPONSE2, namespace="/aquarium")
    print('Conectado ao aquarium')


@sio.on('DISPLAY_PIN', namespace='/aquarium')
def display_pin(data):
    if(AQUARIO_1 == data['aquarium']):
        print(data)
        pin = "PIN: " + data['pin']
        print(pin)
        lcdi2c.lcd_clear()
        lcdi2c.lcd_display_string(pin , 1, 0)
        print('PIN: ', data['pin'])


@sio.on('connect', namespace='/monitoring')
def monitoring_connect():
    sio.emit('CLIENT_INFO', RESPONSE, namespace="/monitoring")
    sio.emit('CLIENT_INFO', RESPONSE2, namespace="/monitoring")
    print('Conectado ao monitoring')


@sio.on('REQUEST_REPORT', namespace='/monitoring')
def respond_report(data):
    if(AQUARIO_1 == data['aquarium']):
        RESPONSE['body'] = i2c.monitoring(slave_addr)

        print(RESPONSE)

        sio.emit('RESPOND_REPORT', RESPONSE, namespace='/monitoring')  
    
    elif(AQUARIO_2 == data['aquarium']):
        RESPONSE2['body'] = i2c.monitoring(slave2_addr)

        print(RESPONSE2)

        sio.emit('RESPOND_REPORT', RESPONSE2, namespace='/monitoring')


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://localhost:8080', socketio_path='/websocket-server',
            namespaces=['/monitoring', '/aquarium', '/scheduling'])
sio.wait()
