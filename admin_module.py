import tkinter as tk
from tkinter import *
from tkinter import PhotoImage
from tkinter import messagebox
from ultralytics import YOLO
from tracker import *
import cvzone
import pandas as pd
import PIL
from timezonefinder import TimezoneFinder
from geopy.geocoders import Photon
from PIL import Image, ImageTk
import mysql.connector
import qrcode
from datetime import *
import requests
import pytz
import cv2 as cv
import time

cap = cv.VideoCapture(0)
detector = cv.QRCodeDetector()

try:
    root = tk.Tk()
    root.title("Crowd Management System")
    root.geometry("925x500+300+200")
    login_count = 0
    total_count = 0

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

    login_icon = PhotoImage(file='images/admin_login.png')
    passshow_icon = PhotoImage(file='images/eye.png')
    passhide_icon = PhotoImage(file='images/hide.png')
    dash_image = PhotoImage(file="images/group_people.png")

    password_mode = True

    login_photo = tk.Label(root, image=login_icon, bg='white')
    login_photo.place(x=20, y=10)

    login_frame = tk.Frame(root, width=350, height=420, bg='white')
    login_frame.place(x=520, y=60)

    login_head = tk.Label(login_frame, text='Admin Login', fg='#57a1f8', bg='white',
                          font=('Microsoft YaHei UI Light', 23, 'bold'))
    login_head.place(x=75, y=5)

    details_icon = PhotoImage(file='images/crowd.png')

    def signin():
        global login_count, details_icon, total_count
        username = login_admin_entry.get()
        password = login_pass_entry.get()

        def home():
            dashboard_frame.place(x=10, y=10)
            dash_photo.place(x=430, y=0)
            database_frame.place_forget()
            forecast_frame.place_forget()
            camera_frame.place_forget()
            scanner_frame.place_forget()
            back_button.place_forget()

        def refresh():
            global total_count
            cursor.execute("select * from people_content")
            user_details = cursor.fetchall()
            total_count = len(user_details)
            crowd_label.config(text="Total Crowd Count: "+str(total_count))

        def database_details():
            dashboard_frame.place_forget()
            dash_photo.place_forget()
            database_frame.place(x=0, y=0)
            details_photo = tk.Label(database_frame, image=details_icon, bg='white')
            details_photo.place(x=430, y=-50)
            back_button.place(x=93, y=430)
            back_button.config(width=42, pady=7)

            page_lable = tk.Label(database_frame, text="People Database Details", font=('Microsoft YaHei UI Light', '23', 'bold'))
            page_lable.config(fg='#57a1f8', bg='white')
            page_lable.place(x=60, y=20)

            def people_enter_details():
                name = people_name_entry.get()
                address = people_address_entry.get()
                age = people_age_entry.get()
                phone_no = people_number_entry.get()

                cursor.execute("select * from people_content where name = %s and phone_number = %s",
                               [(name), (phone_no)])
                user_details = cursor.fetchall()

                if name == 'Person Name' and address == 'Address Details' and age == 'Age' and phone_no == 'Phone Number':
                    messagebox.showwarning("Warning", "Please enter the missing person details to proceed further..")
                elif name == '' or address == '' or age == '' or phone_no == '':
                    messagebox.showwarning("Warning", "Please enter the missing fields to save person details..")
                elif user_details:
                    messagebox.showwarning("Warning", f"{name} details already saved in database..")
                    people_name_entry.delete(0, 'end')
                    people_name_entry.insert(0, 'Person Name')
                    people_address_entry.delete(0, 'end')
                    people_address_entry.insert(0, 'Address Details')
                    people_age_entry.delete(0, 'end')
                    people_age_entry.insert(0, 'Age')
                    people_number_entry.delete(0, 'end')
                    people_number_entry.insert(0, 'Phone Number')
                else:
                    cursor.execute("insert into people_content values(%s,%s,%s,%s)", (name, address, age, phone_no))
                    db.commit()

                    people_data = list()
                    people_data.append(name)
                    people_data.append(address)
                    people_data.append(age)
                    people_data.append(phone_no)

                    people_qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
                    print(people_data)
                    people_qr.add_data(people_data)

                    people_qr.make(fit=True)
                    qr_img = people_qr.make_image(fill_color='violet', back_color='white')
                    qr_img.save('people_qrcode/{}_{}.png'.format(name, phone_no))

                    people_name_entry.delete(0, 'end')
                    people_name_entry.insert(0, 'Person Name')
                    people_address_entry.delete(0, 'end')
                    people_address_entry.insert(0, 'Address Details')
                    people_age_entry.delete(0, 'end')
                    people_age_entry.insert(0, 'Age')
                    people_number_entry.delete(0, 'end')
                    people_number_entry.insert(0, 'Phone Number')

                    messagebox.showinfo("Success", f"{name} details saved successfully in Database!!")

            def name_on_enter(e):
                people_name_entry.delete(0, 'end')

            def name_on_leave(e):
                people_username = people_name_entry.get()
                if people_username == '':
                    people_name_entry.insert(0, 'Person Name')

            people_name_entry = tk.Entry(database_frame, width=25, fg='black', border=0, bg='white',
                                         font=('Microsoft YaHei UI Light', 11))
            people_name_entry.place(x=100, y=110)
            people_name_entry.insert(0, 'Person Name')
            people_name_entry.bind('<FocusIn>', name_on_enter)
            people_name_entry.bind('<FocusOut>', name_on_leave)

            tk.Frame(database_frame, width=295, height=2, bg='black').place(x=95, y=137)

            def address_on_enter(e):
                people_address_entry.delete(0, 'end')

            def address_on_leave(e):
                people_address = people_address_entry.get()
                if people_address == '':
                    people_address_entry.insert(0, 'Address Details')

            people_address_entry = tk.Entry(database_frame, width=25, fg='black', border=0, bg='white',
                                            font=('Microsoft YaHei UI Light', 11))
            people_address_entry.place(x=100, y=180)
            people_address_entry.insert(0, 'Address Details')
            people_address_entry.bind('<FocusIn>', address_on_enter)
            people_address_entry.bind('<FocusOut>', address_on_leave)

            tk.Frame(database_frame, width=295, height=2, bg='black').place(x=95, y=207)

            def age_on_enter(e):
                people_age_entry.delete(0, 'end')

            def age_on_leave(e):
                people_age = people_age_entry.get()
                if people_age == '':
                    people_age_entry.insert(0, 'Age')

            people_age_entry = tk.Entry(database_frame, width=25, fg='black', border=0, bg='white',
                                        font=('Microsoft YaHei UI Light', 11))
            people_age_entry.place(x=100, y=250)
            people_age_entry.insert(0, 'Age')
            people_age_entry.bind('<FocusIn>', age_on_enter)
            people_age_entry.bind('<FocusOut>', age_on_leave)

            tk.Frame(database_frame, width=295, height=2, bg='black').place(x=95, y=277)

            def number_on_enter(e):
                people_number_entry.delete(0, 'end')

            def number_on_leave(e):
                people_number = people_number_entry.get()
                if people_number == '':
                    people_number_entry.insert(0, 'Phone Number')

            people_number_entry = tk.Entry(database_frame, width=25, fg='black', border=0, bg='white',
                                           font=('Microsoft YaHei UI Light', 11))
            people_number_entry.place(x=100, y=320)
            people_number_entry.insert(0, 'Phone Number')
            people_number_entry.bind('<FocusIn>', number_on_enter)
            people_number_entry.bind('<FocusOut>', number_on_leave)

            tk.Frame(database_frame, width=295, height=2, bg='black').place(x=95, y=347)

            details_enter_btn = tk.Button(database_frame, width=42, pady=7, text='Save Details', bg='#57a1f8', fg='white',
                                          border=0)
            details_enter_btn.config(command=people_enter_details)
            details_enter_btn.place(x=93, y=380)

        def forecast_app():
            dashboard_frame.place_forget()
            forecast_frame.place(x=0, y=0)

            weather_lable = Label(forecast_frame, text="Weather Forecast", font=('Microsoft YaHei UI Light', 20, 'bold'))
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

                label2 = Label(forecast_frame, text='Humidity', font=('Microsoft YaHei UI Light', 10), bg='white',
                               fg='#57a1f8')
                label2.place(x=390, y=130)

                label3 = Label(forecast_frame, text='Pressure', font=('Microsoft YaHei UI Light', 10), bg='white',
                               fg='#57a1f8')
                label3.place(x=390, y=150)

                label4 = Label(forecast_frame, text='Wind Speed', font=('Microsoft YaHei UI Light', 10), bg='white',
                               fg='#57a1f8')
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

            back_button.place(x=380, y=410)
            back_button.config(width=25, pady=7)

        def analysis_camera():
            dashboard_frame.place_forget()
            camera_frame.place(x=0, y=0)

            model = YOLO('Dataset/yolov8s.pt')

            def RGB(event, x, y, flags, param):
                if event == cv.EVENT_MOUSEMOVE:
                    point = [x, y]
                    print(point)

            cv.namedWindow('Crowd Analysis')
            cv.setMouseCallback('Crowd Analysis', RGB)
            cap = cv.VideoCapture('Dataset/Video1.mp4')

            my_file = open("Dataset/coco.txt", "r")
            data = my_file.read()
            class_list = data.split("\n")

            count = 0
            persondown = {}
            tracker = Tracker()
            counter1 = []

            personup = {}
            counter2 = []
            cy1 = 194
            cy2 = 220
            offset = 6
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                count += 1
                if count % 3 != 0:
                    continue
                frame = cv.resize(frame, (1020, 500))

                results = model.predict(frame)
                a = results[0].boxes.data
                px = pd.DataFrame(a).astype("float")
                list = []

                for index, row in px.iterrows():
                    x1 = int(row[0])
                    y1 = int(row[1])
                    x2 = int(row[2])
                    y2 = int(row[3])
                    d = int(row[5])

                    c = class_list[d]
                    if 'person' in c:
                        list.append([x1, y1, x2, y2])

                bbox_id = tracker.update(list)
                for bbox in bbox_id:
                    x3, y3, x4, y4, id = bbox
                    cx = int(x3 + x4) // 2
                    cy = int(y3 + y4) // 2
                    cv.circle(frame, (cx, cy), 4, (255, 0, 255), -1)

                    if cy1 < (cy + offset) and cy1 > (cy - offset):
                        cv.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
                        cvzone.putTextRect(frame, f'{id}', (x3, y3), 1, 2)
                        persondown[id] = (cx, cy)

                    if id in persondown:
                        if cy2 < (cy + offset) and cy2 > (cy - offset):
                            cv.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 255), 2)
                            cvzone.putTextRect(frame, f'{id}', (x3, y3), 1, 2)
                            if counter1.count(id) == 0:
                                counter1.append(id)

                    if cy2 < (cy + offset) and cy2 > (cy - offset):
                        cv.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
                        cvzone.putTextRect(frame, f'{id}', (x3, y3), 1, 2)
                        personup[id] = (cx, cy)

                    if id in personup:
                        if cy1 < (cy + offset) and cy1 > (cy - offset):
                            cv.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 255), 2)
                            cvzone.putTextRect(frame, f'{id}', (x3, y3), 1, 2)
                            if counter2.count(id) == 0:
                                counter2.append(id)

                cv.line(frame, (3, cy1), (1018, cy1), (0, 255, 0), 2)
                cv.line(frame, (5, cy2), (1019, cy2), (0, 255, 255), 2)

                down = (len(counter1))
                cvzone.putTextRect(frame, f'Down: {down}', (50, 60), 2, 2)
                up = (len(counter2))
                cvzone.putTextRect(frame, f'Up: {up}', (50, 160), 2, 2)
                cv.imshow("Crowd Analysis", frame)
                if cv.waitKey(1) & 0xFF == ord(' '):
                    break

            back_button.place(x=380, y=410)
            back_button.config(width=25, pady=7)

        def qr_scanner():
            cap = cv.VideoCapture(0)
            dashboard_frame.place_forget()
            scanner_frame.place(x=0, y=0)

            label = tk.Label(scanner_frame)
            label.place(x=30, y=20)

            def clear_content():
                global Name, Address, Age, Phone

                Name.place_forget()
                Address.place_forget()
                Age.place_forget()
                Phone.place_forget()

            def show_frames():
                global Name, Address, Age, Phone
                read = cap.read()[1]
                data, bbox, _ = detector.detectAndDecode(read)

                if data:
                    print("QR Detected Successfully")
                    people_data = data
                    people_data = people_data.split("', '")
                    people_data[0] = people_data[0].replace("['", "")
                    people_data[3] = people_data[3].replace("']", "")
                    print("------------ Person Details -------------")
                    print(f"Name: {people_data[0]}")
                    print(f"Address: {people_data[1]}")
                    print(f"Age: {people_data[2]}")
                    print(f"Phone No: {people_data[3]}")
                    Name = tk.Label(scanner_frame, text=f"Name: {people_data[0]}",
                                    font=('Microsoft YaHei UI Light', '16', 'bold'))
                    Name.config(bg='white', fg='#57a1f8')
                    Name.place(x=600, y=100)
                    Address = tk.Label(scanner_frame, text=f"Address: {people_data[1]}",
                                       font=('Microsoft YaHei UI Light', '16', 'bold'))
                    Address.config(bg='white', fg='#57a1f8')
                    Address.place(x=600, y=150)
                    Age = tk.Label(scanner_frame, text=f"Age: {people_data[2]}",
                                   font=('Microsoft YaHei UI Light', '16', 'bold'))
                    Age.config(bg='white', fg='#57a1f8')
                    Age.place(x=600, y=200)
                    Phone = tk.Label(scanner_frame, text=f"Phone: {people_data[3]}",
                                     font=('Microsoft YaHei UI Light', '16', 'bold'))
                    Phone.config(bg='white', fg='#57a1f8')
                    Phone.place(x=600, y=250)

                    time.sleep(10)

                read = cv.resize(read, (500, 400))
                cv2image = cv.cvtColor(read, cv.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                label.imgtk = imgtk
                label.configure(image=imgtk)
                label.after(10, show_frames)

            show_frames()

            clear_button = tk.Button(scanner_frame, text='Clear', width=25, pady=7, bd=0)
            clear_button.config(command=clear_content)
            clear_button.place(x=640, y=360)
            back_button.place(x=640, y=410)
            back_button.config(width=25, pady=7)

        if username == 'Username' and password == 'Password':
            messagebox.showwarning("Warning", "Please enter username and password to proceed further...")
        elif username == 'admin' and password == 'admin':
            messagebox.showinfo("Success", "Admin Login Successfully !!!")
            login_frame.place_forget()
            login_photo.place_forget()

            dashboard_frame = tk.Frame(root, bg="white", width=905, height=480, bd=0)
            dashboard_frame.place(x=10, y=10)

            database_frame = tk.Frame(root, bg="white", width=905, height=480, bd=0)
            forecast_frame = tk.Frame(root, bg="white", width=905, height=480, bd=0)
            camera_frame = tk.Frame(root, bg="white", width=905, height=480, bd=0)
            scanner_frame = tk.Frame(root, bg="white", width=905, height=480, bd=0)

            dash_photo = tk.Label(dashboard_frame, image=dash_image, width=485, height=485)
            dash_photo.place(x=430, y=0)

            module_title = tk.Label(dashboard_frame, text="Admin Dashboard",
                                    font=('Microsoft YaHei UI Light', 24, 'bold'))
            module_title.config(fg="#57a1f8", bg='white')
            module_title.place(x=60, y=20)

            button_1 = tk.Button(dashboard_frame, text="Add Details", font=('Microsoft YaHei UI Light', 14))
            button_1.config(width=25, height=1, bd=0, command=database_details)
            button_1.place(x=63, y=110)

            button_2 = tk.Button(dashboard_frame, text="Weather Forecast", font=('Microsoft YaHei UI Light', 14))
            button_2.config(width=25, height=1, bd=0, command=forecast_app)
            button_2.place(x=63, y=170)

            button_3 = tk.Button(dashboard_frame, text="Camera Analysis", font=('Microsoft YaHei UI Light', 14))
            button_3.config(width=25, height=1, bd=0, command=analysis_camera)
            button_3.place(x=63, y=230)

            button_4 = tk.Button(dashboard_frame, text="QR Scanner", font=('Microsoft YaHei UI Light', 14))
            button_4.config(width=25, height=1, bd=0, command=qr_scanner)
            button_4.place(x=63, y=290)

            back_button = tk.Button(root, text="Back", bd=0)
            back_button.config(command=home)

            crowd_label = tk.Label(dashboard_frame, text="Total Crowd Count: "+str(total_count), font=('Microsoft YaHei UI Light', 11))
            crowd_label.config(fg="red", bg="white")
            crowd_label.place(x=130, y=370)

            refresh_btn = tk.Button(dashboard_frame, text="Refresh", font=('Microsoft YaHei UI Light', 11))
            refresh_btn.config(command=refresh, bd=0, width=10)
            refresh_btn.place(x=160, y=420)

        else:
            login_count += 1
            if login_count > 3:
                root.destroy()
                messagebox.showwarning("Malfunction Alert", "Someone trying to login Admin database... Be Alert...")
            else:
                messagebox.showerror("Failure", "Username or Password is not correct, Please try again correctly...")

    def admin_on_enter(e):
        login_admin_entry.delete(0, 'end')

    def admin_on_leave(e):
        admin_username = login_admin_entry.get()
        if admin_username == '':
            login_admin_entry.insert(0, 'Username')

    login_admin_entry = tk.Entry(login_frame, width=25, fg='black', border=0, bg='white',
                                 font=('Microsoft YaHei UI Light', 11))
    login_admin_entry.place(x=30, y=80)
    login_admin_entry.insert(0, 'Username')
    login_admin_entry.bind('<FocusIn>', admin_on_enter)
    login_admin_entry.bind('<FocusOut>', admin_on_leave)

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
