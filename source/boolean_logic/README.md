### **Обща концепция**

### **Клас: `BooleanFunction`**

Класът `BooleanFunction` инкапсулира булев израз, предоставяйки функционалности за парсиране, опростяване, оценка, анализ на свойства и минимизиране на израза.

### **Компоненти и Методи:**

1. **Инициализация `__init__`:**
    - **Вход:** Стринг, представляващ булевия израз.
    - **Процес:**
      - Инициализира се изразът и се парсира в AST чрез лексер и парсер.
      - Извличат и сортират се променливите, участващи в израза.
      - Инициализират се различни кешове за съхранение на изчислени свойства и резултати за повишаване на ефективността.
    - **Изход:** Инстанция на `BooleanFunction` с парсираното AST и идентифицираните променливи.

2. **Опростяване `simplify`:**
    - **Цел:** Опростява булевия израз чрез намаляване на неговата сложност.
    - **Процес:**
      - Проверява се дали опростената версия вече е кеширана.
      - Ако не е, опростява се AST и се премахват ненужните външни скоби.
      - Кешира се и връща опростеният израз като стринг.
    - **Изход:** Опростена версия на оригиналния булев израз.
  
3. **Премахване на Външни Скоби `remove_outer_parens`:**
    - **Цел:** Почиства стринга на израза чрез премахване на ненужни външни скоби.
    - **Процес:**
      - Изразът се отстраняват водещите и завършващи интервали.
      - Проверява се дали целият израз е затворен в един комплект скоби.
      - Уверява се, че тези скоби не са необходими за запазване на правилния ред на операциите.
      - Премахват се външните скоби, ако са излишни.
    - **Изход:** Стринг на израза без ненужни външни скоби.

4. **Преобразуване в Жегалкин Полином `to_zhegalkin`:**
    - **Цел:** Преобразува булевия израз в неговото представяне като Жегалкин полином.
    - **Процес:**
      - Използва AST за изчисляване на Жегалкин полинома въз основа на идентифицираните променливи.
      - Преобразува полинома в стринг формат, подходящ за показване или по-нататъшна обработка.
      - Кешира резултата за бъдеща употреба.
    - **Изход:** Стринг, представляващ Жегалкин полинома на булевата функция.

5. **Генериране на Истинна Таблица `get_truth_table`:**
    - **Цел:** Генерира пълната истинна таблица за булевата функция.
    - **Процес:**
      - Итерация през всички възможни комбинации от входни стойности въз основа на броя на променливите.
      - Оценява булевата функция за всяка комбинация.
      - Кешира истинната таблица за ефективно извличане при последващи извиквания.
    - **Изход:** Списък от кортежи, всеки съдържащ набор от входни стойности и съответния изход на булевата функция.                                                
6. **Оценка `evaluate`:**
    - **Цел:** Изчислява стойността на булевата функция за даден набор от присвоявания на променливите.
    - **Вход:** Дикт `variables`, който съпоставя имената на променливите с техните булеви стойности.
    - **Процес:**
      - Използва AST за оценка на израза въз основа на предоставената среда.
    - **Изход:** Резултатът от оценката на булевата функция (0 или 1).
  
7. **Проверка на Свойства:**
    - **Запазване на Нула `preserves_zero`:**
        - **Цел:** Определя дали булевата функция връща 0, когато всички входове са 0.
        - **Процес:** Оценява функцията с всички променливи зададени на 0 и проверява изхода.
    - **Запазване на Единица `preserves_one`:**
        - **Цел:** Определя дали булевата функция връща 1, когато всички входове са 1.
        - **Процес:** Оценява функцията с всички променливи зададени на 1 и проверява изхода.
    - **Самодуелност `is_self_dual`:**
        - **Цел:** Проверява дали функцията е самодуелна, което означава, че размяната на всички 0 с 1 в входа инвертира изхода.
        - **Процес:** Сравнява всеки изход с изхода на допълнената входна комбинация.
    - **Монотонност `is_monotonic`:**
        - **Цел:** Определя дали функцията е монотонна, т.е. увеличаваща се във всички променливи.
        - **Процес:** Уверява се, че променянето на всяка входна стойност от 0 на 1 не намалява изхода.
    - **Линейност `is_linear`:**
        - **Цел:** Проверява дали функцията е линейна, което означава, че може да се изрази като линейна комбинация на променливите без продукти.
        - **Процес:** Анализира Жегалкин полинома, за да се увери, че нито един моном съдържа повече от една променлива.
    - **Кеширане:**
        - Всяка проверка на свойство кешира резултата си, за да избегне излишни изчисления при бъдещи извиквания.

