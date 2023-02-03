# from .utils.common import Region
# from .utils.screen import screen_size_calculate

# import utils
# import utils.screen
from utils.screen import screen_size_calculate

def screen_info():
    ss = screen_size_calculate()
    return 'screen size: {0} x {1}, dpr: {2}'.format(ss[0], ss[1], ss[2])

def main():
    print(screen_size_calculate())

if __name__ == '__main__':
    main()
