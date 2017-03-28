OUTPUT_FILE = '/tmp/events.log'

import os.path

def action(message):

	if os.path.exists(OUTPUT_FILE):
		if message not in open(OUTPUT_FILE).read():

			with open(OUTPUT_FILE, "a") as buffer_file:
					message = message + '\n'
    					buffer_file.write(message)
	else:

		with open(OUTPUT_FILE, "a") as buffer_file:
			message = message + '\n'
			buffer_file.write(message)

	return message
