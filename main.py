from Base_model import *

def main(n=10):
    model = Model(0, 0, 3)
    for _ in range(n):
        model.run()
        print(model.grid)
    print('done')


if __name__ == "__main__":
    main()
