des = "A tool for Noita that takes the path to a sessions folder and returns data based on a query"
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

# Possible search values:
# Stats: items, heart_containers, gold_all, places_visited, projectiles_shot
# hp and heart_containers don't seem to work

def make_parsed_args():
        
        parser = argparse.ArgumentParser(prog = f"{Path(__file__).name}", description=des)
        
        parser.add_argument('-l', "--limit", type=int, help = "Maximum number of seeds to return. -1 is no limit.", default = 3)
        parser.add_argument('-s', '--search', type=str, help="Type of thing to look for", default='kills')
        parser.add_argument("folder", type=str, help = "Filepath to session folder")
        
        parsed = parser.parse_args()
        return parsed

# Returns a list of tuples, of the form (kills file path, stats file path) of Path Objects to xml files
def get_stat_files(dir_path):
      sessions = Path(dir_path)
      out = []
      for kills_file in sessions.glob('*_kills.xml'):
           filename = str(kills_file).split("sessions\\")[1]
           serial = filename.split("_kills")[0]
           stats_file = sessions.glob(f'*{serial}_stats.xml').__next__()
           zipped = (kills_file, stats_file)
           out.append(zipped)
      return out

# Builds the dictionary of search items out of the target files.
def build_dictionary(kills_file, stats_file):
     # Copies the stats file first, since it's bigger.
     stats_tree = ET.parse(stats_file)
     d = stats_tree.find('stats').attrib.copy()
     kills_tree = ET.parse(kills_file)
     d['kills'] = kills_tree.getroot().attrib['kills']
     return d

# Parses a kill or stat xml document, takes a pathlib argument. Returns search value, seed
def parse_xml(file_tuple, search):
    d = build_dictionary(file_tuple[0], file_tuple[1])
    search_value = d[search]
    seed = d["world_seed"]
    return search_value, seed

if __name__ == "__main__":
    args = make_parsed_args()
    files_to_parse = get_stat_files(args.folder)
    sort_list = []
    for tup in files_to_parse:
         sort_list.append(parse_xml(tup, args.search))
    sort_list.sort(key=lambda x : int(x[0]), reverse=True)
    for i in sort_list[0 : args.limit]:
        print(f'{args.search}: {i[0]} , seed: {i[1]}')
