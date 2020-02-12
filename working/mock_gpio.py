
OUT = "OUT"
IN = "IN"

HIGH = True
LOW = False

def setup(channel, mode, initial=False):
    print("*** Mocked GPIO.setup : Channel = " + str(channel) + ", Mode = " + mode + ", Initial = " + str(initial))

def output(channel, state):
    print("*** Mocked GPIO.output : Channel = " + str(channel) + ", State = "+ str(state))

BOARD = "BOARD"
BCM = "BCM"

def setmode(mode):
    print("*** Mocked GPIO.setmode : Mode = "+ mode)

def cleanup():
    print("*** MOCKED GPIO.cleanup")

def setwarnings(flag):
    print("*** MOCKED GPIO.setwarnings : Flag = "+ str(flag))
