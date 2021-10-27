from typing import List, Union
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def get_urls(file_path: str, sheet_name: str, header: Union[int, None], column: Union[str, int]) -> List[str]:

    """
        Reads column that included URLs from the excel file.

        Args:
            file_path(str): Excel file path.
            sheet_name(str): Sheet name in excel file
            header(int | None): Specifies whether there is header row in the excel file. If there is header row in the excel file then, header variable is row number of header column otherwise None.
            column(str | int): name or index number of URL column in the excel file.
        
        Returns:
            (List[int]): This list includes URLs.
    """

    assert type(file_path) == str, "file_path variable must be str."
    assert type(sheet_name) == str, "sheet_name variable must be str."
    assert type(header) == int or header == None, "header variable must be int or None"
    assert type(column) in (str, int), "column variable must be str or int"

    logger.info('Started reading URLs in Excel file')

    df = pd.read_excel(io=file_path, sheet_name=sheet_name, header=header)
    return_data = df[column].tolist()


    logger.info(f'Reading the Excel file is completed. number of URLs: {len(return_data)}')
    return return_data

