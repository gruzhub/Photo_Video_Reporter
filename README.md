# Photo Video Reporter 📸🎬

**Author:** Grzegorz Kuboszek, 2018

Analyze and report on media files (photos, RAW files, videos) in a directory. Convert RAW to DNG format and clean up RAW files without photo pairs.

---

## 🎯 Features

- **Media Analysis** - Scan directories for photos, RAW files, and videos
- **Report Generation** - Create text report with file counts, sizes, and video duration
- **RAW to DNG Conversion** - Batch convert RAW files using Adobe DNG Converter
- **Cleanup** - Remove RAW files without corresponding JPG/PNG pairs
- **Interactive Deletion** - Option to remove original RAW files after DNG conversion

---

## 📋 Supported Formats

- **Photos:** .jpg, .jpeg, .png, .tiff
- **RAW:** .rw2, .dng, .cr2, .nef, .arw, .srf, .crw, .orf
- **Video:** .mp4, .mov, .avi

---

## 🚀 Usage

```bash
python photo_video_reporter.py [options]
```

### Options
 `-t --target` | Directory to analyze (default: current dir)
 `-d --dng` | Convert RAW to DNG format
 `-r --remove-raw` | Remove RAW files without JPG pairs

### Examples

# Analyze current directory
python photo_video_reporter.py

# Analyze specific directory with DNG conversion
python photo_video_reporter.py -t "E:\test" -d

# All options
python photo_video_reporter.py -t "E:\test" -d -r
```
---

## ⚙️ Requirements

- **Python 3.7+**
- **Python packages:** `moviepy`, `tabulate`, `tqdm`
- **Adobe DNG Converter** (for `-d` option only)
  - Default path: `C:\Program Files\Adobe\Adobe DNG Converter\Adobe DNG Converter.exe`

---

## 📋 TODO

- Display orphaned RAW files during scanning
- Add `--photo` and `--video` filters
- Remove videos shorter than 4 seconds
- Input validation
- Dry-run mode for deletion