8. **Минимизиране `minimize`:**
    - **Цел:**: Опростява булевата функция до минимална форма, използвайки алгоритъма на Куин-МакКласки.
    - **Процес:**
      - Генерира истинната таблица и идентифицира всички минтермини, където функцията връща 1.
      - Прилага алгоритъма на Куин-МакКласки за намиране на най-простата сума на продукти.
      - Форматира минимизирания израз и премахва ненужните скоби.
      - Кешира минимизирания израз за бъдеща употреба.
    - **Изход:** Минимизирана версия на булевия израз, оптимизирана за простота.
  
9. **Кофактор `cofactor`:**
    - **Цел:** Изчислява кофактора на булевата функция спрямо конкретна променлива, зададена на дадена стойност.
    - **Вход:**
        - `variable`: Променливата, която ще бъде зададена.
        - `value`: Стойността (0 или 1), която ще се присвои на променливата.
    - **Процес:**
      - Замества зададената променлива с дадената стойност в AST.
      - Опростява полученото изразяване.
      - Връща нова инстанция на `BooleanFunction`, представляваща кофактора.
    - **Изход:** Нова инстанция на `BooleanFunction`, представляваща кофактора с променливата зададена на дадената стойност.
  
10. **Декомпозиция `decompose`:**
    - **Цел:** Декомпозира булевата функция в два кофактора въз основа на конкретна променлива.
    - **Вход:**
        - `variable`: Променливата, спрямо която ще се декомпозира функцията.
    - **Процес:**
      - Изчислява кофактора, където променливата е зададена на 0.
      - Изчислява кофактора, където променливата е зададена на 1.
      - Връща двата кофактора.
    - **Изход:** Кортеж, съдържащ две инстанции на `BooleanFunction`, представляващи функцията с променливата зададена на 0 и 1 съответно.

11. **Равенство и Хеширане `__eq__` и `__hash__`:**
    - **Цел:** Дефинира как инстанциите на `BooleanFunction` се сравняват и съхраняват в колекции, базирани на хеш.
    - **Процес:**
      - Две инстанции на `BooleanFunction` се считат за равни, ако техните изрази са идентични.
      - Хешът на `BooleanFunction` се базира на хеша на стринга на израза.
    - **Изход:**
        - `__eq__`: Връща True, ако изразите съвпадат, иначе `False`.
        - `__hash__`: Връща цяло число, представляващо хеш стойността на израза.
          
---     
### **Клас: `BooleanFunctionSet`**

Класът `BooleanFunctionSet` управлява колекция от уникални инстанции на `BooleanFunction`, предоставяйки функционалности за добавяне на нови функции и извличане на подробна информация за всички съхранени функции.

### **Компоненти и Методи:**          

1. **Инициализация `__init__`:**
    - **Процес:**
      - Инициализира се празен сет за съхранение на инстанции на `BooleanFunction`.
    - **Изход:** Инстанция на `BooleanFunctionSet`, готова да съдържа булеви функции.
  
2. **Добавяне на Функции `add_function`:**
    - **Цел:** Добавя нова инстанция на `BooleanFunction` към сета.
    - **Вход:** Инстанция на BooleanFunction (boolean_function).
    - **Процес:**
      - Вмъква функцията в сета, осигурявайки уникалност на базата на израза на функцията.
    - **Изход:** Функцията се съхранява в сета; няма връщана стойност.
  
3. **Извличане на Информация за Функции `get_functions_info`:**
    - **Цел:** Събира подробна информация за всяка инстанция на `BooleanFunction` в сета.
    - **Процес:**
      - Итерация през всички функции в сета.
      - За всяка функция се компилира речник, съдържащ:
          - **Израз:** Оригиналният булев израз.
          - **Опростен:** Опростената версия на израза.
          - **Жегалкин Полином:** Жегалкин представянето.
          - **Свойства:** Речник, описващ свойства като запазване на нула и единица, самодуелност, монотонност и линейност.
          - **Минимизирани Израз:** Минимизирана форма, използвайки Куин-МакКласки.
          - **Брой на Променливите:** Броят на различните променливи във функцията.
          - **Истинна Таблица:** Форматирана истинна таблица, показваща комбинациите от входове и съответните изходи.
       - Събира всички такива речници в списък.
    - **Изход:** Списък от речници, всеки представляващ подробна информация за една булева функция в сета.
  
