from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector as mq
from mysql.connector import Error
from markupsafe import Markup
from datetime import datetime
import pandas as pd
import requests
import matplotlib.pyplot as plt
from cryptography.fernet import Fernet
import base64
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
key = b'cAtnnFlf_IYaDwMX1twUVg3VDityfm08ushF7M8J4w4='
cipher_suite = Fernet(key)

def dbconnection():
    con = mq.connect(host='localhost', database='crime',user='root',password='root')
    return con

@app.route('/')
def home():
    return render_template('index.html', title='home')

@app.route('/loginpage')
def loginpage():
    return render_template('login.html',title='login')

@app.route('/userregisterpage')
def registerpage():
    return render_template('userregister.html',title='register')

@app.route('/addcriminalpage')
def addcriminalpage():
    return render_template('addcriminal.html',title='add criminal')

@app.route('/regcomplaintpage')
def regcomplaintpage():
    return render_template('regcomplaint.html',title='Register complaint')

@app.route('/viewsos')
def viewsos():
    current_date = datetime.now().strftime('%Y-%m-%d')
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from sos where dat='{}' ORDER BY id DESC".format(
        current_date))
    res = cursor.fetchall()
    
    return render_template('pviewsos.html',res=res)

@app.route('/uviewcriminals')
def uviewcriminals():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from criminals")
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Failed! criminals not found</h3>")
        flash(message)
        return render_template('uviewcriminals.html', title='criminals')
    else:
        return render_template('uviewcriminals.html', title='criminals',res=res)

'''@app.route('/viewcomplaintspage')
def viewcomplaintspage():
    uid = session['uid']
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from complaints where uid={}".format(int(uid)))
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Failed! Complaints not found</h3>")
        flash(message)
        return render_template('uviewcomplaints.html', title='complaints')
    else:
        return render_template('uviewcomplaints.html', title='complaints',res=res)'''

@app.route('/viewcomplaintspage')
def viewcomplaintspage():
    print("inside")
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("SELECT crimetype, place, des, lat, longit, cdate, ctime, photo, video, status, uid FROM complaints")
    complaints = cursor.fetchall()
    
    decrypted_complaints = []
    for complaint in complaints:
        decrypted_complaint = {
            'crimetype': decrypt_data(complaint[0]),
            'place': decrypt_data(complaint[1]),
            'des': decrypt_data(complaint[2]),
            'lat': decrypt_data(complaint[3]),
            'longit': decrypt_data(complaint[4]),
            'cdate': decrypt_data(complaint[5]),
            'ctime': decrypt_data(complaint[6]),
            'photo': decrypt_data(complaint[7]),
            'video': decrypt_data(complaint[8]),
            'status': decrypt_data(complaint[9]),
            'uid': complaint[10]
        }
        decrypted_complaints.append(decrypted_complaint)
        print(decrypted_complaints)
    
    con.close()
    return render_template('uviewcomplaints.html', res=decrypted_complaints)

    
@app.route('/complaintslist')
def complaintslist():
    con = dbconnection()
    cursor = con.cursor()
    '''cursor.execute("select * from complaints ORDER BY id DESC")
    res = cursor.fetchall()'''
    cursor.execute("SELECT id, crimetype, place, des, lat, longit, cdate, ctime, photo, video, status, uid FROM complaints order by id desc")
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Failed! Complaints not found</h3>")
        flash(message)
        return render_template('pviewcomplaints.html', title='complaints')
    else:
        decrypted_complaints = []
    for complaint in res:
        decrypted_complaint = {
            'id' : complaint[0],
            'crimetype': decrypt_data(complaint[1]),
            'place': decrypt_data(complaint[2]),
            'des': decrypt_data(complaint[3]),
            'lat': decrypt_data(complaint[4]),
            'longit': decrypt_data(complaint[5]),
            'cdate': decrypt_data(complaint[6]),
            'ctime': decrypt_data(complaint[7]),
            'photo': decrypt_data(complaint[8]),
            'video': decrypt_data(complaint[9]),
            'status': decrypt_data(complaint[10]),
            'uid': complaint[11]
        }
        decrypted_complaints.append(decrypted_complaint)
        print(decrypted_complaints)
        return render_template('pviewcomplaints.html', title='complaints',res=decrypted_complaints)
    
