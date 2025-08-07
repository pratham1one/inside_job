grade = input("Enter your grade (A, B, C, D, F): ").upper()

match grade:
    case "A":
        print("ohoo topper!")
    case "B":
        print("Good job!")
    case "C":
        print("You passed.")
    case "D":
        print("Needs improvement.")
    case "F":
        print("Fail ho gaya hehehe gandu.")
    case _:
        print("Invalid grade entered.")
