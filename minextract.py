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
    def __init__(self, json_file, extract_dir):
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
    
    def extract_subdir(self, subdir):
        full_subdir = f"minecraft/{subdir}/"
        # Find each line with full_subdir prefix, remove the prefix and keep the rest of the path and the hash
        file_list = {k[len(full_subdir):] : v["hash"] for (k, v) in self.json["objects"].items() if k.startswith(full_subdir)}
        
        print("  {}:".format(subdir))
        for fpath, fhash in file_list.items():
            # Print current extracted file
            print("    {}".format(fpath))
            
            # Ensure the paths are good to go for Windows with properly escaped backslashes in the string
            src_fpath = os.path.normpath(f"{self.objects_dir}/{fhash[:2]}/{fhash}")
            dest_fpath = os.path.normpath(f"{self.output_dir}/{subdir}/{fpath}")

            # Make any directories needed to put the output file into as Python expects
            os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)

            # Copy the file
            shutil.copyfile(src_fpath, dest_fpath)
    
    def extract_icons(self):
        self.extract_subdir("icons")
    
    def extract_lang(self):
        self.extract_subdir("lang")
    
    def extract_resourcepacks(self):
        self.extract_subdir("resourcepacks")
    
    def extract_sounds(self):
        self.extract_subdir("sounds")
    
    def extract_textures(self):
        self.extract_subdir("textures")
    
    def extract_all(self):
        self.extract_icons()
        self.extract_lang()
        self.extract_resourcepacks()
        self.extract_sounds()
        self.extract_textures()
        #TODO: Non-subfolders
    
    def run(self):
        print("File extraction :")
        self.extract_all()



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
