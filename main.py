import sys
import requests

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, 
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Choose a city: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Show weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.iniUI()

    def iniUI(self):
        self.setWindowTitle("[Weather App]")
        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton{font-family: Arial;}
                        
            QLabel#city_label{font-size: 30px; font-weight: bold}
            
            QLineEdit#city_input{font-size: 20px;} 

            QPushButton#get_weather_button{font-size: 20px;}    

            QLabel#temperature_label{font-size: 20px;} 

            QLabel#emoji_label{font-size: 50px; font-family: Segoe UI emoji} 

            QLabel#description_label{font-size: 20px;}    

            """)
        
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "10cd1d0b5982c32f7b963f3186a35b72"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org//data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            if data["cod"] == 200:
                self.display_weather(data)
        
        except requests.exceptions.HTTPError as http_error:
                match response.status_code:
                     case 400:
                          self.display_error("[Bad request]\n")
                     case 403:
                          self.display_error("[Access denied]\n")
                     case 404:
                          self.display_error("[City not found]\n")
                     case 500:
                          self.display_error("[Please try again later]\n")
                     case 502:
                          self.display_error("[Bad Gateway]\n")
                     case 503:
                          self.display_error("[Server is down]\n")
                     case 504:
                          self.display_error("[Timeout]\n")
                     case _:
                          self.display_error(f"[HTTP error]\n{http_error}")
        except requests.exceptions.TooManyRedirects:
                self.display_error("[Try again after a few moments]\n")
        except requests.exceptions.Timeout:
                self.display_error("[A Timeout error has occured]\n")
        except requests.exceptions.ConnectionError:
                self.display_error("[Connection couldn't be established]\n")
        except requests.exceptions.RequestException as req_error:
                self.display_error("[Unkown request error]\n")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()


    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 30px")
        kelvin = data["main"]["temp"]
        celsius = kelvin - 273.15
        fahrenheit = (kelvin * 9/5) - 459.67
        weather_id = data["weather"][0]["id"]
        descriptor = data["weather"][0]["description"]

        self.temperature_label.setText(f"\nCelsius: {celsius:.1f}℃")
        self.emoji_label.setText(self.get_emoji(weather_id))
        self.description_label.setText(descriptor)
    
    @staticmethod
    def get_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈"
        elif 300 <= weather_id <= 321:
            return "🌥"
        elif 500 <= weather_id <= 531:
            return "🌨"
        elif 600 <= weather_id <= 622:
            return "❄"
        elif 701 <= weather_id <= 741:
            return "🌫"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀"
        elif 801 <= weather_id <= 804:
            return "☁"
        else:
            return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())

