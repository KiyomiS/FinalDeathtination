from operationLayer import get_iDict,get_dDict,get_GIC,get_GDC,Search, getMODCountsByGroup, race_list, sex_list, mod_list, age_list, month_list
from dataLayer import convertMOD, encodeKey, get_import_count

#matplotlib and scipy for use in RegressionLine
# import matplotlib as plt
# plt.use('agg')
# import matplotlib.pyplot as plt
# from scipy import stats


# Dictionary for Group Rates
sum_for_percentage = {}
# Dictionary for Average
avg_dict = {}
# LOCAL NOTIFIER THAT THERE HAS BEEN A DELETION/INSERTON/EDIT IN GROUP RATES
LOCAL_DELETE_CHECK_GR = 0
LOCAL_INSERT_CHECK_GR = 0
LOCAL_EDIT_CHECK_GR = 0
LOCAL_IMPORT_CHECK_GR = 0

LOCAL_DELETE_CHECK_AVG = 0
LOCAL_INSERT_CHECK_AVG = 0
LOCAL_EDIT_CHECK_AVG = 0
LOCAL_IMPORT_CHECK_AVG = 0


# Rates
 
def donut_chart(time, var1 ,var2, var3, group_by): 
    # first parse
    global sum_for_percentage
    global LOCAL_DELETE_CHECK_GR
    global LOCAL_INSERT_CHECK_GR
    global LOCAL_IMPORT_CHECK_GR
    
    user_race = "None"
    user_sex = "None"
    user_mod = "None"
    user_age = "None"

    delete_boolean = False
    insert_boolean = False
    import_boolean = False 
    # print("LOCALINSERTCHECK: {}".format(LOCAL_INSERT_CHECK))
    # print("GLOBALINSERTCHECK: {}".format(GLOBAL_INSERT_CHECK))
    if LOCAL_IMPORT_CHECK_GR == get_import_count():
        import_boolean = True 
    else:
        sum_for_percentage.clear()
        LOCAL_IMPORT_CHECK_GR = get_import_count()

    if LOCAL_DELETE_CHECK_GR == get_GDC():
        delete_boolean = True

    if LOCAL_INSERT_CHECK_GR == get_GIC():
        insert_boolean = True
    
    # identify which type of var is inputted
    var_list = [var1, var2, var3]
    for i in range(len(var_list)):
        if var_list[i] in age_list:
            user_age = var_list[i]
        elif var_list[i] in race_list:
            user_race = var_list[i]
        elif var_list[i] in sex_list:
            user_sex = var_list[i]
        elif var_list[i] in mod_list:
            user_mod = var_list[i]

    
    sum_tot = Search(time, user_age, user_sex, user_race, user_mod)

    # print(sum_tot)
    
    group_by_list = []
    # identify the group by data
    if group_by == "Race":
        group_by_list = race_list
    elif group_by == "Age":
        group_by_list = age_list
    elif group_by == "Sex":
        group_by_list = sex_list
    elif group_by == "Manner of Death":
        group_by_list = mod_list
    
    # print(group_by_list)

    percentages = {}
    string_key = ""
    local_dDict = get_dDict()
    local_iDict = get_iDict()

    # let the search function know what list is being put in, and calculate the percentages for each element of the list and store in a dictionary
    for e in range(len(group_by_list)):
        if group_by_list == race_list:
            char_list = [encodeKey[time], encodeKey[user_age], encodeKey[user_sex], encodeKey[group_by_list[e]], encodeKey[user_mod]]
            char_list.sort()
            string_key = "".join(char_list)
            # checks if we have calculated the percentage before
            if string_key in sum_for_percentage:
                if string_key in local_dDict and delete_boolean == False:
                    sum_for_percentage[string_key] = sum_for_percentage[string_key] - local_dDict[string_key]
                    LOCAL_DELETE_CHECK_GR = get_GDC()
                    sum = sum_for_percentage[string_key]
                if string_key in local_iDict and insert_boolean == False:
                    sum_for_percentage[string_key] = sum_for_percentage[string_key] + local_iDict[string_key]
                    LOCAL_INSERT_CHECK_GR = get_GIC()
                    sum = sum_for_percentage[string_key] 
                else:
                    sum = sum_for_percentage[string_key]
                    
                percent_val = round(((sum)/sum_tot), 4)
            else:
                sum = Search(time, user_age, user_sex, group_by_list[e], user_mod)
                percent_val = round(((sum)/sum_tot), 4)
                sum_for_percentage[string_key] = sum

            percentages[percent_val] = group_by_list[e]

        elif group_by_list == age_list:
            char_list = [encodeKey[time], encodeKey[group_by_list[e]], encodeKey[user_sex], encodeKey[user_race], encodeKey[user_mod]]
            char_list.sort()
            string_key = "".join(char_list)
        
            if string_key in sum_for_percentage:
                if string_key in local_dDict and delete_boolean == False:
                    sum_for_percentage[string_key] = sum_for_percentage[string_key] - local_dDict[string_key]
                    LOCAL_DELETE_CHECK_GR = get_GDC()
                    sum = sum_for_percentage[string_key]
                if string_key in local_iDict and insert_boolean == False:
                    sum_for_percentage[string_key] = sum_for_percentage[string_key] + local_iDict[string_key]
                    LOCAL_INSERT_CHECK_GR = get_GIC()
                    sum = sum_for_percentage[string_key] 
                else:
                    sum = sum_for_percentage[string_key]
                    
                percent_val = round(((sum)/sum_tot), 4)
            else:
                sum = Search(time, group_by_list[e], user_sex, user_race, user_mod)
                percent_val = round(((sum)/sum_tot), 4)
                sum_for_percentage[string_key] = sum

            percentages[percent_val] = group_by_list[e]
            
            
        elif group_by_list == sex_list:
            char_list = [encodeKey[time], encodeKey[user_age], encodeKey[group_by_list[e]], encodeKey[user_race], encodeKey[user_mod]]
            char_list.sort()
            string_key = "".join(char_list)
            
            if string_key in sum_for_percentage:
                if string_key in local_dDict and delete_boolean == False:
                    sum_for_percentage[string_key] = sum_for_percentage[string_key] - local_dDict[string_key]
                    LOCAL_DELETE_CHECK_GR = get_GDC()
                    sum = sum_for_percentage[string_key]
                if string_key in local_iDict and insert_boolean == False:
                    sum_for_percentage[string_key] = sum_for_percentage[string_key] + local_iDict[string_key]
                    LOCAL_INSERT_CHECK_GR = get_GIC()
                    sum = sum_for_percentage[string_key] 
                else:
                    sum = sum_for_percentage[string_key]
                    
                percent_val = round(((sum)/sum_tot), 4)
            else:
                sum = Search(time, user_age, group_by_list[e], user_race, user_mod)
                percent_val = round(((sum)/sum_tot), 4)
                sum_for_percentage[string_key] = sum

            percentages[percent_val] = group_by_list[e]
            
           

        elif group_by_list == mod_list:
            char_list = [encodeKey[time], encodeKey[user_age], encodeKey[user_sex], encodeKey[user_race], encodeKey[group_by_list[e]]]
            char_list.sort()
            string_key = "".join(char_list)
            
            if string_key in sum_for_percentage:
                if string_key in local_dDict and delete_boolean == False:
                    sum_for_percentage[string_key] = sum_for_percentage[string_key] - local_dDict[string_key]
                    LOCAL_DELETE_CHECK_GR = get_GDC()
                    sum = sum_for_percentage[string_key]
                if string_key in local_iDict and insert_boolean == False:
                    sum_for_percentage[string_key] = sum_for_percentage[string_key] + local_iDict[string_key]
                    LOCAL_INSERT_CHECK_GR = get_GIC()
                    sum = sum_for_percentage[string_key] 
                else:
                    sum = sum_for_percentage[string_key]
                    
                percent_val = round(((sum)/sum_tot), 4)
            else:
                sum = Search(time, user_age, user_sex, user_race, group_by_list[e])
                percent_val = round(((sum)/sum_tot), 4)
                sum_for_percentage[string_key] = sum

            percentages[percent_val] = group_by_list[e]


    print(percentages)
    return percentages

