# CBTアプリ with ゲーミフィケーション
import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
import json

# 定数設定
USER_DATA_FILE = "user_data.json"
RECORDS_FILE = "cbt_records.csv"

# ユーザーデータの読み込みまたは初期化
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"points": 0, "records": 0, "badges": [], "last_record_date": "", "daily_mission_done": False}

def save_user_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f)

user_data = load_user_data()

# キャラクターと背景の成長
def get_character_and_bg(points):
    if points < 10:
        return ("character_lv1.png", "bg1.png", "ヒヨコちゃん")
    elif points < 30:
        return ("character_lv2.png", "bg2.png", "成長中のヒヨコちゃん")
    else:
        return ("character_lv3.png", "bg3.png", "立派なヒヨコちゃん")

# デイリーミッション内容
def get_daily_mission():
    return "今日あった良いことを1つ書いてみよう！"

# ストリームリットUI構成
st.set_page_config(page_title="CBT with ヒヨコちゃん", layout="centered")
st.title("🐣 CBTダイアリー with ヒヨコちゃん")

# キャラクターと背景表示
char_img, bg_img, char_msg = get_character_and_bg(user_data["points"])
st.image(bg_img, use_container_width=True)  # ← 修正済み
st.image(char_img, width=200)
st.write(f"【{char_msg}】現在のポイント：{user_data['points']}pt / 記録数：{user_data['records']}回")

# デイリーミッション
st.markdown("---")
st.subheader("🌱 今日のミッション")
mission = get_daily_mission()
st.write(f"📌 ミッション: {mission}")

if not user_data.get("daily_mission_done") or user_data.get("last_record_date") != str(date.today()):
    mission_input = st.text_input("入力して達成しよう！")
    if st.button("ミッション達成！") and mission_input:
        user_data["points"] += 3
        user_data["daily_mission_done"] = True
        user_data["last_record_date"] = str(date.today())
        save_user_data(user_data)
        st.success("ミッション達成！+3pt")
else:
    st.success("今日のミッションは達成済み！")

# 思考記録フォーム
st.markdown("---")
st.subheader("📝 今日の思考記録")
with st.form("cbt_form"):
    situation = st.text_area("1. 状況")
    automatic_thought = st.text_area("2. 自動思考")
    emotion = st.text_input("3. 感情と強さ（例：不安 60）")
    balanced_thought = st.text_area("4. 適応的思考")
    submitted = st.form_submit_button("記録する")

if submitted:
    new_record = {
        "日時": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "状況": situation,
        "自動思考": automatic_thought,
        "感情": emotion,
        "適応的思考": balanced_thought
    }

    try:
        df = pd.read_csv(RECORDS_FILE)
    except FileNotFoundError:
        df = pd.DataFrame()

    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    df.to_csv(RECORDS_FILE, index=False)

    # ポイント＆記録数更新
    user_data["records"] += 1
    user_data["points"] += 5
    user_data["last_record_date"] = str(date.today())
    user_data["daily_mission_done"] = True

    # バッジ獲得
    if user_data["records"] >= 1 and "初記録バッジ" not in user_data["badges"]:
        user_data["badges"].append("初記録バッジ")
    if user_data["records"] >= 5 and "5回記録バッジ" not in user_data["badges"]:
        user_data["badges"].append("5回記録バッジ")

    save_user_data(user_data)
    st.success("記録ありがとう！+5pt")

# 記録一覧
st.markdown("---")
st.subheader("📜 過去の記録")
try:
    df = pd.read_csv(RECORDS_FILE)
    st.dataframe(df[::-1])
except FileNotFoundError:
    st.write("まだ記録はありません。")

# バッジ表示
st.markdown("---")
st.subheader("🏅 獲得バッジ")
if user_data["badges"]:
    for badge in user_data["badges"]:
        st.write(f"✅ {badge}")
else:
    st.write("まだバッジはありません。")
