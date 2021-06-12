from classes.pagination.framework import Framework
from colorama import *


class TableFrames:
    def __init__(self):
        self.__table_frames = []
        self.__flag_full_capacity_exceded = False

    def inicialize_table_frame(self):
        for index in range(0, 45):
            frame = Framework(index + 1)
            self.__table_frames.append(frame)

    def __return_number_pages_required(self, process):
        continue_calculate_number_pages = True
        size_process = process.get_size_process()
        number_pages_required = 0
        while continue_calculate_number_pages:
            if (size_process - 4) > 0:
                size_process -= 4
                number_pages_required += 1
            else:
                continue_calculate_number_pages = False
        if size_process > 0:
            number_pages_required += 1
        return number_pages_required

    def __detect_free_pages(self):
        number_pages_free = 0
        for index in range(0, 45):
            if self.__table_frames[index].get_used_size() == 0:
                number_pages_free += 1
        return number_pages_free

    def is_full_table(self):
        return self.__flag_full_capacity_exceded

    def __add_process_to_frames(self, process, number_pages_required):
        size_process = process.get_size_process()
        number_pages = number_pages_required - 1
        for index in range(0, 45):
            if self.__table_frames[index].get_used_size() == 0:
                if number_pages_required > 1:
                    self.__table_frames[index].set_id_process_associate(process.getNumberProgram())
                    self.__table_frames[index].set_used_size(4)
                    number_pages_required -= 1
                elif number_pages_required == 1:
                    number_pages = number_pages * 4
                    size_process = size_process - number_pages
                    if size_process > 0:
                        self.__table_frames[index].set_used_size(size_process)
                        self.__table_frames[index].set_id_process_associate(process.getNumberProgram())
                        number_pages_required -= 1
                else:
                    break


    def add_process_to_table(self, process):
        number_pages_required = self.__return_number_pages_required(process)
        number_pages_free = self.__detect_free_pages()
        if number_pages_free >= number_pages_required:
            self.__add_process_to_frames(process, number_pages_required)
        if number_pages_free == 0:
            self.__flag_full_capacity_exceded = True

    def print_table_frame(self, y):
        number_process = 0
        text_to_print = ""
        print(Cursor.DOWN(y) + Fore.YELLOW + "Tabla de paginas" + Fore.RESET)
        for index in range(0, 45):
            if number_process == 3:
                print(text_to_print, end="\n")
                number_process = 0
                text_to_print = ""
            text_to_print = text_to_print + "  " + self.__table_frames[index].return_framework()
            number_process += 1
        print(text_to_print, end="\n")
