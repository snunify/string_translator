import os

def create_language_folders_with_strings():
    for code in language_codes:
        # Create folder path
        folder_path = os.path.join(base_path, f"values-{code}")
        os.makedirs(folder_path, exist_ok=True)

        # Create strings.xml file with default content
        file_path = os.path.join(folder_path, "strings.xml")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("<resources></resources>")


language_codes = [
    "bn",  # Bengali
    "gu",  # Gujarati
    "hi",  # Hindi
    "kn",  # Kannada
    "ml",  # Malayalam
    "mr",  # Marathi
    "pa",  # Punjabi
    "ta",  # Tamil
    "te",  # Telugu
    "ur",  # Urdu
]
base_path = "/home/unify/Documents/string translator/ex/"  # Adjust as needed
create_language_folders_with_strings()