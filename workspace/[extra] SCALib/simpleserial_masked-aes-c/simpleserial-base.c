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
#define MASK_LEN 10
uint8_t global_k[MAX_DATA_LEN] ={0, };
uint8_t global_p[MAX_DATA_LEN] ={0, };
uint8_t global_ret[MAX_DATA_LEN] = {0,};
uint8_t global_masks[MASK_LEN] = {0,};
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

	if (scmd == (uint8_t)'s') {
		/* 마스크 난수 시드 4바이트 (little-endian). 호스트가 준다.
		 *
		 * 타겟이 스스로 엔트로피를 만들 수 없어서 이렇게 한다. STM32F303 에는
		 * TRNG 가 없고, 스택 주소·전역 주소는 매 부팅 같은 값이라 시드가 되지
		 * 못한다(예전 구현이 그렇게 했다가 재플래시할 때마다 같은 마스크 수열이
		 * 처음부터 재생됐다 — 수집한 profiling 31,500장 중 고유 마스크가
		 * 18,520개뿐이었다).
		 *
		 * 호스트는 연결·재플래시할 때마다 새 시드를 보내고 그 값을 h5 에 남긴다.
		 * 재현 가능하면서 재시작마다 달라진다. */
		unsigned seed = 0;
		for (int i = 0; i < 4 && i < len; i++)
			seed |= ((unsigned)buf[i]) << (8 * i);
		srand(seed);

		simpleserial_put((char)scmd, len < 4 ? len : 4, buf);
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
		/* 트리거 구간 = AES 연산만. 마스크 회수 UART 는 트리거 밖에서. */
		trigger_high();
		
		MY_AES_ECB(global_ret, global_k, global_p, global_len);

		trigger_low();

		/* 연구용: 방금 연산의 mask[10] 보관. 호스트는 0x83 'm' 으로 읽는다. */
		MY_AES_get_last_masks(global_masks);

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

	if (scmd == (uint8_t)'m') {
		/* 마지막 암호화에 쓰인 마스크 10바이트.
		 * 공격자가 모르는 값이지만 실험실 h5 수집(i_m)용. */
		simpleserial_put((char)scmd, MASK_LEN, global_masks);
	}
	

	return 0x00;

}
#endif


int main(void)
{
    platform_init();
	init_uart();
	trigger_setup();

	/* masked-aes-c 는 rand() 로 마스크를 뽑는다. 시드는 **호스트가 0x81 's' 로 준다.**
	 *
	 * 여기서 부팅 기본 시드를 넣지만 이 값은 매 부팅 동일하다 — 즉 호스트가 's' 를
	 * 보내지 않으면 리셋할 때마다 완전히 같은 마스크 수열이 재생된다. 그래도 되는
	 * 값이 아니라 "안 주면 이렇게 된다"는 사실을 드러내려고 상수를 쓴다.
	 * 예전 구현은 스택 주소를 섞어 시드를 만들며 "리셋마다 달라진다"고 주석을 달았지만,
	 * 이 MCU 에서 그 주소들은 매 부팅 같은 값이라 사실이 아니었다. */
	srand(1u);

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
