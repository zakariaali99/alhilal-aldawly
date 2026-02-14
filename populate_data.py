import os
import django
from django.utils.text import slugify
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alhilal_project.settings')
django.setup()

from livestock.models import Category, LivestockItem
from news.models import Article
from core.models import HeroSection, SiteSettings

def create_sample_data():
    print("Starting data population...")

    # 1. Categories
    sheep_cat, _ = Category.objects.get_or_create(
        slug="sheep",
        defaults={
            "name_ar": "الأغنام",
            "name_en": "Sheep",
            "description_ar": "أفضل سلالات الأغنام العالمية برومانية وإسبانية",
            "description_en": "Top global sheep breeds from Romania and Spain"
        }
    )

    cattle_cat, _ = Category.objects.get_or_create(
        slug="cattle",
        defaults={
            "name_ar": "الأبقار",
            "name_en": "Cattle",
            "description_ar": "أبقار عالية الجودة للاستيراد والتربية",
            "description_en": "High-quality cattle for import and breeding"
        }
    )

    camels_cat, _ = Category.objects.get_or_create(
        slug="camels",
        defaults={
            "name_ar": "الإبل",
            "name_en": "Camels",
            "description_ar": "إبل سودانية ممتازة مختارة بعناية",
            "description_en": "Premium Sudanese camels carefully selected"
        }
    )

    # 2. Livestock Items
    LivestockItem.objects.get_or_create(
        category=sheep_cat,
        title_ar="غنم روماني ممتاز",
        title_en="Premium Romanian Sheep",
        slug="premium-romanian-sheep",
        description_ar="أغنام رومانية صحية تمت تربيتها في أفضل المزارع الطبيعية.",
        description_en="Healthy Romanian sheep raised in the finest natural pastures.",
        featured_image="livestock/romanian_sheep.png"
    )

    LivestockItem.objects.get_or_create(
        category=cattle_cat,
        title_ar="أبقار برازيلية",
        title_en="Brazilian Cattle",
        slug="brazilian-cattle",
        description_ar="أبقار برازيلية من سلالات ممتازة لإنتاج اللحوم.",
        description_en="Brazilian cattle from excellent breeds for meat production.",
        featured_image="livestock/brazilian_cattle.png"
    )

    LivestockItem.objects.get_or_create(
        category=camels_cat,
        title_ar="إبل سودانية",
        title_en="Sudanese Camels",
        slug="sudanese-camels",
        description_ar="إبل سودانية أصيلة تتميز بالقوة والجودة العالية.",
        description_en="Authentic Sudanese camels characterized by strength and high quality.",
        featured_image="livestock/sudanese_camels.png"
    )

    # 3. News Articles
    Article.objects.get_or_create(
        title_ar="افتتاح المزرعة الحديثة",
        title_en="Opening of the Modern Farm",
        slug="opening-modern-farm",
        content_ar="قمنا بافتتاح واحدة من أكثر المزارع تطوراً في المنطقة لضمان أفضل رعاية للمواشي.",
        content_en="We have opened one of the most advanced farms in the region to ensure the best care for livestock.",
        featured_image="news/modern_farm.png",
        is_published=True
    )

    Article.objects.get_or_create(
        title_ar="وصول شحنة جديدة",
        title_en="New Shipment Arrival",
        slug="new-shipment-arrival",
        content_ar="وصلت اليوم شحنة جديدة من الأغنام الرومانية الممتازة إلى ميناء مصراتة.",
        content_en="A new shipment of premium Romanian sheep arrived today at Misrata port.",
        featured_image="news/livestock_ship.png",
        is_published=True
    )

    # 4. Hero Section
    HeroSection.objects.get_or_create(
        title_ar="التميز في تجارة المواشي",
        title_en="Excellence in Livestock Trade",
        subtitle_ar="الشركة الرائدة في استيراد وتربية أفضل سلالات المواشي في ليبيا.",
        subtitle_en="The leading company in importing and breeding the finest livestock breeds in Libya.",
        image="hero/hero_livestock.png",
        cta_text_ar="استكشف مواشينا",
        cta_text_en="Explore Our Livestock",
        cta_link="/livestock/",
        is_active=True,
        order=1
    )

    # 5. Site Settings
    SiteSettings.objects.get_or_create(
        id=1,
        defaults={
            "logo": "settings/logo_transparent.png",
            "favicon": "settings/logo_transparent.png",
            "phone": "0918008432",
            "phone_whatsapp": "0912164951",
            "email": "info@alhilal.ly",
            "address_ar": "مصراتة، ليبيا - منطقة طمينة",
            "address_en": "Libya - Misrata - Tamina Area",
            "facebook": "https://facebook.com/alhilal",
            "instagram": "https://instagram.com/alhilal"
        }
    )

    print("Data population completed successfully!")

if __name__ == "__main__":
    create_sample_data()
