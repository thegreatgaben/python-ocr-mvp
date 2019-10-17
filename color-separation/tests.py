from ColorSeparation import ColorSeparationEngine
from modules.color import RGB2CMYK, CMYK2RGB


def edgeDetect1():  # blur, canny edge detection
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.resize(2000, 2000)
    C.blur(6)
    C.edgeDetection(100, 150)
    C.writeOutput('output')


def histBackProj1():  # blur, histogram back projection
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.resize(2000, 2000)
    C.blur(6)
    C.setCache()
    for i in range(3, 20, 2):
        C.histBackProjection(i)
        C.writeOutput('output')
        input('i={}, press any key'.format(i))
        C.restoreFromCache()


def multiOtsuTest1():  # greyscaled multi level otsu
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.resize(2000, 2000)
    C.blur(4)
    C.otsuThreshMultiGrey(3)
    C.writeOutput('output')


def multiOtsuTest2():  # RGB multi level otsu
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.blur(6)
    C.otsuThreshMultiRGB(3)
    C.writeOutput('output')


def colorBalanceTest1(src):  # color balancing
    img = cv2.imread(src)  # 'images/img1.jpg'
    eq = simpleColorBalance(img, 10)
    showRGBHistogram(img)
    showRGBHistogram(eq)
    viewImage(img)
    viewImage(eq)


def colorBalanceTest2():
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.colorBalance()
    C.writeOutput('output')


def multiOtsuTest3():
    C = ColorSeparationEngine()
    C.loadImages('images')
    # C.colorBalance()
    C.blur(4)
    C.otsuThreshMultiRGB(2)
    # C.smartInvert()
    C.writeOutput('output')


def multiOtsuTest4():
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.colorBalance()
    C.blur(4)
    C.otsuThreshMultiRGBv2(2)
    C.smartInvert()
    C.writeOutput('output')


def multiOtsuTest5():
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.colorBalance()
    C.blur(4)
    C.otsuThreshMultiHSV(2)
    C.writeOutput('output2c-4b')


def multiOtsuTest5p5():
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.colorBalance()
    C.otsuThreshMultiHSV(2)
    C.writeOutput('output2c-0b')


def multiOtsuTest6():
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.colorBalance()
    C.otsuThreshMultiHSV(3, False)
    C.writeOutput('output-nt')


def multiOtsuTest7():
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.colorBalance()
    C.blur(20)
    C.otsuThreshMultiHSV(2)
    C.writeOutput('output2c-20b')


def multiOtsuTest8():
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.colorBalance()
    C.blur(20)
    C.otsuThreshMultiRGB(2)
    C.smartInvert()
    C.writeOutput('output2c-20b-nc')


def multiOtsuTest9():
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.colorBalance()
    C.blur(4)
    C.otsuThreshMultiRGB(2)
    C.smartInvert()
    C.writeOutput('output2c-4b-nc')


def multiOtsuTest10():
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.colorBalance()
    C.blur(4)
    C.otsuThreshMultiHSV(2)
    C.smartInvert()
    C.writeOutput('output/output3c-4b-nc')


if __name__ == "__main__":
    for i in range(0, 256, 1):
        rgb = (i, i, i)
        cmyk = RGB2CMYK(rgb)
        newrgb = CMYK2RGB(cmyk)
        print(newrgb)
