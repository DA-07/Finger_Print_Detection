OPENCV_PATH = C:/openCV-3.1.0/opencv/build
INCLUDEPATH += $$OPENCV_PATH/include
LIBS += -L$$OPENCV_PATH/X64/vc12/lib/
LIBS += -lopencv_world310
TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += main.cpp

