import psycopg2
import configparser
import os
import pandas as pd


config = configparser.ConfigParser()
config.read(os.path.expanduser('~/db_config.ini'))

def db_connection():
    conn = psycopg2.connect(
            database=config['DB']['DATABASE'],
            host=config['DB']['HOST'],
            port=config['DB']['PORT'],
            user=config['DB']['USERNAME'],
            password=config['DB']['PASSWORD']
      )
    return conn


def roll_back_from_sql_erorr(connection):
    cursor = connection.cursor()
    cursor.execute('rollback;')

    
# roll_back_from_sql_erorr(con)
def dataframe_from_sql_query(connection, sql_query):
    cursor = connection.cursor()
    cursor.execute(sql_query)
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    return pd.DataFrame(list(rows), columns=column_names)


def load_data_from_sql(file_name):
    sql_path = '/Users/haitaoliu/Documents/reserving_analysis/sql/'
    fd = open(sql_path + file_name, 'r')
    sqlFile = fd.read()
    fd.close()
    
    con = db_connection()
    roll_back_from_sql_erorr(con)
    df = dataframe_from_sql_query(con, sqlFile)
    return df



# test
# df_claim = dataframe_from_sql_query(con, 'select * from edw.fact_financials_accumulating limit 10')