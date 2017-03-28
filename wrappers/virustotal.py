# The API key for invoking the Virus Total service
#_______________________________________________________________________________________
VIRUS_TOTAL_API_KEY = ''
#_______________________________________________________________________________________


import requests
import re

def ishash(buffer):
	if not re.findall(r"([a-fA-F\d]{32})", buffer):
		return 0
	else:
		return 1

def action(message):

	if ishash(message):
		type = 'file'
	else:
		type = 'url'

	PARAMS = {'apikey': VIRUS_TOTAL_API_KEY, 'resource': message}
	HEADERS = {"Accept-Encoding": "gzip, deflate","User-Agent" : "-"}
	try:
		response = requests.get('https://www.virustotal.com/vtapi/v2/' + type + '/report',params=PARAMS, headers=HEADERS)
		result = response.json()
		return str((result["positives"] * 100 )/result["total"]) + " %"

	except:
		return 0







