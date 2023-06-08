from flask import request
from flask import Flask
from flask import render_template
import pyodbc
import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient, BlobServiceClient
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
        # Execute a simple select query
        if(name=="all"):
            query = "SELECT Picture FROM dbo.people where Salary<99000"
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
    row3=''
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
@app.route("/dave.html",methods=['GET', 'POST'])
def dave():
    file=""
    row3=[0]
    server = 'assignmentservershruthaja.database.windows.net'
    database = 'assignment1'
    username = 'shruthaja'
    password = 'mattu4-12'
    driver = '{ODBC Driver 17 for SQL Server}'

    # Establish the connection
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    if request.method == "POST":
        file=request.files['picture']
        name=request.form['pname']
        url=upload(file,name)

        query = "update dbo.people set Picture=? where name=?"
        cursor = conn.cursor()
        cursor.execute(query, url, name)
        conn.commit()
        # Create a cursor object
        query = "Select Picture from dbo.people where name=?"
        cursor.execute(query, name)
        row3 = cursor.fetchone()
    if request.method == "GET":
        name = request.args.get('delname')
        query = "delete from dbo.people where name=?"
        cursor = conn.cursor()
        cursor.execute(query, name)
        conn.commit()
    return render_template("dave.html",url=row3[0])

def upload(file,name):
    account_url="DefaultEndpointsProtocol=https;AccountName=shruthaja;AccountKey=FvxC1NCWJQuBHKf77+JJaniZDHYUsBzqjy9H2o2o4INHFJRAXUTl6E3VB+2wXX3SsjFsMy5Vpm/R+ASto6SosQ==;EndpointSuffix=core.windows.net"
    blob_account_client = BlobServiceClient.from_connection_string(account_url)
    blob_client=blob_account_client.get_blob_client("assignment1",name+".jpg")
    blob_client.upload_blob(file,overwrite=True)
    return "https://shruthaja.blob.core.windows.net/assignment1/"+name+".jpg"
if __name__ == "__main__":
    app.run(debug=True)
