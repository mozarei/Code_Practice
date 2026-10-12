import zipfile

def unzip(zipfile_path, Dest):
    with zipfile.ZipFile(zipfile_path, "r") as archive:
        archive.extractall(Dest)



if __name__ == "__main__":

    unzip(
        "/Users/mzarei/Desktop/Practices/Code_Practice/ScaleAI_Interview_Practice/Day_8_ML_Coding_Practice.zip",
        "Day_8_ML_Coding_Practice"
    )