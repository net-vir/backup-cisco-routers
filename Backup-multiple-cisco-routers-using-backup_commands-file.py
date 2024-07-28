# import the required libraries
from netmiko import ConnectHandler
from datetime import datetime
import getpass
import time
import threading
#import logging


start = time.time()
# below variable will be used to store the password enter by user
passwd = getpass.getpass("Enter the password: ")

# Below code block is used to retrieve the device information/IPs from a text file
with open('Device-list') as file1:
    devices = file1.read().splitlines()

# Below code block is used to retrieve the multiple commands from a file
with open('Backup-commands') as file2:
    commands = file2.read().splitlines()

# Below code block is creating a new function which will be called in the for loop to execute
def backup(cisco_device):
    connection = ConnectHandler(**cisco_device)
    all_commands = []
    for run in commands:
        output = connection.send_command(run)
        all_commands.append(f'\n Output for "{run}": \n{output}\n')
    prompt = connection.find_prompt()
    hostname = prompt[-10:-1]

    #Below variables storing date and time information
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second

    #Below is a nice way of creating a new backup file with date and time information and reducing the chances of overwriting
    backup_file = f'{hostname}_{year}_{month}_{day}_{hour}_{minute}_{second}_Backup.txt'

    with open(backup_file, 'w') as file3:
        file3.writelines(all_commands)

    connection.disconnect()

threads = list()
# below for loop is used to re-iterate the below code for each line item/host in the device-list file
for hostip in devices:
    # below is a dictionary which defines the basic properties of a cisco device required for connection
    cisco_device = {
        'device_type': 'cisco_ios',
        'host': hostip,
        'username': 'admin',
        'password': passwd,
        'port': 22,
        'verbose': True
    }
    th = threading.Thread(target=backup, args=(cisco_device,))
    threads.append(th)

for th in threads:
    th.start()
for th in threads:
    th.join()


end = time.time()

print(f'Total time it took: {end-start}')
