class ListProcessNew:
    def __init__(self):
        self.__list = []

    def addProcess(self, process):
        self.__list.append(process)

    def numberProcess(self):
        return len(self.__list)

    def getActualProcess(self):
        if len(self.__list) > 0:
            return self.__list[0]
        else:
            return None

    def deleteLastProcess(self):
        if len(self.__list) > 0:
            self.__list.pop(0)

    def create_table_bcp_actual(self, table_bcp):
        for index in range(0, len(self.__list)):
            table_bcp.append(self.__list[index])



