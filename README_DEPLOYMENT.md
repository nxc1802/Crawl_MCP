# Hướng Dẫn Deploy Lên Vercel

## 📋 Yêu Cầu

- Tài khoản Vercel (miễn phí tại [vercel.com](https://vercel.com))
- Git repository (GitHub, GitLab, hoặc Bitbucket)
- Vercel CLI (tùy chọn): `npm i -g vercel`

## 🚀 Cách Deploy

### Phương Pháp 1: Deploy Qua Vercel Dashboard (Khuyên Dùng)

1. **Push code lên Git repository:**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Đăng nhập Vercel:**
   - Truy cập [vercel.com](https://vercel.com)
   - Đăng nhập bằng GitHub/GitLab/Bitbucket

3. **Import Project:**
   - Click "Add New" → "Project"
   - Chọn repository của bạn
   - Click "Import"

4. **Configure Project:**
   - Framework Preset: `Other`
   - Root Directory: `./` (mặc định)
   - Build Command: để trống
   - Output Directory: để trống
   - Install Command: `pip install -r requirements.txt`

5. **Deploy:**
   - Click "Deploy"
   - Đợi build hoàn tất (2-3 phút)
   - Vercel sẽ cung cấp URL public

### Phương Pháp 2: Deploy Qua Vercel CLI

1. **Cài đặt Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Login:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   cd /path/to/Crawl_MCP
   vercel
   ```

4. **Follow the prompts:**
   - Set up and deploy? `Y`
   - Which scope? Choose your account
   - Link to existing project? `N`
   - What's your project's name? `crawl-mcp` (hoặc tên khác)
   - In which directory is your code located? `./`
   - Want to override the settings? `N`

5. **Production Deploy:**
   ```bash
   vercel --prod
   ```

## 🔧 Cấu Hình

### Environment Variables (Tùy Chọn)

Nếu cần tùy chỉnh, thêm environment variables trong Vercel Dashboard:

- `PORT`: `8080` (mặc định)
- `DEBUG`: `False`
- `MAX_PAGES`: `50`
- `MAX_RETRIES`: `3`
- `TIMEOUT`: `30`

### File Quan Trọng

1. **vercel.json** - Cấu hình Vercel:
   - Định nghĩa Python runtime
   - Routes và endpoints
   - Environment variables

2. **requirements.txt** - Python dependencies:
   - Đã tối ưu cho serverless
   - Loại bỏ các gói không cần thiết
   - Phiên bản tương thích Python 3.11

3. **api/** - Serverless functions:
   - `index.py` - Main entry point + web UI
   - `scrape.py` - Scraping endpoint
   - `health.py` - Health check

## 📊 API Endpoints

Sau khi deploy, bạn có các endpoints:

- **GET /** - Web interface
- **GET /health** - Health check
- **POST /api/scrape** - Scraping endpoint
- **GET /stats** - Statistics
- **GET /config** - Configuration

### Ví Dụ Sử Dụng API

```bash
# Health check
curl https://your-app.vercel.app/health

# Scrape a website
curl -X POST https://your-app.vercel.app/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "extract_types": ["text", "images", "links", "metadata"]
  }'
```

## 🐛 Troubleshooting

### Lỗi Build

1. **"Failed to install dependencies":**
   - Kiểm tra `requirements.txt` có đúng format
   - Đảm bảo tất cả packages có wheel cho Python 3.11

2. **"Module not found":**
   - Kiểm tra imports trong `api/` files
   - Đảm bảo `sys.path.insert(0, ...)` đúng

3. **"Function timeout":**
   - Vercel có giới hạn 10s cho Hobby plan
   - Cân nhắc upgrade plan hoặc tối ưu scraping

### Lỗi Runtime

1. **"Cannot write to filesystem":**
   - Vercel serverless là read-only
   - Không thể lưu file vào `data/` hoặc `logs/`
   - Sử dụng database hoặc cloud storage thay thế

2. **"Memory limit exceeded":**
   - Giảm số lượng pages scrape mỗi request
   - Tối ưu data structures

## ⚠️ Giới Hạn Vercel

### Hobby Plan (Free):
- ✅ Unlimited deployments
- ✅ SSL certificates
- ✅ 100GB bandwidth/month
- ⚠️ 10s function timeout
- ⚠️ 1024MB memory
- ⚠️ Read-only filesystem

### Pro Plan ($20/month):
- ✅ 60s function timeout
- ✅ 3008MB memory
- ✅ 1TB bandwidth
- ✅ Advanced analytics

## 🎯 Best Practices

1. **Tối ưu hiệu suất:**
   - Scrape ít pages mỗi request
   - Cache results khi có thể
   - Sử dụng external storage cho data lớn

2. **Bảo mật:**
   - Thêm rate limiting
   - Validate inputs
   - Sanitize URLs

3. **Monitoring:**
   - Sử dụng Vercel Analytics
   - Log errors properly
   - Set up alerts

## 📝 Cập Nhật Deploy

### Auto Deploy (Recommended):
- Mọi push lên branch `main` sẽ tự động deploy

### Manual Deploy:
```bash
vercel --prod
```

## 🆘 Support

Nếu gặp vấn đề:

1. Check Vercel build logs
2. Check function logs trong Vercel Dashboard
3. Test locally trước khi deploy:
   ```bash
   vercel dev
   ```

## ✅ Checklist Trước Khi Deploy

- [ ] Đã test local: `python main.py`
- [ ] Requirements.txt đã tối ưu
- [ ] Không có hardcoded paths
- [ ] Không có file I/O trong serverless functions
- [ ] Git repository đã push
- [ ] Environment variables đã set (nếu cần)
- [ ] .gitignore và .vercelignore đã cấu hình

## 🎉 Hoàn Tất!

Sau khi deploy thành công, bạn sẽ có:
- ✅ Public URL cho web scraper
- ✅ API endpoints có thể integrate
- ✅ Auto-deployment từ Git
- ✅ SSL certificate miễn phí
- ✅ Global CDN

Happy Scraping! 🚀

