import pandas as pd
import sqlite3
from script import (
    store_data,
    excel_preprocessing,
    excel_extraction,
    csv_extraction,
    csv_preprocessing,
)
from pandas.testing import assert_frame_equal


def test_excelextract():
    df = excel_extraction(
        "https://opendata.stadt-muenster.de/sites/default/files/Fahrzeugbestand-Regierungsbezirk-Muenster-2018-2022.xlsx"
    )
    assert not df.empty, "excel_extraction() failed"


def test_excelpreprocessing():
    df = excel_extraction(
        "https://opendata.stadt-muenster.de/sites/default/files/Fahrzeugbestand-Regierungsbezirk-Muenster-2018-2022.xlsx"
    )
    df = excel_preprocessing(df)
    assert df.isna().any().any() == False, "There is NAN in dataset"


def test_csvextract():
    df = csv_extraction(
        "https://www.stadt-muenster.de/fileadmin/user_upload/stadt-muenster/61_stadtentwicklung/pdf/sms/05515000_csv_bevoelkerungsentwicklung_geschlecht.csv"
    )
    assert not df.empty, "csv_extraction()failed"


def test_csvpreprocessing():
    df = df = csv_extraction(
        "https://www.stadt-muenster.de/fileadmin/user_upload/stadt-muenster/61_stadtentwicklung/pdf/sms/05515000_csv_bevoelkerungsentwicklung_geschlecht.csv"
    )
    df = csv_preprocessing(df)
    expect_cloum = ["ZEIT", "RAUM", "MERKMAL", "WERT"]
    assert list(df.columns) == expect_cloum, "csv_preprocessing()failed"


def test_store_data():
    data = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=["a", "b", "c"])
    store_data(data, "test_load.sqlite")

    conn = sqlite3.connect("test_load.sqlite")
    result = pd.read_sql_query("SELECT * FROM example_table", conn)
    conn.close()

    assert_frame_equal(result, data)


def test_pipeline():
    test_excelextract()
    test_excelpreprocessing()
    test_csvextract()
    test_csvpreprocessing()
    test_store_data()
