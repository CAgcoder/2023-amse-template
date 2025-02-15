import pandas as pd
import ssl
import sqlite3

url1 = "https://opendata.stadt-muenster.de/sites/default/files/Fahrzeugbestand-Regierungsbezirk-Muenster-2018-2022.xlsx"
url2 = "https://www.stadt-muenster.de/fileadmin/user_upload/stadt-muenster/61_stadtentwicklung/pdf/sms/05515000_csv_bevoelkerungsentwicklung_geschlecht.csv"
url3 = "https://www.stadt-muenster.de/fileadmin/user_upload/stadt-muenster/61_stadtentwicklung/pdf/sms/05515000_csv_bevoelkerungsentwicklung_altersgruppen.csv"
url4 = "https://www.stadt-muenster.de/fileadmin/user_upload/stadt-muenster/61_stadtentwicklung/pdf/sms/05515000_csv_bevoelkerungsentwicklung_staatsangehoerigkeit.csv"


def excel_extraction(url):
    ssl._create_default_https_context = ssl._create_unverified_context
    df = pd.read_excel(url)

    return df


def excel_preprocessing(df):
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

    return df


def csv_extraction(url):
    df = pd.read_csv(url, encoding="ISO-8859-1")

    return df


def csv_preprocessing(df):
    df[["ZEIT", "RAUM", "MERKMAL", "WERT"]] = df["ZEIT;RAUM;MERKMAL;WERT"].str.split(
        ";", expand=True
    )
    df.drop(["ZEIT;RAUM;MERKMAL;WERT"], axis=1, inplace=True)

    return df


def store_data(df, name, databasename):
    conn = sqlite3.connect(databasename)
    df.to_sql(name, conn, if_exists="replace", index=False)
    conn.close()


def main():
    df1 = excel_extraction(url1)
    excel_preprocessing(df1)
    databasename = "./data/mydatabase.sqlite"
    store_data(df1, "Fahrzeugbestand_Excel", databasename)
    df2 = csv_extraction(url2)
    csv_preprocessing(df2)
    store_data(df2, "Bevoelkerungsentwicklung_mit_geschlecht", databasename)
    df3 = csv_extraction(url3)
    csv_preprocessing(df3)
    store_data(df3, "Bevoelkerungsentwicklung_mit_altersgruppen", databasename)
    df4 = csv_extraction(url4)
    csv_preprocessing(df4)
    store_data(df4, "Bevoelkerungsentwicklung_mit_staatsangehoerigkeit", databasename)


if __name__ == "__main__":
    main()
