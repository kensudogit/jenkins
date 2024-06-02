# main.py
import csv

from zoom_breakout import run_zoom_breakout

if __name__ == "__main__":
    # 参加者リスト（日本語を含む）
    filename = 'populationdata.csv'
    
    with open(filename, encoding='utf8', newline='') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            participants = row
    #ダミーデータセット
    if len(participants) == 0:
        participants = ["山田", "大谷", "長嶋", "鈴木", "足立", "尾上", "一ノ瀬", "中森", "近藤", "柳瀬"]

    # ブレイクアウトルームの数
    num_rooms = 3

    # ブレイクアウトセッションの回数
    num_sessions = 5

    # Zoom APIの認証情報
    API_KEY = 'YOUR_API_KEY'
    API_SECRET = 'YOUR_API_SECRET'
    MEETING_ID = 'YOUR_MEETING_ID'
    TOKEN = 'YOUR_ACCESS_TOKEN'  # OAuthで取得したアクセストークン

    # ブレイクアウトセッションを実行
    run_zoom_breakout(participants, num_rooms, num_sessions, MEETING_ID, TOKEN)
