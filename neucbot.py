#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from past.utils import old_div  # pip install future
import sys
import os
sys.path.insert(0, './Scripts/')    # vscode suggests better solution via adding "./Scripts" to extraPass
import re
import subprocess
import shutil
import math
import parseENSDF as ensdf  # pip install sgmllib3k
import getNaturalIsotopes as gni
import getAbundance as isoabund
import chemistry
import os
import matplotlib.pyplot as plt
import numpy as np

class constants:
    N_A = 6.0221409e+23
    MeV_to_keV = 1.e3
    mb_to_cm2 = 1.e-27
    year_to_s = 31536000
    min_bin = 0   # keV
    max_bin = 20000  # keV
    delta_bin = 100  # keV
    run_talys = False
    run_alphas = True
    print_alphas = False
    download_data = False
    download_version = 2
    force_recalculation = False
    ofile = sys.stdout


class material:
    def __init__(self, e, a, f, b):
        self.ele = str(e)
        self.A = float(a)
        self.frac = float(f)
        self.basename = str(b)

    def get_list(self):
        return [self.ele, self.A, self.frac, self.basename]


def isoDir(ele, A): # example './Data/Isotopes/Be/Be9/'
    with open(r"./Data/routes.txt", "r") as file:
        return file.readlines()[14].rstrip()+ele.capitalize()+'/'+ele.capitalize()+str(int(A))+'/'


def save(name='', fmt='png'):
    pwd = os.getcwd()
    iPath = './Pictuers/'
    if not os.path.exists(iPath):
        os.mkdir(iPath)
    os.chdir(iPath)
    plt.savefig(name)
    os.chdir(pwd)


def parseIsotope(iso):  # return [ele, A]
    ele = ''
    A = 0
    for i in iso:
        if i.isalpha():  # если буква
            ele += i
        if i.isdigit():  # если число
            A = A*10 + int(i)
    return [ele, A]


def generateAlphaFileName(ele, A):  # return fName
    outdir = './AlphaLists/'
    # example: ./AlphaLists/Th232Alphas.dat
    fName = outdir + ele.capitalize() + str(A) + 'Alphas.dat'
    return fName


def generateAlphaList(ele, A):
    print('generateAlphaList(', ele, A, ')', file=constants.ofile)
    # Заполняет ./AlphaLists/Th232Alphas.dat
    # ENSDF is a database that contains evaluated nuclear structure
    # and decay information for over 3,000 nuclides    
    ensdf.main(['parseENSDF', ele, A])


def loadAlphaList(fname):   # return alpha_list - просто массив из энергии + вероятности (intensity)
    f = open(fname) # example: fame = ./AlphaLists/Th232Alphas.dat
    tokens = [line.split() for line in f.readlines()]
    alpha_list = []
    for words in tokens:
        # if words[0][0] == '#' or len(words) < 2:
        #    continue
        alpha = []
        for word in words:
            alpha.append(float(word))
        alpha_list.append(alpha)
    f.close()
    # print( alpha_list)
    return alpha_list   # Просто массив из энергии + вероятности (intensity)


def getAlphaList(ele, A):
    # example: fName = ./AlphaLists/Th232Alphas.dat
    fname = generateAlphaFileName(ele, A)
    return loadAlphaList(fname)


def getAlphaListIfExists(ele, A):
    # example: fName = ./AlphaLists/Th232Alphas.dat
    fName = generateAlphaFileName(ele, A)
    tries = 3
    # выполнять пока на этом пути нет файла:
    while not os.path.isfile(fName):
        if tries < 0:
            print('Cannot generate alpha list for ele =', ele, ' and A =', A, file=constants.ofile)
            return 0
        print('generating alpha file', fName, file=constants.ofile)
        generateAlphaList(ele, A)    # Я сюда не лез
        tries -= 1
    # Создаёт заполненный список энергий альфачастиц и вероятность их появления в цепочке
    return getAlphaList(ele, A)


