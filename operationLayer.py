from os import supports_effective_ids
from dataLayer import editData, writeData, deleteData, csv_race,csv_cause, csv_month, csv_sex, csv_age, encodeAge, encodeMOD, encodeMonth, encodeRace, get_size, encodeKey, get_import_count


# Dictionary for search Inputs
search_dict = {}
del_dict = {}
insert_dict = {}

#GLOBAL AND LOCAL CHECKS
LOCAL_IMPORT_CHECK = 0

GLOBAL_DELETE_CHECK = 0
LOCAL_DELETE_CHECK = 0

GLOBAL_INSERT_CHECK = 0
LOCAL_INSERT_CHECK = 0

class dataStruct:
    def __init__(self):
        self.name = ""
        self.internal_list = []
  
# Declare list objects
obj1 = dataStruct()
obj2 = dataStruct()
obj3 = dataStruct()
obj4 = dataStruct() 
obj5 = dataStruct()

# store lists 
obj1.internal_list = csv_month
obj2.internal_list = csv_age
obj3.internal_list = csv_sex
obj4.internal_list = csv_race
obj5.internal_list = csv_cause

# make list of objects for abstraction 
obj_container = [obj1, obj2, obj3, obj4, obj5]
filtered_obj_container = []

#list for analytics parameters 
race_list = [
    "Other",    
    "White", 
    "Black", 
    "American Indian", 
    "Asian or Pacific Islander"]
sex_list = [
    "M",
    "F"]
mod_list = [
    "Accident",
    "Suicide",
    "Homicide",
    "Pending investigation",
    "Could not determine",
    "Self-Inflicted",
    "Natural"
    ]
age_list = [
    "20-24",
    "25-29",
    "30-34",
    "35-39",
    "40-44",
    "45-49",
    "50-54",
    "55-59",
    "60-64",
    "65-69",
    "70-74",
    "75-79",
    "80-84",
    "85-89",
    "90-94",
    "95-99",
    "100+",
    "Age not stated",
    "Under 1 month",
    "1-11months",
    "1",
    "2",
    "3",
    "4",
    "5-9",
    "10-14",
    "15-19"
    ]
month_list = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

# make function to fetch and store inputs in objects
def getData(month, age, sex, race, cause):
    list_of_inputs = [month, age, sex, race, cause]
    
    for i in range(5): 
       
        obj_container[i].name = list_of_inputs[i]

# link obj names with lists 
def parseInputs(input_list1, input_list2):
    for i in range(5):
        if (input_list1[i].name != "None"):
            input_list2.append(input_list1[i])
            # print("appending object {}".format(i))
            
# Final Search for Data 
def SearchData(input_list):
    # print("input list:", input_list)
    sum = 0
    data_list = []
    compare_list = []
    for l in range(len(input_list)):
                compare_list.append(input_list[l].name)  
    for j in range(get_size()):
        for i in range(len(input_list)):
            data_list.append(input_list[i].internal_list[j])

        if (compare_list == data_list):
            sum = sum + 1
        data_list.clear()
    
    return sum 

def getIndices(input_list):
    compare_list = []
    index_list = [] #list that keeps all matching indices 
    for l in range(len(input_list)):
                compare_list.append(input_list[l].name)
    for j in range(get_size()):
        data_list = []
        for i in range(len(input_list)):
            data_list.append(input_list[i].internal_list[j])

        if (compare_list == data_list):

            index_list.append(j) 

    return index_list 

