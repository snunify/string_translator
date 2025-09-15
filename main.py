import asyncio
from googletrans import Translator
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from concurrent.futures import ThreadPoolExecutor

base_path = "/home/unify/Documents/uc/uc-patient-android/core/designsystem/src/main/res/"


def get_language_folders():
    language_folders = [
        folder for folder in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, folder)) and folder.startswith("values")
    ]
    return language_folders


def extract_strings_from_xml(file_path):
    string_map = {}
    try:
        tree = ET.parse(file_path)
    except:
        return string_map
    root = tree.getroot()

    for string_element in root.findall("string"):
        key = string_element.get("name")
        if string_element.get("translatable") == "false":
            continue
        value = string_element.text
        if key and value:
            string_map[key] = value
    return string_map

def extract_language_code(values_folder):
    return values_folder.split("-")[1] if "-" in values_folder else "en"

translations = {}

values_folders = get_language_folders()

# Use ThreadPoolExecutor to parallelize string extraction
def extract_strings_for_folder(folder):
    strings_file = base_path + folder + "/strings.xml"
    string_map = extract_strings_from_xml(strings_file)
    lan_code = extract_language_code(folder)
    print(f"{lan_code} count = {len(string_map)}")
    translations[lan_code] = string_map

# Run string extraction in parallel using ThreadPoolExecutor
with ThreadPoolExecutor() as executor:
    executor.map(extract_strings_for_folder, values_folders)

async def check_all_strings_exist_in_other_languages():
    en_strings = translations.get("en", {})
    async with Translator() as translator:
        tasks = []
        for lang, strings in translations.items():
            if lang == "en":
                continue
            for key, value in en_strings.items():
                if key not in strings:
                    to_translate = en_strings[key]
                    print("Not translated to " + lang + ":", to_translate)
                    task = translator.translate(to_translate, dest=lang, src="en")
                    tasks.append((key, lang, task))  # Added lang to the task

        results = await asyncio.gather(*[task[2] for task in tasks])  # Use task[2] for results
        for i, (key, lang, result) in enumerate(
                zip([task[0] for task in tasks], [task[1] for task in tasks], results)):
            strings = translations[lang]
            strings[key] = result.text
    print(translations)
    create_xml_from_translations()

def prettify_xml(element):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(element, encoding="utf-8")
    parsed = minidom.parseString(rough_string)
    return parsed.toprettyxml(indent="    ")


def create_xml_from_translations():
    for lang, strings in translations.items():
        if lang == "en":
            continue
        root = ET.Element("resources", {
            "xmlns:tools": "http://schemas.android.com/tools"
        })
        for key, value in strings.items():
            attributes = {"name": key}
            if key == "in_progress":
                attributes["tools:url"] = "https://example.com/docs/in_progress"
            string_element = ET.SubElement(root, "string", attributes)
            string_element.text = value

        tree = ET.ElementTree(root)
        pretty_xml = prettify_xml(root)

        file_name = f"{base_path}values-{lang}/strings.xml"
        print("updated: " + file_name)
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(pretty_xml)

print(translations)
asyncio.run(check_all_strings_exist_in_other_languages())
