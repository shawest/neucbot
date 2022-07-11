# Massive submission of the neucbot jobs
# for evaluation of the DarkSide neutron budget
# NeuCBOT + TALYS-1.95

# Author: Gromov Maxim <gromov@physics.msu.ru>
# Maintainer: Gromov Maxim
# Last update: 30.06.2022
# Version: 1.90

#!/bin/bash

echo "Start!"

# Acrylic donchamp

# 232Th

#nohup ./neucbot.py -t -m Materials/Acrylic.dat -c Chains/Th232Chain.dat -o Acrylic_neucbot_talys_1-95_232Th.txt > Acrylic_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -t -m Materials/Acrylic.dat -c Chains/U235Chain.dat -o Acrylic_neucbot_talys_1-95_235U.txt > Acrylic_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -t -m Materials/Acrylic.dat -c Chains/Pb210Chain.dat -o Acrylic_neucbot_talys_1-95_238Ulower.txt > Acrylic_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -t -m Materials/Acrylic.dat -c Chains/U238middleChain_SaG4n.dat -o Acrylic_neucbot_talys_1-95_238Umiddle.txt > Acrylic_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -t -m Materials/Acrylic.dat -c Chains/U238upperChain.dat -o Acrylic_neucbot_talys_1-95_238Uupper.txt > Acrylic_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# python3 ./neucbot.py -m Materials/Al -c Chains/Th232Chain.dat -o Al_neucbot_jendl_Th232.txt > Al_neucbot_jendl_Th232.out &

# python3 ./neucbot.py -m Materials/Al -c Chains/U235Chain.dat -o Al_neucbot_jendl_U235.txt > Al_neucbot_jendl_U235.out &

# python3 ./neucbot.py -m Materials/Al -c Chains/U238lowerChain.dat -o Al_neucbot_jendl_U238lower.txt > Al_neucbot_jendl_U238lower.out &

# python3 ./neucbot.py -m Materials/Al -c Chains/U238upperChain.dat -o Al_neucbot_jendl_U238upper.txt > Al_neucbot_jendl_U238upper.out &

# python3 ./neucbot.py -m Materials/Al -c Chains/U238middleChain_SaG4n.dat -o Al_neucbot_jendl_U238middle.txt > Al_neucbot_jendl_U238middle.out &


# python3 ./neucbot.py -m Materials/Al2O3 -c Chains/Th232Chain.dat -o Al2O3_neucbot_jendl_Th232.txt > Al2O3_neucbot_jendl_Th232.out &

# python3 ./neucbot.py -m Materials/Al2O3 -c Chains/U235Chain.dat -o Al2O3_neucbot_jendl_U235.txt > Al2O3_neucbot_jendl_U235.out &

# python3 ./neucbot.py -m Materials/Al2O3 -c Chains/U238lowerChain.dat -o Al2O3_neucbot_jendl_U238lower.txt > Al2O3_neucbot_jendl_U238lower.out &

# python3 ./neucbot.py -m Materials/Al2O3 -c Chains/U238upperChain.dat -o Al2O3_neucbot_jendl_U238upper.txt > Al2O3_neucbot_jendl_U238upper.out &

# python3 ./neucbot.py -m Materials/Al2O3 -c Chains/U238middleChain_SaG4n.dat -o Al2O3_neucbot_jendl_U238middle.txt > Al2O3_neucbot_jendl_U238middle.out &


# python3 ./neucbot.py -m Materials/B -c Chains/Th232Chain.dat -o B_neucbot_jendl_Th232.txt > B_neucbot_jendl_Th232.out &

# python3 ./neucbot.py -m Materials/B -c Chains/U235Chain.dat -o B_neucbot_jendl_U235.txt > B_neucbot_jendl_U235.out &

# python3 ./neucbot.py -m Materials/B -c Chains/U238lowerChain.dat -o B_neucbot_jendl_U238lower.txt > B_neucbot_jendl_U238lower.out &

# python3 ./neucbot.py -m Materials/B -c Chains/U238upperChain.dat -o B_neucbot_jendl_U238upper.txt > B_neucbot_jendl_U238upper.out &

# python3 ./neucbot.py -m Materials/B -c Chains/U238middleChain_SaG4n.dat -o B_neucbot_jendl_U238middle.txt > B_neucbot_jendl_U238middle.out &


# python3 ./neucbot.py -m Materials/Be -c Chains/Th232Chain.dat -o Be_neucbot_jendl_Th232.txt > Be_neucbot_jendl_Th232.out &

# python3 ./neucbot.py -m Materials/Be -c Chains/U235Chain.dat -o Be_neucbot_jendl_U235.txt > Be_neucbot_jendl_U235.out &

# python3 ./neucbot.py -m Materials/Be -c Chains/U238lowerChain.dat -o Be_neucbot_jendl_U238lower.txt > Be_neucbot_jendl_U238lower.out &

# python3 ./neucbot.py -m Materials/Be -c Chains/U238upperChain.dat -o Be_neucbot_jendl_U238upper.txt > Be_neucbot_jendl_U238upper.out &

# python3 ./neucbot.py -m Materials/Be -c Chains/U238middleChain_SaG4n.dat -o Be_neucbot_jendl_U238middle.txt > Be_neucbot_jendl_U238middle.out &


python3 ./neucbot.py -m Materials/BeO -c Chains/Th232Chain.dat -o BeO_neucbot_jendl_Th232.txt > BeO_neucbot_jendl_Th232.out &

python3 ./neucbot.py -m Materials/BeO -c Chains/U235Chain.dat -o BeO_neucbot_jendl_U235.txt > BeO_neucbot_jendl_U235.out &

