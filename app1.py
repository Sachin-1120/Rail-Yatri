import requests
from flask import Flask,render_template,request
import sqlite3

    
def previous_detail(d):
    l=[]
    for j in range(0,len(d)):
        i=d[j]
        l.append([i['a_day'],i['station_name']+' '+i['station_code'] ,i['sta'],i.get('std'),i['platform_number']])
    return l
app=Flask(__name__)
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method==['POST']:
        message=False
        username=request.form.get('username')
        password=request.form.get('password')
        cur_password=request.form.get('cur_password')
        email=request.form.get('email')
        if password==cur_password:
            con=sqlite3.connect('login.db')
            cursor=con.cursor()
            cursor.execute(f'insert into login values("{username}","{password}","{email}");')
            con.commit()
            cursor.execute('select * from login;')
            result=cursor.fetchall()
            print(result)
            con.close()
            return render_template('login.html')
        else:
            message='Incorrect Password'
            return render_template('signup.html',message=message)
    else:
        return render_template('signup.html')

@app.route('/',methods=['GET','POST'])
def login_i():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        con=sqlite3.connect('login.db')
        cursor=con.cursor()
        cursor.execute('select * from login;')
        d=cursor.fetchall()
        print(d)
        con.close()
        for i in d:

            if i[0].lower()==username.lower():
                print(i[0])
                break
        else:
            return render_template('login.html',message='Invalid Username')
            
        if i[1]==password:
            return render_template('home.html')
        else:
            return render_template('login.html',message='Wrong Password')

    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('./home.html')
@app.route('/track',methods=['GET','POST'])
def train():
    if request.method=='POST':
        train_no=request.form.get('train_no')
        start=request.form.get('start')
        url = "https://irctc1.p.rapidapi.com/api/v1/liveTrainStatus"
        querystring = {"trainNo":train_no,"startDay":start}
        headers = {
            "x-rapidapi-key": "8775ac996fmsh9b9e30fd95efd88p1032b6jsn5b39521a346d",
            "x-rapidapi-host": "irctc1.p.rapidapi.com"
            }   
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code==200:
                
            result=response.json()
            print(result)
            train_name=result['data']['train_name']
            start_date=result['data']['train_start_date']
            status=result['status']
            result['data'].setdefault('previous_stations','')
            l=[]
            d=result['data']['previous_stations']
            for j in range(0,len(d)):
                i=d[j]
                l.append([i['a_day'],i['station_name']+' '+i['station_code'] ,i['sta'],i.get('std'),i['platform_number']])
            curr=[result['data']['a_day'],result['data']['current_station_name']+' '+result['data']['current_station_code'],result['data']['cur_stn_sta'],result['data']['cur_stn_std'],result['data']['platform_number']]
            d=result['data']['upcoming_stations']
            upcoming=[]
            for j in range(0,len(d)):
                i=d[j]
                upcoming.append([i['a_day'],i['station_name']+' '+i['station_code'] ,i['sta'],i.get('std'),i['platform_number']])
            print(l,curr,upcoming)
            return render_template('./index.html',status=status,train_name=train_name,start_date=start_date,previous=l,curr=curr,upcoming=upcoming)
        else:
            return render_template('./index.html',message='Unable to get data')
    else:
        return render_template('./index.html')
@app.route('/search')
def search_train():
    with open('./station_codes.csv','r') as fp:
        result=fp.read()
        result=result.split('\n')
        a=[]
        for i in result:
            z=i.split(',')
            z.append('')
            a.append((z[0],z[1]))            
    return render_template('./search.html',station_name=a)
@app.route('/pnr',methods=['GET','POST'])
def pnr():
    if request.method=='POST':
        pnr_i=request.form.get('pnr')
        print(pnr_i)
        url = f"https://irctc-indian-railway-pnr-status.p.rapidapi.com/getPNRStatus/{pnr_i} "

        headers = {
        "x-rapidapi-key": "5980b42badmshb317a5a1ace298cp1ed1b5jsn5cf77215defc",
        "x-rapidapi-host": "irctc-indian-railway-pnr-status.p.rapidapi.com"
        }

        beta = requests.get(url, headers=headers)
        print(beta)
        if beta.status_code==200:
            response=beta.json()
            print(response)
            train_name=response['data']['trainName']
            trainNo=response['data']['trainNumber']
            date=response['data']['dateOfJourney']
            source=response['data']['sourceStation']
            destination=response['data']['destinationStation']
            passengers=response['data']['numberOfpassenger']
            chartstatus=response['data']['chartStatus']
            result=[train_name,trainNo,date,source,destination,passengers,chartstatus]
            details=[]
            for i in response['data']['passengerList']:
                details.append([i['passengerSerialNumber'],i['passengerNationality'],i['passengerQuota'],i['bookingStatusDetails'],i['currentStatusDetails']])
            return render_template('pnr.html',result=result,detail=details)
        else:
            return render_template('pnr.html',error='Not able to connect')
    else:
        return render_template('pnr.html')
    
if __name__=='__main__':
    app.run('localhost',80,debug=True)