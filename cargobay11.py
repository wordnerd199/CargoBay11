# Madeline Stevens
# 3.10.2

import tkinter as tk
from tkinter import *
from tkinter import messagebox
import random
import json
import cardgo

def nextDay(event):
    global currentDay
    global listDays
    global totalLat
    if currentDay == 14:
        list(listDays.keys())[currentDay].config(state=DISABLED, bg="yellow")
        buttonOffer.config(state=DISABLED)
        buttonContract.config(state=DISABLED)
        buttonNextDay.config(state=DISABLED)
        offers.delete(0,END)
        contracts.delete(0,END)
        if totalLat < 0:
            messagebox.showinfo("Cargo Bay 11", "Congratulations on a spectacular failure! Enjoy being in debt to the Orion Syndicate for the rest of your life.")
        elif totalLat <= 1000:
            messagebox.showinfo("Cargo Bay 11", "Congratulations on keeping your lobes above water! The point is to make a PROFIT, but you'll get there someday...maybe.")
        else:
            messagebox.showinfo("Cargo Bay 11", "Congratulations on turning a profit! The Grand Nagus would be proud.")
    else:
        if currentDay != -1:
            list(listDays.keys())[currentDay].config(state=DISABLED, bg="yellow")
        currentDay += 1
        list(listDays.keys())[currentDay].config(bg="green")
        offerslist.clear()
        contractslist.clear()
        offers.delete(0,END)
        contracts.delete(0,END)
        forSale = []
        forBuy = []
        for i in range(10):
            offer = cardgo.Offer()
            while offer.cargo in forSale:
                offer = cardgo.Offer()
            forSale.append(offer.cargo)
            offerslist.append(offer)
            offers.insert(END, f"{offer.cargo} | {offer.quantity} {offer.unit} | ₷{offer.total} total")
            contract = cardgo.Contract()
            while contract.cargo in forBuy:
                contract = cardgo.Contract()
            forBuy.append(contract.cargo)
            contractslist.append(contract)
            contracts.insert(END, f"{contract.cargo} | {contract.quantity} {contract.unit} | ₷{contract.total} total | due in {str(contract.dueDate)} days")
        stuff = list(contents.get(0, END))
        for i in range(len(stuff)):
            splitstuff = stuff[i].split(" ")
            thing = splitstuff[0]
            if totalCargo[thing][1] != 16:
                totalCargo[thing][1] -= 1
                if totalCargo[thing][1] == 0:
                    messagebox.showinfo("Cargo Bay 11", f"Your {thing} has expired.")
                    stuff[i] = "NONE"
                    totalCargo[thing][0] = 0
                else:
                    splitstuff[-2] = str(totalCargo[thing][1])
                    stuff[i] = " ".join(splitstuff)
        today = list(listDays.keys())[currentDay]
        if len(listDays[today]) > 0:
            for i in range(len((listDays)[today])):
                activeCon = listDays[today][i]
                if totalCargo[activeCon.cargo][0] >= activeCon.quantity:
                    messagebox.showinfo("Cargo Bay 11", f"You have fulfilled your contract to sell {str(activeCon.quantity)} {activeCon.unit} of {activeCon.cargo}.")
                    totalCargo[activeCon.cargo][0] -= activeCon.quantity
                    for i in range(len(stuff)):
                        splitstuff = stuff[i].split(" ")
                        if splitstuff[0] == activeCon.cargo:
                            if totalCargo[activeCon.cargo][0] == 0:
                                totalCargo[activeCon.cargo][1] == 16
                                stuff[i] = "NONE"
                            else:
                                splitstuff[2] = str(totalCargo[activeCon.cargo][0])
                                stuff[i] = " ".join(splitstuff)
                else:
                    messagebox.showinfo("Cargo Bay 11", f"You do not have enough {activeCon.cargo} to fulfill your contract. The buyer is taking back their ₷{str(activeCon.total)}.")
                    totalLat = round(totalLat - activeCon.total, 2)
                    latinum.config(text=f"₷{str(totalLat)}")
        boom = 0
        cops = 0
        vole = 0
        for i in range(len(stuff)):
            if "VOLATILE" in stuff[i]:
                x = random.randint(0,20)
                if x == 1:
                    boom += 1
            if "ILLEGAL" in stuff[i]:
                x = random.randint(0,20)
                if x == 1:
                    cops += 1
            if "Cardassian_voles" in stuff[i]:
                for i in range(totalCargo["Cardassian_voles"][0]):
                    x = random.randint(0,40)
                    if x == 1:
                        vole += 1
        if boom > 0:
            messagebox.showinfo("Cargo Bay 11", "Your volatile cargo exploded, setting off a chain reaction that destroyed the entire cargo bay and everything in it, including your gold-pressed latinum.")
            for i in range(len(stuff)):
                stuff[i] == "NONE"
            totalLat = 0.00
            latinum.config(text=f"₷{str(totalLat)}")
            for k, v in totalCargo.items():
                totalCargo[k][0] = 0
        elif cops > 0:
            messagebox.showinfo("Cargo Bay 11", "Odo, the station's head of security, performed a surprise inspection and confiscated all your illegal goods.")
            for i in range(len(stuff)):
                if "ILLEGAL" in stuff[i]:
                    splitstuff = stuff[i].split(" ")
                    thing = splitstuff[0]
                    totalCargo[thing][0] = 0
                    stuff[i] = "NONE"
        elif vole > 0:
            messagebox.showinfo("Cargo Bay 11", "Your Cardassian_voles escaped and ate all your perishable cargo.")
            for i in range(len(stuff)):
                if "expires" in stuff[i]:
                    splitstuff = stuff[i].split(" ")
                    thing = splitstuff[0]
                    totalCargo[thing][0] = 0
                    totalCargo[thing][1] = 16
                    stuff[i] = "NONE"
        contents.delete(0,END)
        for i in range(len(stuff)):
            if stuff[i] != "NONE":
                contents.insert(END, stuff[i]) 

