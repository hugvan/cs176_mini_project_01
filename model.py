import numpy as np
import cv2 as cv
from cv2.typing import MatLike
from typing import Protocol
from enum import Enum
#from matplotlib import pyplot as plt
import random


Verdict = Enum("Verdict", ["CorrectGuess","IncorrectGuess","isGameOver"])

Image = MatLike

class Filter(Protocol):
    def filter_image(self,image:Image) ->Image:
        ...


class BoxBlur:
    def filter_image(self,image:Image) ->Image:
        box_kernel = np.ones((5, 5), np.float32) / 25
        box_image = cv.filter2D(src=image, ddepth=-1, kernel=box_kernel)
        return box_image
    
class Emboss_Image:
    def filter_image(self,image:Image) ->Image:
        emboss_kernel = np.array([
        [-2, -1, 0],
        [-1, 1, 1],
        [0, 1, 2]
        ])
        embossed_image = cv.filter2D(src=image, ddepth=-1, kernel=emboss_kernel)
        return embossed_image

class SharpenImage:
    def filter_image(self,image:Image) ->Image:
        sharpen_kernel = np.array([
            [0, -1, 0],
            [-1, 8, -1],
            [0, -1, 0]
        ])

        sharpened_img = cv.filter2D(src = image, ddepth=-1, kernel=sharpen_kernel)
        return sharpened_img
    
class Sobel_X:
    def filter_image(self,image:Image) ->Image:
        return cv.Sobel(src=image, ddepth=cv.CV_64F, dx=1, dy=0, ksize=3)
    
class Sobel_Y:
    def filter_image(self,image:Image) ->Image:
        return cv.Sobel(src=image, ddepth=cv.CV_64F, dx=0, dy=1, ksize=3)
    
    
class Increase_Brightness:
    def filter_image(self,image:Image) ->Image:
        return cv.convertScaleAbs(image, alpha=1, beta=127)

class Decrease_Brightness:
    def filter_image(self,image:Image) ->Image:
        return cv.convertScaleAbs(image, alpha=0.5, beta=1)
    
class Increase_Contrast:
    def filter_image(self,image:Image) -> Image:
        contrast = +50
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        return cv.addWeighted(image, alpha_c, image, 0, gamma_c)

class Decrease_Contrast:
    def filter_image(self,image:Image) -> Image:
        contrast = -50
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        return cv.addWeighted(image, alpha_c, image, 0, gamma_c)
    
class Threshold_BinaryInverse:
    def filter_image(self,image:Image) ->Image:
        return cv.threshold(image,127,255,cv.THRESH_BINARY_INV)[1]

class Threshold_ToZero:
    def filter_image(self,image:Image) ->Image:
        return cv.threshold(image,127,255,cv.THRESH_TOZERO)[1]
    
    
class IncreaseSaturation:
    def filter_image(self,image:Image) ->Image:
        new_image = cv.cvtColor(image,cv.COLOR_BGR2HSV)
        h, s, v = cv.split(new_image)
        s = np.clip(s * 1.5, 0, 255).astype(np.uint8)
        new_image = cv.merge([h, s, v])
        saturated_img = cv.cvtColor(new_image, cv.COLOR_HSV2BGR)
        return saturated_img

class DecreaseSaturation:
    def filter_image(self,image:Image) ->Image:
        new_image = cv.cvtColor(image,cv.COLOR_BGR2HSV)
        h, s, v = cv.split(new_image)
        s = np.clip(s * 0.5, 0, 255).astype(np.uint8)
        new_image = cv.merge([h, s, v])
        saturated_img = cv.cvtColor(new_image, cv.COLOR_HSV2BGR)
        return saturated_img

class IncreaseHue:
    def filter_image(self,image:Image) ->Image:
        new_image = cv.cvtColor(image,cv.COLOR_BGR2HSV)
        h, s, v = cv.split(new_image)
        h = np.clip(h * 1.5, 0, 255).astype(np.uint8)
        new_image = cv.merge([h, s, v])
        hue_img = cv.cvtColor(new_image, cv.COLOR_HSV2BGR)
        return hue_img
    
class DecreaseHue:
    def filter_image(self,image:Image) ->Image:
        new_image = cv.cvtColor(image,cv.COLOR_BGR2HSV)
        h, s, v = cv.split(new_image)
        h = np.clip(h * 0.5, 0, 255).astype(np.uint8)
        new_image = cv.merge([h, s, v])
        hue_img = cv.cvtColor(new_image, cv.COLOR_HSV2BGR)
        return hue_img

