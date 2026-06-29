# mp4tosrt

掃描 `mp4` 目錄中的媒體檔，為**尚未產生字幕**的 .mp4 / .mp3 自動生成 .srt 字幕與 .txt 逐字稿（使用 MLX Whisper，適合 Apple Silicon）。

## 功能

- 掃描 `mp4/` 目錄（含子目錄）內所有 .mp4、.mp3
- 若同路徑下已有同名 .srt，則跳過
- 僅對沒有 .srt 的檔案進行語音辨識，並同時寫入 .srt（含時間軸）與 .txt（純文字逐字稿）
- 強制指定中文辨識，並以 OpenCC 轉為繁體（台灣用字）

## 環境需求

- macOS（建議 Apple Silicon 以使用 MLX 加速）
- Python 3.x
- [ffmpeg](https://ffmpeg.org/)（mlx-whisper 讀取音訊所需）

```bash
brew install ffmpeg
```

## 使用方式

### 首次設定

```bash
# 複製專案（若尚未取得）
git clone git@github.com:DevinY/mp4tosrt.git
cd mp4tosrt

# 建立虛擬環境並安裝依賴
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 執行（推薦）

將 .mp4 或 .mp3 放入 `mp4/` 目錄（可含子目錄），然後執行：

```bash
./start.sh
```

`start.sh` 會自動啟用 `venv/bin/activate` 並執行 `python run.py`。

### 手動執行

```bash
source venv/bin/activate
python run.py
```

### 執行結果

- 成功：在同目錄產生同名 `.srt` 與 `.txt`（例如 `mp4/foo/bar.mp4` → `mp4/foo/bar.srt`、`mp4/foo/bar.txt`）
- 已存在 `.srt`：跳過該檔案（若需重新產生，請先刪除對應的 `.srt`）
- 檔案損壞（如 moov atom not found）：略過並顯示錯誤訊息

## 目錄結構

```
mp4tosrt/
├── mp4/              # 放 .mp4 / .mp3，生成的 .srt、.txt 會與原檔同目錄
├── run.py
├── start.sh          # 一鍵啟動（自動 activate venv 並執行）
├── requirements.txt
└── README.md
```
