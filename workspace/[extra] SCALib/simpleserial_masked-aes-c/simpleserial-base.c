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
#define MASK_LEN 10
uint8_t global_k[MAX_DATA_LEN] ={0, };
uint8_t global_p[MAX_DATA_LEN] ={0, };
uint8_t global_ret[MAX_DATA_LEN] = {0,};
uint8_t global_masks[MASK_LEN] = {0,};
uint8_t global_len = 0;


uint8_t get_key(uint8_t* k, uint8_t len)
{
	return 0x00;
}

/* SimpleSerial 1.1 콜백은 빌드 호환성만 유지한다. 수집기의 키·평문·길이·마스크 시드
 * 프로토콜은 SimpleSerial 2.1의 my_init()에서만 완전하게 구현된다. */
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
/* 0x81 입력 명령: 'k'는 AES 키, 'p'는 평문, 's'는 마스크 난수 시드를 저장한다.
 * 'l'은 결과 버퍼를 지운 뒤 연산 길이를 저장한다. 반환값 0은 명령 처리 성공을 뜻한다. */
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

	if (scmd == (uint8_t)'s') {
		/* 마스크 난수 시드 4바이트 (little-endian). 호스트가 준다.
		 *
		 * 타겟이 스스로 엔트로피를 만들 수 없어서 이렇게 한다. STM32F303 에는
		 * TRNG 가 없고, 스택 주소·전역 주소는 매 부팅 같은 값이라 시드가 되지
		 * 못한다. 주소를 시드로 쓰면 재플래시 뒤 같은 마스크 수열이 처음부터 재생된다.
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
		for(int i = 0; i<MAX_DATA_LEN; i++)
			global_ret[i] = 0;

		global_len = buf[0];
		
		simpleserial_put((char)scmd, 1, &global_len);
		
	}

	return 0x00;

}
/* 0x82 'c' 명령: 트리거가 HIGH인 동안에만 AES 연산을 수행한다. 마스크 회수와 UART
 * 응답은 트리거가 LOW가 된 뒤 처리하므로 수집된 Trace(트레이스)에 섞이지 않는다. */
uint8_t my_update(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t *buf)
{

	if (scmd == (uint8_t)'c') {
		/* 트리거 구간 = AES 연산만. 마스크 회수 UART 는 트리거 밖에서. */
		trigger_high();
		
		MY_AES_ECB(global_ret, global_k, global_p, global_len);

		trigger_low();

		/* 연구자 관점 분석을 위해 방금 연산의 마스크 10바이트를 보관한다. 호스트는
		 * 0x83 'm'으로 읽으며 공격자 관점 분석에는 이 값을 제공하지 않는다. */
		MY_AES_get_last_masks(global_masks);
				
	}
	simpleserial_put((char)scmd, 1, (uint8_t[]){0x82});	

	return 0x00;

}
/* 0x83 출력 명령: 'r'은 직전 AES 결과를 'l'로 지정한 길이만큼 반환하고, 'm'은
 * 연구자 관점 진단에만 쓰는 직전 마스크 10바이트를 반환한다. 두 값 모두 0x82 'c'
 * 완료 뒤에만 유효하며 이 함수는 AES를 다시 실행하지 않는다. */
uint8_t my_final(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t *buf)
{

	if (scmd == (uint8_t)'r') {
		simpleserial_put((char)scmd, global_len, global_ret);
		
	}

	if (scmd == (uint8_t)'m') {
		/* 마지막 암호화에 쓰인 마스크 10바이트.
		 * 공격자가 모르는 값이므로 연구자 관점 HDF5 `mask` 배열 수집에만 쓴다. */
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

	/* masked-aes-c 는 rand() 로 마스크를 뽑는다. 시드는 호스트가 0x81 's'로 준다.
	 *
	 * 여기서 부팅 기본 시드를 넣지만 이 값은 매 부팅 동일하다 — 즉 호스트가 's' 를
	 * 보내지 않으면 리셋할 때마다 완전히 같은 마스크 수열이 재생된다. 그래도 되는
	 * 값이 아니라 "안 주면 이렇게 된다"는 사실을 드러내려고 상수를 쓴다.
	 * 예전 구현은 스택 주소를 섞어 시드를 만들며 "리셋마다 달라진다"고 주석을 달았지만,
	 * 이 MCU 에서 그 주소들은 매 부팅 같은 값이라 사실이 아니었다. */
	srand(1u);

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