python3 ./neucbot.py -m Materials/BeO -c Chains/U238lowerChain.dat -o BeO_neucbot_jendl_U238lower.txt > BeO_neucbot_jendl_U238lower.out &

python3 ./neucbot.py -m Materials/BeO -c Chains/U238upperChain.dat -o BeO_neucbot_jendl_U238upper.txt > BeO_neucbot_jendl_U238upper.out &

python3 ./neucbot.py -m Materials/BeO -c Chains/U238middleChain_SaG4n.dat -o BeO_neucbot_jendl_U238middle.txt > BeO_neucbot_jendl_U238middle.out &


python3 ./neucbot.py -m Materials/C -c Chains/Th232Chain.dat -o C_neucbot_jendl_Th232.txt > C_neucbot_jendl_Th232.out &

python3 ./neucbot.py -m Materials/C -c Chains/U235Chain.dat -o C_neucbot_jendl_U235.txt > C_neucbot_jendl_U235.out &

python3 ./neucbot.py -m Materials/C -c Chains/U238lowerChain.dat -o C_neucbot_jendl_U238lower.txt > C_neucbot_jendl_U238lower.out &

python3 ./neucbot.py -m Materials/C -c Chains/U238upperChain.dat -o C_neucbot_jendl_U238upper.txt > C_neucbot_jendl_U238upper.out &

python3 ./neucbot.py -m Materials/C -c Chains/U238middleChain_SaG4n.dat -o C_neucbot_jendl_U238middle.txt > C_neucbot_jendl_U238middle.out &


python3 ./neucbot.py -m Materials/Li -c Chains/Th232Chain.dat -o Li_neucbot_jendl_Th232.txt > Li_neucbot_jendl_Th232.out &

python3 ./neucbot.py -m Materials/Li -c Chains/U235Chain.dat -o Li_neucbot_jendl_U235.txt > Li_neucbot_jendl_U235.out &

python3 ./neucbot.py -m Materials/Li -c Chains/U238lowerChain.dat -o Li_neucbot_jendl_U238lower.txt > Li_neucbot_jendl_U238lower.out &

python3 ./neucbot.py -m Materials/Li -c Chains/U238upperChain.dat -o Li_neucbot_jendl_U238upper.txt > Li_neucbot_jendl_U238upper.out &

python3 ./neucbot.py -m Materials/Li -c Chains/U238middleChain_SaG4n.dat -o Li_neucbot_jendl_U238middle.txt > Li_neucbot_jendl_U238middle.out &


python3 ./neucbot.py -m Materials/Na2CO3 -c Chains/Th232Chain.dat -o Na2CO3_neucbot_jendl_Th232.txt > Na2CO3_neucbot_jendl_Th232.out &

python3 ./neucbot.py -m Materials/Na2CO3 -c Chains/U235Chain.dat -o Na2CO3_neucbot_jendl_U235.txt > Na2CO3_neucbot_jendl_U235.out &

python3 ./neucbot.py -m Materials/Na2CO3 -c Chains/U238lowerChain.dat -o Na2CO3_neucbot_jendl_U238lower.txt > Na2CO3_neucbot_jendl_U238lower.out &

python3 ./neucbot.py -m Materials/Na2CO3 -c Chains/U238upperChain.dat -o Na2CO3_neucbot_jendl_U238upper.txt > Na2CO3_neucbot_jendl_U238upper.out &

python3 ./neucbot.py -m Materials/Na2CO3 -c Chains/U238middleChain_SaG4n.dat -o Na2CO3_neucbot_jendl_U238middle.txt > Na2CO3_neucbot_jendl_U238middle.out &


python3 ./neucbot.py -m Materials/NaF -c Chains/Th232Chain.dat -o NaF_neucbot_jendl_Th232.txt > NaF_neucbot_jendl_Th232.out &

python3 ./neucbot.py -m Materials/NaF -c Chains/U235Chain.dat -o NaF_neucbot_jendl_U235.txt > NaF_neucbot_jendl_U235.out &

python3 ./neucbot.py -m Materials/NaF -c Chains/U238lowerChain.dat -o NaF_neucbot_jendl_U238lower.txt > NaF_neucbot_jendl_U238lower.out &

python3 ./neucbot.py -m Materials/NaF -c Chains/U238upperChain.dat -o NaF_neucbot_jendl_U238upper.txt > NaF_neucbot_jendl_U238upper.out &

python3 ./neucbot.py -m Materials/NaF -c Chains/U238middleChain_SaG4n.dat -o NaF_neucbot_jendl_U238middle.txt > NaF_neucbot_jendl_U238middle.out &


python3 ./neucbot.py -m Materials/Si -c Chains/Th232Chain.dat -o Si_neucbot_jendl_Th232.txt > Si_neucbot_jendl_Th232.out &

python3 ./neucbot.py -m Materials/Si -c Chains/U235Chain.dat -o Si_neucbot_jendl_U235.txt > Si_neucbot_jendl_U235.out &

python3 ./neucbot.py -m Materials/Si -c Chains/U238lowerChain.dat -o Si_neucbot_jendl_U238lower.txt > Si_neucbot_jendl_U238lower.out &

python3 ./neucbot.py -m Materials/Si -c Chains/U238upperChain.dat -o Si_neucbot_jendl_U238upper.txt > Si_neucbot_jendl_U238upper.out &

python3 ./neucbot.py -m Materials/Si -c Chains/U238middleChain_SaG4n.dat -o Si_neucbot_jendl_U238middle.txt > Si_neucbot_jendl_U238middle.out &


