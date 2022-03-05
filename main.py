import os
from os.path import exists
import urllib.request
from urllib.parse import quote
import shutil
import hashlib
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication, QFileDialog, QDialog
from hlavni_menu import Ui_MainWindow_hlavni_menu
import playsound
import webbrowser

class hlavni_menu0(QMainWindow, Ui_MainWindow_hlavni_menu):


    def __init__(self, *args, **kwargs):

        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

    
    def vytvoreni_temp_slozky(self):

        cesta_program = os.getcwd()
        cesta_temp_slozka = cesta_program + "\\temp"

        if not exists(cesta_temp_slozka):

            os.mkdir(cesta_temp_slozka)

    def prvni_spusteni(self):

        # vytvoření složky temp ve složce, kde je main.py

        self.vytvoreni_temp_slozky()

        # otevření okna programu

        hlavni_menu1.show()


    
    def reset_tlacitko(self):

        self.plainTextEdit.clear()
        self.comboBox.setCurrentText("Vyberte jazyk")

    
    def zdrojovy_kod(self):

        webbrowser.open("https://github.com/RxiPland/Text-do-hlasu")


    def presunout_do_temp(self):

        #
        # tato funkce stáhne zvuk a přesune ho do složky temp, která je na stejném místě jako main.py
        #

        text_ke_stazeni = str(self.plainTextEdit.toPlainText())
        jazyk_combobox = str(self.comboBox.currentText())

        dostupne_jazyky = {"Česky": "cs", "Anglicky": "en", "Německy": "de", "Francouzsky": "fr", "Rusky": "ru"}

        # zkontroluje, jestli soubor již existuje - pokud ano, nic se stahovat nebude

        cesta_program = os.getcwd()
        cesta_temp_slozka = cesta_program + "\\temp"

        try:

            zprava_uzivatel_hash = hashlib.md5(text_ke_stazeni.encode())
            zprava_uzivatel_hash = str(zprava_uzivatel_hash.hexdigest())

        except:

            zprava_uzivatel_hash = str("zadny_hash")

            pass

        if jazyk_combobox != "Vyberte jazyk":

            if exists(cesta_temp_slozka + "\\" + dostupne_jazyky[jazyk_combobox] + "_" + zprava_uzivatel_hash + ".mp3"):

                return ("1")

        if text_ke_stazeni == "" or text_ke_stazeni == " ":

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Problém")
            msgBox.setText("Pole pro text nemůže být prázdné!")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

            return

        elif jazyk_combobox == "Vyberte jazyk":

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Problém")
            msgBox.setText("Vyberte jazyk hlasu!")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

            return

        else:

            text_ke_stazeni_url = quote(text_ke_stazeni, safe='/:?&')

            jazyk = dostupne_jazyky[jazyk_combobox]

        url_prekladace = "https://translate.google.com/translate_tts?ie=UTF-8&tl=" + jazyk + "&client=tw-ob&q=" + text_ke_stazeni_url

        try:

            response = urllib.request.urlretrieve(url_prekladace)

            cesta = str(response[0])

        except:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Problém")
            msgBox.setText("Nelze se připojit k síti!")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

            return

        
        cesta_mp3 = cesta.replace("//", "/")

        # zkontroluje jestli existuje temp složka

        self.vytvoreni_temp_slozky()


        # přesunutí mp3 souboru do temp složky a pojmenování souboru md5 hashem zprávy, kterou zadal uživatel

        try:

            cesta_program = os.getcwd()
            cesta_temp_slozka = cesta_program + "\\temp"

            zprava_uzivatel_hash = hashlib.md5(text_ke_stazeni.encode())
            zprava_uzivatel_hash = str(zprava_uzivatel_hash.hexdigest())

            if not exists(cesta_temp_slozka + "\\" + dostupne_jazyky[jazyk_combobox] + "_" + zprava_uzivatel_hash + ".mp3"):

                shutil.move(cesta_mp3, cesta_temp_slozka + "\\" + dostupne_jazyky[jazyk_combobox] + "_" + zprava_uzivatel_hash + ".mp3")

        except:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Problém")
            msgBox.setText("Nastala chyba při přesouvání mp3 souboru do temp složky!")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

            return

        return ("1")

    def poslechnout(self):

        # přehraje stežený soubor


        odpoved = str(self.presunout_do_temp())

        if odpoved != "1":

            return

        text_ke_stazeni = str(self.plainTextEdit.toPlainText())
        jazyk_combobox = str(self.comboBox.currentText())

        dostupne_jazyky = {"Česky": "cs", "Anglicky": "en", "Německy": "de", "Francouzsky": "fr", "Rusky": "ru"}

        cesta_program = os.getcwd()
        cesta_temp_slozka = cesta_program + "\\temp"

        zprava_uzivatel_hash = hashlib.md5(text_ke_stazeni.encode())
        zprava_uzivatel_hash = str(zprava_uzivatel_hash.hexdigest())

        cesta_k_mp3 = str(cesta_temp_slozka + "\\" + dostupne_jazyky[jazyk_combobox] + "_" + zprava_uzivatel_hash + ".mp3")

        try:

            playsound.playsound(cesta_k_mp3, True)

        except:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Problém")
            msgBox.setText("Zvuk se nepodařilo přehrát! Možné řešení:\n\n(1) Názvy složek, kde se nachází tento program mají v názvu háčky nebo čárky (přejmenujte složky)\n\nCesta:\n" + cesta_program)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

    def presunout_do_lokace_od_uzivatele(self):

        # přesune stažený soubor do vybraného místa

        odpoved = str(self.presunout_do_temp())

        if odpoved != "1":

            return

        nova_cesta = file_dialog1.vyberLokace()

        if nova_cesta == "":

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Problém")
            msgBox.setText("Cesta nebyla vybrána!")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

            return

        else:

            text_ke_stazeni = str(self.plainTextEdit.toPlainText())
            jazyk_combobox = str(self.comboBox.currentText())

            dostupne_jazyky = {"Česky": "cs", "Anglicky": "en", "Německy": "de", "Francouzsky": "fr", "Rusky": "ru"}

            cesta_program = os.getcwd()
            cesta_temp_slozka = cesta_program + "\\temp"

            zprava_uzivatel_hash = hashlib.md5(text_ke_stazeni.encode())
            zprava_uzivatel_hash = str(zprava_uzivatel_hash.hexdigest())

            cesta_k_souboru = cesta_temp_slozka + "\\" + dostupne_jazyky[jazyk_combobox] + "_" + zprava_uzivatel_hash + ".mp3"

            try:

                shutil.move(cesta_k_souboru, str(nova_cesta + "\\" + dostupne_jazyky[jazyk_combobox] + "_" + zprava_uzivatel_hash + ".mp3"))

                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Question)
                msgBox.setWindowTitle("Oznámení")
                msgBox.setText("Soubor byl úspěšně přesunut")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()

            except:

                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setWindowTitle("Problém")
                msgBox.setText("Soubor se nepodařilo přesunout!")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()


class file_dialog0(QDialog):

    def vyberLokace(self):

        # otevře průzkumník souborů a uživatel vybere cestu, kam bude chtít uložit mp3 soubor

        dlg = QFileDialog.getExistingDirectory(self, 'Vyberte, kam se má mp3 soubor uložit', '', QFileDialog.ShowDirsOnly)

        return str(dlg)

        

if __name__ == "__main__":

    import sys
    app = QApplication(sys.argv)

    hlavni_menu1 = hlavni_menu0()
    file_dialog1 = file_dialog0()

    hlavni_menu1.prvni_spusteni()

    hlavni_menu1.pushButton.clicked.connect(hlavni_menu1.poslechnout)
    hlavni_menu1.pushButton_2.clicked.connect(hlavni_menu1.presunout_do_lokace_od_uzivatele)
    hlavni_menu1.pushButton_3.clicked.connect(hlavni_menu1.reset_tlacitko)
    hlavni_menu1.pushButton_4.clicked.connect(hlavni_menu1.zdrojovy_kod)

    sys.exit(app.exec_())