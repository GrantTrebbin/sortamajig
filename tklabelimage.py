import tkinter.ttk
from PIL import Image, ImageTk


class TkLabelImage(tkinter.ttk.Label):
    def __init__(self, parent, **kwargs):

        # Initialise the label
        super().__init__(parent, **kwargs)
        self.quality = 'low'
        self.refresh_delay = 1000
        self.lock_aspect_ratio = True

        # Initialise timer for dynamic refresh
        self.refreshTimer = self.after(self.refresh_delay,
                                       self.fill,
                                       1)
        self.after_cancel(self.refreshTimer)

        # A default image of a red square if an image can't be loaded
        self.default = Image.new("RGB", (200, 200), "red")

        # Initialise variables to hold images
        self.image = self.default
        self.tk_image = ImageTk.PhotoImage(self.image)

        # Draw image
        # Note: image will be drawn but not re-sized.  The fill method needs to
        # be called after the label has been drawn.
        self.configure(image=self.tk_image)

    def image_behaviour(self, quality, lock_aspect_ratio, delay=1000):
        self.quality = quality
        self.lock_aspect_ratio = lock_aspect_ratio
        self.refresh_delay = delay

    def load(self, filename):
        # Try to load an image.  If it fails use the default.
        try:
            self.image = Image.open(filename)
        except OSError as e:
            self.image = self.default

        self.fill()

    def fill(self):
        # Based on the quality setting fill_refresh the image.
        if self.quality == 'dynamic':
            # Configure timer for the delayed refresh.
            self.after_cancel(self.refreshTimer)
            self.refreshTimer = self.after(self.refresh_delay,
                                           self.fill_refresh,
                                           1,
                                           True)
            self.fill_refresh(0, False)
        elif self.quality == 'high':
            self.fill_refresh(1, False)
        else:
            self.fill_refresh(0, False)

    def fill_refresh(self, quality, force_refresh):
        # Get label and original image size
        label_width = self.winfo_width()
        label_height = self.winfo_height()
        image_width, image_height = self.image.size

        # Calculate new image size after resizing based on aspect lock
        if self.lock_aspect_ratio:
            width_ratio = image_width / label_width
            height_ratio = image_height / label_height
            resize_ratio = max(width_ratio, height_ratio)

            new_height = int(image_height/resize_ratio)
            new_width = int(image_width/resize_ratio)
        else:
            new_height = label_height
            new_width = label_width

        # Only resize the image on used for the label if its size changes or
        # it's forced
        if ((new_width != self.tk_image.width()) or
                (new_height != self.tk_image.height()) or
                force_refresh):

            # Resize with appropriate quality
            if quality == 1:
                resized_image = self.image.resize((new_width, new_height),
                                                  Image.ANTIALIAS)
            else:
                resized_image = self.image.resize((new_width, new_height))
            self.tk_image = ImageTk.PhotoImage(resized_image)
            self.configure(image=self.tk_image)
