import os
import shutil
from datetime import datetime


# Func to get example and sort folders' paths to folder from user
# Gets text for input and returns folder path and folder name
def get_source_folder(enter_text):
    while True:
        print('')
        # User input path
        folder = input(enter_text).strip()

        # Check if path is real
        if os.path.exists(os.path.abspath(folder)):
            folder_path = os.path.abspath(folder)

            # Check if path is a directory
            if os.path.isdir(folder_path):
                # Check if directory is not empty
                if len(os.listdir(folder_path)) > 0:
                    folder_name = os.path.split(folder_path)[-1]
                    break
        else:
            print('>> This folder seems to be unsuitable, enter another path')

    return folder_path, folder_name


# Func creates destination folder inside the folder given to sort
# Func takes path to folder to sort and returns destination's directory path and name
def create_destination_folder(to_sort_folder_path):
    # Save current path
    previous_path = os.getcwd()
    # Change current working directory to sorting one
    os.chdir(to_sort_folder_path)
    # Generate destination folder's name from current date and time
    destination_dir_name = 'selected ' + str(datetime.now()).split('.')[0].replace(':', '-').replace(' ', '-')
    # Create destination directory
    os.makedirs(destination_dir_name)
    # Get destination directory's absolute path
    destination_path = os.path.abspath(destination_dir_name)
    # Change current working directory back to saved earlier
    os.chdir(previous_path)

    return destination_path, destination_dir_name


# Func lists files in given folder
# Takes path to a folder and returns a list of filenames without extension
def get_images_names_from_folder(folder_path):
    # List files in directory
    images = os.listdir(folder_path)
    # Return updated list of filenames without extensions
    return [image.split('.')[0] for image in images]


# Func compares example and sorted folder
# Takes paths to folders and returns list of intersection and not found files
def get_intersection_list(selected_folder_path, to_select_folder_path):
    # List filenames in both folders
    selected_images_names = get_images_names_from_folder(selected_folder_path)
    to_select_images_names = get_images_names_from_folder(to_select_folder_path)

    # Empty list to save results of comparison
    not_found_names = list()
    selected_names = list()

    for name in selected_images_names:
        # Intersection
        if name in to_select_images_names:
            selected_names.append(name)
        # File from example folder is not found in folder to sort
        else:
            not_found_names.append(name)

    return selected_names, not_found_names


# Func adds extensions to selected files
# Takes path to folder to sort and list of selected filenames
# and returns list of selected files with extension
def add_extension(to_select_folder_path, selected_names):
    # List images from folder to sort
    to_select_images = os.listdir(to_select_folder_path)
    # Empty list to save results
    selected_filenames = list()

    for name in selected_names:
        # Find filename with extension
        for n in to_select_images:
            if n.split('.')[0] == name:
                # Add full filename with extension
                selected_filenames.append(n)
    return selected_filenames


# Func rules the selection process
# Takes example folder's path and folder's to sort path and returns
# the list of selected filenames and not found files' names
def choose_images(selected_folder_path, to_select_folder_path):
    # Get comparison results
    selected_names, not_found_names = get_intersection_list(selected_folder_path, to_select_folder_path)
    # Check if intersection exists
    if len(selected_names) > 0:
        # then return filenames with extensions
        selected_filenames = add_extension(to_select_folder_path, selected_names)
        return selected_filenames, not_found_names
    return selected_names, not_found_names


def main():
    # Texts for user input
    selected_folder_input_text = 'Enter path to the folder with presorted photos: '
    to_select_folder_input_text = 'Enter path to the folder for sorting: '
    # Get path to example folder
    selected_fdr_path, selected_fdr_name = get_source_folder(selected_folder_input_text)
    print(f'>> The folder "{selected_fdr_name}" is found, checked and will be used as an example of sort. Great!')

    # Get path to folder to sort
    while True:
        to_select_fdr_path, to_select_fdr_name = get_source_folder(to_select_folder_input_text)
        if not to_select_fdr_path == selected_fdr_path:
            print(f'>> The folder "{to_select_fdr_name}" is found, checked and will be used as the source for sort. '
                  f'Great!')
            break
        print('>> The folder seems to be the same as an example - give a different one!')

    # Get results of the comparison
    selected_images, not_found_names = choose_images(selected_fdr_path, to_select_fdr_path)

    # Report of unsuccessful comparison
    if len(selected_images) == 0:
        print('>> No photos were selected. Check the similarity of names (not extensions!) and try again!')

    # or Continue the process
    else:
        print(f'>> Selected {len(selected_images)} photos')

        # Create destination folder and save its path and name
        destination_fdr_path, destination_fdr_name = create_destination_folder(to_sort_folder_path=to_select_fdr_path)
        print(f'>> Destination folder "{destination_fdr_name}" was automatically created in "{to_select_fdr_name}" '
              f'folder! Selected images will be placed there.')

        print('')
        scenario_text = 'Do you want to move or copy them into destination folder? m / c: '
        print('')

        # Ask user for scenario
        while True:
            user_choice = input(scenario_text).strip().lower()
            if user_choice in ['m', 'c']:
                break

        # Move chosen files to destination folder
        if user_choice == 'm':
            for filename in selected_images:
                move_source = os.path.join(to_select_fdr_path, filename)
                move_destination = os.path.join(destination_fdr_path, filename)

                shutil.move(move_source, move_destination)
                print(f'>> {filename} moved')

        # Copy chosen files to destination folder
        elif user_choice == 'c':
            for filename in selected_images:
                move_source = os.path.join(to_select_fdr_path, filename)
                move_destination = os.path.join(destination_fdr_path, filename)

                shutil.copy(move_source, move_destination)
                print(f'>> {filename} copied')

        # Report results
        print('')
        print('>> All done!')

    # If exist, give a list of not found images
    if len(not_found_names) > 0:
        print(f'>> Some images in example folder were not found in "{to_select_fdr_name}"')
        print(*not_found_names, sep=', ')

# The end


if __name__ == '__main__':
    main()
