def temperatureCalibration(x,y):
    """
    x: distance
    y: measured temperature
    """
    if(y<28 or y>35):
        return y
    if(x>7):
        return y
    
    p00 = 195.4
    p10 = -12.7
    p01 = -15.83
    p20 = 0.07593
    p11 = 0.8362
    p02 = 0.4491
    p21 = -0.002277
    p12 = -0.01361
    p03 = -0.004415
    val = p00 + p10 * x + p01 * y + p20 * x ** 2 + p11 * x * y + p02 * y ** 2 + p21 * x ** 2 * y+ p12 * x * y ** 2 + p03 * y ** 3

    return val + y