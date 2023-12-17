import os
import random
from moviepy.editor import * 
from moviepy.video.fx.all import crop
from moviepy.audio.fx.all import volumex
from moviepy.audio.fx.all import audio_loop
from pytube import YouTube
from PIL import Image
import cv2


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
                    main_width = 1080
                    main_height = 1920
                    aspect_ratio = 2; # ändrar typ aspect ration på main videon

                    start_time = i * segment_duration
                    end_time = min((i + 1) * segment_duration, main_clip.duration)

                    title_text = TextClip("Part " + str(i+1), font='Impact',color='black',fontsize=60, bg_color='white')
                    title_text = title_text.set_position(('center', 0.85), relative=True).set_duration(10)

                    facecam_width = 250
                    facecam_height = 100
                    facecam_scale = 4

                    facecam_scaled = self.get_facecam(facecam_width, facecam_height, facecam_scale, start_time, end_time, main_clip, 0)
                    segment_main_clip = main_clip.subclip(start_time, end_time).resize(newsize=(main_width*aspect_ratio,(2*(main_height/3)))) # ändrar heighten till 2/3 av hela
                    segment_main_clip_face = CompositeVideoClip([segment_main_clip, facecam_scaled, title_text])
                    segment_main_clip_cropped = crop(segment_main_clip_face, x1=((main_width*aspect_ratio-main_width)/2), width=main_width)

                    # Segment the attention video
                    segment_attention_clip = attention_clip.subclip(start_time, end_time).resize(newsize=(main_width,(main_height/3))) # ändrar heighten till 1/3 av hela

                    # Composite the videos together
                    final_clip = clips_array([[segment_main_clip_cropped], [segment_attention_clip]])
                    output_filename = f"{self.next_file_number(output_folder)}.mp4"
                    output_path = os.path.join(output_folder, output_filename)
                    final_clip.write_videofile(output_path, codec="libx265", fps=24)

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
    
    def get_facecam(self, width, height, scale, start_time, end_time, clip, padding):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        frame = clip.get_frame(10) # Gets a frame from main vid
        fromarray = Image.fromarray(frame) # Gör framen till en "riktig bild"
        fromarray = fromarray.save("frame.png") # Sparar bilden (skitwack att man måste göra det men det funkar inte annars)

        # read and convert image
        img = cv2.imread('./frame.png')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Sparar mittpunkten för ansiktet
        for (x, y, w, h) in faces:
            midpoint_y = y+(h/2)-30
            midpoint_x = x+(w/2)
        facecam = clip.subclip(start_time, end_time).crop(x_center=midpoint_x, y_center=midpoint_y, width=width, height=height) # croppar ut ansiktet
        facecam_scaled = facecam.resize(scale) #gör den större
        facecam_scaled = facecam_scaled.set_position(('center',padding), relative=True)
        return facecam_scaled