4. **Форматиране на Истинни Таблици `_format_truth_table`:**
    - **Цел:** Преобразува суровите данни от истинната таблица в структурирани и четими формати.
    - **Вход:**
        - `truth_table`: Списък от кортежи, съдържащи входни стойности и изход.
        - `variables`: Списък от имена на променливите, съответстващи на входните стойности.
    - **Процес:**
      - Итерация през всяка записа в истинната таблица.
      - За всяка комбинация от входове се създава речник, съпоставящ всяка променлива със съответната ѝ стойност.
      - Асосират всяка входна комбинация с нейния изход.
      - Компилират се тези речници в списък от речници за лесна четимост и по-нататъшна обработка.
    - **Изход:** Списък от речници, всеки съдържащ `inputs` речник и `output` стойност, представляващи истинната таблица в структурирана форма.

### **Функция: `get_variables`**

Функцията `get_variables` е предназначена да извлече всички уникални имена на променливи от даден възел на Абстрактното Синтактично Дърво (AST), който представлява булева израз.

1. **Функционалност:** 
    - **Вход:** Един AST възел `node`, който представлява част от булев израз.
    - **Процес:**
      - Инициализира се празен набор за съхранение на имената на променливите.
      - Проверява се типа на възела:
         - Ако възелът е `VariableNode`, добавя се името на променливата в набора.
         - Ако възелът е `NotNode`, рекурсивно се извличат променливите от неговия операнд.
         - Ако възелът е един от логическите оператори (`AndNode`, `OrNode`, `XorNode`, `ImpNode`, `EqvNode`, `NandNode`, `NorNode`), рекурсивно се извличат                променливите от двата му операнда (ляв и десен).
    - **Изход:** Сортиран списък от уникални имена на променливи, присъстващи в булевия израз.

---
### **Клас: `GateNode`**

Класът `GateNode` представлява възел в абстрактно синтактично дърво (AST) за логически гейтове, използвано за моделиране на логически изрази.

1. **Функционалност:** 
    - **Инициализация:**
        - При създаване на инстанция на `GateNode`, се задава типа на гейта `gate_type`, който може да бъде логически оператор като "AND", "OR", "NOT", или                  променлива ("VAR").  
        - Възможно е да се зададат и деца (children) на възела, които представляват подизрази или операнди. Ако не се предоставят деца, те се инициализират като             празен списък.
    - **Свойства:**
        - **`gate_type`:** Типът на логическия гейт (например "AND", "OR", "NOT", "VAR").
        - **`children`:** Списък от деца възела, които могат да бъдат други GateNode инстанции или стойности.

### **Функция: `parse_minimized_expression`**

Функцията `parse_minimized_expression` парсира опростен логически израз, представен като стринг, и го преобразува в абстрактно синтактично дърво (AST) от типове `GateNode`.

1. **Функционалност:** 
    - **Почистване на израза:**
        - Първоначално, изразът се отстраняват водещите и завършващи интервали.  
    - **Обработка на прости изрази:**
        - Ако изразът е алфанумеричен или представлява "1" или "0", се създава `GateNode` с тип "VAR" и изразът се добавя като дете.
    - **Премахване на външни скоби:**
        - Проверява се дали изразът започва и завършва със скоби.
        - Ако всички скоби балансират правилно и външните скоби са ненужни, те се премахват, като се запазва вътрешното съдържание.
    - **Намиране на най-високо ниво на оператор:**
        - Вътрешна функция `find_top_level_operator` преминава през израза, като проследява нивото на скобите.
        - При откриване на оператор "AND" или "OR" на най-високо ниво (извън всякакви скоби), връща оператора и неговата позиция.
    - **Рекурсивно парсиране на подизразите:**
        - Ако е намерен оператор "AND" или "OR", изразът се разделя на ляв и десен подизраз.
        - Функцията се извиква рекурсивно за всеки от подизразите, създавайки съответните `GateNode` възли.
    - **Обработка на оператор "NOT":**
        - Ако изразът започва с "NOT", се извлича подизразът след "NOT".
        - Функцията се извиква рекурсивно за подизраза, създавайки `GateNode` с тип "NOT" и дете.
    - **Грешки при неразбираем израз:**
        - Ако изразът не отговаря на никой от горепосочените случаи, се издига изключение, указващо, че изразът не може да бъде парсиран.
     - **Изход:** Коренов `GateNode` на AST, представляващ структурираната форма на логическия израз.

### **Функция: `gate_ast_to_graphviz`**

