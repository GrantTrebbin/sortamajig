import numpy as np
import scipy.optimize as spo
from PIL import Image


class ImageRowSystem:
    def __init__(self, dims, width, bounds, balance):
        self.balance = balance
        self.dimensions = dims
        self.number_of_images = len(self.dimensions)
        self.initial_estimate = [1] * self.number_of_images
        self.bounds = bounds
        self.constraint_function = self.construct_constraints(self.dimensions,
                                                              width)
        self.constraint = ({'type': 'eq', 'fun': self.constraint_function})
        self.objective_function = self.objective(self.dimensions,
                                                 width,
                                                 self.balance)

    @staticmethod
    def construct_constraints(dims, width):
        widths = dims[:, 0].transpose()

        def f(x):
            total = np.dot(widths, x)
            return total - width
        return f

    @staticmethod
    def objective(dims, width, bal):
        heights = dims[:, 1].transpose()
        widths = dims[:, 0].transpose()
        areas = np.multiply(heights, widths)

        def f(x):
            scaled_widths = np.multiply(widths, x)
            scaled_heights = np.multiply(heights, x)
            width_deviations = np.std(scaled_widths)
            height_deviations = np.std(scaled_heights)

            combined_metric = width_deviations * (1- bal) + height_deviations * bal
            return combined_metric
        return f

    def solve(self):
        return spo.minimize(self.objective_function,
                            self.initial_estimate,
                            method='SLSQP',
                            bounds=self.bounds,
                            constraints=self.constraint)


def generate_image(dimensions, padding, filename):
    a = np.round(dimensions).astype('int')
    a[a == 0] = 1
    number_of_images = a.shape[0]
    total_width = int(padding * (number_of_images + 1) + sum(a[:, 0]))
    canvas_height = int(np.max(a[:, 1]))
    canvas = Image.new('RGB', (total_width, canvas_height), 'white')

    x_pos = padding
    for dim in range(0, number_of_images):
        width = a[dim, 0]
        height = a[dim, 1]
        image_canvas = Image.new('RGB', (width, height), 'black')
        canvas.paste(image_canvas, (x_pos, int((canvas_height-height)/2)))
        x_pos += padding
        x_pos += width

    canvas.save(filename)


W = 500
dimensions = np.matrix([[11, 1920],
                        [1280, 5],
                        [1280, 839],
                        [1280, 1920],
                        [1920, 854],
                        [1080, 1920],
                        [3, 7]])

print("*** Original Dimensions ***")
print(dimensions)

# If width of image greater than W rescale so that width = W
widths = dimensions[:, 0]
adjusted_widths = widths.clip(0, W)
prescale = np.divide(adjusted_widths, widths)
dimensions_prescaled = np.matrix(dimensions).astype('float')
dimensions_prescaled[:, 0] = np.multiply(dimensions[:, 0], prescale)
dimensions_prescaled[:, 1] = np.multiply(dimensions[:, 1], prescale)

print("*** Prescale Values ***")
print(prescale)

print("*** Normalized Dimensions ***")
print(dimensions_prescaled)

test = ImageRowSystem(np.array(dimensions_prescaled), W, [[0, 1]] * 7, 0.5)
x_result = test.solve().x
print("*** Scale Values ***")
print(x_result)

print("*** Total Scale Values ***")
scale_result = np.multiply(x_result, prescale.transpose())
print(scale_result)

print("*** Scaled Dimensions ***")
scaled_dimensions = np.zeros((7, 2))
scaled_dimensions[:, 0] = np.multiply(dimensions[:, 0], scale_result.transpose()).transpose()
scaled_dimensions[:, 1] = np.multiply(dimensions[:, 1], scale_result.transpose()).transpose()
print(scaled_dimensions)

print("*** New Bounds ***")
new_bounds = np.zeros((7, 2))
new_bounds[:, 0] = 0.85 * np.array(x_result)
new_bounds[:, 1] = 1.15 * np.array(x_result)
new_bounds[new_bounds > 1] = 1
print(new_bounds)

print("*** Second Round Scale Values ***")
test2 = ImageRowSystem(np.array(dimensions_prescaled), W, new_bounds, 1.0)
x_result2 = test2.solve().x
print(x_result2)

print("*** Second Round Total Scale Values ***")
scale_result2 = np.multiply(x_result2, prescale.transpose())
print(scale_result2)

print("*** Second Round Scaled Dimensions ***")
scaled_dimensions2 = np.zeros((7, 2))
scaled_dimensions2[:, 0] = np.multiply(dimensions[:, 0], scale_result2.transpose()).transpose()
scaled_dimensions2[:, 1] = np.multiply(dimensions[:, 1], scale_result2.transpose()).transpose()
print(scaled_dimensions2)

generate_image(scaled_dimensions, 3, '1.png')
generate_image(scaled_dimensions2, 3, '2.png')
