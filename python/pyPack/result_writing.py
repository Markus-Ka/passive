import os


def check_existing_result(result):
    """ 
    Checks if the result file exists, picks correct number if it does and then sends the data and number to write
    """
    
    numeration = 1
    if not os.path.exists("result.txt"):
        numeration =""
    else: 
        while os.path.exists(f"result{numeration}.txt"):
            numeration += 1
    
    save_result(result, numeration)

def save_result(result, numeration):
    with open(f"result{numeration}.txt", "w") as file:
        file.write(result)
        print(f"Saved in result{numeration}.txt")