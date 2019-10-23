include ./makefile.conf
NAME=WojSurMag
STARTUP_DEFS=-D __ATSAM3X8E__

CMSISPATHFLAG=-I /home/piernik/programing/c/WojSurMagSAM/tools/CMSIS/Include

BINFOLDER=./bin
SRC=./src

LINKERPATH=./src/

LDSCRIPTS=-L. -L$(LINKERPATH) -T multi-ram.ld

#flash
FLASHTOOLPATH=/home/piernik/.arduino15/packages/arduino/tools/bossac/1.6.1-arduino/bossac
FLASHPORT=ttyACM0
FLASHTOOLFLAGS=-i -d --port=$(FLASHPORT) -U false -e -w -v


# Must use -u _printf_float to use floating IO
LFLAGS=$(USE_NANO) $(USE_SEMIHOST) $(LDSCRIPTS) $(GC) -u _printf_float

$(BINFOLDER)/$(NAME)-$(CORE).bin: $(SRC)/$(NAME)-$(CORE).axf
	$(objCP) -O binary $^ $@

$(SRC)/$(NAME)-$(CORE).axf: ./$(NAME).c ./$(STARTUP)
	$(CC) $^ $(CFLAGS) $(LFLAGS) $(CMSISPATHFLAG) -o $@
	
.PHONY: start
start:
	mkdir $(SRC) $(BINFOLDER)

clean: 
	rm -f $(SRC)/$(NAME)*.axf $(NAME)*.map $(BINFOLDER)/$(NAME)*.bin 
	
.PHONY: flash 
flash:
	$(FLASHTOOLPATH) $(FLASHTOOLFLAGS) -b $(BINFOLDER)/*.bin -R 

