import os
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
        self.rule_posts_per_day_result = {"old": None, "new": None}
        self.rule_size_result_sentences = {"old": None, "new": None}
        self.rule_size_result_words = {"old": None, "new": None}
        self.rule_result_links = {"old": None, "new": None}
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
                self.posts_old.append("".join(f.readlines()[2:]).strip())
        self.texts_old = "\n".join(self.posts_old)
        for filename_new in tqdm(self.list_dir_new, desc="Reading 'new' files"):
            with open(self.dir_new + filename_new, "r", encoding="utf-8", errors="surrogateescape") as f:
                self.posts_new.append("".join(f.readlines()[2:]).strip())
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

    def rule_posts_per_day(self, data_period):
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
            self.rule_posts_per_day_result[data_period] = round(len(files_list) / month_days[key], 2)
            # self.rule_posts_per_day_result[data_period] = round(len(files_list) / len(set(files_list)), 2)
            return self.rule_posts_per_day_result[data_period]
        self.rule_posts_per_day_result[data_period] = 0.0
        return 0.0

    def rule_size(self, data_period):
        data_dict = {"old": self.words_old,
                     "new": self.words_new}
        posts_num = len(data_dict[data_period])
        sentences_list = [sentence for post in data_dict[data_period] for sentence in post]
        sentences_num = len(sentences_list)
        words_num = len([word for sentence in sentences_list for word in sentence])
        self.rule_size_result_sentences[data_period] = round(sentences_num / posts_num, 2)
        self.rule_size_result_words[data_period] = round(words_num / posts_num, 2)
        return self.rule_size_result_sentences[data_period], self.rule_size_result_words[data_period]

  def rule_links(self, data_period):
        links = re.findall(r'<link>(https?://\S+)<\/link>', self.texts_old if data_period == "old" else self.texts_new)
        num_links = len(links)
        if num_links == 0:
            self.rule_result_links[data_period] = 0
        else:
            self.rule_result_links[data_period] = num_links
        return self.rule_result_links[data_period]

    def full_analysis(self):
        if self.name in os.listdir(self.data_directory):
            # приклад виклику правила і записування результатів
            self.rule("old")
            self.rule("new")
            self.rules_results.append(("Rule name", self.rule_result["old"], self.rule_result["new"]))
            # тут викликати всі функції типу rule_{name}
            self.rule_posts_per_day("old")
            self.rule_posts_per_day("new")
            self.rules_results.append(("Частота дописування",
                                       self.rule_posts_per_day_result["old"], 
                                       self.rule_posts_per_day_result["new"]))
            self.rule_size("old")
            self.rule_size("new")
            self.rules_results.append(("Середня кількість речень у пості",
                                       self.rule_size_result_sentences["old"], self.rule_size_result_sentences["new"]))
            self.rules_results.append(("Середня кількість слів у пості",
                                       self.rule_size_result_words["old"], self.rule_size_result_words["new"]))
            self.rule_links("old")
            self.rule_links("new")
            self.rules_results.append(("Частота посилань на інші джерела/людей", 
                                       self.rule_result_links["old"], self.rule_result_links["new"]))
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
