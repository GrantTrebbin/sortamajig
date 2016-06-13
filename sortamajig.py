import tkinter.ttk
from tklabelimage import TkLabelImage
from sortingmanager import SortingManager
from PIL import Image
import pickle
import random


class MainApplication(tkinter.ttk.Frame):
    def __init__(self, parent):

        # Initialise frame
        tkinter.ttk.Frame.__init__(self, parent)
        self.grid(column=0, row=0, sticky="nsew")
        self.parent = parent
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.parent.title("Sortamajig")
        self.configure(height=400, width=600, cursor='heart')
        self.grid_propagate(False)

        self.leftImageFrame = tkinter.ttk.Frame(self)
        self.leftImageFrame.grid_propagate(False)
        self.leftImageFrame.grid(row=0, column=0, sticky="nwse")

        self.rightImageFrame = tkinter.ttk.Frame(self)
        self.rightImageFrame.grid_propagate(False)
        self.rightImageFrame.grid(row=0, column=1, sticky="nwse")

        self.controlFrame = tkinter.ttk.Frame(self)
        self.controlFrame.grid_propagate(False)
        self.controlFrame.configure(height=180)
        self.controlFrame.grid(row=1, column=0, sticky="nwse", columnspan=2)

        self.columnconfigure(0, pad=0, weight=1)
        self.columnconfigure(1, pad=0, weight=1)
        self.rowconfigure(0, weight=1)

        self.randomButton = tkinter.ttk.Button(self.controlFrame)
        self.randomButton.grid_propagate(False)
        self.randomButton.configure(text="¯\_(ツ)_/¯  Meh!  Either or.", command=self.random_selection)
        self.randomButton.grid(row=0, column=0, pady=3, padx=3, sticky="nsew", columnspan=2)

        self.statusLabel = tkinter.ttk.Label(self.controlFrame)
        self.statusLabel.grid_propagate(False)
        self.statusLabel.configure(text="Progress", anchor="center")
        self.statusLabel.grid(row=1, column=0, pady=3, padx=3, sticky="nsew", columnspan=2)

        self.saveButton = tkinter.ttk.Button(self.controlFrame)
        self.saveButton.grid_propagate(False)
        self.saveButton.configure(text="Save sorting state", command=self.save)
        self.saveButton.grid(row=2, column=0, pady=3, padx=3, sticky="nsew", columnspan=2)

        self.undoButton = tkinter.ttk.Button(self.controlFrame)
        self.undoButton.grid_propagate(False)
        self.undoButton.configure(text="Undo", command=self.undo)
        self.undoButton.grid(row=3, column=0, pady=3, padx=3, sticky="nsew")

        self.redoButton = tkinter.ttk.Button(self.controlFrame)
        self.redoButton.grid_propagate(False)
        self.redoButton.configure(text="Redo", command=self.redo)
        self.redoButton.grid(row=3, column=1, pady=3, padx=3, sticky="nsew")

        self.generateMontageButton = tkinter.ttk.Button(self.controlFrame)
        self.generateMontageButton.grid_propagate(False)
        self.generateMontageButton.configure(text="Generate Output", state=tkinter.DISABLED, command=self.montage)
        self.generateMontageButton.grid(row=4, column=0, pady=3, padx=3, sticky="nsew", columnspan=2)

        self.controlFrame.columnconfigure(0, pad=0, weight=1)
        self.controlFrame.columnconfigure(1, pad=0, weight=1)
        self.controlFrame.rowconfigure(0, weight=1)
        self.controlFrame.rowconfigure(1, weight=1)
        self.controlFrame.rowconfigure(2, weight=1)
        self.controlFrame.rowconfigure(3, weight=1)
        self.controlFrame.rowconfigure(4, weight=1)

        self.label1 = TkLabelImage(self.leftImageFrame)
        self.label1.image_behaviour('dynamic', True, 500)
        self.label1.grid_propagate(False)
        self.label1.grid(row=0, column=0, sticky="nwse")
        self.leftImageFrame.columnconfigure(0, pad=0, weight=1)
        self.leftImageFrame.rowconfigure(0, pad=0, weight=1)
        self.label1.configure(text="Frame1", anchor="center")

        self.label2 = TkLabelImage(self.rightImageFrame)
        self.label2.image_behaviour('dynamic', True, 500)
        self.label2.grid_propagate(False)
        self.label2.grid(row=0, column=0, sticky="nwse")
        self.rightImageFrame.columnconfigure(0, pad=0, weight=1)
        self.rightImageFrame.rowconfigure(0, pad=0, weight=1)
        self.label2.configure(text="Frame2", anchor="center")

        self.commandList = []
        self.parent.bind("<Configure>", self.resize)
        self.label1.bind("<Button-1>", self.label1click)
        self.label2.bind("<Button-1>", self.label2click)

        self.sortableDeque = pickle.load(open("sortable.srt", "rb"))
        self.sm = SortingManager(self.sortableDeque)
        self.load_images()

        self.directoryName = "images/"

    def random_selection(self):
        true_or_false = random.choice([True, False])
        if true_or_false is True:
            self.label1click(None)
        else:
            self.label2click(None)

    def label1click(self, event):
        self.sm.select(0)
        self.load_images()

    def label2click(self, event):
        self.sm.select(1)
        self.load_images()

    def load_images(self):
        images = self.sm.options
        if images is None:
            images = ["sorted.png", "sorted.png"]

        self.label1.load(images[0])
        self.label2.load(images[1])
        progress = self.sm.progress
        progress_string = ''.join(['Sorting Progress: ', str(progress[1] - progress[0]), ' out of ', str(progress[1])])
        self.statusLabel.configure(text=''.join([progress_string]))
        if self.sm.is_sorted():
            self.generateMontageButton.configure(state=tkinter.NORMAL)
        else:
            self.generateMontageButton.configure(state=tkinter.DISABLED)

    def undo(self):
        self.sm.undo()
        self.load_images()

    def redo(self):
        self.sm.redo()
        self.load_images()

    def save(self):
        pickle.dump(self.sortableDeque, open("sortable.srt", "wb"))
        print("saved")

    def resize(self, event):
        self.label1.fill()
        self.label2.fill()
        pass

    def determine_layout(self, dimensions, padding, width, maximum_height):
        return_value = []
        number_of_images = len(dimensions)
        start = 0
        aspect_ratio_sum = 0
        number_of_images_in_row = 0

        for imm in range(0, number_of_images):
            aspect = dimensions[imm][0] / dimensions[imm][1]
            aspect_ratio_sum += aspect
            number_of_images_in_row += 1
            height = (width - padding * (number_of_images_in_row + 1)) / aspect_ratio_sum
            if height < maximum_height:
                return_value.append([start, imm, height])
                start = imm + 1
                aspect_ratio_sum = 0
                number_of_images_in_row = 0
        if number_of_images_in_row is not 0:
            return_value.append([start, number_of_images - 1, maximum_height])
        return return_value

    def montage(self):
        padding = 30
        canvas_size = [1920, 1080]
        canvas = Image.new("RGB", (1920, 1080), "white")
        dimensions = []

        image_file_names = self.sm.sorting_state[1]

        with open('results.txt', 'w') as result_file:
            for image_file in image_file_names:
                result_file.write(''.join([image_file, '\n']))

        for image_file in image_file_names:
            with Image.open(image_file) as im:
                dimensions.append(im.size)

        total_height = 0
        row_height = 0
        while total_height < canvas_size[1]:
            row_height += 1
            layout = self.determine_layout(dimensions, padding, canvas_size[0], row_height)

            total_height = padding
            for row in layout:
                height = int(row[2])
                if height is 0:
                    height = 1
                total_height += padding + height

        final_row_height = (row_height-1)

        layout = self.determine_layout(dimensions, padding, canvas_size[0], final_row_height)

        vertical_position = padding
        for row in layout:
            horizontal_position = padding
            height = int(row[2])
            if height is 0:
                height = 1

            for image_index in range(row[0], row[1]+1):
                width = int(height * dimensions[image_index][0] / dimensions[image_index][1])
                if width is 0:
                    width = 1
                print(image_file_names[image_index])
                print(width, height)
                image = Image.open(image_file_names[image_index])
                image = image.resize((width, height), Image.ANTIALIAS)
                canvas.paste(image, (horizontal_position, vertical_position))

                horizontal_position += width + padding

            vertical_position += height + padding
        canvas.save("test.png")


# Manage closing the program cleanly
def close_program(root_window, frame):
    print("program finished")

    # Destroy needs to be explicitly called
    root_window.destroy()

if __name__ == "__main__":
    root = tkinter.Tk()
    main_frame = MainApplication(root)
    root.protocol("WM_DELETE_WINDOW", lambda: close_program(root, main_frame))
    root.mainloop()