def loadChainAlphaList(fname):      # return list [E_alpha, Intesity of such E_alpha] for each isotop in chain
    f = open(fname)  # f = Chains/Th232Chain.dat
    tokens = [line.split() for line in f.readlines()]
    # читает цепочку распада. 2 столбца:
    # название элемента и
    # вероятность распада в него из предыдущего
    alpha_list = []
    for line in tokens:
        if len(line) < 2 or line[0][0] == '#':
            continue
        # Read isotope and its branching ratio from file
        iso = line[0]   # Элемент + атомная масса
        br = float(line[1])  # Вероятность распада в изотоп из предыдущего
        [ele, A] = parseIsotope(iso)  # дробит Th232 на ele=Th, A=232

        # Now get the isotope's alpha list and add it to the chain's list
        aList_forIso = getAlphaListIfExists(ele, A)
      # aList_forIso = заполненный список энергий альфачастиц и вероятность их появления в цепочке (intesity)
        if constants.print_alphas:  # По умолчанию это False
            print(iso, file=constants.ofile)  # ?????? не важно
            print('\t', aList_forIso, file=constants.ofile)
        # ene -энергия, intensity - вероятность распада в изотоп из предыдущего
        for [ene, intensity] in aList_forIso:
            alpha_list.append([ene, old_div(intensity*br, 100)])
            # print(ene, '\t\t', old_div(intensity*br,100))
    # список из [энергии, вероятность появления такой частицы в цепи] для всех элементов в цепи
    return alpha_list


def readTargetMaterial(fname):
    f = open(fname)  # f = Materials/Acrylic.dat
    mat_comp = []
    tokens = [line.split() for line in f.readlines()]
    for line in tokens:  # Читаем файл из 4х столбцов: название элемента,
        # его массовое число, процентное содержание оного в веществе
        # и название базы данных, откуда его взять (J / T)
        if len(line) < 3:
            continue
        if line[0][0] == '#':
            continue
        ele = line[0].lower()  # считываем данные
        A = int(line[1])
        frac = float(line[2])
        basename = line[3].lower() if len(line) == 4 else 't'

        if A == 0:
            # массовые числа изотопов ele
            natIso_list = gni.findIsotopes(ele).split()
            for A_i in natIso_list:  # разные массовые числа одного изтопа по очереди`
                # ищет распространённость конкретного изотопа
                abund = float(isoabund.findAbundance(
                    str(A_i)+ele.capitalize()))
                # структура из названия элмента, его массы,
                mater = material(ele, A_i, frac*abund/100., basename)
                # и (содержания в веществе)*(распространённость)/100 (=? массовая доля)
                # вставляет в конец списка mat_comp строку mater
                mat_comp.append(mater)
                # print(mater.get_list())
        else:
            # структура из названия элемента, его массы, и масоовой доли в веществе
            mater = material(ele, A, frac, basename)
            # массив из таких структур
            mat_comp.append(mater)

    # Normalize
    norm = 0
    for mat in mat_comp:
        norm += mat.frac
    for mat in mat_comp:
        mat.frac /= norm

    return mat_comp


def calcStoppingPower(e_alpha_MeV, mat_comp):
    # Stopping power as units of keV/(mg/cm^2) or MeV/(g/cm^2)
    e_alpha = e_alpha_MeV
    sp_total = 0
    # First, reduce the material to combine all isotopes with the same Z
    mat_comp_reduced = {}

    for mat in mat_comp:
        if mat.ele in mat_comp_reduced:
            mat_comp_reduced[mat.ele] += mat.frac
        else:
            mat_comp_reduced[mat.ele] = mat.frac

    # Then, for each element, get the stopping power at this alpha energy
    for mat in mat_comp_reduced:
        spDir = './Data/StoppingPowers/'
        spFile = spDir + mat.lower() + '.dat'
        spf = open(spFile)

        tokens = [line.split() for line in spf.readlines()]
        first = True
        sp_found = False
        e_curr = 0
        e_last = 0
        sp_curr = 0
        sp_last = 0
        sp_alpha = 0
        for line in tokens:
            if line[0][0] == '#':
                continue
            e_curr = float(line[0])
            if str(line[1]) == 'keV':
                e_curr /= 1000
            elif str(line[1]) == 'MeV':
                e_curr *= 1
            sp_curr = float(line[3])+float(line[2])

            # Alpha energy is below the list. Use the lowest energy in the list
            if e_curr > e_alpha and first:
                first = False
                sp_found = True
                sp_alpha = sp_curr
                break
            # If this entry is above the alpha energy, the alpha is between this
            # entry and the previous one
            if e_curr > e_alpha:
                first = False
                sp_alpha = old_div((sp_curr-sp_last) *
                                   (e_alpha-e_last), (e_curr-e_last)) + sp_last
                sp_found = True
                break
            # Otherwise, keep looking for the entry
            first = False
            sp_last = sp_curr
            e_last = e_curr
        # if the alpha energy is too high for the list, use the highest energy on the list
        if not sp_found:
            sp_alpha = sp_last
        sp_total += old_div(sp_alpha * mat_comp_reduced[mat], 100)
    return sp_total


