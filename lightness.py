# Perceived lightness algorithm by "Myndex"
# https://stackoverflow.com/questions/596216/formula-to-determine-brightness-of-rgb-color

def color_channel(red, green, blue):
    return (red/255, green/255, blue/255)

def sRGB_to_Linear(colorChannel):
    """Returns a linearized value of sRGB color given its 0.0 - 1.0 color channel"""
    if colorChannel <= 0.04045:
        return colorChannel / 12.92
    else:
        return ((colorChannel + 0.055) / 1.055) ** 2.4

def luminance(red, green, blue):
    """ Find Luminance (Y): Y = R_lin * 0.2126 + G_lin * 0.7152 + B_lin * 0.0722 """
    vR, vG, vB = color_channel(red, green, blue)
    Y = (0.2126 * sRGB_to_Linear(vR)
        + 0.7152 * sRGB_to_Linear(vG)
        + 0.0722 * sRGB_to_Linear(vB))
    return Y

def luminance_to_light(luminance):
    if luminance <= 216/24389:
        return luminance * (24389/27)
    else:
        return (luminance ** (1/3)) * 116 - 16

def pixel_to_grayscale(reg, green, blue):
    Y = luminance(reg, green, blue)
    Lstar = luminance_to_light(Y)
    return Lstar
    