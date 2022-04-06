import os

class Path():

    def __init__(self, path: str) -> None:
        if not os.path.isdir(path): raise Exception("The path passed to MusiCore.PlayList.Path isn't a directory.")
        self.path = path

    def glob(self, include: list):
        if not isinstance(include, list):
            include = [include]

        ucl = [filename for filename in os.listdir(self.path)]
        ulwe = list()
        cl = list()

        for filename in ucl:
            if os.path.isdir(f"{self.path}/{filename}"): pass
            
            for e in include:
                if filename.endswith(e):
                    fnwe = filename[:-len(e)]

                    if fnwe in ulwe:
                        print(f"Skipping double file name: {fnwe}")
                    else:
                        cl.append(filename)
                        ulwe.append(fnwe)
        
        return cl
