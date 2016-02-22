#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include "readjoy.h"

static int joy_device = -1;

int openjoy() {
	joy_device = open(DEVJOY, O_RDONLY | O_NONBLOCK);
	return joy_device;
}

int readjoy(struct js_event *jevent) {
	int rec;
	rec = read(joy_device,jevent,sizeof(*jevent));
	if(rec == -1) return 0;
	if(rec == sizeof(*jevent)) return 1;
	return -1;
}

void closejoy() {
	close(joy_device);
}

int main(int argc,char *argv[]) {
	int dev,jcom;
	struct js_event jevent;
	dev = openjoy();
	if(dev <0){
		exit(1);
	}
	while(1) {
		jcom = readjoy(&jevent);
		usleep(1000);
		if(jcom==1) {
			printf("Event: time %8u, value %8hd, type: %3u, axis/button: %u\n",jevent.time, jevent.value, jevent.type, jevent.number);
		}
	}
}

