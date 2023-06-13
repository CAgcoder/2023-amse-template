import pandas as pd
import sqlite3
import ssl
from datapipline_script import (
    store_data,
    excel_preprocessing,
    # excel_extraction,
    # csv_extraction,
    # csv_preprocessing,
)
from pandas.testing import assert_frame_equal

excel_url = "https://opendata.stadt-muenster.de/sites/default/files/Fahrzeugbestand-Regierungsbezirk-Muenster-2018-2022.xlsx"
csv_url = "https://www.stadt-muenster.de/fileadmin/user_upload/stadt-muenster/61_stadtentwicklung/pdf/sms/05515000_csv_bevoelkerungsentwicklung_geschlecht.csv"


def test_excelextract():
    ssl._create_default_https_context = ssl._create_unverified_context
    df = pd.read_excel(excel_url)
    assert not df.empty, "excel_extraction() failed"


def test_excelpreprocessing():
    ssl._create_default_https_context = ssl._create_unverified_context
    df = pd.read_excel(excel_url)

    # df = excel_preprocessing(df)

    df.iloc[:, 0].fillna(method="ffill", inplace=True)
    df.iloc[:, 1].fillna(method="ffill", inplace=True)

    columns = list(df.columns)
    previous_value = "Begin"

    for i, value in enumerate(columns):
        if value == "Unnamed: {}".format(i):
            if i > 2:
                columns[i] = previous_value + "{}".format(i)
            else:
                columns[i] = previous_value + "{}".format(i)
        else:
            previous_value = value
            columns[i] = value + "{}".format(i)
    df.columns = columns

    assert df.iloc[:, 0:2].isna().any().all() == False, "There is NAN in dataset"
    assert df.iloc[:, 8].isna().any().all() == False, "There is NAN in dataset"


def test_csvextract():
    df = pd.read_csv(csv_url, encoding="ISO-8859-1")
    assert not df.empty, "csv_extraction()failed"


def test_csvpreprocessing():
    df = pd.read_csv(csv_url, encoding="ISO-8859-1")
    df[["ZEIT", "RAUM", "MERKMAL", "WERT"]] = df["ZEIT;RAUM;MERKMAL;WERT"].str.split(
        ";", expand=True
    )
    df.drop(["ZEIT;RAUM;MERKMAL;WERT"], axis=1, inplace=True)
    expect_cloum = ["ZEIT", "RAUM", "MERKMAL", "WERT"]
    assert list(df.columns) == expect_cloum, "csv_preprocessing()failed"


def test_store_data():
    data = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=["a", "b", "c"])
    databasename = "test_load.sqlite"
    tablename = "example_table"
    store_data(data, tablename, databasename)

    conn = sqlite3.connect("test_load.sqlite")
    result = pd.read_sql_query("SELECT * FROM example_table", conn)
    conn.close()

    assert_frame_equal(result, data)


# def test_pipeline():
#     test_excelextract(excel_url)
#     test_excelpreprocessing(excel_url)
#     test_csvextract(csv_url)
#     test_csvpreprocessing(csv_url)
#     test_store_data()
