import cv2
import numpy as np
import math
from os import listdir
from os.path import isfile, join
from fpdf import FPDF
import argparse


def merge_images_to_pdf(path, pdf_path):
    onlyfiles = sorted([f for f in listdir(path ) if f.startswith('Unit_') and f.endswith('.png') and isfile(join(path, f))])    
    batches = np.array_split(onlyfiles, math.ceil(len(onlyfiles)/3))
    
    i = 1
    imginfo = None
    input_pdf_img = []
    for parts in batches:
        arr = [cv2.imread(join(path, a)) for a in parts]
        vis = cv2.vconcat(arr) 
        if i == 1:
            imginfo = vis.shape
        out_path = join(path, f'Page{i:03}.png')
        cv2.imwrite(out_path, vis)
        i += 1
        input_pdf_img.append(out_path)
   
    pdf = FPDF(unit="pt", format=[imginfo[1], imginfo[0]])
    for k in input_pdf_img:
        pdf.add_page()
        pdf.image(k,0,0)
    
    pdf.output(pdf_path, "F")

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input-path", required=True, help="input folder path")
    ap.add_argument("-o", "--output", required=False, help="output pdf file path")
    args = vars(ap.parse_args())
    merge_images_to_pdf(args["input_path"], args["output"])