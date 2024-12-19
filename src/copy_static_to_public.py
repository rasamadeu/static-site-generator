import os
import shutil
import pdb


def recursive_copy_directory(origin, destiny):
    for path in os.listdir(origin):
        current_origin = os.path.join(origin, path)
        current_destiny = os.path.join(destiny, path)

        if os.path.isfile(current_origin):
            shutil.copy(current_origin, current_destiny)
            print(f'Copying {current_origin} to {current_destiny}')
        else:
            os.mkdir(current_destiny)
            recursive_copy_directory(current_origin, current_destiny)
        print(f'Finished Copying {current_origin} to {current_destiny}')


def copy_static_to_public():

    if os.path.exists('./public'):
        shutil.rmtree('./public')
    os.mkdir('./public')

    recursive_copy_directory('./static', './public')
