from os import system, name


def main_p():
    for i in range(10):
        print("Hello")

  
  
# define our clear function
def clear():
  
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
  

if __name__=="__main__":
    main_p()
