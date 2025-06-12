import json
import requests
from pathlib import Path
import re
import argparse
from collections import defaultdict
import opencc


URL_SUBTITLES = "https://api.kcwiki.moe/subtitles/detail"
URL_SEASONAL = "https://zh.kcwiki.cn/api.php"
URL_SHIPS = "http://api.kcwiki.moe/ships"
URL_SEASONAL_KEYS = "https://raw.githubusercontent.com/KC3Kai/KC3Kai/develop/src/data/quotes_size.json"
# FIXME adjust year
OLD_YEAR_FORMAT = 2017
CURRENT_YEAR = 2024

PATTERN_SHIP = r"\{\{台词翻译表\|([^}]+)\}\}"
PATTERN_TABLE = r"\|\s*(\S+)\s*=\s*([^|\n}]+)"
PATTERN_VOICE_TYPE = (
    r"((Const|DockLight|DockMed|Dock|Fleet|Night|Light|Med|Sec|MV)*[A-Z0-9][a-z0-9]*)([A-Z][A-Za-z]+)(\d*)"
)
PATTERN_RETRIEVAL = r"(\d+)@([A-Z][A-Za-z]*)(\d*)"

KCWIKIZH_TYPE_MAP = {
    "Intro": 1,
    "LibIntro": 25,
    "Sec1": 2,
    "Sec12nd": 2,  # Special case for Anniversary
    "Sec13nd": 2,  # Special case for Anniversary
    "2nd": 2,  # Special case for Anniversary
    "3rd": 2,  # Special case for Anniversary
    "Sec2": 3,
    "Sec3": 4,
    "Return": 7,
    "ConstComplete": 5,
    "Achievement": 8,
    "Equip1": 9,
    "Equip2": 10,
    "Equip3": 26,
    "DockLightDmg": 11,
    "DockMedDmg": 12,
    "DockComplete": 6,
    "FleetOrg": 13,
    "Sortie": 14,
    "Battle": 15,
    "Atk1": 16,
    "Atk2": 17,
    "NightBattle": 18,
    "LightDmg1": 19,
    "LightDmg2": 20,
    "MedDmg": 21,
    "Sunk": 22,
    "MVP": 23,
    "Proposal": 24,
    "Resupply": 27,
    "SecWed": 28,
    "Idle": 29,
    "0000": 30,
    "0100": 31,
    "0200": 32,
    "0300": 33,
    "0400": 34,
    "0500": 35,
    "0600": 36,
    "0700": 37,
    "0800": 38,
    "0900": 39,
    "1000": 40,
    "1100": 41,
    "1200": 42,
    "1300": 43,
    "1400": 44,
    "1500": 45,
    "1600": 46,
    "1700": 47,
    "1800": 48,
    "1900": 49,
    "2000": 50,
    "2100": 51,
    "2200": 52,
    "2300": 53,
}

# FIXME: This rule applies only for a special season. Need manual adjustment every season.
SEASON_MAP = {
    "Setubunn": "Setsubun",
    "Setsubunn": "Setsubun",
    "Sanma": "Saury",
    "Autumn": "Fall",
    "Halloween": "Halloween",
    "Shoshuu": "LateFall",
    "MidAutumn": "Cold",
    "Shinnen": "NewYears",
    "Nenmatsu": "YearsEnd",
    "Christmas": "Xmas",
    "Valentine": "Valentines",
    "WhiteDay": "WhiteDay",
    "Hinamaturi": "Hina",
    "Hinamatsuri": "Hina",
    "Haru": "Spring",
    "Spring": "Spring",
    "Sakura": "Spring",
    "Anniv": "Anniversary",
    "FifthAnniversary": "Anniversary2018",
    "SixthAnniversary": "Anniversary2019",
    "SeventhAnniversary": "Anniversary2020",
    "EighthAnniversary": "Anniversary2021",
    "NinethAnniversary": "Anniversary2022",
    "TenthAnniversary": "Anniversary2023",
    "EleventhAnniversary": "Anniversary2024",
}
# These are some regular entries
SKIP_ENTRIES = [
    # "081-Sec3Valentine2021",
    # "081a-Sec3Valentine2021",
    # "145-Equip2EveOfBattle",
]

T2SCONVERTER = opencc.OpenCC("t2s.json")

FILENAME_ID_MAP = "kcwiki_ship_id_map.json"
FILENAME_NORMAL = "kcwiki.json"
FILENAME_SEASON = "kcwiki_season.json"


