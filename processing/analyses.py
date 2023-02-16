import stanza
import tokenize_uk
from tabulate import tabulate
import pymorphy3
morph = pymorphy3.MorphAnalyzer(lang='uk')


class Analysis:
    def __init__(self, name):
        self.name = name
        self.read_files()
        # defined in self.read()
        self.old_texts = None
        self.new_texts = None
        self.posts_old = None
        self.posts_new = None
        self.sentences_old = None
        self.sentences_new = None
        self.words_old = None
        self.words_new = None
        self.tokenize()
        # defined in each rule()
        self.rule_result = None

    def read_files(self):
        # структура файлів для корпусу:
        # "zelenskyi/old/feb_20.1.txt"
        # тобто папка із прізвищем, у ній дві папки: old і new,
        # і в цих папках файли формату
        # дата.порядковий_номер_допису_за_день.txt
        pass

    def tokenize(self):
        # self.old_texts = усі тексти з теки old
        # self.new_texts = усі тексти з теки new
        # self.posts_old = окремі пости з теки old
        # self.posts_new = окремі пости з теки new
        # self.sentences_old = окремі речення з теки old
        # self.sentences_new = окремі речення з теки new
        # self.words_old = окремі слова з теки old
        # self.words_new = окремі слова з теки new
        pass

    def rule(self):
        # тіло аналізу

        # наприклад:
        # if *property* in *text*:
        #    self.analysis_name_result = "результат аналізу"
        #    return self.analysis_name_result
        self.rule_result = False

    def full_analysis(self):
        # тут викликати всі функції типу rule_{name}
        self.rule()
        pass

    def save_results(self):
        pass


if __name__ == "__main__":
    politician = Analysis("volodymyr zelenskyi")
    # politician.rule()
    # print(politician.rule_result)
    politician.full_analysis()
    # politician.save_results()
