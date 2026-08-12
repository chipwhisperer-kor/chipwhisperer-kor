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

/* SimpleSerial 2.1의 249바이트 프레임에는 명령 정보도 들어가므로 사용자 데이터는
 * 245바이트로 제한한다. 아래 전역 버퍼는 0x81 입력, 0x82 연산, 0x83 출력 명령 사이의
 * 상태를 보존한다. 호스트는 'l'에 1바이트 길이를 보내며 그 값은 MAX_DATA_LEN 이하여야
 * 한다. 이 펌웨어는 잘못된 길이를 별도로 검증하지 않는다. */
#define MAX_DATA_LEN 245
uint8_t global_k[MAX_DATA_LEN] ={0, };
uint8_t global_p[MAX_DATA_LEN] ={0, };
uint8_t global_ret[MAX_DATA_LEN] = {0,};
uint8_t global_len = 0;


uint8_t get_key(uint8_t* k, uint8_t len)
{
	return 0x00;
}

/* SimpleSerial 1.1 콜백은 빌드 호환성만 유지한다. 실습의 키·평문·길이 프로토콜은
 * SimpleSerial 2.1의 my_init()에서만 완전하게 구현된다. */
uint8_t get_pt(uint8_t* pt, uint8_t len)
{
 
	simpleserial_put('r', 16, pt);

	return 0x00;
}

uint8_t reset(uint8_t* x, uint8_t len)
{
	return 0x00;
}

#if SS_VER == SS_VER_2_1
/* 0x81 입력 명령: 'k'는 키, 'p'는 평문을 저장하고 같은 바이트를 응답한다. 'l'은
 * 결과 버퍼를 지운 뒤 연산 길이를 저장한다. 반환값 0은 명령 처리 성공을 뜻한다. */
uint8_t my_init(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t *buf)
{
 	if (scmd == (uint8_t)'k') {
		for(int i = 0; i<len; i++)
			global_k[i] = buf[i];
		
		simpleserial_put(scmd, len, global_k);
	
	}

	if (scmd == (uint8_t)'p') {
		for(int i = 0; i<len; i++)
			global_p[i] = buf[i];
		
		simpleserial_put((char)scmd, len, global_p);
	
	}	

	if (scmd == (uint8_t)'l') {
		for(int i = 0; i<MAX_DATA_LEN; i++)
			global_ret[i] = 0;

		global_len = buf[0];
		
		simpleserial_put((char)scmd, 1, &global_len);
		
	}

	return 0x00;

}
/* 0x82 'c' 명령: 트리거가 HIGH인 동안에만 XOR 연산을 수행한다. 따라서 수집된
 * Trace(트레이스)는 UART 응답을 포함하지 않는다. 연산 뒤에는 완료 바이트 0x82를 보낸다. */
uint8_t my_update(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t *buf)
{

	if (scmd == (uint8_t)'c') {
		trigger_high();
		
		MY_OTP(global_ret, global_k, global_p, global_len);

		trigger_low();
				
	}
	simpleserial_put((char)scmd, 1, (uint8_t[]){0x82});	

	return 0x00;

}
/* 0x83 'r' 명령: 직전 연산 결과를 'l'로 지정한 길이만큼 반환한다. 이 함수는 결과를
 * 새로 계산하지 않으므로 호스트는 먼저 0x82 'c'를 완료해야 한다. */
uint8_t my_final(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t *buf)
{

	if (scmd == (uint8_t)'r') {
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

	/* 부팅 문자열을 보내지 않는다. 호스트가 첫 바이트부터 SimpleSerial 프레임으로
	 * 해석하므로 프로토콜 밖의 디버그 출력은 통신을 어긋나게 할 수 있다. */
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
