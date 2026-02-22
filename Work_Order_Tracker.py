import csv
import os
from datetime import datetime, date

FILE_NAME = "work_orders.csv"

FIELDS = [
    "WO ID",
    "Created By",
    "Assigned To",
    "Issue Date",
    "Due Date",
    "Priority",
    "Status",
    "Notes",
]

# ---------------- FILE HANDLING ----------------
def ensure_csv_exists():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()


def load_work_orders():
    work_orders = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "Status" not in row or not row["Status"]:
                    row["Status"] = "Open"
                work_orders.append(row)
    return work_orders


def save_work_orders(work_orders):
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(work_orders)


# ---------------- DATE VALIDATION ----------------
def get_valid_future_date(prompt):
    while True:
        value = input(prompt).strip()
        try:
            d = datetime.strptime(value, "%Y-%m-%d").date()
            if d < date.today():
                print("Date cannot be in the past.")
            else:
                return value
        except ValueError:
            print("Invalid format. Use YYYY-MM-DD.")


# ---------------- STATUS LOGIC ----------------
def update_overdue_status(work_orders):
    today = date.today()
    changed = False
    for wo in work_orders:
        if wo["Status"] in ("Open", "Overdue"):
            due = datetime.strptime(wo["Due Date"], "%Y-%m-%d").date()
            new_status = "Overdue" if due < today else "Open"
            if wo["Status"] != new_status:
                wo["Status"] = new_status
                changed = True
    if changed:
        save_work_orders(work_orders)


# ---------------- DISPLAY ----------------
def display_work_orders(work_orders, allow_sort=False):
    if not work_orders:
        print("\nNo work orders found.\n")
        return

    update_overdue_status(work_orders)

    work_orders.sort(key=lambda x: x["Due Date"])

    def print_table(data):
        headers = ["No"] + FIELDS
        widths = {h: len(h) for h in headers}

        for i, wo in enumerate(data, 1):
            widths["No"] = max(widths["No"], len(str(i)))
            for h in FIELDS:
                widths[h] = max(widths[h], len(str(wo[h])))

        def sep():
            return "+" + "+".join("-" * (widths[h] + 2) for h in headers) + "+"

        def row(values):
            return "|" + "|".join(
                f" {str(values[h]).ljust(widths[h])} " for h in headers
            ) + "|"

        print("\nWORK ORDERS\n")
        print(sep())
        print(row({h: h for h in headers}))
        print(sep())

        for i, wo in enumerate(data, 1):
            r = {"No": i}
            r.update(wo)
            print(row(r))

        print(sep())

    print_table(work_orders)

    if not allow_sort:
        return

    if input("\nSort work orders? (y/n): ").strip().lower() != "y":
        return

    print("\nSORT BY")
    print("1. Created By")
    print("2. Assigned To")
    print("3. Issue Date")
    print("4. Due Date")
    print("5. Priority")
    print("6. Status")

    choice = input("Choose option: ").strip()

    priority_order = {"Low": 1, "Medium": 2, "High": 3}
    key_map = {
        "1": "Created By",
        "2": "Assigned To",
        "3": "Issue Date",
        "4": "Due Date",
        "5": "Priority",
        "6": "Status",
    }

    if choice in key_map:
        key = key_map[choice]
        if key in ("Created By", "Assigned To", "Status"):
            work_orders.sort(key=lambda x: x[key].lower())
        elif key == "Priority":
            work_orders.sort(key=lambda x: priority_order[x["Priority"]])
        else:
            work_orders.sort(key=lambda x: x[key])
        print_table(work_orders)
    else:
        print("Invalid sort option.")


# ---------------- CORE ----------------
def normalize_wo_id(user_input):
    digits = "".join(c for c in user_input if c.isdigit())
    if not digits:
        return None
    return f"WO-{int(digits):03d}"


def generate_wo_id(work_orders):
    if not work_orders:
        return "WO-001"
    return f"WO-{max(int(w['WO ID'][3:]) for w in work_orders) + 1:03d}"


