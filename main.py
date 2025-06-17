from Base_model import *

def main():
    model = Model(5)
    for crew in model.crews:
        print(vars(crew))
    print('done')


if __name__ == "__main__":
    main()
