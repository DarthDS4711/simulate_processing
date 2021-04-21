from classes.process import Process
from classes.automaticGenererateProcess import AutomaticGenerateProcess


def __create_and_return_new_process(last_id_process):
    generate_process = AutomaticGenerateProcess()
    generate_process.set_actual_id_process(last_id_process)
    return generate_process.createProcess()


def add_new_process_to_simulation(last_id_program, queue_process_new):
    process = __create_and_return_new_process(last_id_program)
    queue_process_new.addProcess(process)



