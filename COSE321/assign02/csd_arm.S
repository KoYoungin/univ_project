// ------------------------------------------
//  Author: Prof. Taeweon Suh
//          Computer Science & Engineering
//          College of Informatics, Korea Univ.
//  Date:   March 29, 2020
// ------------------------------------------

#define csd_LED_ADDR 0x41200000

.extern csd_main

.global main
main:

	ldr r0, =Input_data			//input�� �ּҸ� r0�� load
	ldr r1, =Output_data		//output�� �ּҸ� r1�� load
	eor r2, r2, r2			//r2�� 0�� �Ҵ�, �ݺ����� ���ڷ� Ȱ��
	firstloop:
		eor r3, r3, r3		//r3�� 0�� �Ҵ�, �ݺ����� ���ڷ� Ȱ��
		mov r4, r0			//�ӽ÷� ����� input�� �ּҸ� r4�� �־��ش�
		add r5, r4, #4		//r5�� r4 ���� ���� �ּ� �Ҵ�(r4 + 4)
		secondloop:
			ldr r6, [r4]	//r6�� r4�� �ּҿ� �ִ� �� ����
			ldr r7, [r5]	//r7�� r5�� �ּҿ� �ִ� �� ����
			cmp r6, r7		//���� �� NVCV update(r6 - r7)
			strge r6, [r5]	//ge(greater or equal signed) �� �ּҸ� �ٲ���
			strge r7, [r4]
			add r4, #4		//���� �ּ� �Ҵ�
			add r5, #4		//���� �ּ� �Ҵ�
			add r3, #1		//�ݺ�Ƚ�� ����
			cmp r3, #31		//NZCV update
			blne secondloop	//���� ������ �ٽ� loop �ݺ�
		add r2, #1			//�ݺ�Ƚ�� ����
		cmp r2, #31			//NZCV update
		blne firstloop		//���� ������ �ٽ� loop ����
	eor r2, r2, r2			//���ĵ� input�� output�� �����ϱ� ���� �ݺ����� ���ڷ� Ȱ��
	save:
		ldr r3, [r0]		//r3�� r0(input)�� ����Ű�� ���� �־���(-16 - +15)
		str r3, [r1], #4	//r1�� r3�� ���� �����ϰ� r1�� �ּҸ� +4����
		add r0, #4			//r0�� �ּҵ� +4
		add r2, #1			//�ݺ�Ƚ�� ����
		cmp r2, #32			//32���ϸ� output�� ��� ���� ���� NZCV ������Ʈ
		blne save			//32�� �ݺ��� ������ ��� ��������
//loop:
	//ldr r3, [r0], #4	//load a word into r3 and update r0 (= r0 + 4)
 	//str r3, [r1], #4	//store the word to memory and update r1 (= r1 + 4)

 	//subs r2, r2, #1
 	//bne loop

 	//ldr r0, =csd_LED_ADDR
 	//mov r1, #0x5
 	//str r1, [r0]

 	bl csd_main

//forever:
	//nop
 	//b forever

.data
.align 4

Input_data:
 	.word 2, 0, -7, -1, 3, 8, -4, 10
 	.word -9, -16, 15, 13, 1, 4, -3, 14
 	.word -8, -10, -15, 6, -13, -5, 9, 12
 	.word -11, -14, -6, 11, 5, 7, -2, -12

Output_data:
	.word 0, 0, 0, 0, 0, 0, 0, 0
 	.word 0, 0, 0, 0, 0, 0, 0, 0
 	.word 0, 0, 0, 0, 0, 0, 0, 0
 	.word 0, 0, 0, 0, 0, 0, 0, 0
 //	.space 16	allocate memory for 16 words