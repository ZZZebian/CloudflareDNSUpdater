import requests
import time
import threading
import os
import json
import winreg as reg
from tkinter import Tk, Label, Entry, Button, Text, END, Checkbutton, IntVar, StringVar, ttk

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        return response.json()['ip']
    except requests.RequestException as e:
        log_message(f"Error fetching public IP: {e}")
        return None

def update_dns_record(api_token, zone_id, record_id, domain, record_type, ip):
    try:
        api_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_token}',
        }
        data = {
            'type': record_type,
            'name': domain,
            'content': ip,
            'ttl': 300,
            'proxied': False
        }
        response = requests.put(api_url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        if result.get('success'):
            return {"success": True, "message": "DNS record updated successfully."}
        else:
            return {"success": False, "errors": result.get('errors', ["Unknown error"])}
    except requests.RequestException as e:
        log_message(f"Error updating DNS record: {e}")
        return {"success": False, "errors": [str(e)]}

def save_config(config):
    try:
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file)
    except IOError as e:
        log_message(f"Error saving configuration: {e}")

def load_config():
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r') as config_file:
                return json.load(config_file)
        except IOError as e:
            log_message(f"Error loading configuration: {e}")
    return {}

def add_to_startup():
    pth = os.path.dirname(os.path.realpath(__file__))
    s_name = "CloudflareDNSUpdater"
    address = os.path.join(pth, 'update_dns_gui.exe')
    try:
        key = reg.HKEY_CURRENT_USER
        key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        open = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(open, s_name, 0, reg.REG_SZ, address)
        reg.CloseKey(open)
    except Exception as e:
        log_message(f"Error adding to startup: {e}")

def remove_from_startup():
    s_name = "CloudflareDNSUpdater"
    try:
        key = reg.HKEY_CURRENT_USER
        key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        open = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
        try:
            reg.DeleteValue(open, s_name)
            log_message(f"Removed {s_name} from startup.")
        except FileNotFoundError:
            log_message(f"{s_name} not found in startup registry.")
        finally:
            reg.CloseKey(open)
    except Exception as e:
        log_message(f"Error removing from startup: {e}")

def start_updating(api_token, zone_id, record_id, domain, record_type, interval, auto_start):
    def update_loop():
        while True:
            current_ip = get_public_ip()
            if current_ip:
                log_message(f"Current IP: {current_ip}")
                result = update_dns_record(api_token, zone_id, record_id, domain, record_type, current_ip)
                if result["success"]:
                    log_message(result["message"])
                else:
                    log_message(f"Failed to update DNS record: {', '.join(result['errors'])}")
            time.sleep(interval * 60)  # Sleep for the specified interval

    if auto_start.get():
        add_to_startup()
    else:
        remove_from_startup()

    thread = threading.Thread(target=update_loop)
    thread.daemon = True
    thread.start()

def log_message(message):
    log_text.insert(END, f"{message}\n")
    log_text.see(END)

def on_start_button_click():
    api_token = api_token_entry.get()
    zone_id = zone_id_entry.get()
    record_id = record_id_var.get()
    domain = domain_entry.get()
    record_type = record_type_entry.get()
    interval = int(interval_entry.get())

    config = {
        'api_token': api_token,
        'zone_id': zone_id,
        'record_id': record_id,
        'domain': domain,
        'record_type': record_type,
        'interval': interval,
        'auto_start': auto_start.get()
    }
    save_config(config)
    start_updating(api_token, zone_id, record_id, domain, record_type, interval, auto_start)

def populate_records():
    api_token = api_token_entry.get()
    zone_id = zone_id_entry.get()
    
    if not api_token or not zone_id:
        log_message("API Token and Zone ID are required to fetch records.")
        return

    try:
        api_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
        }
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        records = response.json()

        if records.get('success'):
            record_ids = [(record['name'], record['id']) for record in records.get('result', [])]
            if record_ids:
                dropdown_values = [f"{name} ({record_id})" for name, record_id in record_ids]
                record_dropdown['values'] = dropdown_values
                if dropdown_values:
                    record_id_var.set(record_ids[0][1])
            else:
                record_dropdown['values'] = ["No records found"]
                record_id_var.set("")
        else:
            log_message("Failed to fetch DNS records")
    except requests.RequestException as e:
        log_message(f"Error fetching DNS records: {e}")

# Load saved config if available
config = load_config()

# Set up the GUI
root = Tk()
root.title("Cloudflare DNS Updater")
root.iconbitmap('icon.ico')  # Path to your .ico file

Label(root, text="API Token:").grid(row=0, column=0, pady=(10, 5))
api_token_entry = Entry(root, width=50)
api_token_entry.grid(row=0, column=1, pady=(10, 5))
api_token_entry.insert(0, config.get('api_token', ''))

Label(root, text="Zone ID:").grid(row=1, column=0, pady=(5, 5))
zone_id_entry = Entry(root, width=50)
zone_id_entry.grid(row=1, column=1, pady=(5, 5))
zone_id_entry.insert(0, config.get('zone_id', ''))

Label(root, text="DNS Record:").grid(row=2, column=0, pady=(5, 5))
record_id_var = StringVar()
record_dropdown = ttk.Combobox(root, textvariable=record_id_var, width=50)
record_dropdown.grid(row=2, column=1, pady=(5, 5))
record_dropdown.bind('<<ComboboxSelected>>', lambda event: record_id_var.set(record_id_var.get().split('(')[-1].strip(')')))

Label(root, text="(Sub)Domain:").grid(row=3, column=0, pady=(5, 10))
domain_entry = Entry(root, width=50)
domain_entry.grid(row=3, column=1, pady=(5, 10))
domain_entry.insert(0, config.get('domain', ''))

Label(root, text="Record Type:").grid(row=4, column=0, pady=(5, 5))
record_type_entry = Entry(root, width=50)
record_type_entry.grid(row=4, column=1, pady=(5, 5))
record_type_entry.insert(0, config.get('record_type', 'A'))

Label(root, text="Update Interval (minutes):").grid(row=5, column=0, pady=(5, 10))
interval_entry = Entry(root, width=50)
interval_entry.grid(row=5, column=1, pady=(5, 10))
interval_entry.insert(0, config.get('interval', '5'))

auto_start = IntVar(value=config.get('auto_start', 0))
Checkbutton(root, text="Start with Windows", variable=auto_start).grid(row=6, column=1, pady=(5, 10))

update_button = Button(root, text="Update Record List", command=populate_records)
update_button.grid(row=7, column=0, columnspan=2, pady=10)

start_button = Button(root, text="Start Updating", command=on_start_button_click)
start_button.grid(row=8, column=0, columnspan=2, pady=10)

log_text = Text(root, wrap='word', height=15, width=70)
log_text.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
