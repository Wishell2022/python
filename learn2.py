import random

print("Welcome to the guessing game!") 

counts = 3
answer = random.randint(1, 10)

while counts > 0:
    temp = input("enter number: ")
    guess = int(temp)

    if guess == answer:
        print("Congratulations! You guessed the number.")
        break
    else:
        if guess < answer:
            print("Sorry, the number is greater than", guess)
        else:
            print("Sorry, the number is less than", guess)
    counts -= 1

print("Goodbye!")
