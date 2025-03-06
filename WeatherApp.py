import requests
import sys
import os
from PyQt5.QtWidgets import QApplication,QComboBox,QFrame,QListWidgetItem, QListWidget, QMainWindow, QLabel,QLineEdit,QPushButton,QHBoxLayout,QWidget,QVBoxLayout,QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor,QIcon,QPixmap
from PyQt5.QtCore import Qt,QSize,QEvent
from datetime import datetime,timedelta,timezone
from dotenv import load_dotenv

def get_icone(weather_id):    
        if weather_id == 800:
            return "images/sunny_icon.png"  # Clear Sky (Day)
        elif 801 <= weather_id <= 804:
            return "images/cloudy_icon.png"  # Cloudy
        elif 200 <= weather_id <= 232:
            return "images/orange.png"  # Thunderstorm
        elif 300 <= weather_id <= 321:
            return "images/drizzle_icon.png"  # Drizzle
        elif 500 <= weather_id <= 504:
            return "images/Pluie_icone.png"  # Rain
        elif 511 == weather_id or 600 <= weather_id <= 622:
            return "images/Neige_icone.png"  # Snow
        elif 701 <= weather_id <= 781:
            return "images/Brouillard_icone.png"  # Mist/Fog/Dust
        else:
            return "images/sunny_icon.png.png"  # Default: Clear Sky

def get_iconWeeks(code_weather):
    if code_weather==0:
        return "☀"
    elif code_weather==1 or code_weather==2 or code_weather==3 :
         return "🌤"
    elif code_weather==45 or code_weather==48 :
        return "🌫"
    elif code_weather==51 or code_weather==53 or code_weather==55 :
        return " 🌦 "
    elif code_weather==56 or code_weather==57 :
        return "🌨"
    elif code_weather==66  or code_weather==67 :
        return "🧊"
    elif code_weather==61 :
        return "🌦️"
    elif code_weather==63 :
        return "🌧️"
    elif code_weather==65 :
        return "⛈️" 
    elif code_weather==80 or code_weather== 81 or code_weather== 82  :
        return "🌦⚡"
    elif code_weather==95:
        return "⛈"
    elif code_weather==96 or code_weather==99  :
        return "⛈❄"
    elif code_weather==71 or code_weather==  73 or code_weather==75  :
        return "❄"
    elif code_weather==77 :
        return "🌨"
    elif code_weather==85 or code_weather== 86:
        return "🌨"


def shadow_effect(obj,nb1,nb2,nb3,color):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(nb1)  # Soft shadow
        shadow.setXOffset(nb2)
        shadow.setYOffset(nb3)
        shadow.setColor(color)  # Black shadow with slight transparency
        obj.setGraphicsEffect(shadow)


def styleListCity(color_background,color,list):
        list.setStyleSheet(f"""            
                                    border-radius: 35px;
                                    font-size:25px;
                                    font-family:Times New Roman;
                                    background:{color_background};
                                    color:{color};
                                    padding-top:20px;
                                    padding-left:30px;
                                    """)
        

class LineSeparator(QWidget):
    def __init__(self):
        super().__init__()  # Inherit from QWidget
        layout = QVBoxLayout(self)  # Use a vertical layout

        # Create a horizontal line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)  # Set the shape to a horizontal line
        line.setFrameShadow(QFrame.Plain)  # No shadow effect
        line.setStyleSheet("background-color:  #616a6b ; height: 2px;")  # Styling the line
        line.setFixedWidth(300)  # Set the width to 200 pixels
        layout.addWidget(line, alignment=Qt.AlignCenter)  # Align it to center

        layout.addWidget(line)  # Add the line to the layout
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for a clean look
        self.setLayout(layout)  # Apply the layout to the widget

