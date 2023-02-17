import os
from datetime import date
import stanza
import tokenize_uk
from tabulate import tabulate
import pymorphy3
morph = pymorphy3.MorphAnalyzer(lang='uk')


class Analysis:
    present_files = [path.split(".")[0].split("_")
                     for path in os.listdir("../results")
                     if path.split(".")[-1] == "txt" and "test" not in path]

    def __init__(self, name):
        self.name = name
        self.read_files()
        # defined in self.read()
        self.texts_old = None
        self.texts_new = None
        self.posts_old = None
        self.posts_new = None
        self.sentences_old = None
        self.sentences_new = None
        self.words_old = None
        self.words_new = None
        self.tokenize()
        # defined in each rule()
        self.rule_result = {"old": None, "new": None}
        # results of the whole analysis
        self.rules_results = []

    def read_files(self):
        # структура файлів для корпусу:
        # "zelenskyi/old/feb_20.1.txt"
        # тобто папка із прізвищем, у ній дві папки: old і new,
        # і в цих папках файли формату
        # дата.порядковий_номер_допису_за_день.txt
        pass

    def tokenize(self):
        # self.texts_old = усі тексти з теки old
        # self.texts_new = усі тексти з теки new
        # self.posts_old = окремі пости з теки old
        # self.posts_new = окремі пости з теки new
        # self.sentences_old = окремі речення з теки old
        # self.sentences_new = окремі речення з теки new
        # self.words_old = окремі слова з теки old
        # self.words_new = окремі слова з теки new
        pass

    def rule(self, data_period):
        # тіло аналізу

        # наприклад:
        # if *property* in *text*:
        #    self.rule_result[data_period] = "результат аналізу"
        #    return rule_result[data_period]
        return False

    def full_analysis(self):
        if self.name in os.listdir("../data"):
            # тут викликати всі функції типу rule_{name}
            self.rule("old")
            self.rule("new")
            self.rules_results.append(("Rule name", self.rule_result["old"], self.rule_result["new"]))
            return
        raise FileNotFoundError

    def get_file_name(self):
        day = str(date.today()).split("-")[-1]
        number = 1
        if Analysis.present_files:
            numbers = [int(file[-1])
                       if file[0] == self.name and file[1] == str(day)
                       else 0
                       for file in Analysis.present_files]
            number = max(numbers) + 1
        return f"{self.name}_{day}_{number}.txt"

    def show_results(self, headers=("Правило", "2021 рік", "2022 рік"), save=False):
        # options for the tablefmt: "pretty", "fancy_grid"
        if save:
            with open(f"../results/{self.get_file_name()}", "w") as file:
                print(tabulate(self.rules_results, headers=headers, tablefmt="pretty"), file=file)
        print(tabulate(self.rules_results, headers=headers, tablefmt="pretty"))


if __name__ == "__main__":
    politician = Analysis("zelenskyi")
    # politician.rule()
    # print(politician.rule_result)
    # politician.full_analysis()
    # politician.show_results(save=True)