def get_args():
    parser = argparse.ArgumentParser(
        description="Get subtitles translation from kcwiki. Please check README for the correct pipeline."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--season", type=str, help="get seasonal subtitles in for example 2023年秋刀鱼祭典")
    group.add_argument("-r", "--remodel", action="store_true", help="retrieve the remodelGroups and wiki_id_map")
    group.add_argument(
        "-f",
        "--findkey",
        nargs=2,
        metavar=("filename_season", "filename_out"),
        help="retrieve seasonal keys from KC3Kai/src/data/quotes_size.json",
    )
    group.add_argument(
        "-m",
        "--merge",
        nargs=3,
        metavar=("filename_in1", "filename_in2", "filename_out"),
        help="Merge the second json files into the first one, output to the given file name, be sure to check seasonal keys before merge",
    )
    args = parser.parse_args()
    return args


def get_ship_database():
    response = requests.get(URL_SHIPS)
    if response.status_code != 200:
        print(f"Failed to get seasonal subtitles with error {response.status_code}")
        return {}
    ship_list = response.json()
    # convert list to dict
    ship_database = {}
    for entry in ship_list:
        ship_database[entry["id"]] = entry
    # sort_no: id, map from kcwiki_id to ship_id
    wiki_ship_id_map = {}
    # valid ship_ids
    ship_id_list = []
    for ship_id, entry in ship_database.items():
        # exclude enemy ships and seasonal models
        if entry["sort_no"] is not None and entry["sort_no"] > 0:
            wiki_ship_id_map[entry["wiki_id"]] = str(ship_id)
            ship_id_list.append(ship_id)

    return wiki_ship_id_map


def get_normal_subtitles():
    # Get all subtitle details
    response = requests.get(URL_SUBTITLES)
    if response.status_code != 200:
        print(f"Failed to get all subtitles with error {response.status_code}")
        return {}
    # only keep zh entries
    subtitles_detail = response.json()
    subtitles_normal = defaultdict(dict)
    subtitles_no_translation = []
    for ship_id, voice_list in subtitles_detail.items():
        for voice in voice_list:
            voice_id = str(voice["voiceId"])  # id as string
            subtitle = voice["zh"].strip()  # eliminate spaces
            subtitle = T2SCONVERTER.convert(subtitle)
            if "本字幕暂时没有翻译" in subtitle:
                subtitles_no_translation.append(f"{ship_id}-{voice_id}")
                continue
            subtitles_normal[ship_id][voice_id] = subtitle
    print(f"{len(subtitles_no_translation)}条字幕没有翻译：{subtitles_no_translation}")
    return subtitles_normal


def get_seasonal_subtitles(season, wiki_ship_id_map):
    # Get current seasonal subtitles
    rq = {"action": "query", "prop": "revisions", "rvprop": "content", "format": "json", "titles": season}
    response = requests.get(URL_SEASONAL, params=rq)
    if response.status_code != 200:
        print(f"Failed to get seasonal subtitles with error {response.status_code}")
        return {}
    page_id = list(response.json()["query"]["pages"].keys())[0]
    page_content = response.json()["query"]["pages"][page_id]["revisions"][0]["*"]
    subtitles_seasonal = parse_seasonal_subtitles(page_content, wiki_ship_id_map)
    return subtitles_seasonal


def parse_seasonal_subtitles(content, wiki_ship_id_map):
    # print(f"Only years >= {YEAR_TO_PROCESS} are processed.")
    subtitles_seasonal = defaultdict(dict)
    all_voice_type = set()
    all_season = set()
    # find all ships
    matches_ship = re.finditer(PATTERN_SHIP, content)
    for match_ship in matches_ship:
        matches_voice = re.findall(PATTERN_TABLE, match_ship.group(1))
        temp_dict = {}
        for pair in matches_voice:
            temp_dict[pair[0]] = pair[1]
        sort_no = temp_dict["编号"]
        ship_id = wiki_ship_id_map[sort_no]
        text = temp_dict["中文译文"].strip()
        text = T2SCONVERTER.convert(text)
        if len(text) == 0:
            print("Translation empty:", temp_dict)
            continue
        if temp_dict["档名"] in SKIP_ENTRIES:
            print("Skip ", temp_dict)
            continue
        voice_type_season = re.findall(PATTERN_VOICE_TYPE, temp_dict["档名"])
        if len(voice_type_season) == 0:
            print(f"Failed to get seasonal subtitle id: {temp_dict}")
            continue
        voice_type, _, season, year = voice_type_season[0]
        voice_type = KCWIKIZH_TYPE_MAP.get(voice_type)
        if voice_type is None:
            voice_type = input(f"Voice type unknow: {temp_dict}\nEnter correct type or n to skip: ")
            if voice_type == "n":
                print(f"skip {temp_dict['档名']}")
                continue
        try:
            year = int(year)
        except:
            if "Anniv" in season:
                year = ""
                print(f"Anniversary quote, proceed with predefined year: {temp_dict}")
            else:
                year = input(f"Year not available: {temp_dict}\nEnter correct year or n to skip: ")
                if year == "n":
                    print(f"skip {temp_dict['档名']}")
                    continue
                # year = int(year)
        # if year >= YEAR_TO_PROCESS:
        season_name = SEASON_MAP.get(season)
        if season_name is None:
            season_name = input(f'Season "{season}" unknown: {temp_dict}\nEnter correct season or n to skip: ')
            if season_name == "n":
                print(f"skip {temp_dict['档名']}")
                continue
        voice_key = f"{voice_type}@{season_name}{year}"
        subtitles_seasonal[ship_id][voice_key] = text
        all_voice_type.add(voice_type)
        all_season.add(season)
    print("Voice types:", all_voice_type)
    print("Season names in kcwiki:", all_season)
    return subtitles_seasonal


def retrieve_seasonal_keys(subtitles):
    # print("To avoid check in the future, only update seasonal voices appearing in KC3Kai/src/data/quotes_size.json.")
    # Get seasonal quotes-key map
    response = requests.get(URL_SEASONAL_KEYS)
    if response.status_code != 200:
        print(f"Failed to get all subtitles with error {response.status_code}")
        return {}
    # ground-truth seasonal keys
    gt = response.json()
    subtitles_retrieved = defaultdict(dict)
    for ship_id, ship_quotes in subtitles.items():
        gt_ship = gt.get(ship_id)
        # ship not in gt, skip
        if gt_ship is None:
            print(f"Ship {ship_id} not found in gt.")
            continue
        for pred_key, quote in ship_quotes.items():
            voice_info = re.findall(PATTERN_RETRIEVAL, pred_key)
            # predicted key maybe not a seasonal, manual decision
            if len(voice_info) == 0:
                add = input(f"Voice {ship_id}-{pred_key} not seasonal, add as is(k) or skip(n): ")
                if add == "n":
                    print(f"Skip {ship_id}-{pred_key}.")
                else:
                    subtitles_retrieved[ship_id][pred_key] = quote
                    print(f"Add {ship_id}-{pred_key}.")
                continue
            voice_type, season, year = voice_info[0]
            old_key = f"{season}{year}"
            gt_sizes = gt_ship.get(voice_type)
            if gt_sizes is None:
                if len(year) > 0 and int(year) != CURRENT_YEAR:
                    # this voice type is not in gt, skip for now
                    print(f"Voice type of {ship_id}-{pred_key} not found in gt, skip.")
                    continue
                else:
                    # new quote in current year, add as is
                    new_key = old_key
                    print(f"New quote in this year {ship_id}-{pred_key}, but voice type unknown, add as is.")
            else:
                # find all gts with this season
                gt_keys = [k for k in gt_sizes.values() if season in k]
                if len(gt_keys) == 0:
                    if len(year) > 0 and int(year) != CURRENT_YEAR:
                        # no gt key for this season, skip
                        print(f"Voice season {ship_id}-{pred_key} not found in gt, skip.")
                        continue
                    else:
                        # new quote in current year, add as is
                        new_key = old_key
                        print(f"New quote in this year {ship_id}-{pred_key}, but not found in gt, add as is.")
                elif len(gt_keys) == 1:
                    new_key = gt_keys[0]
                    # only one match, check whether they are the same
                    if old_key != new_key:
                        if season != new_key:
                            # year not match, need manual decision
                            proceed = input(
                                f'{new_key} found for {ship_id}-{pred_key}: "{quote}", proceed(y), skip(n), keep as is(k): '
                            )
                        elif len(year) > 0 and int(year) > OLD_YEAR_FORMAT:
                            # no year given in gt, this is maybe an old entry, check year in quote
                            proceed = input(
                                f'{new_key} found for {ship_id}-{pred_key}: "{quote}", proceed(y), skip(n), keep as is(k): '
                            )
                        else:
                            proceed = "y"

                        if proceed == "n":
                            print(f"Skip {ship_id}-{pred_key}")
                            continue
                        elif proceed == "k":
                            new_key = old_key
                else:
                    # more than one key matched, need manual decision, !check en translation!
                    idx = input(
                        f'{gt_keys} found for {ship_id}-{pred_key}: "{quote}", enter index to use, skip(n), keep as is(k): '
                    )
                    if idx == "n":
                        print(f"Skip {ship_id}-{pred_key}")
                        continue
                    elif idx == "k":
                        new_key = old_key
                    else:
                        idx = int(idx)
                        new_key = gt_keys[idx]

            new_key = f"{voice_type}@{new_key}"
            subtitles_retrieved[ship_id][new_key] = quote
            print(f"{ship_id}-{pred_key} -> {new_key}")
    return subtitles_retrieved


def merge_subtitles(subtitles_normal, subtitles_seasonal):
    for ship_id in subtitles_seasonal.keys():
        if ship_id not in subtitles_normal:
            subtitles_normal[ship_id] = subtitles_seasonal[ship_id]
            print(f"ship_id {ship_id} not in normal subtitles")
        else:
            subtitles_normal[ship_id].update(subtitles_seasonal[ship_id])
    subtitles_normal = sort_subtitles_ships(subtitles_normal)
    return subtitles_normal


def sort_subtitles_ships(subtitles):
    new_subtitles = {}
    keys = []
    for key in subtitles.keys():
        if key.isnumeric():
            keys.append(int(key))
        else:
            new_subtitles[key] = subtitles[key]
    keys = sorted(keys)
    for key in keys:
        new_subtitles[str(key)] = subtitles[str(key)]
    return new_subtitles


if __name__ == "__main__":
    args = get_args()

    if args.remodel:
        print("Processing ship database...")
        wiki_ship_id_map = get_ship_database()
        with open(FILENAME_ID_MAP, "w", encoding="utf-8-sig") as f:
            json.dump(wiki_ship_id_map, f, indent="  ")
        print(f"{FILENAME_ID_MAP} saved.")

    elif args.season is not None:
        print("Processing seasonal subtitles...")
        with open(FILENAME_ID_MAP, encoding="utf-8-sig") as f:
            wiki_ship_id_map = json.load(f)
        subtitles_seasonal = get_seasonal_subtitles(f"季节性/{args.season}", wiki_ship_id_map)
        if Path(FILENAME_SEASON).exists():
            overwrite = input(f"{FILENAME_SEASON} already exists, are you sure to overwrite it? (y/n), default n: ")
            if overwrite == "y":
                with open(FILENAME_SEASON, "w", encoding="utf-8-sig") as f:
                    json.dump(subtitles_seasonal, f, ensure_ascii=False, indent="  ")
                print(f"{FILENAME_SEASON} saved. Please double check keys before merge!")
            else:
                print("Keep old file.")
        else:
            with open(FILENAME_SEASON, "w", encoding="utf-8") as f:
                json.dump(subtitles_seasonal, f, ensure_ascii=False, indent="  ")
            print(f"{FILENAME_SEASON} saved. Please double check keys before merge!")

    elif args.findkey is not None:
        print(f"Retrieve seasonal keys for {args.findkey[0]}...")
        with open(args.findkey[0], encoding="utf-8-sig") as f:
            subtitles_seasonal = json.load(f)
        subtitles_seasonal = retrieve_seasonal_keys(subtitles_seasonal)
        if Path(args.findkey[1]).exists():
            overwrite = input(f"{args.findkey[1]} already exists, are you sure to overwrite it? (y/n), default n: ")
            if overwrite == "y":
                with open(args.findkey[1], "w", encoding="utf-8-sig") as f:
                    json.dump(subtitles_seasonal, f, ensure_ascii=False, indent="  ")
                print(f"{args.findkey[1]} saved.")
            else:
                print("Keep old file.")
        else:
            with open(args.findkey[1], "w", encoding="utf-8-sig") as f:
                json.dump(subtitles_seasonal, f, ensure_ascii=False, indent="  ")
            print(f"{args.findkey[1]} saved.")

    elif args.merge is not None:
        print(f"Merging {args.merge[1]} into {args.merge[0]}...")
        with open(args.merge[0], encoding="utf-8-sig") as f:
            subtitles_1 = json.load(f)
        with open(args.merge[1], encoding="utf-8-sig") as f:
            subtitles_2 = json.load(f)
        subtitles_merge = merge_subtitles(subtitles_1, subtitles_2)
        if Path(args.merge[2]).exists():
            overwrite = input(f"{args.merge[2]} already exists, are you sure to overwrite it? (y/n), default n: ")
            if overwrite == "y":
                with open(args.merge[2], "w", encoding="utf-8-sig") as f:
                    json.dump(subtitles_merge, f, ensure_ascii=False, indent="  ")
                print(f"{args.merge[2]} saved.")
            else:
                print("Keep old file.")
        else:
            with open(args.merge[2], "w", encoding="utf-8-sig") as f:
                json.dump(subtitles_merge, f, ensure_ascii=False, indent="  ")
            print(f"{args.merge[2]} saved.")

    else:
        print("Processing normal subtitles...")
        subtitles_normal = get_normal_subtitles()
        if Path(FILENAME_NORMAL).exists():
            overwrite = input(f"{FILENAME_NORMAL} already exists, are you sure to overwrite it? (y/n), default n: ")
            if overwrite == "y":
                with open(FILENAME_NORMAL, "w", encoding="utf-8-sig") as f:
                    json.dump(subtitles_normal, f, ensure_ascii=False, indent="  ")
                print(f"{FILENAME_NORMAL} saved.")
            else:
                print("Keep old file.")
        else:
            with open(FILENAME_NORMAL, "w", encoding="utf-8-sig") as f:
                json.dump(subtitles_normal, f, ensure_ascii=False, indent="  ")
            print(f"{FILENAME_NORMAL} saved.")
