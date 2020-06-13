from django.shortcuts import render
import pymysql
import os
import shutil
import pyaudio
import wave
from aip import AipSpeech
import datetime
import time

con = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='70582829',
    db='old',
    cursorclass=pymysql.cursors.DictCursor,
    charset='utf8'
)

name = ""
id = ""
fa = 0


# Create your views here.
def login(request):
    return render(request, 'login.html')


def logins(request):
    j = 0
    i = 0
    usename = request.POST.get('Userame')
    password = request.POST.get('Password')
    cur1 = con.cursor()
    sqlstr1 = "select * from user;"
    sqlstr2 = "select userid from user;"
    cur1.execute(sqlstr2)
    res1 = cur1.fetchall()
    for ones in res1:
        if usename == ones['userid']:
            j = j + 1
    if j == 0:
        return render(request, 'login.html', {'script': "alert", 'wrong': '账号未注册'})
    else:
        cur2 = con.cursor()
        cur2.execute(sqlstr1)
        res = cur2.fetchall()
        for one in res:
            if usename == one['userid'] and password == one['password']:
                i = i + 1
                global name
                name = usename
                return render(request, 'index.html')
    if i == 0:
        return render(request, 'login.html', {'script': "alert", 'wrong': '密码错误'})


def regist(request):
    i = 0
    id = request.POST.get('UserID')
    usename = request.POST.get('Username1')
    password1 = request.POST.get('Password1')
    password2 = request.POST.get('Password2')
    drop = request.POST.get('drop')
    i=int(drop)
    if i == 0:
        role="老人"
    else:
        role="子女"
    if password1 != password2:
        return render(request, 'login.html', {'script': "alert", 'wrong': '两次密码不同！！'})
    else:
        cur = con.cursor()
        sql = 'select * from user'
        cur.execute(sql)
        res = cur.fetchall()
        for one in res:
            if one['userid'] == id:
                i = i + 1

                return render(request, 'login.html', {'script': "alert", 'wrong': '用户名已存在！！'})
        if i == 0:
            cur1 = con.cursor()
            sql1 = 'insert into user(userid,username,password,role) values({},{},{},{})'.format("'" + id + "'",
                                                                                                "'" + usename + "'",
                                                                                                "'" + password1 + "'",
                                                                                                "'" + role + "'")
            """sql1 = 'insert into user(userid,password) values({},{})'.format(id,password1)"""


            cur1.execute(sql1)
            #con.commit()
            return render(request, 'login.html', {'script': "alert", 'wrong': '注册成功！！'})


def returnindex(request):
    return render(request, 'index.html')


def listdir(path, list_name):  # 传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)


def photo(request):
    i = request.POST.get('nop2')
    j = int(i) - 1
    global fa
    fa = j
    li = []
    cur = con.cursor()
    sql = 'select * from members where userid=%s'
    cur.execute(sql, [name])
    res = cur.fetchall()
    for one in res:
        li.append(one['homeid'])
    cur = con.cursor()
    sql1 = 'select * from photo where homeid=%s'
    cur.execute(sql1, [li[j]])
    res1 = cur.fetchall()
    print(res1)
    return render(request, 'photo1.html', {'t': res1})


def family(request):
    li = []
    li1 = []
    cur = con.cursor()
    sql = 'select * from members where userid=%s'
    cur.execute(sql, [name])
    res = cur.fetchall()
    for one in res:
        li.append(one['homeid'])
    cur = con.cursor()
    sql1 = 'select * from home where homeid=%s'
    for one in li:
        cur.execute(sql1, [one])
        res1 = cur.fetchall()
        li1.append(res1[0])
    return render(request, 'family.html', {'var': li1})


def delete1(request):
    i = request.POST.get('nop1')
    j = int(i) - 1
    cur = con.cursor()
    sql = 'select * from home'
    cur.execute(sql)
    res = cur.fetchall()
    homeid = res[j]['homeid']
    sql1 = 'delete from home where homeid=%s'
    cur1 = con.cursor()
    cur1.execute(sql1, [homeid])
    con.commit()
    cur2 = con.cursor()
    cur2.execute(sql)
    res1 = cur2.fetchall()
    return render(request, 'family.html', {'var': res1})


def shipin(request):
    return render(request, 'shipin.html')


def p2p(request):
    return render(request, 'p2p.html')


def map(request):
    return render(request, 'map.html')


def message(request):
    cur = con.cursor()
    sql = 'select * from user'
    cur.execute(sql)
    res = cur.fetchall()
    for one in res:
        if one['userid'] == name:
            userid = one['userid']
            username = one['username']
            password = one['password']
            address = one['address']
            role = one['role']
    return render(request, 'res1.html',
                  {'ID': userid, 'name': username, 'password': password, 'address': address, 'role': role})


