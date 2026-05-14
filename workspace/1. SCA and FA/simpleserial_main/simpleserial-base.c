/*
    This file is part of the ChipWhisperer Example Targets
    Copyright (C) 2012-2017 NewAE Technology Inc.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include "hal.h"
#include <stdint.h>
#include <stdlib.h>

#include "simpleserial.h"

#include "my_crypt.h"

// SS_VER_2_1의 최대 패킷 크기는 249 바이트. 패킷에는 데이터 이외에 정보가 같이 붙어 최대 패킷 크기 사용 불가
#define MAX_DATA_LEN 245
uint8_t global_k[MAX_DATA_LEN] ={0, };
uint8_t global_p[MAX_DATA_LEN] ={0, };
uint8_t global_ret[MAX_DATA_LEN] = {0,};
uint8_t global_len = 0;


uint8_t get_key(uint8_t* k, uint8_t len)
{
	// Load key here
	return 0x00;
}

//SS_VER_1_1는 사용을 고려하지 않음
uint8_t get_pt(uint8_t* pt, uint8_t len)
{
 
	simpleserial_put('r', 16, pt);

	return 0x00;
}

uint8_t reset(uint8_t* x, uint8_t len)
{
	// Reset key here if needed
	return 0x00;
}

#if SS_VER == SS_VER_2_1
//SS_VER_2_1 사용이 기본
uint8_t my_init(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t *buf)
{
 	if (scmd == (uint8_t)'k') {
		/**********************************
		* Start user-specific code here. */
	
		for(int i = 0; i<len; i++)
			global_k[i] = buf[i];

		/* End user-specific code here. *
		********************************/
		
		simpleserial_put(scmd, len, global_k);
	
	}

	if (scmd == (uint8_t)'p') {
		/**********************************
		* Start user-specific code here. */
	
		for(int i = 0; i<len; i++)
			global_p[i] = buf[i];

		/* End user-specific code here. *
		********************************/
		
		simpleserial_put((char)scmd, len, global_p);
	
	}	

	if (scmd == (uint8_t)'l') {

		/**********************************
		* Start user-specific code here. */
		
		for(int i = 0; i<MAX_DATA_LEN; i++)
			global_ret[i] = 0;

		global_len = buf[0];

		/* End user-specific code here. *
		********************************/
		
		simpleserial_put((char)scmd, 1, &global_len);
		
	}

	return 0x00;

}
uint8_t my_update(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t *buf)
{

	if (scmd == (uint8_t)'c') {

		/**********************************
		* Start user-specific code here. */
		trigger_high();
		
		MY_OTP(global_ret, global_k, global_p, global_len);

		trigger_low();
		/* End user-specific code here. *
		********************************/
				
	}
	simpleserial_put((char)scmd, 1, (uint8_t[]){0x82});	

	return 0x00;

}
uint8_t my_final(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t *buf)
{

	if (scmd == (uint8_t)'r') {

		/**********************************
		* Start user-specific code here. */

		/* End user-specific code here. *
		********************************/
		
		simpleserial_put((char)scmd, global_len, global_ret);
		
	}
	

	return 0x00;

}
#endif


int main(void)
{
    platform_init();
	init_uart();
	trigger_setup();

 	/* Uncomment this to get a HELLO message for debug */
	/*
	putch('h');
	putch('e');
	putch('l');
	putch('l');
	putch('o');
	putch('\n');
	*/

	simpleserial_init();
#if SS_VER != SS_VER_2_1
	simpleserial_addcmd('p', MAX_DATA_LEN, get_pt);
	simpleserial_addcmd('k', MAX_DATA_LEN, get_key);
	simpleserial_addcmd('x', 0, reset);
#else
	simpleserial_addcmd(0x81, MAX_DATA_LEN, my_init);
    simpleserial_addcmd(0x82, MAX_DATA_LEN, my_update);
	simpleserial_addcmd(0x83, MAX_DATA_LEN, my_final);
#endif
	while(1)
		simpleserial_get();
}