python3 ./neucbot.py -m Materials/SiO2 -c Chains/Th232Chain.dat -o SiO2_neucbot_jendl_Th232.txt > SiO2_neucbot_jendl_Th232.out &

python3 ./neucbot.py -m Materials/SiO2 -c Chains/U235Chain.dat -o SiO2_neucbot_jendl_U235.txt > SiO2_neucbot_jendl_U235.out &

python3 ./neucbot.py -m Materials/SiO2 -c Chains/U238lowerChain.dat -o SiO2_neucbot_jendl_U238lower.txt > SiO2_neucbot_jendl_U238lower.out &

python3 ./neucbot.py -m Materials/SiO2 -c Chains/U238upperChain.dat -o SiO2_neucbot_jendl_U238upper.txt > SiO2_neucbot_jendl_U238upper.out &

python3 ./neucbot.py -m Materials/SiO2 -c Chains/U238middleChain_SaG4n.dat -o SiO2_neucbot_jendl_U238middle.txt > SiO2_neucbot_jendl_U238middle.out &

#=======================================================================

# 235U

#nohup ./neucbot.py -t -m Materials/Acrylic.dat -c Chains/U235Chain.dat -o Acrylic_neucbot_talys_1-95_235U.txt > Acrylic_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -t -m Materials/Acrylic.dat -c Chains/Pb210Chain.dat -o Acrylic_neucbot_talys_1-95_238Ulower.txt > Acrylic_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -t -m Materials/Acrylic.dat -c Chains/U238middleChain_SaG4n.dat -o Acrylic_neucbot_talys_1-95_238Umiddle.txt > Acrylic_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -t -m Materials/Acrylic.dat -c Chains/U238upperChain.dat -o Acrylic_neucbot_talys_1-95_238Uupper.txt > Acrylic_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Arlon 55NT

# 232Th

#nohup ./neucbot.py -t -m Materials/Arlon_55NT.dat -c Chains/Th232Chain.dat -o Arlon_55NT_neucbot_talys_1-95_232Th.txt > Arlon_55NT_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -t -m Materials/Arlon_55NT.dat -c Chains/U235Chain.dat -o Arlon_55NT_neucbot_talys_1-95_235U.txt > Arlon_55NT_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -t -m Materials/Arlon_55NT.dat -c Chains/Pb210Chain.dat -o Arlon_55NT_neucbot_talys_1-95_238Ulower.txt > Arlon_55NT_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -t -m Materials/Arlon_55NT.dat -c Chains/U238middleChain_SaG4n.dat -o Arlon_55NT_neucbot_talys_1-95_238Umiddle.txt > Arlon_55NT_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -t -m Materials/Arlon_55NT.dat -c Chains/U238upperChain.dat -o Arlon_55NT_neucbot_talys_1-95_238Uupper.txt > Arlon_55NT_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# PEEK fiber

# 232Th

#nohup ./neucbot.py -t -m Materials/PEEK_fiber.dat -c Chains/Th232Chain.dat -o PEEK_fiber_neucbot_talys_1-95_232Th.txt > PEEK_fiber_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -t -m Materials/PEEK_fiber.dat -c Chains/U235Chain.dat -o PEEK_fiber_neucbot_talys_1-95_235U.txt > PEEK_fiber_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -t -m Materials/PEEK_fiber.dat -c Chains/Pb210Chain.dat -o PEEK_fiber_neucbot_talys_1-95_238Ulower.txt > PEEK_fiber_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -t -m Materials/PEEK_fiber.dat -c Chains/U238middleChain_SaG4n.dat -o PEEK_fiber_neucbot_talys_1-95_238Umiddle.txt > PEEK_fiber_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -t -m Materials/PEEK_fiber.dat -c Chains/U238upperChain.dat -o PEEK_fiber_neucbot_talys_1-95_238Uupper.txt > PEEK_fiber_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# PPS

# 232Th

#nohup ./neucbot.py -t -m Materials/PPS.dat -c Chains/Th232Chain.dat -o PPS_neucbot_talys_1-95_232Th.txt > PPS_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -t -m Materials/PPS.dat -c Chains/U235Chain.dat -o PPS_neucbot_talys_1-95_235U.txt > PPS_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -t -m Materials/PPS.dat -c Chains/Pb210Chain.dat -o PPS_neucbot_talys_1-95_238Ulower.txt > PPS_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -t -m Materials/PPS.dat -c Chains/U238middleChain_SaG4n.dat -o PPS_neucbot_talys_1-95_238Umiddle.txt > PPS_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -t -m Materials/PPS.dat -c Chains/U238upperChain.dat -o PPS_neucbot_talys_1-95_238Uupper.txt > PPS_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Gd2O3 + Acrylic

# 232Th

#nohup ./neucbot.py -t -m Materials/Gd2O3_acrylic.dat -c Chains/Th232Chain.dat -o Gd2O3_acrylic_neucbot_talys_1-95_232Th.txt > Gd2O3_acrylic_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -t -m Materials/Gd2O3_acrylic.dat -c Chains/U235Chain.dat -o Gd2O3_acrylic_neucbot_talys_1-95_235U.txt > Gd2O3_acrylic_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -t -m Materials/Gd2O3_acrylic.dat -c Chains/Pb210Chain.dat -o Gd2O3_acrylic_neucbot_talys_1-95_238Ulower.txt > Gd2O3_acrylic_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -t -m Materials/Gd2O3_acrylic.dat -c Chains/U238middleChain_SaG4n.dat -o Gd2O3_acrylic_neucbot_talys_1-95_238Umiddle.txt > Gd2O3_acrylic_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -t -m Materials/Gd2O3_acrylic.dat -c Chains/U238upperChain.dat -o Gd2O3_acrylic_neucbot_talys_1-95_238Uupper.txt > Gd2O3_acrylic_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# PEN

