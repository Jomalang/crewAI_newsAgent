from youtube_transcript_api import YouTubeTranscriptApi
from crewai.tools import BaseTool

class TranscriptTool(BaseTool):
    name: str = "Transcript Tool"
    description: str = "A tool to get the transcript of a given youtube video"

    def _run(self, url: str) -> str:
        try:
            video_id = url.split("=")[1]
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'ko'])

            transcript_text = ""
            for i in transcript:
                transcript_text += i['text']

            return transcript_text
        except Exception as e:
            return f"Error: {e}"


