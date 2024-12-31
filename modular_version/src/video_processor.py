import cv2
import time
import google.generativeai as genai

def load_local_video(video_path):
    """
    Load and validate a local video file
    Returns: (success, video_info)
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return False, "Error: Could not open video file"

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
        success, video_info = load_local_video(video_path)
        if not success:
            raise ValueError(video_info)
            
        print(f"Video loaded successfully:")
        print(f"Duration: {video_info['duration']:.2f} seconds")
        print(f"FPS: {video_info['fps']}")
        print(f"Total frames: {video_info['total_frames']}")
        
        try:
            uploaded_video = genai.upload_file(video_path)
        except Exception as e:
            raise ValueError(f"Error uploading video to Gemini: {str(e)}")
        
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
