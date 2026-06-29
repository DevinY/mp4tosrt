import os
from pathlib import Path
import mlx_whisper
from datetime import timedelta
from opencc import OpenCC

# 簡體 → 繁體（台灣用字），Whisper 常輸出簡體，寫入字幕前強制轉成繁體
cc_s2t = OpenCC("s2tw")

# 設定目標目錄（如果是目前目錄下的 mp4 資料夾，就寫 "mp4"）
TARGET_DIR = "mp4" 
MODEL_ID = "mlx-community/whisper-large-v3-turbo"

def format_timestamp(seconds: float):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def process_videos():
    # rglob 遞迴搜尋，suffix.lower() 讓 .mp4 / .MP4 / .Mp4 等都能匹配
    video_files = sorted(
        str(p) for p in Path(TARGET_DIR).rglob("*")
        if p.is_file() and p.suffix.lower() == ".mp4"
    )

    if not video_files:
        print(f"在 {TARGET_DIR} 目錄內找不到任何 .mp4 檔案。")
        return

    print(f"找到 {len(video_files)} 個影片檔案，開始檢查字幕狀態...")

    for video_path in video_files:
        srt_path = os.path.splitext(video_path)[0] + ".srt"
        
        if os.path.exists(srt_path):
            print(f"跳過：{os.path.basename(video_path)} (字幕已存在)")
            continue
        
        print(f"\n正在處理：{video_path}")
        
        try:
            result = mlx_whisper.transcribe(
                video_path,
                path_or_hf_repo=MODEL_ID,
                initial_prompt="以下是繁體中文字幕。",
                verbose=False
            )

            with open(srt_path, "w", encoding="utf-8") as f:
                for i, segment in enumerate(result['segments'], start=1):
                    start = format_timestamp(segment['start'])
                    end = format_timestamp(segment['end'])
                    text = cc_s2t.convert(segment['text'].strip())
                    f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
            
            print(f"✅ 成功生成字幕：{srt_path}")

        except Exception as e:
            err = str(e)
            # 從 ffmpeg 冗長輸出中擷取關鍵錯誤（如 moov atom not found）
            if "moov atom not found" in err:
                err = "檔案損壞或未完整寫入（moov atom not found）"
            elif len(err) > 200:
                err = err[:200] + "..."
            print(f"❌ 略過 {os.path.basename(video_path)}：{err}")

if __name__ == "__main__":
    process_videos()
    print("\n所有任務處理完畢。")