def runTALYS(e_a, ele, A):
    iso = str(ele)+str(int(A))
    inpdir = isoDir(ele, A) + 'TalysInputs/'
    outdir = isoDir(ele, A) + 'TalysOut/'
    nspecdir = isoDir(ele, A) + 'NSpectra/'
    if not os.path.exists(inpdir):
        os.makedirs(inpdir)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not os.path.exists(nspecdir):
        os.makedirs(nspecdir)

#    command = '\nprojectile a\nejectiles p n g\nelement '+ele+'\nmass '+str(int(A))+'\nenergy '+str(
#       e_a)+'\npreequilibrium y\ngiantresonance y\nmultipreeq y\noutspectra y\noutlevels y\noutgamdis y\nfilespectrum n\nelwidth 0.2\n'
    command = '\nprojectile a\nejectiles p n g\nelement '+ele+'\nmass '+str(int(A))+'\nenergy '+str(
        e_a)+'\npreequilibrium y\ngiantresonance y\nmultipreeq y\noutspectra y\noutlevels y\noutgamdis y\nfilespectrum n\nelwidth 0.2'

    inp_fname = inpdir+'inputE'+str(e_a)
    inp_f = open(inp_fname, 'w')
    inp_f.write(command)
    inp_f.close()
    out_fname = outdir+'outputE'+str(e_a)

    bashcmd = 'talys < '+inp_fname+' > '+out_fname
    print('Running TALYS:\t', bashcmd, file=constants.ofile)
    runscript_fname = './runscript_temp.sh'
    runscript_f = open(runscript_fname, 'w')
    runscript_f.write('#!/usr/bin/bash\n\n'+bashcmd)
    runscript_f.close()
    process = subprocess.call(bashcmd, shell=True)
    # Move the output neutron spectrum to the appropriate directory
    ls = os.listdir('./')

    moved_file = False
    for f in ls:
        if 'nspec' in f:
            if os.path.exists(nspecdir+f):
                os.remove(nspecdir+f)
            fname = nspecdir+'nspec{0:0>7.3f}.tot'.format(e_a)
            shutil.move(f, fname)
            moved_file = True
    # If no neutron spectrum file is found, make a blank one
    if not moved_file:
        fname = nspecdir+'nspec{0:0>7.3f}.tot'.format(e_a)
        blank_f = open(fname, 'w')
        blank_f.write('EMPTY')
        blank_f.close()


def getMatTerm(mat, mat_comp):  # return N_A * C_m / A_m
    # mat_comp structure: [ele, A, frac, basename]
    # mat structure: ele, A, frac, basename
    A = mat.A
    conc = mat.frac/100.
    mat_term = old_div((constants.N_A * conc), A)
    return mat_term


