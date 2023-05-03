from datetime import datetime, timedelta
import requests
import os
import time
import json
import pandas as pd

UID = input("\033[0;35mUID: \033[0m")
SECRET = input("\033[0;35mSECRET: \033[0m")
headers = {'Content-type':'application/json'}
r = requests.post(f"https://api.intra.42.fr/oauth/token?grant_type=client_credentials&client_id={UID}&client_secret={SECRET}", headers=headers)
access_token = r.json()['access_token']

# Bloc manages coalitions for each campus
campus_id = 34
# Cadet coalition
bloc_id = 50
# Default coalition (RED & BLUE)
bloc_id_2 = 41
# coalition_name & coalition_id paring
coalitions = {
	"kernel":183,
	"seg":182,
	"unix":181,
	"bug": 180,
    "red": 147,
	"blue": 148
}
extra_id = [147, 148]
extra_name = ["RED", "BLUE"]

coalitions_id = [180, 181, 182, 183]
coalitions_name = ["BB", "UU", "SS", "KK"]
def get_all_coalitions(coalition_id, file_name="untitled"):
    i = 1
    tol = 100
    full_list = []
    while tol == 100:
        url = f"https://api.intra.42.fr/v2/coalitions/{coalition_id}/coalitions_users?per_page=100&page={i}&access_token={access_token}"
        response = requests.get(url)
        full_list += response.json()
        tol = len(response.json())
        i += 1
    with open(f"{file_name}.json","w") as f:
        f.write(json.dumps(full_list))
    print(f"\033[0;33mCOALITION {coalition_id} GENERATED\033[0m")

# # Run this to get all users in each coalition
# for i in range(len(coalitions_id)):
#       get_all_coalitions(coalition_id[i], coalitions_name[i])

def check_user_in_coalition(coalition_name, user_id):
    with open(f"{coalition_name}.json", "r") as f:
         coalition_file = json.loads(f.read())
    for c in coalition_file:
        if (c["user_id"] == user_id):
            return (coalition_name)
    return None

def generate_list(file_name="untitled"):
    # Require a json of all cadets
	with open("cadets.json", "r") as f :
		cadets = json.loads(f.read())
	full_list = []
	for cadet in cadets:
		user = {}
		user["id"] = cadet["id"]
		user["intra_id"] = cadet["login"]
		user["intra_full_name"] = cadet["usual_full_name"].upper()
		user["intra_url"] = cadet["url"]
		user["batch"] = datetime.strptime(cadet["cursus_users"][1]["begin_at"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d/%m/%Y")
		user["coalition"] = "NO TEAM"
		for coalition in coalitions_name:
			temp = check_user_in_coalition(coalition, cadet["id"])
			if (check_user_in_coalition(coalition, cadet["id"]) != None):
				user["coalition"] = coalition
				break
		full_list.append(user)
		
	with open(f"{file_name}.json", "w") as f:
		f.write(json.dumps(full_list))
	data = pd.DataFrame.from_dict(full_list)
	data.to_excel(f"{file_name}.xlsx", index=False)

# Specify filename to generate list
generate_list("coalition_list")