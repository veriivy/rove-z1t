#airline value per mile valuations
#codes for American Airlines
economyCodes = ["Y", "H", "K", "M", "L", "V", "G", "S", "N", "Q", "O", "B"]
premiumEconomyCodes = ["W", "P"]
businessAndFirstClassCodes = ["F", "J"]

#codes for United Airlines
uEconomyCodes = ["Y", "H", "K", "M", "L", "V", "G", "S", "N", "Q", "B", "E", "U", "W", "T"]
uPremiumEconomyCodes = ["O", "A", "R"]
uBusinessAndFirstClassCodes=["J", "C", "D", "Z", "P"]

#codes for Delta Airlines

dEconomyCodes = ["H", "W", "K", "L", "E"]
dBusinessClassCodes = ["Y", "B", "M", "W", "S"]
dPremiumBusinessCodes = ["P", "A", "G"]
dFirstClassCodes = ["J", "C", "D", "I", "Z"]

def get_value_per_mile_airlines(airline, classType):
    #American Airlines
    if (airline == "AA"):
        if (classType in economyCodes):
            return 1.6
        elif (classType in premiumEconomyCodes):
            return 1.92
        elif(classType in businessAndFirstClassCodes):
            return 3.3

    #United Airlines    
    if (airline == "UA"):
            if (classType in uEconomyCodes):
                return 1.09
            elif (classType in uPremiumEconomyCodes):
                return 1.32
            elif(classType in uBusinessAndFirstClassCodes):
                return 1.46
    
    #Delta Airlines
    if (airline == "DL"):
            if (classType in dEconomyCodes):
                return 1.12
            elif(classType in dBusinessClassCodes):
                return 1.24
            elif (classType in dPremiumBusinessCodes):
                 return 1.22
            elif (classType in dFirstClassCodes):
                 return 1.10
    


def value_per_mile_giftCards(giftCardType):
    if (giftCardType == "DL"):
         return 0.7
    if (giftCardType == "UA"):
         return 1.2
 
    




def value_per_mile_hotels(airlineType):
     #converting to Marriot Bonvoy
     if (airlineType == "AA"):
          return 0.3
     if (airlineType == "UA"):
          return 1
     if (airlineType == "DL"):
          return 2.5
