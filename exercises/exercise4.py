import urllib.request
import zipfile
import pandas as pd
import sqlite3


zip_file_url = "https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip"
data_file_name = "data.csv"
zip_file_name = "exercises/mowesta-dataset.zip"

urllib.request.urlretrieve(zip_file_url, zip_file_name)

with zipfile.ZipFile(zip_file_name) as zip_ref:
    zip_ref.extract(data_file_name, path="exercises")


df = pd.read_csv(
    "exercises/data.csv",
    usecols=range(15),
    encoding="utf-8",
    sep=";",
)
df = df.reset_index()
rename_columns = {
    "level_0": "Geraet",
    "level_1": "Hersteller",
    "level_2": "Model",
    "level_3": "Monat",
    "level_4": "Temperatur",
    "level_5": "Latitude (WGS84)",
    "level_6": "Longitude (WGS84)",
    "level_7": "Verschleierung (m)",
    "level_8": "Aufenthaltsdauer im Freien (ms)",
    "level_9": "Batterietemperatur",
    "level_10": "Geraet aktiv",
}
df.rename(
    columns=rename_columns,
    inplace=True,
)
df = df.iloc[:, :11]
df = df.drop(
    [
        "Verschleierung (m)",
        "Aufenthaltsdauer im Freien (ms)",
        "Longitude (WGS84)",
        "Latitude (WGS84)",
    ],
    axis=1,
)


df["Temperatur"] = df["Temperatur"].str.replace(",", ".")
df["Temperatur"] = df["Temperatur"].astype(float)
df["Temperatur"] = (df["Temperatur"] * 9 / 5) + 32
df["Temperatur"] = df["Temperatur"].round(2)

df["Batterietemperatur"] = df["Batterietemperatur"].str.replace(",", ".")
df["Batterietemperatur"] = df["Batterietemperatur"].astype(float)
df["Batterietemperatur"] = (df["Batterietemperatur"] * 9 / 5) + 32
df["Batterietemperatur"] = df["Batterietemperatur"].round(2)


df = df[df["Geraet"] > 0]
df = df[df["Geraet"] > 0]

database_name = "exercises/temperatures.sqlite"
table_name = "temperatures"

conn = sqlite3.connect(database_name)
df.to_sql(table_name, conn, if_exists="replace", index=False)

conn.close()
