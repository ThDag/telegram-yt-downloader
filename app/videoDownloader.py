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

        file_name = f"./data/downloads/output{video_index}.mp4"

        yt_command = [
            "yt-dlp",
            "-S",
            "res:1080",  # download no higher than 1080
            "--download-sections",
            f"*{start_time}-{end_time}",
            "--recode-video",
            "mp4",
            "--force-keyframes-at-cuts",
            "-o",
            file_name,  # Please don't inject "rm -rf /" here, thanks :] !
            f"{i}",
        ]

        # bug_trimmer_command = ["ffmpeg", "-i", first_file, "-ss", "10", trimmed_file]
        # trim_output = subprocess.run(bug_trimmer_command)

        download_output = subprocess.run(yt_command)

        if download_output.returncode == 0:
            print("Downloaded")
            output_file_names.append(file_name)
        else:
            print("something went wrong with downloading")
            return None

        video_index += 1

    return output_file_names


def deleteVideo(name: str):
    os.remove(name)


# list = ["https://youtu.be/9PKIs32ldyo?t=18", "https://youtu.be/5B4HENeOic8?t=120"]
#
# print(downloadVideo(list, 15))
