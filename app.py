from flask import Flask , request, render_template, redirect , session

import dbconn
from dbconn import selectUsers
import pymysql
import datetime
import os
import psutil


db=None
cur=None
app = Flask(__name__)
app.secret_key = 'fsdfsfgsfdg3234'

@app.route('/')
def home():
    return render_template('./login/login.html')

@app.route('/subm/mnu001', methods=['GET', 'POST'])
def mnu001f():
    curr = datetime.datetime.now()
    if request.method == 'GET':
        datfr = ''
        datto = ''
        if datfr == '':
            datfr = curr - datetime.timedelta(hours=1)
            datfr = datfr.strftime('%Y-%m-%d %H:00')
        if datto == '':
            datto = curr.strftime('%Y-%m-%d %H:00')
        result = dbconn.fromtoTraffic(datfr, datto)
        return render_template('./subm/mnu001.html', result = result)
    else:
        datfr = request.form.get('datefrom')
        datto = request.form.get('dateto')
        if datfr == '':
            datfr = curr - datetime.timedelta(hours = 1)
        if datto == '':
            datto = curr
        datfr = datfr.strftime('%Y-%m-%d %H:00')
        datto = datto.strftime('%Y-%m-%d %H:00')
        result = dbconn.fromtoTraffic(datfr,datto)
        return render_template("./subm/mnu001.html", result = result)

@app.route('/subm/cpu')  # 요청
def cpustat():
    pid = os.getpid()
    py = psutil.Process(pid)
    cpu_usage = os.popen("ps aux | grep " + str(pid) + " | grep -v grep | awk '{print $3}'").read()
    cpu_usage = cpu_usage.replace("\n", "")
    memory_usage = round(py.memory_info()[0] / 2. ** 30, 2)
    return render_template("stat/dashcpu.html", result_cpu = cpu_usage,result_mem = memory_usage )
@app.route('/subm/disk')  # 요청
def diskstat():
    result_disk = psutil.disk_usage(os.getcwd())
    return render_template("stat/dashdisk.html", result=result_disk)



@app.route('/subm/network')  # 요청
def networkstat():
    db = pymysql.connect(host='192.168.1.45', user='swcore', password='core2020', db='logger', charset='utf8')
    cur = db.cursor()
    sql = "select * from hBefore order by d002 desc limit 200"
    cur.execute(sql)
    result = cur.fetchall()
    db.close()
    print(result)
    return render_template("stat/dashnetwork.html", result=result)

@app.route('/monmain')  # 요청
def okhome():
    db = pymysql.connect(host='192.168.1.45', user='swcore', password='core2020', db='logger', charset='utf8')
    cur = db.cursor()
    sql = "select * from hBefore order by d002 desc limit 200"

    cur.execute(sql)
    result = cur.fetchall()
    db.close()
    print(result)
    return render_template("stat/indexStart.html", result=result)

@app.route('/dashmain')  # 요청
def searchSel():
    db = pymysql.connect(host='192.168.1.45', user='swcore', password='core2020', db='logger', charset='utf8')
    cur = db.cursor()
    sql = "select * from dayservice"
    cur.execute(sql)
    result_service = cur.fetchall()
    sql = "select * from areafrom"
    cur.execute(sql)
    result_area = cur.fetchall()
    db.close()
    return render_template("stat/dashinit.html", result=result_service, area = result_area)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('./login/login.html')
    else:
        uid = request.form.get('uid')
        upw = request.form.get('upw')
        row = selectUsers(uid, upw)
        if row:
            session['userNo'] = row['userNo']
            session['userName'] = row['userName']
            session['userRole'] = row['userRole']
            return redirect('/dashmain')
        else:
            return '''
                <script>
                    // 경고창 
                    alert("로그인 실패, 다시 시도하세요")
                    // 이전페이지로 이동
                    history.back()
                </script>
            '''

@app.route('/logout')
def logout():
    session.clear()
    return render_template('./login/login.html')

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
