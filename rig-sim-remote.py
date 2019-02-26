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
    status = ser.readline()
    if len(status)>0:
        print(
            "Transmission received: %s\n" % status +
            "Status: %s\n" % status[0] +
            "Measured depth: %f\n" % int.from_bytes(status[1:4], 'big') +
            "Bit depth: %f\n" % int.from_bytes(status[4:7], 'big') +
            "Rate of penetration: %f\n" % status[7] +
            "Standpipe pressure: %f\n" % int.from_bytes(status[8:10], 'big') +
            "Mud volume: %f\n" % int.from_bytes(status[10:12], 'big') +
            "Trip tank volume: %f\n" % int.from_bytes(status[12:14], 'big') +
            "RPM: %f\n" % status[14] +
            "Torque: %f\n" % int.from_bytes(status[15:17], 'big')
        )
