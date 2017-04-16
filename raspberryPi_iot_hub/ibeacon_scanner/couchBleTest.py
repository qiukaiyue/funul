# test BLE Scanning software
# jcs 6/8/2014

import couchdb
import blescan
import sys
import bluetooth._bluetooth as bluez

couch = couchdb.Server() #default/empty is localhost
db = couch['books']

dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print ("ble thread started")

except:
	print ("error accessing bluetooth device...")
    	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

while True:
	returnedList = blescan.parse_events(sock, 10)
	print ("----------")
	for beacon in returnedList:
		mac = beacon.split(",")[0]
		if mac == "0c:f3:ee:00:eb:ea":
			doc = {'ble_data': beacon}
			db.save(doc)
			print doc
			#print beacon