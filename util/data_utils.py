import pandas as pd

def read_data_from_file(file_path):

    file = pd.ExcelFile(file_path)
    df = pd.read_excel(file, sheet_name="Categories", header=0)

    return file, df
