// ------------------------------------------
//  Author: Prof. Taeweon Suh
//          Computer Science & Engineering
//          College of Informatics, Korea Univ.
//  Date:   March 29, 2020
// ------------------------------------------

#define csd_LED_ADDR 0x41200000
#define csd_SWI_ADDR 0x41210000

.extern csd_main

.global main
main:
	bl csd_main
	ldr r3, =csd_LED_ADDR
	mov r2, #0b00000001
	led_loop:
		mov r1, r0		//main�� duration(r0)�� r1���� ���ش�
		str r2, [r3]	//led�ּҿ� ���� �־��ش� -> led on
		dur_loop:
			subs r1, r1, #1
			blne dur_loop
		cmp r2, #0b10000000	//0������ 7������ ���״��� Ȯ��
		lsl r2, r2, #1		//shift left�ϸ� led�� �Ѱ��� ����
		blne led_loop
	b main