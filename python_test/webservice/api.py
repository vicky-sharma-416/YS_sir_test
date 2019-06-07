from flask import Flask, jsonify, g, request, json
from sqlite3 import dbapi2 as sqlite3
import os
import detect_face
import face_recog
import uuid
DATABASE = 'test.db'
app = Flask(__name__)

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
		db.row_factory = sqlite3.Row
	return db

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None: db.close()

def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv

def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

def add_student(name='test', age=10, sex='male'):
	sql = "INSERT INTO students (name, sex, age) VALUES('%s', '%s', %d)" %(name, sex, int(age))
	print (sql)
	db = get_db()
	db.execute(sql)
	res = db.commit()
	return res

def find_student(name=''):
	sql = "select * from students where name = '%s' limit 1" %(name)
	print (sql)
	db = get_db()
	rv = db.execute(sql)
	res = rv.fetchall()
	rv.close()
	if len(res)>0:
		return res[0]
	else:
		return 0
	
def find_allstudent():
	data = []
	sql = "select * from students"
	print (sql)
	db = get_db()
	rv = db.execute(sql)
	res = rv.fetchall()
	rv.close()
	for row in res:
		data.append([x for x in row]) # or simply data.append(list(row))
	return data

@app.route('/')
def users():
	return jsonify(hello='world')

@app.route('/add',methods=['POST'])
def add_user():
	add_student(name=request.form['name'], age=request.form['age'], sex=request.form['sex'])
	return ''

@app.route('/find_user')
def find_user_by_name():
	name = request.args.get('name', '')
	student = find_student(name)
	if(student == 0 ):
		return jsonify(msg= name +' not found')
		
	return jsonify(name=student['name'], age=student['age'], sex=student['sex'])

@app.route('/detectface', methods=['POST','GET'])
def extractface():
	responseArray ={}
	if request.method == 'POST':
		images = request.files.to_dict()
		for image in images:     #image will be the key 
			print(images[image])        #this line will print value for the image key
			file_name = images[image].filename
			extension = os.path.splitext(file_name)[1]
			f_name = str(uuid.uuid4()) + extension
			images[image].save(os.path.join('./source', f_name))
			#responseArray.append(detect_face.detect_faces(f_name))
			responseArray[f_name]=detect_face.detect_faces('./source/'+f_name)
			
		return jsonify(responseArray)
	else:
		return jsonify(msg='error')

@app.route('/identify', methods=['POST','GET'])
def recogface():
	responseArray ={}
	if request.method == 'POST':
		images = request.files.to_dict()
		for image in images:     #image will be the key 
			print(images[image])        #this line will print value for the image key
			file_name = images[image].filename
			extension = os.path.splitext(file_name)[1]
			f_name = str(uuid.uuid4()) + extension
			images[image].save(os.path.join('./match', f_name))
			responseArray['result']=face_recog.identifyface('./match/'+f_name)
			
		return jsonify(responseArray)
	else:
		return jsonify(msg='error')

		
@app.route('/find')
def find_all():
	#res = abc()
	#print(res)	
	students = find_allstudent()
	return jsonify(students)	

if __name__ == '__main__' : app.run()


'''from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run()
'''