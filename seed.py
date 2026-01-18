from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models


models.Base.metadata.create_all(bind=engine)

def seed_data():
    db: Session = SessionLocal()

    # CLEAR old data so we can see new images
    print("Clearing old data...")
    db.query(models.Event).delete()   # Delete events first (foreign key)
    db.query(models.Product).delete() # Delete products
    db.commit()

    print("Seeding 50 products...")

    # Helper to keep lines clean
    PLACEHOLDER_IMG = "https://via.placeholder.com/300"

    products_data = [
        
        
        # --- TECH ---
        {
            "title": "Sony WH-1000XM5 Noise Canceling Headphones",
            "description": "Industry-leading noise cancellation with 30-hour battery life and ultra-comfortable fit.",
            "price": 348.00,
            "brand": "Sony",
            "category": "Tech",
            "retailer": "Amazon",
            "url": "https://electronics.sony.com/audio/headphones/headband/p/wh1000xm5-b",
            "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=500&q=60",
            "tags": "audio,wireless,travel,music,premium"
        },
        {
            "title": "Fujifilm Instax Mini 11 Instant Camera",
            "description": "Capture memories instantly with this fun, easy-to-use camera. Built-in selfie lens and auto-exposure.",
            "price": 76.00,
            "brand": "Fujifilm",
            "category": "Tech",
            "retailer": "Target",
            "url": "https://www.target.com/p/fujifilm-instax-mini-11-camera/-/A-78330000",
            "image_url": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=500&q=60",
            "tags": "camera,photography,fun,travel,gift"
        },
        {
            "title": "Apple Watch Series 9",
            "description": "Advanced health sensors, fitness tracking, and safety features. Carbon neutral combination available.",
            "price": 399.00,
            "brand": "Apple",
            "category": "Tech",
            "retailer": "BestBuy",
            "url": "https://www.bestbuy.com/site/apple-watch-series-9",
            "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=500&q=60",
            "tags": "wearable,fitness,health,smartwatch,apple"
        },
        {
            "title": "Marshall Emberton Bluetooth Speaker",
            "description": "Compact portable speaker with the loud and vibrant sound only Marshall can deliver. 20+ hours of playtime.",
            "price": 169.99,
            "brand": "Marshall",
            "category": "Tech",
            "retailer": "Amazon",
            "url": "https://www.marshallheadphones.com/us/en/emberton-ii.html",
            "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=500&q=60",
            "tags": "audio,speaker,music,party,portable"
        },

        # --- BEAUTY ---
        {
            "title": "Glow Recipe Watermelon Glow Niacinamide Dew Drops",
            "description": "A breakthrough, multi-use highlighting serum that hydrates and visibly reduces the look of hyperpigmentation.",
            "price": 35.00,
            "brand": "Glow Recipe",
            "category": "Beauty",
            "retailer": "Sephora",
            "url": "https://www.sephora.com/product/glow-recipe-watermelon-glow-niacinamide-dew-drops-P466123",
            "image_url": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&w=500&q=60",
            "tags": "skincare,glow,serum,hydration,trending"
        },
        {
            "title": "Dyson Airwrap Multi-Styler",
            "description": "Curl. Shape. Smooth and hide flyaways. With no extreme heat. Re-engineered attachments for faster styling.",
            "price": 599.00,
            "brand": "Dyson",
            "category": "Beauty",
            "retailer": "Ulta",
            "url": "https://www.ulta.com/p/airwrap-multi-styler-pimprod2032688",
            "image_url": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=500&q=60",
            "tags": "hair,styling,luxury,tools,haircare"
        },
        {
            "title": "Rare Beauty Soft Pinch Liquid Blush",
            "description": "A weightless, long-lasting liquid blush that blends and builds beautifully for a soft, healthy flush.",
            "price": 23.00,
            "brand": "Rare Beauty",
            "category": "Beauty",
            "retailer": "Sephora",
            "url": "https://www.sephora.com/product/rare-beauty-by-selena-gomez-soft-pinch-liquid-blush-P455739",
            "image_url": "https://images.unsplash.com/photo-1515688594390-b649af70d282?auto=format&fit=crop&w=500&q=60",
            "tags": "makeup,blush,face,viral,gift"
        },
        {
            "title": "Laneige Lip Sleeping Mask",
            "description": "A leave-on lip mask that delivers intense moisture and antioxidants while you sleep.",
            "price": 24.00,
            "brand": "Laneige",
            "category": "Beauty",
            "retailer": "Amazon",
            "url": "https://us.laneige.com/products/lip-sleeping-mask",
            "image_url": "https://images.unsplash.com/photo-1629198688000-71f23e745b6e?auto=format&fit=crop&w=500&q=60",
            "tags": "skincare,lips,mask,hydration,selfcare"
        },

        # --- HOME ---
        {
            "title": "Levitating Moon Lamp",
            "description": "3D printed moon light that floats and spins automatically. 3 colors modes.",
            "price": 99.99,
            "brand": "Gingko",
            "category": "Home",
            "retailer": "Amazon",
            "url": "https://www.amazon.com/Levitating-Moon-Lamp-Floating-Magnetic/dp/B07L32KG4Z",
            "image_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=500&q=60",
            "tags": "decor,lighting,unique,cool,bedroom"
        },
        {
            "title": "Nespresso Vertuo Plus Coffee Maker",
            "description": "Single-serve coffee and espresso machine. Brews 4 cup sizes.",
            "price": 149.00,
            "brand": "Nespresso",
            "category": "Home",
            "retailer": "Williams Sonoma",
            "url": "https://www.nespresso.com/us/en/order/machines/vertuo",
            "image_url": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?auto=format&fit=crop&w=500&q=60",
            "tags": "kitchen,coffee,appliance,morning,gift"
        },
        {
            "title": "Monstera Deliciosa (Swiss Cheese Plant)",
            "description": "Live indoor plant in a ceramic pot. Easy to care for and purifies the air.",
            "price": 45.00,
            "brand": "The Sill",
            "category": "Home",
            "retailer": "The Sill",
            "url": "https://www.thesill.com/products/monstera-deliciosa",
            "image_url": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?auto=format&fit=crop&w=500&q=60",
            "tags": "plants,nature,decor,living room,wellness"
        },
        {
            "title": "Diptyque Baies Scented Candle",
            "description": "Luxurious candle with notes of blackcurrant leaves and Bulgarian roses.",
            "price": 74.00,
            "brand": "Diptyque",
            "category": "Home",
            "retailer": "Nordstrom",
            "url": "https://www.diptyqueparis.com/en_us/p/baies-candle.html",
            "image_url": "https://images.unsplash.com/photo-1603006905003-be475563bc59?auto=format&fit=crop&w=500&q=60",
            "tags": "fragrance,candle,luxury,relax,home"
        },

        # --- TOYS ---
        {
            "title": "LEGO Star Wars Millennium Falcon",
            "description": "Build the iconic starship from Star Wars. 1351 pieces with 7 minifigures.",
            "price": 169.99,
            "brand": "LEGO",
            "category": "Toys",
            "retailer": "LEGO Store",
            "url": "https://www.lego.com/en-us/product/millennium-falcon-75257",
            "image_url": "https://images.unsplash.com/photo-1585366119957-e9730b6d0f60?auto=format&fit=crop&w=500&q=60",
            "tags": "lego,star wars,building,kids,collection"
        },
        {
            "title": "Jellycat Bashful Beige Bunny",
            "description": "The softest plush bunny with floppy ears. Suitable from birth.",
            "price": 25.00,
            "brand": "Jellycat",
            "category": "Toys",
            "retailer": "Amazon",
            "url": "https://www.jellycat.com/us/bashful-beige-bunny-bas3b/",
            "image_url": "https://cdn11.bigcommerce.com/s-23s5gfmhr7/images/stencil/1000w/products/294/41548/BAS3B__06287.1727975732.jpg?c=1",
            "tags": "plush,soft,baby,kids,cute"
        },
        {
            "title": "Magna-Tiles 100-Piece Set",
            "description": "The original 3D magnetic building tiles. Fosters creativity and STEM learning.",
            "price": 119.99,
            "brand": "Magna-Tiles",
            "category": "Toys",
            "retailer": "Target",
            "url": "https://www.target.com/p/magna-tiles-clear-colors-100pc-set/-/A-14264620",
            "image_url": "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?auto=format&fit=crop&w=500&q=60",
            "tags": "educational,building,kids,stem,creative"
        },

        # ==========================================
        # FILLER PRODUCTS 
        # ==========================================
        
        # --- MORE TECH ---
        # Fixed: Image link updated
        {"title": "Fitbit Inspire 3 Fitness Tracker", "description": "Tracks steps, heart rate, and sleep with 10-day battery life.", "price": 99.95, "brand": "Fitbit", "category": "Tech", "retailer": "Target", "url": "https://target.com/p/fitbit-inspire-3", "image_url": "https://target.scene7.com/is/image/Target/GUEST_fc31fcf8-9cd0-4c74-9ea0-124b51378c04?qlt=85&fmt=webp&hei=500&wid=500", "tags": "fitness,health,wearable"},
        {"title": "Roku Streaming Stick 4K", "description": "Stream your favorite shows in brilliant 4K quality with Dolby Vision.", "price": 49.99, "brand": "Roku", "category": "Tech", "retailer": "BestBuy", "url": "https://bestbuy.com/site/roku-streaming-stick-4k", "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=500&q=60", "tags": "tv,streaming,entertainment"},
        {"title": "Logitech Lift Vertical Mouse", "description": "Ergonomic vertical design to reduce wrist strain during work.", "price": 69.99, "brand": "Logitech", "category": "Tech", "retailer": "Amazon", "url": "https://amazon.com/logitech-lift-vertical", "image_url": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&w=500&q=60", "tags": "office,computer,ergonomic"},
        # Fixed: Image link updated
        {"title": "Keychron K2 Mechanical Keyboard", "description": "Wireless RGB mechanical keyboard for Mac and Windows.", "price": 79.99, "brand": "Keychron", "category": "Tech", "retailer": "Amazon", "url": "https://amazon.com/keychron-k2", "image_url": "https://images.unsplash.com/photo-1595225476474-87563907a212?auto=format&fit=crop&w=500&q=60", "tags": "gaming,computer,rgb"},
        {"title": "Anker 737 Power Bank", "description": "24,000mAh ultra-fast portable charger for laptops and phones.", "price": 149.99, "brand": "Anker", "category": "Tech", "retailer": "Anker", "url": "https://www.anker.com/products/a1289", "image_url": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?auto=format&fit=crop&w=500&q=60", "tags": "mobile,travel,accessory"},
        {"title": "Google Nest Audio", "description": "Smart speaker with room-filling sound and Google Assistant.", "price": 99.99, "brand": "Google", "category": "Tech", "retailer": "BestBuy", "url": "https://store.google.com/product/nest_audio", "image_url": "https://images.unsplash.com/photo-1589492477829-5e65395b66cc?auto=format&fit=crop&w=500&q=60", "tags": "smart home,voice,assistant"},
        {"title": "Lamicall Tablet Stand", "description": "Adjustable aluminum stand for iPad, Galaxy Tab, and Kindle.", "price": 19.99, "brand": "Lamicall", "category": "Tech", "retailer": "Amazon", "url": "https://amazon.com/lamicall-tablet-stand", "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=500&q=60", "tags": "accessory,office,tablet"},
        {"title": "Anker USB-C Hub", "description": "Expand your laptop with HDMI, USB 3.0, and SD card slots.", "price": 39.99, "brand": "Anker", "category": "Tech", "retailer": "Amazon", "url": "https://amazon.com/anker-usb-c-hub", "image_url": "https://images.unsplash.com/photo-1625842268584-8f3296236761?auto=format&fit=crop&w=500&q=60", "tags": "computer,accessory,work"},
        # Fixed: Image link updated
        {"title": "Seagate Portable 2TB HDD", "description": "Reliable external storage for backing up your files.", "price": 62.99, "brand": "Seagate", "category": "Tech", "retailer": "Amazon", "url": "https://amazon.com/seagate-portable", "image_url": "https://images.unsplash.com/photo-1597852074816-d933c7d2b988?auto=format&fit=crop&w=500&q=60", "tags": "storage,computer,work"},
        # Fixed: Image link updated
        {"title": "Ring Video Doorbell", "description": "1080p HD video doorbell with enhanced motion detection.", "price": 99.99, "brand": "Ring", "category": "Tech", "retailer": "Amazon", "url": "https://amazon.com/ring-video-doorbell", "image_url": "https://m.media-amazon.com/images/I/61-UAVvjGsL._AC_UY327_FMwebp_QL65_.jpg", "tags": "smart home,security,tech"},

        # --- MORE BEAUTY ---
        {"title": "MAC Matte Lipstick", "description": "The iconic matte lipstick with rich color and no shine.", "price": 23.00, "brand": "MAC", "category": "Beauty", "retailer": "Ulta", "url": "https://ulta.com/mac-matte-lipstick", "image_url": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?auto=format&fit=crop&w=500&q=60", "tags": "makeup,lips,gift set"},
        {"title": "Da Bomb Bath Fizzers", "description": "Handmade bath bombs with a surprise inside.", "price": 7.50, "brand": "Da Bomb", "category": "Beauty", "retailer": "Target", "url": "https://target.com/da-bomb", "image_url": "https://images.unsplash.com/photo-1600880292203-757bb62b4baf?auto=format&fit=crop&w=500&q=60", "tags": "bath,relaxation,spa"},
        # Fixed: Image link updated
        {"title": "CeraVe Daily Moisturizing Lotion", "description": "Lightweight oil-free moisturizer with hyaluronic acid.", "price": 14.99, "brand": "CeraVe", "category": "Beauty", "retailer": "Target", "url": "https://target.com/cerave-lotion", "image_url": "https://target.scene7.com/is/image/Target/GUEST_5876066f-6cd4-41c1-b2d9-58ba0461f7ee?qlt=85&fmt=webp&hei=500&wid=500", "tags": "skincare,face,daily"},
        # Fixed: Image link updated
        {"title": "Real Techniques Brush Set", "description": "Everyday Essentials makeup brush set with sponge.", "price": 19.99, "brand": "Real Techniques", "category": "Beauty", "retailer": "Ulta", "url": "https://ulta.com/real-techniques-set", "image_url": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=500&q=60", "tags": "makeup,tools,travel"},
        {"title": "Origins Clear Improvement Mask", "description": "Active charcoal mask to clear pores.", "price": 29.00, "brand": "Origins", "category": "Beauty", "retailer": "Sephora", "url": "https://sephora.com/origins-mask", "image_url": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=500&q=60", "tags": "skincare,mask,detox"},
        {"title": "Moroccanoil Treatment", "description": "Argan oil hair treatment for conditioning and styling.", "price": 48.00, "brand": "Moroccanoil", "category": "Beauty", "retailer": "Sephora", "url": "https://sephora.com/moroccanoil", "image_url": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&w=500&q=60", "tags": "haircare,repair,oil"},
        {"title": "Herbivore Jade Roller", "description": "Facial roller for reducing puffiness and tension.", "price": 30.00, "brand": "Herbivore", "category": "Beauty", "retailer": "Sephora", "url": "https://sephora.com/herbivore-roller", "image_url": "https://images.unsplash.com/photo-1616683693504-3ea7e9ad6fec?auto=format&fit=crop&w=500&q=60", "tags": "skincare,tools,wellness"},
        {"title": "Harry's Men's Shave Set", "description": "Quality razor handle, blades, and shave gel.", "price": 25.00, "brand": "Harry's", "category": "Beauty", "retailer": "Target", "url": "https://target.com/harrys-set", "image_url": "https://images.unsplash.com/photo-1621607512214-68297480165e?auto=format&fit=crop&w=500&q=60", "tags": "men,grooming,gift set"},

        # --- MORE HOME ---
        {"title": "West Elm Ceramic Planters", "description": "Modern mid-century ceramic planters.", "price": 30.00, "brand": "West Elm", "category": "Home", "retailer": "West Elm", "url": "https://westelm.com/products/planters", "image_url": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?auto=format&fit=crop&w=500&q=60", "tags": "decor,plants,garden"},
        # Fixed: Image link updated
        {"title": "Bearaby Cotton Napper", "description": "Chunky knit weighted blanket made of organic cotton.", "price": 249.00, "brand": "Bearaby", "category": "Home", "retailer": "Bearaby", "url": "https://bearaby.com", "image_url": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?auto=format&fit=crop&w=500&q=60", "tags": "decor,comfort,winter"},
        # Fixed: Image link updated
        {"title": "Hydro Flask Wide Mouth", "description": "32 oz insulated stainless steel water bottle.", "price": 44.95, "brand": "Hydro Flask", "category": "Home", "retailer": "Amazon", "url": "https://amazon.com/hydroflask", "image_url": "https://m.media-amazon.com/images/I/51yfoQ8M9nL._AC_SY300_SX300_QL70_FMwebp_.jpg", "tags": "travel,kitchen,eco-friendly"},
        {"title": "Material Kitchen ReBoard", "description": "Recycled plastic and sugarcane cutting board.", "price": 35.00, "brand": "Material", "category": "Home", "retailer": "Material Kitchen", "url": "https://materialkitchen.com", "image_url": "https://images.unsplash.com/photo-1606787366850-de6330128bfc?auto=format&fit=crop&w=500&q=60", "tags": "kitchen,cooking,eco-friendly"},
        # Fixed: Image link updated
        {"title": "Aura Carver Digital Frame", "description": "Smart digital picture frame with unlimited photo storage.", "price": 149.00, "brand": "Aura", "category": "Home", "retailer": "Amazon", "url": "https://auraframes.com", "image_url": "https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?auto=format&fit=crop&w=500&q=60", "tags": "decor,tech,family"},
        # Fixed: Image link updated
        {"title": "Vitruvi Stone Diffuser", "description": "Ceramic ultrasonic essential oil diffuser.", "price": 123.00, "brand": "Vitruvi", "category": "Home", "retailer": "Vitruvi", "url": "https://vitruvi.com", "image_url": "https://vitruvi.com/cdn/shop/files/pdp_stone-diffuser_front_white_gallery_1_v9_image.png?v=1759291810&width=1100", "tags": "wellness,decor,fragrance"},
        # Fixed: Image link updated
        {"title": "Gravity Weighted Blanket", "description": "The original weighted blanket for sleep and stress.", "price": 195.00, "brand": "Gravity", "category": "Home", "retailer": "Gravity", "url": "https://gravityblankets.com", "image_url": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=500&q=60", "tags": "bedding,wellness,sleep"},
        {"title": "Crate & Barrel Wine Glasses", "description": "Contemporary red wine glasses, set of 4.", "price": 59.95, "brand": "Crate & Barrel", "category": "Home", "retailer": "Crate & Barrel", "url": "https://crateandbarrel.com", "image_url": "https://images.unsplash.com/photo-1535958636474-b021ee887b13?auto=format&fit=crop&w=500&q=60", "tags": "kitchen,dining,party"},
        # Fixed: Image link updated
        {"title": "West Elm Industrial Task Lamp", "description": "Adjustable table lamp with USB charging.", "price": 159.00, "brand": "West Elm", "category": "Home", "retailer": "West Elm", "url": "https://westelm.com", "image_url": "https://assets.weimgs.com/weimgs/rk/images/wcm/products/202543/0015/industrial-outline-table-lamp-27-xl.jpg"},

        # --- MORE TOYS ---
        {"title": "Traxxas Rustler RC Car", "description": "High-performance off-road RC truck.", "price": 199.95, "brand": "Traxxas", "category": "Toys", "retailer": "Amazon", "url": "https://traxxas.com", "image_url": "https://images.unsplash.com/photo-1594787318286-3d835c1d207f?auto=format&fit=crop&w=500&q=60", "tags": "rc,outdoor,vehicle"},
        # Fixed: Image link updated
        {"title": "Catan Board Game", "description": "Trade, build, and settle in this classic strategy game.", "price": 44.00, "brand": "Catan Studio", "category": "Toys", "retailer": "Target", "url": "https://target.com/catan", "image_url": "https://images.unsplash.com/photo-1611195974226-a6a9be9dd763?auto=format&fit=crop&w=500&q=60", "tags": "game,family,strategy"},
        {"title": "Crayola Inspiration Art Case", "description": "140-piece art set with crayons, pencils, and markers.", "price": 24.99, "brand": "Crayola", "category": "Toys", "retailer": "Amazon", "url": "https://crayola.com", "image_url": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=500&q=60", "tags": "creative,art,kids"},
        {"title": "National Geographic Science Kit", "description": "Earth science kit with crystals and tornados.", "price": 29.99, "brand": "National Geographic", "category": "Toys", "retailer": "Amazon", "url": "https://amazon.com/nat-geo", "image_url": "https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&w=500&q=60", "tags": "educational,science,stem"},
        {"title": "Ravensburger Puzzle (1000pc)", "description": "High-quality landscape puzzle.", "price": 25.00, "brand": "Ravensburger", "category": "Toys", "retailer": "Amazon", "url": "https://ravensburger.org", "image_url": "https://images.unsplash.com/photo-1587586062323-836089e60d52?auto=format&fit=crop&w=500&q=60", "tags": "puzzle,family,brain"},
        {"title": "Marvel Legends Action Figure", "description": "6-inch collectible Spider-Man figure.", "price": 24.99, "brand": "Hasbro", "category": "Toys", "retailer": "Target", "url": "https://hasbro.com", "image_url": "https://images.unsplash.com/photo-1608354580875-30bd4168b351?auto=format&fit=crop&w=500&q=60", "tags": "action,kids,collectible"},
        {"title": "Melissa & Doug Wooden Blocks", "description": "Solid wood building blocks set.", "price": 23.99, "brand": "Melissa & Doug", "category": "Toys", "retailer": "Amazon", "url": "https://melissaanddoug.com", "image_url": "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?auto=format&fit=crop&w=500&q=60", "tags": "toddler,building,educational"},
        {"title": "DJI Mini 2 SE Drone", "description": "Lightweight camera drone with QHD video.", "price": 299.00, "brand": "DJI", "category": "Toys", "retailer": "BestBuy", "url": "https://dji.com", "image_url": "https://images.unsplash.com/photo-1507582020474-9a35b7d455d9?auto=format&fit=crop&w=500&q=60", "tags": "tech,outdoor,camera"},
    ]

    for p in products_data:
        db_product = models.Product(**p)
        db.add(db_product)
    
    db.commit()
    print("Successfully seeded 50 products!")
    db.close()

if __name__ == "__main__":
    seed_data()