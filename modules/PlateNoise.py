# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *
from modules import Gaussian
from modules import Threshold


def apply(img):
    """
    Apply a truncate-to-zero threshold
    :param img: input image 
    """
    # apply a threshold before
    pre = Threshold.apply(np.uint8(img), cfg.PLATE_THRESH)

    # apply gaussian blur
    gauss = Gaussian.apply(pre)

    # apply a threshold after
    post = Threshold.apply(np.uint8(gauss), cfg.PLATE_OFFSET)

    return post
# end function


def run(prev, cur, plate):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    :param plate: Stage number of plate image
    """
    runtime = []
    util.log("Stage", cur, "Dilation")
    for read in util.get_images(prev):
        # open image
        file = util.stage_image(read, prev)
        img = cv2.imread(file, cv2.CV_8UC1)

        # get result
        out, time = util.execute_module(apply, img)
        runtime.append(time)

        # save to file
        write = util.stage_image(read, cur)
        cv2.imwrite(write, out)

        # glass view
        file = util.stage_image(read, plate)
        img = cv2.imread(file, cv2.CV_8UC1)
        img[out < 250] = 0
        write = util.stage_image("." + read, cur)
        cv2.imwrite(write, img)

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
