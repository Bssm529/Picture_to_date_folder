import os
import PIL.Image
from datetime import datetime
import shutil
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import ffmpeg
import sys
import dateutil.parser

#folder = "C:\\Users\\ckob\\Documents\\privat\\Fotos\\pictures"

class GUI():
    def __init__(self, master):
        GUI.v_folder = StringVar()
        GUI.v_path = StringVar()
        GUI.pb_lenght = 366
        
        self.master = master
        self.master.title('Foto_Datum-Ordner_Ersteller')
        
        self.left_frame = ttk.Frame(self.master, borderwidth = 5)
        self.left_frame.pack(side = LEFT)
        self.right_frame = ttk.Frame(self.master, borderwidth = 5)
        self.right_frame.pack(side = RIGHT)
       
        self.entry_folder = ttk.Entry(self.left_frame, width = 60)
        self.entry_folder.pack(side = TOP)
        self.button_folder = ttk.Button(self.right_frame, text = 'Select Folder', command = self.func_select_folder)
        self.button_folder.pack(side = TOP)
        
        self.button_start = ttk.Button(self.right_frame, text = "Start", command = self.make_dir_per_date)
        self.button_start.pack()
        
        self.pb = ttk.Progressbar(
        self.left_frame,
        orient='horizontal',
        mode='determinate',
        length=GUI.pb_lenght
        )
        self.pb.pack(side = TOP, expand = True)
        
        self.text = ttk.Label(self.left_frame, textvariable = GUI.v_path)
        self.text.pack(side = TOP, expand = False)
        
    
    def func_select_folder(self):
        self.entry_folder.delete(0, END)
        GUI.v_folder = filedialog.askdirectory()
        self.entry_folder.insert(0, GUI.v_folder)
    
    def files_paths_to_list(self, folder):
        t_files = []
        for root, dirs, files in os.walk(folder):
            for name in files:
                t_files.append(os.path.join(root, name))
        return t_files

    def make_dir_per_date(self):

        folder = GUI.v_folder
        
        t_files = self.files_paths_to_list(folder)
        pb_stepsize = 100/len(t_files)
        
        for file_path in t_files:
            try:
                file_date = PIL.Image.open(file_path)._getexif()[36867]
                file_date = datetime.strptime(file_date, '%Y:%m:%d %H:%M:%S')
                new_path = folder +"\\"+ file_date.strftime('%Y-%m')
            except:
                try:
                    file_date = ffmpeg.probe(file_path)['format']['tags']['creation_time']
                    file_date = dateutil.parser.parse(file_date)
                    new_path = folder +"\\"+ file_date.strftime('%Y-%m')
                except:
                    file_date = os.path.getmtime(file_path)
                    date_c = os.path.getctime(file_path)
                    
                    if file_date  > date_c:
                        file_date = date_c
                    try:
                        file_date = datetime.fromtimestamp(file_date)
                    except:
                        pass
                   
                    new_path = folder +"\\"+ file_date.strftime('%Y-%m')
                    
            file_name = file_path.rsplit('\\')[-1]
            check_path = new_path +"\\" + file_name
            
            path_shown = "\\" + file_date.strftime('%Y-%m') + "\\" + file_name
            print(path_shown)
            GUI.v_path.set(path_shown)
            
            
            if not file_path == check_path:
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                    
                new_path = new_path + "\\" + file_name
                try:
                    shutil.move(file_path,new_path)
                except:             
                    GUI.v_path.set("Something somewhere went wrong")
             
            else:
                pass
                                
             
            
            root.update_idletasks()
            self.pb['value'] = self.pb['value'] + pb_stepsize
        
        for dirpath, dirnames, filenames in os.walk(folder, topdown=False):
          if not dirnames and not filenames:
              os.rmdir(dirpath)

    
                
if __name__ == '__main__':
    root = Tk()
    GUI = GUI(root)
    root.mainloop()

