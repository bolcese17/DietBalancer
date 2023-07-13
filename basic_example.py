__author__ = 'hc'

from flask import Flask, render_template, request

app = Flask(__name__)


#from cosin similarity file in class
import math
import numpy as np 
import pandas as pd 

def dot(v1, v2):
	dotproduct = np.dot(v1,v2)
	return dotproduct

def mag(x): 
	return math.sqrt(sum(i**2 for i in x))

#Caloric Intake NOT USING THIS, WE USE PERSON CLASS WHICH HAS A FUNCTION FOR THIS
def caloric_intake():
  gender = input("Enter Gender (M/F): ")
  weight = int( input("Enter Weight (lbs): ") )
  feet, inches = input("Enter Height (ft,in)").split(",")
  age = int(input("Enter Age: ") )
  while (age <9):
    print("Sorry, our program is only suitable for people of age 9+ for now")
    age = int(input("Enter Age: ") )
  exercise = input("Enter Amount of Daily Activity (None, Light, Moderate, Heavy): ")
  while (exercise not in ["None", "Light", "Moderate", "Heavy"]):
    print("Please input only what's allowed!")
    exercise = input("Enter Amount of Daily Activity (None, Light, Moderate, Heavy): ")
  height = int(feet) * 12 + int(inches)
  
  bmr = 0
  calories = 0
  if gender == "M":
    bmr = 66 + (6.3 * weight) + (12.9 * height) - (6.8 * age)
  elif gender == "F":
    bmr = 655 + (4.3 * weight) + (4.7 * height) - (4.7 * age)
    
  if exercise == "None":
    calories = bmr * 1.2
  elif exercise == "Light":
    calories = bmr * 1.375
  elif exercise == "Moderate":
    calories = bmr * 1.55
  elif exercise == "Heavy":  
    calories = bmr * 1.725

#Macronutrients Intake 
  protein = (calories * .25)/4
  fat = (calories * .25)/9
  carbs = (calories * .50)/4
  print(calories)
  print(protein)
  print(fat)
  print(carbs)
  return [calories, protein, fat, carbs]

class person:
    bmr = 0
    calories = 0
    gender = ''
    age = -1
    
    def __init__(self, input_gender, input_weight, input_height, input_age, input_exercise):
        #print(input_gender, input_weight, input_height, input_age, input_exercise)
        self.gender = input_gender
        self.weight = float(input_weight)
        self.height = float(input_height)
        self.age = int(input_age)
        self.exercise = input_exercise
        self.compute_calo_bmr()
    def compute_calo_bmr(self):
        if self.gender == "M":
            self.bmr = 66 + (6.3 * self.weight) + (12.9 * self.height) - (6.8 * self.age)
            self.gender_interval = 0
        elif self.gender == "F":
            self.bmr = 655 + (4.3 * self.weight) + (4.7 * self.height) - (4.7 * self.age)
            self.gender_interval =1

        if self.exercise == "None":
            self.calories = self.bmr * 1.2
        elif self.exercise == "Light":
            self.calories = self.bmr * 1.375
        elif self.exercise == "Moderate":
            self.calories = self.bmr * 1.55
        elif self.exercise == "Heavy":
            self.calories = self.bmr * 1.725
    def caloric_intake(self):
        self.protein = round((self.calories * .25)/4,2)
        self.fat = round((self.calories * .25)/9,2)
        self.carbs = round((self.calories * .50)/4,2)
        return [self.calories, self.protein, self.fat, self.carbs]

    def nut_needed(self):
        df_ref_class= pd.read_csv('UserTable.csv', low_memory = False)
        df_ref_class = df_ref_class.drop(["Gender_Age"], axis =1)
        if self.age>=9 and self.age<=13:
            self.age_interval =0
        elif self.age>=14 and self.age<=18:
            self.age_interval =1
        elif self.age>=19 and self.age<=30:
            self.age_interval =2
        elif self.age>=31 and self.age<=50:
            self.age_interval =3
        elif self.age>=51 and self.age<=70:
            self.age_interval =4
        else:
            self.age_interval =5
        index = self.age_interval+6*(self.gender_interval)
        self.nut_vector = self.caloric_intake()
        #print(self.nut_vector)
        #print(list(df_ref_class.loc[index]))
        self.nut_vector= (self.nut_vector)+(list(df_ref_class.loc[index]))
        return self.nut_vector



def Sort_Tuple(tup): 
  
    # reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of 
    # sublist lambda has been used 
    tup.sort(key = lambda x: x[1], reverse=True) 
    return tup





@app.route('/')
def index():
    return render_template('test.html')

