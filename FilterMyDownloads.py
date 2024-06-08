import os
from datetime import datetime
import shutil
import time

def Menu():
    print("\033[32mWelcome to \033[33mFilterMyDownloads")
    print("\033[32mThis program made by \033[92mFaisal or \033[0;33mgugga")
    print("\033[32mPlease select the type of filter:")
    print("1- \033[32mDate")
    print("2- \033[32mFile Format\033[0m")
    print("\033[31m3- Delete Empty Folders\033[0m")
    print("\033[31m4- Exit\033[0m")
    put = input("Enter your action: (1, 2, 3 or 4): ").strip()
    if put not in ["1","2","3","4"]:
        raise ValueError("Invaild input. please enter 1, 2, 3 or 4")
    return put

def get_file_date(file_path):
    
    time = os.path.getctime(file_path)
    return datetime.fromtimestamp(time)

def create_folder(base_path, folder_name):
    
    folder_location = os.path.join(base_path, folder_name)
    try:
        if not os.path.exists(folder_location):
            os.makedirs(folder_location)
        return folder_location
    except OSError as err:
        print(f"Error creating folder {folder_name}: {err}")
        log("Error",f"Error creating folder {folder_name}: {err}")
    
def filter_by_format(download_folder):
    
    
    image_formats = ["png","jpeg","jpg","gif","webp"]
    word_formats = ["doc","docx"]
    excel_formats = ["XLS","XLSX"]
    
    
    files = [file for file in os.listdir(download_folder) if os.path.isfile(os.path.join(download_folder,file)) and os.path.abspath(os.path.join(download_folder, file)) != log_path]
    
    for file in files:
        if file == "FilteringMyDownloads.log":
            continue
        file_location = os.path.join(download_folder,file)
        file_format = file.split('.')[-1].lower()
        
        if file_format in image_formats:
            folder = create_folder(download_folder, "Images")
        elif file_format in word_formats:
            folder = create_folder(download_folder, "Word Files")
        elif file_format in excel_formats:
            folder = create_folder(download_folder, "Excel Files")
        else:
            folder = create_folder(download_folder, file_format.lower())
        try:       
            shutil.move(file_location,folder)
            print(f"The file {file} moved to {folder}")
            log("Moved",f"{file} to {folder}")
        except shutil.Error as sherr:
            print(f"Error moving file {file} to {folder}")
            log("Error",f"Error moving file {file} to {folder}: {sherr}")
        
        
def filter_by_date(download_folder):
    
    files = [file for file in os.listdir(download_folder) if os.path.isfile(os.path.join(download_folder,file))]
    
    for file in files:
        if file == "FilterMyDownloads.log":
            continue
        file_path = os.path.join(download_folder,file)
        file_download_date = get_file_date(file_path)
        folder_name = file_download_date.strftime("%Y-%m")
        folder = create_folder(download_folder,folder_name)
        shutil.move(file_path,folder)
        print(f"The file {file} moved to {folder}") 
        log("Moved",f"{file} to {folder_name}")   
    
def delete_all_empty_folders(download_folder):
    for folder_name in os.listdir(download_folder):
        folder_path = os.path.join(download_folder, folder_name)
        if os.path.isdir(folder_path) and not os.listdir(folder_path):
            confirmation = input(f"Are you sure you want to delete empty folder '{folder_path}'? (y/n): ")
            if confirmation.lower() == 'y':
                try:
                    os.rmdir(folder_path)
                    print(f"Deleted empty folder: {folder_path}")
                except OSError as e:
                    print(f"Error deleting folder {folder_path}: {e}")
            else:
                print(f"Skipping deletion of empty folder: {folder_path}")
    print("Done")
                
                
def log(action, location):
        log_file = os.path.join(log_path, "FilteringMyDownloads.log")
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file,'a',encoding='utf-8') as w:
            w.write(f"{time} - {action}: {location}\n")

##Custom filter, such as, file size

##Creating GUI for the first time

##confirmation for every action by user

##duplication for duplicated files

##undo maybe?

def Main():
    
    download_path = input(r"Please enter your downloads path (for example: C:\Users\(UserName)\Downloads): ")
    global log_path
    log_path = os.path.join(download_path)
    try:    
        userInput = Menu()
        if userInput == "1":
            filter_by_date(download_path)
            time.sleep(5)
        elif userInput == "2":
            filter_by_format(download_path)
            time.sleep(5)
        elif userInput == "3":
            delete_all_empty_folders(download_path)
            time.sleep(5)
        elif userInput == "4":
            os.system("exit")
        else:
            print("err")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        log("Error",f"Unexpected error in main function: {e}")
        
Main()
