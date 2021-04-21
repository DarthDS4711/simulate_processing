from classes.listCompleteProcess import ListCompleteProcess
from operationsMathematics.operations import executeOperation
from classes.interruptions.keyboardInterruptions import KeyboardInteruptions
from colorama import init, Cursor, Back, Fore
from classes.queue.queueReadyProcess import QueueReadyProcess
from accountant.calculate_accountant import *
from accountant.generate_table_bcp import *
from generateProcess.randomDataCreateProcess import *
from time import sleep
import os

init()


class VistProcess:
    def __init__(self, list_new_process):
        self.__countProgram = 0
        self.__cursorY = 5
        self.__listProcessFinish = ListCompleteProcess()
        self.__interruption = KeyboardInteruptions()
        self.__flag_unlock_process = False
        self.__queue_new_process = list_new_process
        self.__ready_process = QueueReadyProcess()
        self.__bloqued_process = QueueBloquedProcess()
        self.__id_last_program_to_execute = self.__queue_new_process.numberProcess() + 1

    def add_process_ready(self):
        while True:
            processNew = self.__queue_new_process.getActualProcess()
            if processNew is not None:
                if self.__ready_process.number_enqueue_process() < 5:
                    processNew.set_time_arrival(0)
                    self.__ready_process.enqueue_process_ready(processNew)
                    self.__queue_new_process.deleteLastProcess()
                else:
                    break
            else:
                break

    def __move_new_process(self):
        number_process_active = self.__ready_process.number_enqueue_process()
        number_process_active += self.__bloqued_process.number_process_bloqued()
        if number_process_active < 5:
            process_to_enter = self.__queue_new_process.getActualProcess()
            if process_to_enter is not None:
                process_to_enter.set_time_arrival(self.__countProgram)
                self.__ready_process.enqueue_process_ready(process_to_enter)
                self.__queue_new_process.deleteLastProcess()

    def __printEnqueueBloquedProcess(self):
        print(Cursor.DOWN(2))
        self.__bloqued_process.print_queue()
        print("\r" + Fore.LIGHTYELLOW_EX + "Contador del programa: ",
              str(self.__countProgram), end="")
        print(Fore.RESET)
        print(Cursor.UP(15))
        self.__flag_unlock_process = is_time_bloqued_finish(self.__bloqued_process)
        calculate_bloqued_time(self.__bloqued_process)
        sleep(1)

    def __print_bcp_table_at_moment(self):
        table_bcp = []
        print(Cursor.DOWN(16))
        generate_bcp_per_process(self.__queue_new_process, self.__bloqued_process,
                                 self.__ready_process, self.__listProcessFinish,
                                 table_bcp, self.__countProgram - 1)
        for index in range(0, len(table_bcp)):
            print(table_bcp[index].print_counters_process())

    def __block_e_s_process(self):
        bloqued_len_process = self.__bloqued_process.number_process_bloqued()
        number_process = self.__ready_process.number_enqueue_process()
        number_process += self.__queue_new_process.numberProcess()
        if bloqued_len_process > 0 and number_process == 0:
            self.__cursorY -= 1
            return True
        else:
            return False


    def __statusOfInterruptionInside(self):
        status_to_return = True
        status = self.__interruption.getStatusInterruption()
        if status == 3 or status == 6:
            if status == 6:
                self.__print_bcp_table_at_moment()
            while True:
                self.__interruption.listenInterruption()
                status = self.__interruption.getStatusInterruption()
                if status == 4:
                    break
                if status == 7:
                    status_to_return = False
                    self.__cursorY -= 1
                    break
        if status == 1 or status == 2 or status == 5:
            status_to_return = False
        return status_to_return

    def __statusOfInterruptionOutside(self, process):
        statusInterruption = self.__interruption.getStatusInterruption()
        if statusInterruption == 1 and self.__block_e_s_process() is False:
            process.refresh_time_bloqued()
            self.__bloqued_process.enqueue_process_bloqued(process)
            self.__cursorY -= 1
            self.__ready_process.dequeue_process_ready()
        elif statusInterruption == 2 and self.__block_e_s_process() is False:
            calculate_accountant_process(process, self.__countProgram)
            self.__listProcessFinish.addProcessComplete(process)
            self.__ready_process.dequeue_process_ready()
        elif statusInterruption == 0 or statusInterruption == 4:
            calculate_accountant_process(process, self.__countProgram)
            self.__realizeOperation(process)
            self.__listProcessFinish.addProcessComplete(process)
            self.__ready_process.dequeue_process_ready()
        elif statusInterruption == 5:
            add_new_process_to_simulation(self.__id_last_program_to_execute,
                                          self.__queue_new_process)
            self.__id_last_program_to_execute += 1
            if self.__block_e_s_process() is True:
                self.__cursorY += 1
            else:
                self.__cursorY -= 1
        self.__move_new_process()
        self.__interruption.setStatusInterruption(0)

    def __printProcessActual(self, process):
        idProgram = " "
        operation = " "
        timeRest = " "
        time = " "
        if process is not None:
            maximunTime = process.getMaximumTime()
            idProgram = process.getNumberProgram()
            operation = str(process.getFirstNumber()) + " " + process.getOperation() + " " + str(
                process.getSecondNumber())
            time = maximunTime - process.getTimeTranscurred()
            timeRest = process.getTimeTranscurred()
        print("\r" + Cursor.FORWARD(46) + "Operacion: " + operation, end="\n")
        print("\r" + Cursor.FORWARD(46) + "ID: " + str(idProgram), end="\n")
        print("\r" + Cursor.FORWARD(46) + "Tiempo transcurrido: " + str(timeRest) +
              " \n" + Cursor.FORWARD(46) + "Tiempo restante: " + str(time) + " ", end="\n")
        if process is not None:
            process.setTimeTranscurred(timeRest + 1)

    def __continue_print(self):
        number_process = self.__ready_process.number_enqueue_process()
        number_process += self.__bloqued_process.number_process_bloqued()
        contains_process = True if number_process > 0 else False
        return contains_process

    def __refreshVisualInformation(self, process):
        time_transcurred = process.getTimeTranscurred() if process is not None else 0
        time_maximum = process.getMaximumTime() if process is not None else 0
        calculate_time_response(process, self.__countProgram)
        while time_transcurred <= time_maximum:
            self.__interruption.listenInterruption()
            self.__printProcessActual(process)
            self.__printEnqueueBloquedProcess()
            self.__countProgram += 1
            code_continue = self.__statusOfInterruptionInside()
            time_transcurred += 1
            if code_continue is False:
                break
            if self.__flag_unlock_process:
                break
            if process is None:
                if self.__continue_print():
                    time_transcurred -= 1


    def __realizeOperation(self, process):
        number_1 = process.getFirstNumber()
        number_2 = process.getSecondNumber()
        result = executeOperation(number_1, number_2, process.getOperation())
        if type(result) is float:
            result = round(result, 2)
        operation = str(number_1) + " " + process.getOperation() + " " + str(number_2)
        process.setOperation(operation)
        process.setResult(result)

    def __enqueue_process_bloqued_to_ready(self):
        process = self.__bloqued_process.getactual_process()
        process.refresh_time_bloqued()
        self.__ready_process.enqueue_process_ready(process)
        self.__bloqued_process.dequeue_process_bloqued()
        self.__cursorY -= 1

    def __print_information_to_console(self, flag):
        os.system("cls")
        process = self.__ready_process.getactual_process()
        self.__ready_process.print_queue(1, 2, self.__queue_new_process.numberProcess())
        print("\n")
        self.__listProcessFinish.printListCompleteOfProcess(80, 10)
        print("\n")
        print(Fore.RESET)
        print(Fore.LIGHTCYAN_EX + Cursor.FORWARD(46) +
              Cursor.UP(self.__cursorY) + "proceso en ejecucion", end="\n")
        print(Fore.RESET)
        if flag:
            self.__refreshVisualInformation(process)
            if self.__flag_unlock_process:
                self.__enqueue_process_bloqued_to_ready()
                self.__flag_unlock_process = False
            else:
                self.__statusOfInterruptionOutside(process)
        if not flag:
            self.__refreshVisualInformation(process)
            self.__listProcessFinish.print_table_bcp()

    def __is_valid_continue_to_print(self):
        if self.__queue_new_process.numberProcess() > 0:
            return True
        else:
            if self.__ready_process.number_enqueue_process() > 0:
                return True
            elif self.__bloqued_process.number_process_bloqued() > 0:
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
