from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# 1. Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

def seed_data():
    db: Session = SessionLocal()

    # Check if data already exists
    if db.query(models.Product).count() > 0:
        print("Database already has data. Skipping seed.")
        db.close()
        return

    print("Seeding 50 products...")

    # Helper to keep lines clean
    PLACEHOLDER_IMG = "https://via.placeholder.com/300"

    products_data = [
        # --- TECH ---
        {"title": "Wireless Noise Cancelling Headphones", "description": "Premium over-ear headphones with 30-hour battery life.", "price": 299.99, "brand": "SoundMax", "category": "Tech", "retailer": "Amazon", "url": "https://amazon.com/soundmax-headphones", "image_url": PLACEHOLDER_IMG, "tags": "audio,wireless,travel"},
        {"title": "Smart Fitness Tracker Band", "description": "Tracks steps, heart rate, and sleep. Waterproof.", "price": 49.99, "brand": "FitLife", "category": "Tech", "retailer": "Target", "url": "https://target.com/fitlife-band", "image_url": PLACEHOLDER_IMG, "tags": "fitness,health,wearable"},
        {"title": "4K Ultra HD Streaming Stick", "description": "Stream your favorite shows in brilliant 4K quality.", "price": 39.99, "brand": "StreamMaster", "category": "Tech", "retailer": "BestBuy", "url": "https://bestbuy.com/streammaster-4k", "image_url": PLACEHOLDER_IMG, "tags": "tv,streaming,entertainment"},
        {"title": "Portable Bluetooth Speaker", "description": "Rugged, waterproof speaker with punchy bass.", "price": 89.00, "brand": "BoomBox", "category": "Tech", "retailer": "Amazon", "url": "https://amazon.com/boombox-speaker", "image_url": PLACEHOLDER_IMG, "tags": "audio,outdoor,party"},
        {"title": "Ergonomic Wireless Mouse", "description": "Vertical design to reduce wrist strain during work.", "price": 25.50, "brand": "ErgoTech", "category": "Tech", "retailer": "Walmart", "url": "https://walmart.com/ergotech-mouse", "image_url": PLACEHOLDER_IMG, "tags": "office,computer,ergonomic"},
        {"title": "Mechanical Gaming Keyboard", "description": "RGB backlit keyboard with blue switches.", "price": 75.00, "brand": "GameZone", "category": "Tech", "retailer": "Amazon", "url": "https://amazon.com/gamezone-keyboard", "image_url": PLACEHOLDER_IMG, "tags": "gaming,computer,rgb"},
        {"title": "10000mAh Power Bank", "description": "Fast charging portable battery for phones and tablets.", "price": 22.99, "brand": "ChargeIt", "category": "Tech", "retailer": "Target", "url": "https://target.com/chargeit-bank", "image_url": PLACEHOLDER_IMG, "tags": "mobile,travel,accessory"},
        {"title": "Smart Home Hub Mini", "description": "Control your lights and thermostat with voice.", "price": 35.00, "brand": "HomeSmart", "category": "Tech", "retailer": "BestBuy", "url": "https://bestbuy.com/homesmart-mini", "image_url": PLACEHOLDER_IMG, "tags": "smart home,voice,assistant"},
        {"title": "Tablet Stand Adjustable", "description": "Aluminum stand for iPads and tablets.", "price": 18.99, "brand": "DeskMate", "category": "Tech", "retailer": "Amazon", "url": "https://amazon.com/deskmate-stand", "image_url": PLACEHOLDER_IMG, "tags": "accessory,office,tablet"},
        {"title": "USB-C Hub Adapter", "description": "Expand your laptop ports with HDMI, USB, and SD card.", "price": 45.00, "brand": "PortPlus", "category": "Tech", "retailer": "Walmart", "url": "https://walmart.com/portplus-hub", "image_url": PLACEHOLDER_IMG, "tags": "computer,accessory,work"},

        # --- BEAUTY ---
        {"title": "Hydrating Face Serum", "description": "Hyaluronic acid serum for glowing skin.", "price": 28.00, "brand": "GlowSkin", "category": "Beauty", "retailer": "Sephora", "url": "https://sephora.com/glowskin-serum", "image_url": PLACEHOLDER_IMG, "tags": "skincare,face,hydration"},
        {"title": "Matte Lipstick Set", "description": "Set of 5 long-lasting matte lipsticks.", "price": 32.50, "brand": "LipLuxe", "category": "Beauty", "retailer": "Ulta", "url": "https://ulta.com/lipluxe-set", "image_url": PLACEHOLDER_IMG, "tags": "makeup,lips,gift set"},
        {"title": "Organic Lavender Bath Bombs", "description": "Pack of 6 fizzy bath bombs for relaxation.", "price": 19.99, "brand": "PureBath", "category": "Beauty", "retailer": "Amazon", "url": "https://amazon.com/purebath-bombs", "image_url": PLACEHOLDER_IMG, "tags": "bath,relaxation,spa"},
        {"title": "Vitamin C Daily Moisturizer", "description": "Brightens skin tone and reduces dark spots.", "price": 42.00, "brand": "Radiance", "category": "Beauty", "retailer": "Target", "url": "https://target.com/radiance-vitc", "image_url": PLACEHOLDER_IMG, "tags": "skincare,face,daily"},
        {"title": "Professional Makeup Brush Set", "description": "12-piece synthetic brush set with travel case.", "price": 24.99, "brand": "BrushPro", "category": "Beauty", "retailer": "Amazon", "url": "https://amazon.com/brushpro-set", "image_url": PLACEHOLDER_IMG, "tags": "makeup,tools,travel"},
        {"title": "Charcoal Detox Mask", "description": "Deep cleansing mask to remove impurities.", "price": 15.00, "brand": "ClearFace", "category": "Beauty", "retailer": "Ulta", "url": "https://ulta.com/clearface-mask", "image_url": PLACEHOLDER_IMG, "tags": "skincare,mask,detox"},
        {"title": "Hair Repair Oil", "description": "Argan oil treatment for dry and damaged hair.", "price": 21.50, "brand": "SilkyHair", "category": "Beauty", "retailer": "Sephora", "url": "https://sephora.com/silkyhair-oil", "image_url": PLACEHOLDER_IMG, "tags": "haircare,repair,oil"},
        {"title": "Rose Quartz Roller", "description": "Facial roller for reducing puffiness.", "price": 12.99, "brand": "SkinZen", "category": "Beauty", "retailer": "Amazon", "url": "https://amazon.com/skinzen-roller", "image_url": PLACEHOLDER_IMG, "tags": "skincare,tools,wellness"},
        {"title": "Men's Grooming Kit", "description": "Includes beard oil, comb, and face wash.", "price": 35.00, "brand": "GentlemanCo", "category": "Beauty", "retailer": "Target", "url": "https://target.com/gentlemanco-kit", "image_url": PLACEHOLDER_IMG, "tags": "men,grooming,gift set"},
        {"title": "Scented Soy Candle (Vanilla)", "description": "Hand-poured soy candle with 40h burn time.", "price": 18.00, "brand": "HomeScents", "category": "Beauty", "retailer": "Etsy", "url": "https://etsy.com/homescents-vanilla", "image_url": PLACEHOLDER_IMG, "tags": "home,fragrance,relaxation"},

        # --- HOME ---
        {"title": "Ceramic Plant Pot Set", "description": "Three minimal white pots with drainage holes.", "price": 29.99, "brand": "GreenThumb", "category": "Home", "retailer": "Amazon", "url": "https://amazon.com/greenthumb-pots", "image_url": PLACEHOLDER_IMG, "tags": "decor,plants,garden"},
        {"title": "Soft Throw Blanket", "description": "Fleece blanket, 50x60 inches, navy blue.", "price": 24.50, "brand": "CozyHome", "category": "Home", "retailer": "Target", "url": "https://target.com/cozyhome-blanket", "image_url": PLACEHOLDER_IMG, "tags": "decor,comfort,winter"},
        {"title": "Stainless Steel Water Bottle", "description": "Insulated bottle keeps drinks cold for 24h.", "price": 22.00, "brand": "HydroCool", "category": "Home", "retailer": "Amazon", "url": "https://amazon.com/hydrocool-bottle", "image_url": PLACEHOLDER_IMG, "tags": "travel,kitchen,eco-friendly"},
        {"title": "Bamboo Cutting Board", "description": "Durable and eco-friendly kitchen chopping board.", "price": 16.99, "brand": "ChefChoice", "category": "Home", "retailer": "Walmart", "url": "https://walmart.com/chefchoice-board", "image_url": PLACEHOLDER_IMG, "tags": "kitchen,cooking,eco-friendly"},
        {"title": "Digital Picture Frame", "description": "Share photos instantly via email to this frame.", "price": 89.99, "brand": "Memories", "category": "Home", "retailer": "BestBuy", "url": "https://bestbuy.com/memories-frame", "image_url": PLACEHOLDER_IMG, "tags": "decor,tech,family"},
        {"title": "Essential Oil Diffuser", "description": "Ultrasonic aroma humidifier with LED lights.", "price": 27.99, "brand": "ZenSpace", "category": "Home", "retailer": "Amazon", "url": "https://amazon.com/zenspace-diffuser", "image_url": PLACEHOLDER_IMG, "tags": "wellness,decor,fragrance"},
        {"title": "Coffee Maker (Single Serve)", "description": "Brew a fresh cup in under a minute.", "price": 49.99, "brand": "BrewMaster", "category": "Home", "retailer": "Target", "url": "https://target.com/brewmaster-single", "image_url": PLACEHOLDER_IMG, "tags": "kitchen,coffee,appliance"},
        {"title": "Weighted Blanket (15lbs)", "description": "Promotes better sleep and reduces anxiety.", "price": 55.00, "brand": "SleepWell", "category": "Home", "retailer": "Amazon", "url": "https://amazon.com/sleepwell-weighted", "image_url": PLACEHOLDER_IMG, "tags": "bedding,wellness,sleep"},
        {"title": "Set of 4 Wine Glasses", "description": "Elegant crystal glasses for red or white wine.", "price": 39.00, "brand": "Cheers", "category": "Home", "retailer": "Crate&Barrel", "url": "https://crateandbarrel.com/cheers-glasses", "image_url": PLACEHOLDER_IMG, "tags": "kitchen,dining,party"},
        {"title": "Desk Lamp with USB Port", "description": "LED lamp with adjustable brightness and charging.", "price": 32.99, "brand": "BrightWork", "category": "Home", "retailer": "Amazon", "url": "https://amazon.com/brightwork-lamp", "image_url": PLACEHOLDER_IMG, "tags": "office,decor,lighting"},

        # --- TOYS ---
        {"title": "LEGO Starship Kit", "description": "Build your own space fighter. 500 pieces.", "price": 59.99, "brand": "BrickMaster", "category": "Toys", "retailer": "Target", "url": "https://target.com/brickmaster-starship", "image_url": PLACEHOLDER_IMG, "tags": "building,kids,creative"},
        {"title": "Plush Teddy Bear", "description": "Super soft 12-inch bear. Hypoallergenic.", "price": 14.99, "brand": "CuddleFriends", "category": "Toys", "retailer": "Amazon", "url": "https://amazon.com/cuddlefriends-bear", "image_url": PLACEHOLDER_IMG, "tags": "plush,kids,soft"},
        {"title": "Remote Control Car", "description": "High speed off-road racer with rechargeable battery.", "price": 45.00, "brand": "SpeedRacers", "category": "Toys", "retailer": "Walmart", "url": "https://walmart.com/speedracers-car", "image_url": PLACEHOLDER_IMG, "tags": "rc,outdoor,vehicle"},
        {"title": "Board Game - Strategy", "description": "Conquer territories in this classic strategy game.", "price": 35.00, "brand": "GameNight", "category": "Toys", "retailer": "Amazon", "url": "https://amazon.com/gamenight-strategy", "image_url": PLACEHOLDER_IMG, "tags": "game,family,strategy"},
        {"title": "Art Supplies Kit", "description": "Paints, brushes, and canvas for young artists.", "price": 28.99, "brand": "CreateIt", "category": "Toys", "retailer": "Michaels", "url": "https://michaels.com/createit-kit", "image_url": PLACEHOLDER_IMG, "tags": "creative,art,kids"},
        {"title": "Science Experiment Set", "description": "20 fun chemistry experiments for kids.", "price": 22.50, "brand": "SciKid", "category": "Toys", "retailer": "Target", "url": "https://target.com/scikid-set", "image_url": PLACEHOLDER_IMG, "tags": "educational,science,stem"},
        {"title": "Puzzle (1000 Piece)", "description": "Challenging landscape puzzle of the Alps.", "price": 18.00, "brand": "PuzzleMaster", "category": "Toys", "retailer": "Amazon", "url": "https://amazon.com/puzzlemaster-alps", "image_url": PLACEHOLDER_IMG, "tags": "puzzle,family,brain"},
        {"title": "Action Figure Hero", "description": "Poseable superhero figure with accessories.", "price": 12.99, "brand": "HeroWorld", "category": "Toys", "retailer": "Walmart", "url": "https://walmart.com/heroworld-figure", "image_url": PLACEHOLDER_IMG, "tags": "action,kids,collectible"},
        {"title": "Wooden Building Blocks", "description": "Classic set of 50 wooden blocks for toddlers.", "price": 25.00, "brand": "WoodWorks", "category": "Toys", "retailer": "Amazon", "url": "https://amazon.com/woodworks-blocks", "image_url": PLACEHOLDER_IMG, "tags": "toddler,building,educational"},
        {"title": "Drone with Camera", "description": "Beginner drone with 720p HD camera.", "price": 65.00, "brand": "SkyFly", "category": "Toys", "retailer": "BestBuy", "url": "https://bestbuy.com/skyfly-drone", "image_url": PLACEHOLDER_IMG, "tags": "tech,outdoor,camera"},
        
        # --- MISC ---
        {"title": "Portable Hard Drive 1TB", "description": "Backup your files securely. USB 3.0.", "price": 55.00, "brand": "DataSafe", "category": "Tech", "retailer": "Amazon", "url": "https://amazon.com/datasafe-1tb", "image_url": PLACEHOLDER_IMG, "tags": "storage,computer,work"},
        {"title": "Video Doorbell", "description": "See who is at the door from your phone.", "price": 99.00, "brand": "SecureHome", "category": "Tech", "retailer": "HomeDepot", "url": "https://homedepot.com/securehome-bell", "image_url": PLACEHOLDER_IMG, "tags": "smart home,security,tech"},
        {"title": "Yoga Mat Non-Slip", "description": "Extra thick mat for yoga and pilates.", "price": 22.00, "brand": "ZenFit", "category": "Home", "retailer": "Amazon", "url": "https://amazon.com/zenfit-mat", "image_url": PLACEHOLDER_IMG, "tags": "fitness,health,yoga"},
        {"title": "Cookbook Stand", "description": "Holds your cookbook open while you cook.", "price": 14.50, "brand": "ChefHelper", "category": "Home", "retailer": "Target", "url": "https://target.com/chefhelper-stand", "image_url": PLACEHOLDER_IMG, "tags": "kitchen,cooking,accessory"},
        {"title": "Kids Walkie Talkies", "description": "Long range communication for outdoor play.", "price": 29.99, "brand": "TalkTime", "category": "Toys", "retailer": "Walmart", "url": "https://walmart.com/talktime-walkie", "image_url": PLACEHOLDER_IMG, "tags": "outdoor,kids,communication"},
        {"title": "Electric Toothbrush", "description": "Rechargeable brush with 2 minute timer.", "price": 39.99, "brand": "SmileBright", "category": "Beauty", "retailer": "Amazon", "url": "https://amazon.com/smilebright-electric", "image_url": PLACEHOLDER_IMG, "tags": "dental,health,daily"},
        {"title": "Digital Alarm Clock", "description": "Large display with USB charging port.", "price": 19.99, "brand": "TimeKeeper", "category": "Home", "retailer": "Target", "url": "https://target.com/timekeeper-clock", "image_url": PLACEHOLDER_IMG, "tags": "bedroom,tech,clock"},
        {"title": "Wireless Charging Pad", "description": "Qi-certified charger for iPhone and Android.", "price": 15.99, "brand": "ChargePad", "category": "Tech", "retailer": "Amazon", "url": "https://amazon.com/chargepad-wireless", "image_url": PLACEHOLDER_IMG, "tags": "mobile,accessory,charging"},
        {"title": "Travel Backpack", "description": "Lightweight water-resistant daypack.", "price": 45.00, "brand": "TravelGo", "category": "Home", "retailer": "REI", "url": "https://rei.com/travelgo-pack", "image_url": PLACEHOLDER_IMG, "tags": "travel,outdoor,bag"},
        {"title": "Tea Sampler Box", "description": "Collection of 10 herbal and black teas.", "price": 21.00, "brand": "TeaTime", "category": "Home", "retailer": "Amazon", "url": "https://amazon.com/teatime-sampler", "image_url": PLACEHOLDER_IMG, "tags": "food,drink,gift set"},
    ]

    for p in products_data:
        db_product = models.Product(**p)
        db.add(db_product)
    
    db.commit()
    print("Successfully seeded 50 products!")
    db.close()

if __name__ == "__main__":
    seed_data()