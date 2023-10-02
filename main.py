import os
import requests
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import time
import threading

def download_file(url, output_dir):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        response = requests.get(url, stream=True, headers=headers)
        response.raise_for_status()

        filename = os.path.join(output_dir, url.split("/")[-1])

        with open(filename, 'wb') as file:
            start_time = time.time()
            file_size = 0

            for data in tqdm(response.iter_content(chunk_size=1024), unit='KB', unit_scale=True):
                file.write(data)
                file_size += len(data)
            
            end_time = time.time()
            elapsed_time = end_time - start_time

            file_info = f"Downloaded file: {os.path.basename(filename)}, File size: {file_size / 1024:.2f} KB, Download time: {elapsed_time:.2f} seconds"
            print(file_info)
            print("=" * len(file_info))

    except Exception as e:
        pass

def select_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

def select_output_dir():
    global output_dir
    output_dir = filedialog.askdirectory(title="Select the folder to save files")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_dir)

def download_files():
    if not file_path:
        error_label.config(text="Select a file for download.")
        return
    
    if not output_dir:
        error_label.config(text="Select a path to save files.")
        return
    
    error_label.config(text="")
    
    try:
        df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
    except Exception as e:
        error_label.config(text=f"Error reading the file: {e}")
        return
    
    parallel_downloads = int(parallel_spinbox.get())
    column_index = int(column_spinbox.get()) - 1
    
    def download_in_thread():
        with ThreadPoolExecutor(parallel_downloads) as executor:
            futures = []
            for _, row in df.iterrows():
                url = row[column_index]
                futures.append(executor.submit(download_file, url, output_dir))

            for future in futures:
                future.result()

        result_label.config(text="Download completed!")
        root.update()

    download_thread = threading.Thread(target=download_in_thread)
    download_thread.start()

root = tk.Tk()
root.title("File Downloader")

input_frame = ttk.Frame(root, padding=10)
button_frame = ttk.Frame(root, padding=10)
status_frame = ttk.Frame(root, padding=10)

select_file_button = ttk.Button(input_frame, text="Select File", command=select_file)
select_output_button = ttk.Button(input_frame, text="Select Output Folder", command=select_output_dir)
download_button = ttk.Button(button_frame, text="Download", command=download_files)

error_label = ttk.Label(status_frame, text="", foreground="red")
result_label = ttk.Label(status_frame, text="")

file_entry = ttk.Entry(input_frame)
output_entry = ttk.Entry(input_frame)

input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")
button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")
status_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

select_file_button.grid(row=0, column=0, padx=5, pady=5)
file_entry.grid(row=0, column=1, padx=5, pady=5)
select_output_button.grid(row=1, column=0, padx=5, pady=5)
output_entry.grid(row=1, column=1, padx=5, pady=5)
download_button.pack(padx=5, pady=5, anchor="w")
error_label.pack(padx=5, pady=5, anchor="w")
result_label.pack(padx=5, pady=5, anchor="w")

column_label = ttk.Label(input_frame, text="Column Index for Download (A=1, B=2, etc.):")
column_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
column_spinbox = ttk.Spinbox(input_frame, from_=1, to=100, width=5)
column_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky="w")
column_spinbox.delete(0, tk.END)
column_spinbox.insert(0, "1")

parallel_label = ttk.Label(input_frame, text="Parallel Downloads:")
parallel_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
parallel_spinbox = ttk.Spinbox(input_frame, from_=1, to=32, width=5)
parallel_spinbox.grid(row=3, column=1, padx=5, pady=5, sticky="w")
parallel_spinbox.delete(0, tk.END)
parallel_spinbox.insert(0, "5")

root.mainloop()
