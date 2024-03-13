"""
This demo script shows how to send audio data to Audio2Face Streaming Audio Player via gRPC requests.
There are two options:
 * Send the whole track at once using PushAudioRequest()
 * Send the audio chunks seuqntially in a stream using PushAudioStreamRequest()
For the second option this script emulates the stream of chunks, generated by splitting an input WAV audio file.
But in a real application such stream of chunks may be aquired from some other streaming source:
 * streaming audio via internet, streaming Text-To-Speech, etc
gRPC protocol details could be find in audio2face.proto
"""

import sys
import time

import audio2face_pb2
import audio2face_pb2_grpc
import grpc
import numpy as np
import soundfile


def push_audio_track(url, audio_data, samplerate, instance_name):
    """
    This function pushes the whole audio track at once via PushAudioRequest()
    PushAudioRequest parameters:
     * audio_data: bytes, containing audio data for the whole track, where each sample is encoded as 4 bytes (float32)
     * samplerate: sampling rate for the audio data
     * instance_name: prim path of the Audio2Face Streaming Audio Player on the stage, were to push the audio data
     * block_until_playback_is_finished: if True, the gRPC request will be blocked until the playback of the pushed track is finished
    The request is passed to PushAudio()
    """

    block_until_playback_is_finished = True  # ADJUST
    with grpc.insecure_channel(url) as channel:
        stub = audio2face_pb2_grpc.Audio2FaceStub(channel)
        request = audio2face_pb2.PushAudioRequest()
        request.audio_data = audio_data.astype(np.float32).tobytes()
        request.samplerate = samplerate
        request.instance_name = instance_name
        request.block_until_playback_is_finished = block_until_playback_is_finished
        print("Sending audio data...")
        response = stub.PushAudio(request)
        if response.success:
            print("SUCCESS")
        else:
            print(f"ERROR: {response.message}")
    print("Closed channel")


def push_audio_track_stream(url, audio_data, samplerate, instance_name):
    """
    This function pushes audio chunks sequentially via PushAudioStreamRequest()
    The function emulates the stream of chunks, generated by splitting input audio track.
    But in a real application such stream of chunks may be aquired from some other streaming source.
    The first message must contain start_marker field, containing only meta information (without audio data):
     * samplerate: sampling rate for the audio data
     * instance_name: prim path of the Audio2Face Streaming Audio Player on the stage, were to push the audio data
     * block_until_playback_is_finished: if True, the gRPC request will be blocked until the playback of the pushed track is finished (after the last message)
    Second and other messages must contain audio_data field:
     * audio_data: bytes, containing audio data for an audio chunk, where each sample is encoded as 4 bytes (float32)
    All messages are packed into a Python generator and passed to PushAudioStream()
    """

    chunk_size = samplerate // 10  # ADJUST
    sleep_between_chunks = 0.04  # ADJUST
    block_until_playback_is_finished = True  # ADJUST

    with grpc.insecure_channel(url) as channel:
        print("Channel creadted")
        stub = audio2face_pb2_grpc.Audio2FaceStub(channel)

        def make_generator():
            start_marker = audio2face_pb2.PushAudioRequestStart(
                samplerate=samplerate,
                instance_name=instance_name,
                block_until_playback_is_finished=block_until_playback_is_finished,
            )
            # At first, we send a message with start_marker
            yield audio2face_pb2.PushAudioStreamRequest(start_marker=start_marker)
            # Then we send messages with audio_data
            for i in range(len(audio_data) // chunk_size + 1):
                time.sleep(sleep_between_chunks)
                chunk = audio_data[i * chunk_size : i * chunk_size + chunk_size]
                yield audio2face_pb2.PushAudioStreamRequest(audio_data=chunk.astype(np.float32).tobytes())

        request_generator = make_generator()
        print("Sending audio data...")
        response = stub.PushAudioStream(request_generator)
        if response.success:
            print("SUCCESS")
        else:
            print(f"ERROR: {response.message}")
    print("Channel closed")


def main(audio_file, prim_path):
    """
    This demo script shows how to send audio data to Audio2Face Streaming Audio Player via gRPC requests.
    There two options:
     * Send the whole track at once using PushAudioRequest()
     * Send the audio chunks seuqntially in a stream using PushAudioStreamRequest()
    For the second option this script emulates the stream of chunks, generated by splitting an input WAV audio file.
    But in a real application such stream of chunks may be aquired from some other streaming source:
     * streaming audio via internet, streaming Text-To-Speech, etc
    gRPC protocol details could be find in audio2face.proto
    """

    # if len(sys.argv) < 3:
    #     print("Format: python test_client.py PATH_TO_WAV INSTANCE_NAME")
    #     return

    # Sleep time emulates long latency of the request
    sleep_time = 2.0  # ADJUST

    # URL of the Audio2Face Streaming Audio Player server (where A2F App is running)
    url = "localhost:50051"  # ADJUST

    # Local input WAV file path
    audio_fpath = audio_file

    # Prim path of the Audio2Face Streaming Audio Player on the stage (were to push the audio data)
    instance_name = prim_path

    data, samplerate = soundfile.read(audio_fpath, dtype="float32")

    # Only Mono audio is supported
    if len(data.shape) > 1:
        data = np.average(data, axis=1)

    print(f"Sleeping for {sleep_time} seconds")
    time.sleep(sleep_time)

    if 0:  # ADJUST
        # Push the whole audio track at once
        push_audio_track(url, data, samplerate, instance_name)
    else:
        # Emulate audio stream and push audio chunks sequentially
        push_audio_track_stream(url, data, samplerate, instance_name)


# if __name__ == "__main__":
#     main(audio_file, instance_name)
