import zipfile

def unzip(zipfile_path, Dest):
    with zipfile.ZipFile(zipfile_path, "r") as archive:
        archive.extractall(Dest)



if __name__ == "__main__":

    unzip(
        "/Users/moe/Desktop/Code_Practice/Code_Practice/ScaleAI_Interview_Practice/ML_Interview_Pattern_Practice.zip",
        "ML_Interview_Pattern_Practice"
    )