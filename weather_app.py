from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from datetime import date, time, datetime
from configparser import ConfigParser
import requests
import json

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']


today = date.today()

def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # (city, country, temp_celsius, farenheight, icon)
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (temp_kelvin - 273.15) * (9/5) + 32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        final = (city, country, temp_celsius, temp_fahrenheit, icon, weather)
        return final
    else:
        return None


def search():
    global image
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        location_lbl['text'] = '{}, {}'.format(weather[0], weather[1])
        img['file'] = 'weather_icons/{}@2x.png'.format(weather[4])
        temp_lbl['text'] = '{:.2f}°C, {:.2f}°F'.format(weather[2], weather[3])
        weather_lbl['text'] = weather[5]
    else:
        messagebox.showerror('Error', 'Cannot find city {}'.format(city))


app = Tk()
app.title("Babby's first weather app")
app.geometry("1000x500")
app.configure(bg='white')

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()


search_btn = Button(app, text="search weather", width=12, command=search)
search_btn.pack()

location_lbl = Label(app, text='Location', font=('bold', 20))
location_lbl.pack()

img = PhotoImage(file="")
image = Label(app, image=img)
image.pack()

temp_lbl = Label(app, text='temperature')
temp_lbl.pack()

weather_lbl = Label(app, text='weather')
weather_lbl.pack()

app.mainloop()