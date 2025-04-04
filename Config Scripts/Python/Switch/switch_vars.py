# Serial connection parameters
serial_port = "COM4"         # e.g. COM port on Windows, or "/dev/ttyUSB0" on Linux
baud_rate = 	9600

# Basic device settings
hostname = "Switch1"
mgmt_vlan = "10"
mgmt_ip = "10.10.0.10"
mgmt_mask = "255.255.255.0"

# Default gateway for management network
default_gateway = "10.10.0.1"

# SSH and authentication settings
domain_name = "example.com"
rsa_key_bits = "1024"
username = "cisco"
password = "cisco"        # Local user password

# Interface configurations
trunk_interface = "fa0/23"
trunk_allowed_vlans = "10-12"
access_interface = "fa0/1"
