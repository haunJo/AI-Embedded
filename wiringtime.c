#include <wiringPi.h> 
#include <stdio.h> 
#include <stdlib.h>
#include <time.h>



#define PA 2
#define PB 4
#define PC 1 
#define PD 16
#define PE 15 
#define PF 8 
#define PG 9 
#define PDEC 0
#define PDP1 22
#define PDP2 23
#define PDP3 24
#define PDP4 25















static int times[4] = {0,0,0,0};

char nums[10] = {0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82, 0xf8, 0x80, 0x90};

char pins[8] = {PA, PB, PC, PD, PE, PF, PG, PDEC};
char pindps[4] = {PDP1, PDP2, PDP3, PDP4};

void clear_pin()
{
        int i;
        for (i=0;i<8;i++)
                digitalWrite(pins[i], 1);
        for (i=0;i<4;i++)
                digitalWrite(pindps[i], 1);
}

void set_pin (int n)
{
        int i;
        for(i=0; i<8; i++)
                digitalWrite(pins[i], (nums[n] >> i)&0x1);
}

void init_pin()
{
        int i;
        for (i=0;i < 8; i++)
                pinMode(pins[i], OUTPUT);
        for (i=0; i<4; i++)
                pinMode(pindps[i], OUTPUT);
}

void timechecker()
{
	struct tm *t;
	time_t now = time(NULL);
	t = localtime(&now);
	t->tm_hour = t->tm_hour + 8;
	//this Raspberry Pi's timesystem isn't on KOR.
	times[0] = (t->tm_hour) / 10;
	times[1] = (t->tm_hour) % 10;
	times[2] = (t->tm_min) / 10;
	times[3] = (t->tm_min) % 10;

	//printf("%d%d%d%d",times[0],times[1],times[2],times[3]);

}



int main(void)
{

        int i;
        wiringPiSetup();
        init_pin();
        

	while(1){

		timechecker();
		
		for(i = 0; i<4;i++)
		{
			set_pin(times[i]);
			digitalWrite(pindps[i], 1);
			delay(5);
			digitalWrite(pindps[i], 0);
		}
	}

        clear_pin();

        return 0;
}