def statistics(group):
    #group can be either sex, age, race, or month in string format, capital first letter
    mod_counts = getMODCountsByGroup(group)
    top_causes = []
    stats = []
    index_list = []
    labels = {}
    mean = 0
    median = 0
    stdDev = 0
            
    for i in range(len(mod_counts)):
        top_causes.append(max(mod_counts[i]))
        index_list.append(mod_counts[i].index(top_causes[i]))

    # get labels for graphs
    listptr = []
    if group == "Sex":
        listptr = sex_list
    elif group == "Age":
        listptr = age_list
    elif group == "Month":
        listptr = month_list
    elif group == "Race":
        listptr = race_list
    
    for i in range(len(listptr)):
        labels[top_causes[i]] = listptr[i] + " - " + convertMOD[str(index_list[i]+1)]

    top_causes.sort()

    #calculate mean
    for i in range(len(top_causes)):
        mean = mean + top_causes[i]

    mean = mean / len(top_causes)

    #get middle index
    m_index = int((len(top_causes)/2))

    #get median
    median = top_causes[m_index]

    #calculate standard deviation
    #get sum of (x-mean)^2
    for i in range(len(top_causes)):
        stdDev = stdDev + pow((top_causes[i] - mean),2)

    stdDev = stdDev/(len(top_causes))
    stdDev = (pow(stdDev, 0.5))

    #package data required for bar graph
    stats = [round(mean), median, round(stdDev), labels]

    return stats


