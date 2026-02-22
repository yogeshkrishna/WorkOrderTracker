# 🛠 Work Order Tracker (CLI-Based Management System)

A professional command-line based **Work Order Management System** built in Python.  
This application allows users to create, update, track, sort, and manage work orders efficiently using a CSV-based storage system.

Designed with clean logic, highly structured, modular, with robust input validation and error handling.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Dependencies](https://img.shields.io/badge/Dependencies-None-lightgrey?style=for-the-badge)
![Storage](https://img.shields.io/badge/Storage-CSV-lightgrey?style=for-the-badge)
![Interface](https://img.shields.io/badge/Interface-CLI-black?style=for-the-badge)

---

## 📌 Project Overview

The Work Order Tracker simulates a real-world maintenance/task tracking system.  
It enables structured management of work orders with features such as:

- Unique Work Order ID generation
- Automatic overdue detection
- Status management
- Input validation
- Sorting and structured display
- Persistent CSV storage

This project demonstrates strong fundamentals in:

- File handling and persistent storage  
- Robust input validation  
- Modular program structure  
- Command-line application design  
- Defensive programming practices
- Workflow and state management   


---

## 🚀 Features

### 1. Create Work Orders
- Auto-generates formatted IDs (WO-001, WO-002, etc.)
- Automatically sets Issue Date
- Validates future Due Dates
- Priority selection (Low / Medium / High)
- Stores structured notes
- New work orders are automatically set to Open

### 2. View Work Orders
- Displays formatted table output
- Automatically updates overdue status
- Sorted by Due Date by default
- Optional sorting by:
  - Created By
  - Assigned To
  - Issue Date
  - Due Date
  - Priority
  - Status

### 3. Update Work Orders
- ID for work order to be modified is validated
- Modify selected fields
- Modified fields are updated
- Fields skipped using <Enter> remain unchanged

### 4. Status Management
- New work orders set to Open (by default) can be set to:
  - In Progress
  - Closed
  - Overdue (auto-detected)
- Prevents modifying already closed orders

### 5. Delete Work Orders
- Validates ID to be deleted
- Confirmation before deletion
- Safe removal from CSV

### 6. Automatic Overdue Detection
- Compares Due Date with current date
- Automatically updates status to Overdue
- Saves changes persistently


---

## 🧠 System Architecture

The application is organized into clearly defined functional sections within a single file, based on responsibility:

### FILE HANDLING
- Automatic CSV file creation
- Loading work orders into memory
- Saving structured data persistently

### DATE VALIDATION
- Enforcing `YYYY-MM-DD` format
- Preventing past due dates
- Handling invalid date input safely

### STATUS LOGIC
- Automated overdue detection
- Status transition control
- Protection against modifying closed work orders

### DISPLAY
- Dynamic table formatting
- Adaptive column width calculation
- Sorting functionality
- Structured CLI output rendering

### CORE
- Work order ID normalization
- Sequential ID generation
- Create, update, delete operations

### MAIN
- Menu-driven user interface
- Application control flow
- Centralized execution loop

This internal organization improves clarity, maintainability, and logical separation within the system.


---

## 📄 Data Storage

Data is stored in a CSV file using `csv.DictReader` and `csv.DictWriter`.

Fields:

- WO ID  
- Created By  
- Assigned To  
- Issue Date  
- Due Date  
- Priority  
- Status  
- Notes  

Persistent storage ensures all changes are saved between sessions.


---

## 🛡 Input Validation & Data Integrity

- Date must follow `YYYY-MM-DD`
- Due Date cannot be in the past
- Priority restricted to valid options
- Work Order IDs numerically normalized
- Controlled Field Updates
- Status updates controlled by logic rules

These validation mechanisms ensure consistent state management and reduce the risk of invalid or corrupted records.


---

## ▶ How to Run

Simply run the `python Work_Order_Tracker.py` and provide inputs in the CLI interface.
No additional libraries/modules are required and can run in any local system with Python.

The system will automatically:
- Create the CSV file if it does not exist
- Load existing work orders
- Display the main menu


---

### 📊 Example Menu

```
WORK ORDER TRACKER
1. Create Work Order
2. Update Work Order
3. View Work Orders
4. Change Work Order Status
5. Delete Work Order
6. Exit
```

---

## 👨‍💻 Author

**Yogesh Krishna**  
Computer Science Student at RVCE  

---
