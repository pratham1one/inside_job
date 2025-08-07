number = int(input("Enter a number: "))

match number:
    case 0:
        print("The number is zero.")
    case _ if number % 2 == 0:
        print("The number is even.")
    case _:
        print("The number is odd.")
print("khel khatam hai lala")
