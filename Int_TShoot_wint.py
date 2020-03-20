parser.add_argument("-int", "--interface", help="Enter the interface ID")
args = parser.parse_args()
device_ip = args.router_ip
target = args.interface


 Uses the target network devices IP address and the last four characters of an endpoints MAC-Address
# Used when the switches IP and the last for characters of users PC are known.

import argparse
from netmiko import Netmiko
from getpass import getpass
from ciscoconfparse import CiscoConfParse
import os
import time
import netmiko

# Add arguments as variables when running script from a console.
parser = argparse.ArgumentParser()
parser.add_argument("-ip", "--router_ip", help="Enter the target devices IP address. I.E: /Downloads>tshoot_w-mac.exe -ip x.x.x.x -mac aaaa")
parser.add_argument("-int", "--interface", help="Enter the interface ID")
args = parser.parse_args()

# Create objects from arguments collected when running script.
device_ip = args.router_ip
target = args.interface

# Creates get_input as object to prompt for username.
def get_input(prompt=''):
    try:
        line = input(prompt)
    except NameError:
        line = input(prompt)
    return line

username = get_input('Enter Username: ')
password = getpass()

netmiko_exceptions = (netmiko.ssh_exception.NetMikoAuthenticationException,
                      netmiko.ssh_exception.NetMikoTimeoutException,
                      TimeoutError,)




my_device = {
    "host": device_ip,
    "username": username,
    "password": password,
    "device_type": "cisco_ios",
}

try:
    net_connect = Netmiko(**my_device)                           # Connect to device
    hostname = net_connect.base_prompt
    mac_tbl = net_connect.send_command('sh mac address-table | i ' + macaddr)
    sh_mac = 'sh_mac.txt'

    # Checks that mac-address can be found in the targets mac-table.
    # If mac_tbl returns with a len other than 0, the script will move to the next check.
    print(' * Verifying (' + macaddr + ') is in (' + hostname +') mac table.')
    time.sleep(2)
    mac_tbl
    if len(mac_tbl) == 0:
        print('- Warning:(' + macaddr + '), was not found in (' + hostname + '), mac-address table.')
        time.sleep(2)
        print('  * Please try again with a new target IP and/or MAC address *')
        time.sleep(2)
        print('   - Your target device was: ' + hostname + ' at ' +device_ip)
        time.sleep(2)
        print('   - Your target MAC-Address was: ' +macaddr)
        time.sleep(2)
        print(' Closing connection to: ' + hostname)
        time.sleep(2)
        net_connect.disconnect()
    # Checks that the interface found in the previous check is not a trunk.
    # Check is performed by doing a show run and checking for 'switchport mode trunk'
    # If the port is not a trunk it moves to the next step.
    else:
        with open(sh_mac, 'a') as f:
            print((mac_tbl), file=f)
        print('   - (' + macaddr + ') was found in (' + hostname + '), mac-address table.')

        parse = CiscoConfParse('.\\sh_mac.txt')
        obj = parse.find_objects(r'[GT]\S\S\S\S\S\S\S?')[0]
        mac_int = obj.re_match_typed(r'([GT]\S\S\S\S\S\S\S?)')
        sh_run = 'sh_trunk.txt'
        sh_run_int = net_connect.send_command("show run int " + mac_int)

        with open(sh_run, 'a') as z:
            print((sh_run_int), file=z)

        parse2 = CiscoConfParse('.\\sh_trunk.txt')
        obj2 = parse2.find_lines(r'(switchport mode trunk)')

        time.sleep(1)
        print(' * Verifying (' + macaddr + ') is directly connected to ' + hostname)

        # obj2 should be blank.
        # If obj2 is not blank a warning will print to the user.
        # If obj2 is blank, will prompt for user input to continue.
        if obj2 == []:
            time.sleep(2)
            print('  - (' + macaddr + ') is attached to interface (' + mac_int + ') ')
            time.sleep(1)
            answer = input('  - Would you like to continue? Press Y for YES and N for NO. ')
            if answer == 'y':
                sh_int_status = net_connect.send_command("sh interfaces " + mac_int + ' status')
                sh_int_sum = net_connect.send_command("sh interfaces " + mac_int + ' summary')
                sh_mac_int = net_connect.send_command("sh mac address-table interface " + mac_int)
                sh_cdp = net_connect.send_command("sh cdp neighbors " + mac_int)
                sh_dot1x = net_connect.send_command("sh dot1x interface " + mac_int)
                sh_session = net_connect.send_command("sh authentication sessions interface " + mac_int)
                sh_run_int = net_connect.send_command("show run int " + mac_int)
                print(' ')
                print(' ')
                print('----')
                print('Output from:# Show interface ' + mac_int + ' status:')
                print(sh_int_status)
                print('----')
                print(' <---> ')
                print('----')
                print('Output from:# Show interface ' + mac_int + ' summary:')
                print(sh_int_sum)
                print('----')
                print(' <---> ')
                print('----')
                print('Output from:# Show mac address-table interface ' + mac_int)
                print(sh_mac_int)
                print('----')
                print(' <---> ')
                print('----')
                print('Output from:# Show cdp neighbors ' + mac_int)
                print(sh_cdp)
                print('----')
                print(' <---> ')
                print('----')
                print('Output from:# Show dot1x interface ' + mac_int)
                print(sh_dot1x)
                print('----')
                print(' <---> ')
                print('----')
                print('Output from:# Show authentication sessions interface ' + mac_int)
                print(sh_session)
                print('----')
                print(' <---> ')
                print('----')
                print('Output from:# Show run interface ' + mac_int)
                print(sh_run_int)
                print('----')
                print('*Terminating connection to ' +hostname+'* ')
                print('----')
                net_connect.disconnect()
                os.remove('.\\sh_trunk.txt')
                os.remove('.\\sh_mac.txt')
            # Will run if the user presses 'n'
            elif answer == 'n':
                print('Closing connection to device.')
                time.sleep(1)
                net_connect.disconnect()
                os.remove('.\\sh_trunk.txt')
                os.remove('.\\sh_mac.txt')
        # Will run if "show run" returns with "switchport mode trunk."
        else:
            time.sleep(3)
            print(' ! Warning: (' + macaddr + ') was learned from a trunk port and is not directly connected to your target, (' + hostname + ') at (' + device_ip + ')')
            time.sleep(2)
            print('   - Closing connection with ' + hostname)
            time.sleep(2)
            net_connect.disconnect()
            os.remove('.\\sh_trunk.txt')
            os.remove('.\\sh_mac.txt')
# Will run if there is an error.
except netmiko_exceptions as error:
    time.sleep(1)
    print(' * SSH failed to your target at (' + device_ip + ')')
    print('  - Please check the target IP address and try again')
    time.sleep(2)
