from flask import abort, Blueprint, flash, Flask, jsonify, render_template, request, redirect, url_for
from .models import Employee, Guest, Room
from flask_cors import cross_origin
from flask_login import current_user, login_required
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/data', methods=['POST', 'GET'])
def data():
    # POST a data to database
    if request.method == 'POST':

        firstname = request.form.get("first_name")
        lastname = request.form.get("last_name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        check_in_time = request.form.get("check_in_time")
        room_no = request.form.get("room_no")
        total_cost = request.form.get("total_cost")

        print(f'{firstname}, {lastname}, {age}, {gender}, {room_no}, {check_in_time}, {total_cost}')

        new_guest = Guest(firstname=firstname, lastname=lastname, age=age, gender=gender, room_no=room_no, check_in_time=check_in_time, total_cost=total_cost) # session = mysql.session()
        # id = my_conn.execute(f'INSERT INTO guest(firstname, room_no) VALUES ("{str(firstname)}", {str(room_no)})')
                                #(str(firstname), str(lastname), int(age), str(gender), int(room_no), int(total_cost))).cursor
                                #, str(lastname), int(age), str(gender), time, int(room_no), int(total_cost))

        #cursor.execute('INSERT INTO users VALUES(null, %s, %s)',(str(name), str(age)))
        db.session.add(new_guest)
        db.session.commit()
        print(f'Id of new guest = {new_guest.guest_id}')
        # session.connection().commit()
        # cursor.close()

        status = {
            'status': 'Data is posted to MySQL!',
            'name': firstname,
            'id': new_guest.guest_id
        }
        flash('New guest has been added!')
        return render_template("successfully.html", status = status)
    
    # GET all data from database
    if request.method == 'GET':

        guests = Guest.query.all()
        print("guests :", guests )

        allData = []

        for i in range(len(guests)):
            guest_id = guests[i].guest_id
            name = guests[i].firstname
            lastname = guests[i].lastname
            age = guests[i].age
            gender = guests[i].gender
            room_no = guests[i].room_no
            check_in_time = guests[i].check_in_time
            total_cost = guests[i].total_cost
            dataDict = {
                "guest_id": guest_id,
                "name": name,
                "lastname": lastname,
                "age": age,
                "gender": gender,
                "room_no": room_no,
                "check_in_time": check_in_time,
                "total_cost": total_cost
            }
            allData.append(dataDict)

        return render_template('table.html', users = allData)

@main.route('/insert')
@login_required
def insert():
    return render_template('insert.html')

@main.route('/roomdata', methods = ['GET'])
def rooms():
    rooms = Guest.query.group_by(Guest.room_no).all()
    rooms_all = Room.query.all()
    print("rooms :", rooms)
    data = []
    data_all = []
    final = []
    for i in range(len(rooms)):
        r = rooms[i].room_no
        data.append(r)
    
    for j in range(len(rooms_all)):
        r_all = rooms_all[j].room_no
        data_all.append(r_all)


    data_all = list(set(data_all))

    for p in range(len(data_all)):
        k = 0
        for q in range(len(data)):
            if not data_all[p] == data[q]:
                k += 1
        
        if k == len(data):
            final.append(data_all[p])

    return render_template('rooms.html', room_av = final)

# @main.route('/data/<string:id>', methods=['GET', 'DELETE', 'PUT'])
# def onedata(id):

#     # GET a specific data by id
#     if request.method == 'GET':
#         cursor = mysql.connection.cursor()
#         cursor.execute('SELECT * FROM users WHERE id = %s', (id))
#         users = cursor.fetchall()
#         print(users)
#         data = []
#         for i in range(len(users)):
#             id = users[i][0]
#             name = users[i][1]
#             age = users[i][2]
#             dataDict = {
#                 "id": id,
#                 "name": name,
#                 "age": age
#             }
#             data.append(dataDict)
#         return jsonify(data)

#     # DELETE a data
#     if request.method == 'DELETE':
#         cursor = mysql.connection.cursor()
#         cursor.execute('DELETE FROM users WHERE id = %s', (id))
#         mysql.connection.commit()
#         cursor.close()
#         return jsonify({'status': 'Data '+id+' is deleted on MySQL!'})

#     # UPDATE a data by id
#     if request.method == 'PUT':
#         body = request.json
#         name = body['name']
#         age = body['age']

#         cursor = mysql.connection.cursor()
#         cursor.execute('UPDATE users SET name = %s, age = %s WHERE id = %s', (name, age, id))
#         mysql.connection.commit()
#         cursor.close()
#         return jsonify({'status': 'Data '+id+' is updated on MySQL!'})