# 232Th

#nohup ./neucbot.py -t -m Materials/PEN.dat -c Chains/Th232Chain.dat -o PEN_neucbot_talys_1-95_232Th.txt > PEN_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -t -m Materials/PEN.dat -c Chains/U235Chain.dat -o PEN_neucbot_talys_1-95_235U.txt > PEN_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -t -m Materials/PEN.dat -c Chains/Pb210Chain.dat -o PEN_neucbot_talys_1-95_238Ulower.txt > PEN_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -t -m Materials/PEN.dat -c Chains/U238middleChain_SaG4n.dat -o PEN_neucbot_talys_1-95_238Umiddle.txt > PEN_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -t -m Materials/PEN.dat -c Chains/U238upperChain.dat -o PEN_neucbot_talys_1-95_238Uupper.txt > PEN_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Cu Luvata

# 232Th

#nohup ./neucbot.py -t -m Materials/Cu_Luvata.dat -c Chains/Th232Chain.dat -o Cu_Luvata_neucbot_talys_1-95_232Th.txt > Cu_Luvata_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -t -m Materials/Cu_Luvata.dat -c Chains/U235Chain.dat -o Cu_Luvata_neucbot_talys_1-95_235U.txt > Cu_Luvata_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -t -m Materials/Cu_Luvata.dat -c Chains/Pb210Chain.dat -o Cu_Luvata_neucbot_talys_1-95_238Ulower.txt > Cu_Luvata_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -t -m Materials/Cu_Luvata.dat -c Chains/U238middleChain_SaG4n.dat -o Cu_Luvata_neucbot_talys_1-95_238Umiddle.txt > Cu_Luvata_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -t -m Materials/Cu_Luvata.dat -c Chains/U238upperChain.dat -o Cu_Luvata_neucbot_talys_1-95_238Uupper.txt > Cu_Luvata_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Nylon 66

# 232Th

#nohup ./neucbot.py -t -m Materials/Nylon_66.dat -c Chains/Th232Chain.dat -o Nylon_66_neucbot_talys_1-95_232Th.txt > Nylon_66_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -t -m Materials/Nylon_66.dat -c Chains/U235Chain.dat -o Nylon_66_neucbot_talys_1-95_235U.txt > Nylon_66_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -t -m Materials/Nylon_66.dat -c Chains/Pb210Chain.dat -o Nylon_66_neucbot_talys_1-95_238Ulower.txt > Nylon_66_neucbot_talys_1-95_238Ulower.out &

# 238Umidfellowship

#nohup ./neucbot.py -t -m Materials/Nylon_66.dat -c Chains/U238middleChain_SaG4n.dat -o Nylon_66_neucbot_talys_1-95_238Umiddle.txt > Nylon_66_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -t -m Materials/Nylon_66.dat -c Chains/U238upperChain.dat -o Nylon_66_neucbot_talys_1-95_238Uupper.txt > Nylon_66_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Stainless Steel AISI 318 LN

# 232Th

#nohup ./neucbot.py -t -m Materials/Stainless_steel_AISI_318_LN.dat -c Chains/Th232Chain.dat -o Stainless_steel_AISI_318_LN_neucbot_talys_1-95_232Th.txt > Stainless_steel_AISI_318_LN_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -t -m Materials/Stainless_steel_AISI_318_LN.dat -c Chains/U235Chain.dat -o Stainless_steel_AISI_318_LN_neucbot_talys_1-95_235U.txt > Stainless_steel_AISI_318_LN_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -t -m Materials/Stainless_steel_AISI_318_LN.dat -c Chains/Pb210Chain.dat -o Stainless_steel_AISI_318_LN_neucbot_talys_1-95_238Ulower.txt > Stainless_steel_AISI_318_LN_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -t -m Materials/Stainless_steel_AISI_318_LN.dat -c Chains/U238middleChain_SaG4n.dat -o Stainless_steel_AISI_318_LN_neucbot_talys_1-95_238Umiddle.txt > Stainless_steel_AISI_318_LN_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -t -m Materials/Stainless_steel_AISI_318_LN.dat -c Chains/U238upperChain.dat -o Stainless_steel_AISI_318_LN_neucbot_talys_1-95_238Uupper.txt > Stainless_steel_AISI_318_LN_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# LAr

# 232Th

#nohup ./neucbot.py -t -m Materials/LAr.dat -c Chains/Th232Chain.dat -o LAr_neucbot_talys_1-95_232Th.txt > LAr_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -t -m Materials/LAr.dat -c Chains/U235Chain.dat -o LAr_neucbot_talys_1-95_235U.txt > LAr_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -t -m Materials/LAr.dat -c Chains/Pb210Chain.dat -o LAr_neucbot_talys_1-95_238Ulower.txt > LAr_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -t -m Materials/LAr.dat -c Chains/U238middleChain_SaG4n.dat -o LAr_neucbot_talys_1-95_238Umiddle.txt > LAr_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -t -m Materials/LAr.dat -c Chains/U238upperChain.dat -o LAr_neucbot_talys_1-95_238Uupper.txt > LAr_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# VT1-00

# 232Th

