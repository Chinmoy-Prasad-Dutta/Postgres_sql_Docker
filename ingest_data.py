import pandas as pd
import time
from time import time
import os
import argparse

from sqlalchemy import create_engine as ce


def load_db_to_project(params):

    user = params.user
    password = params.password
    host = params.host
    host = params.host
    port = params.port
    db = params.db
    folder_path = params.folder_path
    # engine = params.engine
    # url = params.url
    # table_name = params.table_name
    # csv_name = "output.csv"

    """Loops through all CSV files in a folder and attempts to print their schema to the console.

    Args:
        folder_path: Path to the folder containing the CSV files.
        engine: A SQLAlchemy engine object for database connection (if applicable).
    """

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            print(f"Processing CSV file: {filename}")

            engine = ce(f"postgresql://{user}:{password}@{host}:{port}/{db}")

            # Read the CSV data into a DataFrame (assuming no schema is provided)
            try:
                df = pd.read_csv(os.path.join(folder_path, filename))
                if engine is not None:
                    # If engine is provided, attempt to print schema using SQLAlchemy
                    print(pd.io.sql.get_schema(df, name=f"{filename}", con=engine))
                else:
                    # If no engine, print basic column information
                    print(df.dtypes)  # Print data types of each column
            except FileNotFoundError:
                print(f"Error: File not found - {filename}")

            df_iter = pd.read_csv(
                os.path.join(folder_path, filename),
                iterator=True,
                chunksize=100000,
            )

            count = 0
            while True:
                try:
                    df = next(df_iter)
                    table_name = filename[:-4]
                    df.to_sql(name=table_name, con=engine, if_exists="append")
                    count += 1
                    print(f"{count}")
                    print("--------------")
                except StopIteration:
                    # Handle the end of the iterator here
                    print("Reached the end of the iterator. Stopping...")
                    break  # Exit the loop


# Example usage (assuming you have a database connection established in engine)
# folder_path = r"I:\2-Docker_sql_PROJECT\DATA"
# engine = ce("postgresql://root:root@localhost:5432/project")
# load_db_to_project(folder_path, engine)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest csv data to Postgres")
    # user, password , host, port, databse name, table name, url of the csv
    parser.add_argument("--user", help="user name for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--db", help="database name")
    # parser.add_argument("--table_name", help="name of the table to write results to")
    # parser.add_argument("--url", help="url of the csv file")
    parser.add_argument("--folder_path", help="folder_path of the csv file")
    # parser.add_argument("--engine", help="engine for pgadmin")

    args = parser.parse_args()

    load_db_to_project(args)
