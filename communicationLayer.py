from flask import Flask, redirect, url_for, render_template, request, sessions
from operationLayer import Search,removeData, changeData, insertData, getTotal, get_data_at_index, age_list, sex_list, race_list, mod_list
from dataLayer import saveData, reloadData
from analyticsLayer import findAverage , donut_chart, statistics, causeWithHighestDeath, monthWithHighestDeath, ageWithHighestDeath, sexWithHighestDeath, raceWithHighestDeath, monthPercentage
import time 




app = Flask(__name__)


# GLOBALS
filename = ""
Import_check = False


# import function
@app.route("/")
def home():
	return render_template("home.html")

# Test
@app.route("/test")
def test():
	return render_template("test.html")

# import function
@app.route("/import/2011")
def importdata2011():
	global Import_check
	Import_check = True
	global filename
	year = "2011"
	filename = "2011_data.csv"
	reloadData(filename)

	return render_template("import.html", user_year=year)

@app.route("/import/2012")
def importdata2012():
	global Import_check
	Import_check = True
	global filename
	year = "2012"
	filename = "2012_data.csv"
	reloadData("2012_data.csv")
	return render_template("import.html", user_year=year)

@app.route("/import/2013")
def importdata2013():
	global Import_check
	Import_check = True
	global filename
	year = "2013"
	filename = "2013_data.csv"
	reloadData("2013_data.csv")
	return render_template("import.html", user_year=year)

@app.route("/import/2014")
def importdata2014():
	global Import_check
	Import_check = True
	global filename
	year = "2014"
	filename = "2014_data.csv"
	reloadData("2014_data.csv")
	return render_template("import.html", user_year=year)

@app.route("/import/2015")
def importdata2015():
	global Import_check
	Import_check = True
	global filename
	year = "2015"
	filename = "2015_data.csv"
	reloadData("2015_data.csv")
	return render_template("import.html", )


# BackUp function
@app.route("/backup/")
def backup():
	global filename
	saveData(filename)
	return render_template("backup.html")


# Search functions
@app.route("/index", methods = ["POST", "GET"])
def index():
	global Import_check
	if (request.method =="POST"):
		raceinput = request.form["Races"]
		sexinput = request.form["Sexes"]
		ageinput = request.form["Ages"]
		modinput = request.form["MoD"]
		monthinput = request.form["Month"]
	
		if raceinput == "None" and sexinput == "None" and ageinput == "None" and modinput == "None" and monthinput == "None":
			return render_template("errorpage.html")
		elif Import_check == False:
			return render_template("errorpage_import.html")
		else:
			return redirect(url_for("attributes", race_in=raceinput, sex_in=sexinput, age_in=ageinput, mod_in=modinput, month_in=monthinput))
			
	else:
	 	return render_template("index.html")

@app.route("/attributes/<race_in>/<sex_in>/<age_in>/<mod_in>/<month_in>")
def attributes(race_in, sex_in, age_in, mod_in, month_in):
	totalsum = str(Search(month_in, age_in, sex_in, race_in, mod_in))
	
	return render_template("sumpage.html", race=race_in, sex=sex_in, age=age_in, cause=mod_in, month=month_in, inputsum=totalsum)
	



# Delete functions
@app.route("/delete", methods = ["POST", "GET"])
def delete():
	global Import_check
	if (request.method =="POST"):
		raceinput = request.form["Races"]
		sexinput = request.form["Sexes"]
		ageinput = request.form["Ages"]
		modinput = request.form["MoD"]
		monthinput = request.form["Month"]
	
		if raceinput == "None" and sexinput == "None" and ageinput == "None" and modinput == "None" and monthinput == "None":
			return render_template("errorpage.html")
		elif Import_check == False:
			return render_template("errorpage_import.html")
		else: 
			return redirect(url_for("delpg", race_in=raceinput, sex_in=sexinput, age_in=ageinput, mod_in=modinput, month_in=monthinput))
			
	else:
	 	return render_template("delete.html")

