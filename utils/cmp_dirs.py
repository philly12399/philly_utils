import os

def compare_directories(dir1, dir2):
    # Get the list of files in each directory
    files1 = set(os.listdir(dir1))
    files2 = set(os.listdir(dir2))

    # Find common files
    common_files = files1.intersection(files2)
    print(f"Common files: {len(common_files)}, DirA:{len(files1)}, DirB:{len(files2)}")
    # Compare the content of common files
    for filename in common_files:
        filepath1 = os.path.join(dir1, filename)
        filepath2 = os.path.join(dir2, filename)
        if os.path.isfile(filepath1) and os.path.isfile(filepath2):
            with open(filepath1, 'rb') as file1, open(filepath2, 'rb') as file2:
                content1 = file1.read()
                content2 = file2.read()
                if content1 == content2:
                    pass
                else:
                    print(f"File '{filename}' has different content in both directories.")
        else:
            print(f"File '{filename}' is not present in both directories or is not a file.")

if __name__ == "__main__":
    dir1 = "/home/philly12399/philly_ssd/ab3dmot/NDT_pkl/cache_pool32/0000/"
    dir2 = "/home/philly12399/philly_ssd/ab3dmot/NDT_pkl/cache_pool16/0000/"
    
    compare_directories(dir1, dir2)