def acceptOffer(event):
    global totalLat
    global totalCargo
    if len(offers.curselection()) > 0:
        selOffer = offerslist[offers.curselection()[0]]
        if selOffer.total > totalLat:
            messagebox.showerror("Cargo Bay 11", "You don't have enough latinum to make this purchase.")
        else:
            totalLat = round(totalLat - selOffer.total, 2)
            warning = ""
            if selOffer.is_perishable == 1:
                warning = warning + (f" | expires in {str(selOffer.expDate)} days")
                totalCargo[selOffer.cargo][1] = selOffer.expDate
            if selOffer.is_illegal == 1:
                warning = warning + (" | ILLEGAL")
            if selOffer.is_volatile == 1:
                warning = warning + (" | VOLATILE")
            latinum.config(text=f"₷{str(totalLat)}")
            if totalCargo[selOffer.cargo][0] == 0:
                totalCargo[selOffer.cargo][0] += selOffer.quantity
                contents.insert(END, f"{selOffer.cargo} | {selOffer.quantity} {selOffer.unit}{warning}")
            else:
                totalCargo[selOffer.cargo][0] += selOffer.quantity
                stuff = list(contents.get(0, END))
                for i in range(len(stuff)):
                    if selOffer.cargo in stuff[i]:
                        stuffText = stuff[i].split(" ")
                        stuffText[2] = str(totalCargo[selOffer.cargo][0])
                        stuffText = " ".join(stuffText)
                        stuff[i] = stuffText
                contents.delete(0,END)
                for i in range(len(stuff)):
                    contents.insert(END, stuff[i])
            offers.delete(offers.curselection()[0])
            offerslist.remove(selOffer)
    else:
        messagebox.showerror("Cargo Bay 11", "No offer has been selected.")
    
def acceptContract(event):
    global totalLat
    if len(contracts.curselection()) > 0:
        selContract = contractslist[contracts.curselection()[0]]
        totalLat = round(totalLat + selContract.total, 2)
        latinum.config(text=f"₷{str(totalLat)}")
        contracts.delete(contracts.curselection()[0])
        contractslist.remove(selContract)
        dayDue = currentDay + selContract.dueDate
        selContract.accept(currentDay)
        if dayDue < 15:
            actualDayDue = list(listDays.keys())[dayDue]
            actualDayDue.config(bg="red")
            listDays[actualDayDue].append(selContract)
    else:
        messagebox.showerror("Cargo Bay 11", "No contract has been selected.")

def contractSelect(event):
    global contractslist
    selContract = contractslist[contracts.curselection()[0]]
    labelContract.config(text=str(selContract))
    
def offerSelect(event):
    global offerslist
    selOffer = offerslist[offers.curselection()[0]]
    labelOffer.config(text=str(selOffer))

def showWarning(actualDay):
    if actualDay.cget("bg") == "red":
        dueContracts = listDays[actualDay]
        for i in range(len(dueContracts)):
            info = listDays[actualDay][i].relative(currentDay)
            messagebox.showinfo("Cargo Bay 11", info)

def saveGame():
    nameWindow = tk.Toplevel(main)
    nameWindow.geometry("250x75")
    nameLabel = tk.Label(nameWindow, text="Enter a name to save this game as:")
    nameLabel.pack()
    nameEntry = tk.Entry(nameWindow)
    nameEntry.pack()
    saveButton = tk.Button(nameWindow, text="Save game", command=lambda: makeFile(nameWindow, nameEntry.get()))
    saveButton.pack()

