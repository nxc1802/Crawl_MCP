# 🚀 Hekate Quick Start Guide

## Cài đặt nhanh

1. **Cài đặt dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Chạy web interface:**
   ```bash
   python demo.py
   ```

3. **Truy cập web interface:**
   Mở http://localhost:8080 trong trình duyệt

## Sử dụng

### Web Interface
- Nhập URL website cần crawl (ví dụ: https://apec2025.kr/?menuno=1)
- Chọn loại dữ liệu cần trích xuất
- Click "Start Scraping"
- Xem kết quả real-time

### Command Line Test
```bash
python test_scraper.py
```

### API Usage
```python
from core.scraper import HekateScraper
from core.config import HekateConfig

config = HekateConfig()
scraper = HekateScraper(config)

result = scraper.scrape_single_page(
    url="https://apec2025.kr/?menuno=1",
    extract_types=['text', 'images', 'links', 'metadata']
)

print(f"Extracted {result['summary']['text_items']} text items")
```

## Tính năng chính

✅ **Universal Support**: Crawl bất kỳ website nào  
✅ **Smart Detection**: Tự động phát hiện cấu trúc website  
✅ **Anti-Detection**: Mô phỏng hành vi người dùng thực  
✅ **Multiple Extraction**: Text, images, links, metadata, tables, forms  
✅ **Web Interface**: Giao diện web thân thiện  
✅ **Error Handling**: Xử lý lỗi toàn diện  
✅ **Proxy Support**: Hỗ trợ proxy rotation  

## Cấu trúc dự án

```
Hekate/
├── core/                 # Core scraping engine
│   ├── config.py        # Configuration
│   ├── scraper.py       # Main scraper
│   ├── detector.py      # Website detection
│   └── extractor.py     # Data extraction
├── utils/               # Utility modules
│   ├── proxy_manager.py # Proxy management
│   ├── human_behavior.py # Human behavior simulation
│   └── helpers.py       # Helper functions
├── web/                 # Web interface
│   ├── app.py          # Flask application
│   └── templates/      # HTML templates
├── data/               # Scraped data storage
├── logs/               # Application logs
├── main.py             # Main entry point
├── demo.py             # Web interface demo
└── test_scraper.py     # Test script
```

## Ví dụ kết quả

Khi crawl https://apec2025.kr/?menuno=1:
- **21 text items** được trích xuất
- **26 images** được tìm thấy
- **84 links** được phát hiện
- **Website type**: social (tự động phát hiện)
- **Language**: en (tự động phát hiện)

## Troubleshooting

### Lỗi import
```bash
cd Hekate
python -c "from core.config import HekateConfig; print('OK')"
```

### Lỗi dependencies
```bash
pip install flask requests beautifulsoup4 lxml
```

### Lỗi port đã sử dụng
Thay đổi PORT trong .env hoặc config.py

## So với AWS-Scraper

| Tính năng | AWS-Scraper | Hekate |
|-----------|-------------|--------|
| Website Support | Amazon only | Universal |
| Architecture | Complex | Simple |
| Maintenance | Difficult | Easy |
| Extensibility | Limited | High |
| UI | Basic | Modern |

Hekate giữ 90% ý tưởng từ AWS-Scraper nhưng đơn giản hóa và mở rộng cho mọi website! 