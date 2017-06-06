from Tkinter  import *
from datetime import datetime
from urllib2  import Request, urlopen, URLError
from PIL      import Image, ImageTk
import json, time, sched


class App:

   def __init__( self, root, verbose=False, dark=False, unit="metric", city="Minneapolis", country="us",
      update_interval=14400000 ): # update_interval default is 4 hours
      print "initializing..."

      self.verbose         = verbose
      self.dark            = dark
      self.unit            = unit
      self.city            = city
      self.country         = country
      self.update_interval = update_interval

      self.ui = Frame(root, height=256, bg="black")
      self.ui.pack(fill=X)

      self.drawing = Canvas(self.ui, width=256, height=256, bg="black", highlightthickness=0)
      self.drawing.pack(side=LEFT, padx=(24, 24))

      self.weather_info = Text(self.ui, width=64, height=2, bg="black", fg="white", relief="flat",
         highlightthickness=0)
      self.weather_info.tag_configure("temperature", font=("Helvetica", 72))
      self.weather_info.tag_configure("description", font=("Helvetica", 36))
      self.weather_info.pack(side=LEFT, fill=Y, pady=(32, 0))

      self.locale_info = Text(self.ui, width=128, height=2, bg="black", fg="white", relief="flat",
         highlightthickness=0)
      self.locale_info.tag_configure("time", font=("Helvetica", 72), justify="right")
      self.locale_info.tag_configure("date", font=("Helvetica", 36), justify="right")
      self.locale_info.pack(side=RIGHT, fill=Y, padx=(0, 50), pady=(34, 0))

      self.updateWeather()
      self.updateTime()

      print "initialized!\n"


   def updateWeather( self ):
      """update, format, and display information"""
      print "updating weather..."

      weather = self.getWeather()

      self.weather_info.delete(1.0, END)
      self.weather_info.insert(INSERT, str(weather['main']['temp']) + unichr(176) + "C" + "\n")
      self.weather_info.insert(INSERT, weather['weather'][0]['main'])
      self.weather_info.tag_add("temperature", 1.0, "1.end")
      self.weather_info.tag_add("description", 2.0, "2.end")

      self.updateIcon(str(weather['weather'][0]['icon']))

      self.ui.after(self.update_interval, self.updateWeather)
      print "updated weather!"


   def getWeather ( self, apikey="8e159274ff1876f6196852067e95e5e9" ):
      """request weather from openweathermap"""
      print "fetching weather..."

      url = 'http://api.openweathermap.org/data/2.5/weather?q={},{}&units={}&appid={}'.format(
         self.country, self.city, self.unit, apikey)
      if self.verbose:
         print url
      request = Request(url)

      try:
         response = urlopen(request)
         raw_weather = response.read()
      except URLError, e:
         print 'Well shit... error code:', e
         return None

      weather = json.loads(raw_weather)

      if self.verbose:
         print "package:\n" + str(weather) 

      print "fetched weather!"
      return weather


   def updateIcon( self, icon ):
      """find and display icon"""
      print "updating icon..."

      path = "/home/diego/Documents/LiteGlass/icons/{}{}.png".format(icon, "_dark" if self.dark else "")

      if self.verbose:
         print path

      self.icon = ImageTk.PhotoImage(file=path)
      self.drawing.create_image(129, 129, image=self.icon)
      self.drawing.pack()

      print "updated icon!"


   def updateTime( self ):
      """update local time"""
      print "updating time..."

      self.locale_info.delete(1.0, END)
      self.locale_info.insert(INSERT, datetime.now().strftime("%H:%M") + "\n")
      self.locale_info.insert(INSERT, datetime.now().strftime("%A, %B %d"))
      self.locale_info.tag_add("time", 1.0, "1.end")
      self.locale_info.tag_add("date", 2.0, "2.end")

      self.ui.after(59999, self.updateTime)
      print "updated time!"