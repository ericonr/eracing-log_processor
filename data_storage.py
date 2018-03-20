#tentando deixar OO

class DataStore():
    def __init__(self):
        self.loaded = False

class PIR(DataStore):
    def __init__(self, pir_type):
        self.type = pir_type
        filenames = {'PirF':'Final_Log_PirF.csv', 'PirR':'Final_Log_PirR.csv', 'PirF_filtrado':'Final_Log_PirF_Filtro.csv', 'PirR_filtrado':'Final_Log_PirR_Filtro.csv'}
        self.filename = filenames[self.type]