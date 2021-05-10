from vist.vistProcess import VistProcess
from classes.automaticGenererateProcess import AutomaticGenerateProcess


def main():
    addProcess = AutomaticGenerateProcess()
    addProcess.addingProcess()
    quantum = addProcess.value_of_quantum()
    vist = VistProcess(addProcess.get_new_process(), quantum)
    vist.add_process_ready()
    vist.printScreen()
    input("Fin del programa")


if __name__ == '__main__':
    main()
