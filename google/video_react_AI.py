# Import necessary libraries
import google.generativeai as genai
import os
import time
import json
from pathlib import Path
import cv2  # for video processing
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv

"""
Section 1: API Configuration
"""

# Load environment variables from .env file
load_dotenv()

def configure_api_direct():
    """
    Load API key from .env file
    Make sure to create a .env file with your GEMINI_API_KEY
    """
    API_KEY = os.getenv('GEMINI_API_KEY')
    if not API_KEY:
        raise ValueError("No API key found. Please set GEMINI_API_KEY in your .env file")
    genai.configure(api_key=API_KEY)
    return genai.GenerativeModel(model_name='gemini-1.5-flash-latest')

"""
Section 2: Video Processing Setup
"""

def load_local_video(video_path):
    """
    Load and validate a local video file
    Returns: (success, video_info)
    """
    try:
        # Open video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return False, "Error: Could not open video file"

        # Get video properties
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        duration = total_frames / fps
        
        video_info = {
            "path": video_path,
            "total_frames": total_frames,
            "fps": fps,
            "duration": duration,
            "total_seconds": int(duration)
        }
        
        cap.release()
        return True, video_info
        
    except Exception as e:
        return False, f"Error loading video: {str(e)}"

class VideoProcessor:
    def __init__(self, model):
        self.model = model
        self.prompt_template = '''
        1) Describe any dialogue or audio content.
        2) Describe visible actions and character movements.
        3) Summarize visual context in the background or scene.
        '''
    
    def process_video(self, video_path):
        """
        Process video file and generate analysis in chunks
        """
        # First load and validate the local video
        success, video_info = load_local_video(video_path)
        if not success:
            raise ValueError(video_info)  # video_info contains error message
            
        print(f"Video loaded successfully:")
        print(f"Duration: {video_info['duration']:.2f} seconds")
        print(f"FPS: {video_info['fps']}")
        print(f"Total frames: {video_info['total_frames']}")
        
        # Upload video to Gemini API
        try:
            uploaded_video = genai.upload_file(video_path)
        except Exception as e:
            raise ValueError(f"Error uploading video to Gemini: {str(e)}")
        
        # Wait for processing
        while uploaded_video.state.name == "PROCESSING":
            print("Processing video...")
            time.sleep(5)
            uploaded_video = genai.get_file(uploaded_video.name)
            print(f"Status: {uploaded_video.state.name}")

        return self._analyze_video_chunks(uploaded_video, video_info['total_seconds'], 10)

    def _analyze_video_chunks(self, uploaded_video, total_duration, chunk_size):
        """
        Analyze video in chunks and generate JSON output
        """
        chunk_results = []
        part_count = 1

        for start_time in range(0, total_duration, chunk_size):
            end_time = min(start_time + chunk_size, total_duration)
            part_data = []

            # Process each 1-second segment
            for i in range(start_time, end_time):
                prompt = self.prompt_template + f"\nAnalyze the scene from {i} to {i + 1} seconds."
                try:
                    response = self.model.generate_content([prompt, uploaded_video])
                    chunk_data = {
                        "time_start": f"00:00:{i:02d}",
                        "time_end": f"00:00:{i+1:02d}",
                        "description": response.text.strip()
                    }
                    part_data.append(chunk_data)
                    print(f"Processed chunk {i}")
                except Exception as e:
                    print(f"Error processing chunk {i}: {e}")

            chunk_results.append({
                "part": part_count,
                "time_start": f"00:00:{start_time:02d}",
                "time_end": f"00:00:{end_time:02d}",
                "chunks": part_data
            })
            part_count += 1

        return chunk_results

"""
Section 2: Video File Selection
"""

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
        # Initialize Tkinter root window
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        # Open file dialog
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
        # Direct path input
        file_path = input("\nEnter the full path to your video file: ").strip()
        
        # Remove quotes if present
        file_path = file_path.strip("'\"")
        
        if os.path.isfile(file_path):
            return file_path
        else:
            print(f"Error: File not found at {file_path}")
            return None
            
    elif choice == "3":
        # Use default videos directory
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
            print("No video files found in the default directory.")
            return None
            
        while True:
            try:
                choice = int(input("\nSelect video number (or 0 to cancel): "))
                if choice == 0:
                    return None
                if 1 <= choice <= len(video_files):
                    return os.path.join(videos_dir, video_files[choice - 1])
                print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    else:
        print("Invalid option selected.")
        return None

"""
Section 3: LLM Interaction
"""

