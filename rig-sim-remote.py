import serial
import socket
import yaml
import errno
import sys
import time


try:
    with open('rig-sim.yaml') as config_file:
        config = yaml.safe_load(config_file)
except (OSError, IOError) as exception:
    if getattr(exception, 'errno', 0) == errno.ENOENT:
        print("Configuration file not found")
        sys.exit()

if __name__ == "__main__":
    ser = None
    sock = None
    if not isinstance(config['connections'], list):
        config['connections'] = [config['connections']]

    for connection in config['connections']:
        if connection['type'] == 'serial':
            try:
                ser = serial.Serial(
                    port=connection['port'],
                    baudrate=connection['baud_rate'],
                    parity=connection['parity'],
                    bytesize=connection['bytesize'],
                    timeout=1,
                )
            except serial.serialutil.SerialException:
                ser = None
            else:
                print("Serial connection established")
        elif connection['type'] == 'socket':
            sock = socket.socket()
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.connect((socket.gethostname(), connection['port']))
            print("Socket established")

    print("Waiting for status")
    previous_status = None
    while True:
        if ser is not None:
            ser.write(bytearray([41]))
            status = ser.read(19)
        elif sock is not None:
            sock.send(bytearray([41]))
            status = sock.recv(19)

        if status != previous_status:
            print(
                "Transmission received: %s\n" % status +
                "Status: %s\n" % status[0] +
                "Measured depth: %.2f feet\n" % (int.from_bytes(status[1:4], 'big') / 100.0) +
                "Bit depth: %.2f feet\n" % (int.from_bytes(status[4:7], 'big') / 100.0) +
                "Rate of penetration: %d ft/hr\n" % status[7] +
                "Standpipe pressure: %d psi\n" % int.from_bytes(status[8:10], 'big') +
                "Mud volume: %d bbls\n" % int.from_bytes(status[10:12], 'big') +
                "Trip tank volume: %d bbls\n" % int.from_bytes(status[12:14], 'big') +
                "Mud return volume rate: %d bbls/min\n" % int.from_bytes(status[14:16], 'big') +
                "RPM: %d\n" % status[16] +
                "Torque: %d ft lb\n" % int.from_bytes(status[17:19], 'big')
            )
            previous_status = status

        time.sleep(2)
