#!/usr/bin/python

import gnupg
from pprint import pprint
import tarfile
import os
import shutil
import time

def comprimir(name, path):
	print("Tar project")
	tar = tarfile.open(path+"/"+name+".tar.gz", "w:gz")
	tar.add(path+"/"+name, arcname=name)
	tar.close()

def encrypt(name, path):
	print("Start encryption")
	savefile = path+"/"+name+".tar.gz.asc"
	proj_path = path+"/"+name+".tar.gz"
	project = open(proj_path, "rb")
	encrypted_ascii_data = gpg.encrypt_file(project, "adaude@bmm.com", always_trust=True, output=savefile)
	project.close()
	print("Encyption finished")

def clean_project(name, path):
	print("Start cleaning project folder...")
	print("Entering Approval Letters direcotry")
	path_proj = os.path.join(path, name)
	path_app = os.path.join(path_proj, "Approval Letters")
	os.chdir(path_app)
	filelist = [ f for f in os.listdir(".") if not (f == "scan") ]
	for f in filelist:
		if os.path.isdir(f):
    			shutil.rmtree(f)
		else:
			os.remove(f)

	print("Entering Test Data direcotry")
	path_test = os.path.join(path, name, "Test Data") 
	os.chdir(path_test)
	filelist = [ f for f in os.listdir(".") if not (f == "Checklists") ]
        for f in filelist:
                if os.path.isdir(f):
                        shutil.rmtree(f)
                else:
                        os.remove(f)

	print("Entering Checklists direcotry")
	path_check = os.path.join(path_test, "Checklists")
	os.chdir(path_check)
	for root, dirs, files in os.walk(path_check):
		for file in files:
			if not(file.endswith(".pdf")):
				os.remove(os.path.join(root, file))
				files.remove(file)

	print("Entering Checklists direcotry")
	path_check = os.path.join(path_test, "Checklists")
	os.chdir(path_check)
	for root, dirs, files in os.walk(path_check, topdown=False):
			if not files and not dirs:
				os.rmdir(root)

	print("Cleaning project main folders...")
	os.chdir(path_proj)
        main_folders = find_all(path_proj)
	for folder in main_folders:
		if not ((folder == "Approval Letters") or (folder == "Test Data")):
			shutil.rmtree(os.path.join(path_proj, folder))
					
def delete_tar(name, path):
	print("Deleting tar file...")
	os.chdir(path+"/")
	os.remove(name+".tar.gz")

def find_all(path):
    result = []
    for dirs in next(os.walk(path))[1]:
    	result.append(dirs)
    return result

def move_folders(name, path):
	print("Moving files...")
        path_approval="/root/Desktop/Python/migration/SPANAPRVAL"
        path_poseidon="/root/Desktop/Python/migration/POSEIDON"
	shutil.move(os.path.join(path, name),path_approval)
        shutil.move(os.path.join(path, name)+".tar.gz.asc", path_poseidon)
def main():
	#Import GPG keys
	gpg = gnupg.GPG(gnupghome='/root/Desktop/Python/migration')
	key_data = open('CloseKey.public.asc').read()
	import_result = gpg.import_keys(key_data)

	#Color for final text
	OKGREEN = '\033[92m'
	ENDC = '\033[0m'

	#Project path
	path = "/root/Desktop/Python/migration/SPANPROJ"
	files = find_all(path)
	print(files)

	#Main
	name = raw_input("Enter name of project to encrypt: ")
	start_time = time.time()
	comprimir(name, path)
	encrypt(name, path)
	clean_project(name, path)
	delete_tar(name, path)
	move_folders(name, path)
	print(OKGREEN + "Process finished in: --- %s seconds ---" % (time.time() - start_time) + ENDC)

if __name__ == '__main__':
	main()