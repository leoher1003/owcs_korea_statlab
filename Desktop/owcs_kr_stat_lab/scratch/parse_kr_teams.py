import urllib.request
import urllib.parse
import gzip
import json
from bs4 import BeautifulSoup
import re
import time

def fetch_page(title):
    encoded = urllib.parse.quote(title.replace(' ', '_'))
    url = f'https://liquipedia.net/overwatch/api.php?action=parse&page={encoded}&prop=text|wikitext&format=json'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'OWCSStatLab/1.0 (Educational research; owcs_kr_stat_lab; test@example.com)',
        'Accept-Encoding': 'gzip'
    })
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            content = gzip.decompress(raw).decode('utf-8') if resp.info().get('Content-Encoding') == 'gzip' else raw.decode('utf-8')
            return json.loads(content)
    except Exception as e:
        return {'error': str(e)}

teams_to_parse = [
    ('Vesta Esports Crew', 'Vesta Crew'),
    ('Sin Prisa Gaming', 'Sin Prisa Gaming'),
    ('FNATIC', 'Fnatic'),
    ('HaeJeokDan', 'HaeJeokDan'),
    ('Old Ocean', 'Old Ocean'),
    ('New Era', 'New Era'),
    ('WAY', 'WAY'),
    ('All Gamers Global', 'All Gamers Global'),
    ('ONSIDE GAMING', 'ONSIDE GAMING'),
    ('WAE', 'WAY'),
    ('Mir Gaming', 'Mir Gaming'),
]

results = {}

for team_key, page in teams_to_parse:
    time.sleep(1.0)
    data = fetch_page(page)
    if 'error' in data or 'parse' not in data:
        results[team_key] = {'error': data.get('error', 'no parse')}
        continue
    
    wt = data['parse']['wikitext']['*']
    soup = BeautifulSoup(data['parse']['text']['*'], 'html.parser')
    
    # 1. Disbanded
    m_dis = re.search(r'\|disbanded=([^\n\|\}]+)', wt)
    dis_date = m_dis.group(1).strip() if m_dis else None
    
    # 2. Extract intro text
    first_p = ''
    for p in soup.find_all('p'):
        t = p.get_text(strip=True)
        if len(t) > 30 and team_key.lower().replace(' ', '') in t.lower().replace(' ', ''):
            first_p = t
            break
    
    # 3. Former players and staff
    former_players = []
    former_staff = []
    
    # Find all table2__table
    for table in soup.find_all('table', class_='table2__table'):
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        if 'ID' in headers and 'Leave Date' in headers:
            # Check section heading
            prev_h = table.find_previous(['h2', 'h3', 'div'], class_=re.compile(r'mw-heading'))
            prev_text = prev_h.get_text(strip=True) if prev_h else ''
            
            # Find whether this is under Organization or Player Roster
            parent_h2 = table.find_previous(['div'], class_='mw-heading2')
            parent_h2_text = parent_h2.get_text(strip=True) if parent_h2 else ''
            
            is_org = 'Organization' in prev_text or 'Organization' in parent_h2_text
            
            for tr in table.find_all('tr')[1:]:
                cols = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                if len(cols) >= 5:
                    entry = {
                        'id': re.sub(r'\[\d+\]', '', cols[0]).strip(),
                        'name': cols[1],
                        'role': re.sub(r'\[\d+\]', '', cols[2]).strip(),
                        'join': re.sub(r'\[\d+\]', '', cols[3]).strip(),
                        'leave': re.sub(r'\[\d+\]', '', cols[4]).strip(),
                        'new_team': cols[5] if len(cols) > 5 else ''
                    }
                    if is_org:
                        former_staff.append(entry)
                    else:
                        former_players.append(entry)
                        
    results[team_key] = {
        'disbanded': dis_date,
        'intro': first_p,
        'players': former_players,
        'staff': former_staff
    }

with open('scratch/kr_teams_parsed.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print('SUCCESS! Saved to scratch/kr_teams_parsed.json')
