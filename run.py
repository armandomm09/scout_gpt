import base64
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai
from gpt_assistant.openai_api import chat_with_gpt
from gpt_assistant.new_vector_file_question import chatWithNewFile
import json
import gzip
from gpt_assistant.stored_files_question import chatWithStoredFile

# scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# creds = ServiceAccountCredentials.from_json_keyfile_name('scoutcredentials.json', scope)

# client = gspread.authorize(creds)

# sheets = client.open('Imperator pitscout database hermosillo')

# sheet = sheets.get_worksheet(0)

# data_range = sheet.get_all_values()

# # Convertir los datos a un formato que se pueda escribir en un archivo JSON
# headers = data_range[0]
# rows = data_range[1:]
# data_dict = [dict(zip(headers, row)) for row in rows]

# # Convertir los datos a JSON
# json_data = json.dumps(data_dict)


# with open('scouted_teams.json', 'w') as f:
#       f.write(json_data)

if len(sys.argv) > 1:
    question = sys.argv[1]
else:
    question = "Que chasis tiene lambot?"


chatWithStoredFile(question)

