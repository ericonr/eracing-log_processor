class DataStore():
    def __init__(self, data_loader, filename):
        self._data_loader = data_loader
        self._loaded = False
        self._filename = filename

    def verify_loaded(self):
        if not self._loaded:
            self.__data = self._data_loader.load_data(self._filename, self.headers)
            self._loaded = True

    @property
    def data(self):
        self.verify_loaded()
        return self.__data
    @data.setter
    def data(self, x):
        pass

class PIR(DataStore):
    headers = ['left', 'right', 'avg_r', 'avg_k', 'time']

    def __init__(self, data_loader, pir_type='PirF'):
        self.type = pir_type
        filenames = {'PirF':'Final_Log_PirF.csv', 'PirR':'Final_Log_PirR.csv', 'PirF_filtrado':'Final_Log_PirF_Filtro.csv', 'PirR_filtrado':'Final_Log_PirR_Filtro.csv'}
        
        DataStore.__init__(self, data_loader, filenames[self.type])

class MotorSpeed(DataStore):
    headers = ['motor', 'torque', 'phase', 'power', 'speed', 'distance', 'time']

    def __init__(self, data_loader):
        DataStore.__init__(self, data_loader, 'Final_Log_VCU_Info_1.csv')