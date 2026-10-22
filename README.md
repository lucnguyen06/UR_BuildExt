# UR_BuildExt - Google Drive Upload Script

Công cụ tự động upload ROM Xiaomi lên Google Drive thông qua Google Drive API.

## 📋 Yêu cầu

- Python 3.8+
- Dependencies: `google-auth-oauthlib`, `google-api-python-client`

```bash
pip install google-auth-oauthlib google-api-python-client
```

## 🔧 Setup

### 1. Tạo Google OAuth Credentials

1. Vào [Google Cloud Console](https://console.cloud.google.com)
2. Tạo project hoặc chọn existing project
3. Enable **Google Drive API**
4. Tạo **OAuth 2.0 Desktop Application** credentials
5. Download JSON file → đặt thành `credentials.json` cạnh script này

### 2. Tạo Token

Chạy script tạo token:

```bash
python gen_token.py
```

Script sẽ:
- Mở browser để bạn đăng nhập Google
- Yêu cầu cấp quyền **full Drive access**
- Lưu token vào `token.pickle`

⚠️ **IMPORTANT:** `token.pickle` chứa access token - **KHÔNG COMMIT LÊN GIT!**

## 📤 Upload file

```bash
python upload_rom_api.py <file_path> \
  --folder_id <google_drive_folder_id> \
  --path <subfolder/path> \
  --share \
  --link_out <output_file>
```

### Tham số:

| Tham số | Mô tả | Ví dụ |
|--------|-------|-------|
| `file_path` | Đường dẫn file upload | `/path/to/rom.zip` |
| `--folder_id` | Google Drive folder ID | `1hxTHOs5ua7Q5uWs236hGW_6X7jxaifKq` |
| `--path` | Tạo subfolder | `xiaomi/13/` |
| `--share` | Chia sẻ công khai (optional) | `--share` |
| `--link_out` | Lưu download link vào file (optional) | `--link_out download_link.txt` |

### Ví dụ:

```bash
python upload_rom_api.py rom.zip \
  --folder_id "1hxTHOs5ua7Q5uWs236hGW_6X7jxaifKq" \
  --path "builds/2026-10/" \
  --share \
  --link_out link.txt
```

## 🔐 GitHub Actions

### Setup Secret

Encode `token.pickle` thành base64 và lưu vào GitHub Secret:

**Windows PowerShell:**
```powershell
[Convert]::ToBase64String([System.IO.File]::ReadAllBytes("token.pickle")) | Set-Clipboard
```

**Linux/Mac:**
```bash
cat token.pickle | base64 | pbcopy  # macOS
cat token.pickle | base64 | xclip   # Linux
```

1. Vào repo Settings → Secrets and variables → Actions
2. Click **New repository secret**
3. Name: `TOKEN_PICKLE_B64`
4. Value: Dán base64 string
5. Click **Add secret**

### Workflow

Workflow sẽ tự động:
1. Decode `TOKEN_PICKLE_B64` → `token.pickle`
2. Sử dụng script upload_rom_api.py
3. Upload ROM lên Google Drive

## 🐛 Troubleshooting

### "invalid_client: The provided client secret is invalid"

→ Client ID/Secret đã hết hạn hoặc bị revoke  
→ Tạo credentials mới từ Google Cloud Console  
→ Chạy lại `python gen_token.py`

### "403 insufficientParentPermissions"

→ Token được tạo với scope `drive.file` (limited)  
→ Tạo lại token với full `drive` scope  
→ Chạy `python gen_token.py` lại

### "file not found: token.pickle"

→ Chạy `python gen_token.py` trước để tạo token

## 📝 Files

- `upload_rom_api.py` - Main upload script
- `gen_token.py` - Tạo/refresh token
- `token.pickle` - OAuth token (local, không commit)
- `credentials.json` - Google credentials (local, không commit)
- `.gitignore` - Bảo vệ sensitive files

## 📄 License

MIT
