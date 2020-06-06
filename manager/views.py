from django.shortcuts import render
import pymysql
import os
import shutil
con = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='70582829',
    db='old',
    cursorclass=pymysql.cursors.DictCursor,
    charset='utf8'
)

def t1(h):
    global name
    name=h

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
    sqlstr2 = "select username from user;"
    cur1.execute(sqlstr2)
    res1 = cur1.fetchall()
    for ones in res1:
        if usename == ones['username']:
            j = j + 1
    if j == 0:
        return render(request, 'login.html', {'script': "alert", 'wrong': '账号未注册'})
    else:
        cur2 = con.cursor()
        cur2.execute(sqlstr1)
        res = cur2.fetchall()
        for one in res:
            if usename == one['username'] and password == one['password']:
                i = i + 1
                t1(usename)
                return render(request, 'index.html')
    if i == 0:
        return render(request, 'login.html', {'script': "alert", 'wrong': '密码错误'})
def returnindex(request):
    return render(request,'index.html')

def listdir(path, list_name):  # 传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)
def photo(request):
    cur=con.cursor()
    sql="select * from photo "
    cur.execute(sql)
    res=cur.fetchall()
    return render(request,'photo1.html',{'t':res})

def family(request):
    cur=con.cursor()
    sql='select * from home'
    cur.execute(sql)
    res=cur.fetchall()
    return render(request,'family.html',{'var':res})

def delete1(request):
    i=request.POST.get('nop1')
    j=int(i)-1
    cur=con.cursor()
    sql='select * from home'
    cur.execute(sql)
    res=cur.fetchall()
    homeid=res[j]['homeid']
    sql1='delete from home where homeid=%s'
    cur1=con.cursor()
    cur1.execute(sql1,[homeid])
    con.commit()
    cur2=con.cursor()
    cur2.execute(sql)
    res1=cur2.fetchall()
    return render(request,'family.html',{'var':res1})

def shipin(request):
    return render(request,'shipin.html')

def p2p(request):
    return render(request,'p2p.html')

def map(request):
    return render(request,'map.html')

def message(request):
    cur=con.cursor()
    sql='select * from user'
    cur.execute(sql)
    res=cur.fetchall()
    for one in res:
        if one['username'] == name:
            userid=one['userid']
            username=one['username']
            password=one['password']
            address=one['address']
            role=one['role']
    return render(request,'res1.html',{'ID':userid,'name':username,'password':password,'address':address,'role':role})

def beiwang(request):
    cur=con.cursor()
    sql='select * from beiwang where username=%s'
    cur.execute(sql,[name])
    res=cur.fetchall()
    print(res)
    return render(request,'beiwang.html',{'var':res})

def xiangqing(request):
    return render(request,'xiangqing1.html')

def describ(request):
    n=request.POST.get('noo')
    print(n)
    print(type(n))
    cur=con.cursor()
    sql='select * from beiwang'
    cur.execute(sql)
    res=cur.fetchall()
    for one in res:
        if one['tname'] == n:
            return render(request,'xiangqing2.html',{'content':one['content'],'name':one['tname']})

def new(request):
    cur=con.cursor()
    sql='select * from news'
    cur.execute(sql)
    res=cur.fetchall()
    return render(request,'news.html',{'var':res})

def shangchuan(request):
    file1=request.FILES.get('file')
    print(file1)
    print(str(file1))
    a=str(file1)
    path='C:/Users/23915/Pictures/Saved Pictures/'
    path=path+a
    print(path)
    newpath='D:/myweb/static/images/ptaki/'
    finalpath='images/ptaki/'+a
    shutil.copy(path,newpath)
    cur=con.cursor()
    sql='insert into photo(photoid,url) values({},{})'.format("'"+a+"'", "'"+finalpath+"'")
    cur.execute(sql)
    con.commit()
    cur1=con.cursor()
    sql1='select * from photo'
    cur1.execute(sql1)
    res=cur1.fetchall()
    return render(request,'photo1.html',{'t':res})