name = input("What is your name? ")
import random
adjective = ["cool", "funny", "smart", "kind", "awesome" , "fearless" , "brave", "creative", "talented", "amazing"]
animals = ["cat", "dog", "elephant", "giraffe", "lion", "tiger", "bear", "monkey", "panda", "zebra"]
lucky_number = range(1, 100)
chosen_adjective = random.choice(adjective)
chosen_animal = random.choice(animals)
chosen_lucky_number = random.choice(lucky_number)
print(name +", your codename is :" + chosen_adjective + " " + chosen_animal) 
print("Your lucky number is:" , " ", chosen_lucky_number)