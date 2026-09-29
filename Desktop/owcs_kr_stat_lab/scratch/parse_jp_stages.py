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
                wait_sec = 20 * (attempt + 1)
                print(f'Rate limited on {page}, waiting {wait_sec}s (attempt {attempt+1})...')
                time.sleep(wait_sec)
            else:
                print(f'HTTP Error {e.code} on {page}: {e}')
                return ''
        except Exception as e:
            print(f'Error fetching {page}: {e}')
            return ''
    return ''

all_stage_data = {}

for stg_label, stg_page in stages:
    print(f'Fetching {stg_label} from {stg_page}...')
    time.sleep(2.5)
    wt = fetch_wikitext_safe(stg_page)
    if not wt:
        print(f'  [-] Failed or empty for {stg_label}')
        continue
    all_stage_data[stg_label] = {}
    
    parts = wt.split('{{Opponent|')
    for part in parts[1:]:
        opp_end = part.find('\n}}\n')
        block = part[:opp_end] if opp_end != -1 else part[:1500]
            
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
            
            if 'tank' in role:
                norm_role = 'TANK'
            elif 'dps' in role:
                norm_role = 'DPS'
            elif 'sup' in role:
                norm_role = 'SPT'
            else:
                norm_role = role.title()
                
            if p_type == 'staff' or 'coach' in role or 'manager' in role:
                staff[pid] = role.title()
            else:
                players[pid] = norm_role
                
        all_stage_data[stg_label][team_name] = {
            'PLAYERS': players,
            'STAFF': staff
        }
    print(f'  [+] Found {len(all_stage_data[stg_label])} teams in {stg_label}')

with open('scratch/jp_stage_rosters.json', 'w', encoding='utf-8') as f:
    json.dump(all_stage_data, f, ensure_ascii=False, indent=2)

print('SUCCESS! Saved to scratch/jp_stage_rosters.json')
