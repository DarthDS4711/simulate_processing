from colorama import *


class Framework:
    def __init__(self, number_framework):
        self.__used_size = 0
        self.__id_process_associate = 0
        self.__number_framework = number_framework
        self.__status_process = 5

    def set_status_process(self, status):
        self.__status_process = status

    def get_status_process(self):
        return self.__status_process

    def set_id_process_associate(self, id_process):
        self.__id_process_associate = id_process

    def get_id_process_associate(self):
        return self.__id_process_associate

    def set_used_size(self, used_size):
        self.__used_size = used_size

    def get_used_size(self):
        return self.__used_size

    def __return_state_process(self):
        chain = ""
        if self.__status_process == 1:
            chain = Fore.BLUE + "Ready" + Fore.RESET
        elif self.__status_process == 2:
            chain = Fore.GREEN + "Execution" + Fore.RESET
        elif self.__status_process == 3:
            chain = Fore.RED + "Blocked" + Fore.RESET
        elif self.__status_process == 4:
            chain = Fore.LIGHTBLACK_EX + "SO" + Fore.RESET
        elif self.__status_process == 5:
            chain = Fore.LIGHTMAGENTA_EX + "Unused" + Fore.RESET
        return chain

    def return_framework(self):
        chain = "page #: " + str(self.__number_framework) + " used size: " \
                + str(self.__used_size) + "/4" + " stat p: " + \
                self.__return_state_process() + " id: " + str(self.__id_process_associate)
        return chain
