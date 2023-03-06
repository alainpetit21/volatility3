source ./venv/bin/activate


python vol.py -f ./data/PhysicalMemory.raw  -v windows.ldrmodules.LdrModules > ./data/out/ldrmodules.txt
cat ./data/out/ldrmodules.txt

python vol.py -f ./data/PhysicalMemory.raw  -v windows.cmdline.CmdLine > ./data/out/CmdLine.txt
cat ./data/out/CmdLine.txt

python vol.py -f ./data/PhysicalMemory.raw  -v windows.dlllist.DllList > ./data/out/DllList.txt
cat ./data/out/DllList.txt

python vol.py -f ./data/PhysicalMemory.raw  -v windows.malfind.Malfind > ./data/out/Malfind.txt
cat ./data/out/Malfind.txt

python vol.py -f ./data/PhysicalMemory.raw  -v windows.envars.Envars > ./data/out/Envars.txt
cat ./data/out/Envars.txt

python vol.py -f ./data/PhysicalMemory.raw  -v windows.pslist.PsList > ./data/out/PsList.txt
cat ./data/out/PsList.txt

python vol.py -f ./data/PhysicalMemory.raw  -v windows.pstree.PsTree > ./data/out/PsTree.txt
cat ./data/out/PsTree.txt
python vol.py -f ./data/PhysicalMemory.raw  -v windows.strings.Strings > ./data/out/Strings.txt
cat ./data/out/Strings.txt
