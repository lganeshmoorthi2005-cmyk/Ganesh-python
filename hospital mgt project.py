# ============================================================
# HEART PATIENT MANAGEMENT SYSTEM
# Tools Used: tkinter, pandas, matplotlib, numpy
# Level: Beginner Friendly
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

# ============================================================
# COLOR THEME
# ============================================================
BG_DARK    = "#0D1B2A"   # deep navy background
BG_CARD    = "#1B2A3B"   # card panels
ACCENT     = "#E63946"   # medical red
ACCENT2    = "#457B9D"   # calm blue
WHITE      = "#F1FAEE"   # off-white text
GRAY       = "#A8DADC"   # muted teal
YELLOW     = "#FFD166"   # highlight yellow
GREEN      = "#06D6A0"   # success green
FONT_TITLE = ("Helvetica", 22, "bold")
FONT_HEAD  = ("Helvetica", 13, "bold")
FONT_BODY  = ("Helvetica", 11)
FONT_SMALL = ("Helvetica", 9)

# ============================================================
# GLOBAL PATIENT DATA STORAGE (list of dicts → DataFrame)
# ============================================================
patient_records = []   # each item is a dictionary

# ============================================================
# FUNCTION: VALIDATE DATE FORMAT
# ============================================================
def validate_date(date_str):
    """Check if date string is in DD-MM-YYYY format."""
    try:
        datetime.datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False

# ============================================================
# FUNCTION: CALCULATE DAYS STAYED
# ============================================================
def calculate_days(admit_date, discharge_date):
    """Return number of days between admission and discharge."""
    admit    = datetime.datetime.strptime(admit_date,    "%d-%m-%Y")
    discharge = datetime.datetime.strptime(discharge_date, "%d-%m-%Y")
    delta = discharge - admit
    return delta.days

# ============================================================
# FUNCTION: ADD PATIENT RECORD
# ============================================================
def add_patient():
    """Read form fields, validate, and save patient record."""

    # --- Read all field values ---
    name          = entry_name.get().strip()
    age_str       = entry_age.get().strip()
    gender        = gender_var.get()
    admit_date    = entry_admit.get().strip()
    discharge_date= entry_discharge.get().strip()
    treatment     = treatment_var.get()
    payment       = payment_var.get()
    surgery_result= surgery_var.get()

    # --- Basic validation ---
    if not name:
        messagebox.showerror("Missing Field", "Please enter patient name.")
        return

    if not age_str.isdigit():
        messagebox.showerror("Invalid Age", "Age must be a number (e.g. 45).")
        return

    age = int(age_str)
    if age < 1 or age > 120:
        messagebox.showerror("Invalid Age", "Age must be between 1 and 120.")
        return

    if gender == "Select":
        messagebox.showerror("Missing Field", "Please select gender.")
        return

    if not validate_date(admit_date):
        messagebox.showerror("Invalid Date", "Admission date must be DD-MM-YYYY.")
        return

    if not validate_date(discharge_date):
        messagebox.showerror("Invalid Date", "Discharge date must be DD-MM-YYYY.")
        return

    days = calculate_days(admit_date, discharge_date)
    if days < 0:
        messagebox.showerror("Date Error", "Discharge date cannot be before admission date.")
        return

    if treatment == "Select":
        messagebox.showerror("Missing Field", "Please select treatment type.")
        return

    if payment == "Select":
        messagebox.showerror("Missing Field", "Please select payment method.")
        return

    if surgery_result == "Select":
        messagebox.showerror("Missing Field", "Please select surgery result.")
        return

    # --- Build patient dictionary ---
    patient = {
        "Name"          : name,
        "Age"           : age,
        "Gender"        : gender,
        "Admit Date"    : admit_date,
        "Discharge Date": discharge_date,
        "Days Stayed"   : days,
        "Treatment"     : treatment,
        "Payment"       : payment,
        "Surgery Result": surgery_result
    }

    # --- Append to global list ---
    patient_records.append(patient)

    # --- Add to table display ---
    tree.insert("", "end", values=(
        len(patient_records),
        name, age, gender,
        admit_date, discharge_date, days,
        treatment, payment, surgery_result
    ))

    messagebox.showinfo("Success", f"Patient '{name}' added successfully!\nDays Stayed: {days}")
    clear_form()

