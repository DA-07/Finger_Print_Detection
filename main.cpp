#include <iostream>
#include <opencv2/opencv.hpp>


using namespace std;
using namespace cv;

int main()
{
  VideoCapture cap(0);//enabling video capture from webcam
  if(!cap.isOpened())
  {
      cout<<" Problem with webcam "<<endl;
      return -1;
  }

  const char* nameOfWindow = "detection of skintone";
  const char* orignal_cap = "Orignal";
  int H_min = 0, H_max = 23, S_min = 51, S_max = 152, V_min = 82, V_max = 255;

  namedWindow("Adjustments",CV_WINDOW_AUTOSIZE);// creating trackbars

  createTrackbar("lowH", "Adjustments", &H_min, 180);// hue= 0---->180
  createTrackbar("highH","Adjustments", &H_max, 180);
  createTrackbar("lowS", "Adjustments", &S_min, 255);// saturation= 0---->255
  createTrackbar("highS","Adjustments", &S_max, 255);
  createTrackbar("lowV", "Adjustments", &V_min, 255);// value= 0---->255
  createTrackbar("highV", "Adjustments", &V_max, 255);

  while (true)
  {    //reading a new cap_image from the webcam and converting to HSV
      Mat cap_image;
      cap >> cap_image;
      Mat hsv,thresholded_img;
      cvtColor(cap_image, hsv, CV_BGR2HSV);
      inRange(hsv, Scalar(H_min, S_min, V_min), Scalar(H_max, S_max, V_max), thresholded_img);
      imshow(nameOfWindow, thresholded_img);
      imshow(orignal_cap,cap_image);

      if (cv::waitKey(30) >= 0)
          break;
  }
  return 0;
}

