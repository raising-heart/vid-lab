import json
import os
from config import configure_api_direct
from video_processor import VideoProcessor
from file_selector import select_video_file
from reactor import VideoReactor

def save_analysis(analysis_data, output_path):
    """Save video analysis to JSON file"""
    try:
        with open(output_path, 'w') as f:
            json.dump(analysis_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving analysis: {e}")
        return False

def main():
    # Initialize API and model
    try:
        model = configure_api_direct()
        print("API configured successfully")
    except Exception as e:
        print(f"Error configuring API: {e}")
        return

    # Select video file
    video_path = select_video_file()
    if not video_path:
        print("No video selected. Exiting...")
        return

    # Process video
    processor = VideoProcessor(model)
    try:
        print("\nProcessing video...")
        analysis = processor.process_video(video_path)
        
        # Save analysis
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "video_analysis.json")
        
        if save_analysis(analysis, output_path):
            print(f"\nAnalysis saved to {output_path}")
        
    except Exception as e:
        print(f"Error processing video: {e}")
        return

    # Initialize reactor
    reactor = VideoReactor(model)
    reactor.load_video_analysis(output_path)

    # Interactive loop
    print("\nAvailable Commands:")
    print("\n1. react <timestamp> <query>")
    print("   Example: react 00:00:30 what is happening in this scene?")
    print("   - Generate AI reaction for a specific moment in the video")
    print("   - <timestamp> format: HH:MM:SS or seconds (e.g., 00:00:30 or 30)")
    print("   - <query> can be any question or prompt about that moment")
    
    print("\n2. continue <query>")
    print("   Example: continue what happened next?")
    print("   - Continue the conversation about the previous timestamp")
    print("   - Useful for follow-up questions about the same scene")
    
    print("\n3. character <new_trait>")
    print("   Example: character movie critic")
    print("   - Change how the AI reacts to scenes")
    print("   - Suggestions: movie critic, sports commentator, comedian, film director")
    
    print("\nType 'quit' to exit the program")

    while True:
        try:
            command = input("\nEnter command: ").strip()
            
            if command.lower() == 'quit':
                break
                
            parts = command.split(maxsplit=2)
            
            if not parts:
                continue
                
            cmd = parts[0].lower()
            
            if cmd == 'react' and len(parts) >= 3:
                timestamp = parts[1]
                query = parts[2]
                response = reactor.react_to_timestamp(timestamp, query)
                print(f"\nReaction: {response}")
                
            elif cmd == 'continue' and len(parts) >= 2:
                query = parts[1]
                response = reactor.continue_conversation(query)
                print(f"\nResponse: {response}")
                
            elif cmd == 'character' and len(parts) >= 2:
                new_trait = parts[1]
                reactor.set_character_trait(new_trait)
                print(f"\nCharacter trait changed to: {new_trait}")
                
            else:
                print("Invalid command format. Please try again.")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
