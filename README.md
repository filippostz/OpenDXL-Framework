# OpenDXL Framework
## Introduction

The OpenDXL Framework is a set of components which brings capabilities to inject, receive and elaborate DXL messages adding fast prototyping capabilities to the existing [McAfee OpenDXL Python Client](https://github.com/opendxl/opendxl-client-python) github project.

![Alt text](https://cloud.githubusercontent.com/assets/24607076/24403564/63ce7e70-13b5-11e7-977f-8de366959385.png "Structure")


**Input Data** injections are made following a standard DXL traffic template and the concept of **DXL_message** is defined as follow:
> **{"TYPE_PAYLOAD": "test", "PAYLOAD": "hello", "SRC_HOST": "client01"}**

To give some traffic regulation, filtering concepts are Built-In and **Filters** can be imported as an Add-On:
> **Filter ( DXL_message )**  

**External services** (ex. VirusTotal) are connected throught **Wrappers** Add-Ons:
> **Wrapper [ Filter ( DXL_message ) ]**  

Every Add-On can provide two different kind of services:
* Answers (ex. VirusTotal URL reputation)
* Actions (ex. Adding rule to the firewall)
> **[ Answer / Action ] = Wrapper [ Filter ( DXL_message ) ]** 

## Use cases

* Fail2Ban [Wiki](https://github.com/filippostz/OpenDXL-Framework/wiki/Fail2Ban)
* VirusTotal [Wiki](https://github.com/filippostz/OpenDXL-Framework/wiki/VirusTotal)
* McAfee WebGateway TODO
* IPfire TODO


## Prerequisites

Python SDK Installation [link](https://opendxl.github.io/opendxl-client-python/pydoc/installation.html)

Certificate Files Creation [link](https://opendxl.github.io/opendxl-client-python/pydoc/certcreation.html)

Provisioning [link](https://opendxl.github.io/opendxl-client-python/pydoc/)

An experimental wizard setup.sh script is also included.


## Framework structure

#### Configuration

> **dxl.conf** : configuration file

#### Certificates and keys

> **client.key** : private key for the client

> **client.crt** : certificate for the client

> **brokercert.crt** : broker certificate

#### Client

> **txquery.py** : send a request to DXL

> **txpublisher.py** : broadcast an information to DXL

#### Server

> **rxservice.py** : service for request and response provider

> **rxnservice.py** : listener for broadcast messages and action runner

#### Add-Ons

> **filter.py** : DXL message filter

> **wrapper.py** : DXL message handler

## Instructions

* #### Run a service for queries/answers requests and send a request from the client (one to one)

This is the typical query/response architecture where a client sends a message pretending an answer.

For example to get the reputation of a website using virusTotal:
Send the website's URL through the DXL fabric with the topic "CHECK/URL/VirusTotal". 

1. Set the variables SERVICE_INPUT, TOPIC_INPUT and WRAPPER inside the script rxservice.py

```clj
SERVICE_INPUT = "/url"
TOPIC_INPUT = SERVICE_INPUT + "/reputation"
FILTER = "clean"
WRAPPER = "virustotal"
```

2. run **rxservice**

```clj
python rxservice.py
```

3. run **txquery -t TOPIC -p PAYLOAD**

```clj
python txquery.py -t /url/reputation -p github.com
```

* #### Run a service for queries/actions requests and broadcast an action request from the client (one to many)

This is the typical query/action architecture where one or more service can receive messages broadcasted to the topic. For example a dxl message containing an IP address can be caught from different services at the same time for different actions.

1. set the variables SERVICE_INPUT, TOPIC_INPUT and WRAPPER inside the script rxnservice.py

```clj
SERVICE_INPUT = "/actions"
TOPIC_INPUT = SERVICE_INPUT + "/event2file"
FILTER = "clean"
WRAPPER = "event2file"
```

2. run **rxnservice**

```clj
python rxnservice.py
```


3. run **txpublisher -t TOPIC -p PAYLOAD**

```clj
python txpublisher.py -t /actions/event2file -p 192.168.0.100
```

## Add-Ons built-in

#### Filter

* Clean - leaves the full message to pass through 
* Payload - filters and leaves only the PAYLOAD pass through 

#### Wrapper

* event2screen - display DXL message 
* event2file - log DXL message in a file with duplication check
* virustotal - url and hash reputation service

#### Create a new service/wrapper Add-On

A Service Add-On is a python script inside the folder "wrappers/example.py"

To create a Service Add-on:

```clj
def action(message):   ;; message variable is the buffer data coming from the dxl fabric
  print message        ;; the main action
  return 1
```

To enable the Service Add-On: set the variable WRAPPER inside the script rxservice.py or rxnservice.py

```clj
WRAPPER = "example"
```
#### Create a new filter Add-On

A Filter Add-On is a python script inside the folder "filters/example.py"

To create a Filter Add-On

```clj
def action(message):   ;; message variable is the buffer data coming from the dxl fabric
  return message + " filtered!"
```

To enable the Filter Add-On: set the variable FILTER inside the script rxservice.py or rxnservice.py

```clj
FILTER = "example"
```


