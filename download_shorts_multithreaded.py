#let's try multithreading
import yt_dlp
import os
import subprocess
import concurrent.futures

def get_short_links(channel_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'playlist_end': 100,
    }
    
    # try to parse the channel URL by yourself -- works for the @username, /channel and /c cases
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

def download_video(link, output_path, format):
    link = link.strip()
    try:
        if format == 'webm':
            subprocess.run(['yt-dlp', '--quiet', '--format', 'bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]', '--output', os.path.join(output_path, '%(title)s.%(ext)s'), link], check=True)
        else:
            subprocess.run(['yt-dlp', '--quiet', '--format', format , '--output', os.path.join(output_path, '%(title)s.%(ext)s'), link], check=True)
        
        print(f"Downloaded: {link}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {link}: {e}")

def download_videos_from_links(links, output_path, format):
    # max_workers can be adjusted based on your system's capabilities
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(download_video, link, output_path, format) for link in links]
        concurrent.futures.wait(futures)

if __name__ == '__main__':
    channel_url = 'https://www.youtube.com/@Techlism'  # Replace with your desired channel URL / This channel (mine) doesn't have any shorts
    output_directory = 'downloads'
    os.makedirs(output_directory, exist_ok=True)

    short_links = get_short_links(channel_url)
    format = 'webm' # best quality is available with webm but it is not supported by all video players
    
    if short_links:
        download_videos_from_links(short_links, output_directory, format)
    else:
        print("No shorts found or failed to retrieve the shorts.")
