import os
from copy import deepcopy
from datetime import datetime
import streamlit as st
import pandas as pd
from bledot_dash_src.session_state import (
    get_session_state,
    init_session_state,
    check_session_state,
)


def get_download_data(df: pd.DataFrame) -> bytes:
    if check_session_state("download_data"):
        return get_session_state("download_data")

    csv_df = deepcopy(df)
    sheet_path = os.path.join(get_session_state("download_dir"), r"sheet.csv")

    if type(csv_df["data_coleta"][0]) is not str:
        csv_df["data_coleta"] = csv_df["data_coleta"].apply(
            lambda x: x.strftime("%y-%m-%d %H:%M:%S.%f")
        )

    csv_df.to_csv(sheet_path, index=False)

    with open(sheet_path, "rb") as sheet:
        return sheet.read()
