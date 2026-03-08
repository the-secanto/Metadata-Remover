import os
from pathlib import Path
from PIL import Image
import piexif
import glob

def read_metadata(file_path: str) -> dict:
    img = Image.open(file_path)
    metadata = {}
    if img.format == "JPEG":
        exif_data = img.info.get("exif")
        if not exif_data:
            return {}
        exif_dict = piexif.load(exif_data)
        for ifd in exif_dict:
            if isinstance(exif_dict[ifd], dict):
                for tag_id, value in exif_dict[ifd].items():
                    tag_name = piexif.TAGS[ifd].get(tag_id, {"name": str(tag_id)})["name"]
                    metadata[tag_name] = value
    elif img.format == "PNG":
        metadata = dict(img.info)
    else:
        raise ValueError(f"Unsupported format: {img.format}")

    return metadata

def remove_metadata(file_path: str, output_path: str) -> None:
    img = Image.open(file_path)
    if img.format == "JPEG":
        exif_data = img.info.get("exif")
        if not exif_data:
            img.save(output_path, "jpeg")
            return

        exif_dict = piexif.load(exif_data)
        for ifd in exif_dict:
            if isinstance(exif_dict[ifd], dict):
                for tag in list(exif_dict[ifd].keys()):
                    tag_name = piexif.TAGS[ifd].get(tag, {"name": str(tag)})["name"]

                    if tag_name not in ("Orientation", "ColorSpace"):
                        del exif_dict[ifd][tag]
        exif_bytes = piexif.dump(exif_dict)
        img.save(output_path, "jpeg", exif=exif_bytes)
        
    elif img.format == "PNG":
        img.save(output_path, "png")
    else:
        raise ValueError(f"Unsupported format: {img.format}")

def process_file(file_path: str, output_dir: str = "cleaned_images") -> str:
    os.makedirs(output_dir, exist_ok=True)
    file_name = Path(file_path).name
    output_path = os.path.join(output_dir, file_name)
    remove_metadata(file_path, output_path)
    return output_path

def process_folder(folder_path: str, output_dir: str = "cleaned_images") -> list[str]:
    image_paths = glob.glob(os.path.join(folder_path, "*.[jJ][pP][gG]")) + \
                  glob.glob(os.path.join(folder_path, "*.[jJ][pP][eE][gG]")) + \
                  glob.glob(os.path.join(folder_path, "*.png"))

    if not image_paths:
        print("No images found in the folder")
        return []

    cleaned_files = []
    for path in image_paths:
        output_path = process_file(path, output_dir)
        cleaned_files.append(output_path)
    return cleaned_files