def add_separator_to_list(list_widget):
    separator_widget = LineSeparator()  # Create a separator widget
    separator_item = QListWidgetItem(list_widget)  # Create a new list item

    # Set the size of the item to match the separator widget
    separator_item.setSizeHint(separator_widget.sizeHint())

    list_widget.addItem(separator_item)  # Add the item to the list
    list_widget.setItemWidget(separator_item, separator_widget)  # Assign the widget to the item


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.city=""
        CentralWidget=QWidget()
        self.image_background = QLabel(self)
        image = QPixmap("images/image_background 2.png")  # Load the image
        self.image_background.setPixmap(image)
        self.image_background.setScaledContents(True)
        # Main layout for the page
        layout = QHBoxLayout()
        layout.addWidget(self.image_background)  # Add the background image to layout
            
        # Set the layout to the main page
        CentralWidget.setLayout(layout)
        self.setCentralWidget(CentralWidget)
        self.body_box=QLabel("",self)
        
        self.toPage_1_button= QPushButton(self)
        self.toPage_2_button = QPushButton(self)
        self.CurentWeather=QLabel("The Current\n  Weather",self)
        self.icone=QLabel(self)
        self.temp=QLabel("",self)
        self.LowtHightemp=QLabel("",self)
        self.description=QLabel("",self)
        self.cityTime=QLabel("",self)
        self.day=QLabel("",self)
        self.Calendar_icon=QLabel(self)
        self.location=QLabel("",self)
        self.location_icon=QLabel(self)
        self.converterPage1=QComboBox(self)
        self.converterPage1.addItem("°C")
        self.converterPage1.addItem("°F")
        
        
        
        #humidity BOX
        self.humidityIcon=QLabel(self)
        self.humidityValeur=QLabel("",self)
        self.humidityLabel=QLabel("Humidity",self)
        

        # pressure BOX
        self.pressureIcon=QLabel(self)
        self.pressureLabel=QLabel("Pressure",self)
        self.pressureValeur=QLabel("",self)
        
        # Visibility BOX
        self.VisibilityIcon=QLabel(self)
        self.VisibilityLabel=QLabel("Visibility",self)
        self.VisibilityValeur=QLabel("",self)
        
        # Wind  BOX
        self.WindIcon=QLabel(self)
        self.WindLabel=QLabel("Wind Speed",self)
        self.WindValeur=QLabel("",self)

        # sunsit surise BOX
        self.sunriseIcon=QLabel(self)
        self.sunriseLabel=QLabel("Sunrise",self)
        self.sunriseValeur=QLabel("",self)
        # sunsit surise BOX
        self.sunsetIcon=QLabel(self)
        self.sunsetLabel=QLabel("Sunset",self)
        self.sunsetValeur=QLabel("",self)

        # Charger les variables d'environnement depuis .env
        if load_dotenv():
            print("Fichier .env chargé avec succès")
        else:
            print("Erreur : Impossible de charger le fichier .env")
        self.Api_Key=os.getenv("API_KEY")
        self.base_url_CityEntered = "http://api.openweathermap.org/geo/1.0/direct"

        #####   VARIABLE PAGE 2 ###############
        self.hours_list = QListWidget(self)
        self.date=QLabel("",self)
        self.Country=QLabel("",self)
        self.locationIcon=QLabel(self)
        self.temp_page2=QLabel("",self)
        self.titre_day=QLabel("7-Days Forecast",self)
        self.titre_hour=QLabel("Next Hour's Forecast",self)
        self.citySearchedList=QListWidget(self)
        self.linesearch_Cadre=QLabel(" ",self)
        self.buttonSearch=QPushButton(self)
        self.line_edit=QLineEdit(self)
        self.buttom=QPushButton("Search",self) #VARIABLE PAGE 1
        self.searchicon=QLabel(self)
        self.converterPage2=QComboBox(self)
        self.converterPage2.addItem("°C")
        self.converterPage2.addItem("°F")
        ## day1 BOX
        self.day1_Text=QLabel("day1",self)
        self.day1_Icon=QLabel("",self)
        self.day1_temp=QLabel("",self)
        
        ## day2 BOX
        self.day2_Text=QLabel("day2",self)
        self.day2_Icon=QLabel("",self)
        self.day2_temp=QLabel("",self)
        
        ## day3 BOX
        self.day3_Text=QLabel("day3",self)
        self.day3_Icon=QLabel("",self)
        self.day3_temp=QLabel("",self)
        
        ## day4 BOX
        self.day4_Text=QLabel("day4",self)
        self.day4_Icon=QLabel("",self)
        self.day4_temp=QLabel("",self)
        
        ## day5 BOX
        self.day5_Text=QLabel("day5",self)
        self.day5_Icon=QLabel("",self)
        self.day5_temp=QLabel("",self)
        
        ## day6 BOX
        self.day6_Text=QLabel("day6",self)
        self.day6_Icon=QLabel("",self)
        self.day6_temp=QLabel("",self)
        
        ## day7 BOX
        self.day7_Text=QLabel("day7",self)
        self.day7_Icon=QLabel("",self)
        self.day7_temp=QLabel("",self)
        

        self.hide_elm_Page2()
        self.initUI()
   
    def initUI(self):
        self.body_box.setGeometry(170,40,1600,850)
        self.body_box.setStyleSheet("background-color: rgba(0, 0, 0, 100);border-radius:35px;")
        self.line_edit.setGeometry(250,80,650,75)
        self.line_edit.setStyleSheet("""
                                    padding-left:60px;
                                    padding-right:80px;
                                    font-size:35px;
                                    font-weight:bold;
                                    font-family:Times New Roman; 
                                    border-radius:35px;
                                    background:rgb(0, 0, 0);
                                    color: white;
                                """)
        self.line_edit.setPlaceholderText("Search City ...")
        self.line_edit.textChanged.connect(self.searchbar)
        self.searchicon.setPixmap(QPixmap("images/search_icone_small.png"))
        self.searchicon.setGeometry(260,100,30,30)
        self.searchicon.setScaledContents(True)

        self.citySearchedList.setGeometry(250,160,650,400)
        self.citySearchedList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        styleListCity("black","white",self.citySearchedList)
        '''self.citySearchedList.setStyleSheet("""
                                            border-top-left-radius: 0px;
                                            border-top-right-radius: 0px;
                                            border-bottom-left-radius: 35px;
                                            border-bottom-right-radius: 35px;
                                            font-size:25px;
                                            font-family:Times New Roman;
                                            background:rgb(0, 0, 0);
                                            color:White;
                                            padding-top:50px;
                                            padding-left:30px;
                                            border: 1px solid;
                                        """)'''
        self.citySearchedList.itemClicked.connect(self.selectItem)
        self.citySearchedList.hide()
        shadow_effect(self.citySearchedList,8,5,5,QColor(0, 0, 0,100))
        self.buttom.setGeometry(830,80,200,75) 
        self.setStyleSheet("""
                           QPushButton{
                           font-size:40px;
                           border-radius:35px;
                           padding: 10px 20px;
                           color:White;
                           font-family:Times New Roman;
                           background:hsl(198, 76.30%, 29.80%);
                           font-weight:bold;
                           }
                           QPushButton:hover{
                           background:hsl(198, 54.40%, 66.50%);
                           }
                           
                           """)
        self.buttom.clicked.connect(self.click_buttonPaga1)
        self.CurentWeather.setGeometry(1220,100,500,200)
        self.CurentWeather.setStyleSheet("color:hsl(0, 7%, 82%);font-size:70px;")
        self.CurentWeather.setAlignment(Qt.AlignCenter)
        shadow_effect(self.CurentWeather,8,2,2,QColor(0, 0, 0, 180))
        self.CurentWeather.hide()
        self.converterPage1.setGeometry(1070,294,80,40)
        self.converterPage1.setStyleSheet("""
                                     font-size: 25px;
                                     border-radius: 10px;
                                     background:hsl(198, 76.30%, 29.80%);  
                                     color: white;
                                     padding: 5px;
                                """)
        # Connect dropdown selection change event
        self.converterPage1.currentIndexChanged.connect(self.convert_temperaturePage1)
        self.converterPage1.hide()
        self.ButtonPageToPage(self.toPage_2_button,"images/button3.png",1790)
        self.toPage_2_button.clicked.connect(self.setup_page_2)
        self.ButtonPageToPage(self.toPage_1_button,"images/button3_inverse.png",80)
        self.toPage_1_button.clicked.connect(self.setup_Page1)
        
        self.temp.setGeometry(580,270,600,300)
        self.temp.setAlignment(Qt.AlignCenter)
        self.temp.setStyleSheet("font-size:150px;font-family: Arial;font-weight:bold;color:White;")
        self.LowtHightemp.setGeometry(670,500,500,40)
        self.LowtHightemp.setStyleSheet("font-size:23px;color:hsl(217, 88%, 92%);font-family: Times New Roman;font-weight:bold;")
        shadow_effect(self.LowtHightemp,8,2,2,QColor(0, 0, 0, 180))
        self.icone.setGeometry(300,270,300,300)
        self.icone.setAlignment(Qt.AlignCenter)
        self.icone.setScaledContents(True)
        self.description.setGeometry(330,570,700,50)
        self.description.setAlignment(Qt.AlignCenter)
        self.description.setStyleSheet("font-size:35px;font-family: Times New Roman;font-weight:bold;color:hsl(39, 97%, 60%);")
        shadow_effect(self.description,8,2,2,QColor(0, 0, 0, 180))
        self.day.setGeometry(100,175,500,100)
        self.day.setAlignment(Qt.AlignCenter)
        self.day.setStyleSheet("font-size:20px;font-family: Roboto ;color:white;font-weight:bold")

        self.Calendar_icon.setPixmap(QPixmap("images/calendar_icon.png"))
        self.Calendar_icon.setScaledContents(True)
        self.Calendar_icon.setAlignment(Qt.AlignCenter)
        self.Calendar_icon.setGeometry(193,210,25,25)
        self.Calendar_icon.hide()
        self.location.setGeometry(230,94,500,200)
        self.location.setStyleSheet("font-size:20px;font-family: Roboto;font-weight:bold;color:white;")
        pixmap=QPixmap("images/location_icon.png")
        self.location_icon.setPixmap(pixmap)
        self.location_icon.setScaledContents(True)
        self.location_icon.setAlignment(Qt.AlignCenter)
        self.location_icon.setGeometry(185,170,40,40)
        self.location_icon.hide()

        
        

        #   CREATE WIDGETS IN THE BUTTOM
        self.widget1=self.create_Widget(self.humidityIcon,"images/humidity_icon1.png",self.humidityLabel,self.humidityValeur)
        self.widget2=self.create_Widget(self.pressureIcon,"images/pressure_icon.png",self.pressureLabel,self.pressureValeur)
        self.widget3=self.create_Widget(self.VisibilityIcon,"images/visibility_weather.png",self.VisibilityLabel,self.VisibilityValeur)
        self.widget4=self.create_Widget(self.WindIcon,"images/wind_icon2.png",self.WindLabel,self.WindValeur)
        self.widget5=self.create_Widget(self.sunriseIcon,"images/sunrise_icon.png",self.sunriseLabel,self.sunriseValeur)
        self.widget6=self.create_Widget(self.sunsetIcon,"images/sunset_icon.png",self.sunsetLabel,self.sunsetValeur)
         #-----------Style_Widget_i
        self.style_widget(self.widget1,130,130)
        self.style_widget(self.widget2,130,130)
        self.style_widget(self.widget3,130,130)
        self.style_widget(self.widget4,130,130)
        self.style_widget(self.widget5,130,130)
        self.style_widget(self.widget6,130,130)
        #------------POSITION BOXES
        self.widget1.move(300,690)
        self.widget2.move(500,690)
        self.widget3.move(700,690)
        self.widget4.move(900,690)
        self.widget5.move(1350,690)
        self.widget6.move(1520,690)
        
        #################       PAGE  2   ##########################################
        self.linesearch_Cadre.setGeometry(230,65,780,108)
        self.linesearch_Cadre.setStyleSheet("background:hsl(0, 7%, 82%);border-radius:50px;")
        
        self.buttonSearch.setIcon(QIcon("images/search_buttom.png"))
        self.buttonSearch.setIconSize(QSize(60,60))
        self.buttonSearch.setGeometry(920,80,70,70)
        self.buttonSearch.setToolTip("Search")
        self.buttonSearch.clicked.connect(self.click_buttonPaga2)
        app.setStyleSheet("""
            QToolTip {
                        background-color: #333;
                        color: white;
                        border: 1px solid #555;
                        padding-left:5px;
                        padding-right:5px;
                        font-size: 16px;  
                        font-weight:bold; 
                        font-family:Arial;                     
                    }
                """)
    
        self.converterPage2.setGeometry(820,100,60,30)
        self.converterPage2.setStyleSheet("""
                                     font-size: 25px;
                                     border-radius: 10px;
                                     background:transparent;
                                     color: hsl(136, 4%, 46%);
                                     font-weight:bold;
                                     padding: 5px;
                                """)
        self.converterPage2.currentIndexChanged.connect(self.convert_temperaturePage2)
        #self.converterPage2.hide()
       
        pixmap=QPixmap("images/location_icon.png")
        self.locationIcon.setPixmap(pixmap)
        self.locationIcon.setScaledContents(True)
        self.locationIcon.setGeometry(110,210,70,70)
        self.Country.setGeometry(180,200,200,100)
        self.Country.setStyleSheet("font-size:30px;font-family: Roboto;font-weight:bold;color:white")
        shadow_effect(self.Country,8,2,2,QColor(0, 0, 0, 180))
        self.date.setGeometry(120,290,400,20)
        self.date.setStyleSheet("font-size:25px;font-family: Roboto;font-weight:bold;color:white")
        shadow_effect(self.date,8,2,2,QColor(0, 0, 0, 180))
        self.temp_page2.setGeometry(150,340,400,40)
        self.temp_page2.setStyleSheet("font-size:40px;font-family: Roboto;font-weight:bold;color:white")
        
        self.hours_list.setGeometry(1420,250,400,330)
        self.hours_list.setStyleSheet("Background:rgba(112, 108, 108,190);font-size:25px;padding-left:40px;padding-top:10px;")
        #self.hours_list.setCursor(QCursor(Qt.PointingHandCursor)
        shadow_effect(self.hours_list,20,8,8,QColor(217, 212, 212))
        '''self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setStyleSheet("background-color: #1f618d ; height: 2px;")
        #self.line.setFixedWidth(450)
        self.setGeometry(10,10,450,10)'''

        self.titre_day.setGeometry(200,550,400,100)
        self.titre_day.setStyleSheet("color:white;font-size:50px;font-family:Times New Roman;")
        shadow_effect(self.titre_day,8,5,5,QColor(0, 0, 0, 180))
        self.titre_hour.setGeometry(1400,150,400,100)
        self.titre_hour.setStyleSheet("color:white;font-size:40px;font-family:Times New Roman;")
        shadow_effect(self.titre_hour,8,5,5,QColor(0, 0, 0, 180))

        #   CREATION WIDGET FOR WEEKS DAY
        self.widgetDay1=self.create_WeeksDay(self.day1_Text,self.day1_Icon,self.day1_temp)
        self.widgetDay2=self.create_WeeksDay(self.day2_Text,self.day2_Icon,self.day2_temp)
        self.widgetDay3=self.create_WeeksDay(self.day3_Text,self.day3_Icon,self.day3_temp)
        self.widgetDay4=self.create_WeeksDay(self.day4_Text,self.day4_Icon,self.day4_temp)
        self.widgetDay5=self.create_WeeksDay(self.day5_Text,self.day5_Icon,self.day5_temp)
        self.widgetDay6=self.create_WeeksDay(self.day6_Text,self.day6_Icon,self.day6_temp)
        self.widgetDay7=self.create_WeeksDay(self.day7_Text,self.day7_Icon,self.day7_temp)
        
        self.widgetDay1.hide()
        self.widgetDay2.hide()
        self.widgetDay3.hide()
        self.widgetDay4.hide()
        self.widgetDay5.hide()
        self.widgetDay6.hide()
        self.widgetDay7.hide()
        #   STYLSHEET WEEKS DAY
        self.style_WeeksDay(self.widgetDay1,180,195)
        self.style_WeeksDay(self.widgetDay2,180,195)
        self.style_WeeksDay(self.widgetDay3,180,195)
        self.style_WeeksDay(self.widgetDay4,180,195)
        self.style_WeeksDay(self.widgetDay5,180,195)
        self.style_WeeksDay(self.widgetDay6,180,195)
        self.style_WeeksDay(self.widgetDay7,180,195)
       
         #------------POSITION WEEKS DAY ----------------------#
        self.widgetDay1.move(260,650)
        self.widgetDay2.move(460,650)
        self.widgetDay3.move(660,650)
        self.widgetDay4.move(860,650)
        self.widgetDay5.move(1060,650)
        self.widgetDay6.move(1260,650)
        self.widgetDay7.move(1460,650)

    

    def searchbar(self):
        query=self.line_edit.text().strip()
        params = {"q": query, "limit": 5, "appid": self.Api_Key}
        reponse = requests.get(self.base_url_CityEntered, params=params)
        if reponse.status_code == 200:
            self.citySearchedList.clear()
            cities=reponse.json()
            i=0
            for city in cities:
                if i==5:
                    break
                self.citySearchedList.addItem(f"◉  {city['name']}, {city['country']}")
                i+=1
            self.citySearchedList.show()
    
    def selectItem(self,item):
        self.line_edit.setText(item.text()[2:])
        self.citySearchedList.hide()
        self.citySearchedList.clear()

    def setup_Page1(self):
        self.hide_elm_Page2()
        self.show_elm_Page1()
        self.citySearchedList.move(250,160)
        styleListCity("black","white",self.citySearchedList)
        self.line_edit.setStyleSheet("padding-left:60px;padding-right:80px; font-size:35px;font-weight:bold; font-family:Times New Roman; border-radius:35px;background:black;color: white;")
        self.body_box.setGeometry(170,40,1600,850)
        self.setStyleSheet("""
                           QPushButton{
                           font-size:40px;
                           border-radius:35px;
                           padding: 10px 20px;
                           color:White;
                           font-family:Times New Roman;
                           background:hsl(198, 76.30%, 29.80%);
                           font-weight:bold;
                           }
                           QPushButton:hover{
                           background:hsl(198, 54.40%, 66.50%);
                           }
                           
                           """)
        self.widgetDay1.hide()
        self.widgetDay2.hide()
        self.widgetDay3.hide()
        self.widgetDay4.hide()
        self.widgetDay5.hide()
        self.widgetDay6.hide()
        self.widgetDay7.hide()
        self.click_button()
    
    def click_buttonPaga2(self):
        self.converterPage2.show()
        self.city=self.line_edit.text()
        self.setup_page_2()
    
    def click_buttonPaga1(self):
        self.city=self.line_edit.text()
        self.click_button()
        
    def click_button(self):
        self.citySearchedList.hide()
        api=os.getenv("OPENCAGE_API_KEY")
        complete_url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.Api_Key}&units=metric"  # metric for Celsius temperature
        location_url = f"https://api.opencagedata.com/geocode/v1/json?q={self.city}+&key={api}"
        # Send the request to the API
        response = requests.get(complete_url)
        repLocation=requests.get(location_url)
        dataLocation=repLocation.json()
        if response.status_code==200:
            self.location_icon.show()
            self.converterPage1.show()
            self.Calendar_icon.show()
            self.CurentWeather.show()
            data=response.json()
            self.main = data['main']
            weather = data['weather'][0]
            self.desc=weather["description"].title()
            weather_id=weather["id"]
            icon_path=get_icone(weather_id)
            self.humidityValeur.setText(f"{self.main['humidity']}  %")
            self.pressureValeur.setText(f"{self.main['pressure']}  hpa")
            self.VisibilityValeur.setText(f"{data['visibility'] * 10**(-3)} Km")
            self.WindValeur.setText(f"{data['wind']['speed'] * 3.6:.2f} Km/h")
            timezone_offset = data['timezone']  # Temps en secondes (décalage UTC)
            
            # Récupérer l'heure UTC actuelle
            utc_now = datetime.now(timezone.utc) #datetime.utcnow() 
            # Appliquer le décalage horaire
            city_time = utc_now + timedelta(seconds=timezone_offset)
            sunset_timestamp =data['sys']['sunset']
            sunset_time = datetime.fromtimestamp(sunset_timestamp, tz=timezone.utc)
            self.sunsetValeur.setText(sunset_time.strftime("%H:%m"))
            sunsrise_timestamp =data['sys']['sunrise']
            sunrise_time = datetime.fromtimestamp(sunsrise_timestamp, tz=timezone.utc)
            self.sunriseValeur.setText(sunrise_time.strftime("%H:%m"))
            self.day.setText(f"{city_time.strftime("%A, %b %d %H:%M")}")#{city_time.strftime("%A, %b %d %H:%M")}
            if dataLocation['results']:
                location_data = dataLocation['results'][0]
                region =f", {location_data['components'].get('region','Inknown')}"
            self.location.setText(f"{data['sys']['country']}/ {self.city.capitalize()}{region.capitalize()}")
            # Charger l'image dans QLabel
            pixmap = QPixmap(icon_path)
            self.icone.setPixmap(pixmap)
            
            self.temperature=self.main["temp"]
            self.temp.setText(f"{self.temperature:.2f}°C")
            self.temp.setStyleSheet("font-size:150px;font-family: Times New Roman;font-weight:bold;color:White;")
            self.LowtHightemp.setText(f"LOW {self.main['temp_min']:.2f}°C | HIGH {self.main['temp_max']:.2f}°C")
            
            self.description.setText(f"{self.desc} | FEELS LIKE {self.main["feels_like"]:.2f}°C")
        elif self.city=="":
            self.CurentWeather.hide()
            self.Calendar_icon.hide()
            self.location_icon.hide()
            self.converterPage1.hide() 
        else:
            self.converterPage1.hide()
            self.cityTime.hide()
            self.LowtHightemp.hide()
            self.location_icon.hide()
            #self.day_icon.hide()
            self.sunsetValeur.setText("")
            self.sunriseValeur.setText("")
            self.WindValeur.setText("")
            self.humidityValeur.setText("")
            self.pressureValeur.setText("")
            self.VisibilityValeur.setText("")
            self.location.setText("")
            self.day.setText("")
            self.temp.setStyleSheet("font-size:100px;font-family: Times New Roman;font-weight:bold;color:White;")
            self.temp.setText("Not Found")
            pixmap=QPixmap("images/sad_nuage.png")
            self.icone.setPixmap(pixmap)
            self.description.setText("No description")

    def setup_page_2(self):
        self.citySearchedList.move(250,180)
        styleListCity("hsl(0, 7%, 82%)","hsl( 184, 5%, 40% )",self.citySearchedList)
        self.citySearchedList.hide()
        self.show_elm_Page2()
        self.hide_elm_Page1()
        self.body_box.setGeometry(70,40,1800,900)
        self.line_edit.setStyleSheet("padding-left:30px;padding-right:80px; font-size:35px;font-weight:bold; font-family:Times New Roman; border-radius:35px;background:white;")
        self.setStyleSheet("""
                            QPushButton{
                            border-radius:25px;
                            background-color: transparent;
                            }
                        """)
        rep=0
        if self.city :
            self.converterPage2.show()
            complete_url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.Api_Key}&units=metric"  # metric for Celsius temperature
            reponse1=requests.get(complete_url)
            if reponse1 .status_code == 200:
                data=reponse1.json()
                longitude=data['coord']['lon']
                latitude=data['coord']['lat']
                timezone_offset = data['timezone']  # Temps en secondes (décalage UTC)
                # Récupérer l'heure UTC actuelle
                utc_now = datetime.now(timezone.utc) #datetime.utcnow() 
                # Appliquer le décalage horaire
                city_time = utc_now + timedelta(seconds=timezone_offset)
                self.main = data['main']
                self.temperature2=self.main["temp"]
                country=data['sys']['country']
                self.date.setText(f"{city_time.strftime("%a, %B %d %H:%M")}")
                self.Country.setText(f"{country}")
                self.temp_page2.setText(f"{self.temperature2}°C")

                url=f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,weathercode&daily=temperature_2m_max,temperature_2m_min,weather_code,relative_humidity_2m_max,relative_humidity_2m_min"
                reponse2=requests.get(url)
                data2 =reponse2.json()
                rep=reponse2.status_code
            if rep==200:
                start_index = None
                for i, time_str in enumerate(data2['hourly']['time']):
                    time_obj = datetime.strptime(time_str, "%Y-%m-%dT%H:%M")
                    if time_obj.hour == city_time.hour:
                        start_index = i
                        break
                if start_index is not None:
                    for i in range(start_index, start_index + 20):  # Get next 10 hours
                        time_str = data2['hourly']['time'][i]
                        temp = data2['hourly']['temperature_2m'][i]
                        icon_code=data2['hourly']['weathercode'][i]
                        time_obj = datetime.strptime(time_str, "%Y-%m-%dT%H:%M")
                        time = time_obj.strftime("%H:%M")  # Correct format
                        tempF= (temp * 9/5) + 32
                        self.hours_list.addItem(f"{time:<4}  {get_iconWeeks(icon_code):<4} {temp}°C-{tempF:.2f}°F")
                        # Ajouter une ligne blue sous chaque prévision
                        add_separator_to_list(self.hours_list)
                        
                dates=data2['daily']['time']
                for i in range(7):
                    self.temp_max=data2['daily']['temperature_2m_max'][i]
                    self.temp_min=data2['daily']['temperature_2m_min'][i]
                    self.humidity_min=data2['daily']['relative_humidity_2m_min'][i]
                    self.humidity_max=data2['daily']['relative_humidity_2m_max'][i]
                    icon_code=data2['daily']['weather_code'][i]
                    time_obj=datetime.strptime(dates[i],"%Y-%m-%d")
                    day_name=time_obj.strftime("%A")
                   
                    # Dynamically create the labels for each day (e.g., day1_Text, day1_Icon, day1_temp, etc.)
                    day_text = getattr(self, f"day{i+1}_Text")
                    day_icon = getattr(self, f"day{i+1}_Icon")
                    day_temp = getattr(self, f"day{i+1}_temp")
                    # Set the text and icon for each day
                    day_text.setText(day_name)
                    day_icon.setText(get_iconWeeks(icon_code))
                    day_temp.setText(f"{self.temp_min}°C / {self.temp_max}°C\n💧 {self.humidity_min}% / {self.humidity_max}%")
     
    def convert_temperaturePage1(self):
        chose=self.converterPage1.currentText()
        if chose=="°F":
            temp= (self.temperature * 9/5) + 32  # Celsius to Fahrenheit formula
            self.temp.setText(f"{temp:.2f}°F")
            temp=self.main["feels_like"]*9/5 + 32
            self.description.setText(f"{self.desc} | FEELS LIKE {temp:.2F}°F")
            tempLow=self.main['temp_min']*9/5 + 32
            temphigh=self.main['temp_max']*9/5 + 32
            self.LowtHightemp.setText(f"LOW {tempLow:.2f}°F | HIGH {temphigh:.2f}°F") 
        else:
            self.temp.setText(f"{str(self.temperature)}°C")
            self.description.setText(f"{self.desc} | FEELS LIKE {self.main["feels_like"]}°C")
            self.LowtHightemp.setText(f"LOW {self.main['temp_min']:.2f}°C | HIGH {self.main['temp_max']:.2f}°C")
            

    def convert_temperaturePage2(self):
        chose=self.converterPage2.currentText()
        if chose=="°F":
            if self.temperature2:
                temp= (self.temperature2 * 9/5) + 32  # Celsius to Fahrenheit formula
                self.temp_page2.setText(f"{temp:.2f}°F")
                for i in range(7):
                    day_temp = getattr(self, f"day{i+1}_temp")
                    tempmin=(self.temp_min * 9/5) + 32 
                    tempmax=(self.temp_max * 9/5) + 32 
                    # Set the text and icon for each day
                    day_temp.setText(f"{tempmin:.2f}°F / {tempmax:.2f}°F\n💧 {self.humidity_min}% / {self.humidity_max}%")
                                            
        else:
            if self.temperature2:
                self.temp_page2.setText(f"{self.temperature2}°C")
                for i in range(7):
                    day_temp = getattr(self, f"day{i+1}_temp")
                    day_temp.setText(f"{self.temp_min}°C / {self.temp_max}°C\n💧 {self.humidity_min}% / {self.humidity_max}%")
                    
         
    def ButtonPageToPage(self,button_name,icon_button,x):
        button_name.setIcon(QIcon(icon_button))  # Set the icon of the button
        button_name.setIconSize(QSize(80, 80))  # Set a fixed size for the icon (adjust as needed)
        button_name.setGeometry(x, 850, 80, 80)  # Set the button's position and size
        button_name.setStyleSheet("""
                                         border-radius:25px;
                                         background-color: transparent;
                                         
                                         """)  # Apply the border radius and make background transparent
                            
        button_name.installEventFilter(self)
    def eventFilter(self, obj, event):
        if isinstance(obj, QPushButton):  # Ensure obj is a button
            if event.type() == QEvent.Enter:
                obj.setIconSize(QSize(70, 70))  # Reduce icon size
                obj.setGeometry(obj.x()+ 7, obj.y() , 70, 70)  # Adjust position
                return True
            elif event.type() == QEvent.Leave:
                obj.setIconSize(QSize(80, 80))  # Restore icon size
                obj.setGeometry(obj.x()-7, obj.y() , 80, 80)  # Reset position
                return True
        return super().eventFilter(obj, event)  # Call default event handler
        #self.toPage_2_button.setGeometry(1750, 830, 150, 150) 
        
        

    def create_Widget(self,icone_label,icone_path,Label,Valeur):
        icone=QPixmap(icone_path)
        icone = icone.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio)
        icone_label.setPixmap(icone)
        #icone_label.setScaledContents(True)
        icone_label.setFixedSize(130,60)
        icone_label.setAlignment(Qt.AlignCenter)
        Label.setAlignment(Qt.AlignCenter)
        shadow_effect(Label,8,2,2,QColor(128, 124, 124,80))
        Valeur.setAlignment(Qt.AlignCenter)
        widget=QWidget(self)
        vbox=QVBoxLayout()
        vbox.addWidget(icone_label)
        vbox.addWidget(Label)
        vbox.addWidget(Valeur)
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        #widget.setFixedSize(100,100)
        widget.setLayout(vbox)
        return widget
    
    def create_WeeksDay(self,Label,icone_label,Valeur):
         #icone_label.setScaledContents(True)
        icone_label.setFixedSize(180,60)
        icone_label.setAlignment(Qt.AlignCenter)
        icone_label.setStyleSheet("font-size:50px;")
        Label.setAlignment(Qt.AlignCenter)
        
        Label.setFixedSize(180,50)
        Label.setStyleSheet("font-size:30px;padding-top:15px;")
        Valeur.setAlignment(Qt.AlignCenter)
        Valeur.setStyleSheet("font-size:20px;")
       
        #Label.setFixedSize(400,100)
        widget=QWidget(self)
        vbox=QVBoxLayout()
        vbox.addWidget(Label)
        vbox.addWidget(icone_label)
        vbox.addWidget(Valeur)
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        #widget.setFixedSize(100,100)
        widget.setLayout(vbox)
        return widget

    def style_widget(self,Widget,x,y):
        Widget.setFixedSize(x,y)
        #this applied for the widget itself
        Widget.setStyleSheet("""
                         QWidget {
                             color:white;
                             font-family:Times New Roman;
                             background:rgba(112, 108, 108,0.5);
                             font-size:21px;
                             font-weight:bold;
                             

                         }
                           QWidget:hover{
                             background:rgba(112, 108, 108,0.2);
                             }  
                         """)
        # Create a shadow effect
        shadow_effect(Widget,20,10,10,QColor(209, 205, 205))

    def style_WeeksDay(self,Widget,x,y):
        Widget.setFixedSize(x,y)
        #this applied on the vboxes inside 
        Widget.setStyleSheet("""
                            QWidget{
                             color:white;
                             font-family:Times New Roman;
                             background:rgba(112, 108, 108,0.8);
                             font-size:20px;
                             font-weight:bold;
                             border-radius:10px;
                             }
                             QWidget:hover{
                             background:rgba(112, 108, 108,0.2);
                             }
                             
                              """)   
  
        
        # Create a shadow effect
        shadow_effect(Widget,20,8,8,QColor(0,0,0))
    
    
    
    def hide_elm_Page2(self):
        self.linesearch_Cadre.hide()
        self.buttonSearch.hide()
        self.temp_page2.hide()
        self.hours_list.hide()
        self.date.hide()
        self.Country.hide()
        self.locationIcon.hide()
        self.toPage_1_button.hide()
        self.titre_day.hide()
        self.titre_hour.hide()
        self.converterPage2.hide()
        self.day1_Icon.hide()
        self.day1_Text.hide()
        self.day1_temp.hide()
        self.day2_Icon.hide()
        self.day2_Text.hide()
        self.day2_temp.hide()
        self.day3_Icon.hide()
        self.day3_Text.hide()
        self.day3_temp.hide()
        self.day4_Icon.hide()
        self.day4_Text.hide()
        self.day4_temp.hide()
        self.day5_Icon.hide()
        self.day5_Text.hide()
        self.day5_temp.hide()
        self.day6_Icon.hide()
        self.day6_Text.hide()
        self.day6_temp.hide()
        self.day7_Icon.hide()
        self.day7_Text.hide()
        self.day7_temp.hide()

    def show_elm_Page2(self):
        self.linesearch_Cadre.show()
        self.buttonSearch.show()
        self.hours_list.show()
        self.date.show()
        self.Country.show()
        self.locationIcon.show()
        self.temp_page2.show()
        self.widgetDay1.show()
        self.widgetDay2.show()
        self.widgetDay3.show()
        self.widgetDay4.show()
        self.widgetDay5.show()
        self.widgetDay6.show()
        self.widgetDay7.show()
        self.toPage_1_button.show()
        self.titre_day.show()
        self.titre_hour.show()
        self.day1_Icon.show()
        self.day1_Text.show()
        self.day1_temp.show()
        self.day2_Icon.show()
        self.day2_Text.show()
        self.day2_temp.show()
        self.day3_Icon.show()
        self.day3_Text.show()
        self.day3_temp.show()
        self.day4_Icon.show()
        self.day4_Text.show()
        self.day4_temp.show()
        self.day5_Icon.show()
        self.day5_Text.show()
        self.day5_temp.show()
        self.day6_Icon.show()
        self.day6_Text.show()
        self.day6_temp.show()
        self.day7_Icon.show()
        self.day7_Text.show()
        self.day7_temp.show()
        
    def hide_elm_Page1(self):
        self.buttom.hide()
        self.icone.hide()
        self.temp.hide()
        self.LowtHightemp.hide()
        self.description.hide()
        self.cityTime.hide()
        self.day.hide()
        self.converterPage1.hide()
        self.location.hide()
        self.location_icon.hide()
        self.Calendar_icon.hide()
        self.CurentWeather.hide()
        self.searchicon.hide()
        #self.converter.hide()
        self.toPage_2_button.hide()
        
        #humidity BOX
        self.humidityIcon.hide()
        self.humidityValeur.hide()
        self.humidityLabel.hide()
        
        # pressure BOX
        self.pressureIcon.hide()
        self.pressureLabel.hide()
        self.pressureValeur.hide()
        
        # Visibility BOX
        self.VisibilityIcon.hide()
        self.VisibilityLabel.hide()
        self.VisibilityValeur.hide()
        
        # Wind  BOX
        self.WindIcon.hide()
        self.WindLabel.hide()
        self.WindValeur.hide()
        # sunsit surise BOX
        self.sunriseIcon.hide()
        self.sunriseLabel.hide()
        self.sunriseValeur.hide()
        # sunsit surise BOX
        self.sunsetIcon.hide()
        self.sunsetLabel.hide()
        self.sunsetValeur.hide()
        self.widget1.hide()
        self.widget2.hide()
        self.widget3.hide()
        self.widget4.hide()
        self.widget5.hide()
        self.widget6.hide()
        
    def show_elm_Page1(self):
        self.buttom.show()
        self.icone.show()
        self.temp.show()
        self.LowtHightemp.show()
        self.description.show()
        self.cityTime.show()
        self.day.show()
        self.Calendar_icon.show()
        self.CurentWeather.show()
        self.location.show()
        self.location_icon.show()
        self.converterPage1.show()
        self.searchicon.show()
        self.toPage_2_button.show()
        
        #humidity BOX
        self.humidityIcon.show()
        self.humidityValeur.show()
        self.humidityLabel.show()
        

        # pressure BOX
        self.pressureIcon.show()
        self.pressureLabel.show()
        self.pressureValeur.show()
        
        # Visibility BOX
        self.VisibilityIcon.show()
        self.VisibilityLabel.show()
        self.VisibilityValeur.show()
        
        # Wind  BOX
        self.WindIcon.show()
        self.WindLabel.show()
        self.WindValeur.show()

        # sunsit surise BOX
        self.sunriseIcon.show()
        self.sunriseLabel.show()
        self.sunriseValeur.show()
        # sunsit surise BOX
        self.sunsetIcon.show()
        self.sunsetLabel.show()
        self.sunsetValeur.show()
        self.widget1.show()
        self.widget2.show()
        self.widget3.show()
        self.widget4.show()
        self.widget5.show()
        self.widget6.show()


####### main function #######
        
app=QApplication(sys.argv)
window=MainWindow()
window.show()
sys.exit(app.exec_())


