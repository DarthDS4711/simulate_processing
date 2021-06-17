from classes.listCompleteProcess import ListCompleteProcess
from operationsMathematics.operations import executeOperation
from classes.listProcessNew import ListProcessNew
from classes.interruptions.keyboardInterruptions import KeyboardInteruptions
from colorama import init, Cursor, Back, Fore
from classes.queue.queueReadyProcess import QueueReadyProcess
from accountant.calculate_accountant import *
from accountant.generate_table_bcp import *
from generateProcess.randomDataCreateProcess import *
from time import sleep
import os
from classes.pagination.tableFrames import TableFrames


init()


class VistProcess:
    def __init__(self, list_new_process, quantum):
        self.__countProgram = 0
        self.__cursorY = 3
        self.__listProcessFinish = ListCompleteProcess()
        self.__interruption = KeyboardInteruptions()
        self.__flag_unlock_process = False
        self.__queue_new_process = ListProcessNew()
        self.__queue_aux_new_process = list_new_process
        self.__ready_process = QueueReadyProcess()
        self.__bloqued_process = QueueBloquedProcess()
        self.__id_last_program_to_execute = self.__queue_new_process.numberProcess() + 1
        self.__quantum = quantum
        self.__table_framework = TableFrames()

    def add_process_ready(self):
        self.__table_framework.inicialize_table_frame()
        continue_add = True
        number_process_ready = 0
        while continue_add:
            processNew = self.__queue_aux_new_process.getActualProcess()
            if number_process_ready < 5:
                if processNew is not None:
                    processNew.set_time_arrival(0)
                    continue_add = self.__table_framework.add_process_to_table(processNew, 1)
                    if continue_add:
                        self.__ready_process.enqueue_process_ready(processNew)
                        self.__queue_aux_new_process.deleteLastProcess()
            else:
                if processNew is not None:
                    continue_add = self.__table_framework.add_process_to_table(processNew, 6)
                    if continue_add:
                        self.__queue_new_process.addProcess(processNew)
                        self.__queue_aux_new_process.deleteLastProcess()
                else:
                    continue_add = False
            number_process_ready += 1
        self.__id_last_program_to_execute = number_process_ready

    def __printEnqueueBloquedProcess(self):
        print(Cursor.DOWN(2))
        self.__bloqued_process.print_queue()
        self.__table_framework.print_table_frame(1)
        print("\r" + Fore.LIGHTYELLOW_EX + "Contador del programa: ",
              str(self.__countProgram), end="")
        print(Fore.RESET)
        print(Cursor.UP(38))
        self.__flag_unlock_process = is_time_bloqued_finish(self.__bloqued_process)
        calculate_bloqued_time(self.__bloqued_process)
        sleep(1)

    def __print_bcp_table_at_moment(self):
        table_bcp = []
        print(Cursor.DOWN(39))
        generate_bcp_per_process(self.__queue_new_process, self.__bloqued_process,
                                 self.__ready_process, self.__listProcessFinish,
                                 table_bcp, self.__countProgram)
        for index in range(0, len(table_bcp)):
            print(table_bcp[index].print_counters_process())

    def __block_e_s_process(self):
        bloqued_len_process = self.__bloqued_process.number_process_bloqued()
        number_process = self.__ready_process.number_enqueue_process()
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

    def __return_process_to_ready(self, process, id_process):
        process.set_quantum(-1)
        self.__table_framework.set_status_process_selected(id_process, 1)
        self.__ready_process.enqueue_process_ready(process)
        self.__ready_process.dequeue_process_ready()
        self.__cursorY -= 1

    def __move_process_to_finish(self, process, id_process, flag_error):
        calculate_accountant_process(process, self.__countProgram)
        self.__table_framework.delete_process_table_framework(id_process)
        if not flag_error:
            self.__realizeOperation(process)
        self.__listProcessFinish.addProcessComplete(process)
        self.__ready_process.dequeue_process_ready()

    def __move_process_to_blocked(self, id_process, process):
        process.refresh_time_bloqued()
        process.set_quantum(-1)
        self.__bloqued_process.enqueue_process_bloqued(process)
        self.__cursorY -= 1
        self.__table_framework.set_status_process_selected(id_process, 3)
        self.__ready_process.dequeue_process_ready()

    def __move_new_process(self):
        process = create_and_return_new_process(self.__id_last_program_to_execute)
        status_add = self.__table_framework.add_process_to_table(process, 6)
        if status_add:
            self.__queue_new_process.addProcess(process)
            self.__id_last_program_to_execute += 1

    def __create_new_process(self):
        self.__move_new_process()
        if self.__block_e_s_process() is True:
            self.__cursorY += 1
        else:
            self.__cursorY -= 1

    def __detect_free_space_table_framework(self):
        process = self.__queue_new_process.getActualProcess()
        number_process = self.__ready_process.number_enqueue_process()
        number_process += self.__bloqued_process.number_process_bloqued()
        if process is not None and number_process < 5:
            self.__table_framework.set_status_process_selected(process.getNumberProgram(), 1)
            process.set_time_arrival(self.__countProgram)
            self.__ready_process.enqueue_process_ready(process)
            self.__queue_new_process.deleteLastProcess()

    def __statusOfInterruptionOutside(self, process):
        statusInterruption = self.__interruption.getStatusInterruption()
        id_process = process.getNumberProgram() if process is not None else -1
        if statusInterruption == 1 and self.__block_e_s_process() is False:
            self.__move_process_to_blocked(id_process, process)
        elif statusInterruption == 2 and self.__block_e_s_process() is False:
            self.__move_process_to_finish(process, id_process, True)
        elif statusInterruption == 0 or statusInterruption == 4:
            is_finished = process.getMaximumTime() == process.getTimeTranscurred()
            is_end_quantum = process.get_quantum() == self.__quantum
            if is_finished is True and (is_end_quantum is True or is_end_quantum is False):
                self.__move_process_to_finish(process, id_process, False)
            else:
                self.__return_process_to_ready(process, id_process)
        elif statusInterruption == 5:
            self.__create_new_process()
        self.__detect_free_space_table_framework()
        self.__interruption.setStatusInterruption(0)

    def __printProcessActual(self, process):
        idProgram = " "
        operation = " "
        timeRest = " "
        time = " "
        value_quantum = " "
        if process is not None:
            process.increment_time_transcurred()
            process.increment_quantum()
            maximunTime = process.getMaximumTime()
            idProgram = process.getNumberProgram()
            operation = str(process.getFirstNumber()) + " " + process.getOperation() + " " + str(
                process.getSecondNumber())
            time = maximunTime - process.getTimeTranscurred()
            timeRest = process.getTimeTranscurred()
            value_quantum = process.get_quantum()
        print("\r" + Cursor.FORWARD(46) + "Operacion: " + operation, end="\n")
        print("\r" + Cursor.FORWARD(46) + "ID: " + str(idProgram), end="\n")
        print("\r" + Cursor.FORWARD(46) + "Tiempo transcurrido: " + str(timeRest) +
              " \n" + Cursor.FORWARD(46) + "Tiempo restante: " + str(time) + " ", end="\n")
        print("\r" + Cursor.FORWARD(46) + "Quantum transcurrido: " + str(value_quantum), end="\n")

    def __continue_print(self):
        number_process = self.__ready_process.number_enqueue_process()
        number_process += self.__bloqued_process.number_process_bloqued()
        contains_process = True if number_process > 0 else False
        return contains_process

    def __refreshVisualInformation(self, process):
        time_transcurred = process.getTimeTranscurred() if process is not None else -1
        time_maximum = process.getMaximumTime() if process is not None else 0
        value_quantum = process.get_quantum() if process is not None else -1
        id_process = process.getNumberProgram() if process is not None else -1
        self.__table_framework.set_status_process_selected(id_process, 2)
        calculate_time_response(process, self.__countProgram)
        if time_transcurred >= time_maximum:
            self.__printProcessActual(None)
            self.__printEnqueueBloquedProcess()
            self.__countProgram += 1
        while (time_transcurred < time_maximum) and (value_quantum < self.__quantum):
            self.__interruption.listenInterruption()
            self.__printProcessActual(process)
            self.__printEnqueueBloquedProcess()
            self.__countProgram += 1
            code_continue = self.__statusOfInterruptionInside()
            time_transcurred += 1
            value_quantum += 1
            if code_continue is False:
                break
            if self.__flag_unlock_process:
                break
            if process is None:
                if self.__continue_print():
                    time_transcurred -= 1
                    value_quantum -= 1

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
        id_process = process.getNumberProgram() if process is not None else -1
        process.refresh_time_bloqued()
        self.__table_framework.set_status_process_selected(id_process, 1)
        self.__ready_process.enqueue_process_ready(process)
        self.__bloqued_process.dequeue_process_bloqued()
        self.__cursorY -= 1

    def __print_information_to_console(self, flag):
        os.system("cls")
        print(Fore.LIGHTMAGENTA_EX + "Quantum: " + str(self.__quantum), end="\n")
        process = self.__ready_process.getactual_process()
        process_new = self.__queue_new_process.getActualProcess()
        size_process_new = process_new.get_size_process() if process_new is not None else " "
        size_process = process.get_size_process() if process is not None else " "
        id_new_process = process_new.getNumberProgram() if process_new is not None else " "
        self.__ready_process.print_queue(2, 2, self.__queue_new_process.numberProcess()
                                         , size_process, size_process_new, id_new_process)
        self.__listProcessFinish.printListCompleteOfProcess(115, 8)
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
        return (self.__ready_process.number_enqueue_process() > 0) \
               or (self.__bloqued_process.number_process_bloqued() > 0)

    def __completeVistAllProcess(self):
        continue_print = self.__is_valid_continue_to_print()
        while continue_print:
            self.__print_information_to_console(True)
            continue_print = self.__is_valid_continue_to_print()
            self.__cursorY += 1
        self.__print_information_to_console(False)

    def printScreen(self):
        self.__completeVistAllProcess()
