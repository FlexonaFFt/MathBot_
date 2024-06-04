import math_path as m

file = 'test_data.xlsx'
obj = m.RegressionModelXI3(file)
obj.read_data()
obj.kef_det()