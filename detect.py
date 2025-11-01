import json
from pathlib import Path
from typing import Dict

import click
import cv2
import numpy as np
from tqdm import tqdm
import argparse


def empty_callback(value):
    pass


def detect(img_path: str) -> Dict[str, int]:

    red = 0;
    yellow = 0;
    green = 0;
    purple = 0;

    while True:

        img1 = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img = cv2.resize(img1, (1200,700), interpolation=cv2.INTER_AREA)
        frame_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        frame_threshold = cv2.inRange(frame_HSV, (20, 240, 100), (25, 255, 255))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        dilated_mask = cv2.dilate(frame_threshold, kernel, iterations=2)
        closing_mask = cv2.morphologyEx(dilated_mask, cv2.MORPH_CLOSE, np.ones((0, 0), np.uint8))
        opening_mask = cv2.morphologyEx(closing_mask, cv2.MORPH_OPEN, np.ones((0, 0), np.uint8))
        contours, _ = cv2.findContours(opening_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 150:
                yellow += 1
            if cv2.contourArea(contour) > 6000:
                yellow = yellow + 5

        frame_threshold = cv2.inRange(frame_HSV, (35, 195, 140), (50, 255, 245))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        dilated_mask = cv2.dilate(frame_threshold, kernel, iterations=2)
        closing_mask = cv2.morphologyEx(dilated_mask, cv2.MORPH_CLOSE, np.ones((0, 0), np.uint8))
        opening_mask = cv2.morphologyEx(closing_mask, cv2.MORPH_OPEN, np.ones((0, 0), np.uint8))
        contours, _ = cv2.findContours(opening_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 140:
                green += 1
            if cv2.contourArea(contour) > 6000:
                green = green + 5

        frame_threshold = cv2.inRange(frame_HSV, (160, 0, 0), (175, 235, 120))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        dilated_mask = cv2.dilate(frame_threshold, kernel, iterations=2)
        closing_mask = cv2.morphologyEx(dilated_mask, cv2.MORPH_CLOSE, np.ones((13, 13), np.uint8))
        opening_mask = cv2.morphologyEx(closing_mask, cv2.MORPH_OPEN, np.ones((0, 0), np.uint8))
        contours, _ = cv2.findContours(opening_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 160:
                purple += 1
            if cv2.contourArea(contour) > 6000:
                purple = purple + 5

        frame_threshold = cv2.inRange(frame_HSV, (175, 175, 110), (180, 225, 215))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        dilated_mask = cv2.dilate(frame_threshold, kernel, iterations=2)
        closing_mask = cv2.morphologyEx(dilated_mask, cv2.MORPH_CLOSE, np.ones((0, 0), np.uint8))
        opening_mask = cv2.morphologyEx(closing_mask, cv2.MORPH_OPEN, np.ones((0, 0), np.uint8))
        contours, _ = cv2.findContours(opening_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 150:
                red += 1
            if cv2.contourArea(contour) > 6000:
                red = red + 5


        #print(red, yellow, green, purple)
        return {'red': red, 'yellow': yellow, 'green': green, 'purple': purple}



@click.command()
@click.option('-p', '--data_path', help='Path to data directory', type=click.Path(exists=True, file_okay=False,
              path_type=Path), required=True)
@click.option('-o', '--output_file_path', help='Path to output file', type=click.Path(dir_okay=False, path_type=Path),
              required=True)
def main(data_path: Path, output_file_path: Path):
    img_list = data_path.glob('*.jpg')

    results = {}

    for img_path in tqdm(sorted(img_list)):
        fruits = detect(str(img_path))
        results[img_path.name] = fruits

    with open(output_file_path, 'w') as ofp:
        json.dump(results, ofp)


if __name__ == '__main__':
    main()
