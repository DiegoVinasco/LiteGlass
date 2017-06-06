from main import *
import argparse


# Parse args
parser = argparse.ArgumentParser(description="An app for displaying locale and weather information.")
parser.add_argument("-w", "--windowed", action="store_true", help="Start in windowed mode")
parser.add_argument("-v", "--verbose", action="store_true", help="Increase information output")
parser.add_argument("-d", "--dark", action="store_true", help="Start in dark theme")
parser.add_argument("--unit", type=str, default="Metric",
	help="Set the temperature unit (Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit)")
parser.add_argument("--city", type=str, default="Minneapolis",
	help="Set the city, eg: Minneapolis, Paris, Bogota")
parser.add_argument("--country", type=str, default="US", help="Set the country, eg: US, France, Colombia")
args = parser.parse_args()

print "Windowed: "   + str(args.windowed)
print "Verbose: "    + str(args.verbose)
print "Dark: "       + str(args.dark)
print "Unit: "       + str(args.unit)
print "City: "       + str(args.city)
print "Country: "    + str(args.country)


# Initialize root
root = Tk()
root.configure(background="black")
root.attributes('-fullscreen', not args.windowed)


# Set keybindings
def exit ( event ):
   print "EXIT EVENT"
   root.quit()

def update ( event ):
   print "UPDATE EVENT"
   app.updateWeather()
   app.updateTime()

def switch ( event ):
	print "SWITCH EVENT"
	app.dark = not app.dark

root.bind("<Escape>", exit)
root.bind("<Return>", update)
root.bind("<space>", switch)


# Initialize application
root.focus_set()
app = App(root, args.verbose, args.dark, args.unit, args.city, args.country)
root.mainloop()
root.destroy()
