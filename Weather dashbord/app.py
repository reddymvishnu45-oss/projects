from pymongo import MongoClient
import tkinter as tk 
import requests
import matplotlib.pyplot as plt 

API_KEY = "f88ee0ac646a22a8e317804f246c4602"

#--------------Data Base ----------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["Wether"]
collection = db["Wether_details"]

def save_data(city , temp, condition):
    collection.insert_one({'city':city,"temperature":temp,"condition":condition})

#------------Weather Api ------------------------
def get_wether():
    city = city_entry.get().strip()

    if city == '':
        result_label.config(text="Enter a city name")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url,timeout=5)
        data = response.json()
        print(data)

        if str(data.get("cod")) == '200':
            temp = data["main"]["temp"]
            condition = data["weather"][0]["description"]
            result_label.config(text=f"{city}\nTemperature: {temp} °C\nCondition: {condition}")

            save_data(city,temp,condition)
        else:
            result_label.config(text="City not found")
    except Exception as e:
        result_label.config(text=str(e))
        print(e)


#-------------------------Show History Function

def show_history():
    rows = collection.find()

    text = ""
    for r in rows:
        text += f"{r['city']}  {r['temperature']}°C  {r['condition']}\n"
    if text == "":
        result_label.config(text="No history found")
    else:
        result_label.config(text = text)

#------------------ How Chart Function -------------
def show_chart():
    rows = list(collection.find())
    if not rows:
        result_label.config(text = 'No data for chat')
        return 
    cities = [r["city"]for r in rows]
    temp = [r["temperature"]for r in rows]
    plt.bar(cities,temp)
    plt.xlabel("City")
    plt.ylabel("Temperature (c)")
    plt.title("weather History")
    plt.show()

# --------------- GUI Section -------------------------

root = tk.Tk()

root.title("Wether Dashboard")
root.geometry("550x500")

title = tk.Label(root , text="Weather Dashboard",font=("Arisl",18))
title.pack(pady=10)

city_entry = tk.Entry(root)
city_entry.pack(pady=10)

btn = tk.Button(root,text="Get Weather", command=get_wether)
btn.pack()

history_button = tk.Button(root,text="Show history",command=show_history)
history_button.pack()

Graph_button = tk.Button(root,text="Show Graph",command=show_chart)
Graph_button.pack()

result_label = tk.Label(root,text="")
result_label.pack(pady=10)

root.mainloop()