def makeFile(window, filename):
    global totalCargo
    global offerslist
    global contractslist
    global totalLat
    global listDays
    global currentDay
    window.destroy()
    offers = [i.tuplify() for i in offerslist]
    contracts = [i.tuplify() for i in contractslist]
    dayValues = list(listDays.values())
    dayValuesJson = []
    for i in range(len(dayValues)):
        new = [x.tuplify() for x in dayValues[i]]
        dayValuesJson.append(new)
    jsonData = json.dumps([totalCargo, offers, contracts, dayValuesJson, totalLat, currentDay])
    with open(filename, "w") as file:
        file.write(jsonData)

def openGame():
    nameWindow = tk.Toplevel(main)
    nameWindow.geometry("250x75")
    nameLabel = tk.Label(nameWindow, text="Enter a file name to open:")
    nameLabel.pack()
    nameEntry = tk.Entry(nameWindow)
    nameEntry.pack()
    saveButton = tk.Button(nameWindow, text="Open file", command=lambda: openFile(nameWindow, nameEntry.get()))
    saveButton.pack()

def openFile(window, filename):
    global currentDay
    global totalCargo
    global totalLat
    global listDays
    # I can't directly convert the Contract/Offer items to JSON, so I convert the relevant parameters to a tuple instead when the game is saved. I thought I could create a new Contract/Offer item and then override those parameters with the ones from the save file, but I haven't been able to get that to work yet. It just doesn't do anything and returns nothing--it even seems to delete the item itself?
    # The save/load function is a work in progress. It doesn't yet reload the contents of the cargo bay, the available contracts/offers, or set the accepted contracts in their specified places on the day tracker. It can set the day tracker to the correct day and reset the latinum total to the correct amount, however.
    window.destroy()
    newGame()
    file = open(filename, "r")
    data = json.loads(file.read())
    file.close()
    totalLat = data[4]
    latinum.config(text=f"₷{str(totalLat)}")
    currentDay = data[5]
    list(listDays.keys())[currentDay].config(bg="green")
    dayKeys = list(listDays.keys())
    dayValues = data[3]
    for i in range(len(dayValues)):
        if len(dayValues[i]) > 0:
            dV = dayValues[i]
            dayValues[i].clear()
            for x in range(len(dV)):
                newcontract = cardgo.Contract()
                newcontract.detuplify(dV[x])
                dayValues[i].append(newContract)
            dayKeys[i].config(bg="red")
    for key in dayKeys:
        for value in dayValues:
            listDays[key] = value
            dayValues.remove(value)
            break

def newGame():
    global currentDay
    global totalCargo
    global totalLat
    global listDays
    totalLat = 1000.00
    latinum.config(text=f"₷{str(totalLat)}")
    contents.delete(0,END)
    contracts.delete(0,END)
    offers.delete(0,END)
    currentDay = -1
    daystracker = list(listDays.keys())
    for i in range(len(daystracker)):
        daybutton = daystracker[i]
        daybutton.config(state=NORMAL, bg="yellow")
        listDays[daybutton] = []
    cargolist = list(totalCargo.keys())
    for i in range(len(cargolist)):
        item = cargolist[i]
        totalCargo[item][0] = 0
        totalCargo[item][1] = 16

def quitGame():
    main.destroy()

