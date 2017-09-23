import psycopg2

def connection():
    conn=psycopg2.connect(host='localhost',port='5432',database='pythonprogramming',user='root',password='root')
    c=conn.cursor()
    return c,conn