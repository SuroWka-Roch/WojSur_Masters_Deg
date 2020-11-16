praca.pdf: praca.tex introduction.tex wyniki.tex projekt.tex beginning.tex ending.tex aneks.tex
	pdflatex praca.tex
	pdflatex praca.tex
	mv praca.log praca.out praca.aux praca.toc ./trash
	mv introduction.aux ./trash
	mv ending.aux ./trash
	mv projekt.aux ./trash
	mv wyniki.aux ./trash
	mv beginning.aux ./trash 
	mv aneks.aux ./trash

 .PHONY: clean
 clean:
	mv praca.log praca.out praca.aux praca.toc ./trash
	mv introduction.aux ./trash
	mv ending.aux ./trash
	mv projekt.aux ./trash
	mv wyniki.aux ./trash
	mv beginning.aux ./trash 