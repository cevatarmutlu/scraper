from typing import List, Union
import pandas as pd

def get_urls(file_path, sheet_name, header, column_name):


    assert type(file_path) == str, "file_path must be str. file_path referenced excel file"
    assert type(sheet_name) == str, "sheet_name must be str."
    assert header == None and type(column_name) == int, "column_name must be."

    df = pd.read_excel(io=file_path, sheet_name=sheet_name, header=header)
    return df[column_name].tolist()
