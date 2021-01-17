import requests
import datetime as dt
import smtplib
import time

priya_email = "TO SEND EMAIL ID"
my_email = "EMAIL ID"
password = "PASSWORD"
MY_LAT = 28.581130
MY_LONG = 77.085410
MY_POSI = (MY_LAT, MY_LONG)
# ------------------ ISS DATA ---------------------------#
iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
iss_response.raise_for_status()
iss_data = iss_response.json()
iss_lat = float(iss_data["iss_position"]["latitude"])
iss_lng = float(iss_data["iss_position"]["longitude"])
iss_parameters = (float(iss_data["iss_position"]["latitude"]), float(iss_data["iss_position"]["longitude"]))
# -------------------- DAY DATA -----------------------------#

parameters = {
            "lat": MY_LAT,
            "lng": MY_LONG,
            "formatted": 0
}
day_response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
day_response.raise_for_status()
day_data = day_response.json()
sunset = int(day_data["results"]["sunset"].split("T")[1].split(":")[0])
time_now = dt.datetime.now()
current_hour = time_now.hour
close_lat = MY_LAT - iss_lat
close_lng = MY_LONG - iss_lng
flag = True
while flag:
    if close_lng <= 5 and close_lat <= 5 and current_hour > sunset:
        with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=priya_email,
                                msg="subject:ISS\n\nLook out ISS Over your head")
    time.sleep(60)

