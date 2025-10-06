import os
import hashlib
import argparse
from pathlib import Path

def calculate_file_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (IOError, PermissionError):
        return None

def get_file_info(directory):
    """Recursively collect file paths and their hashes in a directory."""
    file_info = {}
    directory = Path(directory).resolve()
    
    for file_path in directory.rglob("*"):
        if file_path.is_file():
            relative_path = str(file_path.relative_to(directory))
            file_hash = calculate_file_hash(file_path)
            if file_hash:
                file_info[relative_path] = file_hash
    return file_info

def compare_directories(dir1, dir2):
    """Compare two directories and return differences."""
    dir1_files = get_file_info(dir1)
    dir2_files = get_file_info(dir2)
    
    # Find all unique file paths
    all_files = set(dir1_files.keys()) | set(dir2_files.keys())
    
    changed = []
    disappeared = []
    appeared = []
    
    for file_path in all_files:
        if file_path in dir1_files and file_path in dir2_files:
            if dir1_files[file_path] != dir2_files[file_path]:
                changed.append(file_path)
        elif file_path in dir1_files:
            disappeared.append(file_path)
        else:
            appeared.append(file_path)
    
    return changed, disappeared, appeared

def main():
    parser = argparse.ArgumentParser(description="Compare two directories and report file differences.")
    parser.add_argument("dir1", help="Path to the first directory")
    parser.add_argument("dir2", help="Path to the second directory")
    args = parser.parse_args()
    
    # Validate directory paths
    dir1_path = Path(args.dir1)
    dir2_path = Path(args.dir2)
    
    if not dir1_path.is_dir():
        print(f"Error: {args.dir1} is not a valid directory")
        return
    if not dir2_path.is_dir():
        print(f"Error: {args.dir2} is not a valid directory")
        return
    
    # Compare directories
    changed, disappeared, appeared = compare_directories(dir1_path, dir2_path)
    
    # Print results
    if changed:
        print("\nChanged files:")
        for file in sorted(changed):
            print(f"  {file}")
    
    if disappeared:
        print("\nDisappeared files (present in first directory, missing in second):")
        for file in sorted(disappeared):
            print(f"  {file}")
    
    if appeared:
        print("\nNew files (present in second directory, missing in first):")
        for file in sorted(appeared):
            print(f"  {file}")
    
    if not (changed or disappeared or appeared):
        print("No differences found between the directories.")

if __name__ == "__main__":
    main()
