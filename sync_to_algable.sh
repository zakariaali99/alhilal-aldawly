#!/bin/bash
# Sync script: Copy code changes from alhilal to algable2alakhter
# Preserves: database, media files, branding (colors, logo, company name)

set -e

SOURCE="/Users/zakaria/projects/antigravity/alhilal"
TARGET="/Users/zakaria/projects/antigravity/alhilal/algable2alakhter"

echo "🔄 Syncing changes from alhilal to algable2alakhter..."

# Check if target exists
if [ ! -d "$TARGET" ]; then
    echo "❌ Target directory does not exist. Run setup_algable.sh first."
    exit 1
fi

# Backup algable-specific files before sync
echo "📦 Backing up Algable-specific files..."
mkdir -p /tmp/algable_backup
cp "$TARGET/static/css/main.css" /tmp/algable_backup/main.css 2>/dev/null || true
cp "$TARGET/static/images/logo_clean.png" /tmp/algable_backup/logo_clean.png 2>/dev/null || true
cp "$TARGET/static/images/favicon.png" /tmp/algable_backup/favicon.png 2>/dev/null || true

# Sync Python files (views, models, urls, etc.)
echo "🐍 Syncing Python files..."
rsync -av --exclude='__pycache__' --exclude='*.pyc' --exclude='migrations' \
    "$SOURCE/core/" "$TARGET/core/"
rsync -av --exclude='__pycache__' --exclude='*.pyc' --exclude='migrations' \
    "$SOURCE/livestock/" "$TARGET/livestock/"
rsync -av --exclude='__pycache__' --exclude='*.pyc' --exclude='migrations' \
    "$SOURCE/news/" "$TARGET/news/"
rsync -av --exclude='__pycache__' --exclude='*.pyc' --exclude='migrations' \
    "$SOURCE/dashboard/" "$TARGET/dashboard/"

# Sync templates
echo "📄 Syncing templates..."
rsync -av "$SOURCE/templates/" "$TARGET/templates/"

# Sync static files (except CSS main.css and logo)
echo "🎨 Syncing static files..."
rsync -av --exclude='main.css' --exclude='logo_clean.png' --exclude='favicon.png' --exclude='algable_logo.png' \
    "$SOURCE/static/" "$TARGET/static/"

# Restore Algable-specific CSS (preserving color scheme)
echo "🎨 Restoring Algable color scheme..."
if [ -f /tmp/algable_backup/main.css ]; then
    cp /tmp/algable_backup/main.css "$TARGET/static/css/main.css"
else
    # If no backup, copy from source and update colors
    cp "$SOURCE/static/css/main.css" "$TARGET/static/css/main.css"
    # Update Algable colors
    sed -i '' 's/--primary: #C5A059;/--primary: #cdad7d;/g' "$TARGET/static/css/main.css"
    sed -i '' 's/--primary-dark: #A6803F;/--primary-dark: #b89a6a;/g' "$TARGET/static/css/main.css"
    sed -i '' 's/--black: #FAFAFA;/--black: #f4f1ec;/g' "$TARGET/static/css/main.css"
fi

# Restore Algable logo
echo "🖼️ Restoring Algable logo..."
if [ -f /tmp/algable_backup/logo_clean.png ]; then
    cp /tmp/algable_backup/logo_clean.png "$TARGET/static/images/logo_clean.png"
fi
if [ -f /tmp/algable_backup/favicon.png ]; then
    cp /tmp/algable_backup/favicon.png "$TARGET/static/images/favicon.png"
fi

# Update company names in synced templates
echo "🏷️ Updating company names in templates..."
find "$TARGET/templates" -type f -name "*.html" -exec sed -i '' 's/الهلال الدولي/الجبل الأخضر/g' {} +
find "$TARGET/templates" -type f -name "*.html" -exec sed -i '' 's/Alhilal International/Algable Alakhter/g' {} +
find "$TARGET/templates" -type f -name "*.html" -exec sed -i '' 's/Alhilal/Algable Alakhter/g' {} +

# Clean up backup
rm -rf /tmp/algable_backup

echo "✅ Sync complete!"
echo ""
echo "Files preserved:"
echo "  - Database (db.sqlite3)"
echo "  - Media files (media/)"
echo "  - Color scheme (main.css)"
echo "  - Logo (logo_clean.png)"
echo "  - Company name (replaced in templates)"
echo ""
echo "You may need to run migrations if models changed:"
echo "  cd $TARGET && python3 manage.py migrate"