#nohup ./neucbot.py -t -m Materials/VT1-00.dat -c Chains/Th232Chain.dat -o VT1-00_neucbot_talys_1-95_232Th.txt > VT1-00_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -t -m Materials/VT1-00.dat -c Chains/U235Chain.dat -o VT1-00_neucbot_talys_1-95_235U.txt > VT1-00_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -t -m Materials/VT1-00.dat -c Chains/Pb210Chain.dat -o VT1-00_neucbot_talys_1-95_238Ulower.txt > VT1-00_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -t -m Materials/VT1-00.dat -c Chains/U238middleChain_SaG4n.dat -o VT1-00_neucbot_talys_1-95_238Umiddle.txt > VT1-00_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -t -m Materials/VT1-00.dat -c Chains/U238upperChain.dat -o VT1-00_neucbot_talys_1-95_238Uupper.txt > VT1-00_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# VT1-0

# 232Th

#nohup ./neucbot.py -m Materials/VT1-0.dat -c Chains/Th232Chain.dat -o VT1-0_neucbot_talys_1-95_232Th.txt > VT1-0_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/VT1-0.dat -c Chains/U235Chain.dat -o VT1-0_neucbot_talys_1-95_235U.txt > VT1-0_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/VT1-0.dat -c Chains/Pb210Chain.dat -o VT1-0_neucbot_talys_1-95_238Ulower.txt > VT1-0_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/VT1-0.dat -c Chains/U238middleChain_SaG4n.dat -o VT1-0_neucbot_talys_1-95_238Umiddle.txt > VT1-0_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/VT1-0.dat -c Chains/U238upperChain.dat -o VT1-0_neucbot_talys_1-95_238Uupper.txt > VT1-0_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Ti

# 232Th

#nohup ./neucbot.py -m Materials/Ti.dat -c Chains/Th232Chain.dat -o Ti_neucbot_talys_1-95_232Th.txt > Ti_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/Ti.dat -c Chains/U235Chain.dat -o Ti_neucbot_talys_1-95_235U.txt > Ti_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/Ti.dat -c Chains/Pb210Chain.dat -o Ti_neucbot_talys_1-95_238Ulower.txt > Ti_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/Ti.dat -c Chains/U238middleChain_SaG4n.dat -o Ti_neucbot_talys_1-95_238Umiddle.txt > Ti_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/Ti.dat -c Chains/U238upperChain.dat -o Ti_neucbot_talys_1-95_238Uupper.txt > Ti_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Cu20Ti80

# 232Th

#nohup ./neucbot.py -m Materials/Cu20Ti80.dat -c Chains/Th232Chain.dat -o Cu20Ti80_neucbot_talys_1-95_232Th.txt > Cu20Ti80_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/Cu20Ti80.dat -c Chains/U235Chain.dat -o Cu20Ti80_neucbot_talys_1-95_235U.txt > Cu20Ti80_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/Cu20Ti80.dat -c Chains/Pb210Chain.dat -o Cu20Ti80_neucbot_talys_1-95_238Ulower.txt > Cu20Ti80_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/Cu20Ti80.dat -c Chains/U238middleChain_SaG4n.dat -o Cu20Ti80_neucbot_talys_1-95_238Umiddle.txt > Cu20Ti80_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/Cu20Ti80.dat -c Chains/U238upperChain.dat -o Cu20Ti80_neucbot_talys_1-95_238Uupper.txt > Cu20Ti80_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# SS 08X18H10T

# 232Th

#nohup ./neucbot.py -m Materials/SS_08X18H10T.dat -c Chains/Th232Chain.dat -o SS_08X18H10T_neucbot_talys_1-95_232Th.txt > SS_08X18H10T_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/SS_08X18H10T.dat -c Chains/U235Chain.dat -o SS_08X18H10T_neucbot_talys_1-95_235U.txt > SS_08X18H10T_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/SS_08X18H10T.dat -c Chains/Pb210Chain.dat -o SS_08X18H10T_neucbot_talys_1-95_238Ulower.txt > SS_08X18H10T_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/SS_08X18H10T.dat -c Chains/U238middleChain_SaG4n.dat -o SS_08X18H10T_neucbot_talys_1-95_238Umiddle.txt > SS_08X18H10T_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/SS_08X18H10T.dat -c Chains/U238upperChain.dat -o SS_08X18H10T_neucbot_talys_1-95_238Uupper.txt > SS_08X18H10T_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

#Teflon

# 232Th

#nohup ./neucbot.py -m Materials/Teflon.dat -c Chains/Th232Chain.dat -o Teflon_neucbot_talys_1-95_232Th.txt > Teflon_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/Teflon.dat -c Chains/U235Chain.dat -o Teflon_neucbot_talys_1-95_235U.txt > Teflon_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/Teflon.dat -c Chains/Pb210Chain.dat -o Teflon_neucbot_talys_1-95_238Ulower.txt > Teflon_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/Teflon.dat -c Chains/U238middleChain_SaG4n.dat -o Teflon_neucbot_talys_1-95_238Umiddle.txt > Teflon_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/Teflon.dat -c Chains/U238upperChain.dat -o Teflon_neucbot_talys_1-95_238Uupper.txt > Teflon_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Fused silica

# 232Th

#nohup ./neucbot.py -m Materials/Fused_silica.dat -c Chains/Th232Chain.dat -o Fused_silica_neucbot_talys_1-95_232Th.txt > Fused_silica_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/Fused_silica.dat -c Chains/U235Chain.dat -o Fused_silica_neucbot_talys_1-95_235U.txt > Fused_silica_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/Fused_silica.dat -c Chains/Pb210Chain.dat -o Fused_silica_neucbot_talys_1-95_238Ulower.txt > Fused_silica_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/Fused_silica.dat -c Chains/U238middleChain_SaG4n.dat -o Fused_silica_neucbot_talys_1-95_238Umiddle.txt > Fused_silica_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/Fused_silica.dat -c Chains/U238upperChain.dat -o Fused_silica_neucbot_talys_1-95_238Uupper.txt > Fused_silica_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Gd2O3

