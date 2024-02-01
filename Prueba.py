

from PySide6.QtSerialPort import QSerialPortInfo 

serialPortInfos = QSerialPortInfo.availablePorts()
for portInfo in serialPortInfos:
    print(f"{portInfo.portName()} {type(portInfo.portName())} \n")
             
