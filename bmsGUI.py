import serial.tools.list_ports
from tkinter import *
from tkinter import ttk

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
