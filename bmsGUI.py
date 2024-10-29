import serial.tools.list_ports # type: ignore
from tkinter import *
from tkinter import ttk

#Initialize serial and tkinter
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
root = Tk(screenName="BMS GUI", baseName="Main Screen")
root.title("BMS GUI")
root.geometry("640x480")
scrollbar = Scrollbar(root)
scrollbar.pack(side = RIGHT, fill=Y)

#Get all com ports
portList = Listbox(root, yscrollcommand=Scrollbar.set)

for port in ports:
    portList.insert(END, str(port))
    print(str(port))

portList.pack(side=LEFT, fill=BOTH)
scrollbar.config(command=portList.yview)




#End of tkinter
root.mainloop()