from flask import Flask, json, request
from flaskext.mysql import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
mysql = MySQL()

users = list(range(100))

# mysql configuratoin
app.config['MYSQL_DATABASE_HOST']       = 'localhost'
app.config['MYSQL_DATABASE_USER']       = 'root'
app.config['MYSQL_DATABASE_DB']         = 'CXO'
mysql.init_app(app)

@app.route('/listall')
#GET methodby default
def show():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BU")
    data = cursor.fetchall()
    dataList = []
    if data is not None:
        for item in data:
            dataTempObj = {
                'buid'    : item[0],
                'buname'  : item[1],
                'buhead'  : item[2],
            }
            dataList.append(dataTempObj)
        return json.dumps(dataList)
    else:
        return 'data error'


@app.route('/delete/<id>')
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("DELETE FROM BU WHERE buid = %s",int(id))
    conn.commit()
    conn.close()
    if(result):
        return json.dumps({'delete':'true'})
    else:
        return json.dumps({'delete':'false'})

@app.route('/update/',methods=['POST'])
def update():
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("UPDATE BU SET buhead = %s WHERE buid = %s",(request.form['buhead'],request.form['buid']))
    conn.commit()
    conn.close()
    if(result):
        return json.dumps({'updated':'true'})
    else:
        return json.dumps({'updated':'false'})

@app.route('/addnew/',methods=['POST'])
def addnew():
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("INSERT INTO BU values( %s , %s , %s )",(request.form['buid'],request.form['buname'],request.form['buhead']))
    conn.commit()
    conn.close()
    if(result):
        return json.dumps({'inserted':'true'})
    else:
        return json.dumps({'inserted':'false'})


if __name__ == '__main__':
    app.run(debug=True)
