QT += core gui network sql widgets

CONFIG += c++17
CONFIG += link_pkgconfig

TARGET = NextAI
TEMPLATE = app
VERSION = 1.0.0

# Application settings
APPLICATION_NAME = "NextAI"
CONFIG += warn_on

# Source files
SOURCES += \
    src/main.cpp \
    src/mainwindow.cpp \
    src/aiservice.cpp \
    src/storageservice.cpp \
    src/codeblock.cpp

HEADERS += \
    src/mainwindow.h \
    src/aiservice.h \
    src/storageservice.h \
    src/codeblock.h

# Compiler settings
CONFIG(debug, debug|release) {
    DEFINES += QT_DEBUG_OUTPUT
}

CONFIG(release, debug|release) {
    DEFINES += QT_NO_DEBUG_OUTPUT
}

# Platform specific
unix {
    target.path = /usr/local/bin
    INSTALLS += target
}

windows {
    RESOURCES += assets.qrc
}

macx {
    ICON = assets/nextai.icns
}
