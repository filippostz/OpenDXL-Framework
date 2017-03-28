import sys, getopt,socket,json,os

from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
config = DxlClientConfig.create_dxl_config_from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dxl.conf'))

from dxlclient.message import Event

IP = socket.gethostname()

DXL_MESSAGE = {}

def main(argv):
	TOPIC_DESTINATION = ''
	TYPE_PAYLOAD = ''
	PAYLOAD = ''
	help = 'python ' + sys.argv[0] + ' -t <topic destination> -k <type of payload> -p <payload>'
	
	try:
		opts, args = getopt.getopt(argv,"ht:k:p:",["topic=","typepayload=","payload="])
	except getopt.GetoptError:
		print help
		sys.exit(1)

	for opt, arg in opts:
		if opt == '-h':
			print help
			sys.exit(1)
		elif opt in ("-t", "--topic"):
			TOPIC_DESTINATION = arg
		elif opt in ("-k", "--typepayload"):
			TYPE_PAYLOAD = arg
		elif opt in ("-p", "--payload"):
			PAYLOAD = arg

	if (TOPIC_DESTINATION != '' and PAYLOAD != ''):

		DXL_MESSAGE['SRC_HOST'] = IP
		DXL_MESSAGE['TYPE_PAYLOAD'] = TYPE_PAYLOAD
		DXL_MESSAGE['PAYLOAD'] = PAYLOAD
 
		with DxlClient(config) as client:
			client.connect()
		    	event = Event(TOPIC_DESTINATION)
		    	event.payload = str(json.dumps(DXL_MESSAGE)).encode()
			client.send_event(event)
	else:
		print help
		sys.exit(1)

if __name__ == "__main__":
   main(sys.argv[1:])










