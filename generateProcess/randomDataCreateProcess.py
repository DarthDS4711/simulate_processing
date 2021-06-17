from classes.process import Process
from classes.automaticGenererateProcess import AutomaticGenerateProcess


def create_and_return_new_process(last_id_process):
    generate_process = AutomaticGenerateProcess()
    generate_process.set_actual_id_process(last_id_process)
    return generate_process.createProcess()




