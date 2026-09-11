import random

secret = random.randint(1,100)
while True:
    try:
        choice = int(input("Enter an integer in the range of 1 to 100 :  "))
        if (choice>0 and choice<100):
            placeholder = 0 

        else:
            print("Number must be in the range of 1 to 100 please check again!!")
    except:
        print("Invalid Input, choice entered must be an integer !!!")
        
    
#if number is greater than generated number we say too high and too low for the opposite
