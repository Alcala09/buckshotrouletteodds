import random

possibleItems = ["cigarettes", "beer", "magnifyingGlass", "handsaw", "handcuffs"]
itemsTest = []


def generateShells(): # restarts shells
    shellsList = []

    totalShells = random.randint(2,8)
    liveShells = max(1, totalShells / 2)
    blankShells = totalShells - liveShells

    for _ in range(totalShells):
        choice = random.randint(0, 1)
        if ((choice == 0) and (blankShells > 0)):
            shellsList.append("blank")
            blankShells -= 1
        elif (choice == 1) and (liveShells > 0):
            shellsList.append("live")
            liveShells -= 1

    return shellsList

def generateHealth(): # restarts health
    healthList = []

    startingHealth = random.randint(2, 4)
    
    for _ in range(2):
        healthList.append(startingHealth)

    return healthList



def generateItems(items): # restarts items

    itemsList = items

    itemCount = random.randint(1, 4)

    for _ in range(itemCount):

        if len(itemsList) < 8: 
            itemsList.append(random.choice(possibleItems))
    
    return itemsList

def originalDecision(startingHealth, currentHealth, shells, items, playerCuffed): # decision from original AI
    currentTurn = True

    while (currentTurn) and (currentHealth > 0):
        currentTurn = False
        playerCuffed = False
        knownShell = "none"
        shotgunDamage = 1
        target = "none"

        if len(shells) == 1: 
            knownShell = shells[0] # dealer knows if there is one shell left
            if knownShell == "blank":
                target = "self"
            elif knownShell == "live":
                target = "player"

        for i in range(len(items)):
            if ((items[i] == "magnifyingGlass") and (knownShell == "none") and (len(shells) > 1)):
                items[i] = "none" # uses item
                knownShell = shells[0] # dealer knows shell after using magnifying glass
                if knownShell == "blank":
                    target = "self"
                else:
                    target = "player"

            if ((items[i] == "cigarettes") and (currentHealth<startingHealth)):
                items[i] = "none" # uses cigarretes
                currentHealth += 1
            
            if ((items[i] == "beer") and (knownShell != "live") and (len(shells) > 1)):
                items[i] = "none" # use beer
                shells.pop(0) # removes shell
            
            if ((items[i] == "handcuffs") and (playerCuffed == False) and (len(shells) > 1)):
                items[i] = "none" # use handcuffs
                playerCuffed = True
            
            if ((items[i] == "handsaw") and (shotgunDamage == 1) and (knownShell == "live")):
                items[i] = "none" # use handsaw
                shotgunDamage = 2
            
        if ((shotgunDamage == 1) and ("handsaw" in items) and (knownShell != "blank")):
            choice = random.randint(0, 1)
            if choice == 0:
                target = "self"
            elif choice == 1:
                target = "player"
                items[items.index("handsaw")] = "none" # use handsaw
                shotgunDamage = 2
        
        if target == "none":
            choice = random.randint(0, 1)
            if choice == 0:
                target = "self"
            else:
                target = "player"

        items = [item for item in items if item != "none"]
        if shells[0] == "blank":
            shotgunDamage = 0
            if target == "self":
                currentTurn = True

        elif target == "self":
            currentHealth -= shotgunDamage

        print("Shotgun Damage: " + str(shotgunDamage) + " to " + target)
        print("Items: " + str(items))
        print("Health: " + str(currentHealth))
        print("Max Health: " + str(startingHealth))
        print("------------")

        if not ((shells[0] == "blank") and (target=="self")):
            currentTurn = playerCuffed

shellsTest = generateShells()
itemsTest = generateItems(itemsTest)
startingHealth = generateHealth()[0]

print(shellsTest)
print(itemsTest)

originalDecision(startingHealth, startingHealth, shellsTest, itemsTest, False)