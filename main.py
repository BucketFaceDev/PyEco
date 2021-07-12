"""."""

import time
import random
import threading
import math
from dearpygui.core import *
from dearpygui.simple import *

class Resource:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.priceHistory = []
        self.counter = 0
        self.resources = 1000

    def setPrice(self, price):
        self.counter = self.counter + 1
        self.price = price
        if (math.modf(self.counter/ 5)[0] == 0.0):
            self.priceHistory.append(price)

    def supplyAndDemand(self):
        mineRate = random.randint(50, 70)
        priceDeflation = random.randint(10, 40)
        
        self.resources = self.resources + mineRate
        if (self.price > 1000):
            self.setPrice(self.price - priceDeflation)

        if (self.resources < 1000):
            self.setPrice (self.price + random.randint(40,75))
        if (self.resources > 1000):
            self.setPrice (self.price + random.randint(10, 20))
    
    def buy(self, quantity):
        if (self.resources < quantity):
            return False
        self.resources = self.resources - quantity
        return True

    

# Classes
class Global():
    on = 1
    counterA = 1
    counterB = 1

    mineA = Resource('Mine A', 1000)
    mineB = Resource('Mine B', 1000)
    
    proFactoryResources = 0
    proFactoryBal = 1000
    proResource = 0
    proResourcePrice = 2000
    carFactoryResources = 0
    carFactoryBal = 5000
    waitBetweenUpdatesInSeconds = 1
# Main Program

def buyRawResource():
    if Global.proFactoryBal < 1000:
        log_warning(message="Processing Factory can no longer afford raw material!")
        Global.on = 0
        return
    if (Global.mineA.price <= Global.mineB.price) and Global.mineA.buy(100):
        Global.proFactoryResources = Global.proFactoryResources + 100
        Global.proFactoryBal = Global.proFactoryBal - Global.mineA.price  
    elif (Global.mineB.buy(100)):
        Global.proFactoryResources = Global.proFactoryResources + 100
        Global.proFactoryBal = Global.proFactoryBal - Global.mineB.price
    else:
        log_warning(message="Mines have has run out of resources!")
             

def carBuyRawResource():
    if Global.carFactoryBal >= Global.proResourcePrice:
        if Global.proResource >= 100:
            Global.proResource = Global.proResource - 100
            Global.carFactoryResources = Global.carFactoryResources + 100
            Global.carFactoryBal = Global.carFactoryBal - Global.proResourcePrice

def supplyAndDemand():
    Global.mineA.supplyAndDemand()
    Global.mineB.supplyAndDemand()

def startTheStatCalculator():
    while (Global.on == 1):
        time.sleep(Global.waitBetweenUpdatesInSeconds)

        supplyAndDemand()

        if Global.proFactoryResources < 100:
            buyRawResource()
        else:
            Global.proFactoryResources = Global.proFactoryResources - 100
            Global.proResource = Global.proResource + 50
            Global.proFactoryBal = Global.proFactoryBal + 2000 # temp until more fact/shops added

        if Global.carFactoryResources < 300:
            carBuyRawResource()
        else:
            Global.carFactoryResources = Global.carFactoryResources - 300
            Global.carFactoryBal = Global.carFactoryBal + 10000

            # if (proResource > 4500):
            #     on = 0
            #     print("Resources maxed!")

        print("Processing Factory Raw Material = " + str(Global.proFactoryResources))
        print("Processing Factory Balance = £" + str(Global.proFactoryBal))
        print("Processed Material = " + str(Global.proResource))
        print("\n")
        print("Mine A Raw Material =" + str(Global.mineA.resources))
        print("Mine B Raw Material =" + str(Global.mineB.resources))
        print("Mine A Unit Price = £" + str(Global.mineA.price))
        print("Mine B Unit Price = £" + str(Global.mineA.resources))
        print("\n")

t = threading.Thread(target=startTheStatCalculator, daemon=True)
t.start()

def updatestats(sender, data):

    set_value("Mine A Resources", str(Global.mineA.resources))
    set_value("Mine B Resources", str(Global.mineB.resources))
    set_value("Mine A Price", "£" + str(Global.mineA.price))
    set_value("Mine B Price", "£" + str(Global.mineB.price))
    set_value("Processing Factory Raw", str(Global.proFactoryResources))
    set_value("Processing Factory Bal", str(Global.proFactoryBal))
    set_value("Processed Material", str(Global.proResource))
    set_value("Car Factory Resources", str(Global.carFactoryResources))
    set_value("Car Factory Bal", str(Global.carFactoryBal))

    #if (math.modf(Global.counter/ 500)[0] == 0.0):
    set_value("Mine A Price History", Global.mineA.priceHistory)
    set_value("Mine B Price History", Global.mineB.priceHistory)
    set_value("Processed Material Price", Global.proResourcePrice)
    # Global.waitBetweenUpdatesInSeconds = get_value("Timescale")

# GUI

def primary():

    with window("Home", height=600, width=800):
        
        set_window_pos("Home", 0, 0)

        with tab_bar("TabBar"):

            with tab('XVal', label='Overview'):
                add_text("Current Statistics")

                add_separator

                add_text("Mine A Resources: ")
                add_same_line()
                add_text("Mine A Resources", default_value =str(Global.mineA.resources) + "U")

                add_text("Mine B Resources: ")
                add_same_line()
                add_text("Mine B Resources", default_value=str(Global.mineB.resources)+ "U")

                add_text("Mine A Price: ")
                add_same_line()
                add_text("Mine A Price", default_value=str(Global.mineA.price))


                add_text("Mine B Price: ")
                add_same_line()
                add_text("Mine B Price", default_value=str(Global.mineB.price))
                
                add_text("Processing Factory Raw: ")
                add_same_line()
                add_text("Processing Factory Raw", default_value=str(Global.proFactoryResources))

                add_text("Processing Factory Bal: ")
                add_same_line()
                add_text("Processing Factory Bal", default_value=str(Global.proFactoryBal))

                add_text("Processed Material: ")
                add_same_line()
                add_text("Processed Material", default_value=str(Global.proResource))

                add_text("Processed Material Price: ")
                add_same_line()
                add_text("Processed Material Price")

                add_text("Car Factory Resources: ")
                add_same_line()
                add_text("Car Factory Resources", default_value=str(Global.carFactoryResources) + "U")

                add_text("Car Factory Bal: ")
                add_same_line()
                add_text("Car Factory Bal", default_value=str(Global.carFactoryBal))

                
                add_button("Documentation", callback=show_documentation)

                add_slider_float("Timescale", default_value=1.0, vertical=False, format="%0.1f" ,max_value=2.0, min_value=0.1)
                show_logger()

                # Runs one cycle of the simulation.
                startTheStatCalculator()


            with tab('Yval', label='Graphs'):
                add_text("Mine Price Statistics")
                add_simple_plot("Mine A Price History", value=Global.mineA.priceHistory, height=300, minscale=0, maxscale=3000)
                add_simple_plot("Mine B Price History", value=Global.mineB.priceHistory, height=300, minscale=0, maxscale=3000) 

# GUI init
set_render_callback(updatestats)
start_dearpygui(primary_window="Home")
primary()


