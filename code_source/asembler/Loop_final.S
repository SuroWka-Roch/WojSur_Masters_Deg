.L31:
	eor	r0, r6, #1
	bl	_Z15set_multiplexeri
	ldr	r3, .L34+8
	mov	r0, sp
	movs	r1, #8
	ldr	r9, .L34+20
	ldr	r8, .L34+24
	ldr	r7, [r3]
	bl	_Z15clear_int_tablePii
	mov	r3, #131072
	str	r3, [r9]
	mov	r0, r4
	str	r3, [r8]
	mov	r1, r5
	adr	r3, .L34
	ldrd	r2, [r3]
	bl	__aeabi_dmul
	bl	__aeabi_d2iz
	add	r7, r7, r6, lsl #5
	movs	r1, #0
.L24:
	cmp	r1, r0
	bge	.L28
	movs	r3, #0
.L29:
	mov	r2, #524288
	str	r2, [r8]
	str	r2, [r9]
	ldr	r2, .L34+12         ;r2 = &pin_mask
	ldr	ip, [r2]            ;ip = pin_mask
	ldr	r2, .L34+16         ;r2 = &REG_PIOC_PDSR
	ldr	r10, [r7, r3]       ;r10 = counts_pointer[i]
	ldr	r2, [r2]            ;r2 = REG_PIOC_PDSR
	and	r2, ip, r2          ;r2 = REG_PIOC_PDSR & pin_mask
	ldr	ip, [sp, r3]        ;ip = previousValue[i], r3 = i, sp = previousValue
	lsrs	r2, r2, #1      ;val>>1
	cmp	ip, r2              ;previousValue[i]-val
	itet	gt              ;if
	addgt	fp, r2, #16     ;if previousValue[i]-val > 0 then fp = val + 16
	rsble	ip, ip, r2      ;else previousValue[i] = previousValue[i] - val
	rsbgt	ip, ip, fp      ;if previousValue[i]-val > 0 then previousValue[i] = previousValue[i] - (val + 16)
	add	ip, ip, r10         ;ip =  counts_pointer[i] + ip
	str	ip, [r7, r3]        ;counts_pointer[i] updated
	str	r2, [sp, r3]        ;previous_value[i] updated
	adds	r3, r3, #4      ;i++
	cmp	r3, #32             ;i<8
	bne	.L29                ;loop end
	mov	r3, #524288
	str	r3, [r8]
	adds	r1, r1, #1
	str	r3, [r9]
	b	.L24
.L28:
	adds	r6, r6, #1
	cmp	r6, #2
	bne	.L31