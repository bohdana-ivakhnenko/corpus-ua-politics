import stanza
import pymorphy3
import tokenize_uk
# треба вирішити чим саме користуватимемось. stanza доволі повільна, але можна подивитись які будуть обсяги
# імпортувати штуки для гарного виведення у консоль - кольори й таблички
# імпортувати штуки для збереження - БД?


class Analysis:
    def __init__(self, name):
        self.name = name
        self.read()
        self.tokenize()

    def read(self):
        # структура: папка із прізвищем-ім'ям, у ній папки old і new, у них кожен текст в окремому файлі
        # окремий файл дасть можливість аналізувати частотність певних явищ на пост
        # можна зробити систему із назва файлу - дата і час посту, аналізувати кількість постів на день тощо
        # але якщо чесно мені не хочеться заморачуватись, а чи буде цим займатись хтось інший?
        # або простіше: папка, у ній два файли, у файлах тексти із певним розділювачем (/n/n?)

        # self.text = суцільний текст
        # self.posts = окремі пости
        pass

    def tokenize(self):
        # начебто тільки речення й слова треба
        # чи треба зберігати набори слів/речень під конкретні пости чи можна суцільний текст?

        # self.sents =
        # self.words =
        pass

    def full(self):
        # тут викликати всі інші функції аналізу
        pass

    def analysis_name(self):
        # тіло аналізу

        # if *property* in *text*:
        #    self.analysis_name_result = "результат аналізу"
        #    return self.analysis_name_result
        #
        # self.analysis_name_result = False
        pass

    def save_results(self):
        # у якому форматі будемо зберігати? чи треба це взагалі?
        pass


if __name__ == __main__:
    politician = Analysis("volodymyr zelenskyi")
