from os import remove
import unittest

from dataLayer import *
from operationLayer import *
from analyticsLayer import *

# DATALAYER 
class Test_Load_Data(unittest.TestCase):
    def test_load(self):
        loadData("test.csv")
        self.assertEqual(csv_age[0], "50-54")
        self.assertEqual(csv_month[0], "August")
        self.assertEqual(csv_sex[0], "M")
        self.assertEqual(csv_race[0], "White")
        self.assertEqual(csv_cause[0], "Suicide")

    def test_reload(self):
        loadData("test.csv")
        reloadData("test.csv")
        self.assertEqual(csv_age[0], "50-54")
        self.assertEqual(csv_month[0], "August")
        self.assertEqual(csv_sex[0], "M")
        self.assertEqual(csv_race[0], "White")
        self.assertEqual(csv_cause[0], "Suicide")

class Test_Search(unittest.TestCase):
    def setUp(self):
        reloadData("test.csv")

    def test_search(self):
        total = Search("August", "50-54", "M", "White", "Suicide")
        self.assertGreater(total,0)
        self.assertEqual(5,total)

    def test_search_all(self):
        total = Search("None", "None", "M", "None", "None")
        self.assertGreater(total,0)
        self.assertEqual(total,13)
        

    

# testing write as well 
class Test_Insert_Delete_Update(unittest.TestCase):
    def setUp(self):
        reloadData("test.csv")
    # insert tests
    def test_insert(self):
        insertData("January", "80-84", "M", "White", "Natural")
        self.assertEqual(csv_month[-1], "January")
        self.assertEqual(csv_age[-1], "80-84")
        self.assertEqual(csv_sex[-1], "M", "sex is wrong")
        self.assertEqual(csv_race[-1], "White")
        self.assertEqual(csv_cause[-1], "Natural")

    def test_insert_blanks(self):
        insertData("January", "None", "M", "None", "Natural")
        self.assertEqual(csv_month[-1], "January")
        self.assertEqual(csv_age[-1], "None")
        self.assertEqual(csv_sex[-1], "M")
        self.assertEqual(csv_race[-1], "None")
        self.assertEqual(csv_cause[-1], "Natural")
        self.assertIn("January",csv_month)

    def test_insert_None(self):
        insertData("None", "None", "None", "None", "None")
        self.assertEqual(csv_month[-1], "None")
        self.assertEqual(csv_age[-1], "None")
        self.assertEqual(csv_sex[-1], "None")
        self.assertEqual(csv_race[-1], "None")
        self.assertEqual(csv_cause[-1], "None")

    # delete tests
    def test_delete(self):
        total = Search("January", "None", "M", "White", "Natural")
        removeData("January", "None", "M", "White", "Natural", 2)
        total_after = Search("January", "None", "M", "White", "Natural")
        self.assertEqual(total, total_after + 2)
        self.assertNotEqual(total, total_after)
        self.assertGreater(total, total_after)
        
        
    def test_delete_zero(self):
        total = Search("January", "None", "M", "White", "Natural")
        removeData("January", "None", "M", "White", "Natural", 0)
        total_after = Search("January", "None", "M", "White", "Natural")
        self.assertNotEqual(total, total_after + 2)
        self.assertNotEqual(total, total_after - 2)
        self.assertEqual(total, total_after)

    # edge
    def test_delete_all(self):
        total = Search("February", "55-59", "F", "American Indian", "Homicide")
        size_before = len(csv_age)
        removeData("February", "55-59", "F", "American Indian", "Homicide", 2)
        size_after = len(csv_age)
        total_after = Search("February", "55-59", "F", "American Indian", "Homicide")
        self.assertEqual(total, total_after)
        self.assertEqual(total, 0)
        self.assertEqual(size_before, size_after)
        self.assertEqual(0, total_after)

    # update tests
    def test_edit(self):
        changeData("January", "80-84", "M", "White", "Natural", 2)
        self.assertEqual(csv_month[1], "January")
        self.assertEqual(csv_age[1], "80-84")
        self.assertEqual(csv_sex[1], "M")
        self.assertEqual(csv_race[1], "White")
        self.assertEqual(csv_cause[1], "Natural")

    def test_edit_outofbounds(self):
        self.assertEqual(changeData("January", "80-84", "M", "White", "Natural", 22), "ERROR OUT OF BOUNDS")
        
    def test_edit_blanks(self):
        changeData("January", "None", "M", "None", "Natural", 3)
        self.assertEqual(csv_month[2], "January")
        self.assertEqual(csv_age[2], "85-89")
        self.assertEqual(csv_sex[2], "M")
        self.assertEqual(csv_race[2], "White")
        self.assertEqual(csv_cause[2], "Natural")
        
