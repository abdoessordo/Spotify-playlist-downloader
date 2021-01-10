from tkinter import *
from download import downlaod
import json
from get_URLS import add_urls

# -------------------------------------------------------------
#                       FUNCTIONS
# -------------------------------------------------------------

def font_test():
    fonts = ['Arial','Helvetica', 'Courier New', 'Courier', 'Comic Sans MS', 'Fixedsys', 'MS Sans Serif', 'MS Serif',
    'Symbol', 'System', 'Times New Roman', 'Times', 'Verdana']

    for child in holder_frame.winfo_children():
        child.destroy()
    for font in fonts:
        label = Label(holder_frame,text=font, font=(font, 13))
        label.pack()


def download_btn(foldername):
    with open('./songs.json', 'r') as f:
        SONGS = json.load(f)

    status_label['fg'] = 'red'
    status_label['text'] = 'Downloading ...'
    status_label.update()
    if foldername == '':
        foldername = "OUTPUT/"
    folder_name_entry.delete(0, 'end')
    folder_name_entry.update()
    count = 1
    number_of_songs = len(SONGS)
    print(number_of_songs)
    for song in SONGS:
        root.update()
        status_label['text'] = f'Downloading {count}/{number_of_songs}'
        status_label.update()
        downlaod(song, foldername)
        count += 1

    status_label['text'] = f'All Done'
    status_label['fg'] = 'green'


# -------------------------------------------------------------
#                   INITIALIZATION
# -------------------------------------------------------------


WIDTH = 700
HEIGHT = 600

root = Tk()
root.title("Spotify Playlist Downloader")
canvas = Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()


# -------------------------------------------------------------
#                       FRAMES
# -------------------------------------------------------------

bg_frame = Frame(root, bg='red')
bg_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

holder_frame = Frame(root)
holder_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

prompt_frame = Frame(holder_frame)
prompt_frame.place(relwidth=1, relx=0, relheight=0.3, rely=0)

labels_frame = Frame(prompt_frame)
labels_frame.place(relwidth=0.6, relx=0, relheight=1, rely=0)

entries_frame = Frame(prompt_frame)
entries_frame.place(relwidth=0.4, relx=0.6, relheight=1, rely=0)

# -------------------------------------------------------------
#                           GUI
# -------------------------------------------------------------

# ==================== Labels ==================================
folder_name_label = Label(labels_frame, text='Enter a name for the output folder :',
                          fg='Black', font=('Helvetica', 15))
folder_name_label.place(relx=0.1, rely=0.4)

default_folder_name = Label(labels_frame, text='(Nb: The default folder name is set to: Output)',
                            font=('Helvetica', 11), fg='red')
default_folder_name.place(relx=0.1, rely=0.55)

status_label = Label(holder_frame, font=('Helvetica', 15))
status_label.place(relx=0.42, rely=0.85)

# ==================== Entries ==================================
folder_name_entry = Entry(entries_frame, font=('Helvetica', 13))
folder_name_entry.place(relx=0, relwidth=0.5, rely=0.43, relheight=0.15)

# ==================== Buttons ==================================
download_BTN = Button(holder_frame, text='Download', font=('Helvetica', 13),
                      command=lambda: download_btn(folder_name_entry.get()))
download_BTN.place(relx=0.35, relwidth=0.3, rely=0.5)

# -------------------------------------------------------------
#                        MAIN LOOP
# -------------------------------------------------------------
if __name__ == '__main__':
    # font_test()
    root.mainloop()
