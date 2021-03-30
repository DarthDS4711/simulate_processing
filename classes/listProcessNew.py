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



