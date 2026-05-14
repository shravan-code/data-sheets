# Agent Locking System & Guidelines

This document outlines the mandatory locking protocol for modifying modules in the Data Sheets project. Every agent working on this repository MUST adhere to these rules to ensure data integrity and prevent race conditions or accidental overwrites.

## 1. The Locking Protocol

Before modifying any file, the agent MUST:

1.  **Check Status**: Read `.agents/locks.json` to verify if the relevant module or the `global_lock` is active.
2.  **Acquire Lock**: If the module is not locked, update `.agents/locks.json` to set `locked: true` for the target module.
    *   Set `reason`: Briefly describe the task (e.g., "Updating Python OOP section").
    *   Set `owner`: Set to `agent-name` or `current-session`.
    *   Set `timestamp`: Current ISO string.
3.  **Perform Task**: Execute the code changes.
4.  **Verify**: Ensure the changes are correct and build scripts run successfully.
5.  **Release Lock**: Reset `locked: false` in `.agents/locks.json` and clear the `reason`, `owner`, and `timestamp`.

## 2. Module Definitions

Locks are organized by modules. A lock on a module covers its data files and corresponding build scripts.

-   **python**: `data/python_complete_guide.json`, `scripts/build_python_guide.py`
-   **sql**: `data/sql_complete_guide.json`, `scripts/build_sql_guide.py`
-   **airflow**: `data/airflow_complete_guide.json`
-   **bash**: `data/bash_guide.json`, `data/bash_subpages_data.json`
-   **databricks**: `data/databricks_complete_guide.json`
-   **de_architectures**: `data/de_architectures_complete_guide.json`
-   **powershell**: `data/powershell_guide.json`
-   **home_page**: `index.html`, `css/ds-home.css`
-   **core_site**: `js/json-guide.js`, `css/ds-main.css`, `css/index.css`

## 3. Global Lock

The `global_lock` should only be used for:
-   Major architectural changes affecting all modules.
-   Refactoring core rendering logic in `js/json-guide.js`.
-   Updating the build system or project-wide CSS.

## 4. Conflict Resolution

-   If a module is locked by another task/session, DO NOT modify its files.
-   If a lock seems stale (older than 4 hours), the agent should verify with the USER before force-releasing it.

## 5. Maintenance

-   Always keep `.agents/locks.json` up to date.
-   If you add a new module, register it in the `locks.json` file.
