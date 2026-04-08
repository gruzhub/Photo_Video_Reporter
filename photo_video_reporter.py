#Author: Grzegorz Kuboszek, 2018 
import datetime, argparse
from pathlib import Path
from moviepy.editor import VideoFileClip

# Get list of all files in every directory within the path - recursive searching
def ListAllFiles(path):
    files_list = []
    for media_file in Path(path).rglob('*'):
        if media_file.is_file():
            files_list.append(str(media_file))

    return files_list, len(files_list)

#Get movie duraction and closing readers in case of exception
def getDuration(filename):
    movie = VideoFileClip(filename)
    duration = movie.duration
    movie.reader.close()
    movie.audio.reader.close_proc()
    return duration

#Convert round size to MB or GB
def convertSize(size):
    size = size / 1024
    if size > 1000:
        size = size / 1024
        sizeString = str(round(size,3)) + " GB"         
    else:
        sizeString = str(round(size,3)) + " MB"
    
    return sizeString

#Removing RAW without pair with JPG
def removeRawWithoutPair(filesPath, rawExt):
    deleted = 0
    for filePath in filesPath:
        if filePath["ext"] in rawExt:            
            filename, extension = os.path.splitext(filePath["path"])
        
            if not os.path.isfile(filename + ".jpg") or not os.path.isfile(filename + ".JPG"):
                print("RAW file: " + filePath["path"] + " haven't pair with JPG, removing...")
                try:
                    os.remove(filePath["path"])
                    deleted += 1
                
                except Exception as ex:
                    print("[removeRawWithoutPair] Exception occured: " + str(ex))

    return deleted

def FileWalker(target):
    photo_extensions = {".jpg", ".png", ".tiff", ".jpeg"}
    photo_list = []
    photo_count = 0
    photo_size_bytes = 0.0
    
    raw_extensions = {".rw2", ".dng", ".cr2", ".nef", ".arw", ".srf", ".crw", ".orf"}
    raw_list = []
    raw_count = 0
    raw_size_bytes = 0.0
    
    video_extensions = {".mp4", ".mov", ".avi"}
    video_list = []
    video_count = 0
    video_duration_seconds = 0.0
    video_size_bytes = 0.0
    
    #excluded_extensions = {".txt", ".py", ".bat", ".doc", ".docx", ".xls", ".xlsx", ".pdf", ".zip", ".rar", ".7z", ".exe", ".dll", ".iso", ".img", ".log", ".ps1"}
    other_count = 0
    other_size_bytes = 0.0
    size_all_bytes = 0.0

    for file in Path(target).rglob('*'):
        if file.is_file():
            print(f"Proessing file: {file}", end=' -> ')
            file_extension = Path(file).suffix.lower()
            file_size_bytes = Path(file).stat().st_size
            size_all_bytes += file_size_bytes

            if file_extension in photo_extensions:
                print('PHOTO')
                photo_count += 1
                photo_size_bytes += file_size_bytes
                photo_list.append(str(file))
            elif file_extension in raw_extensions:
                print('RAW')
                raw_count += 1
                raw_size_bytes += file_size_bytes
                raw_list.append(str(file))
            elif file_extension in video_extensions and not args.photo:
                print('VIDEO')
                video_count += 1
                video_size_bytes += file_size_bytes
                video_list.append(str(file))
                try:
                    video_clip = VideoFileClip(file)
                    video_duration_seconds += video_clip.duration
                    video_clip.reader.close()
                except Exception as ex:
                    print(f"Error processing video file {file}: {ex}")    
            else:
                print('EXCLUDED')
                other_count += 1
                other_size_bytes += file_size_bytes
            


    return
##############
# MAIN SCRIPT
##############
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze media files')
    parser.add_argument('-t', '--target', type=str, default='.', help='Path to analyze (default: current directory)')
    parser.add_argument('-p', '--photo', action='store_true', help='Analyze ONLY photos')
    parser.add_argument('-v', '--video', action='store_true', help='Analyze ONLY videos')
    parser.add_argument('-d', '--dng', action='store_true', help='Convert RAW files to DNG format')
    args = parser.parse_args()
    
    START_TIME = datetime.datetime.now()
    REPORT_NAME = f"{START_TIME.strftime('%Y-%m-%d_%H-%M-%S')}_MediaReport.txt"
    
    print("""
 _____ _       _          _____ _   _            _____                 _             
|  _  | |_ ___| |_ ___   |  |  |_|_| |___ ___   | __  |___ ___ ___ ___| |_ ___ ___   
|   __|   | . |  _| . |  |  |  | | . | -_| . |  |    -| -_| . | . |  _|  _| -_|  _|  
|__|  |_|_|___|_| |___|   \\___/|_|___|___|___|  |__|__|___|  _|___|_| |_| |___|_|    
                                                          |_|                                 
""")
    if not args.target.isdir():
        print(f"Error: The specified path '{args.target}' is not a valid directory.")
        exit(1)

    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Files analyzing in path: {args.target}")
    #files_list, total_files = ListAllFiles(args.target)
        
    FileWalker(args.target)
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Total files found: {total_files}")

    
    """

    #Writing to file report
    try:
        f = open(FINALreportFile, "w")
        f.write("Report creation time: " + finishTime.strftime("%Y-%m-%d %H:%M:%S"))
        f.write("\nScript duration: " + str(scriptDuration))
        f.write("\n")
        f.write("="*30)
        f.write("\nMovie clips: " + str(movieCount))
        f.write("\nMovie duration: " + str(movieDuration))
        f.write("\nMovie size: " + convertSize(movieSize))
        f.write("\n")
        f.write("="*30)
        f.write("\nFoto counter: " + str(fotoCount))
        f.write("\nFoto size: " + convertSize(fotoSize))
        f.write("\nRAW counter: " + str(rawCount))
        f.write("\nRAW size: " + convertSize(rawSize))
        f.write("\n")
        f.write("="*30)
        f.write("\nUnknown files counter: " + str(otherCount))
        f.write("\nUnknown files size: " + convertSize(otherSize))
        f.write("\nSize of all files: " + convertSize(sizeAll))
        f.close()

    except Exception as ex:
        print("[VID_COLLECTOR_REPORT] Exception occured during creating and writing file: " + str(ex))
        exit()

    #Optional removing RAW without JPG pair
    option = input("Remove RAW files without JPG pair? [y/n]: ")
    if option == "y" or option == "Y":
        deleted = removeRawWithoutPair(report,rawExt)
        print(str(deleted) + " files has been deleted")
        f = open(FINALreportFile, "a")
        f.write("\nRAW files without JPG pair delected, " + str(deleted) + " files has been removed")
    else:
        print("Goodbye!")
"""