Функцията `gate_ast_to_graphviz` преобразува AST, съставено от `GateNode` инстанции, в графично представяне с помощта на библиотеката Graphviz. Това позволява визуализиране на логическия израз като граф.

1. **Функционалност:** 
    - **Идентифициране на възела:**
        - За всеки `GateNode`, се генерира уникален идентификатор чрез използване на `id(node)`.
    - **Създаване на графичен възел:**
        - Ако възелът представлява променлива ("VAR"), се създава графичен възел със формата "кръг" и етикетира се с името на променливата.
        - Ако възелът представлява логически оператор ("AND", "OR", "NOT"), се създава графичен възел с формата "кутия" и етикетиран с типа на оператора.
    - **Рекурсивно обработване на децата:**
        - За всяко дете на текущия възел:
            - Ако детето е `GateNode`, функцията се извиква рекурсивно за детето, като се създават съответните графични връзки между родителския и детето.
            - Ако детето не е `GateNode` (например, стойност като "1" или "0"), се създава графичен възел за стойността и се свързва към родителския възел.
    - **Връщане на идентификатора на възела:**
        - След създаване на всички възли и връзки, се връща идентификаторът на текущия възел.
     - **Изход:** Идентификатор на кореновия възел в графа, който е използван за визуализиране на цялото AST.

---
### **Клас: `KarnaughMap`**

Класът `KarnaughMap` е предназначен да генерира и визуализира Карно карти (Karnaugh maps) за дадена булева функция. Карно картите са инструмент, използван за опростяване на булеви алгебрични изрази, което е особено полезно в дизайна на цифрови схеми и логически оптимизации. Класът предоставя методи за създаване на Карно карти за булеви функции с 2 до 4 променливи и тяхното визуално представяне чрез графики.

### **Компоненти и Методи:**

1. **Инициализация `__init__`:**
    - **Вход:** Инстанция на `BooleanFunction`, която представлява булевата функция, за която ще се създаде Карно картата.
    - **Процес:**
      - Съхранява се булевата функция и нейните променливи.
      - Изчислява се броят на променливите.
      - Проверява се дали броят на променливите е между 2 и 4 включително, тъй като Карно картите са приложими само за този диапазон.
      - Извлича се истинната таблица на булевата функция за по-нататъшна обработка.
    - **Изход:** Инстанция на `KarnaughMap` с необходимите атрибути и проверени условия за броя на променливите.

2. **Генериране на Карно Карта `generate_map`:**
    - **Цел:** Генерира Карно картата за булевата функция в зависимост от броя на променливите.
    - **Процес:**
      - Връща се резултатът от съответния метод за генериране на Карно карта за 2, 3 или 4 променливи.
    - **Изход:** Карно картата като NumPy масив и списък с имената на променливите.
  
3. **Генериране на Карно Карта за 2 Променливи `_generate_map_2vars`:**
    - **Цел:** Създава Карно карта за булеви функции с 2 променливи.
    - **Процес:**
      - Дефинира се карта с 2 реда и 2 колони, съответстващи на възможните комбинации от входни стойности.
      - Запълва се Карно картата със стойностите от истинната таблица на функцията.
    - **Изход:** Карта като 2x2 NumPy масив и списък с имената на променливите.
      
4. **Генериране на Карно Карта за 3 Променливи `_generate_map_3vars`:**
    - **Цел:** Създава Карно карта за булеви функции с 3 променливи.
    - **Процес:**
      - Дефинира се карта с 2 реда и 4 колони, които представят всички комбинации от трите променливи.
      - Запълва се Карно картата със стойностите от истинната таблица на функцията.
    - **Изход:** Карта като 2x4 NumPy масив и списък с имената на променливите.

5. **Генериране на Карно Карта за 4 Променливи `_generate_map_4vars`:**
    - **Цел:** Създава Карно карта за булеви функции с 4 променливи.
    - **Процес:**
      - Дефинира се карта с 4 реда и 4 колони, които обхващат всички възможни комбинации от четирите променливи.
      - Запълва се Карно картата със стойностите от истинната таблица на функцията.
    - **Изход:** Карта като 4x4 NumPy масив и списък с имената на променливите.
                                                      
