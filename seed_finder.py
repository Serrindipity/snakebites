des = "A tool for Noita that takes the path to a sessions folder and returns data based on a query"
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

# Possible search values:
# Stats: items, hp, gold_all, places_visited, projectiles_shot
# Kills: Stats -> kills

def make_parsed_args():
        
        parser = argparse.ArgumentParser(prog = f"{Path(__file__).name}", description=des)
        parser.add_argument("-f", "--folder", type=str, help = "Filepath to session folder", default = r'c:\Users\jonqu\AppData\LocalLow\Nolla_Games_Noita\save00\stats\sessions')
        parser.add_argument('-l', "--limit", type=int, help = "Maximum number of seeds to return", default = 3)
        parser.add_argument('-s', '--search', type=str, help="Type of thing to look for")
        
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

# Parses a kill or stat xml document, takes a pathlib argument. Returns search value, seed
def parse_xml(file, search):
    for type in stat_types:
          if type.value in str(file):
                parse_type = type
    assert parse_type
    tree = ET.parse(file)
    print(parse_type)
    return_list = []
    match parse_type:
        case stat_types.STATS:
            attrs = tree.find('stats').attrib
            
            
            
        case stat_types.KILLS:
            # Kills parse
            print("parsing kills xml")
    
    seed = attrs["world_seed"]
    return seed

if __name__ == "__main__":
    print("running")
    args = make_parsed_args()
    files_to_parse = get_stat_files(args.folder)
    print(files_to_parse)
    # for file in files_to_parse:
    #      parse_xml(file, args.search)
    #      break
