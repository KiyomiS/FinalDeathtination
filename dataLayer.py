#convert from race key to english representation 
from os import supports_effective_ids


# ENCODE AND DECODE DICTIONARIES FOR CONVERSION
encodeKey = {
        "None":"0",
        # sex
        "M":"1",
        "F":"2",
        # race
        "White":"3",
        "Black":"4",
        "American Indian":"5",
        "Asian or Pacific Islander":"6",
        "Other":"7",
        # manner of death 
        "Accident":"8",
        "Suicide":"9",
        "Homicide":"A",
        "Pending investigation":"B",
        "Could not determine":"C",
        "Self-Inflicted":"D",
        "Natural":"E",
        # age
        "Under 1 month":"F",
        "1-11months":"G",
        "1":"H",
        "2":"I",
        "3":"J",
        "4":"K",
        "5-9":"L",
        "10-14":"M",
        "15-19":"N",
        "20-24":"O",
        "25-29":"P",
        "30-34":"Q",
        "35-39":"R",
        "40-44":"S",
        "45-49":"T",
        "50-54":"U",
        "55-59":"V",
        "60-64":"W",
        "65-69":"X",
        "70-74":"Y",
        "75-79":"Z",
        "80-84":"a",
        "85-89":"b",
        "90-94":"c",
        "95-99":"d",
        "100+":"e",
        "Age not stated":"f",
        # Month
        "January":"g",
        "February":"h",
        "March":"i",
        "April":"j",
        "May":"k",
        "June":"l",
        "July":"m",
        "August":"n",
        "September":"o",
        "October":"p",
        "November":"q",
        "December":"r",
        # Groups
        "Race":"s",
        "Sex":"t",
        "Age":"u",
        "Manner of Death":"v"
}

convertRace = {
        "0\n":"Other",
        "1\n":"White",
        "2\n": "Black",
        "3\n": "American Indian",
        "4\n": "Asian or Pacific Islander",
        "\n":"None"
}

encodeRace = {
        "Other":"0\n",
        "White":"1\n",
        "Black":"2\n",
        "American Indian":"3\n",
        "Asian or Pacific Islander":"4\n",
        "None":"\n",
}


convertSex = {
        "F":"F",    
        "M":"M",
        "":"None"
}

encodeSex = {
        "F":"F",    
        "M":"M",
        "None":"",
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
        "":"None"
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
        "None":""
}

convertMOD = {   
        "1": "Accident",
        "2": "Suicide",
        "3": "Homicide",
        "4": "Pending investigation",
        "5": "Could not determine",
        "6": "Self-Inflicted",
        "7": "Natural",
        "": "None"
}

encodeMOD = {   
        "Accident":"1",
        "Suicide":"2",
        "Homicide":"3",
        "Pending investigation":"4",
        "Could not determine":"5",
        "Self-Inflicted":"6",
        "Natural":"7",
        "None":"",
}

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
        "":"None"
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
        "None":"",
}

#create individual lists
csv_month = []
csv_age = []
csv_sex = []
csv_cause = []
csv_race = []


size = 0
# Checks for delete
delete_global_count = 0
# Dictionary for deleted input
del_dict = {} 
# Checks for import 
import_global_count = 0


def loadData(filestr):

    with open(filestr, 'r') as file:
        next(file)
        for line in file:
            cols = line.split(',')
            csv_month.append(convertMonth[cols[0]])
            csv_sex.append(convertSex[cols[1]])
            csv_age.append(convertAge[cols[2]])
            csv_cause.append(convertMOD[cols[3]])
            csv_race.append(convertRace[cols[4]]) 
            global size
            size = size + 1

        assert(len(csv_age) == len(csv_month) == len(csv_sex) == len(csv_cause) == len(csv_race))
            

def writeData(data):
    #update data in lists
    csv_month.append(data[0])
    csv_age.append(data[2])
    csv_sex.append(data[1])
    csv_race.append(data[4])
    csv_cause.append(data[3])
    global size
    size = size + 1
    return data   

