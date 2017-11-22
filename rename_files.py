folder = "/home/nayara/Desktop/TCC/index_image/"

import os # glob is unnecessary

for root, dirs, filenames in os.walk(folder):
    i=0
    for filename in filenames:
        fullpath = os.path.join(root, filename)
        new_file_name = folder + str(i+1) + ".jpg"
        print(new_file_name)
        os.rename(fullpath, new_file_name)
        i+=1
