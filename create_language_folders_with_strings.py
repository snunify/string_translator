import os


def create_language_folders_with_strings():
    for code in language_codes:
        # Create folder path
        folder_path = os.path.join(base_path, f"values-{code}")

        # Check if folder already exists, if not, create it
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Create strings.xml file with default content only if it does not exist
        file_path = os.path.join(folder_path, "strings.xml")
        if not os.path.exists(file_path):
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
base_path = "/home/unify/Documents/patient-sep/uc-patient-android/core/designsystem/src/main/res/"  # Adjust as needed
create_language_folders_with_strings()