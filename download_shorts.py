# Working as expected
import yt_dlp
import os
import subprocess

def get_short_links(channel_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'playlist_end': 100,
    }
    # try to parse the channel URL by yourself -- works for the @username case
    if '/@' in channel_url:
        channel_username = channel_url.split('/@')[1].split('/')[0]
        channel_url = f'https://www.youtube.com/@{channel_username}/shorts'
    else:
        channel_url += '/shorts'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(channel_url, download=False)
        if 'entries' in result:
            video_ids = [entry['id'] for entry in result['entries']]
            short_links = [f'https://www.youtube.com/shorts/{video_id}' for video_id in video_ids]
            return short_links
        else:
            print("No videos found on the channel.")
            return []

def download_videos_from_links(links, output_path, format):
    total_links = len(links)
    
    for index, link in enumerate(links, start=1):
        link = link.strip()
        try:
            subprocess.run(['yt-dlp', '--quiet', '--format',format, '--output', os.path.join(output_path, '%(title)s.%(ext)s'), link], check=True)
            print(f"Downloading video {index}/{total_links}: {link} - Downloaded successfully")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading {link}: {e}")

if __name__ == '__main__':
    channel_url = 'https://www.youtube.com/@Techlism'  # Replace with your desired channel URL / This channel doesn't have any shorts
    output_directory = 'downloads'
    os.makedirs(output_directory, exist_ok=True)
    format = 'mp4' # the best quality is available with webm but it is not supported by all video players
    short_links = get_short_links(channel_url)
    if short_links:
        download_videos_from_links(short_links, output_directory, format)
    else:
        print("No shorts found or failed to retrieve the shorts.")
