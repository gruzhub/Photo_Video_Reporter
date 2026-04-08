#Author: Grzegorz Kuboszek, 2018 
import argparse, datetime
from pathlib import Path
from tabulate import tabulate
from moviepy.editor import VideoFileClip

def ConvertSize(size_bytes: float):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    
    size_kb = size_bytes / 1024
    if size_kb < 1024:
        return f"{round(size_kb, 3)} KB"
    
    size_mb = size_kb / 1024
    if size_mb < 1024:
        return f"{round(size_mb, 3)} MB"
    
    size_gb = size_mb / 1024
    return f"{round(size_gb, 3)} GB"

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
    photo_extensions = (".jpg", ".png", ".tiff", ".jpeg")
    photo_list = []
    photo_size_bytes = 0
    
    raw_extensions = (".rw2", ".dng", ".cr2", ".nef", ".arw", ".srf", ".crw", ".orf")
    raw_list = []
    raw_size_bytes = 0
    
    video_extensions = (".mp4", ".mov", ".avi")
    video_list = []
    video_duration_seconds = 0
    video_size_bytes = 0
    
    other_count = 0
    other_size_bytes = 0
    size_all_bytes = 0

    for file in Path(target).rglob('*'):
        if file.is_file():
            print(f"{file}", end=' -> ')
            file_extension = Path(file).suffix.lower()
            file_size_bytes = Path(file).stat().st_size
            size_all_bytes += file_size_bytes

            if file_extension in photo_extensions:
                print('PHOTO')
                photo_size_bytes += file_size_bytes
                photo_list.append(str(file))
            elif file_extension in raw_extensions:
                print('RAW')
                raw_size_bytes += file_size_bytes
                raw_list.append(str(file))
            elif file_extension in video_extensions and not args.photo:
                print('VIDEO')
                video_size_bytes += file_size_bytes
                video_list.append(str(file))
                try:
                    video_clip = VideoFileClip(str(file))
                    video_duration_seconds += video_clip.duration
                    video_clip.close()
                except Exception as ex:
                    print(f"Error processing video file {file}: {ex}")
            else:
                print('EXCLUDED')
                other_count += 1
                other_size_bytes += file_size_bytes

    return (photo_size_bytes, len(photo_list), photo_list), \
            (raw_size_bytes, len(raw_list), raw_list), \
            (video_size_bytes, len(video_list), round(video_duration_seconds, 0), video_list), \
            (other_size_bytes, other_count)

def CreateReport(target, photo_stats, raw_stats, video_stats, other_stats):
    now = datetime.datetime.now()
    report_name = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_MediaReport.txt"
    try:
        with open(target + "\\" + report_name, "w") as f:
            f.write(f"Report creation time: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Analyzed path: {target}\n")
            f.write("-"*30 + "\n")
            f.write(f"Photo count: {photo_stats[1]}\n")
            f.write(f"Photo size: {ConvertSize(photo_stats[0])}")
            f.write("\n" + "-"*30 + "\n")
            f.write(f"RAW count: {raw_stats[1]}\n")
            f.write(f"RAW size: {ConvertSize(raw_stats[0])}")
            f.write("\n" + "-"*30 + "\n")
            f.write(f"Movie clips: {video_stats[1]}\n")
            f.write(f"Movie duration: {video_stats[2]} seconds\n")
            f.write(f"Movie size: {ConvertSize(video_stats[0])}")
            f.write("\n" + "-"*30 + "\n")
            f.write(f"Other files count: {other_stats[1]}\n")
            f.write(f"Other files size: {ConvertSize(other_stats[0])}")
            f.write("\n" + "-"*30 + "\n")
            f.write(f"Total size of all files: {ConvertSize(video_stats[0] + photo_stats[0] + raw_stats[0] + other_stats[0])}")
            f.close()
    except Exception as ex:
        print(f"Error occured: {ex}")
    
    return 0

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
    
    print("""
 _____ _       _          _____ _   _            _____                 _             
|  _  | |_ ___| |_ ___   |  |  |_|_| |___ ___   | __  |___ ___ ___ ___| |_ ___ ___   
|   __|   | . |  _| . |  |  |  | | . | -_| . |  |    -| -_| . | . |  _|  _| -_|  _|  
|__|  |_|_|___|_| |___|   \\___/|_|___|___|___|  |__|__|___|  _|___|_| |_| |___|_|    
                                                          |_|                        
""")
    target_exist = Path(args.target).exists()
    if not target_exist:
        print(f"Error: The specified path '{args.target}' is not a valid directory.")
        exit(1)

    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Analyzing files in: {args.target}")
    photo_stats, raw_stats, video_stats, other_stats = FileWalker(args.target)
    
    script_duration = datetime.datetime.now() - START_TIME
    script_duration = str(script_duration).split('.')[0] # Remove miliseconds
    
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Elepased time: {script_duration} | Total files found: {photo_stats[1] + raw_stats[1] + video_stats[1] + other_stats[1]} \n")
    
    headers = ["Type", "Files", "Size", "Duration (s)"]
    tabulate_data = [
        ["Photos", photo_stats[1], ConvertSize(photo_stats[0]), "-"],
        ["RAW", raw_stats[1], ConvertSize(raw_stats[0]), "-"],
        ["Video", video_stats[1], ConvertSize(video_stats[0]), round(video_stats[2], 2)],
        ["Others", other_stats[1], ConvertSize(other_stats[0]), "-"] , 
        ["TOTAL", photo_stats[1] + raw_stats[1] + video_stats[1] + other_stats[1], ConvertSize(photo_stats[0] + raw_stats[0] + video_stats[0] + other_stats[0]), round(video_stats[2], 2)]
        ]
    
    print(tabulate(tabulate_data, headers=headers, tablefmt="github") + '\n')

    print(f"Creating report in target directory {args.target}")
    CreateReport(args.target, photo_stats, raw_stats, video_stats, other_stats)
    
    """

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