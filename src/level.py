class LevelManager:
    def __init__(self, save_file) -> None:
        self.load_save_file(save_file)
    
    def load_save_file(self, save_file):
        with open(save_file, "r") as file:
            data = file.read().split(",")
            self.level = data[0]

    # def load_level(self, level):
    #     self.player = Sprite(self.load_tilemap(level))


    def load_tilemap(self, level):
        print(f"loading level {level}")
        with open(f"tilemaps/{level}.csv", "r") as file:
            tilemap = file.readlines()
            print(tilemap)
        
        sep_tilemap = []
        for i in range(len(tilemap)):
            sep_tilemap.append(tilemap[i].strip().split(",")) 
        print(sep_tilemap)
        return sep_tilemap


