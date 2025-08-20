from os import supports_effective_ids
# from flask import Flask, redirect, url_for, render_template, request, sessionclear
from newDataLayer import editData, loadData, writeData, deleteData, csv_race,csv_cause, csv_month, csv_sex, csv_age
import csv

filestr = "2011_data.csv"
loadData(filestr)

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
            

def SearchData(input_list):
    sum = 0
    data_list = []
    compare_list = []
    for l in range(len(input_list)):
                compare_list.append(input_list[l].name)

    for j in range(len(csv_sex)):
        for i in range(len(input_list)):
            data_list.append(input_list[i].internal_list[j])

        if (compare_list == data_list):
            sum = sum + 1

        data_list.clear()


    return sum 

def getIndices(input_list):
    data_list = []
    compare_list = []
    index_list = [] #list that keeps all matching indices 
    for l in range(len(input_list)):
                compare_list.append(input_list[l].name)

    for j in range(len(csv_sex)):
        for i in range(len(input_list)):
            data_list.append(input_list[i].internal_list[j])

        if (compare_list == data_list):

            index_list.append(j+1) #match found, add the index to list. add 1 to account for title row

        data_list.clear()

    return index_list 


# getData(month1, age1, sex1, race1, cause1)
# parseInputs(obj_container, filtered_obj_container)
# SearchData(filtered_obj_container)

def Search(month, age, sex, race, cause):
    getData(month, age, sex, race, cause)
    parseInputs(obj_container, filtered_obj_container)
    return SearchData(filtered_obj_container)

def removeData(month, age, sex, race, cause, amount): 
    getData(month, age, sex, race, cause)
    parseInputs(obj_container, filtered_obj_container)
    index_list = getIndices(filtered_obj_container)
    deleteData(filestr, index_list, amount)

def changeData(month, age, sex, race, cause, row): 
    data = [month, sex, age, cause, race] 
    editData(filestr, data, row)
   

def insertData(month, age, sex, race, cause): 
    #this function is a little redundant, as all it does is organize data and then call another function...
    data = [month, sex, age, cause, race] 
    writeData(filestr, data)

#TEST CASES 
month1 = "February"
age1 = "15-19"
sex1 = "M"
race1 = "White"
cause1 = "Natural"

# # insert new record/data test
#datatest = ['None', 'F', '25-29','None','None']
print(str(Search(month1, age1, sex1, race1, cause1)))
#removeData(month1, age1, sex1, race1, cause1, 3)
print(str(Search(month1, age1, sex1, race1, cause1)))
# writeData(filestr, data)
    
# # edit record test 
changeData(month1, age1, sex1, race1, cause1, 3)

# delete data test
# removeData("None", "None", "M", "None", "None", 100000)
#removeData("January", "65-69", "F", "White", "Natural")

