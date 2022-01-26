import logging
import os

import numpy as np
import pytest

from kale.loaddata.tabular_access import load_csv_columns
from kale.utils.download import download_file_by_url
from kale.utils.seed import set_seed

seed = 36
set_seed(seed)

LOGGER = logging.getLogger(__name__)

EXPECTED_COLS = [
    "uid",
    "E-CPV Error",
    "E-CPV Uncertainty",
    "E-MHA Error",
    "E-MHA Uncertainty",
    "S-MHA Error",
    "S-MHA Uncertainty",
    "Validation Fold",
    "Testing Fold",
]
landmark_uncertainty_url = (
    "https://github.com/pykale/data/raw/main/tabular/cardiac_landmark_uncertainty/Uncertainty_tuples.zip"
)


# @pytest.mark.parametrize("source_test_file", ["PHD-Net/4CH/uncertainty_pairs_test_l0"])
# @pytest.mark.parametrize(
#     "return_columns",
#     [
#         ("All", EXPECTED_COLS),
#         ([], []),
#         ("S-MHA Error", ["S-MHA Error"]),
#         (["S-MHA Error", "E-MHA Error"], ["S-MHA Error", "E-MHA Error"]),
#     ],
# )
# debug to make sure path is right
# def test_load_csv_columns_cols_return_path_right(download_path, source_test_file, return_columns):
#     # ensure if cols_to_return is "All" that all columns are returned
#     download_file_by_url(
#         landmark_uncertainty_url, download_path, "Uncertainty_tuples.zip", "zip"
#     )

#     returned_cols = load_csv_columns(
#         (os.path.join(download_path, source_test_file)),
#         "Testing Fold",
#         np.arange(8),
#         cols_to_return=return_columns[0],
#     )
#     assert list(returned_cols.columns) == return_columns[1]


@pytest.mark.parametrize("source_test_file", ["PHD-Net/4CH/uncertainty_pairs_test_l0"])
@pytest.mark.parametrize(
    "return_columns",
    [
        ("All", EXPECTED_COLS),
        ([], []),
        ("S-MHA Error", ["S-MHA Error"]),
        (["S-MHA Error", "E-MHA Error"], ["S-MHA Error", "E-MHA Error"]),
    ],
)
def test_load_csv_columns_cols_return(landmark_uncertainty_dl, source_test_file, return_columns):

    # ensure if cols_to_return is "All" that all columns are returned
    # print("LISTING DIR: ", os.listdir(landmark_uncertainty_dl))
    if not os.path.exists(landmark_uncertainty_dl):
        os.makedirs(landmark_uncertainty_dl)
    filename = "Uncertainty_tuples.zip"
    data_path = os.path.join(landmark_uncertainty_dl, filename)
    if not os.path.exists(data_path):
        download_file_by_url(landmark_uncertainty_url, landmark_uncertainty_dl, filename, "zip")

        LOGGER.info("The file is downloaded and dl to downloaded to:  %s " % str(data_path))
        # LOGGER.info('The files inside that path:  %s ' % [os.path.join(path, name) for path, subdirs, files in os.walk(data_path) for name in files])
        LOGGER.info(
            "one step up files:  %s "
            % [os.path.join(path, name) for path, subdirs, files in os.walk(landmark_uncertainty_dl) for name in files]
        )

    else:
        LOGGER.info("The file already exists: %s " % str(data_path))
        # LOGGER.info('The files inside that path: %s ' % [os.path.join(path, name) for path, subdirs, files in os.walk(data_path) for name in files])
        LOGGER.info(
            "one step up files:  %s "
            % [os.path.join(path, name) for path, subdirs, files in os.walk(landmark_uncertainty_dl) for name in files]
        )

    # download_file_by_url(landmark_uncertainty_url, landmark_uncertainty_dl, "Uncertainty_tuples.zip", "zip")
    returned_cols = load_csv_columns(
        (os.path.join("/home/runner/work/pykale/pykale", landmark_uncertainty_dl, source_test_file)),
        "Testing Fold",
        np.arange(8),
        cols_to_return=return_columns[0],
    )
    assert list(returned_cols.columns) == return_columns[1]


@pytest.mark.parametrize("source_test_file", ["PHD-Net/4CH/uncertainty_pairs_test_l0"])
@pytest.mark.parametrize(
    "return_columns",
    [
        ("All", EXPECTED_COLS),
        ([], []),
        ("S-MHA Error", ["S-MHA Error"]),
        (["S-MHA Error", "E-MHA Error"], ["S-MHA Error", "E-MHA Error"]),
    ],
)
def test_load_csv_columns_cols_return2(landmark_uncertainty_dl, source_test_file, return_columns):

    download_file_by_url(landmark_uncertainty_url, landmark_uncertainty_dl, "Uncertainty_tuples.zip", "zip")

    # download_file_by_url(landmark_uncertainty_url, landmark_uncertainty_dl, "Uncertainty_tuples.zip", "zip")
    returned_cols = load_csv_columns(
        (os.path.join(landmark_uncertainty_dl, source_test_file)),
        "Testing Fold",
        np.arange(8),
        cols_to_return=return_columns[0],
    )
    assert list(returned_cols.columns) == return_columns[1]


# # Ensure getting a single fold works
# @pytest.mark.parametrize("source_test_file", ["PHD-Net/4CH/uncertainty_pairs_test_l0"])
# @pytest.mark.parametrize("folds", [0])
# def test_load_csv_columns_single_fold(landmark_uncertainty_dl, source_test_file, folds):

#     returned_single_fold = load_csv_columns(
#         os.path.join(landmark_uncertainty_dl, source_test_file),
#         "Validation Fold",
#         folds,
#         cols_to_return=["S-MHA Error", "E-MHA Error", "Validation Fold"],
#     )
#     assert list(returned_single_fold["Validation Fold"]).count(folds) == len(
#         list(returned_single_fold["Validation Fold"])
#     )


# # Ensure getting a list of folds only return those folds and
# # Ensure all samples are being returned
# @pytest.mark.parametrize("source_test_file", ["PHD-Net/4CH/uncertainty_pairs_test_l0"])
# @pytest.mark.parametrize("folds", [[0, 1, 2]])
# def test_load_csv_columns_multiple_folds(landmark_uncertainty_dl, source_test_file, folds):
#     returned_list_of_folds = load_csv_columns(
#         os.path.join(landmark_uncertainty_dl, source_test_file),
#         "Validation Fold",
#         folds,
#         cols_to_return=["S-MHA Error", "E-MHA Error", "Validation Fold"],
#     )
#     assert all(elem in folds for elem in list(returned_list_of_folds["Validation Fold"]))

#     assert len(returned_list_of_folds.index) == 159
