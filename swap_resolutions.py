#!/usr/bin/python3
#Copyright Arthur Moore 2016
#BSD 3 clause license
import re
import os
import shutil
import logging

#logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.DEBUG)
#logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.INFO)

FFXIV_CONFIG_PATH   =
FFXIV_CHR_PATH      = FFXIV_CONFIG_PATH + 'FFXIV_CHR################################/'

re_width=re.compile('ScreenWidth\t(\\d+)')
re_height=re.compile('ScreenHeight\t(\\d+)')

#Returns all the data in a file
def read_file(file_name):
    in_file = open (file_name)
    #Get the file's size
    in_file.seek(0,2)
    file_size = in_file.tell()
    in_file.seek(0)
    #Return the whole file's data
    data = in_file.read(file_size)
    in_file.close() #Not sure if needed
    return data

#Get the dimensions currently used
def get_current_screen_dimesions():
    raw_data = read_file(FFXIV_CONFIG_PATH+'FFXIV.cfg')
    src_width = int(re.search(re_width,raw_data).group(1))
    src_height = int(re.search(re_height,raw_data).group(1))
    return src_width,src_height

#Helper to give the correct format for the addon file
def get_addon_file_name(width,height):
    return 'ADDON ('+str(width)+'x'+str(height)+').DAT'

#Write the new screen size to the config file, making sure to leave everything else untouched
def set_new_screen_size(width,height):
    #Get and rewrite the data
    data = read_file(FFXIV_CONFIG_PATH+'FFXIV.cfg')
    data = re_width.sub('ScreenWidth\t'+str(width),data)
    data = re_height.sub('ScreenHeight\t'+str(height),data)
    #Now write the data to a new file
    out_file = open(FFXIV_CONFIG_PATH+'FFXIV.cfg.new','w')
    out_file.write(data)
    out_file.close()
    #Now preform some file manipulation so there's always a backup
    shutil.move(FFXIV_CONFIG_PATH+'FFXIV.cfg',FFXIV_CONFIG_PATH+'FFXIV.cfg.old')
    shutil.move(FFXIV_CONFIG_PATH+'FFXIV.cfg.new',FFXIV_CONFIG_PATH+'FFXIV.cfg')

#Back up the current hud settings file
def backup_current_settings():
    src_width,src_height = get_current_screen_dimesions()
    print("Current Width and Height:",src_width,"x",src_height)
    logging.debug("Now backing up HUD Settings.")
    addon_file_name = get_addon_file_name(src_width,src_height)
    backup_path = shutil.copy2(FFXIV_CHR_PATH+'ADDON.DAT',FFXIV_CHR_PATH+addon_file_name)
    logging.info("HUD Settings backed up to: " + backup_path)

#Restore a backed up hud settings file
def restore_hud_settings(width,height):
    print("New Width and Height:",width,'x',height)
    addon_file_name = addon_file_name = get_addon_file_name(width,height)
    if os.path.isfile(FFXIV_CHR_PATH+addon_file_name):
        logging.debug("Now restoring HUD Settings.")
        restore_path = shutil.copy2(FFXIV_CHR_PATH+addon_file_name,FFXIV_CHR_PATH+'ADDON.DAT')
        logging.info("HUD Settings Restored to: " + restore_path)
        logging.debug("Now setting new screen size in FFXIV.cfg.")
        set_new_screen_size(width,height)
    else:
        logging.error("HUD Settings file \'"+addon_file_name+"\' not found!")
        logging.error("Leaving HUD Settings unchanged!")



#dir_list = os.listdir(FFXIV_CHR_PATH)
#all_hud_layout_files = [item for item in list if 'ADDON' in dir_list]
#print('Available HUD sizes are:',all_hud_layout_files)

backup_current_settings()
restore_hud_settings(1920,1200)
#restore_hud_settings(3840,2093)
