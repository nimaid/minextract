import os
import sys
import argparse
import json
import shutil

# Test if this is a PyInstaller executable or a .py file
if getattr(sys, 'frozen', False):
    IS_EXE = True
    PROG_FILE = sys.executable
    PROG_PATH = os.path.dirname(PROG_FILE)
    PATH = sys._MEIPASS
else:
    IS_EXE = False
    PROG_FILE = os.path.realpath(__file__)
    PROG_PATH = os.path.dirname(PROG_FILE)
    PATH = PROG_PATH

# Main class
class Minextract:
    def __init__(self,
        json_file,
        extract_dir
    ):
        self.json_file = os.path.realpath(json_file)
        self.extract_dir = extract_dir
        
        self.output_dir = os.path.join(self.extract_dir, "assets")
        
        self.assets_dir = os.path.split(os.path.split(self.json_file)[0])[0]
        self.objects_dir = os.path.join(self.assets_dir, "objects")
        
        # Make output dir if not existing
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load JSON file
        with open(self.json_file, "r") as f:
            self.json = json.load(f)
    
    def extract_sound(self):
        MC_SOUNDS = r"minecraft/sounds/"
        
        # Find each line with MC_SOUNDS prefix, remove the prefix and keep the rest of the path and the hash
        sounds = {k[len(MC_SOUNDS):] : v["hash"] for (k, v) in self.json["objects"].items() if k.startswith(MC_SOUNDS)}
        
        for fpath, fhash in sounds.items():
            # Ensure the paths are good to go for Windows with properly escaped backslashes in the string
            src_fpath = os.path.normpath(f"{self.objects_dir}/{fhash[:2]}/{fhash}")
            dest_fpath = os.path.normpath(f"{self.output_dir}/sounds/{fpath}")

            # Print current extracted file
            print("    {}".format(fpath))

            # Make any directories needed to put the output file into as Python expects
            os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)

            # Copy the file
            shutil.copyfile(src_fpath, dest_fpath)
    
    def run(self):
        print("File extraction :")
        print("  Sounds:")
        self.extract_sound()



# Helper functions for the argument parser
def file_path(string):
    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)

# Parse arguments
def parse_args(args):
    parser = argparse.ArgumentParser(
        description="An extraction tool for Minecraft assets.\n\nDefault parameters are shown in [brackets].",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("-j", "--json", dest="indexes_json", type=file_path, required=True,
        help="the .json file from the \"indexes\" folder")
    parser.add_argument("-o", "--output", dest="output_direcotry", type=str, required=False, default=".",
        help="the folder to extract the assets to [./]")
    
    return parser.parse_args()

def main(args):
    args = parse_args(args)
    
    minextract = Minextract(
        json_file=args.indexes_json, 
        extract_dir=args.output_direcotry)
    
    minextract.run()

def run():
    main(sys.argv[1:])

if __name__ == "__main__":
    run()
