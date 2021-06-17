from colorama import *


class QueueReadyProcess:
    def __init__(self):
        self.__queue = []

    def enqueue_process_ready(self, process):
        self.__queue.append(process)

    def dequeue_process_ready(self):
        if len(self.__queue) > 0:
            self.__queue.pop(0)

    def getactual_process(self):
        if len(self.__queue) > 0:
            return self.__queue[0]
        else:
            return None

    def number_enqueue_process(self):
        return len(self.__queue)

    def print_queue(self, x, y, number_process, size, size_new, id):
        print(Cursor.UP(y) + Cursor.FORWARD(x - 1) + Fore.LIGHTRED_EX + "N# process new: " +
              str(number_process) + "|| size new: " + str(size_new) + " ID: " + str(id), end="\n")
        print(Cursor.FORWARD(x - 1) + Fore.LIGHTGREEN_EX + "Procesos listos || act size process: " + str(size), end="")
        print(Fore.RESET)
        for index in range(1, 6):
            if index >= len(self.__queue):
                print(" ", end="\n")
            else:
                print(Cursor.FORWARD(x) + " process: ", self.__queue[index], end="\n")

    def create_table_bcp_actual(self, table_bcp):
        for index in range(0, len(self.__queue)):
            table_bcp.append(self.__queue[index])