def gameHelp():
    messagebox.showinfo("Cargo Bay 11 (1/6)", "Welcome to Cargo Bay 11, your responsibility for the next 15 days! Quark is away, taking care of business on Ferenginar, and he's tasked you with running his shipping business while he's gone. All you have to do is keep the latinum flowing in the correct direction so that Quark comes home to a profitable enterprise. What could be simpler?")
    messagebox.showinfo("Cargo Bay 11 (2/6)", "He left you ₷1000.00 and an empty cargo bay to fill. Each day, various vendors on Deep Space 9 will be selling a variety of goods from across the galaxy, each charging a different unit price and selling a different quantity. If you can afford to buy the goods they're selling, you can select the offer and then click on the 'Accept selected offer' button to add those goods to your supply.")
    messagebox.showinfo("Cargo Bay 11 (3/6)", "Before you buy, though, it's worth double-clicking on the offer to see more information about the cargo, because certain goods can be illegal, volatile, and/or perishable. Illegal goods are a perfectly legitimate business strategy, but the nosy station security chief sometimes stops by to inspect and will confiscate any illegal cargo he finds. Volatile cargo can be lucrative, but it has a slight chance to explode and destroy everything around it--handle with care! Perishable goods will have an expiration date--make sure you can sell them before they go bad.")
    messagebox.showinfo("Cargo Bay 11 (4/6)", "One of the more unusual types of cargo that gets trafficked in this region of space is live Cardassian voles (they have to be alive, you see, in order to fight for the amusement of gambling onlookers). Unfortunately, voles are tricky to keep contained, and if they get out, they'll eat all your other perishable cargo and be impossible to catch again. Move the voles quickly!")
    messagebox.showinfo("Cargo Bay 11 (5/6)", "But buying is only one part of commerce--the other is selling! Each day, you will be contacted by a handful of Quark's regular customers, who will be interested in purchasing a specific quantity of an item for a set price at a future date. If you select their contract and click 'Accept selected contract,' they'll give you the latinum now (because they have such faith in Quark's ability to deliver), on the condition that you provide the goods on the due date. If you don't have enough of that item on the due date, the buyer will take their latinum back and leave you with the cargo (and possibly in the red).")
    messagebox.showinfo("Cargo Bay 11 (6/6)", "Once you select a contract, the due date will change to red on the day tracker at the bottom of the screen. You can click on red dates to check which contracts are due that day. If there's no more offers or contracts that you want to accept, click the 'Go to next day' button to advance to the next day and see a new set of offers and contracts. If you can make it through 15 days without ending up in debt, you win! If you can't finish the game in one sitting, you can save your game using the File menu (although I haven't finished the 'Open game' function yet, so save at your own risk). Select File > New game to start over, or File > Quit if you're done for now. Good luck!")

offerslist = []
contractslist = []
totalLat = 1000.00
totalCargo = {"kemocite": [0,16, "kilos"], "dilithium": [0,16, "kilos"], "Andarian_glass_beads": [0,16, "grams"], "antimonium": [0,16, "kilos"], "quadrotriticale": [0,16, "bushels"], "Romulan_ale": [0,16, "bottles"], "Tallonian_crystal": [0,16, "grams"], "synthehol": [0,16, "cases"], "Gramilian_sand_peas": [0,16, "kilos"], "maraji_crystal": [0,16, "grams"], "Hupyrian_beetle_snuff": [0,16, "kilos"], "brizeen_nitrate": [0,16, "kilos"], "tulaberry_wine": [0,16, "vats"], "self-sealing_stem_bolts": [0,16, "gross"], "Saurian_brandy": [0,16, "bottles"], "Aldebaran_whiskey": [0,16, "barrels"], "yamok_sauce": [0,16, "wrappages"], "Kohlanese_barley": [0,16, "bushels"], "Gamzian_wine": [0,16, "bottles"], "bloodwine": [0,16, "cases"], "bio-mimetic_gel": [0,16, "milliliters"], "Cardassian_voles": [0,16, "live voles"], "kanar": [0,16, "cases"], "feldomite": [0,16, "kilos"], "Slug-o-Cola": [0,16, "cases"]}

