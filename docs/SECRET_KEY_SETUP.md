# Setup SECRET_KEY

## Bikin SECRET_KEY Baru

Jalanin command ini buat generate key random yang aman:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Update File .env

1. Copy `.env.example` ke `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` dan ganti `SECRET_KEY` dengan key yang udah di-generate:
```env
SECRET_KEY=your-generated-key-here
```

## Catatan Penting

**JANGAN PERNAH commit `.env` ke Git!**
- `.env` udah ada di `.gitignore`
- Cuma commit `.env.example` (tanpa key beneran)

**Ganti SECRET_KEY di production!**
- Pake key yang beda buat development dan production
- Jangan pernah share SECRET_KEY kamu

**Kalau SECRET_KEY bocor:**
1. Generate key baru secepatnya
2. Update `.env` dengan key baru
3. Restart aplikasi
4. Semua user harus re-login

## Verifikasi Setup

Cek apakah SECRET_KEY udah ke-load:
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('OK' if os.getenv('SECRET_KEY') else 'MISSING')"
```

Harusnya output: `OK`
