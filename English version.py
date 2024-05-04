import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import subprocess
import os
import threading

# Audio formats
audio_formats = ['mp3', 'aac', 'wav', 'wma', 'flac', 'm4a', 'mka', 'mp2', 'mpa', 'ape', 'ogg', 'ra', 'wv', 'tta', 'ac3', 'dts']

# Video formats
video_formats = ['avi', 'asf', 'wmv', 'flv', 'mkv', 'mov', '3gp', 'mp4', 'mpg', 'mpeg', 'vob', 'rm', 'rmvb', 'ts']

def select_source_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        source_entry.config(state=tk.NORMAL)
        source_entry.delete(0, tk.END)
        source_entry.insert(0, folder_path)
        source_entry.config(state="readonly")

def select_destination_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        destination_entry.config(state=tk.NORMAL)
        destination_entry.delete(0, tk.END)
        destination_entry.insert(0, folder_path)
        destination_entry.config(state="readonly")

def convert_media_files():
    source_folder = source_entry.get()
    destination_folder = destination_entry.get()
    output_format = output_format_entry.get()

    if not (source_folder and destination_folder and output_format):
        messagebox.showerror("Error", "Please select source folder, destination folder, and output format")
        return

    if output_format not in audio_formats + video_formats:
        messagebox.showerror("Error", "Unsupported output format")
        return

    response = messagebox.askquestion("Notice", "Are you sure you want to convert in batch?")
    if response != 'yes':
        return

    convert_button.config(state=tk.DISABLED)
    root.withdraw()
    info_window = tk.Toplevel(root)
    info_window.title("Converting")
    info_window.attributes("-topmost", True)
    info_window.geometry("300x100")

    progress_var = tk.DoubleVar()
    progress_bar = Progressbar(info_window, variable=progress_var, maximum=100)
    progress_bar.pack(pady=10)

    label = tk.Label(info_window, text="Converting, please wait...", font=("Arial", 16))
    label.pack(pady=5)

    center_window(info_window)

    thread = threading.Thread(target=convert, args=(source_folder, destination_folder, output_format, info_window, progress_var))
    thread.start()

def check_media_file(file_path):
    ffprobe_cmd = ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=codec_type", "-of", "default=noprint_wrappers=1:nokey=1", file_path]
    process = subprocess.Popen(ffprobe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        codec_type = output.decode().strip()
        return codec_type == 'audio' or codec_type == 'video'
    return False

def convert(source_folder, destination_folder, output_format, info_window, progress_var):
    try:
        ffmpeg_cmd = ["ffmpeg", "-hide_banner", "-y"]

        media_files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]  # Get all files in the source folder
        if not any(check_media_file(os.path.join(source_folder, file)) for file in media_files):
            raise ValueError("No audio or video files in the source folder")

        num_files = len(media_files)

        for i, file in enumerate(media_files):
            input_file_path = os.path.join(source_folder, file)
            if not check_media_file(input_file_path):
                continue
            output_file_name = f"{os.path.splitext(file)[0]}.{output_format}"
            output_file_path = os.path.join(destination_folder, output_file_name)
            cmd = ffmpeg_cmd + ["-i", input_file_path, "-vn", output_file_path]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
            process.communicate()
            
            progress_value = (i + 1) / num_files * 100
            progress_var.set(progress_value)
            info_window.update_idletasks()

        info_window.destroy()
        root.deiconify()
        messagebox.showinfo("Notice", "Batch conversion completed!")
    except Exception as e:
        info_window.destroy()
        root.deiconify()
        messagebox.showerror("Error", f"Conversion error: {str(e)}")
    finally:
        convert_button.config(state=tk.NORMAL)

def center_window(window):
    window.update_idletasks()
    width = window.winfo_reqwidth()
    height = window.winfo_reqheight()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

root = tk.Tk()
root.title("Batch Media File Conversion")
root.geometry("500x250")
root.resizable(False, False)

source_label = tk.Label(root, text="Source Folder:")
source_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

source_entry = tk.Entry(root, width=30, state="readonly")
source_entry.grid(row=0, column=1, padx=10, pady=10)

source_button = tk.Button(root, text="Select Source Folder", command=select_source_folder)
source_button.grid(row=0, column=2, padx=10, pady=10)

destination_label = tk.Label(root, text="Output Folder:")
destination_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

destination_entry = tk.Entry(root, width=30, state="readonly")
destination_entry.grid(row=1, column=1, padx=10, pady=10)

destination_button = tk.Button(root, text="Select Output Folder", command=select_destination_folder)
destination_button.grid(row=1, column=2, padx=10, pady=10)

output_format_label = tk.Label(root, text="Output Format:")
output_format_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

output_format_entry = tk.Entry(root, width=30)
output_format_entry.grid(row=2, column=1, padx=10, pady=10)

convert_button = tk.Button(root, text="Start Conversion", command=convert_media_files)
convert_button.grid(row=3, column=1, padx=10, pady=10)

def on_closing():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

def center_window(window):
    window.update_idletasks()
    width = window.winfo_reqwidth()
    height = window.winfo_reqheight()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

center_window(root)

root.mainloop()
