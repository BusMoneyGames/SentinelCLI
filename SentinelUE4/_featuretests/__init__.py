# coding=utf-8
import pathlib


def get_test_data_path():
    """
    construct the path to the test data folder
    :return: test data path
    """

    current_folder: pathlib.Path = pathlib.Path(__file__).parent
    test_data_path = current_folder.joinpath("testdata")

    return test_data_path
