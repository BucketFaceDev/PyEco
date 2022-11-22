"""."""

import time
import random
import threading
import math
import dearpygui.dearpygui as dpg

# Variables
class Global():
    on = 1
    counterA = 1
    counterB = 1
    mineAResources = 1000
    mineBResources = 1000
    mineAPrice = 1000
    def setMineAPrice(valueA):
        Global.counterA = Global.counterA + 1
        Global.mineAPrice = valueA
        if (math.modf(Global.counterA/ 5)[0] == 0.0):
            Global.mineAPriceHistory.append(valueA)
    def setMineBPrice(valueB):
        Global.counterB = Global.counterB + 1
        Global.mineBPrice = valueB
        if (math.modf(Global.counterB/ 5)[0] == 0.0):
            Global.mineBPriceHistory.append(valueB)

    mineAPriceHistory = []
    mineBPrice = 1000
    mineBPriceHistory = []
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

    if Global.mineAPrice <= Global.mineBPrice:
        if Global.mineAResources >= 100:
            Global.mineAResources = Global.mineAResources - 200
            Global.proFactoryResources = Global.proFactoryResources + 100
            Global.proFactoryBal = Global.proFactoryBal - Global.mineAPrice
    elif Global.mineBPrice <= Global.mineAPrice:
            if Global.mineBResources >= 100:
                Global.mineBResources = Global.mineBResources - 200
                Global.proFactoryResources = Global.proFactoryResources + 100
                Global.proFactoryBal = Global.proFactoryBal - Global.mineBPrice
            else:
                if Global.mineAResources >= 100:
                    Global.mineAResources = Global.mineAResources - 100
                    Global.proFactoryResources = Global.proFactoryResources + 100
                    Global.proFactoryBal = Global.proFactoryBal - Global.mineAPrice
                log_warning(message="Mine B has run out of resources!")

def carBuyRawResource():
    if Global.carFactoryBal >= Global.proResourcePrice:
        if Global.proResource >= 100:
            Global.proResource = Global.proResource - 100
            Global.carFactoryResources = Global.carFactoryResources + 100
            Global.carFactoryBal = Global.carFactoryBal - Global.proResourcePrice

        else:
            log_warning(message="Processing Factory has run out of processed material!")
    else:
        log_error(message="Car Factory can no longer afford processed material!")
        on = 0

def supplyAndDemand():

    mineRate = random.randint(50, 70)
    priceDeflation = random.randint(10, 40)

    Global.mineAResources = Global.mineAResources + mineRate
    Global.mineBResources = Global.mineBResources + mineRate

    if Global.mineAPrice > 1000:
        Global.setMineAPrice(Global.mineAPrice - priceDeflation)

    if Global.mineBPrice > 1000:
        Global.setMineBPrice(Global.mineBPrice - priceDeflation)

    if Global.proResourcePrice > 1000:
        Global.proResourcePrice = Global.proResourcePrice - priceDeflation

#	Mine price per 100U inflation

    if (Global.mineAResources < 1000):
        Global.setMineAPrice (Global.mineAPrice + random.randint(40,75))
    if (Global.mineAResources > 1000):
        Global.setMineAPrice (Global.mineAPrice + random.randint(10, 20))
    
    if (Global.mineBResources < 1000):
        Global.setMineBPrice (Global.mineBPrice + random.randint(40,75))
    if (Global.mineBResources > 1000):
        Global.setMineBPrice (Global.mineBPrice + random.randint(10,20))



def startTheStatCalculator():
    def do_it():
        while (Global.on == 1):

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
            print("Mine A Raw Material =" + str(Global.mineAResources))
            print("Mine B Raw Material =" + str(Global.mineBResources))
            print("Mine A Unit Price = £" + str(Global.mineAPrice))
            print("Mine B Unit Price = £" + str(Global.mineBPrice))
            print("\n")

    t = threading.Thread(target=do_it, daemon=True)
    t.start()

def updatestats(sender, data):

    set_value("Mine A Resources", str(Global.mineAResources))
    set_value("Mine B Resources", str(Global.mineBResources))
    set_value("Mine A Price", "£" + str(Global.mineAPrice))
    set_value("Mine B Price", "£" + str(Global.mineBPrice))
    set_value("Processing Factory Raw", str(Global.proFactoryResources))
    set_value("Processing Factory Bal", str(Global.proFactoryBal))
    set_value("Processed Material", str(Global.proResource))
    set_value("Car Factory Resources", str(Global.carFactoryResources))
    set_value("Car Factory Bal", str(Global.carFactoryBal))

    #if (math.modf(Global.counter/ 500)[0] == 0.0):
    set_value("Mine A Price History", Global.mineAPriceHistory)
    set_value("Mine B Price History", Global.mineBPriceHistory)
    set_value("Processed Material Price", Global.proResourcePrice)
    Global.waitBetweenUpdatesInSeconds = get_value("Timescale")

# GUI

def primary():

    with dpg.window("Home", height=600, width=800):
        
        dpg.set_window_pos("Home", 0, 0)

        with dpg.tab_bar("TabBar"):

            with dpg.tab('XVal', label='Overview'):
                dpg.add_text("Current Statistics")

                dpg.add_separator

                dpg.add_text("Mine A Resources: ")
                dpg.add_same_line()
                dpg.add_text("Mine A Resources", default_value =str(Global.mineAResources) + "U")

                dpg.add_text("Mine B Resources: ")
                dpg.add_same_line()
                dpg.add_text("Mine B Resources", default_value=str(Global.mineBResources)+ "U")

                dpg.add_text("Mine A Price: ")
                dpg.add_same_line()
                dpg.add_text("Mine A Price", default_value=str(Global.mineAPrice))


                dpg.add_text("Mine B Price: ")
                dpg.add_same_line()
                dpg.add_text("Mine B Price", default_value=str(Global.mineBPrice))
                
                dpg.add_text("Processing Factory Raw: ")
                dpg.add_same_line()
                dpg.add_text("Processing Factory Raw", default_value=str(Global.proFactoryResources))

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
                add_simple_plot("Mine A Price History", value=Global.mineAPriceHistory, height=300, minscale=0, maxscale=3000)
                add_simple_plot("Mine B Price History", value=Global.mineBPriceHistory, height=300, minscale=0, maxscale=3000) 

    # GUI init
    set_render_callback(updatestats)
    start_dearpygui(primary_window="Home")
primary()