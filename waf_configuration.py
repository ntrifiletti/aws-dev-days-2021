import socket
import requests
import json
from http_basic_auth import generate_header, parse_header
import os
import re
import time
from bs4 import BeautifulSoup

waf_ip = os.environ['WAFIP']
waf_password = os.environ['WAFPASSWORD']

print("WAF IP: "+waf_ip)
print("WAF Pass: "+waf_password)
base_url = "http://"+waf_ip+":8000"
admin_url = "http://"+waf_ip+":8000/cgi-mod/index.cgi"
p = re.compile('Please wait while the system starts up')

## Wait for the WAF to come up before trying to send APIs
got_waf = 'no'
i = 1
while i < 30:
    r = requests.get(base_url)
    m = p.search(r.text)
    if m:
        # still provisioning
        print("Still provisioning, sleeping 30...")
        time.sleep(30)
        i = i + 1
    else:
        # Looks like EULA
        r = requests.get(admin_url)
        print("===========LOG==================")
        print(r.text)
        break

i = 1
p = re.compile('Barracuda Product Terms')
while i < 180:
    r = requests.get(base_url)
    m = p.search(r.text)
    if m:
        # Still at EULA
        time.sleep(5)
        print("Still at EULA, sleeping 5 seconds...")
        i = i + 1
        soup = BeautfiulSoup(r.text,'html.parser')
        inputs = soup.find_all('input')
        myformdata = {}
        if inputs:
            for item in inputs:
                myname = item.get('name')
                if myname:
                    myvalue = item.get('value')
                    myformdata[myname] = myvalue
            # submit the form
            #json_data = json.dumps(myformdata)
            print("Form data to submit:")
            print(myformdata)
            myheaders = {'content-type': 'application/x-www-form-urlencoded'}
            postreq = requests.post(base_url,headers = myheaders, data = myformdata)
            print(postreq.text)
            time.sleep(10)
    else:
        # Maybe have admin UI now
        break

i = 1
p = re.compile('Please enter your administrator login and password')
while i < 10:
    r = requests.get(admin_url)
    m = p.search(r.text)
    if m:
        # Yay!
        got_waf = 'yes'
        break
    else:
        # Not yet
        print("Still no admin UI, sleeping 10 seconds...")
        i = i +1

if got_waf == 'no':
    print("FATAL: Never got the WAF admin UI...")
    exit

print("Found WAF login page, sleeping 10 seconds...")
time.sleep(10)
print("Waking up from 10 second nap; proceeding with configuration...")

headers = {"Content-Type": "application/json"}
login_url = "http://"+waf_ip+":8000/restapi/v3.1/login"
login_payload = {"username":"admin", "password":waf_password}
login_request = requests.post(login_url, headers=headers, data=json.dumps(login_payload))
token_output=login_request.text
token_split=token_output.split(":")
token_rstrip=token_split[1].rstrip("}")
token=token_rstrip.replace('"','')
auth_header=generate_header('',token)
api_headers = {"Content-Type":"application/json", "Authorization": auth_header}

#Creating the Service
hostname = socket.gethostname()
server = socket.gethostbyname(hostname)

#Create certificate
certificate_url = "http://"+waf_ip+":8000/restapi/v3.1/certificates/self-signed-certificate"
cert_payload = {
  "state": "CA",
  "key-size": "2048",
  "common-name": "training.petstore.com",
  "city": "San Francisco",
  "organizational-unit": "Training",
  "allow-private-key-export": "Yes",
  "name": "petstore",
  "country-code": "US",
  "key-type": "RSA",
  "elliptic-curve-name": "secp256r1",
  "organization-name": "Barracuda Networks"
}

cert_create_resp = requests.post(certificate_url, headers= api_headers, data=json.dumps(cert_payload))

print(cert_create_resp.text)

service_url = "http://"+waf_ip+":8000/restapi/v3.1/services"

## HTTP-Web Service
svc_payload = {
    "address-version": "IPv4",
    "ip-address": waf_ip,
    "name": "HTTP-Web",
    "port":80,
    "status": "On",
    "type": "HTTP"}

create_svc = requests.post(service_url, data=json.dumps(svc_payload), headers = api_headers)
print(create_svc.text)

## Badstore server, listening on port 8000
svr_url = "http://"+waf_ip+":8000/restapi/v3.1/services/HTTP-Web/servers"
svr_payload = {
    "name": "Badstore-8000",
    "port": 8000,
    "ip-address": server,
    "identifier": "IP Address",
    "address-version": "IPv4"
}
create_svr = requests.post(svr_url, headers = api_headers, data=json.dumps(svr_payload))
print(create_svr.text)

## HTTP-API Service
svc_payload = {
    "address-version": "IPv4",
    "ip-address": waf_ip,
    "name": "HTTP-API",
    "port":8080,
    "status": "On",
    "type": "HTTP"}

create_svc = requests.post(service_url, data=json.dumps(svc_payload), headers = api_headers)
print(create_svc.text)

## Petstore server, listening on port 8080
svr_url = "http://"+waf_ip+":8000/restapi/v3.1/services/HTTP-API/servers"
svr_payload = {
    "name": "Petstore-8080",
    "port": 8080,
    "ip-address": server,
    "identifier": "IP Address",
    "address-version": "IPv4"
}
create_svr = requests.post(svr_url, headers = api_headers, data=json.dumps(svr_payload))
print(create_svr.text)

