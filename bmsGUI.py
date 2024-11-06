import serial.tools.list_ports 
import tkinter as tk
import ttkbootstrap as ttk
from time import sleep

#Initialize serial
serialInst = serial.Serial()
serialInst.baudrate = 9600

#Tkinter Window Loop
root = ttk.Window(themename='darkly')
root.title("BMS GUI")
root.minsize(1280,600)

minVolt = tk.StringVar(value='999V')
minTemp = tk.StringVar(value='999C')
maxVolt = tk.StringVar(value='0V')
maxTemp = tk.StringVar(value='0C')
maxAllVolt = tk.StringVar(value='0V')
maxAllTemp = tk.StringVar(value='0V')

voltages = [[tk.StringVar(value='0V') for taps in range(14)] for boards in range(10)]
temps = [[tk.StringVar(value='0C') for taps in range(9)] for boards in range(10)]

def updateVals():
    if serialInst.is_open:
        minV = 999.9
        maxV = 0.0
        minT = 999.9
        maxT = 0.0
        serialInst.reset_input_buffer()
        packets = []

        while not(bool(serialInst.in_waiting)):
            #print('nothing')
            sleep(0.1)
        
        sleep(0.1)
        #print('Updating Vals')
        while serialInst.in_waiting:
            packets.append(serialInst.readline().decode('utf').rstrip('\n\r'))
        
        if len(packets) > 293:
            del packets[171:261]
        
        for board in range(10):
            for tap in range(14):
                #maxVolt = max(maxVolt, float(packets[2 + tap + 17*board]))
                minV = min(minV, float(packets[2 + tap + 17*board]))
                maxV = max(maxV, float(packets[2 + tap + 17*board]))
                voltages[board][tap].set(str(packets[2 + tap + 17*board]) + 'V')
        
        for board in range(10):
            for temp in range(9):
                minT = min(minT,  999.9 if float(packets[173 + temp + 12*board]) == 150.0 else float(packets[173 + temp + 12*board]))
                maxT = max(maxT, 0.0 if float(packets[173 + temp + 12*board]) == 150.0 else float(packets[173 + temp + 12*board]))
                temps[board][temp].set(str(packets[173 + temp + 12*board]) + 'C')

        minVolt.set(str(minV) + 'V')
        maxVolt.set(str(maxV) + 'V')
        minTemp.set(str(minT) + 'C')
        maxTemp.set(str(maxT) + 'C')

        maxAllVolt.set(str(max(maxV, float(maxAllVolt.get().rstrip('V')))) + 'V')
        maxAllTemp.set(str(max(maxT, float(maxAllTemp.get().rstrip('C')))) + 'C')

    root.after(1000, updateVals)

root.after(1000, updateVals)

def resetAll():
    maxAllVolt.set('0V')
    maxAllTemp.set('0C')

#Left side lowest/highest voltages/temps also comport selection
leftFrame = ttk.Frame(master=root)

minMaxFrame = ttk.Frame(master=leftFrame)
comportFrame = ttk.Frame(master=leftFrame)

#Min Max
resetGlobalMax = ttk.Button(master=minMaxFrame, text='Reset All Time Values', command=resetAll)
resetGlobalMax.pack(side='top', fill='x')

#Min Vals
minLabel = ttk.Label(master=minMaxFrame, text='Min Values', anchor="center")
minLabel.pack(side='top', fill='both')
minFrame = ttk.Frame(master=minMaxFrame)
#volt
minVoltFrame = ttk.Frame(master=minFrame)
minVoltLabel = ttk.Label(master=minVoltFrame, text='Voltage:', anchor="center")
minVoltLabel.pack(side='top')
minVoltVal = ttk.Label(master=minVoltFrame, textvariable=minVolt, anchor="center")
minVoltVal.pack(side='top')
minVoltFrame.pack(side='left', expand=True, fill='both')
#temp
minTempFrame = ttk.Frame(master=minFrame)
minTempLabel = ttk.Label(master=minTempFrame, text='Temp:', anchor="center")
minTempLabel.pack(side='top')
minTempVal = ttk.Label(master=minTempFrame, textvariable=minTemp, anchor="center")
minTempVal.pack(side='top')
minTempFrame.pack(side='left', expand=True, fill='both')

minFrame.pack(side='top', expand=False, fill='x')

#High Vals
maxLabel = ttk.Label(master=minMaxFrame, text='Max Values', anchor="center")
maxLabel.pack(side='top', fill='x')
maxFrame = ttk.Frame(master=minMaxFrame)
#volt
maxVoltFrame = ttk.Frame(master=maxFrame)
maxVoltLabel = ttk.Label(master=maxVoltFrame, text='Voltage:', anchor="center")
maxVoltLabel.pack(side='top')
maxVoltVal = ttk.Label(master=maxVoltFrame, textvariable=maxVolt, anchor="center")
maxVoltVal.pack(side='top')
maxVoltFrame.pack(side='left', expand=True, fill='both')
#temp
maxTempFrame = ttk.Frame(master=maxFrame)
maxTempLabel = ttk.Label(master=maxTempFrame, text='Temp:', anchor="center")
maxTempLabel.pack(side='top')
maxTempVal = ttk.Label(master=maxTempFrame, textvariable=maxTemp, anchor="center")
maxTempVal.pack(side='top')
maxTempFrame.pack(side='left', expand=True, fill='both')

