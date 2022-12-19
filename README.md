<!--
 * @Author: SimonCK666 SimonYang223@163.com
 * @Date: 2022-12-17 11:35:32
 * @LastEditors: SimonCK666 SimonYang223@163.com
 * @LastEditTime: 2022-12-17 12:01:57
 * @FilePath: /Trangular_Depth_Estimation/README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# Trangular_Depth_Estimation
Triangulation to get depth value

## Using opencv & numpy to measure this problem

> Steps from ChatGPT

在 python 中，您可以使用 numpy 和 opencv 库来实现三角化。

首先，您需要获取两个摄像头的内参数矩阵，然后将它们存储在 `numpy` 数组中。内参数矩阵包含了摄像头的焦距和光心位置，这些参数将用于计算图像中物体的深度。

接下来，您需要使用 opencv 库中的 `cv2.stereoCalibrate()` 函数来获取两个摄像头之间的外参数。外参数是一组矩阵，它们描述了两个摄像头之间的位置和方向关系。

最后，您可以使用 `opencv` 库中的 `cv2.triangulatePoints()` 函数来计算图像中物体的三维坐标。这个函数需要输入两个摄像头的内参数矩阵和外参数，以及两个摄像头中的特征点的二维坐标。它将返回一个 numpy 数组，其中包含了图像中物体的三维坐标。

## Opencv Feature Matching Methods

> https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html