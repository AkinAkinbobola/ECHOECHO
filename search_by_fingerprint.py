from acrcloud import acrcloud_extr_tool

audio_file = "music/audio.wav"
start_time_seconds = 0
audio_len_seconds = 10
is_db_fingerprint = False

fingerprint = acrcloud_extr_tool.create_fingerprint_by_file(audio_file, start_time_seconds, audio_len_seconds,
                                                            is_db_fingerprint, 0)
print(fingerprint)

