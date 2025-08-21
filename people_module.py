import tkinter as tk
from tkinter import *
from tkinter import PhotoImage
from tkinter import ttk, messagebox
import PIL
from PIL import Image, ImageTk
import mysql.connector
import tkintermapview
from geopy.geocoders import Photon
from timezonefinder import TimezoneFinder
from datetime import *
import requests
import pytz

try:
    root = tk.Tk()
    root.title("Crowd Management System")
    root.geometry("925x500+300+200")

    db = mysql.connector.connect(host='localhost',
                                 port=3306,
                                 database='people_details',
                                 user='root',
                                 password='')
    cursor = db.cursor()

    root.config(bg='#fff')
    root.resizable(False, False)

    logo_img = PIL.Image.open('Images/logo.png').resize((100, 100))
    logo_img = PIL.ImageTk.PhotoImage(logo_img)
    root.iconphoto(logo_img, logo_img)

    login_icon = PhotoImage(file='images/people_login.png')
    passshow_icon = PhotoImage(file='images/eye.png')
    passhide_icon = PhotoImage(file='images/hide.png')
    dash_image = PhotoImage(file="images/people.png")

    password_mode = True

    login_photo = tk.Label(root, image=login_icon, bg='white')
    login_photo.place(x=25, y=125)

    login_frame = tk.Frame(root, width=350, height=420, bg='white')
    login_frame.place(x=520, y=60)

    login_head = tk.Label(login_frame, text='People Login', fg='#57a1f8', bg='white',
                          font=('Microsoft YaHei UI Light', 23, 'bold'))
    login_head.place(x=75, y=5)

    def signin():
        username = login_user_entry.get()
        password = login_pass_entry.get()

        def home():
            dashboard_frame.place(x=10, y=10)
            location_frame.place_forget()
            forecast_frame.place_forget()
            map_frame.place_forget()
            back_button.place_forget()

        def location_details():
            dashboard_frame.place_forget()
            location_frame.place(x=0, y=0)

            detail_content = Label(location_frame, font=('Microsoft YaHei UI Light', 12), bg='white', fg='orange', wraplength=800, justify='center')
            detail_content.config(text="தமிழ்நாட்டில் மிக அதிக பக்தர்கள் வருகைதரும்  கோயில்களில் திருவண்ணாமலையும் ஒன்று. பண்டைய காலத்தில் அண்ணாமலை என்பது அடையமுடியாத மலை என்று பொருள்கொள்ளத்தக்கதாய் இருந்தது. "
                                       "பின்பு இம்மலையின் புனிதத்தன்மையினால் இப்பெயருடன் “திரு” என்ற அடை மொழி முன்னொட்டாக சேர்த்து திருவண்ணாமலை என்று வழங்கப்படுகிறது.இந்தியாவில் முக்கிய மற்றும் பாரம்பரியமான ஆன்மீகத் சைவத்தலமாக  திருவண்ணாமலை விளங்குகிறது. "
                                       "அண்ணாமலை மலையும் அதன் மலைவலமும் தமிழர்களால் மிகவும் வணங்கப்பட்டு வருகிறது. கட்டிடக்கலையிலும், பெருவிழாக்களினாலும் திருவண்ணாமலை கோயில் மிகப் புகழ்பெற்றுள்ளது.  ஆண்டு தோறும் நடக்கும் தீபத்திருவிழா தமிழகம் மட்டுமல்லாது தென்னிந்தியாவில் பல பகுதிகளிலிருந்து பக்தர்கள் வருகை புரிகின்றனர். "
                                       "இவை தவிர்த்து ஆரணி, தேவிகாபுரம், வந்தவாசி போன்ற பகுதிகள் ஆங்கிலேயர் ஆட்சிக்காலத்தில் முக்கிய கேந்திரமாக விளங்கி வந்துள்ளது. சோழர்களின் கீழ் குறுநில மன்னராக விளங்கிய சம்புவராயர்கள் பின்பு படைவீட்டை தலைமையிடமாகக் கொண்டு தனிஅரசாட்சி அமைத்து ஆண்டுவந்துள்ளார். "
                                       "ஆரணியில் உள்ள கோட்டை கைலாசநாதர் கோயிலும் கோட்டை பகுதிகளும் அதற்கு சாட்சியாக விளங்குகின்றன.")
            detail_content.config()
            detail_content.place(x=70, y=65)

            back_button.place(x=340, y=410)

        def forecast_app():
            dashboard_frame.place_forget()
            forecast_frame.place(x=0, y=0)

            weather_lable = Label(forecast_frame, text="Weather Forecast",
                                  font=('Microsoft YaHei UI Light', 20, 'bold'))
            weather_lable.config(fg='#57a1f8', bg='white')
            weather_lable.place(x=345, y=30)

            api = 'http://api.openweathermap.org/data/2.5/forecast?appid=2606f769271b8d545fe3458b2b72ed9f&q=Tiruvannamalai'
            response = requests.get(api).json()

            if response['cod'] == '200':
                geolocator = Photon(user_agent="measurements")
                location = geolocator.geocode('Tiruvannamalai')
                obj = TimezoneFinder()

                long_lat = Label(forecast_frame, font=('Microsoft YaHei UI Light', 18), fg='orange', bg='white')
                long_lat.place(x=650, y=33)

                lng = location.longitude
                lat = location.latitude
                result = obj.timezone_at(lng=lng, lat=lat)
                long_lat.config(text=f'{round(lng, 4)}°N, {round(lat, 4)}°E')

                clock = Label(forecast_frame, font=('Microsoft YaHei UI Light', 30, 'bold'), fg='#57a1f8', bg='white')
                clock.place(x=705, y=420)

                home = pytz.timezone(result)
                local_time = datetime.now(home)
                current_time = local_time.strftime("%I:%M %p")
                clock.config(text=current_time)

                temp = round(response['list'][0]['main']['temp'] - 273.15)
                humidity = round(response['list'][0]['main']['humidity'])
                pressure = round(response['list'][0]['main']['pressure'])
                wind = round(response['list'][0]['wind']['speed'])
                description = response['list'][0]['weather'][0]['description']

                label1 = Label(forecast_frame, text='Temperature', font=('Microsoft YaHei UI Light', 10), bg='white',
                               fg='#57a1f8')
                label1.place(x=390, y=110)

                label2 = Label(forecast_frame, text='Humidity', font=('Microsoft YaHei UI Light', 10), bg='white', fg='#57a1f8')
                label2.place(x=390, y=130)

                label3 = Label(forecast_frame, text='Pressure', font=('Microsoft YaHei UI Light', 10), bg='white', fg='#57a1f8')
                label3.place(x=390, y=150)

                label4 = Label(forecast_frame, text='Wind Speed', font=('Microsoft YaHei UI Light', 10), bg='white', fg='#57a1f8')
                label4.place(x=390, y=170)

                label5 = Label(forecast_frame, text='Description', font=('Microsoft YaHei UI Light', 10), bg='white',
                               fg='#57a1f8')
                label5.place(x=390, y=190)

                t1 = Label(forecast_frame, font=('Microsoft YaHei UI Light', 10), bg='white', fg='orange')
                t1.place(x=470, y=110)

                t2 = Label(forecast_frame, font=('Microsoft YaHei UI Light', 10), bg='white', fg='orange')
                t2.place(x=470, y=130)

                t3 = Label(forecast_frame, font=('Microsoft YaHei UI Light', 10), bg='white', fg='orange')
                t3.place(x=470, y=150)

                t4 = Label(forecast_frame, font=('Microsoft YaHei UI Light', 10), bg='white', fg='orange')
                t4.place(x=470, y=170)

                t5 = Label(forecast_frame, font=('Microsoft YaHei UI Light', 10), bg='white', fg='orange')
                t5.place(x=470, y=190)

                t1.config(text=(temp, '°C'))
                t2.config(text=(humidity, '%'))
                t3.config(text=(pressure, 'hPa'))
                t4.config(text=(wind, 'm/s'))
                t5.config(text=description)

                firstimage = Label(forecast_frame, bg='#7c7d7c', fg='#57a1f8')
                firstimage.place(x=100, y=300)

                secondimage = Label(forecast_frame, bg='#7c7d7c', fg='#57a1f8')
                secondimage.place(x=250, y=300)

                thirdimage = Label(forecast_frame, bg='#7c7d7c', fg='#57a1f8')
                thirdimage.place(x=350, y=300)

                fourthimage = Label(forecast_frame, bg='#7c7d7c', fg='#57a1f8')
                fourthimage.place(x=450, y=300)

                fifthimage = Label(forecast_frame, bg='#7c7d7c', fg='#57a1f8')
                fifthimage.place(x=550, y=300)

                sixthimage = Label(forecast_frame, bg='#7c7d7c', fg='#57a1f8')
                sixthimage.place(x=650, y=300)

                seventhimage = Label(forecast_frame, bg='#7c7d7c', fg='#57a1f8')
                seventhimage.place(x=750, y=300)

                firstdayimage = response['list'][0]['weather'][0]['icon']

                photo1 = PhotoImage(file=f'icon/{firstdayimage}@2x.png')
                firstimage.config(image=photo1)
                firstimage.image = photo1

                tempday1 = round(response['list'][0]['main']['temp_max'] - 273.15)
                tempnight1 = round(response['list'][0]['main']['temp_min'] - 273.15)
                print(f"Day 1 Temp: {tempday1}°C")

                seconddayimage = response['list'][1]['weather'][0]['icon']

                img1 = Image.open(f'icon/{seconddayimage}@2x.png')
                resized_img1 = img1.resize((55, 55))
                photo2 = ImageTk.PhotoImage(resized_img1)
                secondimage.config(image=photo2)
                secondimage.image = photo2

                tempday2 = round(response['list'][1]['main']['temp_max'] - 273.15)
                tempnight2 = round(response['list'][1]['main']['temp_min'] - 273.15)
                print(f"Day 2 Temp: {tempday2}°C")

                thirddayimage = response['list'][2]['weather'][0]['icon']

                img2 = Image.open(f'icon/{thirddayimage}@2x.png')
                resized_img2 = img2.resize((55, 55))
                photo3 = ImageTk.PhotoImage(resized_img2)
                thirdimage.config(image=photo3)
                thirdimage.image = photo3

                tempday3 = round(response['list'][2]['main']['temp_max'] - 273.15)
                tempnight3 = round(response['list'][2]['main']['temp_min'] - 273.15)
                print(f"Day 3 Temp: {tempday3}°C")

                fourthdayimage = response['list'][3]['weather'][0]['icon']

                img3 = Image.open(f'icon/{fourthdayimage}@2x.png')
                resized_img3 = img3.resize((55, 55))
                photo4 = ImageTk.PhotoImage(resized_img3)
                fourthimage.config(image=photo4)
                fourthimage.image = photo4

                tempday4 = round(response['list'][3]['main']['temp_max'] - 273.15)
                tempnight4 = round(response['list'][3]['main']['temp_min'] - 273.15)
                print(f"Day 4 Temp: {tempday4}°C")

                fifthdayimage = response['list'][4]['weather'][0]['icon']

                img4 = Image.open(f'icon/{fifthdayimage}@2x.png')
                resized_img4 = img4.resize((55, 55))
                photo5 = ImageTk.PhotoImage(resized_img4)
                fifthimage.config(image=photo5)
                fifthimage.image = photo5

                tempday5 = round(response['list'][4]['main']['temp_max'] - 273.15)
                tempnight5 = round(response['list'][4]['main']['temp_min'] - 273.15)
                print(f"Day 5 Temp: {tempday5}°C")

                sixthdayimage = response['list'][5]['weather'][0]['icon']

                img5 = Image.open(f'icon/{sixthdayimage}@2x.png')
                resized_img5 = img5.resize((55, 55))
                photo6 = ImageTk.PhotoImage(resized_img5)
                sixthimage.config(image=photo6)
                sixthimage.image = photo6

                tempday6 = round(response['list'][5]['main']['temp_max'] - 273.15)
                tempnight6 = round(response['list'][5]['main']['temp_min'] - 273.15)
                print(f"Day 6 Temp: {tempday6}°C")

                seventhdayimage = response['list'][6]['weather'][0]['icon']

                img6 = Image.open(f'icon/{seventhdayimage}@2x.png')
                resized_img6 = img6.resize((55, 55))
                photo7 = ImageTk.PhotoImage(resized_img6)
                seventhimage.config(image=photo7)
                seventhimage.image = photo7

                tempday7 = round(response['list'][6]['main']['temp_max'] - 273.15)
                tempnight7 = round(response['list'][6]['main']['temp_min'] - 273.15)
                print(f"Day 7 Temp: {tempday7}°C")

                day1 = Label(forecast_frame, font=('Arial', 18, 'bold'), bg='white', fg='#57a1f8')
                day1.place(x=85, y=250)

                first = datetime.now()
                day1.config(text=first.strftime("%A"))

                day2 = Label(forecast_frame, bg='white', fg='#57a1f8')
                day2.place(x=250, y=256)

                second = first + timedelta(days=1)
                day2.config(text=second.strftime("%A"))

                day3 = Label(forecast_frame, bg='white', fg='#57a1f8')
                day3.place(x=350, y=256)

                third = first + timedelta(days=2)
                day3.config(text=third.strftime("%A"))

                day4 = Label(forecast_frame, bg='white', fg='#57a1f8')
                day4.place(x=450, y=256)

                fourth = first + timedelta(days=3)
                day4.config(text=fourth.strftime("%A"))

                day5 = Label(forecast_frame, bg='white', fg='#57a1f8')
                day5.place(x=550, y=256)

                fifth = first + timedelta(days=4)
                day5.config(text=fifth.strftime("%A"))

                day6 = Label(forecast_frame, bg='white', fg='#57a1f8')
                day6.place(x=650, y=256)

                sixth = first + timedelta(days=5)
                day6.config(text=sixth.strftime("%A"))

                day7 = Label(forecast_frame, bg='white', fg='#57a1f8')
                day7.place(x=750, y=256)

                seventh = first + timedelta(days=6)
                day7.config(text=seventh.strftime("%A"))

            back_button.place(x=340, y=410)

        def Map_details():
            dashboard_frame.place_forget()
            map_frame.place(x=0, y=0)
            map_widget.place(x=18, y=25)
            back_button.place(x=340, y=410)

        if username == 'Username' and password == 'Password':
            messagebox.showwarning("Warning", "Please enter username and password to proceed further...")

        else:
            cursor.execute("select * from people_content where name = %s and phone_number = %s",
                           [(username), (password)])
            user_details = cursor.fetchall()

            if user_details:
                username = user_details[0][0]
                messagebox.showinfo("Login Success", f"Welcome {username} !!")
                login_frame.place_forget()
                login_photo.place_forget()

                dashboard_frame = tk.Frame(root, bg="white", width=905, height=480, bd=0)
                dashboard_frame.place(x=10, y=10)

                location_frame = tk.Frame(root, bg="white", width=905, height=480, bd=0)
                forecast_frame = tk.Frame(root, bg="white", width=905, height=480, bd=0)
                map_frame = tk.Frame(root, bg="white", width=905, height=480, bd=0)

                map_widget = tkintermapview.TkinterMapView(map_frame, width=900, height=350, corner_radius=0)
                map_widget.set_position(12.225284, 79.074699)
                map_widget.set_zoom(15)

                dash_photo = tk.Label(dashboard_frame, image=dash_image, width=485, height=485)
                dash_photo.place(x=430, y=0)

                module_title = tk.Label(dashboard_frame, text="People Dashboard",
                                        font=('Microsoft YaHei UI Light', 24, 'bold'))
                module_title.config(fg="#57a1f8", bg='white')
                module_title.place(x=60, y=20)

                button_1 = tk.Button(dashboard_frame, text="Location Details", font=('Microsoft YaHei UI Light', 14))
                button_1.config(width=25, height=1, bd=0, command=location_details)
                button_1.place(x=63, y=120)

                button_2 = tk.Button(dashboard_frame, text="Weather Forecast", font=('Microsoft YaHei UI Light', 14))
                button_2.config(width=25, height=1, bd=0, command=forecast_app)
                button_2.place(x=63, y=200)

                button_3 = tk.Button(dashboard_frame, text="Mini - Mapview", font=('Microsoft YaHei UI Light', 14))
                button_3.config(width=25, height=1, bd=0, command=Map_details)
                button_3.place(x=63, y=280)

                back_button = tk.Button(root, text="Back", font=('Microsoft YaHei UI Light', 14), bd=0)
                back_button.config(command=home, width=20, height=1)

            else:
                messagebox.showerror("Failure", "Username or Password is not correct, Please try again correctly...")

    def user_on_enter(e):
        login_user_entry.delete(0, 'end')

    def user_on_leave(e):
        login_username = login_user_entry.get()
        if login_username == '':
            login_user_entry.insert(0, 'Username')

    login_user_entry = tk.Entry(login_frame, width=25, fg='black', border=0, bg='white',
                                font=('Microsoft YaHei UI Light', 11))
    login_user_entry.place(x=30, y=80)
    login_user_entry.insert(0, 'Username')
    login_user_entry.bind('<FocusIn>', user_on_enter)
    login_user_entry.bind('<FocusOut>', user_on_leave)

    tk.Frame(login_frame, width=295, height=2, bg='black').place(x=25, y=107)

    def pass_on_enter(e):
        login_pass_entry.delete(0, 'end')
        login_pass_entry.config(show='*')
        login_pass_show.config(image=passhide_icon)

    def pass_on_leave(e):
        login_pass_entry.config(show='')
        login_pass_show.config(fg='#fff', image='')
        login_password = login_pass_entry.get()
        if login_password == '':
            login_pass_entry.insert(0, 'Password')

    def passshow():
        global password_mode

        if password_mode:
            login_pass_show.config(image=passshow_icon)
            login_pass_entry.config(show='')
            password_mode = False
        else:
            login_pass_show.config(image=passhide_icon)
            login_pass_entry.config(show='*')
            password_mode = True

    login_pass_entry = tk.Entry(login_frame, width=25, fg='black', border=0, bg='white',
                                font=('Microsoft YaHei UI Light', 11))
    login_pass_entry.place(x=30, y=150)
    login_pass_entry.insert(0, 'Password')
    login_pass_entry.bind('<FocusIn>', pass_on_enter)
    login_pass_entry.bind('<FocusOut>', pass_on_leave)

    login_pass_show = tk.Button(login_frame, image='', border=0, bg='#fff', activebackground='#fff', command=passshow)
    login_pass_show.place(x=280, y=135, width=50, height=50)

    tk.Frame(login_frame, width=295, height=2, bg='black').place(x=25, y=177)

    login_login_btn = tk.Button(login_frame, width=42, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0,
                                command=signin)
    login_login_btn.place(x=25, y=235)

    root.mainloop()

except:
    print("Can't connect to MySQL Server.. If not, Please connect with MySQL Database in Xampp..")
