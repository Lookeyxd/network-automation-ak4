
# 📁 Arbeidskrav 4 – Network Infrastructure Automation

This repository contains a complete solution for automating the initial configuration of Cisco routers and switches using both **Python (Netmiko over serial)** and **Ansible (SSH-based)**. The project includes modular scripts that make it easy to apply and adjust configurations for different device roles in a network.

---

## 🧰 Project Structure

```
Config Scripts/
├── Python/
│   ├── Router1/
│   ├── Router2/
│   ├── Switch/
│   └── L3Switch/
├── Ansible/
│   ├── Router1/
│   ├── Router2/
│   └── Switch/
└── ANSIBLE_HOST_KEY_CHECKING=False ans.txt
```

---

## 🔌 Python Section (Serial Configuration)

Used to configure devices before network access is available. All scripts use **Netmiko over serial (console cable)**.

### 🧾 Features:
- Set hostname
- Configure management IP on VLANs
- Enable SSH (with domain, RSA keys, VTY login)
- Configure trunk/access ports
- Assign default gateway
- Save configuration

Each device (Router1, Router2, Switch, L3Switch) has:
- `configure_device.py`: the main script
- `device_vars.py`: variables like hostname, interface IPs, VLANs, SSH settings

### ▶️ How to Use:
1. Plug in the console cable.
2. Set the correct `serial_port` in the `*_vars.py` file (e.g. COM3).
3. Run the script:
   ```bash
   python configure_device.py
   ```

---

## 🧠 Ansible Section (SSH-Based Automation)

Once management IP and SSH are configured using the Python scripts, use Ansible for modular and extensible automation.

### 📦 Roles & Playbooks:
- Modular files: `main.yaml`, `interfaces.yaml`, `hsrp.yaml`, `subinterfaces.yaml`, `etherchannel.yaml`, `access_ports.yaml`, `dhcp.yaml`
- Variables: Controlled via `variables.yaml` per device
- Conditional logic (e.g. `enable_hsrp: true`) controls which tasks are applied

### 🧾 Example Features:
- Configure subinterfaces
- Enable OSPF on point-to-point router links
- Set up HSRP with virtual IP and priorities
- Build DHCP pools (with exclusions, DNS, and default gateway)
- Create EtherChannel bundles using LACP
- Configure access and trunk ports

### ▶️ How to Run:

1. Make sure SSH is enabled and reachable (verify via `ssh user@device_ip`, or application like putty).
2. Adjust `hosts` file with correct IPs and credentials.
3. Set desired features in `variables.yaml`:
   ```yaml
   enable_hsrp: true
   enable_etherchannel: true
   etherchannel_ports:
     - FastEthernet0/21
     - FastEthernet0/22
   ```
4. Run the playbook:
   ```bash
   ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook main.yaml -i hosts
   ```

---

## 💡 Example Config Scenarios

| Device     | Config via     | Key Roles                                  |
|------------|----------------|---------------------------------------------|
| **Router1** | Python + Ansible | Subinterfaces, HSRP standby, DHCP server     |
| **Router2** | Python + Ansible | HSRP active, OSPF peer, routing             |
| **Switch**  | Python + Ansible | EtherChannel (LACP), VLAN trunking, access ports |
| **L3Switch**| Python only      | Management IP, SSH, Trunk + Access ports    |

---

## ⚠️ Notes

- All default usernames/passwords are `cisco`. Change them in `*_vars.py` and `variables.yaml` before production use.
- Requires Python packages: `netmiko`, `pyserial`
- Ansible must be installed (`pip install ansible`)
- Tested against Cisco IOS devices in GNS3 and Packet Tracer.
- Known error with python script on the routers (look screenshot in python folder), if you get this error keep running the script until you dont. (Error is caused by crypto key generate taking more than 1 second to generate)
- If the python script still isnt working, try manually entering the com port and enter enable mode then close the com and try again. (Netmiko is sensetive on where it is on the device)

---

## 🧑‍💻 Author

Created by Aolian 
As part of Arbeidskrav 4 – Automatisering, 2nd Year ITD
