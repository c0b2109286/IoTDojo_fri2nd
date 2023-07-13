import multiprocessing
import os

def run_script(script_name):
    os.system(f'python {script_name}')

if __name__ == '__main__':
    scripts = ['app.py', 'userdb.py']

    processes = []
    for script in scripts:
        process = multiprocessing.Process(target=run_script, args=(script,))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()
