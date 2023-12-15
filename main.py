import os
import random
from moviepy.editor import * 
from moviepy.video.fx.all import crop
from pytube import YouTube

class VideoCreator:
    def create_tiktok(self, main_directory, attention_directory, output_folder, rest_folder):
        main_videos = self.get_all_videos(main_directory)
        attention_videos = self.get_all_videos(attention_directory)

        for main_video_path in main_videos:
            main_clip = VideoFileClip(main_video_path)
            for attention_video_path in attention_videos:
                attention_clip = VideoFileClip(attention_video_path)

                segment_duration = random.randint(83, 87)  # Duration of each segment in seconds
                num_segments = int(main_clip.duration // segment_duration)
                if main_clip.duration % segment_duration != 0:
                    num_segments += 1  # Add an extra segment for the remainder

                for i in range(num_segments):
                    start_time = i * segment_duration
                    end_time = min((i + 1) * segment_duration, main_clip.duration)
                    segment_main_clip = main_clip.subclip(start_time, end_time)

                    # Segment the attention video
                    segment_attention_clip = attention_clip.subclip(0, min(segment_duration, attention_clip.duration)).resize(height=segment_main_clip.h / 3)

                    # Position the attention clip
                    x_position = segment_main_clip.w - segment_attention_clip.w
                    y_position = segment_main_clip.h - segment_attention_clip.h
                    positioned_attention_clip = segment_attention_clip.set_position((x_position, y_position))

                    # Composite the videos together
                    final_clip = CompositeVideoClip([segment_main_clip, positioned_attention_clip], size=(1080, 1920))
                    output_filename = f"{self.next_file_number(output_folder)}.mp4"
                    output_path = os.path.join(output_folder, output_filename)
                    final_clip.write_videofile(output_path, codec="libx264", fps=24)

            # Move remaining parts of the main clip to the rest folder
            if main_clip.duration % segment_duration != 0:
                rest_clip = main_clip.subclip(num_segments * segment_duration)
                rest_output_filename = f"{self.next_file_number(rest_folder)}.mp4"
                rest_output_path = os.path.join(rest_folder, rest_output_filename)
                rest_clip.write_videofile(rest_output_path, codec="libx264", fps=24)

            main_clip.close()
            attention_clip.close()

    def next_file_number(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        existing_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return len(existing_files) + 1

    def select_video(self, path):
        videos = [f for f in os.listdir(path) if f.endswith('.mp4')]
        return os.path.join(path, videos[0]) if videos else None
    
    def get_all_videos(self, path):
        return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.mp4')]

class VideoDownloader():
    def download_video(self, url, path):
        name = f"{self.next_file_number(path)}.mp4"
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        video.download(output_path=path, filename=name)

    def next_file_number(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        existing_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return len(existing_files) + 1
    
class VideoUploader():
    def uploaded():
        NotImplementedError()

class TxTWriter():
    def write():

        


        file = open('videos.txt' 'r+')



        file.close()
    def read():
        NotImplemented

        
def main():
    creator = VideoCreator()
    downloader = VideoDownloader()
    uploader = VideoUploader()
    txt = TxTWriter()

    main_video_url = "https://www.youtube.com/watch?v=6RbvvsrMlFw"
    retentioner_video_url = "https://www.youtube.com/watch?v=TW-LgJUiMX0"
    main_videos_path = "./downloads/main"
    retention_videos_path = "./downloads/retention"
    edited_path = "./edited"
    rest_folder = "./rest"
    uploaded_path = "./uploaded"

    menu_file = open('menu.txt', 'r')
    menu = menu_file.read()

    def AddtoTxt():
        NotImplemented
    
    def DownloadfromTxt():
        downloader.download_video(main_video_url, main_videos_path)
        downloader.download_video(retentioner_video_url, retention_videos_path)

    def EditfromDownloads():
        creator.create_tiktok(main_videos_path, retention_videos_path, edited_path, rest_folder)

    def UploadfromEdited():
        NotImplemented

    loop = True
    while loop:
        print(menu)
        choice = input("what do?")
        if choice not in ['1','2','3','4']:
            print("no")
            return
        if choice == '1':
            AddtoTxt()
            loop = False
        elif choice == '2':
            DownloadfromTxt()
            loop = False
        elif choice == '3':
            EditfromDownloads()
            loop = False
        elif choice == '4':
            UploadfromEdited()
            loop = False

if __name__  == "__main__":
    main()