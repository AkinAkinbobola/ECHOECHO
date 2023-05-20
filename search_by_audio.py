from acrcloud.recognizer import ACRCloudRecognizer
import sounddevice as sd
from scipy.io.wavfile import write
import threading
import json

AUDIO_FILE = "music/audio.wav"
DURATION = 5
SAMPLING_FREQ = 44100
SPOTIFY_URL = "https://open.spotify.com/"


def record_audio():
    print("Recording...\n")
    recording = sd.rec(int(DURATION * SAMPLING_FREQ), samplerate=SAMPLING_FREQ, channels=2)
    sd.wait()
    write(AUDIO_FILE, SAMPLING_FREQ, recording)
    threading.Thread(target=send_to_acr_cloud, args=(AUDIO_FILE,)).start()


def send_to_acr_cloud(audio):
    config = {
        "host": "identify-us-west-2.acrcloud.com",
        "access_key": "dccaf0c06d15eb512eab05a5f9f5420a",
        "access_secret": "cEXwp8kHkjROtLkKWAmDYmJMJgARP9FCylZMOFy4",
        "timeout": 10
    }
    re = ACRCloudRecognizer(config)
    results = re.recognize_by_file(audio, 0)
    return results


def display_results(data):
    response = json.loads(data)
    print(response)

    if "status" in response and response["status"].get("msg") == "Success":
        print("Music found successfully:\n")

        metadata = response.get("metadata", {})
        if "music" in metadata:
            music = metadata["music"][0]

            if "external_metadata" in music and "spotify" in music["external_metadata"]:
                spotify = music["external_metadata"]["spotify"]

                if "genres" in music and music["genres"]:
                    genre = music["genres"][0]["name"]
                else:
                    genre = "Unknown"
                label = music.get("label")
                release_date = music.get("release_date", "")[:4]

                # Print Spotify details
                spotify_track = spotify["track"]
                spotify_album = spotify["album"]
                spotify_artists = spotify["artists"]

                print(f"Track ID: {SPOTIFY_URL + 'track/' + spotify_track['id']}")
                print(f"Track Name: {spotify_track['name']}")
                print(f"Album Name: {spotify_album['name']}")
                print(f"Album ID: {SPOTIFY_URL + 'album/' + spotify_album['id']}")

                if len(spotify_artists) == 1:
                    print("Artist:")
                else:
                    print("Artists:")
                for artist in spotify_artists:
                    print(f" - ID: {SPOTIFY_URL + 'artist/' + artist['id']}, Name: {artist['name']}")

                print(f"Genre: {genre}")
                print(f"Record Label: {label}")
                print(f"Released: {release_date}")
            else:

                album_name = music["album"]["name"]
                artists = music["artists"]
                song_name = music["title"]
                if "genres" in music and music["genres"]:
                    genre = music["genres"][0]["name"]
                else:
                    genre = "Unknown"
                label = music.get("label")
                release_date = music.get("release_date", "")[:4]

                # Print default details
                print(f"Song Name: {song_name}")
                print(f"Album: {album_name}")
                if artists:
                    if len(artists) == 1:
                        print(f"Artist: {artists[0]['name']}")
                    else:
                        print("Artists:")
                        for artist in artists:
                            print(f" - {artist['name']}")
                else:
                    print("Artist: Unknown")
                print(f"Genre: {genre}")
                print(f"Record Label: {label}")
                print(f"Released: {release_date}")
                print("\nFinished!")
        else:
            print("No music information found.")
    else:
        print("Song not found.")


def main():
    record_audio()
    display_results(send_to_acr_cloud(AUDIO_FILE))


if __name__ == "__main__":
    main()
