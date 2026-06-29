import gc
from pathlib import Path
import mlx_whisper
from opencc import OpenCC

# 簡體 → 繁體（台灣用字）
cc_s2t = OpenCC("s2tw")

TARGET_DIR = "mp4"
MODEL_ID = "mlx-community/whisper-large-v3-turbo"
MEDIA_EXTENSIONS = {".mp4", ".mp3"}

def format_timestamp(seconds: float):
    total_ms = int(round(seconds * 1000))
    hours = total_ms // 3600000
    minutes = (total_ms % 3600000) // 60000
    secs = (total_ms % 60000) // 1000
    millis = total_ms % 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def write_outputs(media_path: Path, result: dict) -> tuple[Path, Path]:
    srt_path = media_path.with_suffix(".srt")
    txt_path = media_path.with_suffix(".txt")
    lines: list[str] = []

    with open(srt_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(result["segments"], start=1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = cc_s2t.convert(segment["text"].strip())
            lines.append(text)
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        if lines:
            f.write("\n")

    return srt_path, txt_path

def process_media():
    target = Path(TARGET_DIR)
    media_files = sorted(
        p for p in target.rglob("*")
        if p.is_file() and p.suffix.lower() in MEDIA_EXTENSIONS
    )

    if not media_files:
        exts = ", ".join(sorted(MEDIA_EXTENSIONS))
        print(f"在 {TARGET_DIR} 目錄內找不到任何 {exts} 檔案。")
        return

    print(f"找到 {len(media_files)} 個媒體檔案，開始檢查字幕狀態...")

    for media_path in media_files:
        srt_path = media_path.with_suffix(".srt")

        if srt_path.exists():
            print(f"跳過：{media_path.name} (字幕已存在)")
            continue

        print(f"\n正在處理：{media_path}")

        try:
            # mlx_whisper 內部以 ModelHolder 快取同一 MODEL_ID，不會每檔重載權重
            result = mlx_whisper.transcribe(
                str(media_path),
                path_or_hf_repo=MODEL_ID,
                language="zh",
                task="transcribe",
                initial_prompt="以下是繁體中文字幕，使用台灣習慣用語。",
                verbose=False
            )

            srt_path, txt_path = write_outputs(media_path, result)
            print(f"✅ 成功生成字幕：{srt_path.name}、逐字稿：{txt_path.name}")

        except Exception as e:
            err = str(e)
            if "moov atom not found" in err:
                err = "檔案損壞或未完整寫入（moov atom not found）"
            elif len(err) > 200:
                err = err[:200] + "..."
            print(f"❌ 略過 {media_path.name}：{err}")
        finally:
            gc.collect()

if __name__ == "__main__":
    process_media()
    print("\n所有任務處理完畢。")
