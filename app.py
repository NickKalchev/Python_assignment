#!/usr/bin/env python3
from flask import Flask, request, jsonify, Response
from datetime import datetime
import sqlite3
from sqlite3 import Error

app = Flask(__name__)


def sql_connection():

    try:
        con = sqlite3.connect('users.db')
        return con

    except Error:
        print(Error)


def sql_table(con):

    cursor_obj = con.cursor()

    cursor_obj.execute(
        """CREATE TABLE if not exists users(
            id integer PRIMARY KEY AUTOINCREMENT, 
            name text NOT NULL, 
            address VARCHAR(100), 
            salary real, 
            age integer NOT NULL
        )"""
    )

    con.commit()
    con.close()


@app.route('/', methods=['GET'])
def index():
    args = request.args
    a = args.get('a')
    b = args.get('b')
    op = args.get('op')
    time_now = datetime.now()
    success_code = Response(status=200, mimetype='application/json')
    bad_req_code = Response(status=400, mimetype='application/json')
    result = ""

    if not a or a == "":
        bad_req_code
        js_arr = jsonify({"status": "error", "reason": "a not found in query string"}), 400
        return js_arr
    elif not b or b == "":
        bad_req_code
        js_arr = jsonify({"status": "error", "reason": "b not found in query string"}), 400
        return js_arr
    elif not op or op == "":
        bad_req_code
        js_arr = jsonify({"status": "error", "reason": "op not found in query string"}), 400
        return js_arr

    if op == "*":
        success_code
        result = float(a) * float(b)
    elif op == "/":
        success_code
        result = float(a) / float(b)
    elif op == "-":
        success_code
        result = float(a) - float(b)
    elif op == "+":
        success_code
        result = float(a) + float(b)

    js_arr = {"status": "ok", "date": time_now.strftime('%Y-%m-%d %H:%M'), "result": result}
    message = jsonify(js_arr)
    return message


@app.route("/users/", methods=['GET', 'POST'])
def user():
    args = request.get_json()
    time_now = datetime.now()
    id_get = request.args.get('id')
    name_get = request.args.get('name')
    name = args.get('name')
    address = args.get('address')
    age = args.get('age')
    salary = args.get('salary')
    not_found_code = Response(status=404, mimetype='application/json')

    if request.method == 'GET':
        users_l = []
        db = sqlite3.connect('users.db')
        cursor = db.cursor()

        if not id_get and not name_get:
            not_found_code
            error = jsonify({"status": "error", "reason": "id or name is required"})
            return error

        if name_get:
            cursor.execute(
                """
                    SELECT * 
                    FROM users 
                    WHERE name=?
                """, (name_get,))
            found_user_name = cursor.fetchone()
            users_l.append(found_user_name)

        if id_get:
            cursor.execute(
                """
                    SELECT * 
                    FROM users 
                    WHERE id=?
                """, [id_get])
            found_user_id = cursor.fetchone()
            users_l.append(found_user_id)

        if id_get and name_get:
            cursor.execute(
                """
                    SELECT * 
                    FROM users 
                    WHERE id=? and name=?
                """, [id_get, name_get])

        if not users_l:
            not_found = jsonify({"status": "error", "reason": "Requested user not found"})
            not_found_code
            return not_found

        db.close()
        result = jsonify({
            "status": "success",
            "result": users_l,
            "date": time_now.strftime('%Y-%m-%d %H:%M')
        })
        return result

    if request.method == 'POST':
        db = sqlite3.connect('users.db')
        cursor = db.cursor()

        if not name or not isinstance(name, str):
            error = jsonify({"status": "error", "reason": "Name is not a string"})
            return error
        if not address or not isinstance(address, str):
            error = jsonify({"status": "error", "reason": "Address is not a string"})
            return error
        if not age or not isinstance(age, int):
            error = jsonify({"status": "error", "reason": "Age is not an integer"})
            return error
        if not salary or not isinstance(salary, int):
            error = jsonify({"status": "error", "reason": "Salary is not an integer"})
            return error

        cursor.execute(
            """
                SELECT name 
                FROM users 
                WHERE name=?
            """, [name])

        found_record = cursor.fetchone()

        if found_record:
            error = jsonify({"status": "error", "reason": "User with such name is already present"})
            return error
        else:
            cursor.execute(
                "INSERT INTO users(name, address, age, salary) VALUES (?, ?, ?, ?)",
                (name, address, age, salary)
            )
            db.commit()
            cursor.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")
            last_item = cursor.fetchone()
            respond = jsonify({"status": "success", "result":
                {
                    "id:": last_item[0],
                    "name": last_item[1],
                    "age": last_item[4],
                    "salary": last_item[3],
                    "address": last_item[2]
                },
                    "date": time_now.strftime('%Y-%m-%d %H:%M')
                })
            db.close()
            return respond


if __name__ == "__main__":
    con = sql_connection()
    sql_table(con)
    app.run(threaded=True, port=8000)