def getIsotopeDifferentialNSpec(e_a, ele, A, basename):
    target = ele+str(int(A))
    # './Data/Isotopes/'+ele.capitalize()+'/'+ele.capitalize()+str(int(A))+'/'

    if basename == 'j':
        path = isoDir(ele, A) + 'JendlOut/'

        if not os.path.exists(path):    # проверка наличия данных
            print("No JENDL data for " + target + "!")
            return getIsotopeDifferentialNSpec(e_a, ele, A, "t")
        
        fname = path + "outputE" + str("{:.4f}".format(int(100*e_a)/100.))

        if not os.path.exists(fname):
            f = open(fname, "w")
            f.write("EMPTY")
            f.close()

        # Данные в файле:
        # Incident particle energy (eV) = 
        # 330000.0
        #
        #cos(theta)	E_n in lab, eV	distribution

        f = open(fname) # JendlOut/... 

        spec = {}
        tokens = [line.split() for line in f.readlines()]
        for line in tokens:  # Идём по энергиям E_out
            if len(line) < 1 or line[0] == 'EMPTY':
                break
            if line[0][0] == '#':
                continue

            # line[0] = E_n in lab, eV	
            # line[1] = distribution

            energy = int(float(line[0])*constants.MeV_to_keV)   # переводим в кэВ
            sigma = float(line[1]) * constants.mb_to_cm2 / constants.MeV_to_keV
            spec[energy] = sigma 
        return spec

        # dirLen = len([name for name in 
        #                     os.listdir("./jendl_an_xs/" + ele.capitalize() + 
        #                                '_' + str(int(A)) + '/MF6_MT50/')])  # число файлов в папке
        # AlphaEnergy = [0.]*2
        # spec = {}
        # fname = "./jendl_an_xs/" + ele.capitalize() + '_' + str(int(A)) + '/MF6_MT50/NK1_NE'
        # for i in range(dirLen): 
        #     f = open(fname + str(i)) # JENDL spectra from ENDF6-reader
        #     j = 0
        #     tokens = [line.split() for line in f.readlines()]
        #     for line in tokens:  # Идём построчно в файле
        #         if i == 0 and j == 1:
        #             AlphaEnergy[1] = float(line[0])/1000000.
        #         if j == 1:
        #             AlphaEnergy[0] = AlphaEnergy[1]
        #             AlphaEnergy[1] = float(line[0])/1000000.   # эВ в МэВ

        #         if j > 3:
        #             if (AlphaEnergy[1]>=e_a and AlphaEnergy[0]<e_a): 
        #                 NeutronEnergy = float(float(line[1])/1000.)   # переводим эВ в кэВ
        #                 table_yield = float(line[3])
        #                 spec[NeutronEnergy] = table_yield * readTotalNXsect(e_a, ele, A, basename) / (2. * 3.1415926)
        #         j += 1
        # return spec

    else:   # if basename == "t"
        path = isoDir(ele, A) + 'NSpectra/'
        if not os.path.exists(path):
            os.makedirs(path)
        fname = path+'nspec{0:0>7.3f}.tot'.format(int(100*e_a)/100.)
        # Данные в файле:
        # a +  13C : neutron  spectrum
        # E-incident =    4.230 (энергия альфы)
        #
        # energies =   135 (количество шагов по энергии E-out)
        # E-out    Total       Direct ...
        # 0.100 ...
        # 0.200 ...

        outpath = isoDir(ele, A) + 'TalysOut'
        if constants.force_recalculation:
            print('Forcibily running TALYS for', int(100*e_a)/100., 'alpha on', target, file=constants.ofile)
            print('Outpath', outpath, file=constants.ofile)
            runTALYS(int(100*e_a)/100., ele, A)

        # If the file does not exist, run TALYS
        if not os.path.exists(fname):
            if constants.run_talys:
                while not os.path.exists(fname):
                    print('Running TALYS for', int(100*e_a)/100., 'alpha on', target, file=constants.ofile)
                    print('Outpath', outpath, file=constants.ofile)
                    runTALYS(int(100*e_a)/100., ele, A)
                    ls = os.listdir(outpath)
            else:
                print('Warning, no (alpha,n) data found for E_a =', e_a, 'MeV on target', target, '...skipping. Consider running with the -d or -t options', file=constants.ofile)
                return {}

        # Load the file
        # If no output was produced, skip this energy
        if not os.path.exists(outpath):
            return {}

        f = open(fname) # NSpectra/... 

        spec = {}
        tokens = [line.split() for line in f.readlines()]
        for line in tokens:  # Идём по энергиям E_out
            if len(line) < 1 or line[0] == 'EMPTY':
                break
            if line[0][0] == '#':
                continue
            # line[0] = E-out
            # line[1] = Total
            # line[2] = Direct
            # line[3] = Pre-equil
            # line[4] = Mult. preeq
            # line[5] = Compound
            # line[6] = Pre-eq ratio
            # convert from mb/MeV to cm^2/MeV
            energy = int(float(line[0])*constants.MeV_to_keV)   # Умножаем на 1000
            sigma = old_div(float(line[1])*constants.mb_to_cm2, constants.MeV_to_keV)    # Делим на 10^30
            spec[energy] = sigma 
        return spec


