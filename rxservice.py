SERVICE_INPUT = "/test"
TOPIC_INPUT = SERVICE_INPUT + "/event2file"
FILTER = "clean"
WRAPPER = "event2file"

if (SERVICE_INPUT == '' or TOPIC_INPUT == ' ' or FILTER == '' or WRAPPER == ''):
	print "Please specify the parameters on the file "+ __file__ 
	exit(1)

import os
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
config = DxlClientConfig.create_dxl_config_from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dxl.conf'))

from dxlclient.message import ErrorResponse, Response

from dxlclient.callbacks import RequestCallback
from dxlclient.service import ServiceRegistrationInfo
import importlib 
import time
import logging

# Enable logging, this will also direct built-in DXL log messages.
log_formatter = logging.Formatter('%(asctime)s %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

# Configure local logger
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

print "TOPIC INPUT:" + TOPIC_INPUT

messagefilter = importlib.import_module("filters." + FILTER)
wrapper = importlib.import_module("wrappers." + WRAPPER)

with DxlClient(config) as client:

    client.connect()   
    class DxlService(RequestCallback):
        def on_request(self, request):
            try:
                query = request.payload.decode()
                logger.info("Service received request payload: " + query)
                response = Response(request)
                response.payload = str(wrapper.action(messagefilter.action(query))).encode()
                client.send_response(response)
                print response

            except Exception as ex:
                print str(ex)
                client.send_response(ErrorResponse(request, error_message=str(ex).encode()))

    info = ServiceRegistrationInfo(client, SERVICE_INPUT)
    info.add_topic(TOPIC_INPUT, DxlService())
    # Register the service with the fabric (wait up to 10 seconds for registration to complete)
    client.register_service_sync(info, 10)
    logger.info("Service is running on topic: " + TOPIC_INPUT)

    # Wait forever
    while True:
    	time.sleep(60)



