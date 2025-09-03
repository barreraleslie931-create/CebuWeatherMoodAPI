def weather_to_mood(main: str, description: str) -> str:
    main = (main or "").title()
    mapping = {
        "Clear": "It's sunny in Cebu! 🌞 Perfect for outdoor plans or a seaside walk.",
        "Clouds": "Cloudy skies ☁️ — great for a chill cafe day or reading indoors.",
        "Rain": "Rainy weather 🌧️ — time for comfort food, music, or a movie.",
        "Thunderstorm": "Stormy ⚡ Stay safe, stay cozy, and enjoy a warm drink.",
        "Drizzle": "Light rain 🌦️ — bring an umbrella and take it slow.",
    }
    return mapping.get(main, f"Enjoy your day in Cebu! 🌴 ({main or 'Weather'})")
