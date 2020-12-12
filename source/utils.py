import cv2 as cv


def draw_rectangle(image, face):
    (start_x, start_y, end_x, end_y) = face["rect"]
    # Arrange color of the detection rectangle to be drawn over image
    detection_rect_color_rgb = (0, 255, 255)
    # Draw the detection rectangle over image
    cv.rectangle(img=image,
                  pt1=(start_x, start_y),
                  pt2=(end_x, end_y),
                  color=detection_rect_color_rgb,
                  thickness=2)

    # Draw detection probability, if it is present
    '''if (face["recognition_prob"] != []):
        # Create probability text to be drawn over image
        text = "{}: {:.2f}%".format(face["name"], face["recognition_prob"])
        # Arrange location of the probability text to be drawn over image
        y = start_y - 10 if start_y - 10 > 10 else start_y + 10
        # Arrange color of the probability text to be drawn over image
        probability_color_rgb = (0, 255, 255)
        # Draw the probability text over image
        cv.putText(img=image,
                    text=text,
                    org=(start_x, y),
                    fontFace=cv.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.45,
                    color=probability_color_rgb,
                    thickness=1)'''
    return image