import os
import shutil

def delete_pycache_folders():
    current_dir = os.getcwd()
    
    for root, dirs, files in os.walk(current_dir):
        if '__pycache__' in dirs:
            folder_path = os.path.join(root, '__pycache__')
            shutil.rmtree(folder_path, ignore_errors=True)
    
if __name__ == "__main__":
    delete_pycache_folders()