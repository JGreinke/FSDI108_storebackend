def say_name (first,last):
    print (first + " " + last)

def test_dict():
    print("--------Dictionary---------")

    me = {
        "first" : "Jasmine",
        "last" : "Greinke",
        "age" : 29, 
        "hobbies" : [], 
        "address" : {
            "street" : "Booker TRL",
            "city" : "San Antonio"
        }
    }

    print (me["first"] + " " + me["last"])
    print (me["address"])
    
    address = me["address"]
    print(address["street"] + " " + address["city"])

def youngest_person():
    ages = [12,42,32,50,56,14,78,30,51,89,12,38,67,10]
    pivot = ages[0]
    for num in ages:
        if num < pivot:
            pivot = num
    print(f"The result is: {pivot}")

say_name("Jasmine", "Greinke")
test_dict()
youngest_person()