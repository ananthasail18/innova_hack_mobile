import logging
import random
from app.database.base import Base
from app.database.session import engine, SessionLocal
from app.models.restaurant import Restaurant
from app.models.category import Category
from app.models.dish import Dish
from app.models.user import User
from app.models.taste_profile import TasteProfile
from app.models.community_signal import CommunitySignal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed():
    # Automatically create tables if they do not exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Clean up database
        logger.info("Cleaning database before seeding...")
        db.query(CommunitySignal).delete()
        db.query(TasteProfile).delete()
        db.query(Dish).delete()
        db.query(Category).delete()
        db.query(Restaurant).delete()
        db.query(User).filter(User.name.startswith("Community User")).delete()
        db.commit()

        # Seed Restaurants
        restaurants_data = [
            {
                "name": "Rameshwaram Cafe",
                "slug": "rameshwaram-cafe",
                "description": "Authentic, high-quality traditional South Indian food served fast.",
                "logo": "/images/logos/logo_ba79b9bfc1.jpg",
                "logo_url": "/images/logos/logo_ba79b9bfc1.jpg",
                "theme_color": "#8b5a2b",
                "primary_color": "#8b5a2b",
                "secondary_color": "#fdf5e6",
                "hero_image": "/images/covers/cover_c2cae50a2d.jpg",
                "cover_image": "/images/covers/cover_c2cae50a2d.jpg",
                "city": "Bengaluru",
                "cuisine": "South Indian",
                "opening_hours": "6:30 AM - 1:00 AM",
                "price_range": "₹ - Budget Friendly"
            },
            {
                "name": "Truffles",
                "slug": "truffles",
                "description": "Legendary gourmet burgers, thick milkshakes, and continental cafe classics.",
                "logo": "/images/logos/logo_1adca79127.jpg",
                "logo_url": "/images/logos/logo_1adca79127.jpg",
                "theme_color": "#013220",
                "primary_color": "#013220",
                "secondary_color": "#b87333",
                "hero_image": "/images/covers/cover_8e6d62755b.jpg",
                "cover_image": "/images/covers/cover_8e6d62755b.jpg",
                "city": "Bengaluru",
                "cuisine": "Continental & Burgers",
                "opening_hours": "11:00 AM - 11:30 PM",
                "price_range": "₹₹ - Moderately Priced"
            },
            {
                "name": "Spice Symphony",
                "slug": "spice-symphony",
                "description": "Exquisite modern Asian fusion dining, fresh sushi rolls, and hot ramen bowls.",
                "logo": "/images/logos/logo_338eae2fa7.jpg",
                "logo_url": "/images/logos/logo_338eae2fa7.jpg",
                "theme_color": "#d4af37",
                "primary_color": "#d4af37",
                "secondary_color": "#0f1e36",
                "hero_image": "/images/covers/cover_8812c79e71.jpg",
                "cover_image": "/images/covers/cover_8812c79e71.jpg",
                "city": "Bengaluru",
                "cuisine": "Asian Fusion",
                "opening_hours": "12:00 PM - 11:00 PM",
                "price_range": "₹₹   - Premium Dining"
            }
        ]

        restaurants = {}
        for r_data in restaurants_data:
            restaurant = Restaurant(**r_data)
            db.add(restaurant)
            db.commit()
            db.refresh(restaurant)
            restaurants[restaurant.slug] = restaurant

        inserted_dishes = []

        # ========================================================
        # RAMESHWARAM CAFE MENU
        # ========================================================
        rc_categories = ["Breakfast", "Idli", "Vada", "Rice", "Combos", "Beverages", "Desserts"]
        rc_cats = {}
        for idx, cat_name in enumerate(rc_categories):
            category = Category(restaurant_id=restaurants["rameshwaram-cafe"].id, name=cat_name, sort_order=idx)
            db.add(category)
            db.commit()
            db.refresh(category)
            rc_cats[cat_name] = category

        rc_dishes = [
            # --- Breakfast ---
            {
                "category_id": rc_cats["Breakfast"].id,
                "name": "Plain Dosa",
                "description": "Crispy golden-brown thin rice crepe cooked to perfection, served with sambar and coconut chutney.",
                "price": 100.00,
                "image_url": "/images/dishes/dish_36ddad041c.jpg",
                "is_vegetarian": True,
                "spice_level": 0.2, "sweetness_level": 0.1, "creaminess_level": 0.2, "tanginess_level": 0.1,
                "masala_intensity_level": 0.2, "crunchiness_level": 0.8, "oiliness_level": 0.1, "saltiness_level": 0.5,
                "ingredients": ["Rice batter", "Urad dal", "Methi seeds"], "allergens": [], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.90
            },
            {
                "category_id": rc_cats["Breakfast"].id,
                "name": "Masala Dosa",
                "description": "Traditional crispy crepe stuffed with a mildly spiced seasoned potato mash, served with signature chutneys.",
                "price": 130.00,
                "image_url": "/images/dishes/dish_1c62afab10.jpg",
                "is_vegetarian": True,
                "spice_level": 0.4, "sweetness_level": 0.1, "creaminess_level": 0.2, "tanginess_level": 0.2,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.8, "oiliness_level": 0.2, "saltiness_level": 0.6,
                "ingredients": ["Rice batter", "Potatoes", "Onions", "Turmeric", "Mustard seeds"], "allergens": [], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.96
            },
            {
                "category_id": rc_cats["Breakfast"].id,
                "name": "Ghee Roast Dosa",
                "description": "Paper-thin extra crispy rice crepe roasted generously with pure aromatic ghee.",
                "price": 150.00,
                "image_url": "https://images.unsplash.com/photo-1601050690597-df056fb4ce78?w=500&q=80",
                "is_vegetarian": True,
                "spice_level": 0.2, "sweetness_level": 0.2, "creaminess_level": 0.5, "tanginess_level": 0.1,
                "masala_intensity_level": 0.3, "crunchiness_level": 0.9, "oiliness_level": 0.2, "saltiness_level": 0.5,
                "ingredients": ["Rice batter", "Pure Ghee"], "allergens": [], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.94
            },
            {
                "category_id": rc_cats["Breakfast"].id,
                "name": "Podi Dosa",
                "description": "Crispy golden crepe smeared internally with spicy lentil gunpowder (podi) and melted butter.",
                "price": 140.00,
                "image_url": "/images/dishes/dish_0e08cb6976.jpg",
                "is_vegetarian": True,
                "spice_level": 0.7, "sweetness_level": 0.1, "creaminess_level": 0.3, "tanginess_level": 0.1,
                "masala_intensity_level": 0.2, "crunchiness_level": 0.8, "oiliness_level": 0.3, "saltiness_level": 0.6,
                "ingredients": ["Rice batter", "Lentil powder (podi)", "Chili", "Ghee"], "allergens": [], "dietary_tags": ["Vegetarian", "Spicy"],
                "popularity_score": 0.97
            },
            {
                "category_id": rc_cats["Breakfast"].id,
                "name": "Benne Dosa",
                "description": "Davanagere style soft yet crispy crepe prepared using generous dollops of fresh white butter.",
                "price": 150.00,
                "image_url": "/images/dishes/dish_6bd4f3c16a.jpg",
                "is_vegetarian": True,
                "spice_level": 0.3, "sweetness_level": 0.2, "creaminess_level": 0.6, "tanginess_level": 0.1,
                "masala_intensity_level": 0.2, "crunchiness_level": 0.7, "oiliness_level": 0.2, "saltiness_level": 0.6,
                "ingredients": ["Rice batter", "Fresh butter (Benne)", "Potato filling"], "allergens": [], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.93
            },
            {
                "category_id": rc_cats["Breakfast"].id,
                "name": "Onion Uttapam",
                "description": "Thick savory rice pancake topped with finely chopped onions, green chilies, and fresh coriander.",
                "price": 130.00,
                "image_url": "/images/dishes/dish_7fad73c10e.jpg",
                "is_vegetarian": True,
                "spice_level": 0.4, "sweetness_level": 0.2, "creaminess_level": 0.2, "tanginess_level": 0.2,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.5, "oiliness_level": 0.2, "saltiness_level": 0.6,
                "ingredients": ["Fermented rice batter", "Red onions", "Green chilies", "Coriander"], "allergens": [], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.91
            },
            {
                "category_id": rc_cats["Breakfast"].id,
                "name": "Rava Dosa",
                "description": "Crispy and lacy crepe made from semolina (rava) batter, spiced with ginger, black pepper, and cumin.",
                "price": 140.00,
                "image_url": "/images/dishes/dish_8c46204421.jpg",
                "is_vegetarian": True,
                "spice_level": 0.4, "sweetness_level": 0.1, "creaminess_level": 0.1, "tanginess_level": 0.2,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.9, "oiliness_level": 0.3, "saltiness_level": 0.7,
                "ingredients": ["Semolina", "Rice flour", "Cumin", "Ginger", "Black pepper"], "allergens": ["Gluten"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.92
            },
            {
                "category_id": rc_cats["Breakfast"].id,
                "name": "Set Dosa",
                "description": "A set of 3 soft, spongy, and fluffy small-sized dosas served with vegetable sagu and coconut chutney.",
                "price": 120.00,
                "image_url": "/images/dishes/dish_1d87d71455.jpg",
                "is_vegetarian": True,
                "spice_level": 0.2, "sweetness_level": 0.2, "creaminess_level": 0.3, "tanginess_level": 0.2,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.2, "oiliness_level": 0.2, "saltiness_level": 0.7,
                "ingredients": ["Rice", "Poha (flattened rice)", "Urad dal"], "allergens": [], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.89
            },

            # --- Idli ---
            {
                "category_id": rc_cats["Idli"].id,
                "name": "Idli",
                "description": "A pair of soft, fluffy, steamed rice cakes served hot with sambar and fresh chutneys.",
                "price": 60.00,
                "image_url": "/images/dishes/dish_0e5e567bdf.jpg",
                "is_vegetarian": True,
                "spice_level": 0.1, "sweetness_level": 0.1, "creaminess_level": 0.1, "tanginess_level": 0.1,
                "masala_intensity_level": 0.0, "crunchiness_level": 0.1, "oiliness_level": 0.1, "saltiness_level": 0.4,
                "ingredients": ["Steamed fermented rice", "Lentil batter"], "allergens": [], "dietary_tags": ["Vegetarian", "Gluten-Free"],
                "popularity_score": 0.94
            },
            {
                "category_id": rc_cats["Idli"].id,
                "name": "Podi Idli",
                "description": "Steamed idli cubes tossed in spicy, dry lentil powder (podi) and refined sesame oil.",
                "price": 90.00,
                "image_url": "/images/dishes/dish_36ddad041c.jpg",
                "is_vegetarian": True,
                "spice_level": 0.6, "sweetness_level": 0.1, "creaminess_level": 0.2, "tanginess_level": 0.1,
                "masala_intensity_level": 0.2, "crunchiness_level": 0.3, "oiliness_level": 0.3, "saltiness_level": 0.4,
                "ingredients": ["Rice cakes", "Gunpowder (podi)", "Oil"], "allergens": [], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.91
            },
            {
                "category_id": rc_cats["Idli"].id,
                "name": "Ghee Podi Idli",
                "description": "Soft steamed idlis completely drenched in rich aromatic pure ghee and signature spicy podi gunpowder.",
                "price": 120.00,
                "image_url": "https://images.unsplash.com/photo-1601050690597-df056fb4ce78?w=500&q=80",
                "is_vegetarian": True,
                "spice_level": 0.7, "sweetness_level": 0.1, "creaminess_level": 0.5, "tanginess_level": 0.1,
                "masala_intensity_level": 0.2, "crunchiness_level": 0.2, "oiliness_level": 0.3, "saltiness_level": 0.4,
                "ingredients": ["Rice cakes", "Pure ghee", "Podi gunpowder"], "allergens": [], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.98
            },
            {
                "category_id": rc_cats["Idli"].id,
                "name": "Mini Idli Sambar",
                "description": "Button-sized miniature steamed idlis (12 pieces) submerged in a bowl of hot piping lentil sambar.",
                "price": 100.00,
                "image_url": "/images/dishes/dish_8befaec9ea.jpg",
                "is_vegetarian": True,
                "spice_level": 0.4, "sweetness_level": 0.2, "creaminess_level": 0.2, "tanginess_level": 0.3,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.1, "oiliness_level": 0.2, "saltiness_level": 0.5,
                "ingredients": ["Mini rice cakes", "Lentil sambar", "Ghee splash"], "allergens": [], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.95
            },
            {
                "category_id": rc_cats["Idli"].id,
                "name": "Thatte Idli",
                "description": "Bidar style flat plate-sized spongy idli served with butter dollops, hot sambar, and coconut chutney.",
                "price": 80.00,
                "image_url": "/images/dishes/dish_0e5e567bdf.jpg",
                "is_vegetarian": True,
                "spice_level": 0.2, "sweetness_level": 0.1, "creaminess_level": 0.4, "tanginess_level": 0.1,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.1, "oiliness_level": 0.2, "saltiness_level": 0.5,
                "ingredients": ["Rice", "Urad dal", "Butter"], "allergens": [], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.93
            },

            # --- Vada ---
            {
                "category_id": rc_cats["Vada"].id,
                "name": "Medu Vada",
                "description": "Crispy golden, donut-shaped deep-fried black lentil fritters (2 pieces) seasoned with pepper and curry leaves.",
                "price": 80.00,
                "image_url": "/images/dishes/dish_36ddad041c.jpg",
                "is_vegetarian": True,
                "spice_level": 0.3, "sweetness_level": 0.0, "creaminess_level": 0.1, "tanginess_level": 0.1,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.9, "oiliness_level": 0.1, "saltiness_level": 0.4,
                "ingredients": ["Urad dal batter", "Black pepper", "Ginger", "Curry leaves"], "allergens": [], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.92
            },
            {
                "category_id": rc_cats["Vada"].id,
                "name": "Sambar Vada",
                "description": "Crispy lentil vadas soaked in hot piping seasoned sambar, garnished with finely chopped fresh onions.",
                "price": 95.00,
                "image_url": "https://images.unsplash.com/photo-1601050690597-df056fb4ce78?w=500&q=80",
                "is_vegetarian": True,
                "spice_level": 0.4, "sweetness_level": 0.2, "creaminess_level": 0.2, "tanginess_level": 0.3,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.6, "oiliness_level": 0.2, "saltiness_level": 0.5,
                "ingredients": ["Urad dal vadas", "Lentil sambar", "Onions"], "allergens": [], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.91
            },

            # --- Rice ---
            {
                "category_id": rc_cats["Rice"].id,
                "name": "Lemon Rice",
                "description": "Flavorful, tangy rice tempered with lemon juice, mustard seeds, curry leaves, and crunchy peanuts.",
                "price": 100.00,
                "image_url": "/images/dishes/dish_0e08cb6976.jpg",
                "is_vegetarian": True,
                "spice_level": 0.3, "sweetness_level": 0.1, "creaminess_level": 0.1, "tanginess_level": 0.7,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.4, "oiliness_level": 0.2, "saltiness_level": 0.6,
                "ingredients": ["Precooked rice", "Lemon juice", "Peanuts", "Turmeric"], "allergens": ["Peanuts"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.88
            },
            {
                "category_id": rc_cats["Rice"].id,
                "name": "Curd Rice",
                "description": "Comforting dish of soft boiled rice mixed with fresh yogurt, salted, and tempered with mustard seeds and curry leaves.",
                "price": 90.00,
                "image_url": "/images/dishes/dish_6bd4f3c16a.jpg",
                "is_vegetarian": True,
                "spice_level": 0.1, "sweetness_level": 0.2, "creaminess_level": 0.7, "tanginess_level": 0.4,
                "masala_intensity_level": 0.0, "crunchiness_level": 0.2, "oiliness_level": 0.1, "saltiness_level": 0.5,
                "ingredients": ["Cooked rice", "Fresh curd (yogurt)", "Milk", "Ginger"], "allergens": ["Dairy"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.89
            },
            {
                "category_id": rc_cats["Rice"].id,
                "name": "Bisibele Bath",
                "description": "Spicy, tangy hot meal of rice, lentils, and mixed vegetables cooked together with a special spice powder.",
                "price": 130.00,
                "image_url": "https://images.unsplash.com/photo-1601050690597-df056fb4ce78?w=500&q=80",
                "is_vegetarian": True,
                "spice_level": 0.6, "sweetness_level": 0.1, "creaminess_level": 0.3, "tanginess_level": 0.4,
                "masala_intensity_level": 0.2, "crunchiness_level": 0.2, "oiliness_level": 0.3, "saltiness_level": 0.7,
                "ingredients": ["Rice", "Toor dal", "Mixed vegetables", "Bisi Bele Bath spices", "Ghee"], "allergens": [], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.95
            },
            {
                "category_id": rc_cats["Rice"].id,
                "name": "Pongal",
                "description": "Cozy, porridge-style rice and yellow lentil dish seasoned with crushed black pepper, cumin, ginger, and cashews.",
                "price": 110.00,
                "image_url": "/images/dishes/dish_36ddad041c.jpg",
                "is_vegetarian": True,
                "spice_level": 0.3, "sweetness_level": 0.1, "creaminess_level": 0.5, "tanginess_level": 0.0,
                "masala_intensity_level": 0.2, "crunchiness_level": 0.3, "oiliness_level": 0.2, "saltiness_level": 0.6,
                "ingredients": ["Rice", "Moong dal", "Black pepper", "Cumin", "Ghee", "Cashews"], "allergens": ["Tree Nuts"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.92
            },
            {
                "category_id": rc_cats["Rice"].id,
                "name": "Khara Bath",
                "description": "Savory roasted semolina pudding cooked with vegetables, ghee, turmeric, and traditional spices.",
                "price": 90.00,
                "image_url": "/images/dishes/dish_8c46204421.jpg",
                "is_vegetarian": True,
                "spice_level": 0.4, "sweetness_level": 0.1, "creaminess_level": 0.3, "tanginess_level": 0.2,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.3, "oiliness_level": 0.2, "saltiness_level": 0.5,
                "ingredients": ["Semolina", "Mixed vegetables", "Ghee", "Mustard seeds"], "allergens": ["Gluten"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.90
            },

            # --- Combos ---
            {
                "category_id": rc_cats["Combos"].id,
                "name": "Mini Tiffin",
                "description": "Sample all classics: 1 mini idli, 1 mini vada, 1 mini masala Dosa, Khara Bath, and Kesari Bath.",
                "price": 200.00,
                "image_url": "/images/dishes/dish_7fad73c10e.jpg",
                "is_vegetarian": True,
                "spice_level": 0.5, "sweetness_level": 0.7, "creaminess_level": 0.4, "tanginess_level": 0.3,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.7, "oiliness_level": 0.6, "saltiness_level": 0.9,
                "ingredients": ["Idli", "Vada", "Dosa", "Upma", "Suji halwa"], "allergens": ["Gluten"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.98
            },
            {
                "category_id": rc_cats["Combos"].id,
                "name": "Idli Vada Combo",
                "description": "Standard breakfast combo of two soft steamed idlis and one crispy medu vada, served with chutneys.",
                "price": 110.00,
                "image_url": "/images/dishes/dish_1d87d71455.jpg",
                "is_vegetarian": True,
                "spice_level": 0.3, "sweetness_level": 0.1, "creaminess_level": 0.2, "tanginess_level": 0.2,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.6, "oiliness_level": 0.2, "saltiness_level": 0.7,
                "ingredients": ["Idlis", "Medu vada"], "allergens": [], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.95
            },
            {
                "category_id": rc_cats["Combos"].id,
                "name": "Dosa Combo",
                "description": "A customized platter featuring one ghee roast podi Dosa, one mini idli, and one cup of filter coffee.",
                "price": 220.00,
                "image_url": "/images/dishes/dish_1c62afab10.jpg",
                "is_vegetarian": True,
                "spice_level": 0.5, "sweetness_level": 0.3, "creaminess_level": 0.4, "tanginess_level": 0.2,
                "masala_intensity_level": 0.2, "crunchiness_level": 0.8, "oiliness_level": 0.4, "saltiness_level": 0.8,
                "ingredients": ["Podi Dosa", "Steamed Idli", "Filter Coffee"], "allergens": ["Dairy"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.94
            },

            # --- Beverages ---
            {
                "category_id": rc_cats["Beverages"].id,
                "name": "Filter Coffee",
                "description": "Authentic South Indian drip-brewed frothed coffee prepared in a traditional brass cup.",
                "price": 90.00,
                "image_url": "/images/dishes/dish_0e08cb6976.jpg",
                "is_vegetarian": True,
                "spice_level": 0.0, "sweetness_level": 0.4, "creaminess_level": 0.5, "tanginess_level": 0.1,
                "masala_intensity_level": 0.3, "crunchiness_level": 0.0, "oiliness_level": 0.2, "saltiness_level": 0.2,
                "ingredients": ["Coffee beans", "Chicory blend", "Boiled milk", "Sugar"], "allergens": ["Dairy"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.99
            },
            {
                "category_id": rc_cats["Beverages"].id,
                "name": "Badam Milk",
                "description": "Rich milk drink flavored with crushed almonds, saffron, and cardamom, served warm or chilled.",
                "price": 100.00,
                "image_url": "https://images.unsplash.com/photo-1568649929103-28fffe997672?w=500&q=80",
                "is_vegetarian": True,
                "spice_level": 0.0, "sweetness_level": 0.8, "creaminess_level": 0.7, "tanginess_level": 0.0,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.2, "oiliness_level": 0.2, "saltiness_level": 0.3,
                "ingredients": ["Almonds", "Saffron", "Milk", "Cardamom"], "allergens": ["Dairy", "Tree Nuts"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.91
            },
            {
                "category_id": rc_cats["Beverages"].id,
                "name": "Fresh Lime Soda",
                "description": "Tangy and refreshing carbonated fresh lime juice, customizable sweet, salted, or mixed.",
                "price": 80.00,
                "image_url": "/images/dishes/dish_42ea6d4aa1.jpg",
                "is_vegetarian": True,
                "spice_level": 0.1, "sweetness_level": 0.5, "creaminess_level": 0.0, "tanginess_level": 0.8,
                "masala_intensity_level": 0.0, "crunchiness_level": 0.0, "oiliness_level": 0.1, "saltiness_level": 0.4,
                "ingredients": ["Lemon juice", "Soda", "Mint leaves", "Sugar/Salt"], "allergens": [], "dietary_tags": ["Vegetarian", "Vegan"],
                "popularity_score": 0.87
            },

            # --- Desserts ---
            {
                "category_id": rc_cats["Desserts"].id,
                "name": "Kesari Bath",
                "description": "Semolina pudding cooked with pure ghee, sugar, saffron, and loaded with Cashew nuts.",
                "price": 90.00,
                "image_url": "/images/dishes/dish_0e5e567bdf.jpg",
                "is_vegetarian": True,
                "spice_level": 0.0, "sweetness_level": 0.9, "creaminess_level": 0.6, "tanginess_level": 0.0,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.3, "oiliness_level": 0.2, "saltiness_level": 0.4,
                "ingredients": ["Semolina", "Saffron", "Cashews", "Ghee"], "allergens": ["Tree Nuts"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.93
            },
            {
                "category_id": rc_cats["Desserts"].id,
                "name": "Sweet Pongal",
                "description": "Traditional sweet dish of rice and yellow moong lentils cooked with jaggery, cardamom, ghee, and raisins.",
                "price": 100.00,
                "image_url": "/images/dishes/dish_6bd4f3c16a.jpg",
                "is_vegetarian": True,
                "spice_level": 0.0, "sweetness_level": 0.8, "creaminess_level": 0.5, "tanginess_level": 0.0,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.2, "oiliness_level": 0.2, "saltiness_level": 0.5,
                "ingredients": ["Rice", "Moong lentil", "Cardamom", "Cashews", "Jaggery syrup"], "allergens": ["Tree Nuts"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.90
            }
        ]

        for d_data in rc_dishes:
            dish = Dish(restaurant_id=restaurants["rameshwaram-cafe"].id, **d_data)
            db.add(dish)
            inserted_dishes.append(dish)


        # ========================================================
        # TRUFFLES MENU
        # ========================================================
        tr_categories = ["Burgers", "Pizza", "Pasta", "Sides", "Drinks", "Desserts"]
        tr_cats = {}
        for idx, cat_name in enumerate(tr_categories):
            category = Category(restaurant_id=restaurants["truffles"].id, name=cat_name, sort_order=idx)
            db.add(category)
            db.commit()
            db.refresh(category)
            tr_cats[cat_name] = category

        tr_dishes = [
            # --- Burgers ---
            {
                "category_id": tr_cats["Burgers"].id,
                "name": "Crunchy Cheese Burger",
                "description": "Crispy seasoned vegetable patty topped with a double layer of melted cheddar cheese and house secret burger sauce.",
                "price": 280.00,
                "image_url": "/images/dishes/dish_8757141b95.jpg",
                "is_vegetarian": True,
                "spice_level": 0.3, "sweetness_level": 0.3, "creaminess_level": 0.7, "tanginess_level": 0.4,
                "masala_intensity_level": 0.2, "crunchiness_level": 0.8, "oiliness_level": 0.3, "saltiness_level": 0.6,
                "ingredients": ["Crispy veggie patty", "Cheddar cheese", "Iceberg lettuce", "Brioche bun"], "allergens": ["Gluten", "Dairy"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.97
            },
            {
                "category_id": tr_cats["Burgers"].id,
                "name": "All American Cheese Burger",
                "description": "Classic grilled prime beef patty topped with pickles, white onions, mustard, ketchup, and processed American cheese.",
                "price": 350.00,
                "image_url": "/images/dishes/dish_6d63c55d81.jpg",
                "is_vegetarian": False,
                "spice_level": 0.2, "sweetness_level": 0.3, "creaminess_level": 0.6, "tanginess_level": 0.4,
                "masala_intensity_level": 0.5, "crunchiness_level": 0.5, "oiliness_level": 0.2, "saltiness_level": 0.7,
                "ingredients": ["Minced beef patty", "American cheese", "Pickles", "Mustard"], "allergens": ["Gluten", "Dairy"], "dietary_tags": [],
                "popularity_score": 0.95
            },
            {
                "category_id": tr_cats["Burgers"].id,
                "name": "BBQ Chicken Burger",
                "description": "Charbroiled tender chicken breast basted in sweet and smoky hickory BBQ sauce, topped with grilled onions.",
                "price": 320.00,
                "image_url": "https://images.unsplash.com/photo-1603060263832-44abf643f807?w=500&q=80",
                "is_vegetarian": False,
                "spice_level": 0.3, "sweetness_level": 0.5, "creaminess_level": 0.5, "tanginess_level": 0.3,
                "masala_intensity_level": 0.7, "crunchiness_level": 0.5, "oiliness_level": 0.4, "saltiness_level": 0.7,
                "ingredients": ["Grilled chicken breast", "Smoky BBQ glaze", "Cheddar", "Caramelized onions"], "allergens": ["Gluten", "Dairy"], "dietary_tags": [],
                "popularity_score": 0.94
            },
            {
                "category_id": tr_cats["Burgers"].id,
                "name": "Lamb Burger",
                "description": "Spiced minced lamb patty grilled, smeared with mint garlic aioli, topped with pickled cucumber slices.",
                "price": 390.00,
                "image_url": "/images/dishes/dish_2110123760.jpg",
                "is_vegetarian": False,
                "spice_level": 0.5, "sweetness_level": 0.2, "creaminess_level": 0.6, "tanginess_level": 0.3,
                "masala_intensity_level": 0.6, "crunchiness_level": 0.4, "oiliness_level": 0.5, "saltiness_level": 0.7,
                "ingredients": ["Minced lamb", "Mint aioli", "Pickles", "Arugula"], "allergens": ["Gluten", "Dairy", "Egg"], "dietary_tags": [],
                "popularity_score": 0.93
            },

            # --- Pizza ---
            {
                "category_id": tr_cats["Pizza"].id,
                "name": "Classic Margherita",
                "description": "Thin-crust stone-baked pizza topped with marinara sauce, fresh bocconcini mozzarella, and fresh basil leaves.",
                "price": 380.00,
                "image_url": "/images/dishes/dish_dfbd63e533.jpg",
                "is_vegetarian": True,
                "spice_level": 0.1, "sweetness_level": 0.2, "creaminess_level": 0.5, "tanginess_level": 0.4,
                "masala_intensity_level": 0.4, "crunchiness_level": 0.6, "oiliness_level": 0.2, "saltiness_level": 0.8,
                "ingredients": ["Stone-baked crust", "San Marzano tomatoes", "Mozzarella", "Fresh basil"], "allergens": ["Gluten", "Dairy"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.92
            },
            {
                "category_id": tr_cats["Pizza"].id,
                "name": "Farmhouse Pizza",
                "description": "Stone-baked pizza loaded with fresh button mushrooms, sweet corn, green bell pepper, and black olives.",
                "price": 440.00,
                "image_url": "/images/dishes/dish_85c9a40977.jpg",
                "is_vegetarian": True,
                "spice_level": 0.2, "sweetness_level": 0.3, "creaminess_level": 0.5, "tanginess_level": 0.3,
                "masala_intensity_level": 0.4, "crunchiness_level": 0.6, "oiliness_level": 0.3, "saltiness_level": 0.8,
                "ingredients": ["Pizza crust", "Mushrooms", "Bell peppers", "Sweet corn", "Black olives"], "allergens": ["Gluten", "Dairy"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.90
            },
            {
                "category_id": tr_cats["Pizza"].id,
                "name": "Pepperoni Pizza",
                "description": "Thin-crust signature pizza loaded with spicy pork pepperoni, marinara, and fresh stringy mozzarella.",
                "price": 490.00,
                "image_url": "/images/dishes/dish_acdcb911a0.jpg",
                "is_vegetarian": False,
                "spice_level": 0.5, "sweetness_level": 0.2, "creaminess_level": 0.5, "tanginess_level": 0.3,
                "masala_intensity_level": 0.5, "crunchiness_level": 0.6, "oiliness_level": 0.4, "saltiness_level": 0.8,
                "ingredients": ["Pizza dough", "Marinara", "Spicy pork pepperoni", "Mozzarella"], "allergens": ["Gluten", "Dairy"], "dietary_tags": [],
                "popularity_score": 0.96
            },

            # --- Pasta ---
            {
                "category_id": tr_cats["Pasta"].id,
                "name": "Alfredo Pasta",
                "description": "Fettuccine pasta tossed in rich, creamy butter and aged parmesan cheese sauce with fresh parsley.",
                "price": 310.00,
                "image_url": "/images/dishes/dish_6c1ea925bc.jpg",
                "is_vegetarian": True,
                "spice_level": 0.1, "sweetness_level": 0.2, "creaminess_level": 0.8, "tanginess_level": 0.1,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.2, "oiliness_level": 0.2, "saltiness_level": 0.6,
                "ingredients": ["Fettuccine", "Aged Parmesan", "Heavy cream", "Butter", "Garlic"], "allergens": ["Gluten", "Dairy"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.93
            },
            {
                "category_id": tr_cats["Pasta"].id,
                "name": "Arrabbiata Pasta",
                "description": "Penne pasta cooked in a fiery hot Italian tomato sauce seasoned with garlic and dried red chili flakes.",
                "price": 290.00,
                "image_url": "/images/dishes/dish_fb90795218.jpg",
                "is_vegetarian": True,
                "spice_level": 0.7, "sweetness_level": 0.2, "creaminess_level": 0.1, "tanginess_level": 0.6,
                "masala_intensity_level": 0.2, "crunchiness_level": 0.2, "oiliness_level": 0.3, "saltiness_level": 0.6,
                "ingredients": ["Penne pasta", "Tomato pure", "Garlic", "Red chili flakes", "Olive oil"], "allergens": ["Gluten"], "dietary_tags": ["Vegetarian", "Spicy"],
                "popularity_score": 0.91
            },

            # --- Sides ---
            {
                "category_id": tr_cats["Sides"].id,
                "name": "Peri Peri Fries",
                "description": "Golden crispy hand-cut french fries generously seasoned with spicy, hot African peri-peri spices.",
                "price": 180.00,
                "image_url": "/images/dishes/dish_f9071b9c2a.jpg",
                "is_vegetarian": True,
                "spice_level": 0.6, "sweetness_level": 0.1, "creaminess_level": 0.1, "tanginess_level": 0.3,
                "masala_intensity_level": 0.2, "crunchiness_level": 0.9, "oiliness_level": 0.2, "saltiness_level": 0.4,
                "ingredients": ["Premium potatoes", "Peri-peri seasoning", "Vegetable oil"], "allergens": [], "dietary_tags": ["Vegetarian", "Vegan"],
                "popularity_score": 0.94
            },
            {
                "category_id": tr_cats["Sides"].id,
                "name": "Loaded Fries",
                "description": "French fries smothered in warm cheese sauce, topped with chopped jalapeños and crispy bacon bits.",
                "price": 240.00,
                "image_url": "/images/dishes/dish_c896a3bf8f.jpg",
                "is_vegetarian": False,
                "spice_level": 0.4, "sweetness_level": 0.2, "creaminess_level": 0.7, "tanginess_level": 0.3,
                "masala_intensity_level": 0.4, "crunchiness_level": 0.7, "oiliness_level": 0.3, "saltiness_level": 0.6,
                "ingredients": ["French fries", "Cheddar cheese sauce", "Jalapenos", "Bacon bits"], "allergens": ["Dairy"], "dietary_tags": [],
                "popularity_score": 0.92
            },
            {
                "category_id": tr_cats["Sides"].id,
                "name": "Onion Rings",
                "description": "Thick-cut sweet white onions battered in seasoned breadcrumbs and fried until golden and extra crunchy.",
                "price": 160.00,
                "image_url": "https://images.unsplash.com/photo-1639024471283-2bc7b3c6a267?w=500&q=80",
                "is_vegetarian": True,
                "spice_level": 0.2, "sweetness_level": 0.3, "creaminess_level": 0.1, "tanginess_level": 0.2,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.9, "oiliness_level": 0.2, "saltiness_level": 0.4,
                "ingredients": ["White onions", "Breadcrumbs flour", "Spiced batter"], "allergens": ["Gluten"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.88
            },
            {
                "category_id": tr_cats["Sides"].id,
                "name": "Nachos",
                "description": "Crispy corn tortilla chips loaded with spicy refried beans, cheddar cheese sauce, sour cream, and salsa.",
                "price": 230.00,
                "image_url": "/images/dishes/dish_7a26b7f6a1.jpg",
                "is_vegetarian": True,
                "spice_level": 0.4, "sweetness_level": 0.2, "creaminess_level": 0.6, "tanginess_level": 0.5,
                "masala_intensity_level": 0.2, "crunchiness_level": 0.8, "oiliness_level": 0.3, "saltiness_level": 0.7,
                "ingredients": ["Corn tortilla chips", "Cheddar cheese sauce", "Refried beans", "Sour cream", "Salsa"], "allergens": ["Dairy"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.91
            },

            # --- Drinks ---
            {
                "category_id": tr_cats["Drinks"].id,
                "name": "Oreo Shake",
                "description": "Thick premium vanilla ice cream milkshake blended with chocolate Oreo biscuits, topped with whipped cream.",
                "price": 180.00,
                "image_url": "/images/dishes/dish_7fbf6fd911.jpg",
                "is_vegetarian": True,
                "spice_level": 0.0, "sweetness_level": 0.9, "creaminess_level": 0.8, "tanginess_level": 0.0,
                "masala_intensity_level": 0.0, "crunchiness_level": 0.4, "oiliness_level": 0.2, "saltiness_level": 0.5,
                "ingredients": ["Oreo cookies", "Vanilla ice cream", "Whole milk", "Whipped cream"], "allergens": ["Dairy", "Gluten"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.96
            },
            {
                "category_id": tr_cats["Drinks"].id,
                "name": "Chocolate Shake",
                "description": "Creamy milkshake blended with rich Belgian dark chocolate syrup and whole milk, topped with chocolate shavings.",
                "price": 170.00,
                "image_url": "/images/dishes/dish_472ac3d242.jpg",
                "is_vegetarian": True,
                "spice_level": 0.0, "sweetness_level": 0.8, "creaminess_level": 0.8, "tanginess_level": 0.0,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.1, "oiliness_level": 0.2, "saltiness_level": 0.5,
                "ingredients": ["Belgian chocolate cocoa", "Milk", "Vanilla ice cream base"], "allergens": ["Dairy"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.93
            },
            {
                "category_id": tr_cats["Drinks"].id,
                "name": "Cold Coffee",
                "description": "Perfect classic blend of premium roasted coffee beans, whole milk, and sugar, served chilled with vanilla ice cream.",
                "price": 160.00,
                "image_url": "/images/dishes/dish_2e87948fb1.jpg",
                "is_vegetarian": True,
                "spice_level": 0.0, "sweetness_level": 0.6, "creaminess_level": 0.6, "tanginess_level": 0.1,
                "masala_intensity_level": 0.2, "crunchiness_level": 0.1, "oiliness_level": 0.2, "saltiness_level": 0.4,
                "ingredients": ["Espresso decoction", "Whole milk", "Vanilla ice cream scoop"], "allergens": ["Dairy"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.94
            },
            {
                "category_id": tr_cats["Drinks"].id,
                "name": "Mojito",
                "description": "Classic cuban refresher containing fresh lime wedges, wild mint leaves, white sugar, and club soda.",
                "price": 150.00,
                "image_url": "/images/dishes/dish_42ea6d4aa1.jpg",
                "is_vegetarian": True,
                "spice_level": 0.1, "sweetness_level": 0.6, "creaminess_level": 0.0, "tanginess_level": 0.8,
                "masala_intensity_level": 0.0, "crunchiness_level": 0.2, "oiliness_level": 0.3, "saltiness_level": 0.4,
                "ingredients": ["Fresh mint", "Lime slices", "Brown sugar", "Soda", "Crushed ice"], "allergens": [], "dietary_tags": ["Vegetarian", "Vegan"],
                "popularity_score": 0.89
            },

            # --- Desserts ---
            {
                "category_id": tr_cats["Desserts"].id,
                "name": "Blueberry Cheesecake",
                "description": "Rich cold-set cream cheese on a buttery graham cracker biscuit crust, topped with wild blueberry compote.",
                "price": 250.00,
                "image_url": "/images/dishes/dish_a15a4d4c8a.jpg",
                "is_vegetarian": True,
                "spice_level": 0.0, "sweetness_level": 0.8, "creaminess_level": 0.7, "tanginess_level": 0.4,
                "masala_intensity_level": 0.0, "crunchiness_level": 0.3, "oiliness_level": 0.3, "saltiness_level": 0.3,
                "ingredients": ["Cream cheese", "Graham crackers", "Wild blueberries", "Ghee butter"], "allergens": ["Dairy", "Gluten"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.96
            },
            {
                "category_id": tr_cats["Desserts"].id,
                "name": "Chocolate Brownie",
                "description": "Fudgy warm double chocolate chip brownie served with a scoop of premium vanilla bean ice cream.",
                "price": 190.00,
                "image_url": "/images/dishes/dish_ee284137d7.jpg",
                "is_vegetarian": True,
                "spice_level": 0.0, "sweetness_level": 0.9, "creaminess_level": 0.6, "tanginess_level": 0.0,
                "masala_intensity_level": 0.2, "crunchiness_level": 0.3, "oiliness_level": 0.2, "saltiness_level": 0.4,
                "ingredients": ["Dark chocolate", "Flour", "Butter", "Vanilla ice cream"], "allergens": ["Dairy", "Gluten"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.95
            },
            {
                "category_id": tr_cats["Desserts"].id,
                "name": "Ice Cream",
                "description": "A double scoop of premium artisanal ice cream. Choose between Madagascan Vanilla or Belgian Dark Chocolate.",
                "price": 120.00,
                "image_url": "/images/dishes/dish_01619dbcef.jpg",
                "is_vegetarian": True,
                "spice_level": 0.0, "sweetness_level": 0.9, "creaminess_level": 0.7, "tanginess_level": 0.0,
                "masala_intensity_level": 0.0, "crunchiness_level": 0.0, "oiliness_level": 0.1, "saltiness_level": 0.3,
                "ingredients": ["Heavy cream base", "Artisanal flavoring extract", "Sugar"], "allergens": ["Dairy"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.90
            }
        ]

        for d_data in tr_dishes:
            dish = Dish(restaurant_id=restaurants["truffles"].id, **d_data)
            db.add(dish)
            inserted_dishes.append(dish)


        # ========================================================
        # SPICE SYMPHONY MENU
        # ========================================================
        ss_categories = ["Sushi Rolls", "Ramen & Soup", "Wok Mains", "Beverages"]
        ss_cats = {}
        for idx, cat_name in enumerate(ss_categories):
            category = Category(restaurant_id=restaurants["spice-symphony"].id, name=cat_name, sort_order=idx)
            db.add(category)
            db.commit()
            db.refresh(category)
            ss_cats[cat_name] = category

        ss_dishes = [
            {
                "category_id": ss_cats["Sushi Rolls"].id,
                "name": "Dragon Roll",
                "description": "Smoked eel and crisp cucumber topped with sliced avocado, black sesame seeds, and sweet unagi glaze.",
                "price": 1279.00,
                "image_url": "/images/dishes/dish_cac223262e.jpg",
                "is_vegetarian": False,
                "spice_level": 0.1, "sweetness_level": 0.5, "creaminess_level": 0.6, "tanginess_level": 0.2,
                "masala_intensity_level": 0.4, "crunchiness_level": 0.4, "oiliness_level": 0.6, "saltiness_level": 0.5,
                "ingredients": ["Smoked eel", "Avocado", "Cucumber", "Nori", "Sushi rice"], "allergens": ["Seafood", "Gluten", "Soy"], "dietary_tags": [],
                "popularity_score": 0.95
            },
            {
                "category_id": ss_cats["Sushi Rolls"].id,
                "name": "Sushi Nigiri Sampler",
                "description": "Premium platter featuring fresh slices of Norwegian salmon, yellowtail, and sweet tiger shrimp on seasoned vinegared rice.",
                "price": 1150.00,
                "image_url": "/images/dishes/dish_19e7de1ea6.jpg",
                "is_vegetarian": False,
                "spice_level": 0.1, "sweetness_level": 0.3, "creaminess_level": 0.3, "tanginess_level": 0.4,
                "masala_intensity_level": 0.1, "crunchiness_level": 0.2, "oiliness_level": 0.7, "saltiness_level": 0.4,
                "ingredients": ["Salmon", "Tuna", "Shrimp", "Vinegared rice", "Wasabi"], "allergens": ["Seafood"], "dietary_tags": [],
                "popularity_score": 0.92
            },
            {
                "category_id": ss_cats["Ramen & Soup"].id,
                "name": "Tonkotsu Ramen",
                "description": "Thick wheat noodles in a rich pork marrow broth, topped with chashu pork belly, soft-boiled marinated egg, and nori.",
                "price": 850.00,
                "image_url": "/images/dishes/dish_934ea3c977.jpg",
                "is_vegetarian": False,
                "spice_level": 0.5, "sweetness_level": 0.2, "creaminess_level": 0.5, "tanginess_level": 0.2,
                "masala_intensity_level": 0.5, "crunchiness_level": 0.3, "oiliness_level": 0.5, "saltiness_level": 0.8,
                "ingredients": ["Wheat noodles", "Chashu pork belly", "Marinated egg", "Bamboo shoots", "Pork broth"], "allergens": ["Gluten", "Egg", "Soy"], "dietary_tags": [],
                "popularity_score": 0.96
            },
            {
                "category_id": ss_cats["Ramen & Soup"].id,
                "name": "Miso Soup",
                "description": "Delicate traditional Japanese broth made of fermented dashi stock, silken tofu cubes, wakame, and chopped spring onions.",
                "price": 320.00,
                "image_url": "/images/dishes/dish_9518aea945.jpg",
                "is_vegetarian": True,
                "spice_level": 0.1, "sweetness_level": 0.2, "creaminess_level": 0.2, "tanginess_level": 0.3,
                "masala_intensity_level": 0.3, "crunchiness_level": 0.2, "oiliness_level": 0.3, "saltiness_level": 0.3,
                "ingredients": ["Miso paste", "Silken tofu", "Wakame seaweed", "Scallions"], "allergens": ["Soy"], "dietary_tags": ["Vegetarian"],
                "popularity_score": 0.84
            },
            {
                "category_id": ss_cats["Wok Mains"].id,
                "name": "Teriyaki Chicken",
                "description": "Pan-roasted tender chicken thighs glazed in a sweet mirin-soy teriyaki sauce, served over a bed of steamed white jasmine rice.",
                "price": 680.00,
                "image_url": "/images/dishes/dish_b27e1cbabf.jpg",
                "is_vegetarian": False,
                "spice_level": 0.2, "sweetness_level": 0.7, "creaminess_level": 0.3, "tanginess_level": 0.3,
                "masala_intensity_level": 0.4, "crunchiness_level": 0.4, "oiliness_level": 0.3, "saltiness_level": 0.7,
                "ingredients": ["Chicken thighs", "Teriyaki glaze", "Broccoli", "Steamed jasmine rice"], "allergens": ["Soy", "Gluten"], "dietary_tags": [],
                "popularity_score": 0.91
            },
            {
                "category_id": ss_cats["Sushi Rolls"].id,
                "name": "Steamed Edamame",
                "description": "Freshly steamed whole young soybean pods lightly tossed in coarse sea salt and cracked red chili flakes.",
                "price": 290.00,
                "image_url": "/images/dishes/dish_188244ccb8.jpg",
                "is_vegetarian": True,
                "spice_level": 0.4, "sweetness_level": 0.1, "creaminess_level": 0.1, "tanginess_level": 0.2,
                "masala_intensity_level": 0.2, "crunchiness_level": 0.5, "oiliness_level": 0.2, "saltiness_level": 0.3,
                "ingredients": ["Edamame pods", "Coarse sea salt", "Chili flakes"], "allergens": ["Soy"], "dietary_tags": ["Vegetarian", "Vegan"],
                "popularity_score": 0.88
            }
        ]

        for d_data in ss_dishes:
            dish = Dish(restaurant_id=restaurants["spice-symphony"].id, **d_data)
            db.add(dish)
            inserted_dishes.append(dish)

        db.commit()

        # Seed Community Users and Signals
        for i in range(15):
            user = User(name=f"Community User {i+1}", email=f"user{i+1}@taste.ai")
            db.add(user)
            db.commit()
            db.refresh(user)

            profile = TasteProfile(
                user_id=user.id,
                spice_preference=random.uniform(0.1, 0.9),
                sweetness_preference=random.uniform(0.1, 0.9),
                creaminess_preference=random.uniform(0.1, 0.9),
                tanginess_preference=random.uniform(0.1, 0.9),
                masala_intensity_preference=random.uniform(0.1, 0.9),
                crunchiness_preference=random.uniform(0.1, 0.9),
                oiliness_preference=random.uniform(0.1, 0.9),
                saltiness_preference=random.uniform(0.1, 0.9),
                confidence_score=random.uniform(0.7, 0.9)
            )
            db.add(profile)
            
            # Each user likes 3-5 random dishes across all restaurants
            user_dishes = random.sample(inserted_dishes, random.randint(3, 5))
            for d in user_dishes:
                signal = CommunitySignal(
                    user_id=user.id,
                    dish_id=d.id,
                    ordered=True,
                    finished=True,
                    liked=True,
                    rating=random.randint(4, 5),
                    would_reorder=random.choice([True, False])
                )
                db.add(signal)
        
        db.commit()
        logger.info("Expanded authentic seeding completed successfully!")

    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
