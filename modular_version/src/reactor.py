import json

class VideoReactor:
    def __init__(self, model, character_trait=None):
        self.model = model
        self.video_data = None
        self.last_reaction_time = None
        self.character_trait = character_trait or "enthusiastic commentator"
    
    def set_character_trait(self, new_trait):
        """Change the character trait of the reactor"""
        self.character_trait = new_trait
    
    def load_video_analysis(self, json_path):
        """Load the video analysis from JSON file"""
        try:
            with open(json_path, 'r') as f:
                self.video_data = json.load(f)
        except Exception as e:
            raise ValueError(f"Error loading video analysis: {str(e)}")
    
    def _get_context_until_time(self, time_stamp):
        """Get video context up to specified timestamp"""
        if not self.video_data:
            return "No video data loaded"
            
        context = []
        for part in self.video_data:
            for chunk in part['chunks']:
                if chunk['time_end'] <= time_stamp:
                    context.append(chunk['description'])
                    
        return "\n".join(context[-3:])  # Return last 3 chunks for context
    
    def react_to_timestamp(self, time_stamp, query, character_trait=None):
        """Generate a reaction to a specific timestamp"""
        if character_trait:
            self.character_trait = character_trait
            
        context = self._get_context_until_time(time_stamp)
        prompt = f"""
        As a {self.character_trait}, respond to this video context:
        {context}
        
        User's question/prompt: {query}
        """
        
        try:
            response = self.model.generate_content(prompt)
            self.last_reaction_time = time_stamp
            return response.text
        except Exception as e:
            return f"Error generating reaction: {str(e)}"
    
    def continue_conversation(self, query):
        """Continue conversation about the last reacted timestamp"""
        if not self.last_reaction_time:
            return "No previous context available. Please react to a timestamp first."
            
        return self.react_to_timestamp(self.last_reaction_time, query)
