#!/usr/bin/python
import sys
import re

def findIsotopes(ele):
    dir = "./Data/" #dir = "./Data/"
    fname = dir + "abundances.dat"
    #fname = "./Data/abundances.dat" - более лаконичный вариант
    f = open(fname) #открываем файл
    #f = fname.open()
    #tokens = [re.split(" ", line) for line in f.readlines()] #снова создаем двумерный массив и убираем все пробелы
    tokens = [re.split(" ", line) for line in f.readlines()]
    
    isotopes = "" #создаем пустую строку

    for words in tokens: #для каждой строки...
        for word in words: #для каждого элемента в строке.....
            if re.sub('[0-9]','',word) == ele.capitalize(): 
            #заменяем челые числа в строке на "ничего", т.е. убираем ВСЕ числа из каждой строки и переводим элемент ele в верхний регистр
            #и если в строке встречается нужный нам элемент, то добавляем его в строку...
            #например, 12С при ele=c заменится на С...
                isotopes += re.sub('[A-Z a-z]','',word) + " " #заменяем все буквы на НИЧЕГО и оставляем только число. 12С >> 12
               
    return isotopes

def main(argv): 
    ele = argv[1] 
    print((findIsotopes(ele))) #print findIsotopes(ele)

if __name__ == '__main__': 
#означает что если файл импортирован как модуль, то код после этих строк исполнен не будет,а если запущен как самостоятельный файл, то код после этих строк будет исполнен 
    main(sys.argv)
