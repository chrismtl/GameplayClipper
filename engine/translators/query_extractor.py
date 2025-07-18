import os
import pandas as pd
import utils.constants as cst
from tools.clip_extractor import extract_clips


def translate_query(user_text):
    user_text = user_text.lower()
    if "kill" in user_text:
        return {"filter": {"event": "kill"}}
    return {"filter": {"event": "unknown"}}

def query():
    if not os.path.exists(cst.OUT_DF_DIR):
        print("❌ No event CSVs found. Run detection first.")
        return

    all_event_dfs = []
    for csv_file in os.listdir(cst.OUT_DF_DIR):
        if csv_file.endswith(".csv"):
            df = pd.read_csv(os.path.join(cst.OUT_DF_DIR, csv_file))
            all_event_dfs.append(df)

    if not all_event_dfs:
        print("❌ No event data available.")
        return

    full_event_df = pd.concat(all_event_dfs, ignore_index=True)

    print("\n💬 Ask a question (e.g. 'Kills with Vader on Endor'):")
    user_query = input(">> ")

    query = translate_query(user_query)
    print(f"\n🧠 Translated Query:\n{query}")

    filtered = query_events(full_event_df, query)
    if filtered.empty:
        print("⚠️ No matching events.")
        return

    print(f"\n🎯 Found {len(filtered)} events.")
    os.makedirs(cst.CLIPS_DIR, exist_ok=True)

    for i, row in filtered.iterrows():
        video_file = os.path.join(cst.MEDIA_DIR, row["video"])
        clip_path = os.path.join(cst.CLIPS_DIR, f"clip_{i}.mp4")
        extract_clips(pd.DataFrame([row]), video_file, clip_path, duration=cst.CLIP_DURATION)

    print("✅ Clips extracted.")


def query_events(events_df: pd.DataFrame, query: dict) -> pd.DataFrame:
    filters = query.get("filter", {})
    df = events_df.copy()

    if "event" in filters:
        df = df[df["event"] == filters["event"]]

    if "video" in filters and "video" in df.columns:
        df = df[df["video"] == filters["video"]]

    if "timestamp" in df.columns and "time_range" in filters:
        start, end = filters["time_range"]
        df = df[(df["timestamp"] >= start) & (df["timestamp"] <= end)]

    return df
