import numpy as np
import cv2 as cv
from cv2.typing import MatLike
from typing import Protocol
from enum import Enum
from typing import Union, Type
#from matplotlib import pyplot as plt
import random


Verdict = Enum("Verdict", ["CorrectClassGuess","IncorrectClassGuess","CorrectFilterGuess","IncorrectFilterGuess","isGameOver","CorrectAnswer"])

Image = MatLike

class Filter(Protocol):
    def filter_image(self,image:Image) ->Image:
        ...

class EqualFilter:
    def __eq__(self, other:object):
        return type(self) is type(other)

class BoxBlur(EqualFilter):
    def filter_image(self,image:Image) ->Image:
        box_kernel = np.ones((5, 5), np.float32) / 25
        box_image = cv.filter2D(src=image, ddepth=-1, kernel=box_kernel)
        return box_image
    def __eq__(self, other:object):
        return isinstance(other, BoxBlur)
    
class Emboss_Image(EqualFilter):
    def filter_image(self,image:Image) ->Image:
        emboss_kernel = np.array([
        [-2, -1, 0],
        [-1, 1, 1],
        [0, 1, 2]
        ])
        embossed_image = cv.filter2D(src=image, ddepth=-1, kernel=emboss_kernel)
        return embossed_image

class SharpenImage(EqualFilter):
    def filter_image(self,image:Image) ->Image:
        sharpen_kernel = np.array([
            [0, -1, 0],
            [-1, 8, -1],
            [0, -1, 0]
        ])

        sharpened_img = cv.filter2D(src = image, ddepth=-1, kernel=sharpen_kernel)
        return sharpened_img
    
class Sobel_X(EqualFilter):
    def filter_image(self,image:Image) ->Image:
        sobel = cv.Sobel(src=image, ddepth=cv.CV_64F, dx=1, dy=0, ksize=3)
        magnitude_8bit = cv.convertScaleAbs(sobel)

        return cv.cvtColor(magnitude_8bit, cv.COLOR_GRAY2BGR)

    
class Sobel_Y(EqualFilter):
    def filter_image(self,image:Image) ->Image:
        return cv.Sobel(src=image, ddepth=cv.CV_64F, dx=0, dy=1, ksize=3)
    
    
class Increase_Brightness(EqualFilter):
    def filter_image(self,image:Image) ->Image:
        return cv.convertScaleAbs(image, alpha=1, beta=127)

class Decrease_Brightness(EqualFilter):
    def filter_image(self,image:Image) ->Image:
        return cv.convertScaleAbs(image, alpha=0.5, beta=1)
    
class Increase_Contrast(EqualFilter):
    def filter_image(self,image:Image) -> Image:
        contrast = +50
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        return cv.addWeighted(image, alpha_c, image, 0, gamma_c)

class Decrease_Contrast(EqualFilter):
    def filter_image(self,image:Image) -> Image:
        contrast = -50
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        return cv.addWeighted(image, alpha_c, image, 0, gamma_c)
    
class Threshold_BinaryInverse(EqualFilter):
    def filter_image(self,image:Image) ->Image:
        return cv.threshold(image,127,255,cv.THRESH_BINARY_INV)[1]

class Threshold_ToZero(EqualFilter):
    def filter_image(self,image:Image) ->Image:
        return cv.threshold(image,127,255,cv.THRESH_TOZERO)[1]
    
    
class IncreaseSaturation(EqualFilter):
    def filter_image(self,image:Image) ->Image:
        new_image = cv.cvtColor(image,cv.COLOR_BGR2HSV)
        h, s, v = cv.split(new_image)
        s = np.clip(s * 1.5, 0, 255).astype(np.uint8)
        new_image = cv.merge([h, s, v])
        saturated_img = cv.cvtColor(new_image, cv.COLOR_HSV2BGR)
        return saturated_img

class DecreaseSaturation(EqualFilter):
    def filter_image(self,image:Image) ->Image:
        new_image = cv.cvtColor(image,cv.COLOR_BGR2HSV)
        h, s, v = cv.split(new_image)
        s = np.clip(s * 0.5, 0, 255).astype(np.uint8)
        new_image = cv.merge([h, s, v])
        saturated_img = cv.cvtColor(new_image, cv.COLOR_HSV2BGR)
        return saturated_img

class IncreaseHue(EqualFilter):
    def filter_image(self,image:Image) ->Image:
        new_image = cv.cvtColor(image,cv.COLOR_BGR2HSV)
        h, s, v = cv.split(new_image)
        h = np.clip(h * 1.5, 0, 255).astype(np.uint8)
        new_image = cv.merge([h, s, v])
        hue_img = cv.cvtColor(new_image, cv.COLOR_HSV2BGR)
        return hue_img
    
class DecreaseHue(EqualFilter):
    def filter_image(self,image:Image) ->Image:
        new_image = cv.cvtColor(image,cv.COLOR_BGR2HSV)
        h, s, v = cv.split(new_image)
        h = np.clip(h * 0.5, 0, 255).astype(np.uint8)
        new_image = cv.merge([h, s, v])
        hue_img = cv.cvtColor(new_image, cv.COLOR_HSV2BGR)
        return hue_img

class BilateralFilter(EqualFilter):
    def filter_image(self,image:Image) ->Image:
        return cv.bilateralFilter(image,9,75,75)

