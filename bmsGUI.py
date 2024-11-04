import serial.tools.list_ports 
import tkinter as tk
import ttkbootstrap as ttk

#Initialize serial
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
serialInst.baudrate = 9600

def updatePorts():
    ports = serial.tools.list_ports.comports()
    print('Com ports updated') #Testing

#Tkinter Window Loop
root = ttk.Window(scaling = 2.0, themename='darkly')
root.title("BMS GUI")
root.minsize(1280,600)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

#Left side lowest/highest voltages/temps also com port selection
leftFrame = ttk.Frame(master=root)
leftFrame.columnconfigure(0, weight=1)
leftFrame.rowconfigure(0, weight=1)
leftFrame.rowconfigure(1, weight=1)

minMaxFrame = ttk.Frame(master=leftFrame)
comportFrame = ttk.Frame(master=leftFrame)

#Min Max Frame Setup
minMaxFrame.columnconfigure(0, weight=1)
minMaxFrame.columnconfigure(1, weight=1)
minMaxFrame.rowconfigure(0, weight=1)
minMaxFrame.rowconfigure(1, weight=1)
minMaxFrame.rowconfigure(2, weight=1)
minMaxFrame.rowconfigure(3, weight=1)
minMaxFrame.rowconfigure(4, weight=1)
minMaxFrame.rowconfigure(5, weight=1)
minMaxFrame.rowconfigure(6, weight=1)

#Min Max
resetGlobalMax = ttk.Button(master=minMaxFrame, text='Reset All Time Max')
resetGlobalMax.grid(row=0, column=0, columnspan=2, sticky='nsew')

#Min Vals
minLabel = ttk.Label(master=minMaxFrame, text='Min Values', anchor="center")
minLabel.grid(row=1, column=0, columnspan=2, sticky='nsew')
lowVoltLabel = ttk.Label(master=minMaxFrame, text='Voltage:', anchor="center")
lowVoltLabel.grid(row=2, column=0, sticky='new')
lowVoltVal = ttk.Label(master=minMaxFrame, text='0V', anchor="center")
lowVoltVal.grid(row=2, column=0, sticky='sew')
lowTempLabel = ttk.Label(master=minMaxFrame, text='Temp:', anchor="center")
lowTempLabel.grid(row=2, column=1, sticky='new')
lowTempVal = ttk.Label(master=minMaxFrame, text='0C', anchor="center")
lowTempVal.grid(row=2, column=1, sticky='sew')

#High Vals
maxLabel = ttk.Label(master=minMaxFrame, text='Max Current Values', anchor="center")
maxLabel.grid(row=3, column=0, columnspan=2, sticky='nsew')
maxVoltLabel = ttk.Label(master=minMaxFrame, text='Voltage:', anchor="center")
maxVoltLabel.grid(row=4, column=0, sticky='new')
maxVoltVal = ttk.Label(master=minMaxFrame, text='0V', anchor="center")
maxVoltVal.grid(row=4, column=0, sticky='sew')
maxTempLabel = ttk.Label(master=minMaxFrame, text='Temp:', anchor="center")
maxTempLabel.grid(row=4, column=1, sticky='new')
maxTempVal = ttk.Label(master=minMaxFrame, text='0C', anchor="center")
maxTempVal.grid(row=4, column=1, sticky='sew')

#High All Time Volt
maxAllLabel = ttk.Label(master=minMaxFrame, text='Max All-Time Values', anchor="center")
maxAllLabel.grid(row=5, column=0, columnspan=2, sticky='nsew')
maxAllVoltLabel = ttk.Label(master=minMaxFrame, text='Voltage:', anchor="center")
maxAllVoltLabel.grid(row=6, column=0, sticky='new')
maxAllVoltVal = ttk.Label(master=minMaxFrame, text='0V', anchor="center")
maxAllVoltVal.grid(row=6, column=0, sticky='sew')
maxAllTempLabel = ttk.Label(master=minMaxFrame, text='Temp:', anchor="center")
maxAllTempLabel.grid(row=6, column=1, sticky='new')
maxAllTempVal = ttk.Label(master=minMaxFrame, text='0C', anchor="center")
maxAllTempVal.grid(row=6, column=1, sticky='sew')

minMaxFrame.grid(row=0, column=0, sticky='nsew')

#Comport Frame


leftFrame.grid(row=0, column=0, sticky='nsew')

#Add tabs for each board
notebook = ttk.Notebook(master=root)
tabs = {}

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
            tapLabel = ttk.Label(master=tapFrame, text=('Tap ' + str(((row*7 + column) + 1))))
            tapLabel.grid(row=row, column=column, sticky='nsew')
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
        tempLabel = ttk.Label(master=tempFrame, text=('Temp ' + str(column+1)))
        tempLabel.grid(row=0, column=column, sticky='nsew')
    #Place Frame
        tempFrame.grid(row=3, column=0, sticky='nsew')

    #Add Whole Frame
    notebook.add(tabs[i], text='Board ' + str(i+1))

notebook.grid(row=0, column=1, sticky='nsew')

#Com port selection menu
menu = tk.Menu(master=root)

#Update com ports
comMenu = tk.Menu(master=menu, tearoff=False)
comMenu.add_command(label='Update Com Ports', command=updatePorts)
menu.add_cascade(label='Com Port Configuration', menu=comMenu)

#Com Ports Sub Menu Selection
comPortsMenu_sub = tk.Menu(menu, tearoff=False)

for port in range(len(ports)):
    comPortsMenu_sub.add_checkbutton(label=str(ports[port]))

comMenu.add_cascade(label='Com Ports:', menu=comPortsMenu_sub)

#Add Menu
root.configure(menu=menu)

#End of tkinter loop
root.mainloop()