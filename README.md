# mp4tosrt

掃描 `mp4` 目錄中的影片，為**尚未產生字幕**的 .mp4 自動生成 .srt 字幕檔（使用 MLX Whisper，適合 Apple Silicon）。

## 功能

- 掃描 `mp4/` 目錄（含子目錄）內所有 .mp4
- 若同路徑下已有同名 .srt，則跳過
- 僅對沒有 .srt 的影片進行語音辨識並寫入 .srt
- 使用繁體中文提示，產出繁體字幕

## 環境需求

- macOS（建議 Apple Silicon 以使用 MLX 加速）
- Python 3.x
- 虛擬環境（建議）

## 使用方式

```bash
# 複製專案（若尚未取得）
git clone git@github.com:DevinY/mp4tosrt.git
cd mp4tosrt

# 啟動虛擬環境
source venv/bin/activate

# 安裝依賴（首次或更新時）
pip install mlx-whisper

# 執行：為 mp4 目錄中未生成 srt 的影片生成字幕
python run.py
```

## 目錄結構

```
mp4tosrt/
├── mp4/          # 放 .mp4 影片，生成的 .srt 會與影片同檔名同目錄
├── run.py
├── requirements.txt
└── README.md
```

將影片放入 `mp4/`（可含子目錄），執行 `python run.py` 後，缺少 .srt 的影片會自動產生對應的 .srt 檔。