class NoiseRemovalGray(EqualFilter):
    def filter_image(self,image:Image) ->Image:
        image=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
        se=cv.getStructuringElement(cv.MORPH_RECT , (8,8))
        bg=cv.morphologyEx(image, cv.MORPH_DILATE, se)
        out_gray=cv.divide(image, bg, scale=255)
        return out_gray
        

class NoiseRemovalBinary(EqualFilter):
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
    BinaryInv = Threshold_BinaryInverse
    ToZero = Threshold_ToZero

class EdgeFilter(Enum):
    EmbossImage = Emboss_Image
    # SobelX = Sobel_X
    # SobelY = Sobel_Y
    SharpenImage = SharpenImage

class BlurFilter(Enum):
    BoxBlur = BoxBlur   
    BilateralFilter = BilateralFilter

class NoiseRemoval(Enum):
    NoiseRemovalBinary = NoiseRemovalBinary
    NoiseRemovalGray = NoiseRemovalGray


FilterClass = Union[
    Type[ColorFilter],
    Type[ContrastFilter],
    Type[BrightnessFilter],
    Type[ThresholdFilter],
    Type[EdgeFilter],
    Type[BlurFilter],
    Type[NoiseRemoval],
]

filter_classes: list[FilterClass] = [
    ColorFilter,
    ContrastFilter,
    BrightnessFilter,
    ThresholdFilter,
    EdgeFilter,
    BlurFilter,
    # NoiseRemoval,
]


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
       

        self._correct_filters:list[Filter] = [] 
        self._correct_filterclasses:list[FilterClass] = []
        
        self._attempt_remaining_guesses = no_of_filters
        self._correct_guesses = 0

        self._guess_filter = False

        self._isRoundOver = False
        self._isGameOver = False

        self._currentImage :MatLike | None = None
        self._filteredImage:MatLike | None = None

        self.generate_random_image()
        self.randfilter_image()
    
    
    def get_incorrectguesses(self):
        return self._attempt_remaining_guesses
    
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
        self._correct_filterclasses = []
        self._correct_filters = []
        self._filteredImage = self._currentImage
        list_filterclass = filter_classes.copy()
        for _ in range(self._no_of_filters):
            random_filterclass = random.choice(list_filterclass)
            self._correct_filterclasses.append(random_filterclass)
            list_filterclass.remove(random_filterclass)
            random_filter = random.choice(list(random_filterclass)).value
            random_filter_instance = random_filter()
            self._correct_filters.append(random_filter_instance)
            self._filteredImage = random_filter_instance.filter_image(self._filteredImage)
    
    def generate_random_image(self):
        self._currentImage = self._images[random.randint(0,len(self._images)-1)]

    def check_roundstate(self):
        if (self._attemptsleft > 0 and self._attempt_remaining_guesses == 0):
            self._attemptsleft -= 1
            self._attempt_remaining_guesses = self._no_of_filters
        if self._attemptsleft == 0:
            self._isRoundOver = True
        if (self.nextRound()):
            self._attemptsleft = self._attempts
            self._current_round += 1
            self._attempt_remaining_guesses = self._no_of_filters
            self.generate_random_image()
            self.randfilter_image()
        elif (self._isRoundOver and (self._current_round + 1 == self._rounds + 1)):
            self._isGameOver = True

    def guess_filterclass(self,guess:FilterClass):
        if(self._isGameOver):
            return Verdict.isGameOver  
        
        verdict = self.check_guess_filterclass(guess)
        
        if verdict == Verdict.CorrectClassGuess:
            self._guess_filter = True
            return verdict
        else:
            self._guess_filter = False
            self._attempt_remaining_guesses -= 1
            self.check_roundstate()
            return verdict
    
    def guess_filter(self,guess:Filter):
        assert self._guess_filter

        verdict = self.check_guess_filter(guess)

        self._attempt_remaining_guesses -= 1
       

        if verdict == Verdict.CorrectFilterGuess:
            self._correct_guesses += 1
            if (self._correct_guesses == self._no_of_filters):
                verdict = Verdict.CorrectAnswer
                self._attemptsleft = 0
            self.check_roundstate()
            return verdict
        
        else:
            self.check_roundstate()
            return verdict


    def check_guess_filterclass(self,guess:FilterClass):
        if guess in self._correct_filterclasses:
            return Verdict.CorrectClassGuess
        else:
            return Verdict.IncorrectClassGuess
    
    def check_guess_filter(self,guess:Filter):
        if guess in self._correct_filters:
            return Verdict.CorrectFilterGuess
        else:
            return Verdict.IncorrectFilterGuess
        
    def check_combined(self, guess_class:FilterClass, guess_filter: Filter):
        v1 = self.check_guess_filterclass(guess_class)
        v2 = self.check_guess_filter(guess_filter)

        if v1 == Verdict.IncorrectClassGuess:
            return v1
        else:
            return v2

"""
image = cv.imread('image1.jpg')
assert image is not None, "file could not be read, check with os.path.exists()" 


# image=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
# se=cv.getStructuringElement(cv.MORPH_RECT , (8,8))
# bg=cv.morphologyEx(image, cv.MORPH_DILATE, se)
# out_gray=cv.divide(image, bg, scale=255)
# out_binary=cv.threshold(out_gray, 0, 255, cv.THRESH_OTSU )[1] 

# cv.imshow('binary', out_binary)  
# cv.imshow('gray', out_gray)  


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
# image = cv.imread('nature.jpg')
# cv.imshow('', Sobel_Y().filter_image(image)) 

# cv.waitKey()