@app.route("/delete/<race_in>/<sex_in>/<age_in>/<mod_in>/<month_in>", methods = ["POST", "GET"])
def delpg(race_in, sex_in, age_in, mod_in, month_in):
	totalsum = str(Search(month_in, age_in, sex_in, race_in, mod_in))
	if (request.method =="POST"):
		delnumber = int(request.form['deletenumber'])
	
		if (delnumber) > int(totalsum):
			return render_template("errorpage.html")
		else: 
			return redirect(url_for("delpgfin", Race_in=race_in, Sex_in=sex_in, Age_in=age_in, Mod_in=mod_in, Month_in=month_in, Delnumber=delnumber))
			
	else:	
	    return render_template("deletepage.html", race=race_in, sex=sex_in, age=age_in, cause=mod_in, month=month_in, inputsum=totalsum)

@app.route("/delpgfin/<Race_in>/<Sex_in>/<Age_in>/<Mod_in>/<Month_in>/<Delnumber>")
def delpgfin(Race_in, Sex_in, Age_in, Mod_in, Month_in, Delnumber):
	removeData(Month_in, Age_in, Sex_in, Race_in, Mod_in, int(Delnumber))
	return render_template("deletepagefinished.html", race=Race_in, sex=Sex_in, age=Age_in, cause=Mod_in, month=Month_in, delnumber=Delnumber)
	


# Edit functions
@app.route("/edit", methods = ["POST", "GET"])
def edit():
    outofbounds = 0
    totalindex = getTotal()
    if (request.method =="POST"):
        userindex = int(request.form["newindex"])
        if (userindex > totalindex or userindex < 0):
            outofbounds += 1
            return render_template("editpage.html", out_of_bounds=outofbounds, totalIndex=totalindex)
        elif Import_check == False:
            return render_template("errorpage_import.html")
        else:
            return redirect(url_for("editexec", index=userindex))
    else:
        return render_template("editpage.html", totalIndex=totalindex)


@app.route("/edit/<index>/", methods = ["POST", "GET"])
def editexec(index):
	newData1 = get_data_at_index(int(index)-1)
	if (request.method =="POST"):
		raceinput = request.form["Races"]
		sexinput = request.form["Sexes"]
		ageinput = request.form["Ages"]
		modinput = request.form["MoD"]
		monthinput = request.form["Month"]
		if raceinput == "None" and sexinput == "None" and ageinput == "None" and modinput == "None" and monthinput == "None":
			return render_template("errorpage.html")
		else: 
			return redirect(url_for("editData",  transferindex = index,RACE = raceinput, SEX = sexinput, AGE = ageinput, MOD = modinput, MONTH = monthinput))
	else: 
		return render_template("editpage2.html", month=newData1[0], age=newData1[1], sex=newData1[2], race=newData1[3], cause=newData1[4])
	

@app.route("/edit/<transferindex>/<RACE>/<SEX>/<AGE>/<MOD>/<MONTH>", methods = ["POST", "GET"])
def editData(RACE,SEX,AGE,MOD,MONTH,transferindex):
	changeData(MONTH,AGE,SEX,RACE,MOD,int(transferindex))
	newData = get_data_at_index(int(transferindex)-1)
	return render_template("editpage3.html", month=newData[0], age=newData[1], sex=newData[2], race=newData[3], cause=newData[4])


# Insert functions 
@app.route("/insert", methods = ["POST", "GET"])
def insert():
	if (request.method =="POST"):
		raceinput = request.form["Races"]
		sexinput = request.form["Sexes"]
		ageinput = request.form["Ages"]
		modinput = request.form["MoD"]
		monthinput = request.form["Month"]
	
		if raceinput == "None" and sexinput == "None" and ageinput == "None" and modinput == "None" and monthinput == "None":
			return render_template("errorpage.html")
		elif Import_check == False:
			return render_template("errorpage_import.html")
		else: 
			return redirect(url_for("insertpg", race_in=raceinput, sex_in=sexinput, age_in=ageinput, mod_in=modinput, month_in=monthinput))
	
	else:
	 	return render_template("insert.html")


@app.route("/insert/<race_in>/<sex_in>/<age_in>/<mod_in>/<month_in>")
def insertpg(race_in, sex_in, age_in, mod_in, month_in):
	insertData(month_in, age_in, sex_in, race_in, mod_in)
	return render_template("insertpage.html", race=race_in, sex=sex_in, age=age_in, cause=mod_in, month=month_in)

