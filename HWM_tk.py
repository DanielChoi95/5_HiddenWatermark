from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
import tkinter.messagebox as msgbox
import os, cv2, random
import numpy as np
from PIL import Image, ImageTk

'''
referance 
https://www.geeksforgeeks.org/image-based-steganography-using-python/?ref=rp
'''

root = Tk()
root.title("Hidden Watermark")
root.resizable()

# Add files
def add_file():
    files = filedialog.askopenfilenames(title="Select Images", filetypes=(("Image files", "*.png *.jpg *.bmp"), ("All", "*.*"))) 
    # print on listbox
    for file in files:
        list_file.insert(END, file)

# Delete Files
def del_file():
    for index in reversed(list_file.curselection()): 
        list_file.delete(index)

# Preview
def preview_radio():
    # reveal
    if rad_var.get() == 1:
        pass
    
    # hide
    elif rad_var.get() == 2:
        pass








# Save path
def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected == '':
        return
    entry_dest_path.delete(0,END)
    entry_dest_path.insert(0, folder_selected)

# Before encoding and decoding operation
def preparation():
    # check if file list is empty
    if list_file.size() == 0:
        msgbox.showwarning("Warning", "Add Image Files")
        return

    # check if save path is unassigned
    if len(entry_dest_path.get()) == 0:
        msgbox.showwarning("Warning", "Select Save Path")
        return

    # check if a file with the same name exists
    # msgbox.askokcancel('OK / Cancel', 'There is a file with the same name, Would you overwrite it?')

# watermark encode
def encode():
    preparation()  
    try:
        img_format = combo_format.get().lower()
        wm_text = entry_watermark.get()
        images = list_file.get(0, END)
        for i in range(list_file.size()):
            img_origin = cv2.imread(images[i])
            h_origin, w_origin, _ = img_origin.shape
            
            # create watermark image
            watermark = np.zeros((h_origin, w_origin, 3), np.uint8)
            for h in range(1, int(h_origin/10)+1):
                for w in range(int(w_origin/10)):
                    height, width = h*10, w*10*len(wm_text)
                    cv2.putText(watermark, wm_text, (width, height), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (30,30,30), 1)

            # encoding
            for h_wm in range(h_origin):
                for w_wm in range(w_origin):
                    for l_wm in range(3):                      
                        # v1 and v2 are 8-bit pixel values of img_origin and watermark respectively
                        v1 = format(img_origin[h_wm][w_wm][l_wm], '08b')
                        v2 = format(watermark[h_wm][w_wm][l_wm], '08b')
                        # Taking 4 MSBs of each image
                        v3 = v1[:4] + v2[:4]                 
                        img_origin[h_wm][w_wm][l_wm]= int(v3, 2)
            
            # save file
            file_name = 'WM_encoded_{}.'.format(i+1) + img_format
            dest_path = os.path.join(entry_dest_path.get(), file_name)
            
            cv2.imwrite(dest_path, img_origin)

            # Progress bar
            progress = (i + 1) / list_file.size() * 100
            p_var.set(progress)
            progress_bar.update()

        msgbox.showinfo("Notice", "Watermark has been successfully encoded")
        
    except Exception as err:
        msgbox.showerror("Error occurred", err)
    
