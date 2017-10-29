import serial, time

s = serial.Serial('/dev/ttyS0',9600,timeout=10)
def move(order) :
    s.write(order)
    time.sleep(0.1)
    s.write('s')