def reloadData(filestr):
    global import_global_count
    global size

    csv_month.clear()
    csv_age.clear()
    csv_sex.clear()
    csv_cause.clear()
    csv_race.clear()
    # updates
    size = 0
    import_global_count = import_global_count + 1

    loadData(filestr)

def editData(data, row):
    row = row -1 #remove 1 to account for the missing title row

    #if the given data is "None", we keep the old data in the record. (i.e. the user does not want to change the data)
    if data[0] != "None":
        csv_month[row] = data[0] #update csv_list with new data

    if data[1] != "None":
        csv_sex[row] = data[1]

    if data[2] != "None":
        csv_age[row] = data[2]

    if data[3] != "None":
        csv_cause[row] = data[3]

    if data[4] != "None":
        csv_race[row] = data[4]

def deleteData(index_list, amount): 
    amount_to_decrement = amount
    # convert inputs in index_list to key and store in the dictionary that keeps track of how many has been deleted

    if (amount == "all"):
        for i in index_list:
            csv_age[i] = "!"
            csv_cause[i] = "!"
            csv_month[i] = "!"
            csv_race[i] = "!"
            csv_sex[i] = "!"
    else:
        for i in index_list:
            if (amount != 0):
                amount = amount - 1
                csv_age[i] = "!"
                csv_cause[i] = "!"
                csv_month[i] = "!"
                csv_race[i] = "!"
                csv_sex[i] = "!"
       
    result = []
    #clean data
    for age in csv_age:
        if (age != "!"):
            result.append(age)
    csv_age[:] = result 
    result.clear()

    for sex in csv_sex:
        if (sex != "!"):
            result.append(sex)
    csv_sex[:] = result 
    result.clear()

    for month in csv_month:
        if (month != "!"):
            result.append(month)
    csv_month[:] = result 
    result.clear()

    for cause in csv_cause:
        if (cause != "!"):
            result.append(cause)
    csv_cause[:] = result 
    result.clear()

    for race in csv_race:
        if (race != "!"):
            result.append(race)
    csv_race[:] = result 
    result.clear()

    global del_dict
    global size
    global delete_global_count
    delete_global_count = delete_global_count + 1
    
    size = size - amount_to_decrement  

def saveData(filestr):
    #open file, clear data, then write the column headers
    file = open(filestr, "w")
    file.write("month_of_death,sex,age_recode_27,manner_of_death,race_recode_5\n")
    file.close()
    #open file in append mode
    file = open(filestr, "a")
    
    for i in range(size):
        data = encodeMonth[csv_month[i]] +","+ encodeSex[csv_sex[i]]+","+encodeAge[csv_age[i]]+","+encodeMOD[csv_cause[i]]+","+encodeRace[csv_race[i]]
        # data = encodeMonth[csv_month[i]] 
        # +","+ encodeSex[csv_sex[i]]+","+encodeAge[csv_age[i]]+","+encodeMOD[csv_cause[i]]+","+encodeRace[csv_race[i]]
        file.write(data)
        
    file.close()

# GETTERS
def get_size():
    return size

def get_delete_gc():
    return delete_global_count

def get_delete_dict():
    return del_dict

def get_import_count():
    return import_global_count




#testing and debugging 
# month1 = "January"
# age1 = "75-79"
# sex1 = "M"
# race1 = "White"
# cause1 = "Natural"

# data1 = [sex1, age1, cause1, race1]
# print(encodeAverage[race1])

# test_list = [encodeAverage[race1],encodeAverage[sex1],encodeAverage[cause1],encodeAverage[age1]]
# print(test_list)
# test_list.sort()
# print(test_list)



# print(string_key)
# print(str(get_size()))
# loadData("2011_data.csv")
# print(str(get_size()))
# print(size)
# reloadData("2011_data.csv")
# print(size)
# writeData(data1)
# print(csv_month)
# saveData("2011_data.csv")