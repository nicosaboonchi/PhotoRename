import os
import csv
import shutil
import time
import webbrowser
from csv import DictReader
from tkinter import *
from tkinter import filedialog, messagebox, ttk

class PhotoRenameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Rename App")
        self.root.eval("tk::PlaceWindow . center")
        self.root.resizable(False, False)

        self.selected_csv = ""
        self.selected_source_dir = ""
        self.selected_dest_dir = ""
        self.total_photos = 0

        self.gui_setup()

    def gui_setup(self):
        notebook = ttk.Notebook(self.root)
        notebook.grid(column=0, row=0)

        # create tabs
        self.fm_tab = ttk.Frame(notebook, padding=10)
        self.eas_tab = ttk.Frame(notebook, padding=10)

        notebook.add(self.fm_tab, text="FM")
        notebook.add(self.eas_tab, text="EAS")

        self.create_eas_widgets()
        self.create_fm_widgets()

    def create_fm_widgets(self):
        summary = ttk.Label(self.fm_tab, text="Welcome to the FM photo renamer. This app renames photos from Fulcrum using\n"+
                                 "the barcode column from a Fulcrum CSV.\n\n" +
                                 "Please select a Fulcrum CSV, the source directory where the photos are stored,\n"+
                                 "and the destination directory where you want the photos to be copied to.\n\n" +
                                 "Press the help button for more information and instructions.")
        summary.grid(column=0, row=0, columnspan=2, padx=5, pady=10, sticky="w")

        self.fm_csv_label = ttk.Label(self.fm_tab, text="Open CSV File")
        self.fm_source_label = ttk.Label(self.fm_tab, text="Open Source Directory")
        self.fm_dest_label = ttk.Label(self.fm_tab, text="Open Destination Directory")
        self.fm_csv_label.grid(column=0, row=1, sticky="w", padx=5, pady=10)
        self.fm_source_label.grid(column=0, row=2, sticky="w", padx=5, pady=10)
        self.fm_dest_label.grid(column=0, row=3, sticky="w", padx=5, pady=10)

        self.fm_csv_button = ttk.Button(self.fm_tab, text="Select CSV", command=lambda: self.get_csv(self.fm_csv_label))
        self.fm_source_button = ttk.Button(self.fm_tab, text="Select Source Destination", command=lambda:self.get_source_dir(self.fm_source_label))
        self.fm_dest_button = ttk.Button(self.fm_tab, text="Select Destination Directory", command=lambda: self.get_destination_dir(self.fm_dest_label))
        self.fm_csv_button.grid(column=1, row=1, sticky="e", padx=5, pady=10)
        self.fm_source_button.grid(column=1, row=2, sticky="e", padx=5, pady=10)
        self.fm_dest_button.grid(column=1, row=3, sticky="e", padx=5, pady=10)

        self.fm_run_button = ttk.Button(self.fm_tab, text="Rename Photos", command=self.run_fm_rename)
        self.fm_run_button.grid(column=1, row=4, sticky="e", padx=5, pady=10)

        self.fm_help_button = ttk.Button(self.fm_tab, text="Help",
                                      command=lambda: webbrowser.open("https://github.com/nicosaboonchi/PhotoRename"))
        self.fm_help_button.grid(column=0, row=4, sticky="w", padx=5, pady=10)

    def create_eas_widgets(self):
        summary = ttk.Label(self.eas_tab, text="Welcome to the EAS Photo Renamer...THis is for the county of san diego\n"
                                               +"to rename photos that is generated from access csv file")
        summary.grid(column=0, row=0, columnspan=2, padx=5, pady=10, sticky="w")

        self.eas_csv_label = ttk.Label(self.eas_tab, text="Open CSV File")
        self.eas_dest_label = ttk.Label(self.eas_tab, text="Open Destination Directory")
        self.eas_csv_label.grid(column=0, row=1, sticky="w", padx=5, pady=10)
        self.eas_dest_label.grid(column=0, row=2, sticky="w", padx=5, pady=10)

        self.eas_csv_button = ttk.Button(self.eas_tab, text="Select CSV", command=lambda: self.get_csv(self.eas_csv_label))
        self.eas_dest_button = ttk.Button(self.eas_tab, text="Select Destination Directory", command=lambda: self.get_destination_dir(self.eas_dest_label))
        self.eas_csv_button.grid(column=1, row=1, sticky="e", padx=5, pady=10)
        self.eas_dest_button.grid(column=1, row=2, sticky="e", padx=5, pady=10)

        self.eas_run_button = ttk.Button(self.eas_tab, text="Rename Photos", command=self.run_eas_rename)
        self.eas_run_button.grid(column=1, row=4, sticky="e", padx=5, pady=10)

    def get_csv(self, label):
        self.selected_csv = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")],
                                                          initialdir=os.path.expanduser("~/Documents"))
        if self.selected_csv:
            label.config(text=f"{os.path.basename(self.selected_csv)}")
            self.total_photos = self.get_num_photos()
            print(f"total photos: {self.total_photos}")

    def get_source_dir(self, label):
        self.selected_source_dir = filedialog.askdirectory(initialdir=os.path.expanduser("~/Documents"))
        if self.selected_source_dir:
            label.config(text=f"{self.selected_source_dir}")

    def get_destination_dir(self, label):
        self.selected_dest_dir = filedialog.askdirectory(initialdir=os.path.expanduser("~/Documents"))
        if self.selected_dest_dir:
            label.config(text=f"{self.selected_dest_dir}")

    def run_fm_rename(self):

        processed_photos = 0

        self.fm_run_button.grid_forget()
        self.fm_help_button.grid_forget()

        progress_bar = ttk.Progressbar(self.fm_tab, orient="horizontal", mode="determinate", length=300,
                                       maximum=self.total_photos)
        progress_label = ttk.Label(self.fm_tab, text=f"Processed {processed_photos} / {self.total_photos}")
        progress_bar.grid(column=0, row=4, sticky=(W, E), padx=5, pady=10, columnspan=2)
        progress_label.grid(column=0, row=5, padx=5, pady=10, columnspan=2)

        time_start = time.time()

        try:
            with open(self.selected_csv, newline="") as csvfile:
                reader = DictReader(csvfile)

                for row in reader:
                    barcode = row["barcode"]
                    photos = row["photos"].split(",")

                    for idx, img in enumerate(photos):
                        org_photo = os.path.join(self.selected_source_dir, img + ".jpg")
                        new_photo_name = f"{barcode} - {idx + 1}.jpg"
                        new_photo_dest = os.path.join(self.selected_dest_dir, new_photo_name)

                        if os.path.exists(new_photo_dest):
                            pass

                        try:
                            shutil.copy(org_photo, new_photo_dest)
                        except FileNotFoundError:
                            print(f"{img} not found")
                        except Exception as error:
                            print(f"Error copying {img}: {error}")

                        processed_photos += 1
                        if processed_photos % 25 == 0:
                            progress_bar["value"] = processed_photos
                            progress_label.config(text=f"Processed {processed_photos} / {self.total_photos}")
                            root.update_idletasks()

        except Exception as error:
            messagebox.showerror(message=f"Error reading CSV file: {error}")
            return

        time_end = time.time()
        total_time = time_end - time_start

        messagebox.showinfo(message=f"Photos have been renamed in {total_time:.2f} seconds")

        root.destroy()

    def run_eas_rename(self):
        processed_photos = 0

        self.eas_run_button.grid_forget()

        progress_bar = ttk.Progressbar(self.eas_tab, orient="horizontal", mode="determinate", length=300,
                                       maximum=self.total_photos)
        progress_label = ttk.Label(self.eas_tab, text=f"Processed {processed_photos} / {self.total_photos}")
        progress_bar.grid(column=0, row=4, sticky=(W, E), padx=5, pady=10, columnspan=2)
        progress_label.grid(column=0, row=5, padx=5, pady=10, columnspan=2)

        time_start = time.time()

        with open(self.selected_csv, newline="") as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                source_path = row["source_path"]
                org_name = row["org_name"]
                new_name = row["new_name"]
                folder = row["folder"]

                org_path = os.path.join(source_path, org_name)
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

                    processed_photos += 1
                    if processed_photos % 25 == 0:
                        progress_bar["value"] = processed_photos
                        progress_label.config(text=f"Processed {processed_photos} / {self.total_photos}")
                        root.update_idletasks()

        time_end = time.time()
        total_time = time_end - time_start

        messagebox.showinfo(message=f"Photos have been renamed in {total_time:.2f} seconds")

        root.destroy()

    def get_num_photos(self):
        total_photos = 0
        with open(self.selected_csv, newline="") as csvfile:
            reader = csv.DictReader(csvfile)

            if "photos" in reader.fieldnames:
                for row in reader:
                    photos = row["photos"].split(",")
                    total_photos += len(photos)

            elif "new_name" in reader.fieldnames:
                for row in reader:
                    total_photos += 1

        return total_photos


if __name__ == "__main__":
    root = Tk()
    app = PhotoRenameApp(root)
    root.mainloop()