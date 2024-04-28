import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd

class RegressionModelXI3:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.read_data()
        self.yi = self.data['yi']
        self.xi1 = self.data['xi1']
        self.xi2 = self.data['xi2']
        self.xi3 = self.data['xi3']
    
    def read_data(self):
        data = pd.read_csv(self.file_path, sep='\t', header=None, names=['yi', 'xi1', 'xi2', 'xi3'])
        return data

    # Коэффициент детерминации
    def kef_det(self):
        X = np.column_stack((np.ones(len(self.xi1)), self.xi1, self.xi2, self.xi3))
        model = sm.OLS(self.yi, X).fit()
        return model.summary()
    
obj = RegressionModelXI3('test_data.txt')
obj.read_data()
obj.kef_det()