from __future__ import unicode_literals
from tkinter import *
import tkinter
import urllib.parse
import urllib.request 
import re
import threading
import os
import subprocess




series_list=[];

desktop_path = os.path.expanduser('~') + '\\Desktop\\'




'''
The following class creates the GUI for interacting in the command line with youtube dl. The inputs include a file name
for the series list, followed by the title of the desired mixtape. As the downloads happen, messages will pop out to the user
to show them there downloads are in progress.
'''


class GUI:
    def __init__(self, master):
        self.master= master
        master.title("TISH video downloader")
        master.geometry("750x500")

        self.label = Label(master, text="Enter file name for the songs list: ")
        self.label.pack()

        self.entry = Entry(master, width=45)
        self.entry.pack()

     
        self.button = Button(master, text="Download video", command=self.download_button_click)
        self.button.pack()

        self.button = Button(master, text="Download audio", command=self.downloader_button_click)
        self.button.pack()

        self.label_help = Label(master, text="\nHOW TO USE:\n1. Create a text file on your desktop listing each series and episode you want line by line."
                                             "\n2. Enter the text file name inside the top most box.\n"
                                             "3. Click download and the series will be created on your desktop."
                                             "\n-----------------------------------------------------------------------------------\n")
        self.label_help.pack()

        self.text = Text(master)
        self.text.pack()
    '''
    On button click, read the inputted file line by line and retrieve all series. Then start
    a seperate thread.
    '''
    def download_button_click(self):
        global series_list
        # read file user has entered in entry box one
        series_list = self.read_file(self.entry.get())

        # tkinter is single threaded, thus start a seperate thread for the download process
        DownloadVideosThread(self.text).start()


    def downloader_button_click(self):
        global series_list
        # read file user has entered in entry box one
        series_list = self.read_file(self.entry.get())

        # tkinter is single threaded, thus start a seperate thread for the download process
        DownloadVideosThreader(self.text).start()

    '''
    Processes the users inputted title for the series and creates a folder on the desktop.
    Reads each line of the file and stores the series in a list.
    '''
    def read_file(self, file_name):
        global desktop_path
        # path to read text file
        file = desktop_path + file_name

        self.update_text_widget("Reading file " + self.entry.get())

        # read contents of file
        with open(file, "r") as f:
            series = f.read().splitlines()

        # set new path to include the title of the shows as the subdirectory
        desktop_path += "VIDEOS" + "\\"

        self.update_text_widget("\nFound " + str(len(series)) + " shows!")

        return series

    '''
    Update text to the tkinter widget to inform user what is happening.
    '''
    def update_text_widget(self, message):
        # Update text to text widget
        self.text.insert(END, message)
        # Move to the end of the text box if text has gone outside the initial length
        self.text.see(END)

'''
The following class runs on a seperate thread for searching youtuberesults and downloading
the songs.

'''




class DownloadVideosThread(threading.Thread):
    def __init__(self, text):
        threading.Thread.__init__(self)
        self.text = text

    def run(self):
        video_urls = self.find_video_urls(series_list)
        self.download_videos(video_urls, series_list)   

    def update_text_widget(self, message):
        self.text.insert(END, message)
        self.text.see(END)

    def download_videos(self, urls, songs):
        self.update_text_widget("\n\nStarting downloads ...")
        index = 0
        for url in urls:
            self.update_text_widget("\nSong - " + songs[index]
                                    + " - Extracting video at " + url + " ...")
            # set flags to ensure the console does not pop up
            no_console = subprocess.STARTUPINFO()
            no_console.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            # command line to do downloads


   
           
            subprocess.call(['youtube-dl', '-o', desktop_path + songs[index] + ".%(ext)s",
                 url], startupinfo=no_console, shell=True)

            self.update_text_widget("\nvideo - " + songs[index] + " - Download complete!")
            index += 1

            self.update_text_widget("\n\nAll downloads complete! Check your desktop for your mixtape!")


    '''
    Query youtube results based on the songs entered in the text file
    '''
    def find_video_urls(self, series):
        videos = list()
        for show in series:
            self.update_text_widget("\nSong - " + show + " - Querying youtube results ...")

            query_string = urllib.parse.urlencode({'search_query': show})


          #  idea = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
           # html_content=idea.read().decode()
            #self.update_text_widget(html_content)
            
            search_song_url = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + query_string)
            video_ids = re.findall(r"watch\?v=(\S{11})", search_song_url.read().decode())
            url="https://www.youtube.com/watch?v=" + video_ids[0]
            str(url)
            print(url)

            videos.append("https://www.youtube.com/watch?v=" + video_ids[0])
            self.update_text_widget("\nSong - " + show + " - Found top result!")

        return videos


class DownloadVideosThreader(threading.Thread):
    def __init__(self, text):
        threading.Thread.__init__(self)
        self.text = text

    def run(self):
        audio_urls = self.find_audio_urls(series_list)
        self.download_audio(audio_urls, series_list)   

    def update_text_widget(self, message):
        self.text.insert(END, message)
        self.text.see(END)

    def find_audio_urls(self, series):
        videos = list()
        for show in series:
            self.update_text_widget("\nSong - " + show + " - Querying youtube results ...")

            query_string = urllib.parse.urlencode({'search_query': show})


          #  idea = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
           # html_content=idea.read().decode()
            #self.update_text_widget(html_content)
            
            search_song_url = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + query_string)
            video_ids = re.findall(r"watch\?v=(\S{11})", search_song_url.read().decode())
            url="https://www.youtube.com/watch?v=" + video_ids[0]
            str(url)
            print(url)

            videos.append("https://www.youtube.com/watch?v=" + video_ids[0])
            self.update_text_widget("\nSong - " + show + " - Found top result!")

        return videos

             
            

           # html_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
             #self.update_text_widget(html_content)


            # retrieve all videos that met the song name criteria
            #search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content)
            
            


            # only take the top result
       
           # inp = "https://www.youtube.com/watch?v=" + search_results[1].read()
            #self.update_text_widget(inp)

    '''
    Call command line for youtube dl. Sets the output directory for downloaded files.
    '''
    

    def download_audio(self, urls, songs):
        self.update_text_widget("\n\nStarting downloads ...")
        index = 0
        for url in urls:
            self.update_text_widget("\nSong - " + songs[index]
                                    + " - Extracting audio at " + url + " ...")
            # set flags to ensure the console does not pop up
            no_console = subprocess.STARTUPINFO()
            no_console.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            # command line to do downloads


   
           
            subprocess.call(['youtube-dl', '-o', desktop_path + songs[index] + ".%(ext)s",
                 "--extract-audio", "--audio-format", "mp3", url], startupinfo=no_console,shell=True)

            self.update_text_widget("\nvideo - " + songs[index] + " - Download complete!")
            index += 1

            self.update_text_widget("\n\nAll downloads complete! Check your desktop for your mixtape!")
root = Tk()
root.resizable(width=False, height=False)
gui = GUI(root)
root.mainloop()