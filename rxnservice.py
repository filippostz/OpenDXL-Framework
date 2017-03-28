SERVICE_INPUT = ""
TOPIC_INPUT = SERVICE_INPUT + "#"
FILTER = "clean"
WRAPPER = "event2screen"

if (TOPIC_INPUT == ' ' or FILTER == '' or WRAPPER == ''):
	print "Please specify the parameters on the file "+ __file__ 
	exit(1)

import os
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
config = DxlClientConfig.create_dxl_config_from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dxl.conf'))

from dxlclient.callbacks import EventCallback

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
    class MyEventCallback(EventCallback):
    	def on_event(self, event):
		logger.info("Event Subscriber - Event received:\n   Topic: %s\n   Payload: %s", event.destination_topic, event.payload.decode())
		wrapper.action(messagefilter.action(event.payload.decode()))
          
    # Wait forever
    logger.info("Adding Event callback function to Topic: %s", TOPIC_INPUT)
    client.add_event_callback(TOPIC_INPUT, MyEventCallback())

        # Wait for DXL Events
    while True:
    	time.sleep(60)



