from pytube import *
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from threading import *

#total size container
file_size=0

# this gets called for updating percentage
def progress(stream=None, chunk=None, file_handle=None, remaining=None):
	# gets the percentage of the file that has been downloaded...
	file_downloaded=(file_size-remaining)
	per = (file_downloaded/file_size)*100
	dBtn.config(text="{:00.0f} % downloaded".format(per))


def startDownload():
	global file_size
	try:
		url = urlField.get()
		print(url)
		#changing buttonm text
		dBtn.config(text='Please wait...')
		dBtn.config(state=DISABLED)
		path_to_save_video = askdirectory()
		print(path_to_save_video)
		if path_to_save_video is None:
			return
		# creating youtube object with url
		ob = YouTube(url, on_progress_callback=progress)
		# strms = ob.streams.all()
		# for s in strms:
		#	print(s)
		strm = ob.streams.filter(progressive=True, res="720p").first()
		file_size = strm.filesize
		vTitle.config(text=strm.title)
		vTitle.pack(side=TOP)
		print(file_size)
		# print(strm)
		# print(strm.filesize)
		# print(strm.title)
		# print(ob.description)
		# now downloading the video
		strm.download(path_to_save_video)
		print("Done...")
		dBtn.config(text="Start Download")
		dBtn.config(state=NORMAL)
		showinfo("Download Finished", "Downloaded Successfully")
		urlField.delete(0,END)
		vTitle.pack_forget()

	except Exception as e:
		print(e)
		print("Error!")

def startDownloadThread():
	# create thread...
	thread = Thread(target=startDownload)
	thread.start()

# start gui building
main = Tk()

# setting the title
main.title("My YouTube Downloader")

# set the icon
# main.iconbitmap("icon1.ico")

# set the width and height
main.geometry("500x600")

# heading icon
file = PhotoImage(file='youtube.png')
headingIcon = Label(main, image=file)
headingIcon.pack(side=TOP)

# url textfield
urlField = Entry(main, font=("verdana", 18), justify=CENTER)
urlField.pack(side=TOP, fill=X, padx=10)

# download button
dBtn = Button(main, text='Start Download', font=("Arial", 15), relief='ridge', command=startDownloadThread)
dBtn.pack(side=TOP, pady=10)

# video title
vTitle = Label(main, text="Video Title")
# vTitle.pack(side=TOP)

main.mainloop()