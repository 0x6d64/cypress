#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import subprocess
import time


class FsWebcamObject(object):
    def __init__(self, resolution_x=1280, resolution_y=800, input_device=None):
        self.resolutionX = resolution_x
        self.resolutionY = resolution_y
        self.frames_to_skip = 0
        self.frames_to_take = 1
        self.input_device = input_device
        self.delay = 0
        self.busy = False

    def take_image(self, filename, constrain_parameters=True):
        if self.busy:
            return -1
        else:
            self.busy = True
            if constrain_parameters:
                self._constrain_parameters()
            cmd = self._get_command_string(filename)
            p = subprocess.Popen(args=cmd, shell=False)
            fs_exit_code = p.communicate()
            self.busy = False
            return fs_exit_code

    def _get_command_string(self, filename):
        command = ['fswebcam']
        # image capture options
        if self.input_device:
            command.append('-d{!s}'.format(self.input_device))
        command.append('-r {!s}x{!s}'.format(self.resolutionX, self.resolutionY))
        command.append('-F {!s}'.format(self.frames_to_take))
        command.append('-S {!s}'.format(self.frames_to_skip))
        command.append('-D {!s}'.format(self.delay))

        # image output options
        # command.append('--jpeg {}'.format(self.quality))
        command.append('--no-banner')
        command.append(str(filename))
        return command

    def _constrain_parameters(self):
        skip_max = 100
        take_make = 100
        self.frames_to_skip = max(min(self.frames_to_skip, skip_max), 0)
        self.frames_to_take = max(min(self.frames_to_take, take_make), 1)


if __name__ == '__main__':
    webcam = FsWebcamObject(input_device='/dev/video1')
    webcam.resolutionX = 800
    webcam.resolutionY = 600
    webcam.frames_to_take = 2
    webcam.frames_to_skip = 5
    current_dir = os.path.dirname(os.path.realpath(__file__))
    res1 = webcam.take_image(os.path.join(current_dir, 'test.jpg'))
    res2 = webcam.take_image(os.path.join(current_dir, 'test.jpg'))
    print('result 1, 2: {!s}, {!s}'.format(res1, res2))

    # subprocess.call(['ls', '-la'])

    pass
