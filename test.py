import serial.tools.list_ports
from time import sleep

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portsList = []

for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))

val = input("Select Port: COM")

for x in range(0,len(portsList)):
    if portsList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portVar)

serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()

voltages = [['' for tabs in range(14)] for boards in range(10)]
temps = [['' for tabs in range(9)] for boards in range(10)]
maxVolt = 0.0
maxTemp = 0.0

while True:
    packets = []
    i = 0
    if serialInst.in_waiting:
        sleep(0.1)
        while serialInst.in_waiting:
            packets.append(serialInst.readline().decode('utf').rstrip('\n\r'))
            i = i+1


    if len(packets) == 1:
        print('Waiting')
    elif (len(packets) > 1):
        del packets[171:261]
        print(packets)
        for k in range(len(packets)):
            print((str(k+1)) + ' ' + packets[k])

        for board in range(10):
            for tap in range(14):
                maxVolt = max(maxVolt, float(packets[2 + tap + 17*board]))
                voltages[board][tap] = packets[2 + tap + 17*board]
        print(voltages)

        for board in range(10):
            for temp in range(9):
                maxTemp = max(maxTemp, 0.0 if float(packets[173 + temp + 12*board]) == 150.0 else float(packets[173 + temp + 12*board]))
                temps[board][temp] = packets[173 + temp + 12*board]
        print(temps)

        print(maxVolt)
        print(maxTemp)

        print('Done printing')
