import time
import datetime
import struct
import serial
import yaml
import pandas as pd
import config as cfg

class Recorder:

    def __init__(self, duration: int, port: str, baudrate: int, timeout: int):
        self.__data = {
            'vin': [],
            'vd': []
        }
        self.__duration = duration

        try:
            self.__ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=timeout
            )
            print(f'Serial initiated: {port}@{baudrate}')
        
        except serial.SerialException as e:        
            print(f"Error: Could not open or read from serial port {port}: {e}")
            exit(code=1)
        
        except Exception as e:
            print(f"Error: Unexpected error when initiating serial: {e}")
            exit(code=1)

    def record(self):
        start_ts = time.time()
        
        while time.time() - start_ts < self.__duration:
            _ = self.__ser.read_until(cfg.PACKET_HEADER)
            payload = self.__ser.read(cfg.DATA_LENGTH)
            tail = self.__ser.read(2)

            if tail != cfg.PACKET_TAIL:
                continue

            data = struct.unpack(cfg.UNPACK_FORMAT, payload)
            self.__data['vin'] += data[:cfg.DATA_PER_CH]
            self.__data['vd'] += data[cfg.DATA_PER_CH:]

        print(f'Recording completed, total data: {len(self.__data['vin'])}')

    def save(self):
        with open(cfg.INFO_YAML_PATH, 'r') as file:
            info_yaml = yaml.safe_load(file)

        data_filename = f'data/{info_yaml['count']:05d}.csv'
        info_yaml[data_filename] = f'{datetime.now()}'
        info_yaml['count'] += 1

        df = pd.DataFrame(self.__data)
        df.to_csv(data_filename, index=False)

        with open(cfg.INFO_YAML_PATH, 'w') as file:
            yaml.safe_dump(info_yaml, file)

        print(f'Data saved')

