import now as now
from flask import Flask , request, render_template, redirect , session

import dbconn
from dbconn import selectUsers
import pymysql
import datetime


db=None
cur=None
app = Flask(__name__)
app.secret_key = 'fsdfsfgsfdg3234'

@app.route('/')
def home():
    return render_template('./login/login.html')

@app.route('/subm/mnu001', methods=['GET', 'POST'])
def mnu001f():
    if request.method == 'GET':
        datfr = ''
        datto = ''
        curr = datetime.datetime.now()
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
        curr = datetime.datetime.now()
        if datfr == '':
            datfr = curr - datetime.timedelta(hours = 1)
        if datto == '':
            datto = curr
        datfr = datfr.strftime('%Y-%m-%d %H:00')
        datto = datto.strftime('%Y-%m-%d %H:00')
        result = dbconn.fromtoTraffic(datfr,datto)
        return render_template("./subm/mnu001.html", result = result)

@app.route('/logman')  # 요청
def okhome():
    db = pymysql.connect(host='192.168.1.45', user='swcore', password='core2020', db='logger', charset='utf8')
    cur = db.cursor()
    sql = "select * from hBefore order by d002 desc limit 200"
    cur.execute(sql)
    result = cur.fetchall()
    db.close()
    return render_template("stat/indexStart.html", result=result)

@app.route('/sslogman')  # 요청
def searchSel():
    db = pymysql.connect(host='192.168.1.45', user='swcore', password='core2020', db='logger', charset='utf8')
    cur = db.cursor()
    sql = "select * from hBefore order by d002 desc"
    cur.execute(sql)
    result = cur.fetchall()
    db.close()
    return render_template("stat/indexSel.html", result=result)

@app.route('/stlogman')  # 요청
def searchTxt():
    db = pymysql.connect(host='192.168.1.45', user='swcore', password='core2020', db='logger', charset='utf8')
    cur = db.cursor()
    sql = "select * from hBefore order by d002 desc"
    cur.execute(sql)
    result = cur.fetchall()
    db.close()
    return render_template("stat/indexTxt.html", result=result)

@app.route('/alllogman')  # 요청
def searchFrto():
    db = pymysql.connect(host='192.168.1.45', user='swcore', password='core2020', db='logger', charset='utf8')
    cur = db.cursor()
    sql = "select * from hBefore order by d002 desc"
    cur.execute(sql)
    result = cur.fetchall()
    db.close()
    return render_template("stat/indexFrto.html", result=result)

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
            return redirect('/logman')
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
