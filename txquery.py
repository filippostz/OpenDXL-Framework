import sys, getopt, json, logging, os

from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
config = DxlClientConfig.create_dxl_config_from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dxl.conf'))

from dxlclient.message import Message, Request

# Configure local logger
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

def main(argv):
	TOPIC_DESTINATION = ''
	PAYLOAD = ''
	help = 'python ' + sys.argv[0] + ' -t <topic destination> -p <payload>'
	
	try:
		opts, args = getopt.getopt(argv,"ht:p:",["topic=","payload="])
	except getopt.GetoptError:
		print help
		sys.exit(1)

	for opt, arg in opts:
		if opt == '-h':
			print help
			sys.exit(1)
		elif opt in ("-t", "--topic"):
			TOPIC_DESTINATION = arg
		elif opt in ("-p", "--payload"):
			PAYLOAD = arg

	if (TOPIC_DESTINATION != '' and PAYLOAD != ''):

            # Create the client
            with DxlClient(config) as client:

                # Connect to the fabric
                client.connect()
                #
                # Invoke the service (send a request)
                #
                # Create the request
                req = Request(TOPIC_DESTINATION)
                # Populate the request payload            
                req.payload = str(PAYLOAD).encode()

                # Send the request and wait for a response (synchronous)
                res = client.sync_request(req)

                # Extract information from the response (if an error did not occur)
                if res.message_type != Message.MESSAGE_TYPE_ERROR:
                    print "result is coming:"
                    print res.payload
                else:
                    logger.error("Error: " + res.error_message + " (" + str(res.error_code) + ")")


	else:
		print help
		sys.exit(1)

if __name__ == "__main__":
   main(sys.argv[1:])
