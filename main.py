import cv2
import os
import os.path
import time
from skimage.metrics import structural_similarity as compare_ssim
import argparse

 
def capture_frame(filePath, output_dir, mirror=False):
 
    cap = cv2.VideoCapture(filePath)
    cv2.namedWindow('Playing..',cv2.WINDOW_AUTOSIZE)
    count = 0
    start = time.time()
    end = start
    lastFrame = None
    while True:
        ret_val, frame = cap.read() 
        if ret_val is None:
            continue

        if frame is None:
            break

        if mirror:
            frame = cv2.flip(frame, 1)           
        
        cv2.imshow('Playing..', frame)
        delta = end - start
       
        if (delta == 0 or delta > 1):
            # Première frame
            if delta == 0:
                cv2.imwrite(os.path.join('.', '%d.png') % count, frame)
                count += 1

            if lastFrame is not None:
                # On transforme en image niveau de gris
                lastGrayFrame = cv2.cvtColor(lastFrame, cv2.COLOR_BGR2GRAY)
                currentGrayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Calcule la similarité des deux frames avec SSIM (Structural similarity index),
                # s'assurer que l'image résulat de différence est retournée
                (score, diff) = compare_ssim(lastGrayFrame, currentGrayFrame, full=True)
                diff = (diff * 255).astype("uint8")
                print("SSIM: {}".format(score))

                # On sauvegarde quand on change de vue.
                if score < 0.99:
                    cv2.imwrite(os.path.join(output_dir, '%d.png') % count, frame)
                    count += 1

            start = end
            lastFrame = frame

        end = time.time()

        if cv2.waitKey(1) == 27:
            break  # esc pour quitter
 
    cv2.destroyAllWindows()
 
def main(args):
    filePath = args["input_file"]    
    output_dir = "."
    if args["output"] is not None:
        output_dir = args["output"]
    
    if os.path.isfile(filePath) and  os.path.isdir(output_dir):
        capture_frame(filePath, output_dir)
    else:
        print("Nop")

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input-file", required=True, help="input video file")
    ap.add_argument("-o", "--output", required=False, help="output images")
    args = vars(ap.parse_args())
    main(args)
