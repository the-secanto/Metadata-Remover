import os
from pathlib import Path
from ex_main import read_metadata, process_file, process_folder
import argparse
import glob

def display_metadata(file_path: str) -> None:
    metadata = read_metadata(file_path)
    if not metadata:
        print(f"No metadata found for {file_path}")
    else:
        print(f"\nMetadata for {file_path}:")
        for k, v in metadata.items():
            print(f"{k}: {v}")

def main():
    parser = argparse.ArgumentParser(description="Metadata Tool for JPEG/PNG files.")
    parser.add_argument("input_path", help="File or folder path")
    parser.add_argument("-r", "--read", action="store_true", help="Display metadata")
    parser.add_argument("-c", "--clean", action="store_true", help="Remove metadata")
    parser.add_argument("-o", "--output", default="cleaned_images", help="Output folder for scrubbed images")

    args = parser.parse_args()
    input_path = args.input_path
    output_dir = args.output

    if not os.path.exists(input_path):
        print("Error, the path does not exist.")
        return

    if args.read:
        if os.path.isfile(input_path):
            display_metadata(input_path)
        elif os.path.isdir(input_path):
            for ext in ["*.jpg", "*.jpeg", "*.png"]:
                for file in glob.glob(os.path.join(input_path, ext)):
                    display_metadata(file)
        else:
            print("Invalid input path for reading metadata.")

    if args.clean:
        if os.path.isfile(input_path):
            output_file = process_file(input_path, output_dir)
            print(f"Cleaned file saved to: {output_file}")
        elif os.path.isdir(input_path):
            cleaned_files = process_folder(input_path, output_dir)
            print(f"Cleaned {len(cleaned_files)} files. Saved to {output_dir}")
        else:
            print("Invalid input path for cleaning metadata.")

if __name__ == "__main__":
    main()