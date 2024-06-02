# coding: utf-8
import random
import sys
from collections import defaultdict

def create_breakout_rooms(participants, num_rooms, previous_groups):
    """
    参加者を少人数のグループに分け、過去のグループと重複しないようにする。
    :param participants: 参加者リスト
    :param num_rooms: グループの数
    :param previous_groups: 過去のグループ分け情報
    :return: 新しいグループ分け
    """
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
    """
    同一ミーティング内で複数回のブレイクアウトルームをスケジュールする。
    :param participants: 参加者リスト
    :param num_rooms: ブレイクアウトルームの数
    :param num_sessions: ブレイクアウトセッションの回数
    :return: 各セッションのグループ分けリスト
    """
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

# 参加者リスト
participants = ["山田", "大谷", "長嶋", "鈴木", "足立", "尾上", "一ノ瀬", "中森", "近藤", "柳瀬"]

# ブレイクアウトルームの数
num_rooms = 3

# ブレイクアウトセッションの回数
num_sessions = 5

# ブレイクアウトセッションをスケジュール
sessions = schedule_breakout_sessions(participants, num_rooms, num_sessions)

# 各セッションの結果を表示
for i, session in enumerate(sessions, 1):
    print(f"Session {i}:")
    for j, group in enumerate(session, 1):
        print(f"  Room {j}: {group}")

# 過去のグループ分け情報を更新（次回以降のセッションのために）
previous_groups = [group for session in sessions for group in session]
