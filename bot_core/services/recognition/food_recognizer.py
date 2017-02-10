import argparse

import numpy as np

import chainer

from chainer import variable
from chainer.dataset import convert

from bot_core.services.recognition import nin


class Recognizer:
    def __init__(self, mean, init_model, label_file):
        self.model = nin.NIN()
        chainer.serializers.load_npz(init_model, self.model)
        labels_file = open(label_file)
        self.labels = list(map(lambda x: x.strip(), labels_file))
        labels_file.close()
        self.mean = np.load(mean).astype('f')

    def recognize(self, _image):
        crop_size = self.model.insize

        try:
            image = np.asarray(_image, dtype=np.float32)
        finally:
            # Only pillow >= 3.0 has 'close' method
            if hasattr(_image, 'close'):
                _image.close()

        image = image.transpose(2, 0, 1)

        _, h, w = image.shape

        top = (h - crop_size) // 2
        left = (w - crop_size) // 2
        bottom = top + crop_size
        right = left + crop_size

        image = image[:, top:bottom, left:right]
        image -= self.mean[:, top:bottom, left:right]
        image *= (1.0 / 255.0)  # Scale to [0, 1]

        x = variable.Variable(convert.concat_examples([image]))
        y = self.model.evaluate(x)
        return self.labels[y[0].data.argmax()]
