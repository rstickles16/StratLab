import pandas as pd

def write_to_excel(
        writer: pd.ExcelWriter,
        df: pd.DataFrame,
        sheet_name: str = 'sheet1'
):
    df.to_excel(writer, sheet_name=sheet_name)
