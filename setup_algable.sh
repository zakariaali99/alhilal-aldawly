#!/bin/bash
# Setup script for Algable Alakhter company website
# Run this script from the alhilal parent directory

set -e

echo "🏔️ Setting up Algable Alakhter company website..."

# Create new project directory
PROJECT_DIR="/Users/zakaria/projects/antigravity/algable2alakhter"

if [ -d "$PROJECT_DIR" ]; then
    echo "⚠️  Directory already exists. Removing..."
    rm -rf "$PROJECT_DIR"
fi

echo "📁 Copying project files..."
cp -r /Users/zakaria/projects/antigravity/alhilal "$PROJECT_DIR"

echo "🎨 Updating color scheme..."
cd "$PROJECT_DIR"

# Update CSS colors
sed -i '' 's/--primary: #C5A059;/--primary: #cdad7d;/g' static/css/main.css
sed -i '' 's/--primary-dark: #A6803F;/--primary-dark: #b89a6a;/g' static/css/main.css
sed -i '' 's/--black: #FAFAFA;/--black: #f4f1ec;/g' static/css/main.css

# Add green color variable after primary-dark
sed -i '' 's/--primary-dark: #b89a6a;/--primary-dark: #b89a6a;\n    --secondary: #2d7a3e;/g' static/css/main.css

echo "🏷️ Updating company name..."
# Update Arabic name
find templates -type f -name "*.html" -exec sed -i '' 's/الهلال الدولي/الجبل الأخضر/g' {} +

# Update English name
find templates -type f -name "*.html" -exec sed -i '' 's/Alhilal International/Algable Alakhter/g' {} +
find templates -type f -name "*.html" -exec sed -i '' 's/Alhilal/Algable Alakhter/g' {} +

echo "📋 Updating page titles..."
# Update base.html title
sed -i '' 's/الهلال الدولي | استيراد المواشي واللحوم/الجبل الأخضر | استيراد المواشي واللحوم/g' templates/base.html
sed -i '' 's/Alhilal.*International.*Livestock Import/Algable Alakhter | Livestock Import/g' templates/base.html

echo "🖼️ Copying logo..."
cp static/images/algable_logo.png static/images/logo_clean.png

echo "🗃️ Setting up fresh database..."
rm -f db.sqlite3
python3 manage.py migrate --no-input

echo "✅ Setup complete!"
echo ""
echo "📍 Company: شركة الجبل الأخضر لاستيراد المواشي واللحوم"
echo "📞 Phone: +218 91 800 84 32"
echo "📧 Email: algable2alakhter@gmail.com"
echo ""
echo "Next steps:"
echo "1. Create superuser: python3 manage.py createsuperuser"
echo "2. Run server: python3 manage.py runserver 8001"
echo "3. Login to admin and add content"
