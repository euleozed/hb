@echo off
echo Executando extract.py...
python "C:\Users\00840207255\OneDrive - Leonardo\Aplicativos\App Direx\etl\extract.py"

echo Executando load.py...
python "C:\Users\00840207255\OneDrive - Leonardo\Aplicativos\App Direx\etl\load.py"

echo Executando transform.py...
python "C:\Users\00840207255\OneDrive - Leonardo\Aplicativos\App Direx\etl\transform.py"

echo Processo concluído!
pause