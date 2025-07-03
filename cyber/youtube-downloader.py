from youtube_transcript_api import YouTubeTranscriptApi

video_id = "8kpnSb4yGR0"
ytt_api = YouTubeTranscriptApi()
ytt_api.fetch(video_id)