#Rankings
def causeWithHighestDeath(month = "None", age="None", sex="None", race="None"): 
    # want it as a table for leading causes during period of time

    countAccident = Search(month, age, sex, race, "Accident")
    countSuicide = Search(month, age, sex, race, "Suicide")
    countHomicide = Search(month, age, sex, race, "Homicide")
    countPending = Search(month, age, sex, race, "Pending investigation")
    countNotAvailable = Search(month, age, sex, race, "Could not determine")
    countSelf = Search(month, age, sex, race, "Self-Inflicted")
    countNatural = Search(month, age, sex, race, "Natural")
    #countNotEnough = Search(month, age, sex, race, "None")
    #Is this actually needed?
    
    count= [countAccident, countSuicide, countHomicide, countPending, countNotAvailable, countSelf,countNatural]
    orderDeath = [] 
    ordered_values = []

    while len(count) > 0:
        a= max(count)
     
        if a == countAccident: 
            ordered_values.append(countAccident)
            orderDeath.append("Accident")
        if a == countSuicide:   
            ordered_values.append(countSuicide)
            orderDeath.append("Suicide")
        if a == countHomicide:
            ordered_values.append(countHomicide)
            orderDeath.append("Homocide")
        if a == countPending:
            ordered_values.append(countPending)
            orderDeath.append("Pending investigation")
        if a == countNotAvailable:
            ordered_values.append(countNotAvailable)
            orderDeath.append("Could not determine")
        if a == countSelf:
            ordered_values.append(countSelf)
            orderDeath.append("Self-Inflicted")
        if a == countNatural:
            ordered_values.append(countNatural)
            orderDeath.append("Natural")
        #if a == countSelf:
        #    orderDeath.append("")
        #is this actually needed?
        count.remove(a)
    
    ordered_values.reverse()
    orderDeath.reverse()
    #values_and_cause = {ordered_values[i]: orderDeath[i] for i in range(len(orderDeath))}
    values_and_cause = {orderDeath[i]: ordered_values[i] for i in range(len(orderDeath))}
    return values_and_cause

def monthWithHighestDeath(age="None", sex="None", race="None", cause="None"):
    count = []
    for i in month_list :
        count.append(Search( i, age, sex, race, cause))


    count_index = sorted(range(len(count)), key=count.__getitem__)
    #count_index.reverse()


    ordered_count = []
    ranking_list = []
    for j in count_index :
        ordered_count.append(count[j])
        ranking_list.append(month_list[j])

    both_lists = {ranking_list[i]: ordered_count[i] for i in range(len(ordered_count))}

           
    return both_lists

def ageWithHighestDeath(month="None", sex="None", race="None", cause="None"):
 
    count = []
    for i in age_list :
        count.append(Search( month, i, sex, race, cause))

    count_index = sorted(range(len(count)), key=count.__getitem__)
    #count_index.reverse()

    ordered_count = []
    ranking_list = []
    for j in count_index :
        ordered_count.append(count[j])
        ranking_list.append(age_list[j])

    both_lists = {ranking_list[i]: ordered_count[i] for i in range(len(ordered_count))}

    return both_lists

def raceWithHighestDeath(month="None", age="None", sex="None", cause="None"):
 
    count = []
    for i in race_list :
        count.append(Search( month, age, sex, i, cause))

    count_index = sorted(range(len(count)), key=count.__getitem__)
    #count_index.reverse()

    ordered_count = []
    ranking_list = []
    for j in count_index :
        ordered_count.append(count[j])
        ranking_list.append(race_list[j])

    both_lists = {ranking_list[i]: ordered_count[i] for i in range(len(ordered_count))}

    return both_lists

def sexWithHighestDeath(month="None", age="None", race="None", cause="None"):
  
    max_value = 0
    low_value = 0
    gender_rank = []
    if (Search( month, age, "M", race, cause)) >  (Search( month, age, "F", race, cause)):
        max_value = Search( month, age, "M", race, cause)
        gender_rank.append("M")
        low_value = Search( month, age, "F", race, cause)
        gender_rank.append("F")
    else :
        max_value = Search( month, age, "F", race, cause)
        gender_rank.append("F")
        low_value = Search( month, age, "M", race, cause)
        gender_rank.append("M")
    
    value_list = [max_value, low_value]
    value_list.reverse()
    gender_rank.reverse()

    both_lists = {gender_rank[i]: value_list[i] for i in range(len(value_list))}

    return both_lists

