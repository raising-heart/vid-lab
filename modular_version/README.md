# Video React AI - Modular Version

An intelligent video analysis system that uses Google's Gemini API to process videos and generate AI-powered reactions and commentary. The system can analyze video content, understand context, and engage in conversations about specific moments in the video.

## Features

- **Smart Video Analysis**: Processes videos to understand scenes, dialogue, and actions
- **Interactive AI Commentary**: Generate context-aware reactions to specific moments
- **Customizable AI Personalities**: Switch between different commentator styles
- **Conversational Memory**: Maintain context for follow-up questions
- **Flexible File Selection**: Choose videos via GUI, direct path, or default folder

## Project Structure

```
modular_version/
├── src/
│   ├── config.py         # API configuration and setup
│   ├── video_processor.py # Video analysis and processing
│   ├── file_selector.py  # Video file selection utilities
│   ├── reactor.py        # AI reaction generation
│   └── main.py          # Main application entry point
├── output/              # Directory for analysis output files
│   └── video_analysis.json  # Generated video analysis data
├── .env                 # Environment variables (API keys)
├── requirements.txt     # Project dependencies
└── README.md           # Documentation
```

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Supported video formats: MP4, AVI, MOV, MKV

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd modular_version
   ```

2. Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```bash
   python src/main.py
   ```

2. Select a video file using one of three methods:
   - GUI file picker
   - Direct path input
   - Default videos folder

3. Wait for the video analysis to complete. The analysis will be saved to `output/video_analysis.json`.

4. Use the following commands to interact with the AI:

   ```
   1. react <timestamp> <query>
      Example: react 00:00:30 what is happening in this scene?
      - Generate AI reaction for a specific moment
      - Timestamp format: HH:MM:SS or seconds (e.g., 00:00:30 or 30)
   
   2. continue <query>
      Example: continue what happened next?
      - Ask follow-up questions about the same scene
   
   3. character <new_trait>
      Example: character movie critic
      - Change the AI's personality
      - Suggestions: movie critic, sports commentator, comedian, film director
   ```

## Example Session

```
> react 00:00:30 describe the main action in this scene
[AI responds with scene description]

> continue what emotions are the characters showing?
[AI analyzes emotional content]

> character movie critic
Character trait changed to: movie critic

> react 00:01:00 analyze the cinematography
[AI responds with critical analysis]
```

## Error Handling

- If video file is invalid or corrupted, the system will display an error message
- API connection issues will be reported with specific error details
- Invalid commands will show usage instructions

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.
