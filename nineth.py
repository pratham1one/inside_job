day_number=int(input("enter a number (1-7): "))

match day_number:
    case 1:
        print("monday")
    case 2:
        print("tuesday")
    case 3:
        print("wednesday") 
    case 4:
        print("thursday")
    case 5:
        print("friday")
    case 6:
        print("saturday")
    case _:
        print("Invalid number! please write the number between 1 and 7.")                       
 