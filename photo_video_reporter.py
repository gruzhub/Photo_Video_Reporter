#Author: Grzegorz Kuboszek, 2018 
import argparse
import datetime
import subprocess
from pathlib import Path
from tabulate import tabulate
from moviepy.editor import VideoFileClip
from tqdm import tqdm


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

def RemoveRawWithoutPair(raw_list, PHOTO_EXTENSIONS):
    deleted_counter = 0
    deleted_size_bytes = 0
    
    for raw_file in raw_list:
        raw_filename = Path(raw_file).name.split('.')[0]
        
        pair_exist = False
        for extension in PHOTO_EXTENSIONS:
            if Path(raw_file).parent.joinpath(raw_filename + extension).exists():
                pair_exist = True
                break

        if not pair_exist:
            deleted_counter += 1
            deleted_size_bytes += Path(raw_file).stat().st_size
            print(f'{raw_file} has NO pair, deleting', end=' -> ')
            Path(raw_file).unlink()
            print('DELETED')

    return (deleted_counter, deleted_size_bytes)

def FileWalker(target, PHOTO_EXTENSIONS, RAW_EXTENSIONS, VIDEO_EXTENSIONS):
    photo_list = []
    photo_size_bytes = 0
    raw_list = []
    raw_size_bytes = 0 
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

            if file_extension in PHOTO_EXTENSIONS:
                print('PHOTO')
                photo_size_bytes += file_size_bytes
                photo_list.append(str(file))
            elif file_extension in RAW_EXTENSIONS:
                print('RAW')
                raw_size_bytes += file_size_bytes
                raw_list.append(str(file))
            elif file_extension in VIDEO_EXTENSIONS:
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

def CreateReport(REPORT_NAME, target, photo_stats, raw_stats, video_stats, other_stats):
    now = datetime.datetime.now()

    try:
        with open(target + "\\" + REPORT_NAME, "w") as f:
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

def ConvertDNGConverter(DNG_CONVERTER_PATH, raw_list):
    dng_converter_exist = Path(DNG_CONVERTER_PATH).exists()
    if not dng_converter_exist:
        print(f'Error: DNG Converter is not present at "{DNG_CONVERTER_PATH}"')
        return False, False
    
    if not raw_list:
        print("Warning: No RAW files to convert")
        return (0,0)

    successful = 0
    failed = 0
    
    for raw in tqdm(raw_list, desc="Converting RAW files to DNG"):
        command = [DNG_CONVERTER_PATH, '-c', raw]
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                successful += 1
            else:
                failed += 1
                print(f"Error converting {raw}: {result.stderr}")
        except Exception as ex:
            failed += 1
            print(f"Error launching DNG Converter for {raw}: {ex}")
    
    print(f"\nConversion complete: {successful} succeeded, {failed} failed")
    return (successful, failed)

