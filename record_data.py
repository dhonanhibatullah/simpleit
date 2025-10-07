from modules.recorder import Recorder

SERIAL_PORT         = 'COM9'
SERIAL_BAUDRATE     = 115200
SERIAL_TIMEOUT      = 1
RECORDING_DURATION  = 10

def main():
    rec = Recorder(
        RECORDING_DURATION, 
        SERIAL_PORT, 
        SERIAL_BAUDRATE, 
        SERIAL_TIMEOUT
    )
    rec.record()
    rec.save()

if __name__ == '__main__':
    main()