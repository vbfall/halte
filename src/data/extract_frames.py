import cv2
import os
import pathlib

# from PIL import Image
#


IMAGES_PATH = pathlib.Path('../../data/raw/images')
CLIPS_PATH = pathlib.Path('../../data/raw/clips')
NUM_FRAMES = 20
DEVELOPMENT = True # if TRUE, will use only one clip and extract/save only 2 frames


def get_file_number(file_path):
    path_string = str(file_path)

def get_highest_current_image_number(images_path):
    previous_image_list = [str(path) for path in list(images_path.glob('*/*'))]
    previous_image_numbers = [int(path.split(os.path.sep)[-1].split('.')[0]) for path in previous_image_list]
    return max(previous_image_numbers)

def take_frames(clip, num_frames=10):
    # Receives a cv2 VideoCapture object and extracts num_frames frames from it
    # regularly spaced and returns them in a list

    frame_list = []

    print('getting clip metadata...')
    clip_size = int(clip.get(cv2.CAP_PROP_FRAME_COUNT))
    sample_rate = int(clip_size / (num_frames+2))

    count = 0
    ret = True

    print('Collecting frames:', end='')
    while(ret):

        ret, frame = clip.read()
        if ret:
            if (count>0) and (count%sample_rate==0):
                print(' {}'.format(count+1), end='')
                frame_list.append(frame)
        if len(frame_list) >= num_frames:
            print('')
            break
        else:
            count += 1

    return frame_list


if __name__ == "__main__":

    highest_image_number = get_highest_current_image_number(IMAGES_PATH)
    print('\nFound previous images numbered up to {}'.format(highest_image_number), end='\n\n')

    clips_list = [str(path) for path in list(CLIPS_PATH.glob('*/*'))]
    # Safety / test
    if DEVELOPMENT:
        clips_list = clips_list[0:1]
        NUM_FRAMES = 2

    for clip_path in clips_list:
        weapon = clip_path.split(os.path.sep)[-2]
        print('Processing file {}'.format(clip_path))
        clip = cv2.VideoCapture(clip_path)
        print('Clip open... ', end='')
        frames = take_frames(clip, NUM_FRAMES)
        #save frames
        for f in frames:
            highest_image_number += 1
            img_path = pathlib.Path('../../data/raw/images/'+weapon+'/'+str(highest_image_number).zfill(12)+'.jpg')
            print('saving image {}'.format(img_path))
            cv2.imwrite(str(img_path), f)
        #close clip
        print('Closing file {}'.format(clip_path), end='\n\n')
        clip.release()

exit()
