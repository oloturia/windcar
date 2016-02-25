#include <stdio.h>
#include <fcntl.h>
#ifndef __JOYSTICK__
#define __JOYSTICK__

#define DEVJOY "/dev/input/js0"

struct js_event {
	unsigned int time;
	short value;
	unsigned char type;
	unsigned char number;
};

#define JS_EVENT_BUTTON 0X01
#define JS_EVENT_AXIS 0x02
#define JS_EVENT_INIT 0x80

#endif
