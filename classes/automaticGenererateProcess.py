from classes.process import Process
from classes.listProcessNew import ListProcessNew
from classes.container.tableIndex import TableIndex
import random
import os


class AutomaticGenerateProcess:
    def __init__(self):
        self.__tableId = TableIndex()
        self.__numberProgram = 1
        self.__list_new_process = ListProcessNew()

    def addingProcess(self):
        numberMaximumProcess = int(input("Ingresa el numero de procesos a ejecutar: "))
        if numberMaximumProcess == 0:
            numberMaximumProcess = 1
        for index in range(0, numberMaximumProcess):
            process = self.__createProcess()
            self.__list_new_process.addProcess(process)

    def __optionsOperations(self):
        operation = random.randint(1, 5)
        if operation == 1:
            return "sum"
        elif operation == 2:
            return "rest"
        elif operation == 3:
            return "mult"
        elif operation == 4:
            return "div"
        elif operation == 5:
            return "mod"

    def __createProcess(self):
        os.system("cls")
        operation = self.__optionsOperations()
        number1 = random.randint(0, 200)
        number2 = random.randint(1, 200)
        timeMaximumProcess = random.randint(5, 15)
        idProgram = self.__numberProgram
        process = Process(operation, timeMaximumProcess, idProgram, number1, number2)
        self.__numberProgram += 1
        return process

    def get_new_process(self):
        return self.__list_new_process