@app.route('/hello', methods=['POST'])
def hello():
    #df_nutr = pd.read_csv("NutrientData.csv")

    #df_dnutr= df_nutr.drop(['Food Code', 'Food Name'], axis = 1)
    #df_dnutr.apply(pd.to_numeric) #changes entire df to int
    #Initializing User
    gender = request.form['gender']
    weight = request.form['weight']
    height = request.form['height']
    age = request.form['age']
    exercise = request.form['exercise']

    f0 = request.form['food0']
    f1 = request.form['food1']
    f2 = request.form['food2']
    f3 = request.form['food3']
    f4 = request.form['food4']
    f5 = request.form['food5']
    f6 = request.form['food6']
    f7 = request.form['food7']
    f8 = request.form['food8']
    f9 = request.form['food9']
    foodsdata = [f0, f1, f2, f3, f4, f5, f6, f7, f8, f9]
    s0 = request.form['serving0']
    s1 = request.form['serving1']
    s2 = request.form['serving2']
    s3 = request.form['serving3']
    s4 = request.form['serving4']
    s5 = request.form['serving5']
    s6 = request.form['serving6']
    s7 = request.form['serving7']
    s8 = request.form['serving8']
    s9 = request.form['serving9']
    servingsdata = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9]

    #print(request.form)
    #user = person(gender, weight, height, age, exercise) #FEED IN input_gender, input_weight, input_height, input_age, input exercise
    #user_nutr = user.nut_needed()
    df_nutr = pd.read_csv("NutrientData.csv", low_memory = False)
    df_dnutr= df_nutr.drop(['Food Code', 'Food Name'], axis = 1)
    df_dnutr.apply(pd.to_numeric) #changes entire df to int
    df_dnutr.head()

    ### GRAB USER NUTRITION CLASS###
    #df_reference_class = pd.read_csv('UserTable.csv') #csv file that contains nutrition class info
    #input_tuple = request.form()
    #input_tuple = [('gender', 'M'), ('age', '30'), ('weight', '150'), ('height', '69'), ('exercise', 'Light'), ('food0', 'Ackee, canned, drained'), ('serving0', '1'), ('food1', 'Ackee, canned, drained'), ('serving1', '1'), ('food2', 'Ackee, canned, drained'), ('serving2', '1'), ('food3', 'Ackee, canned, drained'), ('serving3', '1'), ('food4', 'Ackee, canned, drained'), ('serving4', '1'), ('food5', 'Ackee, canned, drained'), ('serving5', '1'), ('food6', 'Ackee, canned, drained'), ('serving6', '1'), ('food7', 'Ackee, canned, drained'), ('serving7', '1'), ('food8', 'Ackee, canned, drained'), ('serving8', '1'), ('food9', 'Ackee, canned, drained'), ('serving9', '1'), ('form', 'Submit')]
    #input_dict = dict((x, y) for x, y in input_tuple)
    user = person(gender, weight, height, age,exercise) #FEED IN input_gender, input_weight, input_height, input_age, input exercise

    #self, input_gender, input_weight, input_height, input_age, input_exercise):
    user_nutr_needed = user.nut_needed()
    #print(user_nutr) 

    ### GET USER CONSUMPTION NUTRITION### 
    consumption_matrix = np.zeros(30) 
    
    for i in range (9):
        food_row = df_nutr[df_nutr[  'Food Name' ]  == foodsdata[i] ]
        food_row = food_row.drop(['Food Code', 'Food Name'], axis = 1)

        food_total = (food_row.values)* int( servingsdata[i] )
        consumption_matrix  = np.add(consumption_matrix, food_total)


    user_final_matrix = np.subtract(user_nutr_needed,consumption_matrix) 
    user_final_matrix[user_final_matrix<0] = 0 #change all negatives to 0
    
    ### COMPUTE FOR NUTRITION NEEDED### use np.subtract(A,B)
    #REMEMBER TO CHANGE ALL NEG NUMBERS TO 0 IF USER ATE TOO MUCH

    #test = [1809,79,43,275,23,1363,1481,961,241,162,13,1,0,2103,2,26,130,661,1,0,0,0,0,244,3,26,65,14,13,90] #supposing person has 1 serving of asparagus & 2 servings of beef
    #print(user_final_matrix)

    user_vector = list(user_final_matrix)[0]
    need_mag = round(mag(user_vector),2)
    sim_list= []
    #for entry in df_dnutr.values:
    #  #print(entry)
    #  entry_mag = round(mag(entry),2)
    #  magnitude = round(entry_mag*need_mag, 2)
    #  dotproduct = dot(entry,test)
    #  result = round((dotproduct/magnitude),2)
    #  sim_list.append(result)
    #  if (len(sim_list) >500):
    #    break
    for i in range(2880):
        entry = df_dnutr.values[i]
        #print (entry)
        entry_mag = round(mag(entry),2)
        magnitude = round(entry_mag*need_mag, 2)
        dotproduct = dot(entry,user_vector)
        result = round((dotproduct/magnitude),2)
        sim_list.append ( (i, result) )
        #if (len(sim_list) >500):
        # break
        final_ranked_list = [] #where the final foods will be stored. tuples of cosine sim score + food name.
        ranked_tp = Sort_Tuple(sim_list)

    food_name_1st_term_list = []
    counter_for_final = 0
    k=0
    rec_list = []
    rec_str = ""
    while (counter_for_final < 20):
        x = ranked_tp[k]
        food_name = df_nutr.iloc[x[0],1]
        food_name_1st_term = food_name.split()[0]
        if food_name_1st_term in food_name_1st_term_list: #if food rn is a repeat
            k+=1
            continue
        food_name_1st_term_list.append(food_name_1st_term)
        #print(x[1])
        #print(food_name)
        rec_list.append((x[1],food_name))
        rec_str = rec_str + str(food_name)+" "+ str(x[1]) +' <br> '
        final_ranked_list.append(food_name)
        k+=1
        counter_for_final+=1
    print("Finished Running!")
    result = 'Results: <br/> %s  <br/> <a href="/">Back Home</a>' % (rec_str)
    return result

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000)