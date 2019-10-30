import socketio

AQUARIUM_NAME = 'AQUARIO_DU_LERMEN'

# RESPONSE = {
#     'params': {'name': AQUARIUM_NAME},
#     'body': {
#         'ph': '9.9',
#         'waterLevel': '99%',
#         'temperature': '99°C',
#     }
# }
RESPONSE_2 = {
    'params': {'name': AQUARIUM_NAME},
    'body': {}
}


sio = socketio.Client()


@sio.on('connect', namespace='/scheduling')
def scheduling_connect():
    sio.emit('CLIENT_INFO', RESPONSE_2, namespace="/scheduling")


@sio.on('REQUEST_FEED_FISHES', namespace='/scheduling')
def feed_fishes(data):
    if(AQUARIUM_NAME == data['aquarium']):
        print('FEEDIND FISHES')


@sio.on('REQUEST_TURN_ON_LIGHTS', namespace='/scheduling')
def turn_on_lights(data):
    if(AQUARIUM_NAME == data['aquarium']):
        print('TURNING ON LIGHTS')


@sio.on('REQUEST_TURN_OFF_LIGHTS', namespace='/scheduling')
def turn_off_lights(data):
    if(AQUARIUM_NAME == data['aquarium']):
        print('TURNING OFF LIGHTS')


@sio.on('connect', namespace='/aquarium')
def aquarium_connect():
    sio.emit('CLIENT_INFO', RESPONSE_2, namespace="/aquarium")


@sio.on('DISPLAY_PIN', namespace='/aquarium')
def display_pin(data):
    if(AQUARIUM_NAME == data['aquarium']):
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
        file = open('aquario1.txt', 'r')
        RESPONSE = {'params': {'name': AQUARIUM_NAME}}
        RESPONSE['body'] = eval(file.read())
        file.close()

        print(RESPONSE)

        sio.emit('RESPOND_REPORT', RESPONSE, namespace='/monitoring')


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://localhost:8080', socketio_path='/websocket-server',
            namespaces=['/monitoring', '/aquarium', '/scheduling'])
sio.wait()
