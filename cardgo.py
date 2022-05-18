# Madeline Stevens
# 3.10.2

import random, math, json

# material name: [illegal,volatile,perishable (0=no, 1=yes),
# unit, avg quan, quan margin, avg price, price margin]
materials = {
"kemocite": [1,1,0,"kilos",200,100,7.5,2.5],
"dilithium": [0,0,0,"kilos",162.5,87,5,3,2],
"Andarian_glass_beads": [0,0,0,"grams",200,100,12.5,2.5],
"antimonium": [0,1,0,"kilos",27.5,22.5,7.5,2.5],
"quadrotriticale": [0,0,1,"bushels",175,125,6.5,3.5],
"Romulan_ale": [1,0,0,"bottles",30,20,75,25],
"Tallonian_crystal": [1,0,0,"grams",125,75,15,5],
"synthehol": [0,0,0,"cases",50,25,8.5,3.5],
"Gramilian_sand_peas": [0,0,1,"kilos",20,10,3.5,1.5],
"maraji_crystal": [1,0,0,"grams",55,45,30,20],
"Hupyrian_beetle_snuff": [0,0,0,"kilos",27.5,22.5,22.5,7.5],
"brizeen_nitrate": [0,0,0,"kilos",300,200,4,1],
"tulaberry_wine": [0,0,0,"vats",30,20,7.5,2.5],
"self-sealing_stem_bolts": [0,0,0,"gross",125,75,2,1],
"Saurian_brandy": [0,0,0,"bottles",20,10,20,10],
"Aldebaran_whiskey": [0,0,0,"barrels",12.5,7.5,32.5,17.5],
"yamok_sauce": [0,0,1,"wrappages",1000,500,0.3,0.2],
"Kohlanese_barley": [0,0,1,"bushels",225,175,1,0.25],
"Gamzian_wine": [0,0,0,"bottles",50,25,20,5],
"bloodwine": [0,0,0,"cases",30,15,30,20],
"bio-mimetic_gel": [1,1,0,"milliliters",17.5,7.5,175,25],
"Cardassian_voles": [0,0,1,"live voles",10,5,7.5,2.5],
"kanar": [0,0,0,"cases",17.5,7.5,10,5],
"feldomite": [0,0,0,"kilos",200,50,0.875,0.375],
"Slug-o-Cola": [0,0,1,"cases",30,15,6,3]
}

class Offer:
    def __init__(self):
        self.cargo = random.choice(list(materials.keys()))
        self.stats = materials[self.cargo]
        self.is_illegal = materials[self.cargo][0]
        self.is_volatile = materials[self.cargo][1]
        self.is_perishable = materials[self.cargo][2]
        self.unit = materials[self.cargo][3]
        self.avgQ = materials[self.cargo][4]
        self.marginQ = materials[self.cargo][5]
        self.minQ = self.avgQ - self.marginQ
        self.maxQ = self.avgQ + self.marginQ
        self.avgP = materials[self.cargo][6]
        self.marginP = materials[self.cargo][7]
        self.minP = self.avgP - self.marginP
        self.maxP = self.avgP + self.marginP
        self.muQ = math.log(self.avgQ)
        self.muP = math.log(self.avgP)
        self.sigmaQ = (math.log(self.maxQ)-math.log(self.minQ))/5.16
        self.sigmaP = (math.log(self.maxP)-math.log(self.minP))/5.16
        self.quantity = round(random.lognormvariate(self.muQ, self.sigmaQ))
        self.price = round(random.lognormvariate(self.muP, self.sigmaP),2)
        self.total = round(self.quantity*self.price,2)
        if self.is_perishable == 1:
            self.expDate = random.randint(3,8)
        else:
            self.expDate = 16
    def __str__(self):
        self.warnings = ""
        if self.is_perishable == 1:
            self.warnings = self.warnings + "\nThis cargo will expire in " + str(self.expDate) + " days."
        if self.is_illegal == 1:
            self.warnings = self.warnings + "\nThis cargo is illegal."
        if self.is_volatile == 1:
            self.warnings = self.warnings + "\nThis cargo is volatile."
        return (f"A vendor is selling {str(self.quantity)} {self.unit} of\n{self.cargo} for a unit price of\n ₷{self.price}, totaling ₷{self.total}.{self.warnings}")
    def tuplify(self):
        return (self.cargo, self.is_illegal, self.is_volatile, self.is_perishable, self.unit, self.quantity, self.price, self.total, self.expDate)
    def detuplify(self, data):
        self.cargo = data[0]
        self.is_illegal = data[1]
        self.is_volatile = data[2]
        self.is_perishable = data[3]
        self.unit = data[4]
        self.quantity = data[5]
        self.price = data[6]
        self.total = data[7]
        self.expDate = data[8]
        print(self)
        
class Contract:
    def __init__(self):
        self.cargo = random.choice(list(materials.keys()))
        self.stats = materials[self.cargo]
        self.is_illegal = materials[self.cargo][0]
        self.is_volatile = materials[self.cargo][1]
        self.is_perishable = materials[self.cargo][2]
        self.unit = materials[self.cargo][3]
        self.avgQ = materials[self.cargo][4]
        self.marginQ = materials[self.cargo][5]
        self.minQ = self.avgQ - self.marginQ
        self.maxQ = self.avgQ + self.marginQ
        self.avgP = materials[self.cargo][6]
        self.marginP = materials[self.cargo][7]
        self.minP = self.avgP - self.marginP
        self.maxP = self.avgP + self.marginP
        self.muQ = math.log(self.avgQ)
        self.muP = math.log(self.avgP)
        self.sigmaQ = (math.log(self.maxQ)-math.log(self.minQ))/5.16
        self.sigmaP = (math.log(self.maxP)-math.log(self.minP))/5.16
        self.quantity = round(random.lognormvariate(self.muQ, self.sigmaQ))
        self.price = round(random.lognormvariate(self.muP, self.sigmaP),2)
        self.total = round(self.quantity*self.price,2)
        self.dueDate = random.randint(2,6)
    def __str__(self):
        self.warnings = ""
        if self.is_illegal == 1:
            self.warnings = self.warnings + "\nThis cargo is illegal."
        if self.is_volatile == 1:
            self.warnings = self.warnings + "\nThis cargo is volatile."
        return (f"Contract to sell {str(self.quantity)} {self.unit} of\n{self.cargo} in {self.dueDate} days.\nThe unit price is ₷{self.price}, for a\n total value of ₷{self.total}.{self.warnings}")
    def accept(self, currentDay):
        self.actualDueDate = currentDay + self.dueDate
    def relative(self, currentDay):
        self.warnings = ""
        if self.is_illegal == 1:
            self.warnings = self.warnings + "\nThis cargo is illegal."
        if self.is_volatile == 1:
            self.warnings = self.warnings + "\nThis cargo is volatile."
        actualDay = self.actualDueDate - currentDay
        return (f"Contract to sell {str(self.quantity)} {self.unit} of\n{self.cargo} in {str(actualDay)} days.\nThe unit price is ₷{str(self.price)}, for a\n total value of ₷{str(self.total)}.{self.warnings}")
    def tuplify(self):
        return (self.cargo, self.is_illegal, self.is_volatile, self.is_perishable, self.unit, self.quantity, self.price, self.total, self.dueDate)
    def detuplify(self, data):
        self.cargo = data[0]
        self.is_illegal = data[1]
        self.is_volatile = data[2]
        self.is_perishable = data[3]
        self.unit = data[4]
        self.quantity = data[5]
        self.price = data[6]
        self.total = data[7]
        self.dueDate = data[8]
        print(self)