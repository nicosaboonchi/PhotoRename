# ---------------------------------
# Created by: Nico Saboonchi
# File Name: Rename Script.py
# Date: 9/9/2024
# Function: Provides the GUI interface for which users and interact with the photo rename script
#            in a more familiar way. The rename script needs to be in the same location as the GUI file.
# ---------------------------------

from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter.filedialog import askdirectory
import os
import csv
import shutil
import time
import webbrowser

# Global variables instance
selected_csv = ""
selected_source = ""
selected_dest = ""

# allows user to select a csv file and sets as global var
def getCSV():
    csv_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")],
                                          initialdir=os.path.expanduser("~/Documents") )
    if csv_file:
        csv_label.config(text=f"Selected CSV File:\n{os.path.basename(csv_file)}" )
        global selected_csv
        selected_csv = csv_file

# allows user to select a source dir and sets as global var
def getSourceDir():
    source_path = askdirectory()
    if source_path:
        source_label.config(text=f"Selected source path:\n{source_path}")
        global selected_source
        selected_source = source_path

# allows user to select a dest dir and sets as global var
def getDestPath():
    dest_path = askdirectory(initialdir=os.path.expanduser("~/Documents"))
    if dest_path:
        dest_label.config(text=f"Selected destination path:\n{dest_path}")
        global selected_dest
        selected_dest = dest_path


def get_total_photos(csv_file):
    total_photos = 0
    with open(csv_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            photos = row["photos"].split(",")
            total_photos += len(photos)
    return total_photos

def update_label(processed_rows, total_rows):
    progress_label.config(text=f"Processed {processed_rows} / {total_rows} photos")

# checks to make sure all variables are satisfied then runs renaming
def run_script():
    if not (selected_csv and selected_source and selected_dest):
        messagebox.showerror(message="Please select CSV file, source directory, and destination directory.")
        return

    # hide the run button and help button and show the progress bar
    run.grid_forget()
    help_button.grid_forget()
    progress_bar.grid(column=0, row=4, sticky=(W, E), padx=5, pady=10, columnspan=2)
    progress_label.grid(column=0, row=5, padx=5, pady=10, columnspan=2)

    # get the total number of photos for the progress bar
    total_photos = get_total_photos(selected_csv)
    progress_bar["maximum"] = total_photos

    time_start = time.time()

    # open the csv and read each line from the csv
    with open(selected_csv, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        processed_photos = 0

        # store the barcode and photos for each row
        for row in reader:
            barcode = row["barcode"]
            photos = row["photos"].split(",")

            # store the original path and creates new file names and path
            for idx, img in enumerate(photos):
                org_file_path = os.path.join(selected_source, img+".jpg")
                new_file_name = f"{barcode} - {idx+1}.jpg"
                dest_file_path = os.path.join(selected_dest, new_file_name)

                # check if the new file name already exists
                if os.path.exists(dest_file_path):
                    print(f"{new_file_name} already exists, skipping file")
                    pass

                # using shutil to copy the img to the new path
                else:
                    try:
                        shutil.copy(org_file_path, dest_file_path)
                        print(f"Successfully renamed {img} to {new_file_name}")
                    except FileNotFoundError:
                        print(f"{img} file not found")

                # update the progress bar
                processed_photos += 1
                progress_bar["value"] = processed_photos
                update_label(processed_photos, total_photos)
                root.update_idletasks()

    time_end = time.time()
    total_time = time_end - time_start

    messagebox.showinfo(message=f"Photos have been renamed in {total_time:.2f} seconds" )

    root.destroy()

# GUI setup and creation
root = Tk()
root.title("Photo Renamer")
root.eval("tk::PlaceWindow . center")
root.resizable(False, False)

# Create tabs within the GUI for different departments
notebook = ttk.Notebook(root)
notebook.grid(column=0, row=0)

# Creating widgets
fm_tab = ttk.Frame(notebook, padding=10)
eas_tab = ttk.Frame(notebook, padding=10)

notebook.add(fm_tab, text="FM Renamer")
notebook.add(eas_tab, text="EAS Tab Coming Soon")

summary = ttk.Label(fm_tab, text="Welcome to the FM photo renamer. This app renames photos from Fulcrum using\n"+
                                 "the barcode column from a Fulcrum CSV.\n\n" +
                                 "Please select a Fulcrum CSV, the source directory where the photos are stored,\n"+
                                 "and the destination directory where you want the photos to be copied to.\n\n" +
                                 "Press the help button for more information and instructions.")

# FM GUI Block ---------------------------------------------------------
# Widget Initialization
csv_label = ttk.Label(fm_tab, text="Open CSV File")
source_label = ttk.Label(fm_tab, text="Open Source Directory")
dest_label = ttk.Label(fm_tab, text="Open Destination Path")
csv_button = ttk.Button(fm_tab, text="Select CSV", command=getCSV)
source_button = ttk.Button(fm_tab, text="Select Source Destination", command=getSourceDir)
dest_button = ttk.Button(fm_tab, text="Select Destination Directory", command=getDestPath)
run = ttk.Button(fm_tab, text="Rename Photos", command=run_script)
progress_bar = ttk.Progressbar(fm_tab, orient="horizontal", mode="determinate", length=300)
progress_label = ttk.Label(fm_tab, text="")
help_button = ttk.Button(fm_tab, text="Help", command=lambda:webbrowser.open("https://github.com/nicosaboonchi/PhotoRename"))

# Placement of widgets
summary.grid(column=0, row=0, columnspan=2, padx=5, pady=10, sticky="w")
csv_label.grid(column=0, row=1, sticky="w", padx=5, pady=10)
source_label.grid(column=0, row=2, sticky="w", padx=5, pady=10)
dest_label.grid(column=0, row=3, sticky="w", padx=5, pady=10)
csv_button.grid(column=1, row=1, sticky="e", padx=5, pady=10)
source_button.grid(column=1, row=2, sticky="e", padx=5, pady=10)
dest_button.grid(column=1, sticky="e", padx=5, pady=10, row=3)
run.grid(column=1, row=4, sticky="e", padx=5, pady=10)
help_button.grid(column=0, row=4, sticky="w", padx=5, pady=10)
# ---------------------------------------------------------------------------

root.mainloop()

