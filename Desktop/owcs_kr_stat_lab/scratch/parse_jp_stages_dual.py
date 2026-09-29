import urllib.request
import urllib.parse
import gzip
import json
import re
import time

stages = [
    ('2024_Stage_1', 'Overwatch_Champions_Series/2024/Asia/Stage_1/Japan'),
    ('2024_Stage_2', 'Overwatch_Champions_Series/2024/Asia/Stage_2/Japan'),
    ('2025_Stage_1', 'Overwatch_Champions_Series/2025/Asia/Stage_1/Japan'),
    ('2025_Stage_2', 'Overwatch_Champions_Series/2025/Asia/Stage_2/Japan'),
    ('2025_Stage_3', 'Overwatch_Champions_Series/2025/Asia/Stage_3/Japan'),
    ('2026_Stage_1', 'Overwatch_Champions_Series/2026/Asia/Stage_1/Japan'),
    ('2026_Stage_2', 'Overwatch_Champions_Series/2026/Asia/Stage_2/Japan'),
    ('2026_Stage_3', 'Overwatch_Champions_Series/2026/Asia/Stage_3/Japan')
]

def fetch_wikitext_safe(page):
    encoded = urllib.parse.quote(page.replace(' ', '_'))
    url = f'https://liquipedia.net/overwatch/api.php?action=parse&page={encoded}&prop=wikitext&format=json'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'OWCSStatLab/1.0 (Educational research; owcs_kr_stat_lab; contact@statlab.local)',
        'Accept-Encoding': 'gzip'
    })
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req) as resp:
                raw = resp.read()
                content = gzip.decompress(raw).decode('utf-8') if resp.info().get('Content-Encoding') == 'gzip' else raw.decode('utf-8')
                return json.loads(content).get('parse', {}).get('wikitext', {}).get('*', '')
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_sec = 25 * (attempt + 1)
                print(f'Rate limited on {page}, waiting {wait_sec}s (attempt {attempt+1})...')
                time.sleep(wait_sec)
            else:
                print(f'HTTP Error {e.code} on {page}: {e}')
                return ''
        except Exception as e:
            print(f'Error fetching {page}: {e}')
            return ''
    return ''

def normalize_role(role_str):
    r = role_str.lower()
    if 'tank' in r:
        return 'TANK'
    elif 'dps' in r:
        return 'DPS'
    elif 'sup' in r:
        return 'SPT'
    elif 'flex' in r:
        return 'FLEX'
    return role_str.title()

def parse_wikitext_rosters(wt):
    teams = {}
    
    # 1. Try {{TeamCard
    cards = wt.split('{{TeamCard')
    for card in cards[1:]:
        end_idx = card.find('\n}}\n')
        block = card[:end_idx] if end_idx != -1 else card[:2000]
        
        m_team = re.search(r'\|team=([^\n\|\}]+)', block)
        if not m_team:
            continue
        team_name = m_team.group(1).strip()
        
        players = {}
        staff = {}
        
        # Players: |p1=Name|pos1=role or |t3p1=Name|t3p1pos=role
        # Let's find all |p(\d+)=([^|\n]+) and |pos(\d+)=([^|\n]+)
        p_ids = dict(re.findall(r'\|p(\d+)=([^\|\n\}]+)', block))
        p_roles = dict(re.findall(r'\|pos(\d+)=([^\|\n\}]+)', block))
        for num, pid in p_ids.items():
            clean_id = re.sub(r'\[\[.*?\|(.*?)\]\]', r'\1', pid)
            clean_id = re.sub(r'\[\[(.*?)\]\]', r'\1', clean_id).strip()
            role = p_roles.get(num, 'unknown')
            players[clean_id] = normalize_role(role)
            
        # Subs: |t3p(\d+)=
        sub_ids = dict(re.findall(r'\|t3p(\d+)=([^\|\n\}]+)', block))
        sub_roles = dict(re.findall(r'\|t3p(\d+)pos=([^\|\n\}]+)', block))
        for num, pid in sub_ids.items():
            clean_id = re.sub(r'\[\[.*?\|(.*?)\]\]', r'\1', pid)
            clean_id = re.sub(r'\[\[(.*?)\]\]', r'\1', clean_id).strip()
            role = sub_roles.get(num, 'unknown')
            players[clean_id] = normalize_role(role)
            
        # Staff: |t2c(\d+)= and |t2c(\d+)pos=
        c_ids = dict(re.findall(r'\|t2c(\d+)=([^\|\n\}]+)', block))
        c_roles = dict(re.findall(r'\|t2c(\d+)pos=([^\|\n\}]+)', block))
        for num, cid in c_ids.items():
            clean_id = re.sub(r'\[\[.*?\|(.*?)\]\]', r'\1', cid)
            clean_id = re.sub(r'\[\[(.*?)\]\]', r'\1', clean_id).strip()
            role = c_roles.get(num, 'Coach')
            staff[clean_id] = role.title()
            
        if players or staff:
            teams[team_name] = {'PLAYERS': players, 'STAFF': staff}
            
    # 2. Try {{Opponent|
    opps = wt.split('{{Opponent|')
    for opp in opps[1:]:
        end_idx = opp.find('\n}}\n')
        block = opp[:end_idx] if end_idx != -1 else opp[:2000]
        lines = block.split('\n')
        team_name = lines[0].strip()
        
        players = {}
        staff = {}
        
        persons = re.findall(r'\{\{Person\|([^\|\}]+)(.*?)\}\}', block)
        for pid, meta in persons:
            meta_dict = {}
            for item in meta.split('|'):
                if '=' in item:
                    k, v = item.split('=', 1)
                    meta_dict[k.strip().lower()] = v.strip().lower()
            
            p_type = meta_dict.get('type', 'player')
            role = meta_dict.get('role', 'unknown')
            
            clean_id = pid.strip()
            if p_type == 'staff' or 'coach' in role or 'manager' in role:
                staff[clean_id] = role.title()
            else:
                players[clean_id] = normalize_role(role)
                
        if (players or staff) and team_name not in teams:
            teams[team_name] = {'PLAYERS': players, 'STAFF': staff}
            
    return teams

all_stage_data = {}

for stg_label, stg_page in stages:
    print(f'Fetching {stg_label} from {stg_page}...')
    time.sleep(2.5)
    wt = fetch_wikitext_safe(stg_page)
    if not wt:
        print(f'  [-] Failed for {stg_label}')
        continue
    teams = parse_wikitext_rosters(wt)
    all_stage_data[stg_label] = teams
    print(f'  [+] Successfully parsed {len(teams)} teams for {stg_label}: {list(teams.keys())}')

with open('scratch/jp_stage_rosters_dual.json', 'w', encoding='utf-8') as f:
    json.dump(all_stage_data, f, ensure_ascii=False, indent=2)

print('ALL DONE! Saved to scratch/jp_stage_rosters_dual.json')
