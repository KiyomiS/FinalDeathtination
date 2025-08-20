

#convert from race key to english representation 

convertRace = {
        "0\n":"Other",
        "1\n":"White",
        "2\n": "Black",
        "3\n": "American Indian",
        "4\n": "Asian or Pacific Islander",
        "" : "Not specified"
}

encodeRace = {
        "Other":"0\n",
        "White":"1\n",
        "Black":"2\n",
        "American Indian":"3\n",
        "Asian or Pacific Islander":"4\n",
        "Not specified":"",
}

convertAge = {
        "10":"20-24",
        "11":"25-29",
        "12":"30-34",
        "13":"35-39",
        "14":"40-44",
        "15":"45-49",
        "16":"50-54",
        "17":"55-59",
        "18":"60-64",
        "19":"65-69",
        "20":"70-74",
        "21":"75-79",
        "22":"80-84",
        "23":"85-89",
        "24":"90-94",
        "25":"95-99",
        "26":"100+",
        "27":"Age not stated",
        "1":"Under 1 month",
        "2":"1-11months",
        "3":"1",
        "4":"2",
        "5":"3",
        "6":"4",
        "7":"5-9",
        "8":"10-14",
        "9":"15-19",
}

encodeAge = {
        "20-24":"10",
        "25-29":"11",
        "30-34":"12",
        "35-39":"13",
        "40-44":"14",
        "45-49":"15",
        "50-54":"16",
        "55-59":"17",
        "60-64":"18",
        "65-69":"19",
        "70-74":"20",
        "75-79":"21",
        "80-84":"22",
        "85-89":"23",
        "90-94":"24",
        "95-99":"25",
        "100+":"26",
        "Age not stated":"27",
        "Under 1 month":"1",
        "1-11months":"2",
        "1":"3",
        "2":"4",
        "3":"5",
        "4":"6",
        "5-9":"7",
        "10-14":"8",
        "15-19":"9",
}
#convert from method of death key to english representation 

convertMOD = {   
        "1": "Accident",
        "2": "Suicide",
        "3": "Homicide",
        "4": "Pending investigation",
        "5": "Could not determine",
        "6": "Self-Inflicted",
        "7": "Natural",
        "": "Not specified"
    }

encodeMOD = {   
        "Accident":"1",
        "Suicide":"2",
        "Homicide":"3",
        "Pending investigation":"4",
        "Could not determine":"5",
        "Self-Inflicted":"6",
        "Natural":"7",
        "Not specified":"",
    }

#convert from month key to english representation 
convertMonth =  {
        "1": "January",
        "2": "February",
        "3": "March",
        "4": "April",
        "5": "May",
        "6": "June",
        "7": "July",
        "8": "August",
        "9": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    }

encodeMonth =  {
        "January":"1",
        "February":"2",
        "March":"3",
        "April":"4",
        "May":"5",
        "June":"6",
        "July":"7",
        "August":"8",
        "September":"9",
        "October":"10",
        "November":"11",
        "December":"12",
    }
#create individual lists
csv_month = []
csv_age = []
csv_sex = []
csv_cause = []
csv_race = []

def loadData(filestr):

    with open(filestr, 'r') as file:
        next(file)
        for line in file:
            cols = line.split(',')
            csv_month.append(convertMonth[cols[0]])
            csv_sex.append(cols[1])
            csv_age.append(convertAge[cols[2]])
            csv_cause.append(convertMOD[cols[3]])
            csv_race.append(convertRace[cols[4]])

def writeData(filestr, data):
    #encode the data for csv
    data[0] = encodeMonth[data[0]]
    data[2] = encodeAge[data[2]]
    data[4] = encodeRace[data[4]]
    data[3] = encodeMOD[data[3]]

    #update data in lists
    csv_month.append(data[0])
    csv_age.append(data[2])
    csv_sex.append(data[1])
    csv_race.append(data[4])
    csv_cause.append(data[3])

    #create string in csv format
    csvstr = ",".join(data)

    #add new record to end of csv
    file = open(filestr,"a")
    file.write(csvstr)
    file.close()

def editData(filestr,data, row):
    row = row -1 #remove 1 to account for the missing title row

    #if the given data is "None", we keep the old data in the record. (i.e. the user does not want to change the data)
    if data[0] != "None":
        data[0] =  encodeMonth[data[0]] #encode the data
        csv_month[row] = data[0] #update csv with new data
    else: 
        data[0] = encodeMonth[csv_month[row]] #keep old data

    if data[1] != "None":
        csv_sex[row] = data[1]
    else:
        data[1] = csv_sex[row]

    if data[2] != "None":
        data[2] = encodeAge[data[2]]
        csv_age[row] = data[2]
    else:
        data[2] = encodeAge[csv_age[row]]

    if data[3] != "None":
        data[3] = encodeMOD[data[3]]
        csv_cause[row] = data[3]
    else:
        data[3] = encodeMOD[csv_cause[row]]

    if data[4] != "None":
        data[4] = encodeRace[data[4]]
        csv_race[row] = data[4]
    else:
        data[4] = encodeRace[csv_race[row]]

    csvstr = ",".join(data) #str in csv format

    file = open(filestr,"r")
    stringList = file.readlines() #list of strings, each string represents a single row in the csv
    file.close()

    stringList[row+1] = csvstr #replace the row    

    file = open(filestr, "w")
    newData = "".join(stringList)
    file.write(newData)
    file.close()

def deleteData(filestr, index_list, amount): 

    file = open(filestr, "r")
    stringList = file.readlines()
    file.close()
    
    if (amount == "all"):
        for i in index_list:
            stringList[i] = ""
    else:
        for i in index_list:
            if (amount != 0):
                amount = amount - 1
                stringList[i] = ""
    
    file = open(filestr, "w")
    newData = "".join(stringList)
    file.write(newData)
    file.close()


