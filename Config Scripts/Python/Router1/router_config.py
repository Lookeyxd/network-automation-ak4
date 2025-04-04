# router_config.py

# Serial Port Settings
SERIAL_PORT = 'COM5'       # Adjust to your COM port (e.g., '/dev/ttyUSB0' for Linux)
BAUD_RATE = 9600

# Router Basic Configurations
HOSTNAME = 'Router1'
DOMAIN_NAME = 'example.com'

# Credentials
USERNAME = 'cisco'
PASSWORD = 'cisco'
ENABLE_SECRET = 'cisco'

# SSH Settings
RSA_KEY_SIZE = 1024
VTY_LINE = 1  # Configures lines 0 through this value

# Interface for management (initial IP setup)
MGMT_INTERFACE = 'GigabitEthernet0/1.10'
MGMT_IP = '10.10.0.1'
MGMT_SUBNET_MASK = '255.255.255.0'

# VLAN ID for subinterface encapsulation
VLAN_ID = 10
