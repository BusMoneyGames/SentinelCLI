# coding=utf-8
import zipfile
import shutil
import os
import logging
from PIL import Image

L = logging.getLogger(__name__)


def zip_folder(folder_path, folder_name):

    zip_file_name = folder_name + ".zip"
    zip_file_path = os.path.join(folder_path, zip_file_name)
    zipobj = zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_STORED)

    rootlen = len(folder_path.as_posix()) + 1
    for base, dirs, files in os.walk(folder_path):
        for file in files:
            if file == zip_file_name:
                # Skipping the zip file itself
                continue
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])

    return zip_file_path


def delete_folder(path):

    L.debug("Removing: %s", path)
    if os.path.exists(path):
        shutil.rmtree(path)


def unzip_folder(zip_file_path, output_path):
    zip_ref = zipfile.ZipFile(zip_file_path, 'r')
    zip_ref.extractall(output_path)
    zip_ref.close()


def compress_png_to_jpg(image_list):
    """
    Goes through a list of screenshots and compresses them as jpg's.  The jpgs are stored at the same path with the
    extention changed to .jpg

    :param image_list: list of png images to compress
    :return: list of compressed image paths
    """

    compressed_files = []

    for source_image_path in image_list:
        source_image_path = source_image_path.as_posix()
        jpg = source_image_path.replace(".png", ".jpg")

        # Converting the image to jpg and saving it
        img = Image.open(source_image_path).convert('RGB')
        img.save(jpg, quality=100, optimize=True)

        # Adding to the list
        compressed_files.append(jpg)

    return compressed_files


def compress_png_file(png_file_path, output_file_path):

    img = Image.open(png_file_path).convert('RGB')
    img.save(output_file_path, quality=100, optimize=True)

    return output_file_path


def get_all_file_paths_of_type_in_directory(root_directory, file_type):
    """
    Return a path to all files of type inside of a folder
    :param root_directory: root folder of the search
    :param file_type: type of file
    :return: list of found files
    """

    if not file_type.startswith("."):
        file_type = "." + file_type

    L.debug("Searching for all files of type: \"%s\" in directory \"%s\"", file_type, root_directory)
    found_file_list = []

    for dirName, subdirList, fileList in os.walk(root_directory):
        for fname in fileList:
            if fname.endswith(file_type):
                found_file = os.path.join(dirName, fname)
                L.debug(found_file)
                found_file_list.append(found_file)

    L.debug("Found: %s number of files", str(len(found_file_list)))

    return found_file_list


def get_all_file_paths_from_directory(root_directory):
    found_file_list = []
    for dirName, subdirList, fileList in os.walk(root_directory):
        for fname in fileList:
                found_file = os.path.join(dirName, fname)
                L.debug(found_file)
                found_file_list.append(found_file)

    return found_file_list