@app.route('/viewphoto')
def viewphoto():
    path = request.args.get('pname')
    return render_template('viewimage.html', path=path)

    
@app.route('/viewvideo')
def viewvideo():
    path = request.args.get('vname')
    return render_template('viewvideo.html', path=path)


@app.route('/userregister', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
       
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        aadno = request.form['aadno']
        password = request.form['password']
        con = dbconnection()
        cursor = con.cursor()
        cursor.execute("select * from users where email='{}'".format(email))
        res = cursor.fetchall()
        if res==[]:
            cursor.execute("insert into users(name,email,phone,gender,aadno,password)values('{}','{}','{}','{}','{}','{}')".format(
                name,email,phone,gender,aadno,password))
            con.commit()
            con.close()
            message = Markup("<h3> Registration success</h3>")
            flash(message)
            return redirect(url_for('loginpage'))
        else:
            message = Markup("<h3>Failed! email already exists</h3>")
            flash(message)
            return redirect(url_for('userregisterpage'))
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        ltype = request.form['ltype']
        if ltype=='police':
            con = dbconnection()
            cursor = con.cursor()
            cursor.execute("select * from police where email='{}' and password='{}'".format(email,password))
            res = cursor.fetchall()
            if res==[]:
                message = Markup("<h3>Failed! Invalid Email or Password</h3>")
                flash(message)
                return redirect(url_for('loginpage'))
            else:
                return redirect(url_for('viewsos'))
        elif ltype=='user':
            con = dbconnection()
            cursor = con.cursor()
            cursor.execute("select * from users where email='{}' and password='{}'".format(email,password))
            res = cursor.fetchall()
            if res==[]:
                message = Markup("<h3>Failed! Invalid Email or Password</h3>")
                flash(message)
                return redirect(url_for('loginpage'))
            else:
                session['uid']=res[0][0]
                return redirect(url_for('uviewcriminals'))
            
@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    # Handle the latitude and longitude here (e.g., save to the database, trigger alerts, etc.)
    print(f"Received location: Latitude {latitude}, Longitude {longitude}")
    # Get current date and time
    # Get the current date and time
    current_datetime = datetime.now()

    # Get the date and time separately
    current_date = current_datetime.date()  # This will give you the date
    current_time = current_datetime.time()  # This will give you the time

    # Format them as strings if needed
    formatted_date = current_date.strftime("%Y-%m-%d")
    formatted_time = current_time.strftime("%H:%M:%S")

    # Print the formatted date and time
    print(formatted_date)
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("insert into sos(lat,longit,dat,tim)values('{}','{}','{}','{}')".format(
                latitude,longitude,formatted_date,formatted_time))
    con.commit()
    con.close()
    
    # You can return a response
    return jsonify({'status': 'Location received successfully!'})

@app.route('/savecriminal', methods=['POST'])
def savecriminal():
    cname = request.form['cname']
    crimes = request.form['crimes']
    height = request.form['height']
    identification = request.form['identification']
    description = request.form['description']
    uploaded_file = request.files['photo']
    if uploaded_file.filename != '':
        # Save the uploaded file to a specific folder
        filename = 'static/uploads/criminals/' + uploaded_file.filename
        onlyfilename=uploaded_file.filename
        print(filename)
        uploaded_file.save(filename)
        con = dbconnection()
        cursor = con.cursor()
        cursor.execute("insert into criminals(cname,crimes,height,identification,description,img)values('{}','{}','{}','{}','{}','{}')".format(
            cname,crimes,height,identification,description,onlyfilename))
        con.commit()
        con.close()
        message = Markup("<h3>Success! Criminal Added!</h3>")
        flash(message)
        return redirect(url_for('addcriminalpage'))
    else:
        message = Markup("<h3>failed! Please select image</h3>")
        flash(message)
        return redirect(url_for('addcriminalpage'))

@app.route('/pviewcriminals')
def pviewcriminals():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from criminals")
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Failed! criminals not found</h3>")
        flash(message)
        return render_template('pviewcriminals.html', title='criminals')
    else:
        return render_template('pviewcriminals.html', title='criminals',res=res)
        
@app.route('/deletec')
def deletec():
    id =request.args.get('id')
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("delete from criminals where id={}".format(int(id)))
    con.commit()
    con.close()
    message = Markup("<h3>Success! Row Deleted</h3>")
    flash(message)
    return redirect(url_for('pviewcriminals'))

@app.route('/deletecomplaint')
def deletecomplaint():
    id =request.args.get('id')
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("delete from complaint where id={}".format(int(id)))
    con.commit()
    con.close()
    message = Markup("<h3>Success! Row Deleted</h3>")
    flash(message)
    return redirect(url_for('viewcomplaintspage'))

'''@app.route('/complaintreg', methods=['POST'])
def complaintreg():
    uid=session['uid']
    crimetype = request.form['crimetype']
    place = request.form['place']
    des = request.form['des']
    lat = request.form['lat']
    longit = request.form['longit']
    uploaded_file1 = request.files['photo']
    uploaded_file2 = request.files['video']
    imagefilename=""
    videofilename=""
    if uploaded_file1.filename != '':
        # Save the uploaded file to a specific folder
        filename = 'static/uploads/crimeimages/' + uploaded_file1.filename
        imagefilename=uploaded_file1.filename
        print(filename)
        uploaded_file1.save(filename)
    if uploaded_file2.filename !='':
        filename = 'static/uploads/crimevideos/' + uploaded_file2.filename
        videofilename=uploaded_file2.filename
        print(filename)
        uploaded_file1.save(filename)
    
    current_datetime = datetime.now()

    # Get the date and time separately
    current_date = current_datetime.date()  # This will give you the date
    current_time = current_datetime.time()  # This will give you the time

    # Format them as strings if needed
    formatted_date = current_date.strftime("%Y-%m-%d")
    formatted_time = current_time.strftime("%H:%M:%S")
        
    con = dbconnection()
    cursor = con.cursor()
    print(imagefilename)
    print(videofilename)
    status="Pending"
    cursor.execute("insert into complaints(crimetype,place,des,lat,longit,cdate,ctime,photo,video,status,uid)values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{})".format(
        crimetype,place,des,lat,longit,formatted_date,formatted_time,imagefilename,videofilename,status,int(uid)))
    con.commit()
    con.close()
    message = Markup("<h3>Success! Complaint Registered!</h3>")
    flash(message)
    return redirect(url_for('viewcomplaintspage'))'''

def encrypt_data(data):
    """Encrypts data using Fernet."""
    encrypted_data = cipher_suite.encrypt(data.encode())  # Encrypts the data
    return encrypted_data.decode()  # Convert to string for storage

def decrypt_data(encrypted_data):
    """Decrypts data using Fernet."""
    return cipher_suite.decrypt(encrypted_data.encode()).decode()  # Convert to bytes for decryption

def convert_to_mp4(input_path, output_path):
    ffmpeg_command = [
        'ffmpeg', '-i', input_path,
        '-vcodec', 'h264', '-acodec', 'aac',
        '-strict', 'experimental', output_path
    ]
    subprocess.run(ffmpeg_command)

    
@app.route('/complaintreg', methods=['POST'])
def complaintreg():
    uid = session['uid']
    crimetype = request.form['crimetype']
    place = request.form['place']
    des = request.form['des']
    lat = request.form['lat']
    longit = request.form['longit']
    uploaded_file1 = request.files['photo']
    uploaded_file2 = request.files['video']
    imagefilename = ""
    videofilename = ""
    
    # Handle file uploads
    if uploaded_file1.filename != '':
        filename = 'static/uploads/crimeimages/' + uploaded_file1.filename
        imagefilename = uploaded_file1.filename
        uploaded_file1.save(filename)
    
    if uploaded_file2.filename != '':
        filename = 'static/uploads/crimevideos/' + uploaded_file2.filename
        videofilename = uploaded_file2.filename
        
        uploaded_file2.save(filename)
        #convert_to_mp4(filename,filename)
    
    # Get current date and time
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%Y-%m-%d")
    formatted_time = current_datetime.strftime("%H:%M:%S")
    
    # Encrypt each field
    encrypted_crimetype = encrypt_data(crimetype)
    encrypted_place = encrypt_data(place)
    encrypted_des = encrypt_data(des)
    encrypted_lat = encrypt_data(lat)
    encrypted_longit = encrypt_data(longit)
    encrypted_cdate = encrypt_data(formatted_date)
    encrypted_ctime = encrypt_data(formatted_time)
    encrypted_imagefilename = encrypt_data(imagefilename)
    encrypted_videofilename = encrypt_data(videofilename)
    encrypted_status = encrypt_data("Pending")
    #encrypted_uid = encrypt_data(str(uid))
    
    # Save encrypted data to the database
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO complaints (crimetype, place, des, lat, longit, cdate, ctime, photo, video, status, uid)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (encrypted_crimetype, encrypted_place, encrypted_des, encrypted_lat, encrypted_longit,
          encrypted_cdate, encrypted_ctime, encrypted_imagefilename, encrypted_videofilename,
          encrypted_status, uid))
    
    con.commit()
    con.close()
    
    # Success message
    message = Markup("<h3>Success! Complaint Registered!</h3>")
    flash(message)
    return redirect(url_for('viewcomplaintspage'))