class Test_Analytics(unittest.TestCase):
    def setUp(self):
        reloadData("test.csv")

    # average
    def test_average(self):
        avg = findAverage("M", "None", "None", "None")
        self.assertEqual(1,avg)

    def test_average_all(self):
        avg = findAverage("None", "None", "None", "None")
        self.assertEqual(2,avg)

    def test_average_all_inputs(self):
        avg = findAverage("M", "80-84", "Black", "Natural")
        self.assertEqual(0,avg)

    # group rates
    def test_group_rates_altered_tot(self):
        dict = {}
        dict_compare = {}
        dict[0.0] = "Self-Inflicted"
        dict[0.375] = "Suicide"
        dict[0.625] = "Natural"
        dict_compare = donut_chart("None", "White", "Male", "None", "Manner of Death")
        self.assertEqual(dict, dict_compare)
     
#Ranking Analytic Tests    
class Test_Analytic_Ranking(unittest.TestCase):
    def setUp(self):
        reloadData("test.csv")
        
    def test_Month(self) :
        monthWithDeaths = monthWithHighestDeath()
        self.assertEqual(len(monthWithDeaths), 12)
        self.assertEqual(monthWithDeaths["August"], 7)
        self.assertEqual(monthWithDeaths["April"], 0)


        j = 1
        values = list(monthWithDeaths.values())
        while j < len(monthWithDeaths):
            self.assertGreaterEqual(values[j], values[j - 1])
            j += 1

    def test_Age(self) :
        rankTesting = ageWithHighestDeath()
        self.assertEqual(len(rankTesting), 27)
        self.assertEqual(rankTesting["50-54"], 5)
        self.assertEqual(rankTesting["20-24"], 0)

        j = 1
        values = list(rankTesting.values())
        while j < len(rankTesting):
            self.assertGreaterEqual(values[j], values[j - 1])
            j += 1
    
    def test_Race(self) :
        rankTesting = raceWithHighestDeath()
        self.assertEqual(len(rankTesting), 5)
        self.assertEqual(rankTesting["White"], 16)
        self.assertEqual(rankTesting["Black"], 1)

        j = 1
        values = list(rankTesting.values())
        while j < len(rankTesting):
            self.assertGreaterEqual(values[j], values[j - 1])
            j += 1

    def test_Cause(self) :
        rankTesting = causeWithHighestDeath()
        self.assertEqual(len(rankTesting), 7)
        self.assertEqual(rankTesting["Suicide"], 6)
        self.assertEqual(rankTesting["Natural"], 12)

        j = 1
        values = list(rankTesting.values())
        while j < len(rankTesting):
            self.assertGreaterEqual(values[j], values[j - 1])
            j += 1

    def test_Sex(self) :
        rankTesting = sexWithHighestDeath()
        self.assertEqual(len(rankTesting), 2)
        self.assertEqual(rankTesting["M"], 13)
        self.assertEqual(rankTesting["F"], 5)

        j = 1
        values = list(rankTesting.values())
        while j < len(rankTesting):
            self.assertGreaterEqual(values[j], values[j - 1])
            j += 1
        
        
    




