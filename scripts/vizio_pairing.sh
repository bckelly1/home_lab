#!/bin/bash

VIZIO_IP="192.168.2.20"
VIZIO_PORT="7345"

curl -k -H "Content-Type: application/json" -X PUT -d '{"DEVICE_ID":"pyvizio","DEVICE_NAME":"Python Vizio"}' https://${VIZIO_IP}:${VIZIO_PORT}/pairing/start

read -p "PIN:  " VIZIO_PIN
read -p "PAIRING_REQ_TOKEN:  " VIZIO_PAIRING_REQ_TOKEN

curl -k -H "Content-Type: application/json" -X PUT -d '{"DEVICE_ID": "pyvizio","CHALLENGE_TYPE": 1,"RESPONSE_VALUE": "'"${VIZIO_PIN}"'","PAIRING_REQ_TOKEN": '"${VIZIO_PAIRING_REQ_TOKEN}"'}' https://${VIZIO_IP}:${VIZIO_PORT}/pairing/pair