##############
# MAIN SCRIPT
##############
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze media files')
    parser.add_argument('-t', '--target', type=str, default='.', help='Path to analyze (default: current directory)')
    #parser.add_argument('-p', '--photo', action='store_true', help='Analyze ONLY photos')
    #parser.add_argument('-v', '--video', action='store_true', help='Analyze ONLY videos')
    parser.add_argument('-d', '--dng', action='store_true', help='Convert RAW files to DNG format')
    parser.add_argument('-r', '--remove-raw', action='store_true', help='Remove RAW files without JPG pair')
    args = parser.parse_args()

    START_TIME = datetime.datetime.now()
    REPORT_NAME = f'{START_TIME.strftime("%Y-%m-%d_%H-%M-%S")}_report.txt'
    PHOTO_EXTENSIONS = ('.jpg', '.png', '.tiff', '.jpeg')
    RAW_EXTENSIONS = ('.rw2', '.dng', '.cr2', '.nef', '.arw', '.srf', '.crw', '.orf')
    VIDEO_EXTENSIONS = ('.mp4', '.mov', '.avi')
    DNG_CONVERTER_PATH = r'C:\Program Files\Adobe\Adobe DNG Converter\Adobe DNG Converter.exe'

    print("""
 _____ _       _          _____ _   _            _____                 _             
|  _  | |_ ___| |_ ___   |  |  |_|_| |___ ___   | __  |___ ___ ___ ___| |_ ___ ___   
|   __|   | . |  _| . |  |  |  | | . | -_| . |  |    -| -_| . | . |  _|  _| -_|  _|  
|__|  |_|_|___|_| |___|   \\___/|_|___|___|___|  |__|__|___|  _|___|_| |_| |___|_|   
                                                          |_|                        
""")
    target_exist = Path(args.target).exists()
    if not target_exist:
        print(f'Error: The specified path "{args.target}" is not a valid directory.')
        exit(1)

    #---------------
    # FILE ANALYSIS
    #---------------
    print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | Analyzing files in: {args.target}')
    photo_stats, raw_stats, video_stats, other_stats = FileWalker(args.target, PHOTO_EXTENSIONS, RAW_EXTENSIONS, VIDEO_EXTENSIONS)
    print(f'{raw_stats[2]}')
    #---------
    # SUMMARY
    #---------
    script_duration = datetime.datetime.now() - START_TIME
    script_duration = str(script_duration).split('.')[0] # Remove miliseconds
    
    print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | Elapsed time: {script_duration} | Total files found: {photo_stats[1] + raw_stats[1] + video_stats[1] + other_stats[1]} \n')
    
    headers = ['Type', 'Files', 'Size', 'Duration (s)']
    tabulate_data = [
        ['Photos', photo_stats[1], ConvertSize(photo_stats[0]), "-"],
        ['RAW', raw_stats[1], ConvertSize(raw_stats[0]), "-"],
        ['Video', video_stats[1], ConvertSize(video_stats[0]), round(video_stats[2], 2)],
        ['Others', other_stats[1], ConvertSize(other_stats[0]), "-"] , 
        ['TOTAL', photo_stats[1] + raw_stats[1] + video_stats[1] + other_stats[1], ConvertSize(photo_stats[0] + raw_stats[0] + video_stats[0] + other_stats[0]), round(video_stats[2], 2)]
        ]
    
    print(tabulate(tabulate_data, headers=headers, tablefmt="github") + '\n')

    #-----------------
    # REPORT CREATION
    #-----------------
    print(f'Creating report in target directory {args.target}', end=' -> ')
    CreateReport(REPORT_NAME, args.target, photo_stats, raw_stats, video_stats, other_stats)
    print('DONE')

    #-------------
    # RAW CLEANUP
    #-------------
    if args.remove_raw:
        deleted_counter, deleted_size_bytes = RemoveRawWithoutPair(raw_stats[2], PHOTO_EXTENSIONS)
        with open(args.target + '\\' + REPORT_NAME, 'a') as f:
            f.write(f'\n{deleted_counter} RAW files has been deleted, freed: {ConvertSize(deleted_size_bytes)}')
            f.close()
        print(f'{deleted_counter} RAW files has been deleted, freed: {ConvertSize(deleted_size_bytes)}')

    #---------------
    # DNG CONVERTER
    #---------------
    if args.dng:
        print(f'Launching DNG Converter', end=' -> ')
        successful, failed = ConvertDNGConverter(DNG_CONVERTER_PATH, raw_stats[2])


        with open(args.target + '\\' + REPORT_NAME, 'a') as f:
            f.write(f'\nConverted: {successful}, failed conversion: {failed}, TOTAL : {successful + failed}')
            f.close()

        remove_raw = input('Do you want to remove original RAW files after conversion? (y/n): ')
        if remove_raw.lower() == 'y':
            removed = 0
            for raw in tqdm(raw_stats[2], desc="Deleting original RAW files"):
                try:
                    Path(raw).unlink()
                    removed += 1
                except Exception as ex:
                    print(f"Error deleting RAW file {raw}: {ex}")      
            with open(args.target + '\\' + REPORT_NAME, 'a') as f:
                f.write(f'\nRemoved original RAW files: {removed}')
                f.close()
    
    print('End of script, thank you for using Photo Video Reporter!')