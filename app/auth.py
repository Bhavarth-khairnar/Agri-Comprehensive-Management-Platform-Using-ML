import re



#                                             Authenticate User                                            #
############################################################################################################
def name_valid(name):
    if name.isalpha() and len(name) > 1:
        return True
    else:
        return False

def password_valid(pass1):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
	
	# compiling regex
    pat = re.compile(reg)
	
	# searching regex				
    mat = re.search(pat, pass1)
	
	# validating conditions
    if mat:
        return True
    else:
        return False

def password_check(password1, password2):
    if password1 == password2:
        return True
    else : 
        return False

def contact_valid(number):
    Pattern = re.fullmatch("[6-9][0-9]{9}",number)
    if Pattern != None:
        return True
    else:
        return False

def authentication(first_name, last_name, pass1, pass2, phone_number):
    if name_valid(first_name) == False:
        return "Invalid First Name"           
    elif name_valid(last_name) == False:
            return "Invalid Last Name"
    elif contact_valid(phone_number) == False:
            return "Invalid Phone Number"
    elif password_valid(pass1) == False:
        return "Password Should be in Proper Format. (eg. Password@1234)"
    elif password_check(pass1, pass2) == False:
        return "Password Not Matched"
    else:
        return "success"

#                                            Authenticate Input                                            #
############################################################################################################
# Validators
def farmer_name_valid(full_name):
    return bool(full_name) and all(ch.isalpha() or ch.isspace() for ch in full_name)


def contact_valid(contact_no):
    return contact_no.isdigit() and len(contact_no) == 10


def ratio_valid(ratio):
    try:
        return 0 <= int(ratio) <= 100
    except:
        return False


def percentage_valid(percent):
    try:
        return 0 <= float(percent) <= 100
    except:
        return False


def ph_valid(pH):
    try:
        return 0 <= float(pH) <= 14
    except:
        return False


def rainfall_valid(mm):
    try:
        return float(mm) >= 0
    except:
        return False
    

def soil_type_valid(soil_type):
    allowed_soils = ["loamy", "sandy", "clayey", "black", "red"]
    return soil_type.lower() in allowed_soils


def season_valid(season):
    allowed_season = ["kharif", "rabi", "zaid", "perennial"]
    return season.lower() in allowed_season


def region_valid(region):
    allowed_region = ["nashik", "konkan", "vidarbha", "west bengal"]
    return region.lower() in allowed_region
        

def input_verification(
    farmer_name, contact_no,
    n, p, k,
    temperature, humidity, ph, rainfall,
    soil_type, season, region
):
    if not farmer_name_valid(farmer_name):
        return "Invalid Farmer Name"

    elif not contact_valid(contact_no):
        return "Invalid Contact Number"

    elif not ratio_valid(n):
        return "Invalid ratio of Nitrogen content in soil"

    elif not ratio_valid(p):
        return "Invalid ratio of Phosphorous content in soil"

    elif not ratio_valid(k):
        return "Invalid ratio of Potassium content in soil"

    elif not percentage_valid(temperature):
        return "Invalid Temperature Value"

    elif not percentage_valid(humidity):
        return "Invalid Humidity Percentage"

    elif not ph_valid(ph):
        return "Invalid pH Value"

    elif not rainfall_valid(rainfall):
        return "Invalid Rainfall (in mm)"

    elif not soil_type_valid(soil_type):
        return "Invalid Soil Type"

    elif not season_valid(season):
        return "Invalid Season"

    elif not region_valid(region):
        return "Invalid Region"

    else:
        return "Success"


def input_verification1(farmer_name, n, p, k, temperature, humidity,):
    if farmer_name_valid(farmer_name) == False:
        return "Invalid Farmer Name"
    elif ratio_valid(n) == False:
        return "Invalid ratio of Nitrogen content in soil"
    elif ratio_valid(p) == False:
        return "Invalid ratio of Phosphorous content in soil"
    elif ratio_valid(k) == False:
        return "Invalid ratio of Potassium content in soil"
    elif percentage_valid(temperature) == False:
        return "Invalid Temperature Value"
    elif percentage_valid(humidity) == False:
        return "Invalid Humidity Pecentage"
    else:
        return "Success"