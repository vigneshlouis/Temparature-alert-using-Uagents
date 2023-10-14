from uagents import Agent, Context
import requests
from plyer import notification

alice = Agent(name="alice", seed="alice recovery phrase")
global city_name
global min_temp
global max_temp



city_name = input("enter city")
min_temp = float(input("set your minimum temparature"))
max_temp = float(input("set your maximum temparature"))

@alice.on_interval(period=60.0)


async def get_weather(ctx: Context):
    ctx.storage.set("city_name", city_name)
    ctx.storage.set("min_temp", min_temp)
    ctx.storage.set("max_temp", max_temp)

    ctx.storage.set('api_key',"38c2e88646774f7019213f1986c39730")

    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={ctx.storage.get('city_name')}&appid={ctx.storage.get('api_key')}"
    params = {
        "name": ctx.storage.get('city_name'),
        "units": "metric",
        "appid": ctx.storage.get('api_key')
    }
    response = requests.get(api_url, params=params)
    data = response.json()


    name = data['name']
    desc = data['weather'][0]['description']
    temp = data['main']['temp']
    wndspeed = data['wind']['speed']
    humidity = data['main']['humidity']


    ctx.storage.set("temp",temp)
    ctx.storage.set("humidity", humidity)
    ctx.storage.set("wndspeed", wndspeed)
    ctx.storage.set("desc", desc)

    ctx.logger.info(f'hello, my name is {ctx.name}')
    ctx.logger.info(f"Alert!the temparature at your location is {ctx.storage.get('temp')}")
    ctx.logger.info(f"Your Location:{ctx.storage.get('city_name')}")
    ctx.logger.info(f"condition:{ctx.storage.get('desc')}")
    ctx.logger.info(f"Humidity:{ctx.storage.get('humidity')}%")
    ctx.logger.info(f"windspeed:{ctx.storage.get('wndspeed')}")


    if ctx.storage.get('temp')<ctx.storage.get('min_temp') or ctx.storage.get('temp') > ctx.storage.get('max_temp'):



        notification.notify(
            title="Alert",
            message=f"the temparature at{name} is{temp} !",
            app_name="main.py",
        )




if __name__ == "__main__":
    alice.run()
