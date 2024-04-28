import math_path as mp

file_path = 'test_data.xlsx'
math_path_obj = mp.RegressionModelXI3(file_path)
math_path_obj.read_data()
math_path_obj.kef_det()