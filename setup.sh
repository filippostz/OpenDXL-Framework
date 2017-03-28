COUNTRY="IE"
STATE="Cork"
CITY="Cork"
ORGANIZATION="example"
ORGANIZATIONUNIT="exampleoffice"
ORGANIZATIONUNITCA="exampleofficeca"
COMMONNAME="office"

VERSION="dxlclient-python-sdk-3.0.1"

LIMIT="----------------------------------------------------------------------------------------------------------------"

wget https://github.com/opendxl/opendxl-client-python/releases/download/3.0.1.181/$VERSION.zip

unzip $VERSION.zip >> /dev/null

unzip $VERSION/lib/*zip >> /dev/null

mv dxlclient*/dxlclient .

mkdir ca

echo "certificate authority (CA) creation:"

openssl req -new -x509 -days 365 -extensions v3_ca -keyout ca/ca.key -out ca/ca.crt -subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORGANIZATION/OU=$ORGANIZATIONUNIT/CN=$COMMONNAME"

echo "Generate a Private Key for the client:"

openssl genrsa -out certs/client.key 2048

echo "Create a Certificate Signing Request (CSR) for the client:"

openssl req -out certs/client.csr -key certs/client.key -new -subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORGANIZATION/OU=$ORGANIZATIONUNITCA/CN=$COMMONNAME"

echo "Sign the Certificate Signing Request (CSR):"

openssl x509 -req -in certs/client.csr -CA ca/ca.crt -CAkey ca/ca.key -CAcreateserial -out certs/client.crt -days 365

rm -r dxlclient-*

echo $LIMIT

echo "ePO Certificate Authority (CA) Import: https://opendxl.github.io/opendxl-client-python/pydoc/epocaimport.html"

echo $LIMIT

echo "ePO Broker Certificates Export: https://opendxl.github.io/opendxl-client-python/pydoc/epobrokercertsexport.html"

echo $LIMIT

echo "ePO Broker List Export: https://opendxl.github.io/opendxl-client-python/pydoc/epobrokerlistexport.html"

echo $LIMIT
