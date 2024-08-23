import sys
import os

files = {
    "config.ini": """
[Secure]
WebAPIToken = token
AccountSteamID = steamID64

[Main]
SkipGamesWithZeroPlaytime = true
""",
}


if __name__ == '__main__':
    print("\n".join(sys.path))
    path_num = int(input("Enter path id: "))
    
    if path_num < 0 or path_num >= len(sys.path): 
        print("Invalid path id!")
        sys.exit(1)
    
    path = sys.path[path_num]
    
    for i, data in files.items(): 
        if not os.path.isfile(os.path.join(path, i)):
            with open(os.path.join(path, i), 'a') as f:
                if data: 
                    f.write(data)
                
                print(f"Created {i} in {path}")
        else:
            print(f"{i} already exists in {path}")