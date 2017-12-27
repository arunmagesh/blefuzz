import time
import threading
import binascii
import pygatt
import copy
import re
from random import *
from bluetooth.ble import DiscoveryService
service = DiscoveryService()
devices = service.discover(5)
adapter = pygatt.GATTToolBackend()

def print_menu():       ## Menu
    print 30 * "-" , "Welcome to Simple BLE fuzzer" , 30 * "-"
    print "1. Scan for all BLE devices"
    print "2. View all characteristics"
    print "3. Random fuzz"
    print "4. Sequential fuzz"
    print "5. Exit"
    print 67 * "-"
  
loop=True      
  
while loop:          ## While loop which will keep going until loop = False
    print_menu()    ## Displays menu
    choice = input("Enter your choice [1-5]: ")

    if choice==1:     ## Choice 1 to start the BLE scan and display it
        print "Scanning"
        start = time.time()
        while time.time() < start + 5:
            for address, name in devices.items():
                print("Address: {}".format(address))  # Print the address
                time.sleep(0.5)   ##Wait for a bit

    elif choice==2:
        print "Enter the BD address"
        mac=raw_input('>>')  # BD adress
        adapter.start() #BT adapter start
        while True:  ## connecting to the device using random addressing
            try:
                device = adapter.connect(mac, timeout=1, address_type=pygatt.BLEAddressType.random)
                break
            except pygatt.exceptions.NotConnectedError:
                print('Waiting...')
        for uuid in device.discover_characteristics().keys():   ## display UUID and Handle
            print("UUID--> %s | Handle --> 0x%s" %(uuid,hex(device.get_handle(uuid)).split('x')[-1].zfill(4)))
        adapter.stop() # closing bt adapter

    elif choice==3:  # Random Fuzz
        mac=raw_input('Enter the BD address>>')  # getting user data
        hnd=raw_input('Enter the Handle to S.Fuzz:>>')
        ite=raw_input('Enter the number of iterations:>>')
        print('Enter all the 20 bytes you want to write')
        data = []
        print("Enter data for fixed and [ for random fuzzing")

        for i in range(0, 20):  # Getting 20 byte data
            print("[%d]"%(i))
            x = raw_input('>>')
            data.append(x)

        print(data)
        adapter.start()#BT adapter start
        while True:  ## connecting to the device using random addressing
            try:
                device = adapter.connect(mac, timeout=1, address_type=pygatt.BLEAddressType.random)
                break
            except pygatt.exceptions.NotConnectedError:
                print('Waiting...')

        for i in range(0,int(ite)+1):  #Iteration loop
            data1 = copy.copy(data)  # making a temp copy of the list
            for j in range(0,20):
                if data1[j] == '[':
                    data1[j] = hex(randint(1, 255)).split('x')[-1]  # selecting [ and randomizing it
            sent_str = ''.join(data1)  # concatinate into a string
            print("%s>>%s " %(i,sent_str))  # print data
            print("char-write-req %s %s'" %(str(hnd),str(sent_str)))
            adapter.sendline("char-write-req %s %s" %(str(hnd),str(sent_str)))  # gatt write command
            time.sleep(.3) 
            data1 = copy.copy(data) # recopy the orginal list
        adapter.stop() # closing bt adapter
            
    elif choice==4: 
        mac=raw_input('Enter the BD address>>')  # user input stuff
        hnd=raw_input('Enter the Handle to S.Fuzz:>>')
        ite=raw_input('Enter the number of iterations:>>')
        print('Enter all the 20 bytes you want to write')
        data = []
        print("Enter data for fixed and [ for Sequential fuzzing")

        for i in range(0, 20):  # Getting 20 byte data
            print("[%d]"%(i))
            x = raw_input('>>')
            data.append(x)

        print(data)  #log
        adapter.start()
        while True:   ## connecting to the device using random addressing
            try:
                device = adapter.connect(mac, timeout=1, address_type=pygatt.BLEAddressType.random)
                break
            except pygatt.exceptions.NotConnectedError:
                print('Waiting...')

        for i in range(0,int(ite)): #Iteration loop
            data1 = copy.copy(data) # making a temp copy of the list 
            for j in range(0,20):
                if data1[j] == '[':
                   data1[j] = chr(i).encode('hex') # selecting [ and incrementing  it
            sent_str = ''.join(data1)   # concatinate into a string
            print("%s>>%s " %(i,sent_str))   # Print data
            adapter.sendline("char-write-req %s %s" %(str(hnd),str(sent_str))) # gatt write command
            time.sleep(.3)
            data1 = copy.copy(data) # recopy the orginal list

        adapter.stop()  # closing bt adapter
    elif choice==5:
        print "Exiting...."
        loop=False 
    else:
        # Any integer inputs other than values 1-5 we print an error message
        raw_input("Wrong option selection. Enter any key to try again..")
