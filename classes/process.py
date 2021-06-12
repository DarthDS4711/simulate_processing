class Process:
    def __init__(self, operation, maximumTime, numberProgram, number1, number2, size_process):
        self.__operation = operation
        self.__maximumTime = maximumTime
        self.__numberProgram = numberProgram
        self.__number1 = number1
        self.__number2 = number2
        self.__result = "Error"
        self.__timeTranscurred = -1
        self.__time_arrival = -1
        self.__time_finish = 0
        self.__time_return = 0
        self.__time_response = -1
        self.__time_wait = 0
        self.__time_service = 0
        self.__execute_first_time = False
        self.__time_bloqued = 0
        self.__quantum = -1
        self.__size_process = size_process

    def set_size_process(self, size):
        self.__size_process = size

    def get_size_process(self):
        return self.__size_process

    def setTimeTranscurred(self, time):
        self.__timeTranscurred = time

    def getTimeTranscurred(self):
        return self.__timeTranscurred

    def increment_time_transcurred(self):
        self.__timeTranscurred += 1

    def getOperation(self):
        return self.__operation

    def getMaximumTime(self):
        return self.__maximumTime

    def getNumberProgram(self):
        return self.__numberProgram

    def getFirstNumber(self):
        return self.__number1

    def getSecondNumber(self):
        return self.__number2

    def get_quantum(self):
        return self.__quantum

    def set_quantum(self, quantum):
        self.__quantum = quantum

    def increment_quantum(self):
        self.__quantum += 1

    def __str__(self):
        time = self.__timeTranscurred if self.__timeTranscurred >= 0 else 0
        chain = "ID: " + str(self.__numberProgram) + " " + \
                "TME: " + str(self.__maximumTime) + " " + \
                "TT: " + str(time) + " Size: " + str(self.__size_process)
        return chain

    def getResult(self):
        return self.__result

    def setResult(self, result):
        self.__result = result

    def toStringProcessComplete(self):
        chain = "ID: " + str(self.__numberProgram) + "  ope: " + \
                self.__operation + " result: " + str(self.__result)
        return chain

    def print_counters_process(self):
        if self.__time_arrival == -1:
            return self.__counters_new_process()
        elif self.__time_finish == 0 and self.__time_bloqued == 0:
            return self.__calculate_counter_non_finish_process()
        elif self.__time_bloqued >= 1:
            return self.__counter_bloqued_process()
        else:
            return self.__calculate_counter_finish_process()

    def __counters_new_process(self):
        chain = "ID: " + str(self.__numberProgram) + " TLL: " + \
                " TF: " + " TW: " + " TS: " + " TRET: " + " TRES: " + \
                " status: " + " TME: "
        return chain

    def __counter_bloqued_process(self):
        chain = "ID: " + str(self.__numberProgram) + " TLL: " + str(self.__time_arrival) \
                + " TW: " + str(self.__time_wait) + \
                " TS: " + str(self.__time_service) + " TRES: " + str(self.__time_response) + \
                " status: en memoria bloqueado" + " TB: " + str(self.__time_bloqued - 1) +\
                " TME: " + str(self.__maximumTime)
        return chain

    def __calculate_counter_finish_process(self):
        is_terminated = "terminado" if self.__time_service == self.__maximumTime \
            else "no terminado por error"
        chain = "ID: " + str(self.__numberProgram) + " TLL: " + str(self.__time_arrival) \
                + " TF: " + str(self.__time_finish) + " TW: " + str(self.__time_wait) + \
                " TS: " + str(self.__time_service) + " TRET: " + \
                str(self.__time_return) + " TRES: " + str(self.__time_response) + \
                " status: " + is_terminated + " TME: " + str(self.__maximumTime) +\
                " operacion: " + self.__operation + " datos: " + str(self.__number1) + \
                ", " + str(self.__number2) + " result: " + str(self.__result)
        return chain

    def __calculate_counter_non_finish_process(self):
        time_wait = self.__time_wait if self.__time_wait >= 0 else 0
        time_service = self.__time_service if self.__time_service >= 0 else 0
        time_res = self.__time_response if self.__time_response >= 0 else " "
        chain = "ID: " + str(self.__numberProgram) + " TLL: " + str(self.__time_arrival) \
                + " TW: " + str(time_wait) + \
                " TS: " + str(time_service) + " TRES: " + str(time_res) + \
                " status: en memoria" + " TME: " + str(self.__maximumTime)
        return chain

    def print_process_bloqued(self):
        chain = "ID: " + str(self.__numberProgram) + " TB: " + \
                str(self.__time_bloqued)
        return chain

    def setOperation(self, operation):
        self.__operation = operation

    def set_time_arrival(self, time_arrival):
        self.__time_arrival = time_arrival

    def set_time_finish(self, time_finish):
        self.__time_finish = time_finish

    def get_time_finish(self):
        return self.__time_finish

    def set_time_return(self):
        self.__time_return = self.__time_finish - self.__time_arrival

    def set_time_response(self, count_program):
        if not self.__execute_first_time:
            self.__time_response = count_program - self.__time_arrival
            self.__execute_first_time = True

    def set_time_wait(self):
        self.__time_wait = self.__time_return - self.__time_service

    def set_time_service(self):
        self.__time_service = self.__timeTranscurred

    def get_flag_execute(self):
        return self.__execute_first_time

    def set_flag_execute(self, execute_first_time):
        self.__execute_first_time = execute_first_time

    def get_time_bloqued(self):
        return self.__time_bloqued

    def get_time_arrival(self):
        return self.__time_arrival

    def increment_time_bloqued(self):
        self.__time_bloqued = self.__time_bloqued + 1

    def refresh_time_bloqued(self):
        self.__time_bloqued = 0
