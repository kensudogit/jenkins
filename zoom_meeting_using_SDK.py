import requests																																		
import random																																		
import json																																		
from collections import defaultdict																																		
																																		
# Zoom APIの認証情報																																		
API_KEY = 'YOUR_API_KEY'																																		
API_SECRET = 'YOUR_API_SECRET'																																		
MEETING_ID = 'YOUR_MEETING_ID'																																		
TOKEN = 'YOUR_ACCESS_TOKEN'  # OAuthで取得したアクセストークン																																		
																																		
def create_breakout_rooms(participants, num_rooms, previous_groups):																																		
    def is_duplicate(group, previous_groups):																																		
        return any(set(group) == set(prev_group) for prev_group in previous_groups)																																		
    																																		
    def generate_groups():																																		
        shuffled_participants = participants[:]																																		
        random.shuffle(shuffled_participants)																																		
        groups = [shuffled_participants[i::num_rooms] for i in range(num_rooms)]																																		
        return groups																																		
																																		
    new_groups = []																																		
    attempts = 0																																		
    max_attempts = 1000																																		
																																		
    while attempts < max_attempts:																																		
        attempts += 1																																		
        new_groups = generate_groups()																																		
        if not any(is_duplicate(group, previous_groups) for group in new_groups):																																		
            break																																		
    else:																																		
        print("Could not find a non-duplicate arrangement after maximum attempts.")																																		
    																																		
    return new_groups																																		
																																		
def schedule_breakout_sessions(participants, num_rooms, num_sessions):																																		
    previous_groups = []																																		
    all_sessions = []																																		
																																		
    for session in range(num_sessions):																																		
        new_groups = create_breakout_rooms(participants, num_rooms, previous_groups)																																		
        if not new_groups:																																		
            print(f"Session {session + 1}: Unable to create non-duplicate groups.")																																		
            break																																		
        all_sessions.append(new_groups)																																		
        previous_groups.extend(new_groups)																																		
    																																		
    return all_sessions																																		
																																		
def set_breakout_rooms(meeting_id, breakout_rooms, token):																																		
    url = f"https://api.zoom.us/v2/meetings/{meeting_id}/livestream/status"																																		
    headers = {																																		
        "Authorization": f"Bearer {token}",																																		
        "Content-Type": "application/json"																																		
    }																																		
    payload = {																																		
        "breakout_rooms": [																																		
            {																																		
                "name": f"Room {i+1}",																																		
                "participants": group																																		
            } for i, group in enumerate(breakout_rooms)																																		
        ]																																		
    }																																		
    response = requests.post(url, headers=headers, data=json.dumps(payload))																																		
    if response.status_code == 201:																																		
        print("Breakout rooms created successfully!")																																		
    else:																																		
        print(f"Error creating breakout rooms: {response.status_code}")																																		
        print(response.json())																																		
																																		
# 参加者リスト（日本語を含む）																																		
participants = ["山田", "大谷", "長嶋", "鈴木", "足立", "尾上", "一ノ瀬", "中森", "近藤", "柳瀬"]																																		
																																		
# ブレイクアウトルームの数																																		
num_rooms = 3																																		
																																		
# ブレイクアウトセッションの回数																																		
num_sessions = 5																																		
																																		
# ブレイクアウトセッションをスケジュール																																		
sessions = schedule_breakout_sessions(participants, num_rooms, num_sessions)																																		
																																		
# 各セッションのブレイクアウトルームを設定																																		
for i, session in enumerate(sessions, 1):																																		
    print(f"Setting breakout rooms for session {i}...")																																		
    set_breakout_rooms(MEETING_ID, session, TOKEN)																																		
