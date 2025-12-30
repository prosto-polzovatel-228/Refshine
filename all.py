import subprocess

# Список файлов с ботами
bots = ["gr_storm.py", "gr_klin.py", "other.py"]

processes = []

# Запускаем каждый бот отдельным процессом
for bot in bots:
    p = subprocess.Popen(["python3", bot])
    processes.append(p)

# Чтобы главный файл не завершился
for p in processes:
    p.wait()