# ============================================================
# FUNCTION: CLEAR FORM FIELDS
# ============================================================
def clear_form():
    """Reset all input fields to empty/default."""
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    gender_var.set("Select")
    entry_admit.delete(0, tk.END)
    entry_discharge.delete(0, tk.END)
    treatment_var.set("Select")
    payment_var.set("Select")
    surgery_var.set("Select")

# ============================================================
# FUNCTION: DELETE SELECTED RECORD
# ============================================================
def delete_patient():
    """Delete selected row from table and patient_records list."""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a patient row to delete.")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
    if not confirm:
        return

    item   = tree.item(selected[0])
    row_no = int(item["values"][0]) - 1   # serial number is 1-based

    patient_records.pop(row_no)
    tree.delete(selected[0])

    # Refresh serial numbers in table
    for idx, row_id in enumerate(tree.get_children()):
        tree.item(row_id, values=(idx + 1,) + tree.item(row_id)["values"][1:])

    messagebox.showinfo("Deleted", "Patient record deleted.")

# ============================================================
# FUNCTION: SHOW SUMMARY STATISTICS
# ============================================================
def show_summary():
    """Display count and stats using pandas + numpy."""
    if not patient_records:
        messagebox.showwarning("No Data", "No patient records found.")
        return

    df = pd.DataFrame(patient_records)

    total      = len(df)
    avg_age    = np.mean(df["Age"].values)
    avg_days   = np.mean(df["Days Stayed"].values)
    male_count = len(df[df["Gender"] == "Male"])
    fem_count  = len(df[df["Gender"] == "Female"])
    success    = len(df[df["Surgery Result"] == "Success"])
    fail       = len(df[df["Surgery Result"] == "Failure"])

    summary_win = tk.Toplevel(root)
    summary_win.title("Summary Statistics")
    summary_win.configure(bg=BG_DARK)
    summary_win.geometry("420x380")

    tk.Label(summary_win, text="📊 Patient Summary",
             font=FONT_TITLE, bg=BG_DARK, fg=ACCENT).pack(pady=15)

    stats = [
        ("Total Patients",    total),
        ("Average Age",       f"{avg_age:.1f} yrs"),
        ("Avg. Days Stayed",  f"{avg_days:.1f} days"),
        ("Male Patients",     male_count),
        ("Female Patients",   fem_count),
        ("Surgery Success",   success),
        ("Surgery Failure",   fail),
    ]

    for label, value in stats:
        row = tk.Frame(summary_win, bg=BG_CARD, pady=6, padx=10)
        row.pack(fill="x", padx=20, pady=3)
        tk.Label(row, text=label, font=FONT_BODY, bg=BG_CARD, fg=GRAY,
                 anchor="w").pack(side="left")
        tk.Label(row, text=str(value), font=FONT_HEAD, bg=BG_CARD,
                 fg=YELLOW, anchor="e").pack(side="right")

# ============================================================
# FUNCTION: SHOW BAR CHART (Age distribution)
# ============================================================
def show_age_chart():
    """Plot age distribution using matplotlib."""
    if not patient_records:
        messagebox.showwarning("No Data", "No patient records found.")
        return

    df   = pd.DataFrame(patient_records)
    ages = df["Age"].values

    bins   = [0, 20, 40, 60, 80, 100]
    labels = ["0-20", "21-40", "41-60", "61-80", "81-100"]
    counts = []
    for i in range(len(bins) - 1):
        count = len([a for a in ages if bins[i] < a <= bins[i + 1]])
        counts.append(count)

    fig, ax = plt.subplots(figsize=(6, 4), facecolor=BG_DARK)
    ax.set_facecolor(BG_CARD)
    bars = ax.bar(labels, counts, color=[ACCENT, ACCENT2, YELLOW, GREEN, GRAY], width=0.5)
    ax.set_title("Patient Age Distribution", color=WHITE, fontsize=13, fontweight="bold")
    ax.set_xlabel("Age Group", color=GRAY)
    ax.set_ylabel("Number of Patients", color=GRAY)
    ax.tick_params(colors=WHITE)
    for spine in ax.spines.values():
        spine.set_edgecolor(BG_CARD)
    for bar, val in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                str(val), ha="center", color=WHITE, fontsize=11)

    plt.tight_layout()
    plt.show()

