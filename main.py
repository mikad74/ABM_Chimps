from Base_model import *

def main():
    model = Model(5, 1, 10)
    model.run()
    print(model.grid)
    model.run()
    print(model.grid)
    model.run()
    print(model.grid)
    model.run()
    print(model.grid)
    print('done')


if __name__ == "__main__":
    main()