6. **Визуализиране на Карно Карта `plot_map`:**
    - **Цел:** Създава графично представяне на генерираната Карно карта чрез библиотеката Matplotlib.
    - **Процес:**
      - Генерира се Карно картата чрез извикване на метода `generate_map`.
      - Определят се имената на редовете и колоните в зависимост от броя на променливите.
      - Използва се `plt.table` за създаване на таблица, която представя Карно картата с етикети за редове и колони.
      - Настройва се скалата на таблицата и се добавя заглавие.
      - Показва се визуализацията чрез `plt.show()`.
    - **Изход:** Графично представяне на Карно картата, показващо логическите стойности на булевата функция за всички комбинации от входни променливи.

---
### **Клас: `Validator`**

Класът `Validator` е предназначен да проверява валидността на дадени булеви изрази. Той предоставя метод за валидация, който проверява дали изразът е синтактично правилен чрез процесирането му чрез лексера и парсера. Това е полезно за осигуряване на коректността на изразите преди тяхната по-нататъшна обработка или анализ. Класът `Validator` съдържа само един статичен метод, който извършва валидацията на булевия израз. Статичните методи са методи, които не изискват инстанция на класа за да бъдат извикани и могат да бъдат използвани директно чрез името на класа.

### **Компоненти и Методи:**

1. **Статичен Метод `validate`:**
    - **Цел:** Методът `validate` проверява дали даден булев израз е синтактично правилен. Той се опитва да го обработи чрез лексера и парсера и връща резултат,           указващ дали изразът е валиден или не, както и евентуално съобщение за грешка, ако има такава.
    - **Вход:** `expression`: Стринг, представляващ булевия израз, който трябва да бъде валидиран.
    - **Процес:**
      - **Инициализация на Лексера:** Създава се инстанция на класа `Lexer`, като се подава входният израз. Лексерът ще се погрижи за разделянето на израза на              токени, които представляват основните елементи на израза (например, променливи, логически оператори).
      - **Токенизация:** Използва се методът `tokenize` на лексера за преобразуване на израза в поредица от токени. Този процес включва разпознаване и                      категоризиране на различните части на израза.
      - **Инициализация на Парсера:** Създава се инстанция на класа `Parser`, като се подава списъкът от токени, генериран от лексера. Парсерът ще анализира тази           поредица от токени, за да изгради AST, което представлява структурираното представяне на израза.
      - **Парсинг:** Използва се методът `parse` на парсера за изграждане на AST от токените. Ако парсингът е успешен, това означава, че изразът е синтактично              правилен.
    - **Изход:**
        - Ако изразът е валиден: Връща се кортеж `(True, None)`, където `True` указва успешната валидация, а `None` означава липса на грешки.
        - Ако изразът е невалиден: Връща се кортеж `(False, str(e))`, където `False` указва неуспешната валидация, а `str(e)` съдържа текста на изключението,                което описва причината за грешката. 

---
### **Функция: `add_polynomials`**

Функцията `add_polynomials` е предназначена за събиране на два полинома, представени като множества от мономи. В контекста на булевата алгебра, тази операция се извършва чрез симетрично разлика на множествата, което съответства на операцията XOR (изключващо ИЛИ) между мономите.

1. **Функционалност:** 
     - **Вход:**
         - `polynomial1`: Първият полином, представен като множество от мономи.
         - `polynomial2`: Вторият полином, също представен като множество от мономи.
     - **Процес:**
         - Използва се симетрично разлика `symmetric_difference` между множествата `polynomial1` и `polynomial2`.
         - Това означава, че мономите, които се срещат само в един от двата полинома, ще бъдат включени в резултата.
         - Мономите, които присъстват и в двата полинома, ще бъдат премахнати, тъй като в булевата алгебра тяхното събиране води до нула.
     - **Изход:** Връща се ново множество, представляващо сумата на двата полинома.
  
### **Функция: `multiply_polynomials`**

Функцията `multiply_polynomials` се използва за умножение на два полинома, представени като множества от мономи. В булевата алгебра, умножението на мономи се осъществява чрез логическото И (AND), което съответства на комбинирането на битове чрез XOR (изключващо ИЛИ) в контекста на Жегалкин полиномите.

1. **Функционалност:** 
     - **Вход:**
         - `polynomial1`: Първият полином, представен като множество от мономи.
         - `polynomial2`: Вторият полином, също представен като множество от мономи.
     - **Процес:**
         - Инициализира се празно множество за съхранение на резултата.
         - За всеки моном от първия полином `m1`:
             - За всеки моном от втория полином `m2`:
                 - Извършва се XOR операция между `m1` и `m2`, което представлява умножението на двата монома.
                 - Ако резултатният моном вече съществува в резултатното множество, той се премахва (тъй като XOR два пъти една и съща стойност връща обратно до                      оригиналната стойност).
                 - Ако не съществува, той се добавя.
     - **Изход:** Връща се множество, съдържащо резултатните мономи от умножението на двата полинома.
  
