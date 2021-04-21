from classes.process import Process
from classes.queue.queueBloquedProcess import QueueBloquedProcess


def calculate_time_response(process, count_program):
    if process is not None:
        process.set_time_response(count_program)


def calculate_accountant_process(process, count_program):
    process.set_time_finish(count_program - 1)
    process.set_time_return()
    process.set_time_service()
    process.set_time_wait()


def calculate_bloqued_time(queue_bloqued_process):
    queue_bloqued_process.increment_counter_bloqued()


def is_time_bloqued_finish(queue_bloqued_process):
    process = queue_bloqued_process.getactual_process()
    if process is not None:
        if process.get_time_bloqued() == 5:
            return True
        else:
            return False
    else:
        return False
