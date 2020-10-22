"""
Check the serial port connection. Document says rts and dts should be enabled for hardware flow control. This did
not work for me.
"""
import serial


ser = serial.Serial()
ser.port = 'COM1'
ser.baudrate = 38400

ser.timeout = 1

ser.open()
if not ser.is_open:
    raise ValueError('Serial Port cannot open')


bs = ser.read(26)
print('Bytes Read:', bs)

ser.close()