### **Функция: `monomial_to_str`**

Функцията `monomial_to_str` преобразува един моном (представен като цяло число) в неговото текстово представяне, използвайки списък с променливи. Това улеснява визуалното представяне и разбирането на мономите в човекоразбираем формат.

1. **Функционалност:** 
     - **Вход:**
         - `monomial`: Мономът, представен като цяло число, където всеки бит представлява присъствието (1) или отсъствието (0) на съответната променлива.
         - `variables`: Списък от имена на променливи, които съответстват на битовите позиции в монома.
     - **Процес:**
         - Инициализира се празен списък за събиране на термините.
         - За всяка променлива и нейния индекс:
             - Проверява се дали съответният бит в монома е зададен на 1.
             - Ако е, името на променливата се добавя към списъка от термини.
         - Ако няма активни битове (т.е., мономът е 0), се връща стринг "1", което представлява константа 1 в булевата алгебра.
         - В противен случай, мономът се преобразува в стринг чрез свързване на термини с "*" (логическо И).
     - **Изход:** Стринг, представляващ монома в четим формат, като например "A*B" за моном с променливите A и B активни.
     - **Пример:**
         - Ако `monomial` е `3` (двоично `11`) и variables са `['A', 'B']`, функцията ще върне "A*B".
         - Ако `monomial` е `0`, ще върне "1".

### **Функция: `zhegalkin_polynomial_to_str`**

Функцията `zhegalkin_polynomial_to_str` преобразува множество от мономи, представляващи Жегалкин полином, в неговото текстово представяне. Жегалкин полиномите са уникални алгебрични представяния на булеви функции, които използват само операцията XOR и константата 1.

1. **Функционалност:** 
     - **Вход:**
         - `polynomial`: Множество от мономи, представляващи Жегалкин полином.
         - `variables`: Списък от имена на променливи, които съответстват на битовите позиции в мономите.
     - **Процес:**
         - Проверява се дали полиномът е празен. Ако е, се връща "0", което представлява константа 0 в булевата алгебра.
         - За всеки моном в полинома:
             - Извиква се функцията `monomial_to_str`, за да се преобразува мономът в текстов формат.
         - Събира се списък от текстови представяния на всички мономи.
         - Обединява се списъкът чрез " + " (логическо XOR), което представлява сумата на мономите в Жегалкин полинома.
     - **Изход:** Стринг, представляващ Жегалкин полином в четим формат, като например "A + BC" за полином с мономите A и BС.
     - **Пример:**
         - Ако `polynomial` е `{1, 2}` и `variables` са `['A', 'B']`, функцията ще върне "A + B".
         - Ако `polynomial` е празно множество, ще върне "0".

---
### **Обща Информация за Алгоритъма на Куин-МакКласки**

Алгоритъмът на Куин-МакКласки е метод за минимизиране на булеви функции. Той автоматизира процеса на намиране на най-простите форми на булеви изрази, като идентифицира и елиминира излишните термини. Това е особено полезно при дизайна на цифрови схеми и оптимизацията на логически изрази.

### **Функция: `quine_mccluskey`**

Функцията `quine_mccluskey` реализира алгоритъма на Куин-МакКласки за минимизиране на булеви функции. Тя приема списък от минтермини и (по избор) неразглеждани термини `don't cares` и връща множество от есенциални първични импликанти, които представляват минимизирания булев израз.

1. **Функционалност:** 
     - **Вход:**
         - `minterms`: Списък от минтермини, представляващи комбинациите от променливи, при които булевата функция е 1.
         - `num_vars`: Броят на променливите в булевата функция.
         - `dont_cares` (по избор): Списък от термини, които могат да бъдат пренебрегнати при минимизацията (необходими за допълнителна гъвкавост при                         опростяването).
     - **Процес:**
         - Комбиниране на Минтермини и Неразглеждани Термини: Всички минтермини и неразглеждани термини се комбинират в едно общо множество, което ще се                      използва за групиране по броя на единиците в двоичната им форма.
         - Групиране по Брой Единици: Минтермините се групират в речник `groups`, където ключът е броят на единиците в двоичната форма на термина, а                          стойността е списък от тези термини.
         - Идентифициране на Първични Импликанти:
             - Извършва се итеративен процес на комбиниране на термини от съседни групи (разлика от една единица) и създаване на нови комбинирани термини с                       използване на символа `-` за различните позиции.
             - Термините, които не могат да бъдат комбинирани повече, се считат за първични импликанти и се добавят към множеството `prime_implicants`.
             - Процесът продължава, докато не могат да се създадат нови комбинирани групи.
         - Намиране на Есенциални Първични Импликанти: Извиква се функцията `find_essential_prime_implicants_with_dont_cares`, която определя кои от                          първичните импликанти са есенциални (необходими за покриване на всички минтермини).
         - Връщане на Резултат: Връща се множество от есенциални първични импликанти, които формират минимизирания булев израз.
     - **Изход:** `essential_prime_implicants`: Множество от първични импликанти, представляващи минимизирания булев израз.
  
