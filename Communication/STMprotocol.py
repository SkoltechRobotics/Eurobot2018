import serial
import struct
import datetime


class STMprotocol:
    def __init__(self, serial_port):
        self.ser = serial.Serial(serial_port, 115200, timeout=0.2)
        self.pack_format = {
            0x01: "BBBB",
            0x03: "Bf",
            0x04: "B",
            0x05: "B",
            0x09: "Bf",
            0x0a: "B",
            0x0b: "BH",
            0xa0: "fff",
            0xa1: "fff"
        }

        self.unpack_format = {
            0x01: "BBBB",
            0x03: "BB",
            0x04: "BB",
            0x05: "BB",
            0x09: "BB",
            0x0a: "f",
            0x0b: "BB",
            0xa0: "Bfff",
            0xa1: "BB"
        }

    def send_command(self, cmd, args):
        parameters = bytearray(struct.pack(self.format, *args))
        msg_len = len(parameters) + 5
        msg = bytearray([0xfa, 0xaf, msg_len, cmd]) + parameters
        crc = sum(msg) % 256
        msg += bytearray([crc])

        print("send ", repr(msg))
        ser.write(msg)

        start_time = datetime.datetime.now()
        time_threshold = datetime.timedelta(seconds=1)
        dt = start_time - start_time

        data = ser.read()[0]
        while (data != 0xfa) and (dt < time_threshold):
            data = ser.read()[0]

            current_time = datetime.datetime.now()
            dt = start_time - current_time

        adr = ser.read()[0]
        answer_len = ser.read()[0]
        answer = bytearray(ser.read(answer_len - 3))
        print("answer ", repr(bytearray([data, adr, answer_len]) + answer))

        args = struct.unpack(self.unpack_format, answer[1:-1])
        return args
