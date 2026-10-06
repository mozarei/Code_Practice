import zipfile

def unzip(zipfile_path, Dest):
    with zipfile.ZipFile(zipfile_path, "r") as archive:
        archive.extractall(Dest)



if __name__ == "__main__":

    unzip(
        "/Users/moe/Desktop/Code_Practice/SCale_Interview_Practice/Day_3_ML_Coding_Practice.zip",
        "Day_3_ML_Coding_Practice"
    )