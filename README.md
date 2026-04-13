# Photo Video Reporter

**Author:** Grzegorz Kuboszek, 2018

Analyze and report on media files (photos, RAW files, videos) in a directory. Convert RAW to DNG format and clean up RAW files without photo pairs.
---
## Features
- **Media Analysis** - Scan directories for photos, RAW files, and videos
- **Report Generation** - Create text report with file counts, sizes, and video duration
- **RAW to DNG Conversion** - Batch convert RAW files using Adobe DNG Converter
- **Cleanup** - Remove RAW files without corresponding JPG/PNG pairs

## Supported Formats
- **Photos:** .jpg, .jpeg, .png, .tiff
- **RAW:** .rw2, .dng, .cr2, .nef, .arw, .srf, .crw, .orf
- **Video:** .mp4, .mov, .avi

## Arguments
 - `-t --target` Directory to analyze (default: current dir)
 - `-d --dng` Convert RAW to DNG format
 - `-r --remove-raw` Remove RAW files without JPG pairs

## TODO
- [ ] Display orphaned RAW files during scanning
- [ ] Add `--photo` and `--video` filters
- [ ] Remove videos shorter than 4 seconds
- [ ] Input validation