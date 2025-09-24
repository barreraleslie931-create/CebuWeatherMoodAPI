from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from .mood import weather_to_mood
from .services import WeatherService

app = FastAPI(
    title="Cebu Weather Mood API",
    description="Real-time weather updates with mood suggestions for Cebu City, PH.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

weather_service = WeatherService()

# ==============================
#  Real-Time Weather Mood (Styled Webpage with Auto-Refresh)
# ==============================
@app.get("/weather-mood", response_class=HTMLResponse, tags=["weather"])
def weather_mood_page():
    try:
        # Force Cebu City only
        city = "Cebu City"
        country = "PH"
        units = "metric"

        w = weather_service.fetch_current_weather(city=city, country=country, units=units)
        mood = weather_to_mood(w["weather"], w["description"])

        # Pick weather icon
        weather_icon = "🌤️"
        if "rain" in w["weather"].lower():
            weather_icon = "🌧️"
        elif "cloud" in w["weather"].lower():
            weather_icon = "☁️"
        elif "clear" in w["weather"].lower():
            weather_icon = "☀️"
        elif "storm" in w["weather"].lower() or "thunder" in w["weather"].lower():
            weather_icon = "⛈️"

        html_content = f"""
        <html>
            <head>
                <title>Cebu City Weather Mood</title>
                <meta http-equiv="refresh" content="60">
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        text-align: center;
                        background: linear-gradient(to right, #56ccf2, #2f80ed);
                        color: white;
                        padding: 50px;
                        margin: 0;
                    }}
                    .card {{
                        background: rgba(255,255,255,0.15);
                        padding: 40px;
                        border-radius: 20px;
                        box-shadow: 0px 4px 20px rgba(0,0,0,0.5);
                        display: inline-block;
                        max-width: 500px;
                    }}
                    h1 {{
                        margin-bottom: 20px;
                        font-size: 36px;
                    }}
                    p {{
                        font-size: 22px;
                        margin: 8px 0;
                    }}
                    .icon {{
                        font-size: 60px;
                    }}
                    small {{
                        display: block;
                        margin-top: 15px;
                        opacity: 0.8;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <div class="icon">{weather_icon}</div>
                    <h1>Cebu City Weather Mood</h1>
                    <p><b>City:</b> {city}, {country}</p>
                    <p><b>Weather:</b> {w["weather"]} - {w["description"]}</p>
                    <p><b>Temperature:</b> {w["temperature"]}°C</p>
                    <p><b>Mood Suggestion:</b> {mood}</p>
                    <small>Source: {w["source"]} | Auto-refresh every 1 minute 🔄</small>
                </div>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content)

    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


# ==============================
#  QR Code Generator (links to /weather-mood)
# ==============================
@app.get("/qrcode", response_class=HTMLResponse, tags=["utility"])
def generate_qrcode():
    qr_link = "http://10.22.22.2:8000/weather-mood"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={qr_link}"

    html_content = f"""
    <html>
        <head>
            <title>Cebu City Weather QR</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    text-align: center;
                    background: linear-gradient(to right, #00c6ff, #0072ff);
                    color: white;
                    padding: 50px;
                }}
                .card {{
                    background: rgba(255,255,255,0.15);
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0px 4px 20px rgba(0,0,0,0.5);
                    display: inline-block;
                }}
                img {{
                    margin-top: 20px;
                    border: 5px solid white;
                    border-radius: 15px;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>📱 Cebu City Weather QR</h1>
                <p>Scan this QR code to view Cebu City’s live weather & mood!</p>
                <img src="{qr_url}" alt="QR Code">
                <p><small>QR redirects to: <br><code>{qr_link}</code></small></p>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# ==============================
#  Homepage (styled landing page)
# ==============================
@app.get("/", response_class=HTMLResponse, tags=["home"])
def homepage():
    html_content = """
    <html>
        <head>
            <title>Cebu City Weather Mood API</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    text-align: center;
                    background: linear-gradient(135deg, #1e3c72, #2a5298);
                    color: white;
                    margin: 0;
                    padding: 0;
                }
                header {
                    padding: 50px 20px;
                    background: rgba(0,0,0,0.3);
                    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
                }
                h1 {
                    margin: 0;
                    font-size: 45px;
                }
                p {
                    font-size: 20px;
                    margin-top: 10px;
                }
                .container {
                    margin-top: 100px;
                }
                .button {
                    display: inline-block;
                    margin: 20px;
                    padding: 20px 40px;
                    font-size: 22px;
                    font-weight: bold;
                    text-decoration: none;
                    color: white;
                    border-radius: 15px;
                    box-shadow: 0px 6px 15px rgba(0,0,0,0.5);
                    transition: transform 0.2s, background 0.3s;
                }
                .button:hover {
                    transform: scale(1.08);
                }
                .click-weather {
                    background: linear-gradient(to right, #ff416c, #ff4b2b);
                }
                .click-weather:hover {
                    background: linear-gradient(to right, #ff4b2b, #ff416c);
                }
                .scan-weather {
                    background: linear-gradient(to right, #00b09b, #96c93d);
                }
                .scan-weather:hover {
                    background: linear-gradient(to right, #96c93d, #00b09b);
                }
                .secondary {
                    background: linear-gradient(to right, #0072ff, #00c6ff);
                    font-size: 18px;
                }
                .secondary:hover {
                    background: linear-gradient(to right, #00c6ff, #0072ff);
                }
                footer {
                    margin-top: 120px;
                    padding: 20px;
                    font-size: 14px;
                    background: rgba(0,0,0,0.3);
                }
            </style>
        </head>
        <body>
            <header>
                <h1>🌤️ Cebu City Weather Mood API</h1>
                <p>Real-time weather updates with mood suggestions for Cebu City</p>
            </header>
            <div class="container">
                <a class="button click-weather" href="/weather-mood">🌞 Click to Know Cebu City Weather Mood</a>
                <a class="button scan-weather" href="/qrcode">📱 Scan QR Code to Know Cebu City Weather Mood</a>
                <br>
                <a class="button secondary" href="/docs">📖 API Docs</a>
            </div>
            <footer>
                &copy; 2025 Cebu City Weather Mood API Project | Made with ❤️ in Cebu
            </footer>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
