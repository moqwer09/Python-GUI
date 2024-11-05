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
root.minsize(1280,720)

voltages = [[tk.StringVar(value='0V') for tabs in range(14)] for boards in range(10)]
temps = [[tk.StringVar(value='0C') for tabs in range(9)] for boards in range(10)]

def updateVals():
    if serialInst.is_open:
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
            #print('board' + str(board))
            for tap in range(14):
                #maxVolt = max(maxVolt, float(packets[2 + tap + 17*board]))
                voltages[board][tap].set(str(packets[2 + tap + 17*board]) + 'V')
        
        for board in range(10):
            for temp in range(9):
                #maxTemp = max(maxTemp, 0.0 if float(packets[173 + temp + 12*board]) == 150.0 else float(packets[173 + temp + 12*board]))
                temps[board][temp].set(str(packets[173 + temp + 12*board]) + 'C')


    root.after(1000, updateVals)

def updateClear():
    if serialInst.is_open:
        updateVals()

root.after(1000, updateVals)

#Left side lowest/highest voltages/temps also comport selection
leftFrame = ttk.Frame(master=root)

minMaxFrame = ttk.Frame(master=leftFrame)
comportFrame = ttk.Frame(master=leftFrame)

#Min Max
resetGlobalMax = ttk.Button(master=minMaxFrame, text='Reset All Time Values')
resetGlobalMax.pack(side='top', fill='x')

#Min Vals
minLabel = ttk.Label(master=minMaxFrame, text='Min Values', anchor="center", relief='solid', borderwidth=1)
minLabel.pack(side='top', fill='both')
minFrame = ttk.Frame(master=minMaxFrame, relief='solid', borderwidth=1)
#volt
minVoltFrame = ttk.Frame(master=minFrame, relief='solid', borderwidth=1)
minVoltLabel = ttk.Label(master=minVoltFrame, text='Voltage:', anchor="center")
minVoltLabel.pack(side='top')
minVoltVal = ttk.Label(master=minVoltFrame, text='0V', anchor="center")
minVoltVal.pack(side='top')
minVoltFrame.pack(side='left', expand=True, fill='both')
#temp
minTempFrame = ttk.Frame(master=minFrame, relief='solid', borderwidth=1)
minTempLabel = ttk.Label(master=minTempFrame, text='Temp:', anchor="center")
minTempLabel.pack(side='top')
minTempVal = ttk.Label(master=minTempFrame, text='0C', anchor="center")
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
maxVoltVal = ttk.Label(master=maxVoltFrame, text='0V', anchor="center")
maxVoltVal.pack(side='top')
maxVoltFrame.pack(side='left', expand=True, fill='both')
#temp
maxTempFrame = ttk.Frame(master=maxFrame)
maxTempLabel = ttk.Label(master=maxTempFrame, text='Temp:', anchor="center")
maxTempLabel.pack(side='top')
maxTempVal = ttk.Label(master=maxTempFrame, text='0C', anchor="center")
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
maxAllVoltVal = ttk.Label(master=maxAllVoltFrame, text='0V', anchor="center")
maxAllVoltVal.pack(side='top')
maxAllVoltFrame.pack(side='left', expand=True, fill='both')
#temp
maxAllTempFrame = ttk.Frame(master=maxAllFrame)
maxAllTempLabel = ttk.Label(master=maxAllTempFrame, text='Temp:', anchor="center")
maxAllTempLabel.pack(side='top')
maxAllTempVal = ttk.Label(master=maxAllTempFrame, text='0C', anchor="center")
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
    

#tapLabels = [[ttk.Label(master=tabs[boards]) for taps in range(14)] for boards in range(10)]


for i in range(10):
    #Tab Setup
    tabs[i] = ttk.Frame(master=notebook)
    #Row Setup
    tabs[i].rowconfigure(0, weight=1)
    tabs[i].rowconfigure(1, weight=8)
    tabs[i].rowconfigure(2, weight=1)
    tabs[i].rowconfigure(3, weight=4)
    #Column Setup
    tabs[i].columnconfigure(0,weight=1)

    #Voltage taps
    voltLabel = ttk.Label(master=tabs[i], text='Voltages')
    voltLabel.grid(row=0, column=0, sticky='nsew')
    tapFrame = ttk.Frame(master=tabs[i])
    #Row Setup
    for row in range(2):
        tapFrame.rowconfigure(row, weight=1)
    #Column Setup
    for column in range(7):
        tapFrame.columnconfigure(column, weight=1)
    #Placing Tap Labels
    for row in range(2):
        for column in range(7):
            #voltages[i][row*7 + column] = str(i*10 + row*7 + column) + 'V' #Testing
            tapLabel = ttk.Label(master=tapFrame, text=('Tap ' + str(((row*7 + column) + 1)) + ': '))
            tapVal = ttk.Label(master=tapFrame, textvariable=voltages[i][row*7 + column])
            tapLabel.grid(row=row, column=column, sticky='new')
            tapVal.grid(row=row, column=column, sticky='sew')
    #Place Frame
    tapFrame.grid(row=1, column=0, sticky='nsew')
    
    #Temp taps
    tempLabel = ttk.Label(master=tabs[i], text='Temperatures')
    tempLabel.grid(row=2, column=0, sticky='nsew')
    tempFrame = ttk.Frame(master=tabs[i])
    #Row Setup
    tempFrame.rowconfigure(row, weight=1)
    #Column Setup
    for column in range(9):
        tempFrame.columnconfigure(column, weight=1)
    #Placing Tap Labels
    for column in range(9):
        #temps[i][column] = str(i*10 + column) + 'C' #Testing
        tempLabel = ttk.Label(master=tempFrame, text=('Temp ' + str(column+1)))
        tempVal = ttk.Label(master=tempFrame, textvariable=temps[i][column])
        tempLabel.grid(row=0, column=column, sticky='new')
        tempVal.grid(row=0, column=column, sticky='sew')
    #Place Frame
        tempFrame.grid(row=3, column=0, sticky='nsew')

    #Add Whole Frame
    notebook.add(tabs[i], text='Board ' + str(i+1))

notebook.pack(side='left', expand=True, fill='both')

#End of tkinter loop
root.mainloop()