def Search(month, age, sex, race, cause):
    char_list = [encodeKey[month], encodeKey[age], encodeKey[sex], encodeKey[race], encodeKey[cause]]
    char_list.sort()
    string_key = "".join(char_list)
    global search_dict
    global insert_dict
    global del_dict
    global GLOBAL_DELETE_CHECK
    global GLOBAL_INSERT_CHECK
    global LOCAL_DELETE_CHECK
    global LOCAL_INSERT_CHECK
    global LOCAL_IMPORT_CHECK

    # POLL IF THERE HAS BEEN A DELETED CHANGE IN A STORED INPUT
    delete_boolean = False
    insert_boolean = False
    import_boolean = False


    if LOCAL_DELETE_CHECK == GLOBAL_DELETE_CHECK:
        delete_boolean = True

    if LOCAL_INSERT_CHECK == GLOBAL_INSERT_CHECK:
        insert_boolean = True

    if LOCAL_IMPORT_CHECK == get_import_count():
        import_boolean = True 
    else:
        search_dict.clear()
        LOCAL_IMPORT_CHECK = get_import_count()



    # IF THERE HAS BEEN A CHANGE CHECK IF THE IT AFFECTS A STORED INPUT

    if string_key in search_dict:
        if string_key in del_dict and delete_boolean == False:
            if not search_dict[string_key] == 0:
                search_dict[string_key] = search_dict[string_key] - del_dict[string_key]
                LOCAL_DELETE_CHECK = GLOBAL_DELETE_CHECK
                return search_dict[string_key]
        if string_key in insert_dict and insert_boolean == False:
            search_dict[string_key] = search_dict[string_key] + insert_dict[string_key]
            LOCAL_INSERT_CHECK = GLOBAL_INSERT_CHECK
            return search_dict[string_key]
        else:
            return search_dict[string_key]
    else:
        filtered_obj_container.clear()
        getData(month, age, sex, race, cause)
        parseInputs(obj_container, filtered_obj_container)
        search_dict[string_key] = SearchData(filtered_obj_container)
        return search_dict[string_key]
    
def removeData(month, age, sex, race, cause, amount): 
    global GLOBAL_DELETE_CHECK
    global del_dict
    GLOBAL_DELETE_CHECK = GLOBAL_DELETE_CHECK + 1
    char_list = [encodeKey[month], encodeKey[age], encodeKey[sex], encodeKey[race], encodeKey[cause]]
    char_list.sort()
    string_key = "".join(char_list)

    
    filtered_obj_container.clear()
    getData(month, age, sex, race, cause)
    parseInputs(obj_container, filtered_obj_container)
    index_list = getIndices(filtered_obj_container)
    deleteData(index_list, amount)
    del_dict[string_key] = amount

def changeData(month, age, sex, race, cause, row): 
    if row > get_size() or row < 0:
        return "ERROR OUT OF BOUNDS"
    else:
        data = [month, sex, age, cause, race] 
        editData(data, row)

def insertData(month, age, sex, race, cause): 
    global GLOBAL_INSERT_CHECK
    global insert_dict

    GLOBAL_INSERT_CHECK = GLOBAL_INSERT_CHECK + 1
    # print("GLOBALINSERTCHECK IN INSERT: {}".format(GLOBAL_INSERT_CHECK))
    # print("LOCALINSERTCHECK IN INSERT: {}".format(LOCAL_INSERT_CHECK))


    char_list = [encodeKey[month], encodeKey[age], encodeKey[sex], encodeKey[race], encodeKey[cause]]
    char_list.sort()
    string_key = "".join(char_list)
    #this function is a little redundant, as all it does is organize data and then call another function...
    data = [month, sex, age, cause, race]     
    writeData(data)
    if string_key in insert_dict:
        insert_dict[string_key] = insert_dict[string_key] + 1
    else:
        insert_dict[string_key] = 1  

# getters
# gets the size from data layer
def getTotal():
   return get_size()

def get_data_at_index(index):
    if index > get_size() or index < 0:
        data = []
        data.append(-1)
        data.append(-1)
        data.append(-1)
        data.append(-1)
        data.append(-1)
    else:
        data = []
        data.append(csv_month[index])
        data.append(csv_age[index])
        data.append(csv_sex[index])
        data.append(csv_race[index])
        data.append(csv_cause[index])
    return data

