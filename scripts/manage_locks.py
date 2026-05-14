import json
import os
import sys
from datetime import datetime

LOCK_FILE = os.path.join(os.path.dirname(__file__), '..', '.agents', 'locks.json')

def load_locks():
    if not os.path.exists(LOCK_FILE):
        print(f"Error: {LOCK_FILE} not found.")
        sys.exit(1)
    with open(LOCK_FILE, 'r') as f:
        return json.load(f)

def save_locks(data):
    data['last_updated'] = datetime.utcnow().isoformat() + 'Z'
    with open(LOCK_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def acquire(module, reason, owner="agent"):
    data = load_locks()
    if module == "global" or data.get('global_lock', {}).get('locked'):
        target = data.get('global_lock', {})
        name = "global"
    elif module in data['modules']:
        target = data['modules'][module]
        name = module
    else:
        print(f"Error: Module '{module}' not found.")
        sys.exit(1)

    if target.get('locked'):
        print(f"Error: '{name}' is already locked by {target.get('owner')} for: {target.get('reason')}")
        sys.exit(1)

    target['locked'] = True
    target['reason'] = reason
    target['owner'] = owner
    target['timestamp'] = datetime.utcnow().isoformat() + 'Z'
    
    save_locks(data)
    print(f"Successfully acquired lock for '{name}'.")

def release(module):
    data = load_locks()
    if module == "global":
        target = data.get('global_lock', {})
        name = "global"
    elif module in data['modules']:
        target = data['modules'][module]
        name = module
    else:
        print(f"Error: Module '{module}' not found.")
        sys.exit(1)

    target['locked'] = False
    target['reason'] = None
    target['owner'] = None
    target['timestamp'] = None
    
    save_locks(data)
    print(f"Successfully released lock for '{name}'.")

def status():
    data = load_locks()
    print("\n--- Project Locking Status ---")
    g = data.get('global_lock', {})
    print(f"Global Lock: {'LOCKED' if g.get('locked') else 'UNLOCKED'}")
    if g.get('locked'):
        print(f"  Reason: {g.get('reason')}")
        print(f"  Owner:  {g.get('owner')}")

    print("\nModules:")
    for mod, info in data['modules'].items():
        status_str = "LOCKED" if info.get('locked') else "UNLOCKED"
        print(f"- {mod:15}: {status_str}")
        if info.get('locked'):
            print(f"  Reason: {info.get('reason')}")
            print(f"  Owner:  {info.get('owner')}")
    print("\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python manage_locks.py [status|acquire|release] [module] [reason]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "status":
        status()
    elif command == "acquire":
        if len(sys.argv) < 4:
            print("Usage: python manage_locks.py acquire [module] [reason]")
            sys.exit(1)
        acquire(sys.argv[2], sys.argv[3])
    elif command == "release":
        if len(sys.argv) < 3:
            print("Usage: python manage_locks.py release [module]")
            sys.exit(1)
        release(sys.argv[2])
    else:
        print("Unknown command.")