# Rates 
@app.route("/rates", methods = ["POST", "GET"])
def rates():
	if (request.method =="POST"):
		timeinput = request.form["Month"]
		var1 = request.form["Variable 1"]
		var2 = request.form["Variable 2"]
		var3 = request.form["Variable 3"]
		group = request.form["Group"]

		var_list = [var1, var2, var3]
		sum_age, sum_race, sum_sex, sum_mod = 0,0,0,0
		duplicate = 0
		for item in range(3):
				if var_list[item] in age_list:
					sum_age += 1
				elif var_list[item] in race_list:
					sum_race += 1
				elif var_list[item] in sex_list:
					sum_sex += 1
				elif var_list[item] in mod_list:
					sum_mod += 1
		
		if sum_age > 1 or sum_race > 1 or sum_sex > 1 or sum_mod > 1:
			duplicate += 1
			return render_template("ratespage.html", duplicate=duplicate)
		elif Import_check == False:
			return render_template("errorpage_import.html")
		else: 
			return redirect(url_for("ratespg", Time=timeinput, var_1=var1, var_2=var2, var_3=var3, group_by=group))		
	else:
		return render_template("ratespage.html")

@app.route("/rates/<Time>/<var_1>/<var_2>/<var_3>/<group_by>")
def ratespg(Time, var_1, var_2, var_3, group_by): 
	
	tic = time.perf_counter()
	data = donut_chart(Time, var_1, var_2, var_3, group_by)
	toc = time.perf_counter()
	performance = round((toc - tic)*1000,3)

	if Time == "None":
		Time = "All Months"

	
	return render_template("ratespage2.html", data=data, TIME=Time, VAR1=var_1, VAR2=var_2, VAR3=var_3, Groupby=group_by, perf_time=performance)

# Month Percentage
@app.route("/month_percentages", methods = ["POST", "GET"])
def month_percentage():
	if (request.method == "POST"):
		ageInput = request.form["Age"]
		sexInput = request.form["Sex"]
		raceInput = request.form["Race"]
		causeInput = request.form["Cause"]
		if Import_check == False:
			return render_template("errorpage_import.html")
		else:
			return redirect(url_for("month_percentage_pg", age = ageInput, sex =  sexInput, race = raceInput, cause = causeInput))

	else:
		return render_template("month_per.html")

@app.route("/month_percentages/<age>/<sex>/<race>/<cause>")
def month_percentage_pg(age,sex,race,cause):
	data = monthPercentage(age, sex, race, cause)
	return render_template("month_per2.html", topMonth = data[0], labels = data[1])

# Stats
@app.route("/stats", methods = ["POST", "GET"])
def stats():
	if (request.method == "POST"):
		groupInput = request.form["Group"]
		if Import_check == False:
			return render_template("errorpage_import.html")
		else:
			return redirect(url_for("statspg", Group = groupInput))

	else:
		return render_template("statspage.html")

@app.route("/stats/<Group>")
def statspg(Group):
	data = statistics(Group)
	return render_template("statspage2.html", mean = data[0], median = data[1], stdDev = data[2], labels = data[3])

#Ranking
@app.route("/rank", methods = ["POST", "GET"])
def rank():
	if (request.method == "POST"):
		groupInput = request.form["Group"]
		if Import_check == False:
			return render_template("errorpage_import.html")
		else:
			return redirect(url_for("rankCause", Group = groupInput))

	else:
		return render_template("rankpage.html")

@app.route("/rank/<Group>")
def rankCause(Group):
	#Month_in, Age_in, Sex_in, Race_in
	if Group == "Cause" :
		data = causeWithHighestDeath()
	if Group == "Month" :
		data = monthWithHighestDeath()
	if Group == "Age" :
		data = ageWithHighestDeath()
	if Group == "Race" :
		data = raceWithHighestDeath()
	if Group == "Sex" :
		data = sexWithHighestDeath()
	return render_template("rankingCause.html", labels = data, Group = Group)