### **Функция: `find_essential_prime_implicants_with_dont_cares`**

Функцията `find_essential_prime_implicants_with_dont_cares` идентифицира есенциалните първични импликанти от множеството на всички първични импликанти, като взема предвид минтермините и неразглежданите термини `don't cares`. 

1. **Функционалност:** 
     - **Вход:**
         - `prime_implicants`: Множество от първични импликанти, които са били генерирани от основната функция `quine_mccluskey`.
         - `minterms`: Списък от минтермини, които трябва да бъдат покрити от импликантите.
         - `num_vars`: Броят на променливите в булевата функция.
     - **Процес:**
         - Преобразуване на Минтермини в Двоична Форма: Минтермините се преобразуват в двоични стрингове, съобразени с броя на променливите.
         - Покритие на Минтермини от Импликанти: За всеки първичен импликант се определя кои минтермини той покрива, като се проверява дали всички битове                     съвпадат или са заменени със символа `-` (който представлява "don't care" за тази позиция).
         - Идентифициране на Есенциални Импликанти:
             - За всеки минтермин се определя кои първични импликанти го покриват
             - Ако даден минтермин се покрива само от един импликант, този импликант се счита за есенциален и се добавя към множеството `essential_pis`.
         - Покриване на Останалите Минтермини:
             - Минтермините, които не са покрити от есенциалните импликанти, трябва да бъдат покрити от останалите импликанти.
             - Използва се методът на backtracking за намиране на най-малкия набор от импликанти, които покриват всички останали минтермини. 
         - Финално Събиране на Резултати: Есенциалните импликанти се комбинират с допълнителните импликанти, нужни за покриване на всички минтермини.
     - **Изход:** `final_solution`: Множество от есенциални и допълнителни импликанти, формиращи минимизирания булев израз.

### **Функция: `matches`**

Функцията `matches` проверява дали даден първичен импликант покрива конкретен минтермин. Това става чрез сравняване на двоичните представяния на импликанта и минтермита, като се допуска символът `-` в импликанта, който представлява "don't care" за съответната позиция.

1. **Функционалност:** 
     - **Вход:**
         - `prime_implicant`: Стринг, представляващ първичен импликант с възможни символи `0`, `1` и `-`.
         - `minterm`: Стринг, представляващ минтермин, състоящ се само от символи `0` и `1`.
     - **Процес:**
         - За всяка позиция в двата стринга се сравняват символите:
             - Ако символът в импликанта е `-`, тази позиция се счита за съвпадаща независимо от стойността в минтермита.
             - Ако символът не е `-`, той трябва да съвпада точно със символа в минтермита за съответната позиция.
         - Ако всички позиции отговарят на тези условия, функцията връща `True`, в противен случай `False`.
     - **Изход:**
         - `True` ако импликантът покрива минтермита.
         - `False` ако не покрива.
---
### **Примери:**

### **Клас: `BooleanFunction`**
- **Създаване и Опростяване на Булева Функция:**
    - **Вход:** "`A AND (B OR NOT C)`"
    - **Изход:** "`A*B + A*~C`"
- **Генериране на Истинна Таблица:**
    - **Израз:** "`A OR B`" 
    - **Изход:** `[({'A': 0, 'B': 0}, 0),    ({'A': 0, 'B': 1}, 1),    ({'A': 1, 'B': 0}, 1),    ({'A': 1, 'B': 1}, 1)]`
- **Оценка на Булева Функция:**
    - **Израз:** "`A AND B OR C`"
    - **Среда:** `{'A': 1, 'B': 0, 'C': 1}`
    - **Изход:** `1` 
