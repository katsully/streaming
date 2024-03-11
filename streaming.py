from elevenlabs import generate, stream, Voice, VoiceSettings, set_api_key
import os
import io
from gtts import gTTS 

set_api_key(os.environ.get("ELEVENLABS_API_KEY"))
voice_id=os.environ.get("ELEVENLABS_VOICE_ID")

audio_stream = generate(
	text = "This is a streaming voice!",
	voice=Voice(
        voice_id=voice_id,
        settings=VoiceSettings(stability=0.35, similarity_boost=0.85, style=0, use_speaker_boost=False)
    ),
    model="eleven_turbo_v2",
	stream=True,
    # default is 128kbps sample rate
    output_format = "mp3_44100_192"
)

# need to download mvc, go here: https://mpv.io/
stream(audio_stream)

print(type(audio_stream))

# mp3_file = io.BytesIO()  
# audio_stream.save(mp3_file)  
# mp3_file.seek(0)  # reset pointer back to beginning of the BytesIO object  

file_path = os.path.join('static/', "audio.wav")
with open(file_path, "wb") as f:
        f.write(audio)
  
# Convert mp3 bytes to wav  
audio = AudioSegment.from_file(mp3_fp, format="mp3")  
# Change frame rate to 48000 (48kHz)  
audio = audio.set_frame_rate(48000)  

wav_data = io.BytesIO()  
audio.export(wav_data, format="wav")  
wav_data.seek(0)  # reset pointer back to beginning of the BytesIO object  
  
# Save to a temporary file  
with tempfile.NamedTemporaryFile(delete=True) as fp:  
    fp.write(wav_data.read())  
    fp.flush()  
  
    # Now you can pass `fp.name` to your code that expects a file  
