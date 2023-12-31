import math

"""
NOTE
- to reverse an animation, i.e have it move backwards, you must use the opposite function that the forward animation would use
    - easeInSin --reverse--> easeOutSin
    - easeOutQuad --reverse--> easeInQuad
- then you must calculate the inverse of the returned value
    - value = 1 - value
"""

def linear(t):
    return t

def easeInSin(t):
    return -math.cos(t * math.pi / 2) + 1

def easeOutSin(t):
    return math.sin(t * math.pi / 2)

def easeInOutSin(t):
    return -(math.cos(math.pi * t) - 1) / 2

def easeInQuad(t):
    return t * t

def easeOutQuad(t):
    return -t * (t - 2)

def easeInOutQuad(t):
    t *= 2
    if t < 1:
        return t * t / 2
    else:
        t -= 1
        return -(t * (t - 2) - 1) / 2
    
def easeInCubic(t):
    return t * t * t

def easeOutCubic(t):
    t -= 1
    return t * t * t + 1

def easeInOutCubic(t):
    t *= 2
    if t < 1:
        return t * t * t / 2
    else:
        t -= 2
        return (t * t * t + 2) / 2
    
def easeInQuart(t):
    return t * t * t * t

def easeOutQuart(t):
    t -= 1
    return -(t * t * t * t - 1)

def easeInOutQuart(t):
    t *= 2
    if t < 1:
        return t * t * t * t / 2
    else:
        t -= 2
        return -(t * t * t * t - 2) / 2
    
def easeInQuint(t):
    return t * t * t * t * t

def easeOutQuint(t):
    t -= 1
    return (t * t * t * t * t + 1)

def easeInOutQuint(t):
    t *= 2
    if t < 1:
        return t * t * t * t * t / 2
    else:
        t -= 2
        return (t * t * t * t * t + 2) / 2
    
def easeInExpo(t):
    return math.pow(2, 10 * (t - 1))

def easeOutExpo(t):
    return -math.pow(2, -10 * t) + 1

def easeInOutExpo(t):
    if t == 0:
        return 0
    elif t == 1:
        return 1
    elif t < 0.5:
        return math.pow(2, 20 * t - 10) / 2
    else:
        return (2 - math.pow(2, -20 * t + 10)) / 2
    
def easeInCirc(t):
    return 1 - math.sqrt(1 - t * t)

def easeOutCirc(t):
    t -= 1
    return math.sqrt(1 - t * t)

def easeInOutCirc(t):
    t *= 2
    if t < 1:
        return -(math.sqrt(1 - t * t) - 1) / 2
    else:
        t -= 2
        return (math.sqrt(1 - t * t) + 1) / 2

def easeInBack(t):
    c1 = 1.70158
    c3 = c1 + 1
    return c3 * t * t * t - c1 * t * t

def easeOutBack(t):
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

def easeInOutBack(t):
    c1 = 1.70158
    c2 = c1 * 1.525
    if t < 0.5:
        return (pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2
    else:
        return (pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2

def easeInElastic(t):
    c4 = (2 * math.pi) / 3
    if t == 0:
        return 0
    elif t == 1:
        return 1
    else:
        return -math.pow(2, 10 * t - 10) * math.sin((t * 10 - 10.75) * c4)

def easeOutElastic(t):
    c4 = (2 * math.pi) / 3

    if t == 0:
        return 0
    elif t == 1:
        return 1
    else:
        return math.pow(2, -10 * t) * math.sin((t * 10 - 0.75) * c4) + 1
    
def easeInOutElastic(t):
    c5 = (2 * math.pi) / 4.5
    if t == 0:
        return 0
    elif t == 1:
        return 1
    elif t < 0.5:
        return -(math.pow(2, 20 * t - 10) * math.sin((20 * t - 11.125) * c5)) / 2
    else:
        return (math.pow(2, -20 * t + 10) * math.sin((20 * t - 11.125) * c5)) / 2 + 1
    
def easeInBounce(t):
    return 1 - easeOutBounce(1 - t)

def easeOutBounce(t):
    n1 = 7.5625
    d1 = 2.75

    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375

def easeInOutBounce(t):
    if t < 0.5:
        return (1 - easeOutBounce(1 - 2 * t)) / 2
    else:
        return (1 + easeOutBounce(2 * t - 1)) / 2