# 232Th

#nohup ./neucbot.py -m Materials/Gd2O3.dat -c Chains/Th232Chain.dat -o Gd2O3_neucbot_talys_1-95_232Th.txt > Gd2O3_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/Gd2O3.dat -c Chains/U235Chain.dat -o Gd2O3_neucbot_talys_1-95_235U.txt > Gd2O3_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/Gd2O3.dat -c Chains/Pb210Chain.dat -o Gd2O3_neucbot_talys_1-95_238Ulower.txt > Gd2O3_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/Gd2O3.dat -c Chains/U238middleChain_SaG4n.dat -o Gd2O3_neucbot_talys_1-95_238Umiddle.txt > Gd2O3_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/Gd2O3.dat -c Chains/U238upperChain.dat -o Gd2O3_neucbot_talys_1-95_238Uupper.txt > Gd2O3_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Si

# 232Th

#nohup ./neucbot.py -m Materials/Si.dat -c Chains/Th232Chain.dat -o Si_neucbot_talys_1-95_232Th.txt > Si_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/Si.dat -c Chains/U235Chain.dat -o Si_neucbot_talys_1-95_235U.txt > Si_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/Si.dat -c Chains/Pb210Chain.dat -o Si_neucbot_talys_1-95_238Ulower.txt > Si_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/Si.dat -c Chains/U238middleChain_SaG4n.dat -o Si_neucbot_talys_1-95_238Umiddle.txt > Si_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/Si.dat -c Chains/U238upperChain.dat -o Si_neucbot_talys_1-95_238Uupper.txt > Si_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Carbon steel warm

# 232Th

#nohup ./neucbot.py -m Materials/Carbon_steel_warm.dat -c Chains/Th232Chain.dat -o Carbon_steel_warm_neucbot_talys_1-95_232Th.txt > Carbon_steel_warm_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/Carbon_steel_warm.dat -c Chains/U235Chain.dat -o Carbon_steel_warm_neucbot_talys_1-95_235U.txt > Carbon_steel_warm_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/Carbon_steel_warm.dat -c Chains/Pb210Chain.dat -o Carbon_steel_warm_neucbot_talys_1-95_238Ulower.txt > Carbon_steel_warm_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/Carbon_steel_warm.dat -c Chains/U238middleChain_SaG4n.dat -o Carbon_steel_warm_neucbot_talys_1-95_238Umiddle.txt > Carbon_steel_warm_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/Carbon_steel_warm.dat -c Chains/U238upperChain.dat -o Carbon_steel_warm_neucbot_talys_1-95_238Uupper.txt > Carbon_steel_warm_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# IGEPAL Co-520 surfactant

# 232Th

#nohup ./neucbot.py -m Materials/IGEPAL.dat -c Chains/Th232Chain.dat -o IGEPAL_neucbot_talys_1-95_232Th.txt > IGEPAL_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/IGEPAL.dat -c Chains/U235Chain.dat -o IGEPAL_neucbot_talys_1-95_235U.txt > IGEPAL_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/IGEPAL.dat -c Chains/Pb210Chain.dat -o IGEPAL_neucbot_talys_1-95_238Ulower.txt > IGEPAL_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/IGEPAL.dat -c Chains/U238middleChain_SaG4n.dat -o IGEPAL_neucbot_talys_1-95_238Umiddle.txt > IGEPAL_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/IGEPAL.dat -c Chains/U238upperChain.dat -o IGEPAL_neucbot_talys_1-95_238Uupper.txt > IGEPAL_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Plywood

# 232Th

#nohup ./neucbot.py -m Materials/Plywood.dat -c Chafellowshipins/Th232Chain.dat -o Plywood_neucbot_talys_1-95_232Th.txt > Plywood_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/Plywood.dat -c Chains/U235Chain.dat -o Plywood_neucbot_talys_1-95_235U.txt > Plywood_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/Plywood.dat -c Chains/Pb210Chain.dat -o Plywood_neucbot_talys_1-95_238Ulower.txt > Plywood_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/Plywood.dat -c Chains/U238middleChain_SaG4n.dat -o Plywood_neucbot_talys_1-95_238Umiddle.txt > Plywood_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/Plywood.dat -c Chains/U238upperChain.dat -o Plywood_neucbot_talys_1-95_238Uupper.txt > Plywood_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# RPUF EA

# 232Th

#nohup ./neucbot.py -m Materials/RPUF_EA.dat -c Chains/Th232Chain.dat -o RPUF_EA_neucbot_talys_1-95_232Th.txt > RPUF_EA_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/RPUF_EA.dat -c Chains/U235Chain.dat -o RPUF_EA_neucbot_talys_1-95_235U.txt > RPUF_EA_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/RPUF_EA.dat -c Chains/Pb210Chain.dat -o RPUF_EA_neucbot_talys_1-95_238Ulower.txt > RPUF_EA_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/RPUF_EA.dat -c Chains/U238middleChain_SaG4n.dat -o RPUF_EA_neucbot_talys_1-95_238Umiddle.txt > RPUF_EA_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/RPUF_EA.dat -c Chains/U238upperChain.dat -o RPUF_EA_neucbot_talys_1-95_238Uupper.txt > RPUF_EA_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Mastic rope

# 232Th