# watermark decode
def decode():
    preparation()
    try:
        img_format = combo_format.get().lower()
        images = list_file.get(0, END)
        for i in range(list_file.size()):
            img_wm = cv2.imread(images[i])
            h_wm, w_wm, _ = img_wm.shape

            # img1 and img2 are two blank images
            img1 = np.zeros((h_wm, w_wm, 3), np.uint8)
            img2 = np.zeros((h_wm, w_wm, 3), np.uint8)
        
            for i in range(h_wm):
                for j in range(w_wm):
                    for l in range(3):
                        v1 = format(img_wm[i][j][l], '08b')
                        v2 = v1[:4] + chr(random.randint(0, 1)+48) * 4
                        v3 = v1[4:] + chr(random.randint(0, 1)+48) * 4
                  
                        # Appending data to img1 and img2
                        img1[i][j][l]= int(v2, 2)
                        img2[i][j][l]= int(v3, 2)

            # save file
            file_name1 = 'WM_decoded_image{}.'.format(i+1) + img_format
            file_name2 = 'WM_decoded_watermark{}.'.format(i+1) + img_format
            dest_path1 = os.path.join(entry_dest_path.get(), file_name1)
            dest_path2 = os.path.join(entry_dest_path.get(), file_name2)
            # 동일한 파일 이름 체크
            cv2.imwrite(dest_path1, img1)
            cv2.imwrite(dest_path2, img2)

            # Progress bar
            progress = (i + 1) / list_file.size() * 100
            p_var.set(progress)
            progress_bar.update()

        msgbox.showinfo("Notice", "Watermark has been successfully decoded")
        
    except Exception as err:
        msgbox.showerror("Error occurred", err)


    




'''
Layouts <>><><><><><><><><><>
'''

# Add and delete files
frame_file = Frame(root)
frame_file.pack(fill="x", padx=5, pady=5)

btn_add_file = Button(frame_file, text="Add Files", padx=5, pady=5, width=12, command=add_file)
btn_add_file.pack(side="left", padx = 5)

btn_del_file = Button(frame_file, text="Delete Files", padx=5, pady=5, width=12, command=del_file)
btn_del_file.pack(side="left", padx = 5)

# Listbox
frame_list = Frame(root)
frame_list.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(frame_list)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(frame_list, selectmode="extended", height=5, yscrollcommand=scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

# Preview
frame_preview = LabelFrame(root, text = 'Preview')
frame_preview.pack(fill = 'x', padx = 5, pady = 5)

rad_var = IntVar()

radio_reveal = Radiobutton(frame_preview, text = 'Reveal', variable = rad_var, value = 1, command = preview_radio, width = 6)
radio_reveal.pack(side = 'left', padx = 5)

radio_hide = Radiobutton(frame_preview, text = 'Hide', variable = rad_var, value = 2, command = preview_radio, width = 6)
radio_hide.pack(side = 'left', padx = 5)

preview = Canvas(root)
preview.pack(fill = 'both', padx = 5, pady = 5)







# Save Path
frame_path = LabelFrame(root, text="Save Path")
frame_path.pack(fill="x", padx=5, pady=5, ipady=5)

entry_dest_path = Entry(frame_path)
entry_dest_path.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4)

btn_dest_path = Button(frame_path, text="Browse", width=10, command=browse_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)

# Options [Watermark, Format]
frame_options = LabelFrame(root, text="Options")
frame_options.pack(padx=5, pady=5, ipady=5)

# Watermark
label_watermark = Label(frame_options, text = 'Watermark Text')
label_watermark.pack(side = 'left', padx = 5, pady = 5)

entry_watermark = Entry(frame_options)
entry_watermark.pack(side = 'left', padx = 5, pady = 5)

# Format
label_format = Label(frame_options, text="Format")
label_format.pack(side="left", padx=5, pady=5)

opt_format = ["png", "jpg", "bmp"]
combo_format = ttk.Combobox(frame_options, state="readonly", values=opt_format, width=10)
combo_format.current(0)
combo_format.pack(side="left", padx=5, pady=5)

# Progress Bar
frame_progress = LabelFrame(root, text="Progression")
frame_progress.pack(fill="x", padx=5, pady=5, ipady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill="x", padx=5, pady=5)

# Encode / Decode / Close
frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5)

btn_encode = Button(frame_run, padx=5, pady=5, text="Encode", width=12, command=encode)
btn_encode.pack(side="left", padx=5, pady=5)

btn_decode = Button(frame_run, padx=5, pady=5, text="Decode", width=12, command=decode)
btn_decode.pack(side="left", padx=5, pady=5)

btn_close = Button(frame_run, padx=5, pady=5, text="Close", width=12, command=root.quit)
btn_close.pack(side="left", padx=5, pady=5)

root.mainloop()