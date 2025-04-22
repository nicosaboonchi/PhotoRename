"""
 Created by: Nico Saboonchi
 File Name: Rename Script.py
 Date: 9/6/2024
 Function: This script will take a fulcrum CSV and rename all the downloaded photos with columns from the csv file
           place them into a new directory.
"""


import os
import csv
import shutil
import time
import tkinter
import webbrowser
from csv import DictReader
from tkinter import *
from tkinter import filedialog, messagebox, ttk


class PhotoRenameApp(tkinter.Tk):
    def __init__(self):
        super().__init__()
        # Global variables and basic properties of the GUI

        self.call("source", "azure.tcl")
        self.call("set_theme", "dark")

        self.iconbitmap(r"construction-industry-helmet-protection_108590.ico")
        self.title("Photo Rename App")
        self.eval("tk::PlaceWindow . center")
        self.resizable(False, False)

        self.selected_csv = ""
        self.selected_source_dir = ""
        self.selected_dest_dir = ""
        self.total_photos = 0
        self.errors = []

        self.gui_setup()

    def gui_setup(self):
        """Creates high level framing for the GUI interface where widgets will be placed"""
        notebook = ttk.Notebook(self)
        notebook.grid(column=0, row=0)

        # create tabs
        self.fm_tab = ttk.Frame(notebook, padding=10)
        self.eas_tab = ttk.Frame(notebook, padding=10)

        notebook.add(self.fm_tab, text="FM")
        notebook.add(self.eas_tab, text="EAS")

        self.create_eas_widgets()
        self.create_fm_widgets()

    def create_fm_widgets(self):
        """Creates the widgets for the FM tab"""

        summary = ttk.Label(self.fm_tab,
                            text="Welcome to the FM photo renamer. This app renames photos from Fulcrum using"
                                 "the barcode column from a Fulcrum CSV.\n\n"
                                 "Please select a Fulcrum CSV, the source directory where the photos are stored,"
                                 "and the destination directory where you want the photos to be copied to.\n\n"
                                 "Press the help button for more information and instructions.",
                            wraplength=400,
                            width=70)

        summary.grid(column=0, row=0, columnspan=2, padx=5, pady=10, sticky="w")

        self.fm_csv_label = ttk.Label(self.fm_tab, text="Open CSV File")
        self.fm_source_label = ttk.Label(self.fm_tab, text="Open Source Directory")
        self.fm_dest_label = ttk.Label(self.fm_tab, text="Open Destination Directory")
        self.fm_csv_label.grid(column=0, row=1, sticky="w", padx=5, pady=10)
        self.fm_source_label.grid(column=0, row=2, sticky="w", padx=5, pady=10)
        self.fm_dest_label.grid(column=0, row=3, sticky="w", padx=5, pady=10)

        self.fm_csv_button = ttk.Button(self.fm_tab, text="Select CSV",
                                        command=lambda: self.get_csv(self.fm_csv_label, "FM"))

        self.fm_source_button = ttk.Button(self.fm_tab, text="Select Source Destination",
                                           command=lambda:self.get_source_dir(self.fm_source_label))

        self.fm_dest_button = ttk.Button(self.fm_tab, text="Select Destination Directory",
                                         command=lambda: self.get_destination_dir(self.fm_dest_label))

        self.fm_csv_button.grid(column=1, row=1, sticky="e", padx=5, pady=10)
        self.fm_source_button.grid(column=1, row=2, sticky="e", padx=5, pady=10)
        self.fm_dest_button.grid(column=1, row=3, sticky="e", padx=5, pady=10)

        self.fm_run_button = ttk.Button(self.fm_tab, text="Rename Photos", command=self.run_fm_rename)
        self.fm_run_button.grid(column=1, row=4, sticky="e", padx=5, pady=10)

        self.fm_help_button = ttk.Button(self.fm_tab, text="Help",
                                      command=lambda: webbrowser.open("https://github.com/nicosaboonchi/PhotoRename"))
        self.fm_help_button.grid(column=0, row=4, sticky="w", padx=5, pady=10)

    def create_eas_widgets(self):
        """Creates the widgets for the EAS tab"""

        summary = ttk.Label(self.eas_tab,
                            text="Welcome to the EAS Photo Renamer. This tab is used for renaming San Diego County assets.\n\n"
                                 "Generate a CSV file from Access and add a `source_path` column to the CSV file.\n\n"
                                 "Please select the CSV file and a destination directory where the renamed photos will be stored.\n\n"
                                 "Press the help button for a more detailed walkthrough, error help, and video demo.",
                            wraplength=400,
                            width=70)

        summary.grid(column=0, row=0, columnspan=2, padx=5, pady=10, sticky="w")

        self.eas_csv_label = ttk.Label(self.eas_tab, text="Open CSV File")
        self.eas_dest_label = ttk.Label(self.eas_tab, text="Open Destination Directory")
        self.eas_csv_label.grid(column=0, row=1, sticky="w", padx=5, pady=10)
        self.eas_source_label = ttk.Label(self.eas_tab, text="Open Source Directory")
        self.eas_dest_label.grid(column=0, row=3, sticky="w", padx=5, pady=10)
        self.eas_source_label.grid(column=0, row=2, sticky="w", padx=5, pady=10)

        self.eas_csv_button = ttk.Button(self.eas_tab, text="Select CSV",
                                         command=lambda: self.get_csv(self.eas_csv_label, "EAS"))
        self.eas_source_button = ttk.Button(self.eas_tab, text="Select Source Directory",
                                           command=lambda: self.get_source_dir(self.eas_source_label))
        
        self.eas_dest_button = ttk.Button(self.eas_tab, text="Select Destination Directory",
                                          command=lambda: self.get_destination_dir(self.eas_dest_label))
        
        self.eas_csv_button.grid(column=1, row=1, sticky="e", padx=5, pady=10)
        self.eas_source_button.grid(column=1, row=2, sticky="e", padx=5, pady=10)
        self.eas_dest_button.grid(column=1, row=3, sticky="e", padx=5, pady=10)

        self.eas_run_button = ttk.Button(self.eas_tab, text="Rename Photos", command=self.run_eas_rename)
        self.eas_run_button.grid(column=1, row=4, sticky="e", padx=5, pady=10)

        self.eas_help_button = ttk.Button(self.eas_tab, text="Help",
                                          command=lambda: webbrowser.open("https://github.com/nicosaboonchi/PhotoRename"))
        self.eas_help_button.grid(column=0, row=4, sticky="w", padx=5, pady=10)

    def get_csv(self, label, context):
        """Sets the global variable and gets the total number of photos in the CSV
        a context variable is passed since the EAS and FM CSVs are different."""
        self.selected_csv = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")],
                                                          initialdir=os.path.expanduser("~/Documents"))
        if self.selected_csv:
            label.config(text=f"{os.path.basename(self.selected_csv)}")
            self.total_photos = self.get_num_photos(context)

    def get_source_dir(self, label):
        """Used for the source dir button. Asks for folder from user and sets to global"""
        self.selected_source_dir = filedialog.askdirectory(initialdir=os.path.expanduser("~/Documents"))
        if self.selected_source_dir:
            label.config(text=f"{self.selected_source_dir}")

    def get_destination_dir(self, label):
        """Used for the dest button. Asks for folder from user and sets to global"""
        self.selected_dest_dir = filedialog.askdirectory(initialdir=os.path.expanduser("~/Documents"))
        if self.selected_dest_dir:
            label.config(text=f"{self.selected_dest_dir}")

    def run_fm_rename(self):
        """Renaming photo logic for FM. Requires a CSV file with a column named barcode and photos.
        Fulcrum export should already contain these columns."""
        if not (self.selected_csv and self.selected_source_dir and self.selected_dest_dir):
            messagebox.showerror(message="Please select valid CSV file, source directory, and destination directory")
            return

        processed_photos = 0

        # hide the buttons when ran
        self.fm_run_button.grid_forget()
        self.fm_help_button.grid_forget()

        # Create progress bar
        progress_bar = ttk.Progressbar(self.fm_tab, orient="horizontal", mode="determinate", length=300,
                                       maximum=self.total_photos)
        progress_label = ttk.Label(self.fm_tab, text=f"Processed {processed_photos} / {self.total_photos}")
        progress_bar.grid(column=0, row=4, sticky=(W, E), padx=5, pady=10, columnspan=2)
        progress_label.grid(column=0, row=5, padx=5, pady=10, columnspan=2)

        time_start = time.time()

        try:
            with open(self.selected_csv, newline="") as csvfile:
                reader = DictReader(csvfile)

                # store each row barcode and photos
                for row in reader:
                    barcode = row["barcode"]
                    photos = row["photos"].split(",") # photos are separated my commas

                    # creates index for each photo and creates the new names and paths
                    for idx, img in enumerate(photos):
                        org_photo = os.path.join(self.selected_source_dir, img + ".jpg")
                        new_photo_name = f"{barcode} - {idx + 1}.jpg"
                        new_photo_dest = os.path.join(self.selected_dest_dir, new_photo_name)

                        if os.path.exists(new_photo_dest):
                            self.errors.append(f"{new_photo_name} already exists skipping")
                            continue
                        try:
                            shutil.copy(org_photo, new_photo_dest)
                        except FileNotFoundError:
                            self.errors.append(f"{img} not found in source directory")
                        except Exception as error:
                            self.errors.append(f"Error copying {img}: {error}")

                        # progress bar updates every 25 photos
                        processed_photos += 1
                        if (processed_photos % 25 == 0) or (processed_photos % self.total_photos == 0):
                            progress_bar["value"] = processed_photos
                            progress_label.config(text=f"Processed {processed_photos} / {self.total_photos}")
                            self.update()

        except Exception as error:
            messagebox.showerror(message=f"Error reading CSV file: {error}")
            return

        time_end = time.time()
        total_time = time_end - time_start

        if self.errors:
            with open(f"{self.selected_source_dir}/errors.txt", "w") as errorfile:
                for err in self.errors:
                    errorfile.write(f"{time.asctime()}\t{err}\n")

        messagebox.showinfo(message=f"Photos have been renamed with {len(self.errors)} errors\n"
                                    f" in {total_time:.2f} seconds, please check error file for any errors")

        self.destroy()

    def run_eas_rename(self):
        """Renaming logic for EAS. CSV requires columns: source_path, org_name, new_name, folder.
        CSV can be created from the Access database but a source_path will still need to be provided."""
        if not (self.selected_csv and self.selected_dest_dir):
            messagebox.showerror(message="Please select valid CSV file and destination directory")
            return

        processed_photos = 0

        # hide the run and help buttons
        self.eas_run_button.grid_forget()
        self.eas_help_button.grid_forget()

        # create and show progress bar
        progress_bar = ttk.Progressbar(self.eas_tab, orient="horizontal", mode="determinate", length=300,
                                       maximum=self.total_photos)
        progress_label = ttk.Label(self.eas_tab, text=f"Processed {processed_photos} / {self.total_photos}")
        progress_bar.grid(column=0, row=4, sticky=(W, E), padx=5, pady=10, columnspan=2)
        progress_label.grid(column=0, row=5, padx=5, pady=10, columnspan=2)

        time_start = time.time()

        with open(self.selected_csv, newline="") as csvfile:
            reader = DictReader(csvfile)

            # iterate each row storing the info
            for row in reader:
                org_name = row["org_name"]
                new_name = row["new_name"]
                folder = row["folder"]

                # creates new paths
                org_path = os.path.join(self.selected_source_dir, org_name)
                folder_dir = os.path.join(self.selected_dest_dir, folder)
                new_img_path = os.path.join(folder_dir, new_name)

                if os.path.isdir(folder_dir):
                    pass
                else:
                    os.makedirs(folder_dir)

                if os.path.exists(new_img_path):
                    pass
                else:
                    try:
                        shutil.copy(org_path, new_img_path)
                    except FileNotFoundError:
                        print(f"{org_name} not found")
                    except Exception as error:
                        print(f"Error copying {org_name}: {error}")

                    # update progress bar every 25 photos
                    processed_photos += 1
                    if processed_photos % 25 == 0:
                        progress_bar["value"] = processed_photos
                        progress_label.config(text=f"Processed {processed_photos} / {self.total_photos}")
                        self.update()

        time_end = time.time()
        total_time = time_end - time_start

        messagebox.showinfo(message=f"Photos have been renamed in {total_time:.2f} seconds")

        self.destroy()

    def get_num_photos(self, context):
        """When CSV is selected it will get the number of photos in the CSV depending on
        which CSV is provided."""
        total_photos = 0
        with open(self.selected_csv, newline="") as csvfile:
            reader = csv.DictReader(csvfile)

            if context == "FM":
                required_fields = {"photos", "barcode"}
                if not required_fields.issubset(reader.fieldnames):
                    messagebox.showerror(message="CSV does not contain either 'photos' or 'barcode' column")
                    return

                for row in reader:
                    photos = row["photos"].split(",")
                    total_photos += len(photos)

            elif context == "EAS":
                required_fields = {"org_name", "new_name", "folder"}
                if  not required_fields.issubset(reader.fieldnames):
                    messagebox.showerror(message="CSV missing 'org_name', 'new_name', 'folder'")
                    return

                for _ in reader:
                    total_photos += 1

        return total_photos

if __name__ == "__main__":
    app = PhotoRenameApp()
    app.mainloop()