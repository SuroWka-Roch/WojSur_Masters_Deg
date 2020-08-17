praca.pdf: praca.tex
	pdflatex praca.tex
	pdflatex praca.tex
	mv praca.log ./trash
	mv praca.out ./trash
	mv praca.aux ./trash
	mv praca.toc ./trash