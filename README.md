# Master Thesis WS

Mój projekt magisterski, projekt to układ akwizycji i wizualizacji danych dla układu detektora promieniowania x.

## Mikrokontroler

Program znajduje się w folderze controler_side. Jest on pisany na arduino due z detykowaną płytką liczników.

## Program

Program znajduje się w folderze pc_side zawiera:

* gui pyQT
* wizualizacja na żywo matplotlib
* akwizycję danych w wybranych formatach (CSV, JSON)
* Framework komunikacyjny z programem na mikrokontrolerze. (PySerial)

Program sam w sobie dzieli się na główny program *main.py* oraz 2 moduły *gui_module* oraz *backend_module*. 