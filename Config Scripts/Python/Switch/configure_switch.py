from netmiko import ConnectHandler
import time
import switch_vars  # Import our variable file

# Prepare device connection parameters for Netmiko (using serial console)
device_params = {
    "device_type": "cisco_ios_serial",
    "serial_settings": {
        "port": switch_vars.serial_port,
        "baudrate": switch_vars.baud_rate,
    },
    "fast_cli": False  # Disable fast CLI for better reliability over serial
}

print(f"[*] Connecting to serial port {switch_vars.serial_port} at {switch_vars.baud_rate} baud...")
net_connect = ConnectHandler(**device_params)  # Open the console connection
net_connect.enable()  # Enter enable mode (if needed)

# Build the configuration command list using variables.
# We now explicitly create VLANs 10, 11, and 12 before applying interface configurations.
config_commands = [
    # 1. Set Hostname
    f"hostname {switch_vars.hostname}",
    
    # 2. Create VLANs
    "vlan 10",
    " name Management",
    "exit",
    "vlan 11",
    " name VLAN11",
    "exit",
    "vlan 12",
    " name VLAN12",
    "exit",
    
    # 3. Set Default Gateway for management traffic
    f"ip default-gateway {switch_vars.default_gateway}",
    
    # 4. Configure Management VLAN interface (SVI) with IP
    f"interface vlan {switch_vars.mgmt_vlan}",
    f"ip address {switch_vars.mgmt_ip} {switch_vars.mgmt_mask}",
    "no shutdown",
    "exit",
    
    # 5. SSH Setup: Set domain, generate RSA key, create local user, and configure VTY lines for SSH
    f"ip domain-name {switch_vars.domain_name}",
    f"crypto key generate rsa modulus {switch_vars.rsa_key_bits}",
    "ip ssh version 2",
    f"username {switch_vars.username} privilege 15 secret {switch_vars.password}",
    "line vty 0 15",
    "transport input ssh",
    "login local",
    "exit",
    
    # 6. Configure Trunk Port: Set interface mode to trunk and allow VLANs 10-12
    f"interface {switch_vars.trunk_interface}",
    "switchport mode trunk",
    f"switchport trunk allowed vlan {switch_vars.trunk_allowed_vlans}",
    "no shutdown",
    "exit",
    
    # 7. Configure Access Port: Set interface mode to access and assign to management VLAN (VLAN 10)
    f"interface {switch_vars.access_interface}",
    "switchport mode access",
    f"switchport access vlan {switch_vars.mgmt_vlan}",
    "no shutdown",
    "exit"
]

print("[*] Entering configuration mode and applying settings...")
# Send configuration commands to the device
output = net_connect.send_config_set(config_commands)
print(output)  # Display device responses for verification

# Save the running configuration to the startup configuration
print("[*] Saving configuration to startup-config...")
net_connect.save_config()

# End the Netmiko session
net_connect.disconnect()
print("[*] Configuration complete. Connection closed.")
