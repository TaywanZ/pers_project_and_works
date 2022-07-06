import requests

appid = "pass"  # полученный при регистрации на OpenWeatherMap.org

# city_id for Кучугуры
city_id = 000000


def get_wind_direction(deg):
    l = ['С ','СВ',' В','ЮВ','Ю ','ЮЗ',' З','СЗ']
    for i in range(0,8):
        step = 45.
        min = i*step - 45/2.
        max = i*step + 45/2.
        if i == 0 and deg > 360-45/2.:
            deg = deg - 360
        if deg >= min and deg <= max:
            res = l[i]
            break
    return res


# Прогноз
def request_forecast(city_id = 539946):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        weawer = str()
        for i in data['list']:
            if i['dt_txt'][11:13] in ['09', '18']:
                weawer += '*' + i["dt_txt"][5:16].replace('-', '.') + '*' + ': 🌡' + '{0:+3.0f}'.format(i["main"]["temp"]) + ', 💨'
                weawer += '{0:2.0f}'.format(i['wind']['speed']) + " м/с" + ' ' + get_wind_direction(i['wind']['deg'])
                weawer += ', ' + i['weather'][0]['description'] + '\n'
        return weawer
    except:
        return 'Сервер прогноза погоды временно не доступен'

