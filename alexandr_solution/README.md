# boots-recognition

Соревнование по своей сути, ввиду большого числа классов, было схоже с соревнованием https://www.kaggle.com/c/happy-whale-and-dolphin.
Поэтому за основу решения был взят ноутбук https://www.kaggle.com/code/debarshichanda/pytorch-arcface-gem-pooling-starter (most votes).

Первоначально, было замечено большое количество дубликатов в обучающей выборке. 
Поэтому была применена идея в виде заполнения одинаковых значений хэша от файлов одинаковыми метками (с трейна в тест).

В процессе обучения было протестировано множество различных моделей (efficientnet[0-5], inception). 
В качестве финального решения используется ..

НАПИСАТЬ ПРО ИДЕЮ С УДАЛЕНИЕМ ФОНА 
НАПИСАТЬ ПРО ИДЕЮ С ВРЕМЕНЕМ СОЗДАНИЯ ФАЙЛА