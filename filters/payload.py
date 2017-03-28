import json

def action(message):
	
    try:

    	filtered = json.loads(message)
	filtered = str(filtered['PAYLOAD'])

    except:
	
	filtered = ""

    return filtered

