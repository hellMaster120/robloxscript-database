from re import L
import re
from flask import Flask,request,jsonify
import sqlite3


uuid = "xxxxxx-2xx2xxxxx-5xxxxxxxx-3xxxxxxxx-4xxxxxxxxxx-44xxxxxxxxxx"
publickey = "xxxx-xxxxx-xxxxx-xxxxx-xxxxxxx"

app = Flask(__name__)
def db_connect():
    conn = None
    try:
        conn = sqlite3.connect("users.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

@app.route("/data/get",methods={"POST"})
def GetData():
    conn = db_connect()
    cursor = conn.cursor()
    if request.method == "POST":
        if  request.form["Type"] != "login":
            if request.form["Type"] == "id":
                id = request.form["id"]
                cursor = conn.execute("SELECT * FROM users WHERE id=?",(id,))
            if request.form["Type"] == "name":
                name = request.form["name"]
                cursor = conn.execute("SELECT * FROM users WHERE name=?",(name,))
            if request.form["Type"] == "publickey":
                publickey = request.form["publickey"]
                cursor = conn.execute("SELECT * FROM users WHERE publickey=?",(publickey,))
            rows = cursor.fetchall()
            for data in rows:
                DataId = data[0]
                DataUserName = data[1]
                DataPublicKey = data[5]
                return jsonify(data)
                return {"id":DataId,"username":DataUserName,"publickey":DataPublicKey}
        else:
            password = request.form["password"] or None
            username = request.form["username"] or None
            email = request.form["email"] or None
            uuid = request.form["uuid"] or None
            if password != "none" and username != "none" or email != "none":
                    cursor = conn.execute("SELECT * FROM users WHERE username=? OR email=?",(username,email))
                    rows = cursor.fetchall()
                    for data in rows:
                        if data[3] == password:
                            return jsonify(data)
                        else:
                            return "wrong password",404
                    return "wrong email/username",404
            if password == "none" and username == "none" or email == "none":
                cursor = conn.execute("SELECT * FROM users WHERE uuid=?",(uuid,))
                rows = cursor.fetchall()
                for data in rows:
                    return jsonify(data)
                return "wrong uuid",404
            else:
                if uuid == "none":
                    cursor = conn.execute("SELECT * FROM users WHERE username=? OR email=?",(username,email))
                    rows = cursor.fetchall()
                    for data in rows:
                        if data[3] == password:
                            return jsonify(data)
                        else:
                            return "wrong password",404
                    return "wrong email/username",404

@app.route("/data",methods={"POST","PUT"})
def Data():
    conn = db_connect()
    cursor = conn.cursor()
    if request.method == "POST":
        id = request.form["id"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        uuid = request.form["uuid"]
        publickey = request.form["publickey"]
        sql = """INSERT INTO users (id,username,email,password,uuid,publickey)
                VALUES (?,?,?,?,?,?)"""
        cursor = conn.execute(sql,(id,username,email,password,uuid,publickey))
        conn.commit()
        return "added to database"
    if request.method == "PUT":
        uuid = request.form["uuid"]
        if request.form["loged_in"] == "true":
            if request.form["Type"] == "password":
                newpassword = request.form["newpassword"]
                sql = """UPDATE users
                            SET password=?
                        WHERE uuid=?"""
                conn.execute(sql,(newpassword,uuid))
                conn.commit()
                return "new password"
            if request.form["Type"] == "username":
                newusername = request.form["newusername"]
                sql = """UPDATE users
                            SET username=?
                        WHERE uuid=?"""
                conn.execute(sql,(newusername,uuid))
                conn.commit()
                return newusername
        return "not logied in"


if __name__ == "__main__":
    app.run(debug=True)