@app.route('/updatecomplaint', methods=['POST'])
def update_complaint():
    data = request.get_json()
    complaint_id = data['id']
    update_text = update_text = data['update']
    encstatus = encrypt_data(update_text)
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("update complaints set status='{}' where id={}".format(encstatus,int(complaint_id)))
    con.commit()
    con.close()
    return jsonify({"success": True}), 200

# Load the datasets
def load_data():
    crime_data = pd.read_csv('10_Property_stolen_and_recovered.csv')
    rape_data = pd.read_csv('20_Victims_of_rape.csv')
    return crime_data, rape_data

# Generate graphs for both datasets
def create_graphs(crime_data, rape_data):
    graphs = []
    
    # Bar graph for Cases Recovered vs Stolen
    plt.figure()
    crime_data.groupby('Area_Name').sum()['Cases_Property_Recovered'].plot(kind='bar', color='green', alpha=0.7, label='Recovered')
    crime_data.groupby('Area_Name').sum()['Cases_Property_Stolen'].plot(kind='bar', color='red', alpha=0.7, label='Stolen')
    plt.title('Cases of Property Recovered vs Stolen')
    plt.ylabel('Number of Cases')
    plt.xlabel('Area')
    plt.legend()
    plt.savefig('static/cases_comparison.png',bbox_inches='tight')
    graphs.append('static/cases_comparison.png')
    
    # Pie chart for Property Recovery Value
    plt.figure()
    crime_data.groupby('Area_Name')['Value_of_Property_Recovered'].sum().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Value of Property Recovered by Area')
    plt.ylabel('')
    plt.savefig('static/property_recovered_value.png',bbox_inches='tight')
    graphs.append('static/property_recovered_value.png')
    
    # Line graph for Stolen Property Value
    plt.figure()
    crime_data.groupby('Area_Name').sum()['Value_of_Property_Stolen'].plot(kind='line', marker='o')
    plt.title('Value of Property Stolen Over Areas')
    plt.ylabel('Value of Property Stolen')
    plt.xlabel('Area')
    plt.savefig('static/property_stolen_value.png',bbox_inches='tight')
    graphs.append('static/property_stolen_value.png')

    # Bar graph for Rape Cases by Age Group
    plt.figure()
    rape_data[['Victims_Above_50_Yrs', 'Victims_Between_10-14_Yrs', 'Victims_Between_14-18_Yrs', 'Victims_Between_18-30_Yrs', 'Victims_Between_30-50_Yrs', 'Victims_Upto_10_Yrs']].sum().plot(kind='bar', color='purple', alpha=0.7)
    plt.title('Victims of Rape by Age Group')
    plt.ylabel('Number of Victims')
    plt.xlabel('Age Group')
    plt.xticks(rotation=45)
    plt.savefig('static/rape_victims_age_group.png',bbox_inches='tight')
    graphs.append('static/rape_victims_age_group.png')

    return graphs

@app.route('/crimerates')
def crimerates():
    crime_data, rape_data = load_data()
    graphs = create_graphs(crime_data, rape_data)
    return render_template('crimegraph.html', graphs=graphs)


    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
