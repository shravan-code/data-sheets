# Project Locking System

I have implemented a comprehensive locking system for the Data Sheets project. This system ensures that only one process (agent or human) is modifying a specific module at a time, preventing data corruption and conflicting changes.

## Components

### 1. State Management: `.agents/locks.json`
A centralized JSON file that tracks the lock status of every module in the project. It includes timestamps, owners, and reasons for each lock.

### 2. Mandatory Guidelines: `.agents/AGENT_GUIDELINES.md`
A set of rules that every agent working on this repository must follow. It outlines the protocol for acquiring, checking, and releasing locks.

### 3. Management Utility: `scripts/manage_locks.py`
A CLI tool to manage locks easily.
- `python scripts/manage_locks.py status`: View current lock status.
- `python scripts/manage_locks.py acquire <module> "<reason>"`: Acquire a lock.
- `python scripts/manage_locks.py release <module>`: Release a lock.

### 4. Build System Integration: `scripts/builder/core.py`
The `GuideBuilder` now automatically checks for locks before starting a build. 
- If a **Global Lock** is active, the build will abort.
- If a **Module Lock** is active for the specific guide being built, it will print a prominent warning.

## How to use it

**For Agents:**
Before making changes to any JSON data or build scripts, I will now:
1. Run `python scripts/manage_locks.py acquire <module> "Reason for change"`
2. Perform the edits.
3. Run `python scripts/manage_locks.py release <module>`

**For You:**
You can use the same script to lock modules if you are doing manual maintenance, which will signal to me (and future agents) to stay clear of those files.
