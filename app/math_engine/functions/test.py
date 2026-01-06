from functions import Logarithmic, Exponential
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

Logarithmic().plot()
img = mpimg.imread("img-1.png")
plt.imshow(img)
plt.axis("off")
plt.show()