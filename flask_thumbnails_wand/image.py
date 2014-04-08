import wand.image

class Image(wand.image.Image):

    @wand.image.manipulative
    def fit(self, size, bleed=0.0, centering=(0.5, 0.5)):
        """
        Adaptation of ImageOp.fit code from PIL for Wand

        Returns a sized and cropped version of the image, cropped to the
        requested aspect ratio and size.

        This function was contributed by Kevin Cazabon.

        :param size: The requested output size in pixels, given as a
                     (width, height) tuple.
        :param bleed: Remove a border around the outside of the image (from all
                      four edges. The value is a decimal percentage (use 0.01 for
                      one percent). The default value is 0 (no border).
        :param centering: Control the cropping position.  Use (0.5, 0.5) for
                          center cropping (e.g. if cropping the width, take 50% off
                          of the left side, and therefore 50% off the right side).
                          (0.0, 0.0) will crop from the top left corner (i.e. if
                          cropping the width, take all of the crop off of the right
                          side, and if cropping the height, take all of it off the
                          bottom).  (1.0, 0.0) will crop from the bottom left
                          corner, etc. (i.e. if cropping the width, take all of the
                          crop off the left side, and if cropping the height take
                          none from the top, and therefore all off the bottom).
        :return: An image.
        """

        if centering[0] > 1.0 or centering[0] < 0.0: centering = 0.5
        if centering[1] > 1.0 or centering[1] < 0.0: centering = 0.5
        if bleed > 0.49999 or bleed < 0.0: bleed = 0.0

        trimed_pixels = (int(float(bleed) * float(self.size[0]) + 0.5),
                         int(float(bleed) * float(self.size[1]) + 0.5))

        live_area = (0, 0, self.size[0], self.size[1])

        if bleed > 0.5:
            live_area = (trimed_pixels[0], trimed_pixels[1],
                         self.size[0] - trimed_pixels[0] - 1,
                         self.size[1] - trimed_pixels[1] - 1)

        live_size = (live_area[2] - live_area[0], live_area[3] - live_area[1])
        live_area_aspect_ratio = float(live_size[0]) / float(live_size[1])

        aspect_ratio = float(size[0]) / float(size[1])

        if live_area_aspect_ratio >= aspect_ratio:
            crop_width = aspect_ratio * float(live_size[1]) + 0.5
            crop_height = live_size[1]
        else:
            crop_width = live_size[0]
            crop_height = float(live_size[0]) / aspect_ratio + 0.5

        crop_width = int(crop_width)
        crop_height = int(crop_height)

        left_side = live_area[0] + float(live_size[0] - crop_width)  * centering[0]
        top_side = live_area[1] + float(live_size[1] - crop_height) * centering[1]

        left_side = 0 if left_side < 0 else int(left_side)
        top_side = 0 if top_side < 0 else int(top_side)

        self.crop(left_side, top_side, width=crop_width, height=crop_height)
        self.resize(size[0], size[1])
