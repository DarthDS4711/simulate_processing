from classes.listProcessNew import ListProcessNew
from classes.listCompleteProcess import ListCompleteProcess
from operationsMathematics.operations import executeOperation
from classes.interruptions.keyboardInterruptions import KeyboardInteruptions
from colorama import init, Cursor, Back, Fore
from classes.queue.queueBloquedProcess import QueueBloquedProcess
from classes.queue.queueReadyProcess import QueueReadyProcess
from time import sleep
import os

init()


class VistProcess:
    def __init__(self, list_new_process):
        self.__countProgram = 0
        self.__cursorY = 5
        self.__listProcessFinish = ListCompleteProcess()
        self.__interruption = KeyboardInteruptions()
        self.__flagToContinuePrintProcess = True
        self.__queue_new_process = list_new_process
        self.__ready_process = QueueReadyProcess()
        self.__bloqued_process = QueueBloquedProcess()

    def add_process_ready(self):
        while True:
            processNew = self.__queue_new_process.getActualProcess()
            if processNew is not None:
                if self.__ready_process.number_enqueue_process() < 5:
                    self.__ready_process.enqueue_process_ready(processNew)
                    self.__queue_new_process.deleteLastProcess()
                else:
                    break
            else:
                break

    def __printEnqueueBloquedProcess(self):
        print(Cursor.DOWN(2))
        self.__bloqued_process.print_queue()
        print("\r" + Fore.LIGHTYELLOW_EX + "Contador del programa: ",
              str(self.__countProgram), end="")
        print(Fore.RESET)
        print(Cursor.UP(15))
        self.__countProgram += 1
        sleep(1)

    def __statusOfInterruptionInside(self):
        status = self.__interruption.getStatusInterruption()
        if status == 3:
            while True:
                self.__interruption.listenInterruption()
                status = self.__interruption.getStatusInterruption()
                if status == 4:
                    return 1
        if status == 1 or status == 2:
            return 2
        else:
            return 3

    def __statusOfInterruptionOutside(self, process):
        statusInterruption = self.__interruption.getStatusInterruption()
        if statusInterruption == 1:
            self.__bloqued_process.enqueue_process_bloqued(process)
            self.__cursorY -= 1
            self.__ready_process.dequeue_process_ready()
        elif statusInterruption == 2:
            self.__listProcessFinish.addProcessComplete(process)
            self.__ready_process.dequeue_process_ready()
        elif statusInterruption == 0 or statusInterruption == 4:
            self.__realizeOperation(process)
            self.__listProcessFinish.addProcessComplete(process)
            self.__ready_process.dequeue_process_ready()
        self.__interruption.setStatusInterruption(0)

    def __printProcessActual(self, process):
        idProgram = " "
        operation = " "
        timeRest = " "
        time = " "
        if process is not None:
            maximunTime = process.getMaximumTime()
            idProgram = process.getNumberProgram()
            operation = str(process.getFirstNumber()) + " " + \
                        process.getOperation() + " " + str(process.getSecondNumber())
            time = maximunTime - process.getTimeTranscurred()
            timeRest = process.getTimeTranscurred()
        print("\r" + Cursor.FORWARD(46) + "Operacion: " + operation, end="\n")
        print("\r" + Cursor.FORWARD(46) + "ID: " + str(idProgram), end="\n")
        print("\r" + Cursor.FORWARD(46) +
              "Tiempo transcurrido: " + str(time) + " \n" + Cursor.FORWARD(46) +
              "Tiempo restante: " + str(timeRest) + " ", end="\n")
        if process is not None:
            process.setTimeTranscurred(timeRest + 1)

    def __refreshVisualInformation(self, process):
        time_transcurred = 0
        time_maximum = process.getMaximumTime()
        while time_transcurred <= time_maximum:
            self.__interruption.listenInterruption()
            self.__printProcessActual(process)
            self.__printEnqueueBloquedProcess()
            time_transcurred = process.getTimeTranscurred()
            code_continue = self.__statusOfInterruptionInside()
            if code_continue == 2:
                break

    def __realizeOperation(self, process):
        number_1 = process.getFirstNumber()
        number_2 = process.getSecondNumber()
        result = executeOperation(number_1, number_2, process.getOperation())
        if type(result) is float:
            result = round(result, 2)
        operation = str(number_1) + " " + \
                    process.getOperation() + " " + str(number_2)
        process.setOperation(operation)
        process.setResult(result)

    def __print_information_to_console(self, flag):
        os.system("cls")
        process = self.__ready_process.getactual_process()
        self.__ready_process.print_queue(1, 2, self.__queue_new_process.numberProcess())
        print("\n")
        self.__listProcessFinish.printListCompleteOfProcess(80, 9)
        print("\n")
        print(Fore.RESET)
        print(Fore.LIGHTCYAN_EX + Cursor.FORWARD(46) +
              Cursor.UP(self.__cursorY) + "proceso en ejecucion", end="\n")
        print(Fore.RESET)
        if flag:
            self.__refreshVisualInformation(process)
            self.__statusOfInterruptionOutside(process)
        else:
            self.__printProcessActual(process)
        print("\n\n\n\n")
        if not flag:
            self.__listProcessFinish.numberProcessComplete()

    def __is_valid_continue_to_print(self):
        if self.__queue_new_process.numberProcess() > 0:
            return True
        else:
            return False

    def __completeVistAllProcess(self):
        continue_print = self.__is_valid_continue_to_print()
        while continue_print:
            self.__print_information_to_console(True)
            continue_print = self.__is_valid_continue_to_print()
            self.__cursorY += 1
        self.__print_information_to_console(False)

    def printScreen(self):
        self.__completeVistAllProcess()