main = tk.Tk()
main.geometry("1200x600")
main.title("Cargo Bay 11")
menuBar = tk.Menu(main)
fileMenu = tk.Menu(menuBar, tearoff=0)
fileMenu.add_command(label="Save game", command=saveGame)
fileMenu.add_command(label="Open game", command=openGame)
fileMenu.add_command(label="New game", command=newGame)
fileMenu.add_command(label="Quit", command=quitGame)
menuBar.add_cascade(label="File", menu=fileMenu)
helpMenu = tk.Menu(menuBar, tearoff=0)
helpMenu.add_command(label="How to play", command=gameHelp)
menuBar.add_cascade(label="Help", menu=helpMenu)
main.config(menu=menuBar)
titleContents = tk.Label(main, text="Contents of Cargo Bay 11", font=("Bauhaus 93", 18))
titleContents.grid(row=0,column=0)
contents = tk.Listbox(main, height=25, width=50)
contents.grid(row=1,column=0, rowspan=5, padx=5)
titleOffers = tk.Label(main, text="Today's offers", font=("Bahnschrift", 14))
titleOffers.grid(row=0,column=1)
offers = tk.Listbox(main, height=10, width=55)
offers.grid(row=1,column=1, padx=5)
offers.bind("<Double-1>", offerSelect)
labelOffer = tk.Label(main, text="Double-click on an \n offer for more information", font=("Bahnschrift",12))
labelOffer.grid(row=2, column=1, rowspan=3)
titleContracts = tk.Label(main, text="Today's contracts", font=("Bahnschrift", 14))
titleContracts.grid(row=0,column=2)
contracts = tk.Listbox(main, height=10, width=55)
contracts.grid(row=1,column=2, padx=5)
contracts.bind("<Double-1>", contractSelect)
labelContract = tk.Label(main, text="Double-click on a contract\nfor more information", font=("Bahnschrift",12))
labelContract.grid(row=2, column=2, rowspan=3)
titleLat = tk.Label(main, text="Total gold-pressed latinum available:", font=("Bahnschrift",12))
titleLat.grid(row=6,column=0)
latinum = tk.Label(main, text=f"₷{str(totalLat)}", font=("Bauhaus 93", 56))
latinum.grid(row=7,column=0)
buttonsFrame = tk.Frame(main)
buttonOffer = tk.Button(buttonsFrame, text="Accept selected offer", font=("Bahnschrift",16))
buttonOffer.grid(row=0,column=0)
buttonOffer.bind("<Button-1>", acceptOffer)
buttonContract = tk.Button(buttonsFrame, text="Accept selected contract", font=("Bahnschrift",16))
buttonContract.grid(row=0,column=1)
buttonContract.bind("<Button-1>", acceptContract)
buttonNextDay = tk.Button(buttonsFrame, text="Go to next day", font=("Bahnschrift",16))
buttonNextDay.grid(row=0,column=2)
buttonNextDay.bind("<Button-1>", nextDay)
buttonsFrame.grid(row=5, column=1, columnspan=2)
dayTrack = tk.Frame(main)
day1 = tk.Button(dayTrack, text="1", font=("Bauhaus 93",18), relief="raised", bg="yellow", command=lambda: showWarning(day1))
day1.grid(row=0,column=0)
day2 = tk.Button(dayTrack, text="2", font=("Bauhaus 93",18), relief="raised", bg="yellow", command=lambda: showWarning(day2))
day2.grid(row=0,column=1)
day3 = tk.Button(dayTrack, text="3", font=("Bauhaus 93",18), relief="raised", bg="yellow", command=lambda: showWarning(day3))
day3.grid(row=0,column=2)
day4 = tk.Button(dayTrack, text="4", font=("Bauhaus 93",18), relief="raised", bg="yellow", command=lambda: showWarning(day4))
day4.grid(row=0,column=3)
day5 = tk.Button(dayTrack, text="5", font=("Bauhaus 93",18), relief="raised", bg="yellow", command=lambda: showWarning(day5))
day5.grid(row=0,column=4)
day6 = tk.Button(dayTrack, text="6", font=("Bauhaus 93",18), relief="raised", bg="yellow", command=lambda: showWarning(day6))
day6.grid(row=0,column=5)
day7 = tk.Button(dayTrack, text="7", font=("Bauhaus 93",18), relief="raised", bg="yellow", command=lambda: showWarning(day7))
day7.grid(row=0,column=6)
day8 = tk.Button(dayTrack, text="8", font=("Bauhaus 93",18), relief="raised", bg="yellow", command=lambda: showWarning(day8))
day8.grid(row=0,column=7)
day9 = tk.Button(dayTrack, text="9", font=("Bauhaus 93",18), relief="raised", bg="yellow", command=lambda: showWarning(day9))
day9.grid(row=0,column=8)
day10 = tk.Button(dayTrack, text="10", font=("Bauhaus 93",18), relief="raised", bg="yellow", command=lambda: showWarning(day10))
day10.grid(row=0,column=9)
day11 = tk.Button(dayTrack, text="11", font=("Bauhaus 93",18), relief="raised", bg="yellow", command=lambda: showWarning(day11))
day11.grid(row=0,column=10)
day12 = tk.Button(dayTrack, text="12", font=("Bauhaus 93",18), relief="raised", bg="yellow", command=lambda: showWarning(day12))
day12.grid(row=0,column=11)
day13 = tk.Button(dayTrack, text="13", font=("Bauhaus 93",18), relief="raised", bg="yellow", command=lambda: showWarning(day13))
day13.grid(row=0,column=12)
day14 = tk.Button(dayTrack, text="14", font=("Bauhaus 93",18), relief="raised", bg="yellow", command=lambda: showWarning(day14))
day14.grid(row=0,column=13)
day15 = tk.Button(dayTrack, text="15", font=("Bauhaus 93",18), relief="raised", bg="yellow", command=lambda: showWarning(day15))
day15.grid(row=0,column=14)
dayTrack.grid(row=6, rowspan=2, column=1, columnspan=2)
listDays = {day1: [], day2: [], day3: [], day4: [], day5: [], day6: [], day7: [], day8: [], day9: [], day10: [], day11: [], day12: [], day13: [], day14: [], day15: []}
currentDay = -1
main.mainloop()