class VideoReactor:
    def __init__(self, model, character_trait=None):
        self.model = model
        self.video_data = None
        self.last_reaction_time = None
        self.character_trait = character_trait or "enthusiastic commentator"

    def set_character_trait(self, new_trait):
        """Change the character trait of the reactor"""
        self.character_trait = new_trait
        return f"Character trait changed to: {new_trait}"
    
    def load_video_analysis(self, json_path):
        """Load the video analysis from JSON file"""
        try:
            with open(json_path, 'r') as f:
                self.video_data = json.load(f)
            print("Video analysis loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading video analysis: {e}")
            return False
    
    def _get_context_until_time(self, time_stamp):
        """Get video context up to specified timestamp"""
        relevant_context = []
        for part in self.video_data:
            for chunk in part["chunks"]:
                if chunk["time_start"] <= time_stamp:
                    relevant_context.append(
                        f"{chunk['time_start']} - {chunk['time_end']}: {chunk['description']}"
                    )
                else:
                    break
        return "\n".join(relevant_context)
    
    def react_to_timestamp(self, time_stamp, query, character_trait=None):
        """Generate a reaction to a specific timestamp"""
        if character_trait:
            self.character_trait = character_trait
            
        context = self._get_context_until_time(time_stamp)
        prompt = f"""
        You are a {self.character_trait}. Based on the following video context up to {time_stamp},
        provide a reaction to the user's question: '{query}'
        
        Video Context:
        {context}
        """
        
        try:
            response = self.model.generate_content(prompt)
            self.last_reaction_time = time_stamp
            return response.text
        except Exception as e:
            return f"Error generating reaction: {e}"
    
    def continue_conversation(self, query):
        """Continue conversation about the last reacted timestamp"""
        if not self.last_reaction_time:
            return "Please first react to a specific timestamp using react_to_timestamp()"
            
        context = self._get_context_until_time(self.last_reaction_time)
        prompt = f"""
        You are a {self.character_trait}. Based on the video context up to {self.last_reaction_time},
        continue the conversation by responding to: '{query}'
        
        Video Context:
        {context}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error continuing conversation: {e}"

def main():
    try:
        # Configure API
        model = configure_api_direct()
        
        while True:
            try:
                process_new_video = input("Do you want to process a new video? (yes/no): ").lower()
                if process_new_video not in ['yes', 'no']:
                    print("Please enter 'yes' or 'no'")
                    continue
                    
                if process_new_video == 'no':
                    break
                    
                # Select and process video
                video_path = select_video_file()
                if not video_path:
                    print("No valid video file selected. Please try again.")
                    continue
                    
                # Process the video
                processor = VideoProcessor(model)
                results = processor.process_video(video_path)
                
                # Save results
                output_file = f"video_analysis_{int(time.time())}.json"
                with open(output_file, 'w') as f:
                    json.dump(results, f, indent=2)
                print(f"\nAnalysis saved to {output_file}")
                
                # Initialize reactor with user-defined character trait
                print("\nChoose a character trait for the AI commentator.")
                print("Examples: enthusiastic commentator, movie critic, technical analyst, casual observer")
                character_trait = input("Enter character trait (press Enter for default 'enthusiastic commentator'): ").strip()
                reactor = VideoReactor(model, character_trait if character_trait else None)
                reactor.load_video_analysis(output_file)
                
                # Interactive reaction loop
                while True:
                    try:
                        print("\nCommands:")
                        print("- Enter timestamp (MM:SS) for video analysis")
                        print("- Type 'trait' to change AI character trait")
                        print("- Type 'quit' to exit")
                        
                        command = input("\nEnter command: ").strip().lower()
                        
                        if command == 'quit':
                            break
                        elif command == 'trait':
                            new_trait = input("Enter new character trait: ").strip()
                            print(reactor.set_character_trait(new_trait))
                            continue
                            
                        # Process timestamp analysis
                        timestamp = command
                        query = input("What would you like to know about this moment? ")
                        reaction = reactor.react_to_timestamp(timestamp, query)
                        print("\nReaction:", reaction)
                        
                        while True:
                            follow_up = input("\nAny follow-up questions? (yes/no): ").lower()
                            if follow_up == 'no':
                                break
                            elif follow_up == 'yes':
                                query = input("What would you like to know? ")
                                response = reactor.continue_conversation(query)
                                print("\nResponse:", response)
                            else:
                                print("Please enter 'yes' or 'no'")
                                
                    except KeyboardInterrupt:
                        print("\nExiting reaction loop...")
                        break
                    except Exception as e:
                        print(f"Error during reaction: {str(e)}")
                        continue
                        
            except KeyboardInterrupt:
                print("\nProgram interrupted by user")
                break
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                continue
                
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"Fatal error: {str(e)}")
    finally:
        print("\nThank you for using the Video Analysis tool!")

if __name__ == "__main__":
    main()