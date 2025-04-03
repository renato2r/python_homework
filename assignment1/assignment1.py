# Write your code here.

#-------------Task1-------------------#
def hello():
    test = "Hello!"
    return test
print(hello())

#-------------Task2------------------#
def greet(name):
    return f'Hello, {name}!'
greet('James')

#------------Task3-------------------#
def calc(arg1,arg2,arg3="multiply"):
    result = 0
    try:
        match arg3:
            case "add":
                result = arg1 + arg2
            case "subtract":
                result = arg1 - arg2
            case "divide":
                result = arg1 / arg2
            case "modulo":
                result = arg1 % arg2
            case "int_divide":
                result = arg1 // arg2
            case "power":
                result = arg1 ** arg2
            case _:
                result = arg1 * arg2
            
        return result
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return "You can't multiply those values!"
    except Exception as e:
        return f"An error ocurred {e}"

print(calc(10,20,"divide"))

#------------Task4-------------------#
def data_type_conversion(value,dataType):
    try:
        
        match dataType:
            case "float":
                result = float(value)
            case "str":
                result = str(value)
            case "int":
                result = int(value)
            case _:
                return "Invalid data type!"
        return result
    except ValueError:
        return f"You can't convert {value} into a {dataType}."
    except Exception as e:
        return f"An error ocurred {e}"

print(data_type_conversion(10,"float"))
    
#------------Task5-------------------#

def grade(*args):
    try:
        total = 0
        avg = 0
        qtdArgs = len(args)
        for num in args:
            total += num
        #print (f'Total {total}')
        avg = total/qtdArgs
        #print (avg)
        if(avg >= 90):
            return 'A'
        elif(avg >= 80 and avg <=89):
            return 'B'
        elif(avg >=70 and avg <=79):
            return 'C'
        elif(avg >=60 and avg <=69):
            return 'D'
        elif(avg <= 60):
            return 'F'
        return avg
    except Exception as e:
        return 'Invalid data was provided.'

print(grade(19,29,400))
        
#------------Task6-------------------#

def repeat(string, count):
    i=0
    result = ""
    while i < count:
        result += string
        i += 1
    return result

print(repeat('hello',3))
        
#------------Task7-------------------#

def student_scores(arg1, **kwargs):
    if not kwargs:
        return "No scores provided"
    
    if(arg1 == 'best'):
        return max(kwargs, key=kwargs.get)
    elif(arg1 == 'mean'):
        return sum(kwargs.values()) / len(kwargs)
    else:
        return "Invalid mode. Use 'best' or 'mean'."

#------------Task8-------------------#

def titleize(text):
    little_words = {"a", "on", "an", "the", "of", "and", "is", "in"}  
    words = text.lower().split()  
    
    for i, word in enumerate(words):
        if i == 0 or i == len(words) - 1 or word not in little_words:
            words[i] = word.capitalize()  

    return " ".join(words)  


print(titleize("the lord of the rings")) 

#------------Task9-------------------#

def hangman(secret,guess):
    result = ""
    for letter in secret:
        if letter in guess:
            result += letter
        else:
            result +="_"
    return result
   
print(hangman('alphabet','ab'))
    
#------------Task10-------------------#
def pig_latin(text):
    vowels = "aeiou"
    words = text.split()
    result = []
    
    for word in words:
        if word[0] in vowels:
            result.append(word + "ay")
        else:
            i = 0
            while i < len(word) and word[i] not in vowels:
                if word[i:i+2] == "qu":  # Se encontrar "qu", trata como uma unidade
                    i += 2
                    break
                i += 1
            result.append(word[i:] + word[:i] + "ay")
    
    return " ".join(result)

# Testes
print(pig_latin("hello world"))  