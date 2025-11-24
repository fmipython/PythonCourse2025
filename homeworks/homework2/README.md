# Домашно 2

Второто ни домашно оставя картите, и ни изпраща да търсим из файлове (локални, и не толкова локални).
Целта е да създадем наша паралелна версия на командата `grep` (която ще наричаме `mgrep`), която да поддържа следните опции:

```text
usage: mgrep.py [-h] [-n] [-m] [-p PARALLEL] [-r | -u] pattern [files ...]

positional arguments:
  pattern               Шаблон, по който да се търси
  files                 Файлове, в които да се търси

options:
  -h, --help            show this help message and exit
  -n, --line-number     Показване на номерата на редовете със съвпадения
  -m, --in-memory       Зареждане на целия файл в паметта преди търсене
  -p, --parallel PARALLEL
                        Брой паралелни търсения
  -r, --recursive       Рекурсивно търсене във всички файлове в директорията
  -u, --from-url        Търсене във файлове от URL адреси
```

## CLI аргументи

- `pattern` - шаблона, по който търсим във файловете.
- `files` - списък с 0 или повече файлове, в които ще търсим.
- `line-number` - при подаване, принтира всеки резултат във формата: `{file}:{line_number} - {line}`
- `in-memory` - при подаване, зарежда цялата съдържание на файла в паметта. В противен случай, чете файловете ред по ред.
- `parallel` - дефинира броя паралелни търсения.
- `recursive` - намира всички файлове рекурсивно под текущата директория и търси в тях.
- `from-url` - третира подадените пътища в `files` като URL-и. Сваля всеки един от файлове и търси в сваления файл.
- `help` - принтира по-горното съобщение, съдържащо информация за аргументите на grep

Аргументите `recursive` и `from-url` са взаимно-изключващи се.

За създаването на CLI интерфейса, може да използвате [argparse](https://docs.python.org/3.13/howto/argparse.html).

## Търсене

`pattern` поддържа [регулярни изрази](https://docs.python.org/3.13/library/re.html).

За основната логика при търсене във файл, дефинирайте функция на име `search_in_file`, която приема три аргумента - `pattern` по който да се търси, `file_path` в който да се търси и `is_in_memory` която определя дали съдържанието на файла да се държи в паметта. Като нейн резултат се очаква списък от tuple, съдържащи редовете, които отговарят на шаблона, името на файла в който е намерено съвпадението, и номера на реда.

Ако файла в който търсим не съществува, да се хвърли `InvalidFileError`.

## Памет

Ако файла трябва да се зареди в паметта, цялото му съдържание се прочита наведнъж.
В противен случай, файла се чете ред по ред.

## Паралелно търсене

При подаден аргумент `parallel` равен на 0, не се стартират отделни процеси за търсене. Търсенето се изпълнява в рамките на същия процес.

Ако броят на файловете в които търсим е по-малък от броя паралелни търсения, трябва да се хвърли `InvalidAmountOfWorkers`.

Ако броя паралелни търсения е по-малък от 0, също се хвърля `InvalidAmountOfWorkers`.

При паралелно търсене, файловете в които ще се търси се разделят на подгрупи. Към всеки от процесите се заделя група. Даден процес изпълня търсенето върху първия файл от групата, после върху втория и т.н. При приключване с групата, се взима следваща, ако такава е налична. (Всичко това е имплементирано в [`Pool`](https://docs.python.org/3.13/library/multiprocessing.html#module-multiprocessing.pool) обекта).

**Важно:** Тестовете разчитат на стартирането на нов процес, а не на нова нишка.

За целта, напишете функция `run_multi_threaded`, която приема следните аргументи:

- `pattern` по който да се търси
- списък с файлове, върху които ще се търси
- `is_in_memory`, който определя дали съдържанието на файла да се държи в паметта.
- `is_line_numbers` - дали да се показва името на файла и номера на реда, в който е открит шаблона.
- `amount_of_workers` - броя процеси, които ще се изпълняват в паралел.

Функцията принтира резултатите от търсенето.

## Файлове зад URL

Когато имаме файл зад URL, трябва да го свалите и запазите под директория `temp`, която се намира в текущата директория.

Може да приемете, че файла ще бъде наличен директно като отговор на заявката.

При неналичие на файла, покажете `Error when reading file.` и продължете към следващите файлове, ако има такива.

При приключване на работата на скрипта, тази директория трябва да бъде изтрита.

## Type hints

За да получите максималния брой точки, типовете на аргументите на функциите ви и това какво връща функцията трябва да бъдат указани чрез type hints.

## Структура

В решението ви очакваме един файл с име `mgrep.py`.

Освен споменатите изрични функции, имената и сигнатурите на останалите са по ваш избор.  

## Примери

```bash
$ python3 mgrep.py "ode" assets/first.txt

Machine learning models require quality data.
Version control tracks code changes efficiently.
```

```bash
$ python3 mgrep.py "ode" assets/first.txt -n
assets/first.txt:8 - Machine learning models require quality data.
assets/first.txt:21 - Version control tracks code changes efficiently.
```

```bash
$ python3 mgrep.py "one" -rn
./assets/second.txt:10 - Her phone buzzed with a message she wasn’t expecting.
./assets/second.txt:19 - The meeting dragged on longer than anyone had anticipated.
./assets/subdir/third.txt:11 - A narrow stream trickled peacefully between the mossy stones.
```

```bash
$ python3 mgrep.py ipsum "https://raw.githubusercontent.com/fmipython/PythonCourse2025/refs/heads/main/08%20-%20Files/files/1.txt" -u
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
```

```bash
$ python3 mgrep.py ipsum "https://raw.githubusercontent.com/fmipython/PythonCourse2025/refs/heads/main/08%20-%20Files/files/1.txt" -un
temp/1.txt:1 - Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
```
