import os
import subprocess
from urllib.parse import parse_qs, urlparse


def downloadVideo(links: list[str], length: int):

    output_file_names = []
    video_index = 0

    for i in links:
        parsed = urlparse(i)
        queries = parse_qs(parsed.query)
        start_time = int(queries.get("t", [0])[0])

        end_time = start_time + length

        first_file = f"downloads/output{video_index}_untrimmed.mp4"
        trimmed_file = f"downloads/output{video_index}.mp4"

        yt_command = [
            "yt-dlp",
            "-S",
            "res:1080",  # download no higher than 1080
            "--download-sections",
            f"*{start_time}-{end_time}",
            "--recode-video",
            "mp4",
            "-o",
            first_file,
            f"{i}",
        ]

        bug_trimmer_command = ["ffmpeg", "-i", first_file, "-ss", "10", trimmed_file]

        subprocess.run(yt_command)

        trim_output = subprocess.run(bug_trimmer_command)

        if trim_output.returncode == 0:
            os.remove(first_file)
            print("Downloaded, trimmed, and untrimmed file removed")
            output_file_names.append(trimmed_file)
        else:
            print("something went wrong with trimming")
            return None

        video_index += 1

    return output_file_names


list = ["https://youtu.be/9PKIs32ldyo?t=18", "https://youtu.be/5B4HENeOic8?t=120"]

print(downloadVideo(list, 15))
