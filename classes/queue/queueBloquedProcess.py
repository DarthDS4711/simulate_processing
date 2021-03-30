from classes.process import Process
from colorama import *

init()


class QueueBloquedProcess:
    def __init__(self):
        self.__queue = []

    def enqueue_process_bloqued(self, process):
        self.__queue.append(process)

    def dequeue_process_bloqued(self):
        if len(self.__queue) > 0:
            self.__queue.pop(0)

    def getactual_process(self):
        if len(self.__queue) > 0:
            return self.__queue[0]
        else:
            return None

    def print_queue(self):
        print('\r' + Fore.LIGHTRED_EX + "Procesos bloqueados" + Fore.RESET, end="\n")
        for index in range(0, 5):
            if index >= len(self.__queue):
                print(" ", end="\n")
            else:
                print('\r' + "process: ", self.__queue[index], end="\n")
