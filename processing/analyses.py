import os
from collections import Counter
from datetime import date
import stanza
# stanza.download('uk')  # завантажте українську модель один раз
from tabulate import tabulate
import re
from tqdm import tqdm

nlp = stanza.Pipeline("uk")


class Analysis:
    present_files = [path.split(".")[0].split("_")
                     for path in os.listdir("../results")
                     if path.split(".")[-1] == "txt" and "test" not in path]

    def __init__(self, name, data_directory='../data/'):
        self.name = name
        self.data_directory = data_directory
        self.dir_old = self.data_directory + self.name + '/old/'
        self.list_dir_old = [file for file in os.listdir(self.dir_old) if file.endswith("txt")]
        self.dir_new = self.data_directory + self.name + '/new/'
        self.list_dir_new = [file for file in os.listdir(self.dir_new) if file.endswith("txt")]
        # defined in self.read_files()
        self.texts_old = ''
        self.texts_new = ''
        self.posts_old = []
        self.posts_new = []
        self.read_files()
        # defined in self.tokenize()
        self.sentences_old = []
        self.sentences_new = []
        # words are already parametrised
        self.words_old = []
        self.words_new = []
        self.tokenize()
        # defined in each rule()
        self.rule_result = {"old": None, "new": None}
        self.rule_freq_result = {"old": None, "new": None}
        self.rule_frequency_list_result = {'old': None, 'new': None}
        # results of the whole analysis
        self.rules_results = []

    def read_files(self):
        # структура файлів для корпусу:
        # "zelenskyi/old/feb_20.1.txt"
        # тобто папка із прізвищем, у ній дві папки: old і new,
        # і в цих папках файли формату
        # дата.порядковий_номер_допису_за_день.txt
        # self.texts_old = усі тексти з теки old
        # self.texts_new = усі тексти з теки new
        # self.posts_old = окремі пости з теки old
        # self.posts_new = окремі пости з теки new
        for filename_old in tqdm(self.list_dir_old, desc="Reading 'old' files"):
            with open(self.dir_old + filename_old, "r", encoding="utf-8", errors="surrogateescape") as f:
                self.posts_old.append("".join(f.readlines()[2:]))
        self.texts_old = "\n".join(self.posts_old)
        for filename_new in tqdm(self.list_dir_new, desc="Reading 'new' files"):
            with open(self.dir_new + filename_new, "r", encoding="utf-8", errors="surrogateescape") as f:
                self.posts_new.append("".join(f.readlines()[2:]))
        self.texts_new = "\n".join(self.posts_new)

    def tokenize(self):
        # self.sentences_old = окремі речення з теки old
        # self.sentences_new = окремі речення з теки new
        # self.words_old = окремі слова з теки old
        # self.words_new = окремі слова з теки new
        for post in tqdm(self.posts_old, desc="Tokenizing 'old' files"):
            self.sentences_old.append([sentence.text for sentence in nlp(post).sentences])
            self.words_old.append([sentence.words for sentence in nlp(post).sentences])
        for post in tqdm(self.posts_new, desc="Tokenizing 'new' files"):
            self.sentences_new.append([sentence.text for sentence in nlp(post).sentences])
            self.words_new.append([sentence.words for sentence in nlp(post).sentences])

    def rule(self, data_period):
        # тіло аналізу
        # результат аналізу має бути в форматі словника:
        # {'назва параметру аналізу':*значення*, тощо}
        # навіть якщо параметр один

        # наприклад:
        # if *property* in *text*:
        #    self.rule_result[data_period] = "результат аналізу"
        #    return rule_result[data_period]
        # return False
        pass

    def rule_freq(self, data_period):
        data_dict = {"old": self.list_dir_old,
                     "new": self.list_dir_new}
        month_days = {("feb"): 28,
                      ("apr", "jun", "sep", "nov"): 30,
                      ("jan", "mar", "may", "jul", "aug", "oct", "dec"): 31}
        files_list = []
        if data_period in ["old", "new"]:
            for file in data_dict[data_period]:
                file_name = file.split(".")
                files_list.append(file_name[0])
        if files_list:
            month = files_list[0].split("_")[0]
            key = [key for key in month_days.keys() if month in key][0]
            self.rule_freq_result[data_period] = round(len(files_list) / month_days[key], 2)
            # self.rule_result_freq[data_period] = round(len(files_list) / len(set(files_list)), 2)
            return self.rule_freq_result[data_period]
        self.rule_freq_result[data_period] = 0.0
        return 0.0

    def rule_frequency_list(self, data_period):
        data_dict_sentences = {"old": self.sentences_old,
                               "new": self.sentences_new}
        data_dict_words = {
            "old": self.words_old,
            "new": self.words_new
        }
        self.rule_frequency_list_result[data_period] = {}
        lemmas = []

        for text in data_dict_words[data_period]:
            for sentence in text:
                for word in sentence:
                    if word.upos in ['PUNKT', 'SYM', 'X']:
                        continue
                    lemmas.append(word.lemma)
                    self.rule_frequency_list_result[data_period][word.lemma] = 0

        lemmas = list(set(lemmas))

        for lemma in lemmas:
            for text in data_dict_sentences[data_period]:
                counts = Counter()
                for sentence in text:
                    counts.update(word.strip('.,?!"\':;').lower() for word in sentence.split())
                self.rule_frequency_list_result[data_period][lemma] += counts[lemma]

        return self.rule_frequency_list_result[data_period]

    def prepare_frequency_list_to_print(self, data_period, words, words_in_line):
        sorted_freq_words = dict(sorted(self.rule_frequency_list_result[data_period].items(), key=lambda x: x[1], reverse=True))
        prepared_values = list(sum(zip(*[iter(list(sorted_freq_words.keys())[:words])] * words_in_line, ['\n'] * 100), tuple()))
        return ' '.join(prepared_values)

    def full_analysis(self, words=10, words_in_line=5):
        if self.name in os.listdir(self.data_directory):
            # приклад виклику правила і записування результатів
            self.rule("old")
            self.rule("new")
            self.rules_results.append(("Rule name", self.rule_result["old"], self.rule_result["new"]))
            # тут викликати всі функції типу rule_{name}
            self.rule_freq("old")
            self.rule_freq("new")
            self.rules_results.append(("Частота дописування",
                                       self.rule_freq_result["old"], self.rule_freq_result["new"]))

            self.rule_frequency_list('old')
            self.rule_frequency_list('new')
            self.rules_results.append(("Частотні слова",
                                       self.prepare_frequency_list_to_print("old", words, words_in_line),
                                       self.prepare_frequency_list_to_print("new", words, words_in_line)))
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
    politician = Analysis("shmygal")
    # politician.rule()
    # print(politician.rule_result)
    politician.full_analysis(70, 7)
    politician.show_results(save=True)
