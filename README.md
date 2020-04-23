# Hand-Owner-Recognition

This algorithm calculates ratios betwwen length of fingers to determine the hand owner. Script uses OpenCV library to binary threshold, then contour is found as shown below. There is implemented method to find the deepest point in convexity defect (point C).\

<img src="https://i.imgur.com/5L8QLnt.jpg" width="300">

It measures the mean square error to determine who is the owner. For each person there were calculated 6 sets of ratio vectors to compare with new image. If the limit of square error is exceeded program output is: None
<img src="https://i.imgur.com/DLqhbSc.jpg" width="300">
