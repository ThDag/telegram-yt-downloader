import os
import subprocess
from urllib.parse import parse_qs, urlparse


def downloadVideo(links: list[str], length: int):

    output_file_names = []

    def file_namer():
        # reads the list of files in download directory and gives you the name of the next file.
        current_files = os.listdir("./data/downloads")

        numbers = []
        for i in current_files:
            current_file_number = ""
            for a in i:
                if a.isdigit():
                    current_file_number += a
            if current_file_number:
                numbers.append(current_file_number)

        int_number = list(map(int, numbers))
        new_number = int(max(int_number) + 1)

        file_name = f"./data/downloads/output{new_number}.mp4"
        return file_name

    for i in links:
        parsed = urlparse(i)
        queries = parse_qs(parsed.query)
        start_time = int(queries.get("t", [0])[0])

        end_time = start_time + length

        file_name = file_namer()

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

        download_output = subprocess.run(yt_command, capture_output=True, text=True)

        if download_output.returncode == 0:
            print("Downloaded")
            output_file_names.append(file_name)
        else:
            print("something went wrong with downloading")
            return str(download_output.stderr)

    return output_file_names


def deleteVideo(name: str):
    os.remove(name)


# list = ["https://youtu.be/9PKIs32ldyo?t=18", "https://youtu.be/5B4HENeOic8?t=120"]
#
# print(downloadVideo(list, 15))
