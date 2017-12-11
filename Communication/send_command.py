from STMprotocol import STMprotocol
import sys

protocol = STMprotocol(sys.argv[1])

cmd = int(argv[2])
parameters = []

if cmd == 1:
    args = protocol.send_command(cmd, b"ECHO")
elif cmd == 3 or cmd == 9:
    args = protocol.send_command(cmd, [int(sys.argv[3]), sys.argv[4]])
elif cmd == 4 or cmd == 5 or cmd == 10:
    args = protocol.send_command(cmd, [int(sys.argv[3])])
elif cmd == 11:
    args = protocol.send_command(cmd, [int(sys.argv[3]), int(sys.argv[4])])
else:
    args = protocol.send_command(cmd, [float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])])

print(args)
