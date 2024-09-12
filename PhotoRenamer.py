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
from HelperFunctions import timer
import time

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

# def get_total_rows(csv_file):
#     with open(csv_file, "r") as file:
#         return sum(1 for line in file)

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
@timer
def run_script():
    if not (selected_csv and selected_source and selected_dest):
        messagebox.showerror(message="Please select CSV file, source directory, and destination directory.")
        return

    run.grid_forget()
    progress_bar.grid(column=0, row=4, sticky=(W, E), padx=5, pady=10, columnspan=2)
    progress_label.grid(column=0, row=5, padx=5, pady=10, columnspan=2)

    total_photos = get_total_photos(selected_csv)
    progress_bar["maximum"] = total_photos

    time_start = time.time()

    missing_photos = []

    with open(selected_csv, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        processed_photos = 0
        for row in reader:
            barcode = row["barcode"]
            photos = row["photos"].split(",")

            for idx, img in enumerate(photos):
                org_file_path = os.path.join(selected_source, img+".jpg")
                new_file_name = f"{barcode} - {idx+1}.jpg"
                dest_file_path = os.path.join(selected_dest, new_file_name)

                if os.path.exists(dest_file_path):
                    print(f"{new_file_name} already exists, skipping file")
                    pass
                else:
                    try:
                        shutil.copy(org_file_path, dest_file_path)
                        print(f"Successfully renamed {img} to {new_file_name}")
                    except FileNotFoundError:
                        print(f"{img} file not found")
                        missing_photos.append(img)

                processed_photos += 1
                progress_bar["value"] = processed_photos
                update_label(processed_photos, total_photos)
                root.update_idletasks()

    time_end = time.time()
    total_time = time_end - time_start

    messagebox.showinfo(message=f"Photos have been renamed with {len(missing_photos)} errors\nCompleted in {total_time:.2f} seconds" )

    if missing_photos:
        missing_photos_str = "\n".join(missing_photos)
        messagebox.showwarning(message=f"The following files were not found:\n{missing_photos_str}")

    root.destroy()

# GUI setup and creation
root = Tk()
root.title("Photo Rename")
root.eval("tk::PlaceWindow . center")
root.resizable(False, False)

# Creating widgets
content = ttk.Frame(root, padding=10)
summary = ttk.Label(content, text="This tool allows you to rename photos from fulcrum using a CSV file.\n" +
                                  "Please enter the fulcrum asset CSV, the folder where the photos are located,\n" +
                                  "and the folder where you want the renamed photos to be copied")

csv_label = ttk.Label(content, text="Open CSV File")
source_label = ttk.Label(content, text="Open Source Directory")
dest_label = ttk.Label(content, text="Open Destination Path")
csv_button = ttk.Button(content, text="Select CSV", command=getCSV)
source_button = ttk.Button(content, text="Select Source Destination", command=getSourceDir)
dest_button = ttk.Button(content, text="Select Destination Directory", command=getDestPath)
run = ttk.Button(content, text="Rename Photos", command=run_script)
progress_bar = ttk.Progressbar(content, orient="horizontal", mode="determinate", length=300)
progress_label = ttk.Label(content, text="")

# placement of gui and widgets
content.grid(column=0, row=0)
summary.grid(column=0, row=0, columnspan=3, padx=5, pady=10, sticky="w")
csv_label.grid(column=0, row=1, sticky="w", padx=5, pady=10)
source_label.grid(column=0, row=2, sticky="w", padx=5, pady=10)
dest_label.grid(column=0, row=3, sticky="w", padx=5, pady=10)
csv_button.grid(column=1, row=1, sticky="e", padx=5, pady=10)
source_button.grid(column=1, row=2, sticky="e", padx=5, pady=10)
dest_button.grid(column=1, sticky="e", padx=5, pady=10, row=3)
run.grid(column=0, row=4, sticky="w", padx=5, pady=10)

root.mainloop()

