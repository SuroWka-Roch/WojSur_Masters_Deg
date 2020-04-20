all: gui.py resorce_rc.py
.PHONY: all

gui.py: ./desiner_resorces/counter.ui
	pyuic5 ./desiner_resorces/counter.ui -o gui.py

resorce_rc.py: desiner_resorces/resorce.qrc
	pyrcc5 -o resorce_rc.py desiner_resorces/resorce.qrc