class VideoCreator2:
    def create_tiktok(self, main_directory, music_dir, output_folder, rest_folder, title):
        main_videos = self.get_all_videos(main_directory)
        main_musics = self.get_all_musics(music_dir)

        for main_video_path in main_videos:
            main_clip = VideoFileClip(main_video_path)

            for main_music_path in main_musics:
                music_clip = VideoFileClip(main_music_path)

                segment_duration = random.randint(83, 87)  # Duration of each segment in seconds
                num_segments = int(main_clip.duration // segment_duration)
                if main_clip.duration % segment_duration != 0:
                    num_segments += 1  # Add an extra segment for the remainder

                for i in range(num_segments):
                    main_width = 1080
                    main_height = 1920
                    aspect_ratio = 2; # ändrar typ aspect ration på main videon
    
                    start_time = i * segment_duration
                    end_time = min((i + 1) * segment_duration, main_clip.duration)
    
                    title_text = TextClip(title + "\npart " + str(i+1), font='Impact',color='black',fontsize=100, bg_color='white')
                    title_text = title_text.set_position(('center', 0.7), relative=True).set_duration(10)
    
                    facecam_width = 250
                    facecam_height = 125
                    facecam_scale = 4
    
                    facecam_scaled = self.get_facecam(facecam_width, facecam_height, facecam_scale, start_time, end_time, main_clip, 0.03)
                    
                    segment_music_clip = music_clip.subclip(start_time, end_time).resize(newsize=(1,1))
                    segment_music_clip_lower = volumex(segment_music_clip, 0.08)
    
                    segment_main_clip = main_clip.subclip(start_time, end_time).resize(width=main_width*aspect_ratio)
                    final_segment = segment_main_clip.resize(height=main_height)
                    final_segment_cropped = crop(final_segment, x1=(main_width), width=main_width)
                    final_clip = CompositeVideoClip([final_segment_cropped, facecam_scaled, title_text, segment_music_clip_lower])
                    #segment_main_clip_cropped = crop(segment_main_clip_face, x1=((main_width*aspect_ratio-main_width)/2), width=main_width)
    
                
                    #main_audio = AudioFileClip(main_clip)
                    ##new_audioclip = CompositeAudioClip([music_clip_lower, main_audio])

                    output_filename = f"{self.next_file_number(output_folder)}.mp4"
                    output_path = os.path.join(output_folder, output_filename)
                    #final_clip.audio = new_audioclip
                    final_clip.write_videofile(output_path, codec="libx265", fps=24)

                    segment_duration = random.randint(83, 87)  # Duration of each segment in seconds
                    num_segments = int(main_clip.duration // segment_duration)

            # Move remaining parts of the main clip to the rest folder
            if main_clip.duration % segment_duration != 0:
                rest_clip = main_clip.subclip(num_segments * segment_duration)
                rest_output_filename = f"{self.next_file_number(rest_folder)}.mp4"
                rest_output_path = os.path.join(rest_folder, rest_output_filename)
                rest_clip.write_videofile(rest_output_path, codec="libx264", fps=24)

            main_clip.close()

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
    
    def get_all_musics(self, path):
        return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.mp4')]
    
    def get_facecam(self, width, height, scale, start_time, end_time, clip, padding):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        frame = clip.get_frame(10) # Gets a frame from main vid
        fromarray = Image.fromarray(frame) # Gör framen till en "riktig bild"
        fromarray = fromarray.save("frame.png") # Sparar bilden (skitwack att man måste göra det men det funkar inte annars)

        # read and convert image
        img = cv2.imread('./frame.png')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Sparar mittpunkten för ansiktet
        for (x, y, w, h) in faces:
            midpoint_y = y+(h/2)-30
            midpoint_x = x+(w/2)
        facecam = clip.subclip(start_time, end_time).crop(x_center=midpoint_x, y_center=midpoint_y, width=width, height=height) # croppar ut ansiktet
        facecam_scaled = facecam.resize(scale) #gör den större
        facecam_scaled = facecam_scaled.set_position(('center',padding), relative=True)
        return facecam_scaled

class VideoDownloader():
    def download_from_file(self, file_path, main_folder, ret_folder, music_folder):
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('Main: '):
                    url = line.replace('Main: ', '').strip()
                    self.download_video(url, main_folder)
                if line.startswith('Ret: '):
                    url = line.replace('Ret: ', '').strip()
                    self.download_video(url, ret_folder)
                elif line.startswith('Music: '):
                    url = line.replace('Ret: ', '').strip()
                    self.download_music(url, music_folder)

    def download_video(self, url, path):
        name = f"{self.next_file_number(path)}.mp4"
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        video.download(output_path=path, filename=name)

    def download_music(self, url, path):
        name = f"{self.next_file_number(path)}.mp4"
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().last()
        video.download(output_path=path, filename=name)


    def next_file_number(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        existing_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return len(existing_files) + 1

class TxT():
    def writer(self):
        with open('videos.txt', 'a') as file:
            link = input("paste link:")
            category, categorized_link = self.categorize(link)
            file.write(f"{category}{categorized_link}\n")

    def categorize(self, link):
        choice = input("main or ret link?")
        if choice not in ["main", "ret"]:
            print("no")
            return
        elif choice == "main":
            return "Main: ",link
        elif choice == "ret":
            return "Ret: ",link
    

def main():
    creator = VideoCreator()
    creator2 = VideoCreator2()
    downloader = VideoDownloader()
    txt = TxT()

    videos = './videos.txt'
    main_videos_path = "./downloads/main"
    retention_videos_path = "./downloads/retention"
    music_path = "./downloads/music"
    edited_path = "./edited"
    rest_folder = "./rest"
    uploaded_path = "./uploaded"

    menu_file = open('menu.txt', 'r')
    menu = menu_file.read()

    def AddtoTxt():
        txt.writer()
    
    def DownloadfromTxt():
        downloader.download_from_file(videos, main_videos_path, retention_videos_path, music_path)

    def EditfromDownloads():
        creator.create_tiktok(main_videos_path, retention_videos_path, edited_path, rest_folder)

    def EditfromDownloads2():
        userTitle = str(input("Write a title"))
        creator2.create_tiktok(main_videos_path, music_path, edited_path, rest_folder, userTitle)

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
        if choice == '2':
            DownloadfromTxt()
            loop = False
        if choice == '3':
            EditfromDownloads()
            loop = False
        elif choice == '4':
            EditfromDownloads2()
            loop = False

if __name__  == "__main__":
    main()