# :star2: corpus-ua-politics :star2:

Дока проєкту: https://docs.google.com/document/d/1Vo4vSQtpU6_YFY0PQ14P9CR2hqSWG-6i7bJb1faypv4/edit?usp=sharing

Таблиця зі списком правил і політиків: https://docs.google.com/spreadsheets/d/1n8Ags5MENNNpxJ-ANYwhFNqPZlHl7U9QguwCOCQ-PZw/edit?usp=sharing

## :keyboard: Збір текстів
Ми збираємо усі дописи з фейсбука певної публічної особи за однин місяць з 2021 року і один місяць 2022 року (наприклад, березень або квітень).

#### Як оформити файл?
```
посилання-на-допис (воно заховане в даті/часі публікації)

Речення допису. Речення допису.
Наступний аззац допису.
Останній абзац допису.
```
#### Як назвати файл?
За принципом (місяць-скорочено)_(день).(порядковий-номер-допису-за-день).txt

_Приклад_: `feb_20.1.txt`

#### Куди зберегти файл?
Усі тексти будуть у теці `data`, розсортовані за прізвищами людей, чиї тексти ми збираємо. У теці кожної людини будуть теки `old` (для текстів з 2021 року) і  `new` (тексти з 2022). Кожен допис має бути у  своєму окремому файлі, незалежно від його довжини.

_Приклад_: `data/zelenskyi/old/feb_20.1.txt`

Будь ласка, будьте із цим максимально уважні, зверніть увагу на формат дати (якщо беремо березень, то буде `mar_1` тощо)! Це важливо, щоб усі файли автоматично гарно зчитувались програмою і не викликали проблем.

#### Що робити з посиланнями в дописах?
* Якщо у вас в постах є посилання на сторінки, за можливості варто оформлювати їх отак: `<link>посилання</link>`.
* Якщо у ваших постах є посилання на фейсбучні профілі, будь ласка, додавайте їх окремо після згадування: `Микола Тищенко <link>посилання</link>`.

#### Що робити з емодзі?
Збираємо їх також.

## :writing_hand: Написання коду

### Що варто зробити до того як писати код правила?

#### 1. Зібрати мінімальну кількість даних
По 2-3 дописи для кожного періоду. Так ви будете краще уявляти свої дані й зможете перевіряти як на них працює ваше правило (наприклад, чи сходяться формати даних на вході).

#### 2. Написати тексти і оформити їх за прикладом у теці testing
Важливо мати не тільки TP випадки, а й TN, щоб бути впевненими, що ваше правило враховує необхідний контекст, і мати потім менше проблем з дебаґинґом.
Саме їх ми використовуємо для перевірки функціональности правила.

Для того, щоб цей процес був більш контрольованим, дані для тестів можна складати в окрему теку (наприклад всередині `testing`).

___Приклад 1___:

Перевірка: Чи є імена в тексті?

Текст: 
`Під час зустрічі з міністром закордонних справ Канади Mélanie Joly розповів про першочергові потреби Сил оборони України.`

Результат: `["Mélanie Joly"]`

___Приклад 2___:

Перевірка: та сама

Текст: 
`Детально обговорили подальшу взаємодію у сфері безпеки та оборони. Підтримка Канади української армії є неоціненною у ці важкі для нас часи.`

Результат: `[]`

#### 3. Чітко уявити як ваше правило має працювати
Зокрема, подивитися на дані, які ви будете отримувати на вході, їх формат, зорієнтуватися, що ви хочете отримати на виході, зрозуміти як потрібно зманіпулювати даними для цього, які бібліотеки вам для цього знадобляться.

_У загальному випадку правило має повертати список даних, яке воно зловило._

___Приклад 1___: 

якщо я шукаю імена, то пустий список буде означати, що імен немає (=False, по суті), а список з кількох елементів покаже нам, що результат позитивний, одночасно дозволивши побачити, що саме правило зловило, і зрозуміти, чи є помилка. 

___Приклад 2___: 

якщо я шукаю слова у незвичному значенні (сленг абощо), то мені також важливий контекст, тож у цьому випадку можливо краще повертати список словників, де ключем буде слово, яке ми зловили, а значенням — контекст, що покаже нам чи в цільовому значенні слово насправді вжито (`[{"бавовна": ["Пишуть про потужну бавовну в Білорусі. Звук вибуху ..."], ...}, ...]`)

### Приклади рівнів токенізації

1. всі тексти за період (одна велика стрінга з усіх дописів)
`"допис_1 ... допис_n"`

2. окремі дописи (список стрінгів з дописами)
`["допис_1", ..., "допис_n"]`

3. окремі речення (список списків дописів, де кінцевою стрінгою будуть окремі речення)
`[["речення_1 в допис_1", "речення_2 в допис_1", ...], ..., ["речення_1 в допис_n", "речення_2 в допис_n", ...]]`

4. окремі слова (список списків списків)))
`[[["слова", "в" , "речення_1", "допис_1"], ["слова", "в" , "речення_2", "допис_1"], ...], ..., [["слова", "в" , "речення_1", "допис_n"], ["слова", "в" , "речення_2", "допис_n"], ...]`

Stanza токенізує слова, тому кожне слово — це словник вигляду:
```
{
  "id": 1,
  "text": "Використовуємо",
  "lemma": "використовувати",
  "upos": "VERB",
  "xpos": "Vmpip1p",
  "feats": "Aspect=Imp|Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin",
  "head": 0,
  "deprel": "root",
  "start_char": 0,
  "end_char": 14
}
```

## :deciduous_tree: Як додавати свої зміни до проєкту?

Якщо ви раніше не працювали із системою git, то перед початком роботи на проєктом раджу пошукати в інтернеті як налаштувати акаунт в github. Також через `git config` варто визначити імʼя, прізвище та пошту користувача:ки (вас).

Якщо ви вже клонували проєкт на локальну машину, то прямий порядок приблизно такий:
1. Підтягніть останні зміни на гілці main (`git pull`);
2. Створіть свою гілку для змін (`git branch name_of_the_branch`);
3. Перейдіть на свою гілку (`git checkout name_of_the_branch` або `git checkout name_of_the_branch`);
4. Внесіть зміни, збережіть файли;
5. Виберіть, які файли ви хочете додати в коміт (`git add`);
6. Збережіть коміт в системі (`git commit -m "Опис зміни"`);
7. Коли ви готові, передайте свої локальні зміни у віддалений репозиторій у ґітгабі (`git push`);
8. Після того, як ваша робота буде готова, ми додамо її до головної гілки.

Щоб побачити актуальний стан речей з вашими змінами, викликайте `git status`.

Якщо ви не впевнені, що правильно все зробите з першого разу, то **зробіть бекап файлів в іншій теці** перед тим як вводити команди! Це може допомогти не втратити свою роботу, якщо щось піде не за планом.

Загалом, спершу з ґітом спершу може бути заплутано і незрозуміло, але в інтернеті багато відповідей на найрізноманітніші запитання щодо нього.

## Корисні посилання

Бібліотека, яку можна використати для переведення **емодзів** у читабельну для людини і програми текстову версію: https://pypi.org/project/emoji/

Документація до української версії **stanza**: https://universaldependencies.org/treebanks/uk_iu/index.html

## Бажаю всім успіхів та натхнення! :chocolate_bar:
![black-fast-typing-cat-rfo58klql1gydnw3](https://user-images.githubusercontent.com/64704141/219503802-7b3195b7-b874-40c9-8180-4eac4dc0c51d.gif)