# def RegressionLine(age="None", sex="None", race="None", cause="None"):
#     fig, ax = plt.subplots(figsize=(10,10))
#     arr1=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"] #one will be months, the others will be data depenidng on stuff
#     arr2=[]#fill this array up take parameters to do regression line 
#     #search each month and then draw line use csv_month
#     arr3=[1,2,3,4,5,6,7,8,9,10,11,12]
#     for i in month_list :
#         arr2.append(Search( i, age, sex, race, cause))
#     #now for everymonth we should have the list but it doesn't need to be sorted
#     #now have both arrays, sorted by parameters 
#     slope, intercept, r, p, std_err = stats.linregress(arr3, arr2)
#     def func(arr3):
#         return slope*arr3+intercept
    
#     model=list(map(func,arr3))
#     plt.scatter(arr3, arr2)
#     plt.plot(arr3, model)
#     plt.xlabel("Months")
#     plt.ylabel("Deaths")
#     plt.savefig('Scatterplot.png')

def monthPercentage(age, sex, race, cause):

    month_percentages = {}
    top_value = 0
    total = Search("None", age, sex, race, cause)
    top_month = ""

    for i in range(len(month_list)):
        val = Search(month_list[i], age, sex, race, cause)
        #month_percentages[round(val / total * 100, 1)] = month_list[i]
        month_percentages[month_list[i]] = round(val / total * 100, 1)
        print (month_list[i], val, "new")
        total = total + val
        if val > top_value:
            top_value = val
            top_month = month_list[i]

    data = [top_month, month_percentages]
    return data

def findAverage(var1, var2, var3, var4):
    global avg_dict
    global LOCAL_DELETE_CHECK_AVG
    global LOCAL_INSERT_CHECK_AVG
    global LOCAL_IMPORT_CHECK_AVG

    delete_boolean = False
    insert_boolean = False

    if LOCAL_IMPORT_CHECK_AVG == get_import_count():
        import_boolean = True 
    else:
        avg_dict.clear()
        LOCAL_IMPORT_CHECK_GR = get_import_count()

    if LOCAL_DELETE_CHECK_AVG == get_GDC():
        delete_boolean = True

    if LOCAL_INSERT_CHECK_AVG == get_GIC():
        insert_boolean = True
       

    user_age = "None"
    user_race = "None"
    user_sex = "None"
    user_mod = "None"
    var_list = [var1, var2, var3, var4]
    for i in range(len(var_list)):
        if var_list[i] in age_list:
            user_age = var_list[i]
        elif var_list[i] in race_list:
            user_race = var_list[i]
        elif var_list[i] in sex_list:
            user_sex = var_list[i]
        elif var_list[i] in mod_list:
            user_mod = var_list[i]

    char_list = [encodeKey[var1], encodeKey[var2], encodeKey[var3], encodeKey[var4]]
    char_list.sort()
    string_key = "".join(char_list)
    local_dDict = get_dDict()
    local_iDict = get_iDict()


    if string_key in avg_dict:
        if string_key in local_dDict and delete_boolean == False:
            avg_dict[string_key] = avg_dict[string_key] - local_dDict[string_key]
            LOCAL_DELETE_CHECK_AVG = get_GDC()
            sum = avg_dict[string_key]
        if string_key in local_iDict and insert_boolean == False:
            avg_dict[string_key] = avg_dict[string_key] + local_iDict[string_key]
            LOCAL_INSERT_CHECK_AVG = get_GIC()
            sum = avg_dict[string_key] 
        else:
            sum = avg_dict[string_key]
    else:
        sum = Search("None", user_age, user_sex, user_race, user_mod)
        avg_dict[string_key] = sum
    
    avg = sum/12.0
    return round(avg)





# test
# test cases
# reloadData("2011_data.csv")
# RegressionLine("None", "None", "None", "None")
# test_age = "None"
# test_sex = "M"
# test_mod = "None"
# test_race = "White"
# loadData("2012_data.csv")
# print("MANUAL AVERAGE")
# manual_avg = round(Search("None",test_age,test_sex,test_race,test_mod)/12.0)
# print(manual_avg)
# print("AVG")
# print(findAverage(test_age,test_sex,test_race,test_mod))
# print("AFTER DELETE")
# removeData("None",test_age,test_sex,test_race,test_mod,100000)
# print("MANUAL AVERAGE")
# manual_avg = round(Search("None",test_age,test_sex,test_race,test_mod)/12.0)
# print(manual_avg)
# print("AVG")
# print(findAverage(test_age,test_sex,test_race,test_mod))
# print(findAverage(test_age,test_sex,test_race,test_mod))
# donut_chart("None", "White", "Male", "None", "Manner of Death")
# print("second time around")
# donut_chart("None", "Male", "None", "White", "Manner of Death")
# print(get_GDC())
# print(get_GIC())

# print(str(findAverage("50-54", "M", "White", "None")))