def getMODCountsByGroup(group):
    #there are four different branches in this function, but they all behave the same
    #only difference between them is how the data was stored. some data lists' values start at 0, some at 1.
    #theres also the sex data list which isn't in integers but characters. because of this there are 4 branches 
    #to accomadate
    
    parameters_list = [] #list of lists, each sublist represents a subgroup (e.g. a month, age group, etc.)
                         #each sublist will have 7 int values, each repreenting a cause of death count
    total = getTotal()

    if group == "Month":
        group = 0
        for i in range(12): # make the right # of sublists
            mod_counts = [0,0,0,0,0,0,0]
            parameters_list.append(mod_counts)
        
        for i in range(total): #count the causes, skip the ones not specified
            data = get_data_at_index(i)
            if (data[4] == "None"):
                continue

            # print(data[group])
            month_group = int(encodeMonth[data[group]])-1
            death_type = int(encodeMOD[data[4]])-1

            parameters_list[month_group][death_type] = parameters_list[month_group][death_type] + 1

    elif group == "Age":
        group = 1
        for i in range(len(age_list)):
            mod_counts = [0,0,0,0,0,0,0]
            parameters_list.append(mod_counts)
        
        for i in range(total):
            data = get_data_at_index(i)
            if (data[4] == "None"):
                continue

            age_group = int(encodeAge[data[group]])-1
            death_type = int(encodeMOD[data[4]])-1

            parameters_list[age_group][death_type] = parameters_list[age_group][death_type] + 1

    elif group == "Sex":
        group = 2
        for i in range(len(sex_list)):
            mod_counts = [0,0,0,0,0,0,0]
            parameters_list.append(mod_counts)

        for i in range(total):
            data = get_data_at_index(i)
            if (data[4] ==  "None"):
                continue

            sex_group = 0
            if (data[group] == 'M'):
                sex_group = 1
            
            death_type = int(encodeMOD[data[4]])-1

            parameters_list[sex_group][death_type] = parameters_list[sex_group][death_type] + 1
            
    elif group == "Race":
        group = 3
        for i in range(len(race_list)):
            mod_counts = [0,0,0,0,0,0,0]
            parameters_list.append(mod_counts)
        for i in range(total):
            data = get_data_at_index(i)
            if (data[4] == "None" or data[group] == "None"):
                continue
    
            race_group = int(encodeRace[data[group]])
            death_type = int(encodeMOD[data[4]])-1

            parameters_list[race_group][death_type] = parameters_list[race_group][death_type] + 1

    else:
        #error
        return
    return parameters_list

# get global insert count
def get_GIC():
    return GLOBAL_INSERT_CHECK 
# get global delete count
def get_GDC():
    return GLOBAL_DELETE_CHECK
# get insert dictionary
def get_iDict():
    return insert_dict
# get delete dictionary
def get_dDict():
    return del_dict











#TEST CASES


# month1 = "None"
# age1 = "None"
# sex1 = "None"
# race1 = "White"
# cause1 = "None"

# filename = "2011_data.csv"
# loadData(filename)
# print(str(Search(month1,age1,sex1,race1,cause1)))



# print(donut_chart("January", "White", "None", "None", "Race"))

# # insert new record/data test


# print(str(get_size()))
# print(csv_race)


# # print(csv_race)
# # print(str(get_size()))
# # backUp(filestr)
# reloadData(filestr)
# print(str(get_size()))
# print(str(Search(month1,age1,sex1,race1,cause1)))

# removeData(month1,age1,sex1,race1,cause1,1)


    
# # edit record test 
# changeData(month1, age1, sex1, race1, cause1, 1)

# delete data test
# removeData("None", "None", "M", "None", "None", "all")
# removeData("January", "65-69", "F", "White", "Natural")

# #integration test
# #all males removed, then a single one inserted at index 1. only males in csv after test should be index 1 and last index.
# removeData("None", "None", "M", "None", "None", "all")
# changeData(month1, age1, sex1, race1, cause1, 1)
# insertData("April", "30-34", "F", "American Indian", "Homsicide")
# saveData(filestr)
# print(str(Search("None","20-24","None","None","None")))
# print(str(Search("None","None","F","None","None")))
# print(str(Search("None","20-24","None","None","None")))