class BilateralFilter:
    def filter_image(self,image:Image) ->Image:
        return cv.bilateralFilter(image,9,75,75)

class NoiseRemovalGray:
    def filter_image(self,image:Image) ->Image:
        image=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
        se=cv.getStructuringElement(cv.MORPH_RECT , (8,8))
        bg=cv.morphologyEx(image, cv.MORPH_DILATE, se)
        out_gray=cv.divide(image, bg, scale=255)
        return out_gray
        

class NoiseRemovalBinary:
    def filter_image(self,image:Image) ->Image:
        image=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
        se=cv.getStructuringElement(cv.MORPH_RECT , (8,8))
        bg=cv.morphologyEx(image, cv.MORPH_DILATE, se)
        out_gray=cv.divide(image, bg, scale=255)
        out_binary=cv.threshold(out_gray, 0, 255, cv.THRESH_OTSU )[1] 
        return out_binary
    
class ColorFilter(Enum):
    IncSaturation = IncreaseSaturation
    DecSaturation = DecreaseSaturation
    IncreaseHue = IncreaseHue
    DecreaseHue = DecreaseHue

class ContrastFilter(Enum):
    IncContrast = Increase_Contrast
    DecContrast = Decrease_Contrast

class BrightnessFilter(Enum):
    IncBrightness = Increase_Brightness
    DecBrightness = Decrease_Brightness

class ThresholdFilter(Enum):
    ThresholdBinaryInv = Threshold_BinaryInverse
    ThresholdToZero = Threshold_ToZero

class EdgeFilter(Enum):
    EmbossImage = Emboss_Image
    SharpenImage = SharpenImage
    # SobelX = Sobel_X
    # SobelY = Sobel_Y

class BlurFilter(Enum):
    BoxBlur = BoxBlur   
    BilateralFilter = BilateralFilter

class NoiseRemoval(Enum):
    NoiseRemovalBinary = NoiseRemovalBinary
    NoiseRemovalGray = NoiseRemovalGray

class Filter_Classes(Enum):
    ColorFilter = ColorFilter
    ContrastFilter = ContrastFilter
    BrightnessFilter = BrightnessFilter
    ThresholdFilter = ThresholdFilter
    EdgeFilter = EdgeFilter
    BlurFilter = BlurFilter
    # NoiseRemoval = NoiseRemoval


class FilterDleGame:
    def __init__(self,rounds:int,attempts:int,no_of_filters:int,images:list[Image]) -> None:
        assert rounds >= 0, "Invalid rounds"
        assert attempts >= 0, "Invalid attempts"
        assert len(images) != 0,"No images"
        assert no_of_filters >= 1, "Invalid number of filters"

        self._rounds = rounds
        self._attempts = attempts
        self._no_of_filters = no_of_filters
        self._images = images

        self._attemptsleft = attempts
        self._current_round = 0
        self._current_correctguesses = 0

        self._correct_filters:list[Filter] = [] 

        self._incorrectguesses:list[Filter] = []
        self._correctguesses:list[Filter] = [] 

        self._isRoundOver = False
        self._isGameOver = False
        self._currentImage :MatLike | None = None
        self._filteredImage:MatLike | None = None

        self.generate_random_image()
        self.randfilter_image()
    
    def get_correctguesses(self):
        return self._correctguesses
    
    def get_incorrectguesses(self):
        return self._incorrectguesses
    
    def get_rounds(self):
        return self._rounds
    
    def get_attempts(self):
        return self._attempts
    
    def get_currentImage(self):
        return self._currentImage
    
    def get_filteredImage(self):
        return self._filteredImage
    
    def nextRound(self):
        return self._isRoundOver and (self._current_round + 1 != self._rounds + 1)
    
    def randfilter_image(self):
        assert self._currentImage is not None
        self._filteredImage = self._currentImage
        list_filterclass = list(Filter_Classes)
        for _ in range(self._no_of_filters):
            random_filterclass = random.choice(list_filterclass)
            list_filterclass.remove(random_filterclass)
            random_filter_enum = random.choice(list(random_filterclass.value))
            random_filter = random_filter_enum.value
            random_filter_instance = random_filter()
            self._correct_filters.append(random_filter_instance)
            self._filteredImage = random_filter_instance.filter_image(self._filteredImage)
    
    def generate_random_image(self):
        self._currentImage = self._images[random.randint(0,len(self._images)-1)]

    def remove_guess(self,guess:Filter):
        if guess in self._incorrectguesses:
            self._incorrectguesses.remove(guess)
        else:
            self._correctguesses.remove(guess)
    
    def make_guess(self,guess:Filter):
        if(self._isGameOver):
            return Verdict.isGameOver
        
        verdict = self._check_guess(guess)
        match verdict:
            case Verdict.CorrectGuess:
                self._incorrectguesses.append(guess)
            case Verdict.IncorrectGuess:
                self._correctguesses.append(guess)


        if len(self._incorrectguesses)+len(self._correctguesses) == self._no_of_filters:
            self._attempts -= 1

        if self._attemptsleft == 0 :
            self._isRoundOver = True

        if (self.nextRound()):
            self._attemptsleft = self._attempts
            self._guessed_filters = []
            self._incorrectguesses = []
            self._correctguesses = []
            self._current_round += 1
            self.generate_random_image()
            self.randfilter_image()

        elif (self._isRoundOver and (self._current_round + 1 == self._rounds + 1)):
            self._isGameOver = True
        

        return verdict

    def _check_guess(self,guess:Filter):
        if guess in self._correct_filters:
            return Verdict.CorrectGuess
        else:
            return Verdict.IncorrectGuess
            


