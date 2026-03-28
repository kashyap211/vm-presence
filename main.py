from pypresence import Presence
import time
import subprocess
import pygetwindow as gw
import os
client_id = os.getenv("DISCORD_CLIENT_ID")
RPC = None  

VM_PROCESSES = [
    "vmware.exe",
    "vmware-vmx.exe",
    "virtualboxvm.exe",
    "vmwp.exe",
    "qemu-system-x86_64.exe"
]

EDITORS = [
    "code.exe",       
    "pycharm64.exe"
]

def get_tasks():
    return subprocess.check_output("tasklist", shell=True).decode().lower()

def get_running_vm(tasks):
    for process in VM_PROCESSES:
        if process in tasks:
            return process
    return None

def is_editor_running(tasks):
    for editor in EDITORS:
        if editor in tasks:
            return True
    return False

def get_editor_file():
    windows = gw.getAllTitles()
    
    for title in windows:
        if "visual studio code" in title.lower():
            return title.split(" - ")[0]
    
    return None

def get_vm_name():
    windows = gw.getAllTitles()
    
    for title in windows:
        t = title.lower()
        
        if "oracle vm virtualbox" in t or "vmware workstation" in t:
            return title.split(" - ")[0]
    
    return "Virtual Machine"

print("Smart VM Presence running...")

start_time = None
current_vm = None
connected = False

while True:
    tasks = get_tasks()
    vm = get_running_vm(tasks)
    editor = is_editor_running(tasks)

    if vm:
        if not connected:
            RPC = Presence(client_id)
            RPC.connect()
            connected = True
            start_time = time.time()

        vm_name = get_vm_name()
        file = get_editor_file()

        # 🔥 Smart logic for text + icons
        if editor and file:
            state_text = f"Coding {file} + {vm_name}"
            large_image = "code"
            large_text = "Coding"
            small_image = "vm"
            small_text = vm_name

        elif editor:
            state_text = f"Coding + {vm_name}"
            large_image = "code"
            large_text = "Coding"
            small_image = "vm"
            small_text = vm_name

        else:
            state_text = f"Running {vm_name}"
            large_image = "vm"
            large_text = vm_name
            small_image = None
            small_text = None

        # 🔥 Update Discord presence
        RPC.update(
            state=state_text,
            details="Virtual Machine Lab",
            large_image=large_image,
            large_text=large_text,
            small_image=small_image,
            small_text=small_text,
            start=start_time
        )

        print(state_text)

    else:
        if connected:
            RPC.clear()
            RPC.close()
            connected = False
            print("VM stopped → returning control to Discord")

    time.sleep(10)