#nohup ./neucbot.py -m Materials/Mastic_rope.dat -c Chains/Th232Chain.dat -o Mastic_rope_neucbot_talys_1-95_232Th.txt > Mastic_rope_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/Mastic_rope.dat -c Chains/U235Chain.dat -o Mastic_rope_neucbot_talys_1-95_235U.txt > Mastic_rope_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/Mastic_rope.dat -c Chains/Pb210Chain.dat -o Mastic_rope_neucbot_talys_1-95_238Ulower.txt > Mastic_rope_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/Mastic_rope.dat -c Chains/U238middleChain_SaG4n.dat -o Mastic_rope_neucbot_talys_1-95_238Umiddle.txt > Mastic_rope_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/Mastic_rope.dat -c Chains/U238upperChain.dat -o Mastic_rope_neucbot_talys_1-95_238Uupper.txt > Mastic_rope_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Rigid barrier EA

# 232Th

#nohup ./neucbot.py -m Materials/Rigid_EA.dat -c Chains/Th232Chain.dat -o Rigid_EA_neucbot_talys_1-95_232Th.txt > Rigid_EA_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/Rigid_EA.dat -c Chains/U235Chain.dat -o Rigid_EA_neucbot_talys_1-95_235U.txt > Rigid_EA_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/Rigid_EA.dat -c Chains/Pb210Chain.dat -o Rigid_EA_neucbot_talys_1-95_238Ulower.txt > Rigid_EA_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/Rigid_EA.dat -c Chains/U238middleChain_SaG4n.dat -o Rigid_EA_neucbot_talys_1-95_238Umiddle.txt > Rigid_EA_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/Rigid_EA.dat -c Chains/U238upperChain.dat -o Rigid_EA_neucbot_talys_1-95_238Uupper.txt > Rigid_EA_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Flexible barrier EA

# 232Th

#nohup ./neucbot.py -m Materials/Flexible_EA.dat -c Chains/Th232Chain.dat -o Flexible_EA_neucbot_talys_1-95_232Th.txt > Flexible_EA_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/Flexible_EA.dat -c Chains/U235Chain.dat -o Flexible_EA_neucbot_talys_1-95_235U.txt > Flexible_EA_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/Flexible_EA.dat -c Chains/Pb210Chain.dat -o Flexible_EA_neucbot_talys_1-95_238Ulower.txt > Flexible_EA_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/Flexible_EA.dat -c Chains/U238middleChain_SaG4n.dat -o Flexible_EA_neucbot_talys_1-95_238Umiddle.txt > Flexible_EA_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/Flexible_EA.dat -c Chains/U238upperChain.dat -o Flexible_EA_neucbot_talys_1-95_238Uupper.txt > Flexible_EA_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# FC resistor

# 232Th

#nohup ./neucbot.py -m Materials/FC_resistor.dat -c Chains/Th232Chain.dat -o FC_resistor_neucbot_talys_1-95_232Th.txt > FC_resistor_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/FC_resistor.dat -c Chains/U235Chain.dat -o FC_resistor_neucbot_talys_1-95_235U.txt > FC_resistor_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/FC_resistor.dat -c Chains/Pb210Chain.dat -o FC_resistor_neucbot_talys_1-95_238Ulower.txt > FC_resistor_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/FC_resistor.dat -c Chains/U238middleChain_SaG4n.dat -o FC_resistor_neucbot_talys_1-95_238Umiddle.txt > FC_resistor_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/FC_resistor.dat -c Chains/U238upperChain.dat -o FC_resistor_neucbot_talys_1-95_238Uupper.txt > FC_resistor_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Chip sot23

# 232Th

#nohup ./neucbot.py -m Materials/Chip_sot23.dat -c Chains/Th232Chain.dat -o Chip_sot23_neucbot_talys_1-95_232Th.txt > Chip_sot23_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/Chip_sot23.dat -c Chains/U235Chain.dat -o Chip_sot23_neucbot_talys_1-95_235U.txt > Chip_sot23_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/Chip_sot23.dat -c Chains/Pb210Chain.dat -o Chip_sot23_neucbot_talys_1-95_238Ulower.txt > Chip_sot23_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/Chip_sot23.dat -c Chains/U238middleChain_SaG4n.dat -o Chip_sot23_neucbot_talys_1-95_238Umiddle.txt > Chip_sot23_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/Chip_sot23.dat -c Chains/U238upperChain.dat -o Chip_sot23_neucbot_talys_1-95_238Uupper.txt > Chip_sot23_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Chip ATTiny102

# 232Th

#nohup ./neucbot.py -m Materials/Chip_ATTiny102.dat -c Chains/Th232Chain.dat -o Chip_ATTiny102_neucbot_talys_1-95_232Th.txt > Chip_ATTiny102_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/Chip_ATTiny102.dat -c Chains/U235Chain.dat -o Chip_ATTiny102_neucbot_talys_1-95_235U.txt > Chip_ATTiny102_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/Chip_ATTiny102.dat -c Chains/Pb210Chain.dat -o Chip_ATTiny102_neucbot_talys_1-95_238Ulower.txt > Chip_ATTiny102_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/Chip_ATTiny102.dat -c Chains/U238middleChain_SaG4n.dat -o Chip_ATTiny102_neucbot_talys_1-95_238Umiddle.txt > Chip_ATTiny102_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/Chip_ATTiny102.dat -c Chains/U238upperChain.dat -o Chip_ATTiny102_neucbot_talys_1-95_238Uupper.txt > Chip_ATTiny102_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Solder InAgAr

# 232Th

