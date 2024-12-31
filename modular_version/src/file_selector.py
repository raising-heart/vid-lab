import os
import tkinter as tk
from tkinter import filedialog

def select_video_file():
    """
    Provides multiple ways to select a video file:
    1. GUI file picker
    2. Drag and drop path
    3. Direct path input
    Returns: Selected video file path
    """
    print("\nVideo File Selection Options:")
    print("1. Use GUI file picker")
    print("2. Enter file path directly")
    print("3. Use default videos folder")
    
    choice = input("\nChoose option (1-3): ").strip()
    
    if choice == "1":
        root = tk.Tk()
        root.withdraw()
        
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            print("No file selected.")
            return None
            
        return file_path
        
    elif choice == "2":
        file_path = input("\nEnter the full path to your video file: ").strip()
        file_path = file_path.strip("'\"")
        
        if os.path.isfile(file_path):
            return file_path
        else:
            print(f"Error: File not found at {file_path}")
            return None
            
    elif choice == "3":
        videos_dir = os.path.join(os.path.expanduser("~"), "Videos")
        if not os.path.exists(videos_dir):
            videos_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        
        print(f"\nAvailable videos in {videos_dir}:")
        video_files = []
        
        for file in os.listdir(videos_dir):
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                video_files.append(file)
                print(f"{len(video_files)}. {file}")
        
        if not video_files:
            print("No video files found in default directory.")
            return None
            
        while True:
            try:
                choice = int(input("\nSelect video number (or 0 to cancel): "))
                if choice == 0:
                    return None
                if 1 <= choice <= len(video_files):
                    return os.path.join(videos_dir, video_files[choice-1])
                print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    else:
        print("Invalid option selected.")
        return None
