Interface TSHOOTER

These scripts can be used to quickly obtain information from a Cisco switch interface while
troubleshooting endpoint connectivity issues.

Script Output:
  - Show interface x/x/x status
  - Show interface x/x/x summary
  - Show mac address-table interface x/x/x
  - Show cdp neighbors x/x/x
  - Show dot1x interface x/x/x
  - Show authentication sessions interface x/x/x
  - Show run interface x/x/x

To run the script you will need the last four of the endpoints MAC-Address and the switch IP it's connected on.

To run:
  1. Open a cmd promt where tshoot_w-mac.py or tshoot_w-mac.exe are located.
  2. Run the command with the desired target vairables:
    .py   - C:\Desktop\tshoot_w-mac.py  -ip 10.0.0.2 -mac ab12
    .exe  - C:\Desktop\tshoot_w-mac.exe -ip 10.0.0.2 -mac ab12
     help - C:\Desktop\tshoot_w-mac.exe --help
  
  3. Hit enter and the script will start by verifying the mac-address is stored in the address table
    and is directly connected to the target switch. 
     - IF one of these test fail the script will print the reason for halting the script.
     - If both test pass you will be show the target paramaters and asked for Y/N input to continue.
  
  
I have included a working executible file or you can create your own. This lets you run the script run on any computer. 
I sent this version to our helpdesk as they don't always have a python environment setup to run these scripts. 
For help withcreating an .exe file from .py see the links below:
  - Auto PY to EXE - https://pypi.org/project/auto-py-to-exe/
  - Auto PY to EXE Tutorial - https://youtu.be/OZSZHmWSOeM