# ============================================================
# FUNCTION: SHOW PIE CHART (Surgery Result)
# ============================================================
def show_surgery_chart():
    """Pie chart for surgery success vs failure."""
    if not patient_records:
        messagebox.showwarning("No Data", "No patient records found.")
        return

    df      = pd.DataFrame(patient_records)
    success = len(df[df["Surgery Result"] == "Success"])
    failure = len(df[df["Surgery Result"] == "Failure"])

    if success == 0 and failure == 0:
        messagebox.showinfo("No Data", "No surgery records available.")
        return

    fig, ax = plt.subplots(figsize=(5, 5), facecolor=BG_DARK)
    wedges, texts, autotexts = ax.pie(
        [success, failure],
        labels=["Success", "Failure"],
        colors=[GREEN, ACCENT],
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"edgecolor": BG_DARK, "linewidth": 2}
    )
    for t in texts:
        t.set_color(WHITE)
    for at in autotexts:
        at.set_color(BG_DARK)
        at.set_fontweight("bold")
    ax.set_title("Surgery Results", color=WHITE, fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()

# ============================================================
# FUNCTION: SHOW PIE CHART (Payment Method)
# ============================================================
def show_payment_chart():
    """Pie chart for payment method breakdown."""
    if not patient_records:
        messagebox.showwarning("No Data", "No patient records found.")
        return

    df     = pd.DataFrame(patient_records)
    counts = df["Payment"].value_counts()

    fig, ax = plt.subplots(figsize=(5, 5), facecolor=BG_DARK)
    colors_list = [ACCENT, ACCENT2, YELLOW, GREEN, GRAY]
    ax.pie(
        counts.values,
        labels=counts.index,
        colors=colors_list[:len(counts)],
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"edgecolor": BG_DARK, "linewidth": 2}
    )
    ax.set_title("Payment Method Breakdown", color=WHITE, fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()

# ============================================================
# FUNCTION: SEARCH PATIENT BY NAME
# ============================================================
def search_patient():
    """Filter table rows by patient name."""
    query = entry_search.get().strip().lower()

    for row in tree.get_children():
        tree.delete(row)

    for idx, p in enumerate(patient_records):
        if query in p["Name"].lower():
            tree.insert("", "end", values=(
                idx + 1,
                p["Name"], p["Age"], p["Gender"],
                p["Admit Date"], p["Discharge Date"], p["Days Stayed"],
                p["Treatment"], p["Payment"], p["Surgery Result"]
            ))

# ============================================================
# FUNCTION: RESET SEARCH (show all records)
# ============================================================
def reset_search():
    """Show all records again after search."""
    entry_search.delete(0, tk.END)
    for row in tree.get_children():
        tree.delete(row)
    for idx, p in enumerate(patient_records):
        tree.insert("", "end", values=(
            idx + 1,
            p["Name"], p["Age"], p["Gender"],
            p["Admit Date"], p["Discharge Date"], p["Days Stayed"],
            p["Treatment"], p["Payment"], p["Surgery Result"]
        ))

# ============================================================
# HELPER: STYLED BUTTON
# ============================================================
def make_button(parent, text, command, color=ACCENT2, fg=WHITE):
    return tk.Button(
        parent, text=text, command=command,
        bg=color, fg=fg, font=FONT_BODY,
        relief="flat", cursor="hand2",
        padx=10, pady=5,
        activebackground=ACCENT, activeforeground=WHITE
    )

# ============================================================
# HELPER: STYLED LABEL + ENTRY ROW
# ============================================================
def make_field(parent, label_text, row_num):
    tk.Label(parent, text=label_text, font=FONT_BODY,
             bg=BG_CARD, fg=GRAY, anchor="w").grid(
        row=row_num, column=0, padx=10, pady=6, sticky="w")
    entry = tk.Entry(parent, font=FONT_BODY, bg="#1e3145",
                     fg=WHITE, insertbackground=WHITE,
                     relief="flat", width=22)
    entry.grid(row=row_num, column=1, padx=10, pady=6, sticky="ew")
    return entry

# ============================================================
# HELPER: STYLED DROPDOWN
# ============================================================
def make_dropdown(parent, variable, options, row_num, label_text):
    tk.Label(parent, text=label_text, font=FONT_BODY,
             bg=BG_CARD, fg=GRAY, anchor="w").grid(
        row=row_num, column=0, padx=10, pady=6, sticky="w")
    menu = ttk.Combobox(parent, textvariable=variable,
                        values=options, state="readonly",
                        font=FONT_BODY, width=20)
    menu.grid(row=row_num, column=1, padx=10, pady=6, sticky="ew")
    return menu

# ============================================================
# BUILD MAIN WINDOW
# ============================================================
root = tk.Tk()
root.title("❤️  Heart Patient Management System")
root.configure(bg=BG_DARK)
root.geometry("1280x750")
root.resizable(True, True)

# ---- TITLE BAR ----
title_bar = tk.Frame(root, bg=ACCENT, height=60)
title_bar.pack(fill="x")
tk.Label(title_bar, text="❤️  HEART PATIENT MANAGEMENT SYSTEM",
         font=FONT_TITLE, bg=ACCENT, fg=WHITE,
         pady=10).pack(side="left", padx=20)
tk.Label(title_bar, text="Powered by Python | pandas | matplotlib | numpy",
         font=FONT_SMALL, bg=ACCENT, fg="#ffcccc",
         pady=10).pack(side="right", padx=20)

# ---- MAIN LAYOUT: Left Form | Right Table ----
main_frame = tk.Frame(root, bg=BG_DARK)
main_frame.pack(fill="both", expand=True, padx=15, pady=10)

# ---- LEFT: INPUT FORM ----
left_frame = tk.Frame(main_frame, bg=BG_CARD,
                      bd=0, relief="flat", width=340)
left_frame.pack(side="left", fill="y", padx=(0, 10), pady=0)
left_frame.pack_propagate(False)

tk.Label(left_frame, text="➕  Add Patient Record",
         font=FONT_HEAD, bg=BG_CARD, fg=ACCENT).grid(
    row=0, column=0, columnspan=2, pady=(15, 5))

# Form Fields
entry_name      = make_field(left_frame, "Patient Name",    1)
entry_age       = make_field(left_frame, "Age (years)",     2)

gender_var      = tk.StringVar(value="Select")
make_dropdown(left_frame, gender_var,
              ["Male", "Female", "Other"],
              3, "Gender")

entry_admit     = make_field(left_frame, "Admit Date (DD-MM-YYYY)",     4)
entry_discharge = make_field(left_frame, "Discharge Date (DD-MM-YYYY)", 5)

treatment_var   = tk.StringVar(value="Select")
make_dropdown(left_frame, treatment_var,
              ["Angioplasty", "Bypass Surgery",
               "Pacemaker", "Medication", "ECG Monitoring"],
              6, "Treatment Type")

payment_var     = tk.StringVar(value="Select")
make_dropdown(left_frame, payment_var,
              ["Cash", "Insurance", "Government Scheme", "Credit Card"],
              7, "Payment Method")

surgery_var     = tk.StringVar(value="Select")
make_dropdown(left_frame, surgery_var,
              ["Success", "Failure", "No Surgery"],
              8, "Surgery Result")

# Action Buttons (in form)
btn_frame = tk.Frame(left_frame, bg=BG_CARD)
btn_frame.grid(row=9, column=0, columnspan=2, pady=15)

make_button(btn_frame, "✅  Save Patient", add_patient,
            color=GREEN, fg=BG_DARK).grid(row=0, column=0, padx=6, pady=4)
make_button(btn_frame, "🗑  Clear Form", clear_form,
            color="#555").grid(row=0, column=1, padx=6, pady=4)
make_button(btn_frame, "❌  Delete Selected", delete_patient,
            color=ACCENT).grid(row=1, column=0, columnspan=2, pady=4, sticky="ew", padx=6)

# Charts Section in left panel
tk.Label(left_frame, text="📈  View Charts",
         font=FONT_HEAD, bg=BG_CARD, fg=ACCENT2).grid(
    row=10, column=0, columnspan=2, pady=(15, 5))

chart_frame = tk.Frame(left_frame, bg=BG_CARD)
chart_frame.grid(row=11, column=0, columnspan=2)

make_button(chart_frame, "🎂 Age Chart",      show_age_chart,    color=ACCENT2).grid(row=0, column=0, padx=5, pady=4)
make_button(chart_frame, "💉 Surgery Chart",  show_surgery_chart, color="#6a0572").grid(row=0, column=1, padx=5, pady=4)
make_button(chart_frame, "💳 Payment Chart",  show_payment_chart, color="#0077b6").grid(row=1, column=0, columnspan=2, pady=4, sticky="ew", padx=5)

make_button(left_frame, "📊  Summary Statistics", show_summary,
            color=YELLOW, fg=BG_DARK).grid(
    row=12, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# ---- RIGHT: TABLE SECTION ----
right_frame = tk.Frame(main_frame, bg=BG_DARK)
right_frame.pack(side="left", fill="both", expand=True)

# Search Bar
search_frame = tk.Frame(right_frame, bg=BG_DARK)
search_frame.pack(fill="x", pady=(0, 8))

tk.Label(search_frame, text="🔍 Search Patient:",
         font=FONT_BODY, bg=BG_DARK, fg=GRAY).pack(side="left", padx=(0, 6))
entry_search = tk.Entry(search_frame, font=FONT_BODY,
                        bg="#1e3145", fg=WHITE,
                        insertbackground=WHITE, relief="flat", width=25)
entry_search.pack(side="left", padx=(0, 6))
make_button(search_frame, "Search", search_patient, color=ACCENT2).pack(side="left", padx=4)
make_button(search_frame, "Reset",  reset_search,   color="#555").pack(side="left", padx=4)

tk.Label(right_frame, text="📋  Patient Records",
         font=FONT_HEAD, bg=BG_DARK, fg=WHITE).pack(anchor="w", pady=(0, 5))

# Treeview Table
columns = ("#", "Name", "Age", "Gender",
           "Admit", "Discharge", "Days",
           "Treatment", "Payment", "Surgery")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background=BG_CARD,
                foreground=WHITE,
                rowheight=28,
                fieldbackground=BG_CARD,
                font=FONT_BODY)
style.configure("Treeview.Heading",
                background=ACCENT,
                foreground=WHITE,
                font=FONT_HEAD)
style.map("Treeview", background=[("selected", ACCENT2)])

tree_frame = tk.Frame(right_frame, bg=BG_DARK)
tree_frame.pack(fill="both", expand=True)

scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")

tree = ttk.Treeview(tree_frame, columns=columns,
                    show="headings",
                    yscrollcommand=scroll_y.set,
                    xscrollcommand=scroll_x.set)

scroll_y.config(command=tree.yview)
scroll_x.config(command=tree.xview)
scroll_y.pack(side="right", fill="y")
scroll_x.pack(side="bottom", fill="x")
tree.pack(fill="both", expand=True)

# Column widths
col_widths = [40, 130, 50, 70, 100, 105, 55, 130, 110, 90]
for col, width in zip(columns, col_widths):
    tree.heading(col, text=col)
    tree.column(col, width=width, anchor="center")

# Alternate row color (tag)
tree.tag_configure("odd",  background="#1a2e42")
tree.tag_configure("even", background=BG_CARD)

# ---- STATUS BAR ----
status = tk.Label(root, text="Ready  |  Heart Patient Management System  |  Python + tkinter",
                  font=FONT_SMALL, bg="#0a1520", fg=GRAY, anchor="w", pady=4)
status.pack(fill="x", side="bottom", padx=10)

# ============================================================
# START APPLICATION
# ============================================================
root.mainloop()