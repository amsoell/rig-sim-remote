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
    status = ser.read(19)
    if len(status) > 0:
        print(
            "Transmission received: %s\n" % status +
            "Status: %s\n" % status[0] +
            "Measured depth: %.2f\n" % (int.from_bytes(status[1:4], 'big') / 100.0) +
            "Bit depth: %.2f\n" % (int.from_bytes(status[4:7], 'big') / 100.0) +
            "Rate of penetration: %d\n" % status[7] +
            "Standpipe pressure: %d\n" % int.from_bytes(status[8:10], 'big') +
            "Mud volume: %d\n" % int.from_bytes(status[10:12], 'big') +
            "Trip tank volume: %d\n" % int.from_bytes(status[12:14], 'big') +
            "Mud return volume rate: %d\n" % int.from_bytes(status[14:16], 'big') +
            "RPM: %d\n" % status[16] +
            "Torque: %d\n" % int.from_bytes(status[17:19], 'big')
        )