@app.route("/rank/<Group>", methods = ["POST", "GET"])
def rankInput(Group):
	if (request.method =="POST"):
	
		raceinput = "None"
		sexinput = "None"
		ageinput = "None"
		modinput = "None"
		monthinput = "None"
		
		if Group != "Race" :
			raceinput = request.form["Races"]
		if Group != "Sex" :
			sexinput = request.form["Sexes"]
		if Group != "Age" :
			ageinput = request.form["Ages"]
		if Group != "Cause" :
			modinput = request.form["Cause"]
		if Group != "Month" :
			monthinput = request.form["Month"]
	
		if Group == "None":
			return render_template("errorpage.html")
		else: 
			if Group == "Cause" :
				data = causeWithHighestDeath(month = monthinput, age = ageinput, sex = sexinput, race = raceinput)
			elif Group == "Month" :
				data = monthWithHighestDeath(age = ageinput, sex = sexinput, race = raceinput, cause = modinput)
			elif Group == "Age" :
				data = ageWithHighestDeath(month = monthinput, sex = sexinput, race = raceinput, cause = modinput)
			elif Group == "Race" :
				data = raceWithHighestDeath(month = monthinput, age = ageinput, sex = sexinput, cause = modinput)
			elif Group == "Sex" :
				data = sexWithHighestDeath(month = monthinput, age = ageinput, race = raceinput, cause = modinput)
			return render_template("rankingCause.html", labels = data, Group = Group)
			
	else:
	 	return render_template("rankingCause.html")


# Prediction
@app.route("/predict", methods = ["POST", "GET"])
def predict():
	if (request.method == "POST"):
		ageInput = request.form["Age"]
		sexInput = request.form["Sex"]
		raceInput = request.form["Race"]
		causeInput = request.form["Cause"]
		
		if Import_check == False:
			return render_template("errorpage_import.html")
		else:
			return redirect(url_for("predictInput", age = ageInput, sex =  sexInput, race = raceInput, cause = causeInput))

	else:
		return render_template("predict.html")

@app.route("/predict/<age>/<sex>/<race>/<cause>")
def predictInput(age,sex,race,cause):
	# RegressionLine(age, sex, race, cause)
	return render_template("predict2.html")

# Averages
@app.route("/average/", methods = ["POST", "GET"])
def findAvg():
	if (request.method =="POST"):
		var1 = request.form["Variable 1"]
		var2 = request.form["Variable 2"]
		var3 = request.form["Variable 3"]
		var4 = request.form["Variable 4"]

		var_list = [var1, var2, var3, var4]
		# CHECK FOR DUPLICATES
		sum_age, sum_race, sum_sex, sum_mod = 0,0,0,0
		duplicate = 0
		for item in range(3):
				if var_list[item] in age_list:

					sum_age += 1
				elif var_list[item] in race_list:
					sum_race += 1
				elif var_list[item] in sex_list:
					sum_sex += 1
				elif var_list[item] in mod_list:
					sum_mod += 1
	
		if sum_age > 1 or sum_race > 1 or sum_sex > 1 or sum_mod > 1:
			duplicate += 1
			return render_template("averagepage1.html", duplicate=duplicate)
		# END OF CHECK FOR DUPICATES
		elif Import_check == False:
			return render_template("errorpage_import.html")
		else:
			return redirect(url_for("findAvg1", var_1=var1, var_2=var2, var_3=var3, var_4=var4))
			
	else:
		return render_template("averagepage1.html")


@app.route("/average/<var_1>/<var_2>/<var_3>/<var_4>")
def findAvg1(var_1,var_2,var_3,var_4):
	var_list = [var_1, var_2, var_3, var_4]
	agein, racein, sexin, modin = "None","None","None","None"
	# identify queries 
	for item in range(3):
			if var_list[item] in age_list:
				agein = var_list[item]
			elif var_list[item] in race_list:
				racein = var_list[item]
			elif var_list[item] in sex_list:
				sexin = var_list[item]
			elif var_list[item] in mod_list:
				modin = var_list[item]
	tic = time.perf_counter()
	Avg = findAverage(var_1,var_2,var_3,var_4)	
	toc = time.perf_counter()
	performance = round((toc - tic)*1000,3)
	return render_template("averagepage2.html", AVG=Avg, age=agein, race=racein, sex=sexin, cause=modin,perf_time=performance)




if __name__ == "__main__":
	app.run(debug = True, host = "0.0.0.0", port = 3000)