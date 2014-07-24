#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: ./genstrings.sh <project_base_directory> <localization_bundle_path>"
    exit 0
fi


PROJECT_BASE_DIR=$1
LOCALIZATION_BUNDLE_PATH=$2


LOCALIZATION_DIR=$LOCALIZATION_BUNDLE_PATH/en.lproj
LOCALIZATION_FILE=$LOCALIZATION_DIR/Localizable.strings
TMP_LOCALIZATION_DIR=/tmp/en.proj
TMP_LOCALIZATION_FILE=$TMP_LOCALIZATION_DIR/Localizable.strings

rm -rf $TMP_LOCALIZATION_DIR
mkdir $TMP_LOCALIZATION_DIR
echo "Running genstrings"
genstrings_output=$(find $PROJECT_BASE_DIR ! -path "*matlab*" -name "*.m" -print | xargs genstrings -s JTLocalizedString -o $TMP_LOCALIZATION_DIR 2>&1)
echo $genstrings_output | python add_genstrings_comments_to_file.py $TMP_LOCALIZATION_FILE

echo "Fetching strings from .xib and .storyboard files"
python create_localized_strings_from_ib_files.py $PROJECT_BASE_DIR $TMP_LOCALIZATION_FILE


echo "Omitting duplicates..."
python handle_duplicates_in_localization.py $TMP_LOCALIZATION_FILE

if [ -f $LOCALIZATION_FILE ]; then
    echo "Merging old localizable with new one..."
    python merge_strings_files.py $LOCALIZATION_FILE $TMP_LOCALIZATION_FILE
else
    echo "No Localizable yet, moving the created file..."
    mv $TMP_LOCALIZATION_FILE $LOCALIZATION_FILE
fi

# The Server localization is set directly into the localization directory, and the general localization file is handled
# separately, what's left is to take care of the other file created by the script in the temporary directory.

find $TMP_LOCALIZATION_DIR -not -name "Localizable.strings" -and -not -path $TMP_LOCALIZATION_DIR -exec cp "{}" $LOCALIZATION_DIR \;
