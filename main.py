from Base_model import *

def main():
    model = Model(5, 1, 10)
    model.print_grid()
    for crew in model.crews:
        print(vars(crew))
        crew.move(model.grid_size)
    model.print_grid()
    print('done')


if __name__ == "__main__":
    main()