def rebin(histo, step, minbin, maxbin): # histo = spec_raw
    # histo - распределение сечения нейтронов по энергии их выхода для конкретных альфы и атома
    nbins = old_div((maxbin-minbin), step)   # Количество столбцов в итоговом спектре
    newhisto = {}   #
    normhisto = {}  #
    for i in sorted(histo):  # Сортирует по энергии выхода сечения нейтронов и перебирвет их. i - значение энергии
        index = sorted(histo).index(i)  # Номер столбца в спектре. index - число
        # Get the spacing between points
        delta = sorted(histo)[0]    # изначально дельта равна самой маленькой энергии
        if index > 0:
            # Разница энергий между соседями 
            delta = sorted(histo)[index] - sorted(histo)[index-1]
        # If the x value is too low, put it in the underflow bin (-1)
        if i < minbin:
            print('Underflow:', i, ' (minbin =', minbin, ')', file=constants.ofile)
            if -1 in newhisto:
                newhisto[-1] += histo[i]*delta
                normhisto[-1] += delta
            else:
                newhisto[-1] = histo[i]*delta
                normhisto[-1] = delta
        # ...or the overflow bin if too high
        if i > maxbin:
            print('Overflow:', histo[i], ' (maxbin =', maxbin, ')', file=constants.ofile)
            overflowbin = int(nbins+10*step)
            if overflowbin in newhisto:
                newhisto[overflowbin] += histo[i]*delta
                normhisto[overflowbin] += delta
            else:
                newhisto[overflowbin] = histo[i]*delta
                normhisto[overflowbin] = delta
        # Otherwise, calculate the bin
        # Расставляет newbin вместо i на расстояниях, кратных 100кэВ
        newbin = int(minbin+(int(old_div((i-minbin), step))*step))
        if newbin in newhisto:  # newhisto - новая гистограмма, в которой столбцы стоят на расстояниях кратных delta_bin = 100keV
            # Сечение для данной энергии * на разницу сечений
            newhisto[newbin] += histo[i]*delta
            normhisto[newbin] += delta
        else:
            newhisto[newbin] = histo[i]*delta
            normhisto[newbin] = delta

    # Renormalize the new histogram
    for i in newhisto:
        if normhisto[i] > 0:
            newhisto[i] /= normhisto[i]

    return newhisto


def integrate(histo):
    integral = 0
    for i in sorted(histo):
        # Get the bin width
        delta = sorted(histo)[0]
        index = sorted(histo).index(i)
        if index > 0:
            delta = sorted(histo)[index] - sorted(histo)[index-1]

        integral += histo[i]*delta
    return integral


def readTotalNXsect(e_a, ele, A, basename): # возвращает сечение (a,n) в см2

    if basename == 'j':
        # Обычный режим
        Z = chemistry.getZ(ele)
        # fname = isoDir(ele, A) + 'JendlOut/xs_an_Z' + str(Z) + '_A' + str(int(A))+'.txt'  так должно быть (надо распихать файлы по папкам)
        fname = "./jendl_an_totalxs/xs_an_Z" + str(Z) + "_A" + str(int(A)) + ".txt" # так есть сейчас
        # fname = "./jendl_an_partialxs/xs_an_Z" + str(Z) + "_A" + str(int(A)) + ".txt" 

        if not os.path.exists(fname):   # Если нет файла Jendl
            print ("There is no JENDL data for Z=" + str(Z) + " A=" + str(int(A)))
            # print('No such Jendl file', fname, file = constants.ofile)
            basename = 't'
            return readTotalNXsect(e_a, ele, A, basename)
        
        f = open(fname)
        
        # Массив из массивов, состоящих из слов,
        lines = [line.split() for line in f.readlines()]
        # составляющих строки в файле
        sigma = 0
        for line in lines:
            if (line[0] != "#"):
                if e_a >= float(line[0]):   # Тут знак >= тк файлы jendl идут по возрастанию энергии. 
                                            # (файлы talys - по убыванию, поэтому там знак <= ) 
                    sigma = float(line[1])
        
        # Добавить проверку на случай если не зашёл в if!!! Иначе ошибка
        ''' Проверка завышенных значений выхода для jendl
        if ele == 'c' and A == 12:
            print(e_a, sigma)
        '''
        return sigma    # в см2

    else:
        fname = isoDir(ele, A) + 'TalysOut/outputE' + str(int(100*e_a)/100.)
        if not os.path.exists(fname):
            print('Could not find file', fname, file=constants.ofile)
            return 0
        f = open(fname)
        # Массив из массивов, состоящих их слов,
        lines = [line.split() for line in f.readlines()]
        # составляющих строки в файле
        xsect_line = 0
        for line in lines:  # Бежим по каждой строке, ищем строку с сечением
            if line == ['2.', 'Binary', 'non-elastic', 'cross', 'sections', '(non-exclusive)']:
                break
            else:
                xsect_line += 1

        xsect_line += 3  # Берём сечение нейтрона
        if len(lines) < xsect_line:
            return 0
        if lines[xsect_line][0] != 'neutron':
            return 0
        sigma = float(lines[xsect_line][2])  # Сечение (a,n) в мб

        

        if(ele == "c" and A == 13):     # запись полных сечений талиса в файл
            # f = open('tmp_file_TALYS_totXS', 'w')
            # f.close()
            f = open("tmp_file_TALYS_totXS", "a")
            # f.seek(0)
            f.write(str("{0:.2f}".format(int(100*e_a)/100.)) + "\t\t" + str(sigma) + "\n")
            f.close()



        sigma *= constants.mb_to_cm2

        return sigma