# image = cv.imread('image1.jpg')
# assert image is not None, "file could not be read, check with os.path.exists()" 


# image=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
# se=cv.getStructuringElement(cv.MORPH_RECT , (8,8))
# bg=cv.morphologyEx(image, cv.MORPH_DILATE, se)
# out_gray=cv.divide(image, bg, scale=255)
# out_binary=cv.threshold(out_gray, 0, 255, cv.THRESH_OTSU )[1] 

# cv.imshow('binary', out_binary)  
# cv.imshow('gray', out_gray)  

"""
contrast = 50
f = 131*(contrast + 127)/(127*(131-contrast))
alpha_c = f
gamma_c = 127*(1-f)
 
out = cv.convertScaleAbs(image, alpha=0.5, beta=1)

new_image = cv.cvtColor(image,cv.COLOR_BGR2HSV)
h, s, v = cv.split(new_image)
v = np.clip(v * 2, 0, 255).astype(np.uint8)
new_image = cv.merge([h, s, v])
saturated_img = cv.cvtColor(new_image, cv.COLOR_HSV2BGR)
"""
#new_image = cv.addWeighted(image, alpha_c, image, 0, gamma_c)#cv.convertScaleAbs(image, alpha=0.5, beta=1)




#cv.imshow('Original Image', image)
#cv.imshow('New Image', saturated_img)
"""
 #cv.cvtColor(image,cv.COLOR_BGR2HSV)#cv.convertScaleAbs(image, alpha=2, beta=1)
h, s, v = cv.split(new_image)
s = np.clip(s * 2.0, 0, 255).astype(np.uint8)
new_image = cv.merge([h, s, v])
saturated_img = cv.cvtColor(new_image, cv.COLOR_HSV2BGR)
""" 
# Wait until user press some key
# cv.waitKey()



"""
#fft
f = np.fft.fft2(image)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20*np.log(np.abs(fshift))
 
rows, cols = image.shape
crow, ccol = rows//2, cols//2
fshift[crow-30:crow+31, ccol-30:ccol+31] = 0
f_ishift = np.fft.ifftshift(fshift)
image_back = np.fft.ifft2(f_ishift)
image_back = np.real(image_back)
 

def thresh_binary(image,threshold,max_val):
    return cv.threshold(image,127,255,cv.THRESH_BINARY)

ret,thresh1 = cv.threshold(image,127,255,cv.THRESH_BINARY)
ret,thresh2 = cv.threshold(image,127,255,cv.THRESH_BINARY_INV)
ret,thresh3 = cv.threshold(image,127,255,cv.THRESH_TRUNC)
ret,thresh4 = cv.threshold(image,127,255,cv.THRESH_TOZERO)
ret,thresh5 = cv.threshold(image,127,255,cv.THRESH_TOZERO_INV)


ret,thresh6 = cv.threshold(image,200,255,cv.THRESH_BINARY)
 
titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV',"COMBI"]
images = [image3, thresh1, thresh2, thresh3, thresh4, thresh5,thresh6]

for i in range(7):
    plt.subplot(3,3,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
 
plt.show()
"""