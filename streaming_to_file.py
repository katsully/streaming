from elevenlabs import generate, stream, Voice, VoiceSettings, set_api_key
import os

set_api_key(os.environ.get("ELEVENLABS_API_KEY"))
voice_id=os.environ.get("ELEVENLABS_VOICE_ID")

audio_stream = generate(
	text = "This is a streaming voice! I'm really excited to tell you all about it",
	voice=Voice(
        voice_id=voice_id,
        settings=VoiceSettings(stability=0.35, similarity_boost=0.85, style=0, use_speaker_boost=False)
    ),
    model="eleven_turbo_v2",
	stream=True,
    # default is 128kbps sample rate
    output_format = "mp3_44100_192"
)

with open('output.wav', 'wb') as f:
    for i,chunk in enumerate(audio_stream):
        if chunk: 
            f.write(chunk)