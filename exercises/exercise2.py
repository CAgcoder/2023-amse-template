import pandas as pd
import sqlite3


def read_data(url):
    df_trainstop = pd.read_csv(url, sep=";")
    return df_trainstop


def drop_colum(df, column_name):
    df = df.drop(column_name, axis=1)
    return df


def drop_invalid_row(df, column_name, valid):
    df = df.fillna(pd.NA)
    df = df.dropna()
    if isinstance(valid, list) and all(isinstance(item, str) for item in valid):
        df = df.drop(df[~df[column_name].isin(valid)].index)
        return df
    elif isinstance(valid, (float, int)):
        df[column_name] = df[column_name].str.replace(",", ".").astype(float)
        df = df.drop(df[df[column_name] < -valid].index)
        df = df.drop(df[df[column_name] > valid].index)
        return df
    elif column_name == "IFOPT":
        df = df.drop(df[~df[column_name].str.match(valid, na=False)].index)
        return df


def store_data(df, name, address, data_type):
    conn = sqlite3.connect(address)
    df.to_sql(name, conn, if_exists="replace", index=False, dtype=data_type)
    conn.close()


def main():
    data_url = "https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV"
    df = read_data(data_url)
    df1 = drop_colum(df, "Status")
    valid_Verkehr = ["RV", "FV", "nur DPN"]
    df2 = drop_invalid_row(df1, "Verkehr", valid_Verkehr)
    df3 = drop_invalid_row(df2, "Laenge", 90)
    df4 = drop_invalid_row(df3, "Breite", 90)
    df5 = drop_invalid_row(df4, "IFOPT", r"^[A-Za-z]{2}:\d+:\d+(?::\d+)?$")
    store_data(
        df5,
        "trainstops",
        "trainstops.sqlite",
        {
            "ID": "BIGINT",
            "Verkehr": "TEXT",
            "Laenge": "FLOAT",
            "Breite": "FLOAT",
            "IFOPT": "TEXT",
            "Betreiber_Nr": "INT",
        },
    )


if __name__ == "__main__":
    main()