- **Проверка на Свойства:**
    - **Израз:** "`A OR B`" 
        - **Запазва нула:** `True` (когато A=0 и B=0, изходът е 0)
        - **Запазва единица:** `False` (когато A=1 и B=1, изходът е 1)
        - **Самодуелна:** `False`
        - **Монотонна:** `True`
        - **Линейна:** `True`
- **Минимизиране на Булева Функция:**
    - **Вход:** "`A OR (B AND C)`"
    - **Изход:** "`A + B*C`"
  
### **Клас: `BooleanFunctionSet`**
- **Добавяне и Управление на Булеви Функции:**
    - **Действие:**
        - Добавяне на функция "`A AND B`"
        - Добавяне на функция "`A OR B`"
        - Добавяне на функция "`A AND B`" (ще бъде игнориран, тъй като вече съществува)
- **Съдържание на Сета:**
    - "`A AND B`"
    - "`A OR B`"
- **Извличане на Информация за Функции:**
    - **Сет:** Функции "`A AND B`" и "`A OR B`"
    - **Изход:**
   `[
    {
        "Израз": "A AND B",
        "Опростен": "A*B",
        "Жегалкин Полином": "A*B",
        "Свойства": {
            "Запазва нула": True,
            "Запазва единица": True,
            "Самодуелна": False,
            "Монотонна": True,
            "Линейна": False
        },
        "Минимизирани Израз": "A*B",
        "Брой на Променливите": 2,
        "Истинна Таблица": [
            {"inputs": {"A": 0, "B": 0}, "output": 0},
            {"inputs": {"A": 0, "B": 1}, "output": 0},
            {"inputs": {"A": 1, "B": 0}, "output": 0},
            {"inputs": {"A": 1, "B": 1}, "output": 1}
        ]
    },
    {
        "Израз": "A OR B",
        "Опростен": "A + B",
        "Жегалкин Полином": "A + B",
        "Свойства": {
            "Запазва нула": True,
            "Запазва единица": False,
            "Самодуелна": False,
            "Монотонна": True,
            "Линейна": True
        },
        "Минимизирани Израз": "A + B",
        "Брой на Променливите": 2,
        "Истинна Таблица": [
            {"inputs": {"A": 0, "B": 0}, "output": 0},
            {"inputs": {"A": 0, "B": 1}, "output": 1},
            {"inputs": {"A": 1, "B": 0}, "output": 1},
            {"inputs": {"A": 1, "B": 1}, "output": 1}
        ]
    }
]`

**Функция: `add_polynomials`**
- Ако `polynomial1` е `{1, 2}` и `polynomial2` е `{2, 3}`, функцията ще върне `{1, 3}`.
- Ако `polynomial1` е `{0, 1}` и `polynomial2` е `{1, 2}`, функцията ще върне `{0, 2}`.
  
**Функция: `multiply_polynomials`**
- Ако `polynomial1` е `{1, 2}` и `polynomial2` е `{2, 3}`, функцията ще върне `{1, 3}`.
- Ако `polynomial1` е `{0, 1}` и `polynomial2` е `{1, 2}`, функцията ще върне `{2, 3}`.
  
**Функция: `monomial_to_str`**
- Ако `monomial` е `3` и variables са `['A', 'B']`, функцията ще върне "`A*B`".
- Ако `monomial` е `0` и variables са `['A', 'B']`, функцията ще върне "`1`".
  
**Функция: `zhegalkin_polynomial_to_str`**
- Ако `polynomial` е `{1, 2}` и variables са `['A', 'B']`, функцията ще върне "`A + B`".
- Ако `polynomial` е празно множество, функцията ще върне "`0`".
  
**Функция: `quine_mccluskey`**
- Ако `minterms` са `[0, 1, 2, 5, 6, 7]`, `num_vars` е `3` и `dont_cares` са `[3, 4]`, функцията ще върне `{'0-0', '1-1', '-11'}`.
- Ако `minterms` са `[0, 1, 3, 7]`, `num_vars` е `3` и няма `dont_cares`, функцията ще върне `{'0-0', '1-1', '-11'}`.
  
**Функция: `matches`**
- Ако `prime_implicant` е "`1-0`" и `minterm` е "`110`", функцията ще върне `True`.
- Ако `prime_implicant` е "`1-0`" и `minterm` е "`101`", функцията ще върне `False`.
  
**Функция: `get_variables`**
- Ако AST е на израз "`A AND (B OR C)`", функцията ще върне `['A', 'B', 'C']`.
  
**Функция: `gate_ast_to_graphviz`**
- Ако AST е на израз "`A AND B`", функцията ще визуализира логическото И между A и B.
---
