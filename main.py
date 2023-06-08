from flask import request
from flask import Flask
from flask import render_template
import pyodbc
import os

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient, BlobServiceClient

account_url = "https://shruthaja.blob.core.windows.net/"

creds = DefaultAzureCredential()
service_client = BlobServiceClient(
    account_url=account_url,
    credential=creds
)

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
@app.route("/", methods=['GET'])

def hello_world():
    name = ""
    salpics = []
    picture=''
    if request.method == "GET":
        name = request.args.get('name')
        server = 'assignmentservershruthaja.database.windows.net'
        database = 'assignment1'
        username = 'shruthaja'
        password = 'mattu4-12'
        driver = '{ODBC Driver 17 for SQL Server}'

        # Establish the connection
        conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')

        # Create a cursor object
        cursor = conn.cursor()
        print(cursor)
        # Execute a simple select query
        if(name=="all"):
            query = "SELECT Picture FROM dbo.people where Salary<9000"
            cursor.execute(query)
            # Fetch the first row from the result set
            rows = cursor.fetchall()
            for i in rows:
                salpics.append(i[0])

        else:
            query = "SELECT Picture FROM dbo.people WHERE name = ?"
            cursor.execute(query, name)

            # Fetch the first row from the result set
            row = cursor.fetchone()
            if row is not None:
                picture = row.Picture
            else:
                picture = None

    return render_template("index.html", name=name, picture=picture,salpics=salpics)

@app.route("/change.html",methods=['GET', 'POST'])
def change():
    name=""
    row=''
    row2=""
    keywords=""
    sname = ""
    salary = ""
    if request.method == "GET":
        name=request.args.get('cname')
        keywords=request.args.get('keywords')
        server = 'assignmentservershruthaja.database.windows.net'
        database = 'assignment1'
        username = 'shruthaja'
        password = 'mattu4-12'
        driver = '{ODBC Driver 17 for SQL Server}'
        # Establish the connection
        conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        # Create a cursor object
        cursor = conn.cursor()
        query = "update dbo.people set Keywords=? where name=?"
        conn.commit()
        cursor.execute(query,keywords,name)
        # Fetch the first row from the result set
        cursor = conn.cursor()
        conn.commit()
        query="Select * from dbo.people where name=?"
        cursor.execute(query, name)
        row = cursor.fetchone()
        print(row)
    if request.method == "POST":
        sname=request.form['sname']
        salary=request.form['salary']
        server = 'assignmentservershruthaja.database.windows.net'
        database = 'assignment1'
        username = 'shruthaja'
        password = 'mattu4-12'
        driver = '{ODBC Driver 17 for SQL Server}'
        # Establish the connection
        conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        # Create a cursor object
        cursor = conn.cursor()
        query = "update dbo.people set Salary=? where name=?"
        cursor.execute(query, salary, sname)
        conn.commit()
        query = "Select * from dbo.people where name=?"
        cursor.execute(query, sname)
        row2= cursor.fetchone()
    return render_template("change.html",row=row,row2=row2)

if __name__ == "__main__":
    app.run()
