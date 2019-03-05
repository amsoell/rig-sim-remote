import serial
import yaml
import errno
import sys


try:
    with open('rig-sim.yaml') as config_file:
        config = yaml.safe_load(config_file)
except (OSError, IOError) as exception:
    if getattr(exception, 'errno', 0) == errno.ENOENT:
        print("Configuration file not found")
        sys.exit()

try:
    ser = serial.Serial(
        port=config['hardware']['serial_port'],
        baudrate=config['hardware']['baud_rate'],
        parity=config['hardware']['parity'],
        bytesize=config['hardware']['bytesize'],
        timeout=1,
    ) if 'hardware' in config else None
except serial.serialutil.SerialException:
    print("Serial connection could not be established")
    sys.exit()

print("Waiting for status")
while True:
    status = ser.read(17)
    if len(status) > 0:
        print(
            "Transmission received: %s\n" % status +
            "Status: %s\n" % status[0] +
            "Measured depth: %f\n" % int.from_bytes(status[1:3], 'big') +
            "Bit depth: %f\n" % int.from_bytes(status[3:5], 'big') +
            "Rate of penetration: %f\n" % status[5] +
            "Standpipe pressure: %f\n" % int.from_bytes(status[6:8], 'big') +
            "Mud volume: %f\n" % int.from_bytes(status[8:10], 'big') +
            "Trip tank volume: %f\n" % int.from_bytes(status[10:12], 'big') +
            "Mud return volume rate: %f\n" % int.from_bytes(status[12:14], 'big') +
            "RPM: %f\n" % status[14] +
            "Torque: %f\n" % int.from_bytes(status[15:17], 'big')
        )
