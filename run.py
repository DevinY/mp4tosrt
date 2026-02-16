import os
import glob
import mlx_whisper
from datetime import timedelta

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
    # 使用 recursive=True 讓它自動進入子資料夾尋找
    # **/*.mp4 代表找尋目前目錄及所有子目錄下的 mp4
    search_pattern = os.path.join(TARGET_DIR, "**/*.mp4")
    video_files = glob.glob(search_pattern, recursive=True)

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
                    text = segment['text'].strip()
                    f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
            
            print(f"✅ 成功生成字幕：{srt_path}")

        except Exception as e:
            print(f"❌ 處理 {video_path} 時出錯：{str(e)}")

if __name__ == "__main__":
    process_videos()
    print("\n所有任務處理完畢。")