#nohup ./neucbot.py -m Materials/Solder_InAgAr.dat -c Chains/Th232Chain.dat -o Solder_InAgAr_neucbot_talys_1-95_232Th.txt > Solder_InAgAr_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/Solder_InAgAr.dat -c Chains/U235Chain.dat -o Solder_InAgAr_neucbot_talys_1-95_235U.txt > Solder_InAgAr_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/Solder_InAgAr.dat -c Chains/Pb210Chain.dat -o Solder_InAgAr_neucbot_talys_1-95_238Ulower.txt > Solder_InAgAr_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/Solder_InAgAr.dat -c Chains/U238middleChain_SaG4n.dat -o Solder_InAgAr_neucbot_talys_1-95_238Umiddle.txt > Solder_InAgAr_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/Solder_InAgAr.dat -c Chains/U238upperChain.dat -o Solder_InAgAr_neucbot_talys_1-95_238Uupper.txt > Solder_InAgAr_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Siltem pellets

# 232Th

#nohup ./neucbot.py -m Materials/Siltem_pellets.dat -c Chains/Th232Chain.dat -o Siltem_pellets_neucbot_talys_1-95_232Th.txt > Siltem_pellets_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/Siltem_pellets.dat -c Chains/U235Chain.dat -o Siltem_pellets_neucbot_talys_1-95_235U.txt > Siltem_pellets_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/Siltem_pellets.dat -c Chains/Pb210Chain.dat -o Siltem_pellets_neucbot_talys_1-95_238Ulower.txt > Siltem_pellets_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/Siltem_pellets.dat -c Chains/U238middleChain_SaG4n.dat -o Siltem_pellets_neucbot_talys_1-95_238Umiddle.txt > Siltem_pellets_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/Siltem_pellets.dat -c Chains/U238upperChain.dat -o Siltem_pellets_neucbot_talys_1-95_238Uupper.txt > Siltem_pellets_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# Brass

# 232Th

#nohup ./neucbot.py -m Materials/Brass.dat -c Chains/Th232Chain.dat -o Brass_neucbot_talys_1-95_232Th.txt > Brass_neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/Brass.dat -c Chains/U235Chain.dat -o Brass_neucbot_talys_1-95_235U.txt > Brass_neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/Brass.dat -c Chains/Pb210Chain.dat -o Brass_neucbot_talys_1-95_238Ulower.txt > Brass_neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/Brass.dat -c Chains/U238middleChain_SaG4n.dat -o Brass_neucbot_talys_1-95_238Umiddle.txt > Brass_neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/Brass.dat -c Chains/U238upperChain.dat -o Brass_neucbot_talys_1-95_238Uupper.txt > Brass_neucbot_talys_1-95_238Uupper.out &

#=======================================================================

# 232Th

#nohup ./neucbot.py -t -m Materials/.dat -c Chains/Th232Chain.dat -o _neucbot_talys_1-95_232Th.txt > _neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -t -m Materials/.dat -c Chains/U235Chain.dat -o _neucbot_talys_1-95_235U.txt > _neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -t -m Materials/.dat -c Chains/Pb210Chain.dat -o _neucbot_talys_1-95_238Ulower.txt > _neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -t -m Materials/.dat -c Chains/U238middleChain_SaG4n.dat -o _neucbot_talys_1-95_238Umiddle.txt > _neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -t -m Materials/.dat -c Chains/U238upperChain.dat -o _neucbot_talys_1-95_238Uupper.txt > _neucbot_talys_1-95_238Uupper.out &

#=======================================================================


# 232Th

#nohup ./neucbot.py -m Materials/.dat -c Chains/Th232Chain.dat -o _neucbot_talys_1-95_232Th.txt > _neucbot_talys_1-95_232Th.out &

# 235U

#nohup ./neucbot.py -m Materials/.dat -c Chains/U235Chain.dat -o _neucbot_talys_1-95_235U.txt > _neucbot_talys_1-95_235U.out &

# 238Ulow

#nohup ./neucbot.py -m Materials/.dat -c Chains/Pb210Chain.dat -o _neucbot_talys_1-95_238Ulower.txt > _neucbot_talys_1-95_238Ulower.out &

# 238Umid

#nohup ./neucbot.py -m Materials/.dat -c Chains/U238middleChain_SaG4n.dat -o _neucbot_talys_1-95_238Umiddle.txt > _neucbot_talys_1-95_238Umiddle.out &

# 238Uup

#nohup ./neucbot.py -m Materials/.dat -c Chains/U238upperChain.dat -o _neucbot_talys_1-95_238Uupper.txt > _neucbot_talys_1-95_238Uupper.out &

#=======================================================================

echo "Done!"

# Version 1.90. 30.06.2022
# Added Brass 

# Version 1.80. 29.06.2022
# Added Solder InAgAr
# Added Siltem pellets

# Version 1.70. 28.06.2022
# Added FC resistor
# Added Chip sot23
# Added Chip ATTiny102

# Version 1.60. 23.06.2022
# Added Flexible barrier EA

# Version 1.50. 17.06.2022
# Added Rigid barrier EA

# Version 1.40. 14.06.2022
# Added Plywood
# Added RPUF EA
# Added Mastic rope

# Version 1.30. 01.06.2022
# Added Si
# Added Carbon steel warm
# Added IGEPAL Co-520 surfactant 

# Version 1.20. 27.05.2022
# Added Teflon
# Added Fused silica
# Added Gd2O3

# Version 1.10. 03.12.2021
# Added VT1-0 
# Added Ti
# Added Cu20Ti80 
# Added stainless steel 08X18H10T

# Version 1.00. 23.10.2020
# Initial release based on massive_submitter_materials.sh
# Added acrylic donchamp
# Added PEEK fiber
# Added Arlon 55NT
# Added PPS
# Added a two-component material: Gd2O3 (Gd - 2% by weight) + Acrylic
# Added PEN
# Added Cu Luvata
# Added Nylon 66
# Added stainless steel AISI 318 LN
# Added LAr
# Added VT1-00
