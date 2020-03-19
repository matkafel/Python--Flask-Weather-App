from flask import Flask, render_template, request
import datetime
import time
import requests


class ZapisPogodowy:
    def __init__(self, godzina, temperatura, wiatr, poziomZachmurzenia, cisnienie):
        self.godzina = godzina
        self.temperatura = temperatura
        self.wiatr = wiatr
        self.poziomZachmurzenia = poziomZachmurzenia
        self.cisnienie = cisnienie

    def __str__(self):
        return (str(self.godzina)+"\n"+str(self.temperatura)+"\n"+str(self.wiatr)+"\n"+str(self.poziomZachmurzenia)+"\n"+str(self.cisnienie))


class metody:

    @staticmethod
    def get_weather(location):
        url = "https://api.openweathermap.org/data/2.5/forecast?q={}&appid=53d0a415a6e0cd631d9f0bf05c1ab4d1".format(
            location)
        r = requests.get(url)
        return r.json()


class aplikacja:
    app = Flask("Apkka")

    @staticmethod
    @app.route('/temperature', methods=['POST'])
    def temperature():
        city = request.form['zip']

        w_data = metody.get_weather(city)
        ts = time.time()
        notowaniaPogodwe = []
        for i in range(4):
            godzina = w_data['list'][i]['dt_txt'].split()[1]
            w_data['list'][i]['main']['temp'] = format(
                w_data['list'][i]['main']['temp']-273.15, '.2f')
            temperatura = w_data['list'][i]['main']['temp']
            wiatr = w_data['list'][i]['wind']['speed']
            poziomzachmurzenia = w_data['list'][i]['clouds']['all']
            cisnienie = w_data['list'][i]['main']['pressure']
            nowy = ZapisPogodowy(godzina, temperatura, wiatr,
                                 poziomzachmurzenia, cisnienie)
            notowaniaPogodwe.append(nowy)
            print(notowaniaPogodwe[i])
            print("\n")
        st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

        return render_template('temperature.html', city=city, data=w_data, time=st)

    @staticmethod
    @app.route('/')
    def index():
        return render_template('index.html')

    if __name__ == '__main__':
        app.run(debug=True)
