#   Created by Jiří Strouhal (2023).
#   Written in Python 3.10.10
#   Licensed under the MIT License. See the LICENSE in the project root folder. 
#   Public repository: https://github.com/jiristrouhal/makewxs.
#   Use MznStrouhal@gmail.com to reach the author.


import make_wxs_tools as mwt
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
import tkinter as tk
import os
import xml.etree.ElementTree as et
import appdirs


#set default source and target to the root location, independent of OS
DEFAULT_SOURCE = os.path.abspath(os.sep)
DEFAULT_TARGET = os.path.abspath(os.sep)
DEFAULT_PROJECT_NAME = "untitled_app"


APP_NAME = "MakeWxs"
AUTHOR_NAME = "MakeWxs"
LOCAL_DATA_FOLDER = appdirs.user_data_dir(APP_NAME, AUTHOR_NAME)
LAST_USED_LOCS_XML_NAME = "last_used_locs.xml"
LAST_USED_LOCS_XML_PATH = os.path.join(LOCAL_DATA_FOLDER, LAST_USED_LOCS_XML_NAME)


def main():

    project_name_win = tk.Tk()
    project_name_win.title("Enter the project name")
    project_name_win.iconbitmap("src/makewxs.ico")

    last_source = DEFAULT_SOURCE
    last_target = DEFAULT_TARGET
    last_project_name = DEFAULT_PROJECT_NAME

    try: 
        last_locs = et.parse(LAST_USED_LOCS_XML_PATH)
        last_locs_root = last_locs.find("LastUsedLocations")
        last_source = last_locs_root.find("Source").text
        last_target = last_locs_root.find("Target").text
        last_project_name = last_locs_root.find("ProjectName").text
    except:
        if not os.path.isdir(LOCAL_DATA_FOLDER): os.makedirs(LOCAL_DATA_FOLDER)
        last_locs_root = et.Element("LastUsedLocations")
        last_source = DEFAULT_SOURCE
        last_target = DEFAULT_TARGET
        last_project_name = DEFAULT_PROJECT_NAME
        et.SubElement(last_locs_root,"Source").text=DEFAULT_SOURCE
        et.SubElement(last_locs_root,"Target").text=DEFAULT_TARGET
        et.SubElement(last_locs_root,"ProjectName").text=DEFAULT_PROJECT_NAME
        et.indent(last_locs_root,"\t")
        et.ElementTree(last_locs_root).write(LAST_USED_LOCS_XML_PATH,encoding="UTF-8",xml_declaration=True)

    target = askdirectory(title="Select target directory", initialdir=last_target)
    if target=="":
        showerror(title="No target directory selected", message="No target directory selected. The program will exit without action.") 
        return

    source = askdirectory(title="Select source directory", initialdir=last_source)
    if source=="": 
        showerror(title="No source directory selected", message="No source directory selected. The program will exit without action.") 
        return
    

    last_locs_root = et.parse(LAST_USED_LOCS_XML_PATH)
    last_locs_root.find("Source").text = source
    last_locs_root.find("Target").text = target
    last_locs_root.write(LAST_USED_LOCS_XML_PATH) 


    project_name_entry = tk.Entry(master=project_name_win,width=60)
    project_name_entry.pack()
    project_name_entry.insert(tk.END, last_project_name)

    def confirm_name()->None:
        project_name_win.quit()

    ok_button = tk.Button(master=project_name_win, text="Ok", command=confirm_name)
    ok_button.pack(side=tk.BOTTOM)
    ok_button.focus()
    project_name_win.mainloop()
    
    last_locs_root.find("ProjectName").text = project_name_entry.get()
    last_locs_root.write(LAST_USED_LOCS_XML_PATH)

    mwt.get_wxs_files(source, target, project_name_entry.get())

    return


main()
