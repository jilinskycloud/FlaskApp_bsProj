#/usr/bin/python3
from flask import Flask
from markupsafe import escape
from flask import url_for, request, render_template, flash, redirect, session
import psutil, time, sqlite3, subprocess
  
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
dbName = "db/FlaskDb.db"

#	Delete User	
###########################################################
@app.route('/delProfile/<ids>')
def delProfile(ids=None):
	conn = sqlite3.connect(dbName)
	f = conn.execute("DELETE FROM login where id=?", (ids,))
	conn.commit()
	conn.close()
	flash("Deleted successfully")
	return redirect(url_for('settings'))


#	Redirect to Dashboard Page
###########################################################
@app.route('/')
@app.route('/index/')
@app.route('/index')
def index():
	if 'username' in session:

		return redirect(url_for('dashboard'))
	return redirect(url_for('login'))


#	Change	Language
###########################################################
@app.route('/lng', methods=['GET', 'POST'])
def lng():
	if 'username' in session:
		if request.method == 'POST':
			session['lng'] = request.form["lng"]
			print("This is the Language:::", session['lng'])
			return redirect(url_for('dashboard'))
	else:
		return redirect(url_for('index'))


#	Dashboard Page
###########################################################
@app.route('/dashboard')
def dashboard():
	if 'username' in session:
		global sensor_conf_
		u_name = escape(session['username'])
		cmd = "hostname"                   
		proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
		(gw_id, err1) = proc.communicate()       
		gw_id = gw_id.decode('utf-8')
		gw_id = gw_id.strip()   
		data = {}
		data['serial'] = gw_id
		data['cpu'] = psutil.cpu_percent()
		data['stats'] = psutil.cpu_stats()
		data['cpu_freq'] = psutil.cpu_freq()
		data['cpu_load'] = psutil.getloadavg()
		data['ttl_memo'] = round(psutil.virtual_memory().total/1048576)
		data['ttl_memo_used'] = round(psutil.virtual_memory().used/1048576)
		data['ttl_memo_avai'] = round(psutil.virtual_memory().available/1048576)
		data['swp_memo'] = psutil.swap_memory()
		data['hostname'] =cm("hostname")
		data['routeM'] = '****'
		data['FirmV'] = 'v0.0.1'
		data['lTime'] = cm('date')
		data['runTime'] = cm('uptime')
		data['network'] = cm("ifconfig eth0| egrep -o '([[:digit:]]{1,3}\.){3}[[:digit:]]{1,3}'")
		data['mount'] = psutil.disk_partitions(all=False)
		data['disk_io_count'] = psutil.disk_io_counters(perdisk=False, nowrap=True)
		data['net_io_count'] = psutil.net_io_counters(pernic=False, nowrap=True)
		data['nic_addr'] = psutil.net_if_addrs()
		data['boot_time'] = psutil.boot_time()
		data['c_user'] = psutil.users()
		data['reload'] = time.time()
		return render_template('en/dashboard.html', data=data, u_name=escape(session['username']))
	else:
		return redirect(url_for('login'))


#	Get command from Dashboard
###########################################################
def cm(dt):
	klog = subprocess.Popen(dt, shell=True, stdout=subprocess.PIPE).stdout
	klog1 =  klog.read()
	cm_ret = klog1.decode()
	return cm_ret


#	Console Log Page
###########################################################
@app.route('/console_logs')
def console_logs():
	global _paths
	if 'username' in session:
		return render_template('en/console-logs.html', u_name=escape(session['username']))
	else:
		return redirect(url_for('login'))


#	Network Page
###########################################################
@app.route('/network', methods=['GET', 'POST'])
def network():
	if 'username' in session:
		return render_template('en/network.html', u_name=escape(session['username'])) #, net=net, ssid=abc[1], password=abc[6], state=state)
	else:
		return redirect(url_for('login'))


#	Settings Page
###########################################################
@app.route('/settings', methods=['GET', 'POST'])
def settings():
	global sensor_conf_
	global gw_conf_
	error = None
	data = []
	rec=[]
	if 'username' in session:
		if request.method == 'POST':
			data.append(request.form['name'])
			data.append(request.form['pass'])
			conn = sqlite3.connect(dbName)
			conn.execute("INSERT INTO login (username,password) VALUES (?,?)",(data[0], data[1]) )
			conn.commit()
			conn.close()
			msg = "Record successfully added"
			flash("Login Details Added successfully")
		conn = sqlite3.connect(dbName)
		f = conn.execute("SELECT * FROM login")
		rec = f.fetchall()
		conn.close()
		return render_template('en/settings.html', error=error, data=data, rec=rec, u_name=escape(session['username']))
	else:
		return redirect(url_for('login'))


#	Login Page
###########################################################
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		u_name = request.form['username']
		u_pass = request.form['password']
		flag = 0
		conn = sqlite3.connect(dbName)
		f = conn.execute("SELECT * FROM login WHERE username=? and password=?", (u_name, u_pass))
		v = f.fetchall()
		if(len(v) > 0):
			flag = 0
		else:
			flag = -1
		conn.close()
		if(flag == -1):
			error = 'Invalid Credentials. Please try again.'
		else:
			session['username'] = request.form['username']
			session['lng'] = 'en'
			flash('Successfully logged in')

			return redirect(url_for('index'))
	return render_template('en/login.html', error=error)


#	Logout Function
###########################################################
@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))


#	Main Function
###########################################################
if  __name__  ==  '__main__' : 
	print("Starting Flask Web ")
	app.run(host='0.0.0.0', port=80, threaded = True, debug = True)# ssl_context='adhoc') #Ssl_context = Context ,
