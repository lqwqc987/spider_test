import logging
class LogFile:
    def __init__(self,fileName,level=logging.INFO):
        fh = logging.FileHandler(fileName)
        self.logger = logging.getLogger()
        self.logger.setLevel(level)
        formatter = logging.Formatter('%(asctime)s : %(message)s','%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def setLog(self,message):
        self.logger.info(message)

    def setErrorLog(self,message):
        self.logger.error(message)