maxFrame.pack(side='top', expand=False, fill='x')


#All Time High Vals
maxAllLabel = ttk.Label(master=minMaxFrame, text='All Time Max Values', anchor="center")
maxAllLabel.pack(side='top', fill='x')
maxAllFrame = ttk.Frame(master=minMaxFrame)
#volt
maxAllVoltFrame = ttk.Frame(master=maxAllFrame)
maxAllVoltLabel = ttk.Label(master=maxAllVoltFrame, text='Voltage:', anchor="center")
maxAllVoltLabel.pack(side='top')
maxAllVoltVal = ttk.Label(master=maxAllVoltFrame, textvariable=maxAllVolt, anchor="center")
maxAllVoltVal.pack(side='top')
maxAllVoltFrame.pack(side='left', expand=True, fill='both')
#temp
maxAllTempFrame = ttk.Frame(master=maxAllFrame)
maxAllTempLabel = ttk.Label(master=maxAllTempFrame, text='Temp:', anchor="center")
maxAllTempLabel.pack(side='top')
maxAllTempVal = ttk.Label(master=maxAllTempFrame, textvariable=maxAllTemp, anchor="center")
maxAllTempVal.pack(side='top')
maxAllTempFrame.pack(side='left', expand=True, fill='both')

maxAllFrame.pack(side='top', expand=False, fill='x')

minMaxFrame.pack(side='top', expand=False, fill='both')

#Comport Frame setup

portTable = ttk.Treeview(master=comportFrame, columns=('comName', 'comDesc'), show='headings', selectmode='browse')
portTable.heading('comName', text='Port')
portTable.column('comName', width=60)
portTable.heading('comDesc', text='Description')
portTable.column('comDesc', width=250)

def updatePorts():
    portTable.delete(*portTable.get_children())
    ports = serial.tools.list_ports.comports()
    for i in range(len(ports)):
        data = (str(ports[i].name), str(ports[i].description))
        portTable.insert(parent='', index=i, values=data)

def openPort(_):
    if serialInst.is_open:
        serialInst.close()
    
    serialInst.port = str(portTable.item(portTable.selection())['values'][0])
    serialInst.open()

    if serialInst.is_open:
        print('Port opened')
    else:
        print('Port did not open')

portTable.bind('<<TreeviewSelect>>', openPort)

updatePortsButton = ttk.Button(master=comportFrame, text='Update Com Ports', command=updatePorts)
updatePortsButton.pack(side='top', fill='x')

portTable.pack(side='top', expand=True, fill='both')

comportFrame.pack(side='top', expand=True, fill='both')

leftFrame.pack(side='left', fill='y')

#Add tabs for each board
notebook = ttk.Notebook(master=root)
tabs = {}

for i in range(10):
    #Tab Setup
    tabs[i] = ttk.Frame(master=notebook)

    #Voltage taps
    voltLabel = ttk.Label(master=tabs[i], text='Voltages', anchor='center')
    voltLabel.pack(side='top', fill='x', pady=10)
    topBottom = {}
    topBottom[0] = ttk.Frame(master=tabs[i])
    topBottom[1] = ttk.Frame(master=tabs[i])

    tapFrames = {}

    for rows in range(2):
        for cols in range(7):
            tapFrames[rows*7 + cols] = ttk.Frame(master=topBottom[rows])
    
    #Placing Tap Labels
    for row in range(2):
        for column in range(7):
            #voltages[i][row*7 + column] = str(i*10 + row*7 + column) + 'V' #Testing
            tapLabel = ttk.Label(master=tapFrames[row*7 + column], text=('Tap ' + str(((row*7 + column) + 1)) + ': '), anchor='center')
            tapVal = ttk.Label(master=tapFrames[row*7 + column], textvariable=voltages[i][row*7 + column], anchor='center')
            tapLabel.pack(side='top', fill='both')
            tapVal.pack(side='top', expand=True, fill='both')
            tapFrames[row*7 + column].pack(side='left', expand=True, fill='both')
    #Place Frame
    topBottom[0].pack(side='top', expand=True, fill='both')
    topBottom[1].pack(side='top', expand=True, fill='both')
    
    #Temp taps
    tempLabel = ttk.Label(master=tabs[i], text='Temperatures', anchor='center')
    tempLabel.pack(side='top', fill='x', pady=10)
    tempFr = ttk.Frame(master=tabs[i])
    tempFrames = {}
    for cols in range(9):
        tempFrames[cols] = ttk.Frame(master=tempFr)
    #Placing Tap Labels
    for column in range(9):
        #temps[i][column] = str(i*10 + column) + 'C' #Testing
        tempLabel = ttk.Label(master=tempFrames[column], text=('Temp ' + str(column+1)), anchor='center')
        tempVal = ttk.Label(master=tempFrames[column], textvariable=temps[i][column], anchor='center')
        tempLabel.pack(side='top', fill='both')
        tempVal.pack(side='top', expand=True, fill='both')
        tempFrames[column].pack(side='left', expand=True, fill='both')

    tempFr.pack(side='top', expand=True, fill='both')

    #Add Whole Frame
    notebook.add(tabs[i], text='Board ' + str(i+1))

notebook.pack(side='left', expand=True, fill='both')

#End of tkinter loop
root.mainloop()