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

    def print_queue(self, x, y, number_process_new):
        print(Fore.RED + Cursor.UP(y) + Cursor.FORWARD(x) +
              "Numero de procesos nuevos: ", number_process_new)
        print(Fore.LIGHTGREEN_EX + Cursor.FORWARD(x) + "Procesos listos")
        print(Fore.RESET)
        for index in range(1, 6):
            if index >= len(self.__queue):
                print(" ", end="\n")
            else:
                print(Cursor.FORWARD(x) + "process: ", self.__queue[index], end="\n")