
def generate_weather_data_summary(weather_data):
    weather_summary = []
    days = []

    if "list" in weather_data:
        city = weather_data['city'].get('name', 'Unknown')
        for i, day in enumerate(weather_data["list"]):
         if i % 8 == 0: # if it's forecast for 5 days with 40 items in list
             days.append(weather_data['list'][i])
    else:
        city = weather_data.get('name', 'Unknown')
        days.append(weather_data)

    for day in days:
        day_summary = {
            "city": city,
            "current_temp": day['main'].get('temp'),
            "feels_like_temp": day['main'].get('feels_like'),
            "min_temp": day['main'].get('temp_min'),
            "max_temp": day['main'].get('temp_max'),
            "description": day['weather'][0].get('description'),
            "humidity": day['main'].get('humidity'),
            "wind_speed": day['wind'].get('speed'),
            "wind_deg": day['wind'].get('deg', 0),
            "rain_volume": day.get('rain', {}).get('1h', 0),
            "cloudiness": day['clouds'].get('all'),
        }
        weather_summary.append(day_summary)

    return weather_summary
