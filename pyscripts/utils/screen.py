import random
import pyautogui
from PIL import Image, ImageGrab
import cv2
import numpy
import easyocr

from .common import Region
# Region = tuple[int, int, int, int]

def screen_size_calculate() -> tuple[int, int, int]:
    resolution = pyautogui.size()
    img: Image.Image = ImageGrab.grab()
    return resolution.width, resolution.height, int(img.width / resolution.width)


class ScreenText:
    def __init__(self, text: str, region: Region) -> None:
        self.x = region[0]
        self.y = region[1]
        self.width = region[2]
        self.height = region[3]
        self.text = text

    def region(self) -> Region:
        return self.x, self.y, self.width, self.height

    def __str__(self) -> str:
        return '<ScreenText> "{0}": ({1}, {2}, {3}, {4})'.format(self.text, self.x, self.y, self.width, self.height)


class Screen:
    # 屏幕独立像素宽、高，dpr(device pixel ratio)
    width, height, dpr = screen_size_calculate()
    # print('Screen width:{0} height:{1} dpr:{2}'.format(width, height, dpr))

    def capture_image(path: str=None, region: Region=None) -> Image.Image:
        bbox = None if region is None else (region[0], region[1], region[0] + region[2], region[1] + region[3])
        img = ImageGrab.grab(bbox)
        if path:
            img.save(path)
        return img

    def locate_image(region: Region, image: Image.Image, grayscale=True, confidence=0.9) -> Region:
        screen_image = Screen.capture_image(region=region)
        box = pyautogui.locate(image, screen_image, grayscale=grayscale, confidence=confidence)
        if box is not None:
            return (region[0] + box[0], region[1] + box[1], box[2], box[3])
        return None

    def detecte_one(ocr: easyocr.Reader, texts: tuple[str], region: Region, matching='full') -> ScreenText:
        result = Screen.readtext(ocr, region)
        for d in result:
            print('\t\tOCR [{0}]'.format(d[1]))
            ocr_text: str = d[1].strip()
            for text in texts:
                if ((matching == 'startswith' and ocr_text.startswith(text)) or
                    (matching == 'endswith' and ocr_text.endswith(text)) or
                    (matching == 'contains' and ocr_text.find(text) >= 0) or
                    ocr_text == text):
                    left_top = tuple(d[0][0])
                    right_bottom = tuple(d[0][2])
                    text_region = (region[0] + left_top[0],
                                   region[1] + left_top[1],
                                   right_bottom[0] - left_top[0],
                                   right_bottom[1] - left_top[1])
                    return ScreenText(texts[0], text_region)
        return None

    def detecte_all(ocr: easyocr.Reader, region: Region, allowlist=None) -> list[ScreenText]:
        result = Screen.readtext(ocr, region, allowlist=allowlist)
        texts: list[ScreenText] = []
        for d in result:
            print('\t\tOCR [{0}]'.format(d[1]))
            ocr_text = d[1].strip()
            left_top = tuple(d[0][0])
            right_bottom = tuple(d[0][2])
            text_region = (region[0] + left_top[0],
                           region[1] + left_top[1],
                           right_bottom[0] - left_top[0],
                           right_bottom[1] - left_top[1])
            texts.append(ScreenText(ocr_text, text_region))
        return texts

    def click_region(r: Region, randomly: bool=True):
        # randomly 会在区域内随机位置点击，否则点击区域中间
        px = int(r[0] + r[2] / 2) if not randomly else random.randint(r[0], r[0] + r[2])
        py = int(r[1] + r[3] / 2) if not randomly else random.randint(r[1], r[1] + r[3])
        pyautogui.click(px, py)

    def readtext(ocr: easyocr.Reader, region: Region, allowlist=None):
        image = ImageGrab.grab((region[0], region[1], region[0] + region[2], region[1] + region[3]))
        data = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
        return ocr.readtext(data, allowlist=allowlist)
