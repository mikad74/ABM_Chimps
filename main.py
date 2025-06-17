from Base_model import *

def main():
    model = Model(5, 10, 10)
    for crew in model.crews:
        print(vars(crew))
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