def beiwang(request):
    cur = con.cursor()
    sql = 'select * from beiwang where username=%s'
    cur.execute(sql, [name])
    res = cur.fetchall()
    print(res)
    return render(request, 'beiwang.html', {'var': res})


def xiangqing(request):
    return render(request, 'xiangqing1.html')


def describ(request):
    n = request.POST.get('noo')
    print(n)
    print(type(n))
    cur = con.cursor()
    sql = 'select * from beiwang'
    cur.execute(sql)
    res = cur.fetchall()
    for one in res:
        if one['tname'] == n:
            return render(request, 'xiangqing2.html', {'content': one['content'], 'name': one['tname']})


def new(request):
    cur = con.cursor()
    sql = 'select * from news'
    cur.execute(sql)
    res = cur.fetchall()
    return render(request, 'news.html', {'var': res})


def shangchuan(request):
    file1 = request.FILES.get('file')
    print(file1)
    print(str(file1))
    a = str(file1)
    path = 'C:/Users/23915/Pictures/Saved Pictures/'
    path = path + a
    print(path)
    newpath = 'D:/myweb/static/images/ptaki/'
    finalpath = 'images/ptaki/' + a
    cur = con.cursor()
    sql = 'select * from members where userid=%s'
    cur.execute(sql, [name])
    rg = cur.fetchall()
    homeid = rg[fa]['homeid']
    print(homeid)
    cur = con.cursor()
    sql2 = 'select * from photo'
    cur.execute(sql2)
    res1 = cur.fetchall()
    i = 0
    for one in res1:
        if one['photoid'] == a and one['homeid'] == homeid:
            i = i + 1
    if i == 0:
        shutil.copy(path, newpath)
        cur = con.cursor()
        sql = 'insert into photo(photoid,url,homeid) values({},{},{})'.format("'" + a + "'", "'" + finalpath + "'",
                                                                              "'" + homeid + "'")
        cur.execute(sql)
        con.commit()
        li = []
        cur = con.cursor()
        sql = 'select * from members where userid=%s'
        cur.execute(sql, [name])
        res = cur.fetchall()
        for one in res:
            li.append(one['homeid'])
        cur = con.cursor()
        sql1 = 'select * from photo where homeid=%s'
        cur.execute(sql1, [li[fa]])
        res1 = cur.fetchall()
        print(res1)
        return render(request, 'photo1.html', {'t': res1})
    else:
        cur = con.cursor()
        sql1 = 'select * from home'
        cur.execute(sql1)
        r = cur.fetchall()
        s = r[fa]['homeid']
        cur = con.cursor()
        sql = "select * from photo where homeid=%s"
        cur.execute(sql, [s])
        res1 = cur.fetchall()
        return render(request, 'photo1.html', {'script': "alert", 'wrong': '该文件已存在', 't': res1})


def wwav():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "D:\\test.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("* recording")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def shibie():
    APP_ID = '17673156'
    API_KEY = 'VuOEZqEHiQmv6brzxjWpvVqq'
    SECRET_KEY = 'So5k1Topwq7frkeGo7jzr5jOeVrvcnak'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    file_handle = open('D:\\test.wav', 'rb')
    file_content = file_handle.read()

    result = client.asr(file_content, 'pcm', 16000, {
        'dev_pid': '1536',
    })

    if result['err_no'] == 0:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " >> " + result['result'][0])
        return result['result'][0]
    else:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " >> " + "err_no:" + str(result['err_no']))


def yuyin(request):
    wwav()
    time.sleep(1)
    res0 = shibie()
    time.sleep(1)
    if "新闻" in res0:
        cur = con.cursor()
        sql = 'select * from news'
        cur.execute(sql)
        res = cur.fetchall()
        return render(request, 'news.html', {'var': res})
    elif "备忘录" in res0:
        cur = con.cursor()
        sql = 'select * from beiwang where username=%s'
        cur.execute(sql, [name])
        res = cur.fetchall()
        print(res)
        return render(request, 'beiwang.html', {'var': res})
    elif "个人信息" in res0:
        cur = con.cursor()
        sql = 'select * from user'
        cur.execute(sql)
        res = cur.fetchall()
        for one in res:
            if one['username'] == name:
                userid = one['userid']
                username = one['username']
                password = one['password']
                address = one['address']
                role = one['role']
        return render(request, 'res1.html',
                      {'ID': userid, 'name': username, 'password': password, 'address': address, 'role': role})
    elif "家庭组" in res0:
        cur = con.cursor()
        sql = 'select * from home'
        cur.execute(sql)
        res = cur.fetchall()
        return render(request, 'family.html', {'var': res})
