# **Photo Renamer App**

This app renames photos using information from a CSV file. It simplifies the process of renaming photos based on barcodes and ensures that each image follows the format: `barcode_1.jpg`, `barcode_2.jpg`, and so on.

## **Getting Started with Facilities Management** 🚀

### 1. **Download the CSV File**
   - From **Fulcrum**, export the CSV file by checking the "Include Photos" option.
   - Ensure the file format is set to **CSV**, and leave the **Date Range** blank. This will export all relevant data.
   - Once the export is complete, download the CSV file from Fulcrum.

### 2. **Unzip the Folder**
   - Unzip the folder containing the photos and CSV file by right-clicking and selecting **Extract All**. This will expand the contents, including three CSV files and the photos.

### 3. **Choose Storage Location**
   - You can place the unzipped folder on your local machine or a network drive.  
   - For faster performance, store the folder locally.

### 4. **Open the Photo Renamer App**

### 5. **Select the CSV File**
   - Click the **Select CSV** button to open a file dialog. The system will default to your **Documents** folder.  
   - Navigate to the correct folder if needed. The CSV file should have the same name as your Fulcrum app and should not include the words "photo" or "photos."

### 6. **Verify CSV Contents**
   - Ensure that the selected CSV contains two key columns:  
     - `barcode` (for photo renaming)
     - `photos` (with the original image filenames)

### 7. **Select Source Folder**
   - Click **Select Source Destination** to choose the folder containing the original photos. This should match the folder where the CSV is located unless you've moved the files.

### 8. **Verify Source Folder**
   - Double-check that the selected folder contains the photos you want to rename.

### 9. **Select Destination Folder**
   - Click **Select Destination Directory** to choose where the renamed photos will be saved.  
   - If necessary, create a new folder for the renamed files.

### 10. **Confirm Destination Folder**
   - Ensure the correct destination folder is selected.

### 11. **Rename Photos**
   - Click **Rename Photos** to start the renaming process.  
   - The progress bar will update every 25 photos, giving you an indication of the process speed.
   - Depending on the file count and source location, the renaming may take anywhere from a few seconds to a few minutes.

### 12. **Completion Notification**
   - Once the renaming process is complete, a pop-up will inform you of the operation's success. It will display the total time taken and any errors encountered.
   - If errors occur, an `errorslog.txt` file will be generated in the **source directory**.
   - Press **OK** to automatically close the app.

### 13. **Close the App**
   - To manually close the app, click the **X** button.  
   - If a "reporting problem to Windows" prompt appears, feel free to skip it.

---

## **Common Errors & How to Fix Them** 😒

- **Missing `photos` or `barcode` column**:  
  The CSV file is missing one or both of the required columns. Ensure you’ve selected the correct CSV file.
  
- **Photo name already exists**:
  A photo with the same name already exists in the destination folder. **This can be a big problem** since that can imply two different assets have the same barcode number. 
  
- **Image not found in source directory**:  
  The script couldn't locate the original photo in the source folder. This may occur if a photo was deleted, moved, or never existed for the asset in question.
  
- **Error copying image**:  
  A script issue prevented the image from being copied. Try rerunning the app.
  
- **Error reading CSV file**:  
  If the CSV file is corrupt or incorrectly formatted, an error will display with further details.

---

## **Video Tutorial** 🎥  
A demo video is available to walk you through the entire process.
