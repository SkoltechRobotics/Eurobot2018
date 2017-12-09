import serial
import sys
import struct

cmd = int(sys.argv[1])
if cmd == 1:
    parameters = bytearray("ECHO")
elif cmd == 3:
    ch = int(sys.argv[2])
    f = float(sys.argv[3])
    parameters = bytearray([ch]) + bytearray(struct.pack("f", f))
elif cmd == 4 or cmd == 5:
    ch = int(sys.argv[2])
    parameters = bytearray([ch])

msg_len = len(parameters) + 2
msg = bytearray([0xfa, 0xaf, msg_len, cmd]) + parameters
crc = sum(msg) % 256
msg += bytearray([crc])

print(repr(msg))
ser = serial.Serial("/dev/ttyUSB0", 9600)
print("send ", repr(msg))
ser.write(msg)

while(ser.read() != 0xfa):
    pass
adr = ser.read()[0]
answ_len = ser.read()[0]
answ = bytearray(ser.read(answ_len))
print("anwer ", repr(answ))

#print(bytearray(ser.read(9)))
