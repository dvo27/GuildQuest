from models import *
import warnings

warnings.filterwarnings("ignore", category=SyntaxWarning)

c1 = Character("A", "Mage")
c2 = Character("B", "Rogue")

c1.curr_inventory.add_inventory(Item("Sword", "Rare", "10", "Default Sword"))

# print(len(c1.curr_inventory.items)) # 1
# print(len(c2.curr_inventory.items)) # 0

def main():
    print("""
   ______      _ __    __   ____                  __ 
  / ____/_  __(_) /___/ /  / __ \\__  _____  _____/ /_
 / / __/ / / / / / __  /  / / / / / / / _ \\/ ___/ __/
/ /_/ / /_/ / / / /_/ /  / /_/ / /_/ /  __(__  ) /_  
\\____/\\__,_/_/_/\\__,_/   \\___\\\\_\\__,_/\\___/____/\\__/  
                                                     
          """
          )
    
    
if __name__ == "__main__":
    main()