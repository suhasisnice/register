import random

secretNumber = random.randint(1,20)
print("Welcome to the number guessing game!")
print("You have 5 attempts to guess the number I'm thinking of, which is between 1 and 20.")
print("After your second guess, I'll tell you if you're getting warmer or colder.")
print("Enter 0 if you want to exit the game.")
print("Let's begin!")
guessCount = 0
maxGuesses = 5
guess = 0
distance = int
temp = 0
while guessCount<maxGuesses:
    guess = int(input("Enter a number in the range [1, 20] or 0 to exit: "))
    distance=abs(secretNumber-guess)
    # Give the user a clear way to exit the program
    if guess == 0:
        print("CONGRATULATIONSS, YOU MADE IT OUTT! NOW PISS OFF!")
        break

    # Validate the entered value    
    if guess not in range(1, 21):
        print("ARREY, CHOTI BACHHII HO KYAA, READ THE INSTRUCTIONS!!!")
        continue
    if guessCount>=1 and guess != secretNumber:
        if(distance<temp):
            print("Warmer")
        elif(distance==temp):
            print("Same as before")
        else:
            print("Colder")
        print("You're wrong")
    temp=distance

    if guess==secretNumber:
        if(guessCount==0):
            print("Not bad my guy!")
            break
        else:
            print(f"Bro your'e bad at this game you took {guessCount+1} tries")
            break
        print(f"Dude the number was {secretNumber   }")
    guessCount += 1
if(guessCount>6):
    print(f"The secret number was {secretNumber}")