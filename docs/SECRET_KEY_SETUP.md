# 🔐 SECRET_KEY Setup Guide

## Generate New SECRET_KEY

Run this command to generate a secure random key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Update .env File

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` and replace `SECRET_KEY` with generated key:
```env
SECRET_KEY=your-generated-key-here
```

## Important Notes

⚠️ **NEVER commit `.env` to Git!**
- `.env` is in `.gitignore`
- Only commit `.env.example` (without real keys)

⚠️ **Change SECRET_KEY in production!**
- Use different key for development and production
- Never share your SECRET_KEY

⚠️ **If SECRET_KEY is exposed:**
1. Generate new key immediately
2. Update `.env` with new key
3. Restart application
4. All users will need to re-login

## Verify Setup

Check if SECRET_KEY is loaded:
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('OK' if os.getenv('SECRET_KEY') else 'MISSING')"
```

Should output: `OK`
