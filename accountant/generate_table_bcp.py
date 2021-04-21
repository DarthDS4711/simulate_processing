from accountant.calculate_accountant import calculate_accountant_process

def generate_bcp_per_process(queue_new, queue_bloqued, queue_ready, finished, table_bcp, clock):
    queue_new.create_table_bcp_actual(table_bcp)
    queue_bloqued.create_table_bcp_actual(table_bcp)
    queue_ready.create_table_bcp_actual(table_bcp)
    finished.create_table_bcp_actual(table_bcp)
    __calculate_bcp_per_process(table_bcp, clock)


def __calculate_bcp_per_process(table_bcp, clock):
    for index in range(0, len(table_bcp)):
        process = table_bcp[index]
        if process.get_time_arrival() != -1:
            if process.get_time_finish() == 0:
                calculate_accountant_process(process, clock)
                process.set_time_finish(0)
            else:
                calculate_accountant_process(process, clock)
            table_bcp[index] = process

