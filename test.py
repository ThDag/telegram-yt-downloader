# import yt_dlp
import subprocess

# YouTube URL
video_url = "https://www.youtube.com/watch?v=pHvP71rwYAc"

# Start and end times (in seconds)
start_time = 10
end_time = 20

yt_command = [
    "yt-dlp",
    "--download-sections",
    f"*{start_time}-{end_time}",
    "--recode-video",
    "mp4",
    "-o",
    "output.mp4",
    f"{video_url}",
]

bug_trimmer_command = ["ffmpeg", "-i", f"output.mp4", "-ss", "10", "output_fixed.mp4"]

download_output = subprocess.run(yt_command, capture_output=True, text=True)
print(download_output)

bug_trimmer_output = subprocess.run(bug_trimmer_command, capture_output=True, text=True)
print("\n\n trimmer bug \n\n")
print(bug_trimmer_output)
print("\n\n trim complete \n\n")


# yt-dlp options
# ydl_opts = {
#     "download_sections": {"*": {"start_time": start_time, "end_time": end_time}},
#     "outtmpl": "clip.%(ext)s",  # output filename
# }
