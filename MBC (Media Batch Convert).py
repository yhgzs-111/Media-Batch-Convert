import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import subprocess
import os
import threading
import ctypes

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

def convert_videos_to_audio():
    source_folder = source_entry.get()
    destination_folder = destination_entry.get()
    audio_format = audio_format_combobox.get()

    if not (source_folder and destination_folder):
        messagebox.showerror("错误", "请选择目标文件夹和输出文件夹")
        return

    has_audio_video_files = check_audio_video_files(source_folder)
    if not has_audio_video_files:
        messagebox.showerror("错误", "目标文件夹无任何音视频文件，请重新选择！")
        return

    response = messagebox.askquestion("提示", "确定要转换吗？")
    if response != 'yes':
        return

    convert_button.config(state=tk.DISABLED)
    root.withdraw()
    info_window = tk.Toplevel(root)
    info_window.title("转换中")
    info_window.attributes("-topmost", True)
    info_window.geometry("300x100")

    label = tk.Label(info_window, text="正在转换，请稍等……", font=("Arial", 16))
    label.pack(pady=20)

    center_window(info_window)

    thread = threading.Thread(target=convert, args=(source_folder, destination_folder, audio_format, info_window))
    thread.start()

def check_audio_video_files(folder):
    audio_video_extensions = {'.mp3', '.aac', '.wav', '.wma', '.cda', '.flac', '.m4a', '.mid', '.mka', '.mp2', '.mpa', '.mpc', '.ape', '.ofr', '.ogg', '.ra', '.wv', '.tta', '.ac3', '.dts', '.avi', '.asf', '.wmv', '.avs', '.flv', '.mkv', '.mov', '.3gp', '.mp4', '.mpg', '.mpeg', '.dat', '.ogm', '.vob', '.rm', '.rmvb', '.ts', '.tp', '.ifo', '.nsv'}

    for file in os.listdir(folder):
        ffprobe_output = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_type", "-of", "csv=p=0", f"{folder}/{file}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        if ffprobe_output.stdout.strip() != '':
            file_extension = os.path.splitext(file)[-1].lower()
            if file_extension in audio_video_extensions:
                return True
    return False

def convert(source_folder, destination_folder, audio_format, info_window):
    try:
        ffmpeg_cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]

        all_files = os.listdir(source_folder)

        for file in all_files:
            output_file_name = f"{os.path.splitext(file)[0]}.{audio_format}"
            output_file_path = os.path.join(destination_folder, output_file_name)
            subprocess.run(ffmpeg_cmd + ["-i", f"{source_folder}/{file}", "-vn", "-f", audio_format, output_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')

        info_window.destroy()
        root.deiconify()
        messagebox.showinfo("提示", "批量转换完成！")
    except Exception as e:
        info_window.destroy()
        root.deiconify()
        ctypes.windll.user32.MessageBoxW(0, f"转换出错: {str(e)}", "错误", 0)
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
root.title("视频/音频批量转换")
root.geometry("500x200")
root.resizable(False, False)

source_label = tk.Label(root, text="目标文件夹:")
source_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

source_entry = tk.Entry(root, width=30, state="readonly")
source_entry.grid(row=0, column=1, padx=10, pady=10)

source_button = tk.Button(root, text="选择目标文件夹", command=select_source_folder)
source_button.grid(row=0, column=2, padx=10, pady=10)

destination_label = tk.Label(root, text="输出文件夹:")
destination_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

destination_entry = tk.Entry(root, width=30, state="readonly")
destination_entry.grid(row=1, column=1, padx=10, pady=10)

destination_button = tk.Button(root, text="选择输出文件夹", command=select_destination_folder)
destination_button.grid(row=1, column=2, padx=10, pady=10)

audio_format_label = tk.Label(root, text="选择输出格式:")
audio_format_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

audio_formats = ["mp3", "flac", "wav"]
audio_format_combobox = ttk.Combobox(root, values=audio_formats, state="readonly")
audio_format_combobox.current(0)
audio_format_combobox.grid(row=2, column=1, padx=10, pady=10)

convert_button = tk.Button(root, text="开始转换", command=convert_videos_to_audio)
convert_button.grid(row=3, column=1, padx=10, pady=10)

def on_closing():
    if messagebox.askokcancel("退出", "确定要退出吗？"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

center_window(root)

root.mainloop()