def condense_alpha_list(alpha_list, alpha_step_size):
    # alpha_list - список энергий альфа-частиц с вероятностью встретить конкретную в цепочке распада
    # alpha_step_size = шаг по энергии
    alpha_ene_cdf = []
    # Самая большая энергия распада + её вероятность
    max_alpha = max(alpha_list)
    e_a_max = int(max_alpha[0]*100 + 0.5)/100.  # Округляет энергию альфы. Можно сделать через floor
    alpha_ene_cdf.append([e_a_max, max_alpha[1]]) # записывает округлённую максимальную энергию альфы и её вероятность
    e_a = e_a_max
    while e_a > 0:  # Функция суммирует для каждого e_a все вероятности, которые соответсвуют энергиям,
        # меньшим чем e_a. e_a - бегунок от максимальной энергии до нуля.
        cum_int = 0
        for alpha in alpha_list:
            this_e_a = int(alpha[0]*100+0.5)/100.   # Округляет конкретную энергию альфы
            if this_e_a >= e_a:
                cum_int += alpha[1] # cumulated_intensity
        alpha_ene_cdf.append([e_a, cum_int])
        e_a -= alpha_step_size
    return alpha_ene_cdf


def run_alpha(alpha_list, mat_comp, e_alpha_step):
    # alpha_list - список энергий альфачастиц с вероятностью встретить конкретную в цепочке распада
    # mat_comp - Список из структур из названия элемента, его массы, и масоовой доли в веществе
    # e_alpha_step - ширина шага спектра (по энергии) == 0,01 МэВ по умолчанию

    binsize = 0.1   # Bin size for output spectrum, MeV

    spec_tot = {}   # объект типа dictonary # Спектр интегральный
    xsects = {}     # объект типа dictonary # Сечение реакции(?)
    total_xsect = 0
    counter = 0
    # Рассчёт просуммированной функции распределения вероятностей альф по энергиям
    alpha_ene_cdf = condense_alpha_list(alpha_list, e_alpha_step)                                                  
    stopping_power = 0

    for [e_a, intensity] in alpha_ene_cdf:  # Перебор по энергии альфы (заодно сообщается intensity = P_a)
        counter += 1
        if counter % (int(old_div(len(alpha_ene_cdf), 100))) == 0:
            sys.stdout.write('\r')
            sys.stdout.write('[%-100s] %d%%' % ('='*int(old_div(counter*100, len(alpha_ene_cdf))), 
                                                old_div(100*counter, len(alpha_ene_cdf))))
            sys.stdout.flush()
        
        stopping_power = calcStoppingPower(e_a, mat_comp)   # ksi(E_a)

        for mat in mat_comp:    # перебираем разные материалы (Summ by m)
            
            # запись данных talys в формате jendl для дальнейшей проверки
            #
            #  sigma = readTotalNXsect(e_a, mat.ele, mat.A, mat.basename)
            # Z = chemistry.getZ(mat.ele)
            # fname = './Data/check/xs_an_Z' + \
            #     str(Z) + '_A' + str(int(mat.A))+'.txt'
            # ch = open(fname, 'a')
            # ch.write(str(e_a)+ '\t'+str(sigma)+'\n')
            
            # коэффициент перед интегралом по энергии = N_A * C_m / A_m
            mat_term = getMatTerm(mat, mat_comp)
            
            # Get alpha-n spectrum for current alpha and current target
            # Распределение сечения нейтронов по энергии.
            spec_raw = getIsotopeDifferentialNSpec(e_a, mat.ele, mat.A, mat.basename)
            # print (spec_raw)
            # Для конкретной альфы и конкретного атома
            spec = rebin(spec_raw, constants.delta_bin, constants.min_bin, constants.max_bin)
            # Add this spectrum to the total spectrum
            delta_ea = e_alpha_step
            if e_a - e_alpha_step < 0:
                delta_ea = e_a

            # подынтегральное выражение
            prefactors = old_div((intensity/100.) * mat_term * delta_ea, stopping_power)

            # Значение просуммированного спектра (без вычисления интеграла)
            xsect = prefactors * readTotalNXsect(e_a, mat.ele, mat.A, mat.basename) # cm^2

            #print (e_a,mat.ele,mat.A)
            total_xsect += xsect
            matname = str(mat.ele)+str(int(mat.A))
            if matname in xsects:
                xsects[matname] += xsect
            else:
                xsects[matname] = xsect

            for e in spec:
                val = prefactors * spec[e]
                if e in spec_tot:
                    spec_tot[e] += val
                else:
                    spec_tot[e] = val


    sys.stdout.write('\r')
    sys.stdout.write('[%-100s] %d%%' % ('='*int(old_div((counter*100),
                     len(alpha_ene_cdf))), old_div(100*(counter+1), len(alpha_ene_cdf))))
    sys.stdout.flush()
    print('', file=sys.stdout)
    # print out total spectrum
    newspec = spec_tot
    print('', file=constants.ofile)
    print('# Total neutron yield =', total_xsect, ' n/decay', file=constants.ofile)
    for x in sorted(xsects):
        print('\t', x, xsects[x], file=constants.ofile)

    print('# Integral of spectrum =', integrate(newspec), ' n/decay', file=constants.ofile)
    for e in sorted(newspec):
        print(e, newspec[e], file=constants.ofile)

    # График
    # hist()
    
    #fig, ax = plt.subplots()

    #ax.hist(newspec, bins=250, linewidth=0.5, edgecolor="white")

    #fig = plt.figure()
    # plt.hist(newspec)
    #plt.title('Simple histogramm')
    # plt.grid(True)
    #save('pic.png')


