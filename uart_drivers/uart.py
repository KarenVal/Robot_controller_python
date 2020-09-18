"""Functions to read and send UART commands between RBPi and DA14585"""
import serial
import os


def send_uart_command():
    return


def read_uart_command():
    return


if __name__ == '__main__':
    '''    with serial.Serial() as ser:
            ser.baudrate = 115200
            ser.port = 'COM18'
            ser.open()
            ser.write(b'hello')'''

    robo_ser = serial.Serial('COM3', 115200, bytesize=8, timeout=0, parity='N', rtscts=1)
    robo_ser.write(b'R, 100, E, 100, F')
    print("Done")
