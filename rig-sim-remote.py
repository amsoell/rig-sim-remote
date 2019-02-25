import serial
import configparser


config = configparser.ConfigParser()
config.read('rig-sim.ini')

serial_port = '/dev/ttyS0'
baud_rate = 9600
if 'Hardware' in config:
    config_hardware = config['Hardware']
    serial_port = config_hardware.get('serial_port', serial_port)
    baud_rate = config_hardware.get('baud_rate', baud_rate)

ser = serial.Serial(
    port=serial_port,
    baudrate=baud_rate,
    parity=serial.PARITY_NONE,
    bytesize=serial.EIGHTBITS,
    timeout=1,
)

print("Waiting for status")
while True:
    status=ser.readline()
    if len(status)>0:
        print(
            "Transmission received: %s\n" % status +
            "Status: %s\n" % status[0] +
            "Measured depth: %f\n" % status[1] + 
            "Total vertical depth: %f\n" % status[2] + 
            "Bit depth: %f" % status[3]
        )
