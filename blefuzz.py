## Text menu in Python
from bluetooth.ble import DiscoveryService
import time
from random import *
import threading
service = DiscoveryService()
devices = service.discover(5)
import binascii
import pygatt

def print_menu():       ## Your menu design here
    print 30 * "-" , "Welcome to Simple BLE fuzzer" , 30 * "-"
    print "1. Scan for all BLE devices"
    print "2. View all characteristics"
    print "3. Sequential"
    print "4. Random"
    print "5. Exit"
    print 67 * "-"
  
loop=True      
  
while loop:          ## While loop which will keep going until loop = False
    print_menu()    ## Displays menu
    choice = input("Enter your choice [1-5]: ")
     
    if choice==1:     
        print "scanning"
        start = time.time()
        while time.time() < start + 5:
            for address, name in devices.items():
                print("Name: {} | Address: {}".format(name, address))
                time.sleep(1)

        ## You can add your code or functions here
    elif choice==2:
        print "Enter the MAC"
        mac=raw_input('>>')
        adapter = pygatt.GATTToolBackend()
        adapter.start()
        while True:  
            try:
                device = adapter.connect(mac, timeout=1, address_type=pygatt.BLEAddressType.random)
                break
            except pygatt.exceptions.NotConnectedError:
                print('Waiting...')

        for uuid in device.discover_characteristics().keys():
            print("Read UUID %s" % (uuid))
        ## You can add your code or functions here
    elif choice==3:
        print "Menu 3 has been selected"
        ## You can add your code or functions here
    elif choice==4:
        print "Menu 4 has been selected"
        ## You can dad your code or functions here
    elif choice==5:
        print "Menu 5 has been selected"
        ## You can add your code or functions here
        loop=False # This will make the while loop to end as not value of loop is set to False
    else:
        # Any integer inputs other than values 1-5 we print an error message
        raw_input("Wrong option selection. Enter any key to try again..")
