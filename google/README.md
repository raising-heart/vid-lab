# Video Analysis Tool

## Overview
The Video Analysis Tool is a Python application that utilizes Google Generative AI to analyze video content. It processes videos to generate descriptive analyses based on visual and audio elements, allowing users to interact with the AI for insights and commentary.

## Features
- Load and validate local video files.
- Upload videos to the Gemini API for processing.
- Analyze video content in chunks and generate JSON output.
- Interactive command-line interface for user queries and reactions.
- Customizable AI character traits for varied commentary styles.

## Requirements
- Python 3.x
- Required libraries:
  - `google.generativeai`
  - `opencv-python`
  - `tkinter`
  - `python-dotenv`
  - `json`
  - `os`
  - `time`
  
You can install the required libraries using pip:

## Setup
1. Clone the repository or download the project files.
2. Create a `.env` file in the project directory and add your API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Ensure you have video files in supported formats (e.g., `.mp4`, `.avi`, `.mov`, `.mkv`).

## Usage
1. Run the application:
   ```bash
   python video_react_AI.py
   ```
2. Follow the prompts to select a video file and choose how to process it.
3. Interact with the AI by entering timestamps and asking questions about the video content.
4. Change the AI's character trait for different commentary styles.

## Example Output
The application provides detailed analyses of video segments, as well as user-defined reactions based on the context of the video. An example output is included in `Example_Output.txt`.

## Acknowledgments
- This project utilizes Google Generative AI for video analysis.
- Special thanks to the contributors and the open-source community.
