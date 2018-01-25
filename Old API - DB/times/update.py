import create, populate, unique, os

# TODO : Run Update Outside of Directory

def update():
    print("Removing Old db file...")
    os.remove('times.db')
    print("...Old db file removed.")
    print("Creating new db...")
    create.main()
    print("...New db created.")
    print("Populating new db...")
    populate.main()
    print("...New db populated.")
    print("Creating unique JSONs...")
    unique.main()
    print("...unique JSONs created.")

if __name__ == '__main__':
    update()