def help_message():
    print('Usage: You must specify an alpha list or decay chain file and a target material file.\n\
          You may also specify a step size to for integrating the alphas as they slow down in MeV; the default value is 0.01 MeV\n\
          \t-l [alpha list file name]\n\
          \t-c [decay chain file name]\n\
          \t-m [material composition file name]\n\
          \t-s [alpha step size in MeV]\n\
          \t-t (to run TALYS for reactions not in libraries)\n\
          \t-d (download isotopic data for isotopes missing from database; default behavior is v2)\n\
          \t\t-d v1 (use V1 database, TALYS-1.6)\n\
          \t-d v2 (use V2 database, TALYS-1.95)\n\
          \t-o [output file name]', file=sys.stdout)


def main():
    alpha_list = []
    mat_comp = []
    alpha_step_size = 0.01  # 0.01 MeV (default value)
    # Load arguments
    #argv = ['neucbot.py', '-m', 'Materials/Acrylic.dat', '-c', 'Chains/Th232Chain.dat']
    for arg in sys.argv:
        # for arg in argv:
        if arg == '-l':
            alphalist_file = sys.argv[sys.argv.index(arg)+1]
            print('load alpha list', alphalist_file, file=sys.stdout)
            alpha_list = loadAlphaList(alphalist_file)

        if arg == '-c': 
            '''mat_file = sys.argv[sys.argv.index('-m')+1]
            mat_comp = readTargetMaterial(mat_file)
            if mat_comp[1] == 'j':
                continue'''
            chain_file = sys.argv[sys.argv.index(arg)+1]
            # chain_file = argv[argv.index(arg)+1]    # example: chain_file = Chains/Th232Chain.dat
            print('load alpha chain', chain_file, file=sys.stdout)
            # Подгружает цепочку энергий распада
            alpha_list = loadChainAlphaList(chain_file)
            #print(alpha_list, '\n')

        if arg == '-m': 
            mat_file = sys.argv[sys.argv.index(arg)+1]
            # mat_file = argv[argv.index(arg)+1]  # example: mat_file = Materials/Acrylic.dat
            print('load target material', mat_file, file=sys.stdout)
            mat_comp = readTargetMaterial(mat_file)
            # Выдаёт писок из структур из названия элемента, его массы, и масоовой доли в веществе

        if arg == '-s':
            alpha_step_size = float(sys.argv[sys.argv.index(arg)+1])
            print('step size now is', alpha_step_size, file=sys.stdout)
        if arg == '-h':
            help_message()
            return 0
        if arg == '-t':
            constants.run_talys = True
        if arg == '-d':
            constants.download_data = True
            constants.download_version = 2
            version_choice = sys.argv[sys.argv.index(arg)+1]
            if (not version_choice[0] == '-') and (version_choice[0].lower() == 'v'):
                version_num = int(version_choice[1])
                constants.download_version = version_num
                print('Downloading data from version', version_num)
        if arg == '--print-alphas':
            constants.print_alphas = True
        if arg == '--print-alphas-only':
            print('Only printing alphas', file=sys.stdout)
            constants.print_alphas = True
            constants.run_alphas = False
        if arg == '--force-recalculation':
            constants.force_recalculation = True
        if arg == '-o':
            ofile = str(sys.argv[sys.argv.index(arg)+1])
            print('Printing output to', ofile, file=sys.stdout)
            constants.ofile = open(ofile, 'w')
            #sys.stdout = open(ofile,'w')

    if len(alpha_list) == 0 or len(mat_comp) == 0:
        if len(alpha_list) == 0:
            print('No alpha list or chain specified', file=sys.stdout)
        if len(mat_comp) == 0:
            print('No target material specified', file=sys.stdout)
        print('', file=sys.stdout)
        help_message()
        return 0

    if constants.print_alphas:
        print('Alpha List:', file=sys.stdout)
        print(max(alpha_list), file=sys.stdout)
        condense_alpha_list(alpha_list, alpha_step_size)
        for alph in alpha_list:
            print(alph[0], '&', alph[1], '\\\\', file=sys.stdout)

    if constants.download_data:
        for mat in mat_comp:
            ele = mat.ele
            basename = mat.basename
            if basename == 't':
                with open(r"./Data/routes.txt", "r") as file:
                    #   if not os.path.exists('Talys'+file.readlines()[14].rstrip()+ele.capitalize()):
                    #   надо бы написать чтобы загрузка шла в папку с 'talys' в названии
                    if not os.path.exists(file.readlines()[14].rstrip()+ele.capitalize()):
                        if constants.download_version == 2:
                            print('\tDownloading (datset V2) data for', ele, file=sys.stdout)
                            bashcmd = './Scripts/download_element.sh ' + ele
                            process = subprocess.call(bashcmd, shell=True)
                        elif constants.download_version == 1:
                            print('\tDownloading (dataset V1) data for', ele, file=sys.stdout)
                            bashcmd = './Scripts/download_element_v1.sh ' + ele
                            process = subprocess.call(bashcmd, shell=True)
            else:
                with open(r"./Data/routes.txt", "r") as file:
                    #   надо бы написать чтобы загрузка шла в папку с 'talys' в названии
                    if not os.path.exists('jendl'+file.readlines()[14].rstrip()+ele.capitalize()):
                        print('ERROR: there is no folder for jendl')
                        '''
                        if constants.download_version == 2:
                            print('\tDownloading (datset V2) data for',ele, file = sys.stdout)
                            bashcmd = './Scripts/download_element.sh ' + ele
                            process = subprocess.call(bashcmd,shell=True)
                        elif constants.download_version == 1:
                            print('\tDownloading (dataset V1) data for',ele, file = sys.stdout)
                            bashcmd = './Scripts/download_element_v1.sh ' + ele
                            process = subprocess.call(bashcmd,shell=True)
                            '''

    if constants.run_alphas:
        print('Running alphas:', file=sys.stdout)
        run_alpha(alpha_list, mat_comp, alpha_step_size)
        # alpha_list - цепочка энергий распада
        # mat_comp - Список из структур из названия элемента, его массы, и масоовой доли в веществе
        # alpha_step_size - ширина шага спектра (по энергии) == 0,01 МэВ по умолчанию


if __name__ == '__main__':
    main()
