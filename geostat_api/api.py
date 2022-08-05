from calendar import firstweekday
import os

def run():
    os.system('pygeoapi serve')


if __name__ == '__main__':
    import fire
    fire.Fire(run)
