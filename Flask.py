from flask import Flask, render_template, request
import mysql.connector
import datetime
import pytz

app = Flask(__name__)

app.config['dbconfig'] = {'host': '<your_host>',  # Auth_data 
                          'user': '<user>',
			  'password': '<password>',
			  'database': '<DB name>'}


def log_request(req: 'flask_request') -> None:
	conn = mysql.connector.connect(**app.config['dbconfig'])
	cursor = conn.cursor()
	tzmoscow = pytz.timezone('Europe/Moscow')
	now = datetime.datetime.now(tzmoscow)

	_SQL = """insert into krasnodar (id, time, name, age, edu, target,sex,city,
	family,child,home,work,car,smoke, user_agent, remote_addr)
	values
	(null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
	cursor.execute(_SQL, (now.strftime("%d-%m-%Y %H:%M"), req.form['name'], req.form['age'], req.form['edu'], req.form['target'], req.form['sex'], req.form['city'], req.form['family'], req.form['child'], req.form['home'], req.form['work'], req.form['car'], req.form['smoke'],
	               str(req.user_agent), str(req.remote_addr),))
	conn.commit()
	cursor.close()
	conn.close()


@app.route('/', methods=['POST', 'GET'])
def function():
    return render_template('spage.html')


@app.route('/start', methods=['POST'])
def function2():
	return render_template('newindex.html')


@app.route('/finish', methods=['POST'])
def function3():
	log_request(request)
	return render_template('results.html')


if __name__ == '__main__':
    app.debug = True
    app.run(port=5001)
