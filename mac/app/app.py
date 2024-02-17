import streamlit as st
import pandas as pd
import os
import socket
import fcntl
import struct
from datetime import datetime

# CSV file name
csv_file = 'mac.csv'

# Check if CSV file exists, if not, create it
if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=['Date', 'Name', 'MAC Address', 'Interface', 'First_Time', 'Ping Status'])
    df.to_csv(csv_file, index=False)

# Function to get MAC address for a given interface
def get_interface_mac(interface):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        mac_bytes = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', interface[:15].encode()))
        mac_address = ':'.join(['{:02x}'.format(b) for b in mac_bytes[18:24]])
        return mac_address
    except Exception as e:
        print("Error:", e)
        return None

# Function to get all network interfaces and their MAC addresses
def get_all_interfaces_macs():
    try:
        interfaces_macs = {}
        with open('/proc/net/dev', 'r') as f:
            for line in f:
                if ':' in line:
                    interface = line.split(':')[0].strip()
                    if interface != 'lo':
                        mac_address = get_interface_mac(interface)
                        if mac_address:
                            interfaces_macs[interface] = mac_address
        return interfaces_macs
    except Exception as e:
        print("Error:", e)
        return None

# Function to check if MAC address is first time
def check_first_time(mac_address):
    df = pd.read_csv(csv_file)
    if mac_address in df['MAC Address'].values:
        return 'No'
    else:
        return 'Yes'

# Function to check ping status
def check_ping():
    # Add your ping logic here
    return 'Success'

# Function to log user data
def log_user_data(name, interfaces_macs, ping_status):
    date_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    df = pd.read_csv(csv_file)
    for interface, mac_address in interfaces_macs.items():
        first_time = check_first_time(mac_address)
        new_entry = pd.DataFrame({'Date': [date_time], 'Name': [name], 'MAC Address': [mac_address], 'Interface': [interface], 'First_Time': [first_time], 'Ping Status': [ping_status]})
        df = pd.concat([new_entry, df], ignore_index=True)
    df.to_csv(csv_file, index=False)

# Streamlit app
def main():
    st.title('MAC Address Logger')

    # Input field for user name
    name = st.text_input('Enter your name')

    # Display button to log user data
    button_clicked = st.button('SEND')

    if button_clicked and not name:
        st.error('Name cannot be empty')

    if button_clicked and name:
        # Get all network interfaces and their MAC addresses
        interfaces_macs = get_all_interfaces_macs()

        # Check ping status
        ping_status = check_ping()

        # Log user data
        log_user_data(name, interfaces_macs, ping_status)

        st.success('Thank you! Your data has been logged successfully!')

if __name__ == '__main__':
    main()

