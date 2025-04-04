from netmiko import ConnectHandler
import router_config
import time

def configure_ssh_via_console():
    device = {
        'device_type': 'cisco_ios_serial',
        'serial_settings': {
            'port': router_config.SERIAL_PORT,
            'baudrate': router_config.BAUD_RATE,
        },
        "fast_cli": False  # Disable fast CLI for better reliability over serial
    }

    print(f"Connecting to router on {router_config.SERIAL_PORT}...")

    # Connect via serial console
    net_connect = ConnectHandler(**device)
    time.sleep(3)  # Allow connection to stabilize

    print("Connected via console.")

    # Enter enable mode (initially there's usually no password)
    net_connect.enable()

    # Configuration commands
    config_commands = [
        "no logging console",
        f"hostname {router_config.HOSTNAME}",
        f"ip domain-name {router_config.DOMAIN_NAME}",
        
        # Configure subinterface and encapsulation
        f"interface {router_config.MGMT_INTERFACE}",
        f"encapsulation dot1Q {router_config.VLAN_ID}",
        f"ip address {router_config.MGMT_IP} {router_config.MGMT_SUBNET_MASK}",
        "no shutdown",
        "exit",

        "interface GigabitEthernet0/1",
        "no shutdown",
        "exit",

        f"crypto key generate rsa modulus {router_config.RSA_KEY_SIZE}",
        f"{time.sleep(5)}",
        "ip ssh version 2",
        f"username {router_config.USERNAME} privilege 15 secret {router_config.PASSWORD}",
        f"line vty 0 {router_config.VTY_LINE}",
        "transport input ssh",
        "login local",
        "exit",
        f"enable secret {router_config.ENABLE_SECRET}",
        "end"
    ]

    # Send configuration
    
    print("Sending configuration commands...")
    output = net_connect.send_config_set(config_commands)
    print(output)

    # Save configuration
    print("Saving configuration...")
    save_output = net_connect.save_config()
    print(save_output)

    # Disconnect
    net_connect.disconnect()
    print("Disconnected from router.")

if __name__ == "__main__":
    configure_ssh_via_console()
