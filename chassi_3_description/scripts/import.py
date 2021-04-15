import serial
import time
ser=serial.Serial('COM7',baudrate=9600, timeout=1)
while 1:
    a=input("enter char")
    time.sleep(1)
    ser.write(a.encode())
    

   




    