def create_work_order(work_orders):
    print("\nCREATE WORK ORDER\n")
    wo = {
        "WO ID": generate_wo_id(work_orders),
        "Created By": input("Created by: ").strip(),
        "Assigned To": input("Assigned to: ").strip(),
        "Issue Date": datetime.now().strftime("%Y-%m-%d"),
        "Due Date": get_valid_future_date("Due date (YYYY-MM-DD): "),
        "Status": "Open",
        "Notes": input("Notes: ").strip(),
    }

    while True:
        p = input("Priority (Low / Medium / High): ").strip().capitalize()
        if p in ("Low", "Medium", "High"):
            wo["Priority"] = p
            break
        print("Invalid priority.")

    work_orders.append(wo)
    save_work_orders(work_orders)
    print("\nWork order created.\n")


def update_work_order(work_orders):
    display_work_orders(work_orders)
    raw = input("Enter WO ID to update: ").strip()
    wo_id = normalize_wo_id(raw)

    for wo in work_orders:
        if wo["WO ID"] == wo_id:
            print("\nPress Enter to keep existing value.\n")

            val = input(f"Created By [{wo['Created By']}]: ").strip()
            if val:
                wo["Created By"] = val

            val = input(f"Assigned To [{wo['Assigned To']}]: ").strip()
            if val:
                wo["Assigned To"] = val

            val = input(f"Due Date [{wo['Due Date']}]: ").strip()
            if val:
                wo["Due Date"] = get_valid_future_date("Enter new due date (YYYY-MM-DD): ")

            while True:
                p = input(f"Priority [{wo['Priority']}]: ").strip()
                if not p:
                    break
                p = p.capitalize()
                if p in ("Low", "Medium", "High"):
                    wo["Priority"] = p
                    break
                print("Invalid priority.")

            val = input(f"Notes [{wo['Notes']}]: ").strip()
            if val:
                wo["Notes"] = val

            save_work_orders(work_orders)
            print("\nWork order updated.\n")
            return

    print("\nWork order not found.\n")


def set_work_order_status(work_orders):
    display_work_orders(work_orders)
    wo_id = normalize_wo_id(input("Enter WO ID: ").strip())

    for wo in work_orders:
        if wo["WO ID"] == wo_id:
            if wo["Status"] == "Closed":
                print("Work order already closed.")
                return

            print("\n1. Set In Progress")
            print("2. Close Work Order")
            c = input("Choose option: ").strip()

            if c == "1":
                wo["Status"] = "In Progress"
            elif c == "2":
                wo["Status"] = "Closed"
            else:
                print("Invalid choice.")
                return

            save_work_orders(work_orders)
            print("Status updated.")
            return

    print("Work order not found.")


def delete_work_order(work_orders):
    display_work_orders(work_orders)
    wo_id = normalize_wo_id(input("Enter WO ID to delete: ").strip())

    for wo in work_orders:
        if wo["WO ID"] == wo_id:
            if input(f"Delete {wo_id}? (y/n): ").lower() == "y":
                work_orders.remove(wo)
                save_work_orders(work_orders)
                print("Work order deleted.")
            return

    print("Work order not found.")


# ---------------- MAIN ----------------
def main():
    ensure_csv_exists()
    work_orders = load_work_orders()

    while True:
        print("\nWORK ORDER TRACKER")
        print("1. Create Work Order")
        print("2. Update Work Order")
        print("3. View Work Orders")
        print("4. Change Work Order Status")
        print("5. Delete Work Order")
        print("6. Exit")

        choice = input("Select option: ").strip()

        if choice == "1":
            create_work_order(work_orders)
        elif choice == "2":
            update_work_order(work_orders)
        elif choice == "3":
            display_work_orders(work_orders, allow_sort=True)
        elif choice == "4":
            set_work_order_status(work_orders)
        elif choice == "5":
            delete_work_order(work_orders)
        elif choice == "6":
            save_work_orders(work_orders)
            print("\nData saved. Exiting.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()

