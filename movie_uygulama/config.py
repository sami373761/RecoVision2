import os
from dotenv import load_dotenv

load_dotenv()

# ----------------------------
# API Anahtarları
# ----------------------------
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "c999e9521d42cbbf37212d74828cbd5d")
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY", "AIzaSyBkf8kSV95UAEVued1SRd_3atQ1ZdKOzNk")
# ----------------------------
# Film Kategorileri (Movie)
# ----------------------------
CATEGORY_NAMES_MOVIE = {
    "action": "28",
    "adventure": "12",
    "animation": "16",
    "comedy": "35",
    "crime": "80",
    "documentary": "99",
    "drama": "18",
    "family": "10751",
    "fantasy": "14",
    "history": "36",
    "horror": "27",
    "music": "10402",
    "mystery": "9648",
    "romance": "10749",
    "science": "878",
    "tv": "10770",
    "thriller": "53",
    "war": "10752",
    "western": "37"
}

# ----------------------------
# Dizi Kategorileri (TV)
# TMDB'de resmi olarak tanımlı TV türleri bunlardır.
# ----------------------------
CATEGORY_NAMES_TV = {
    "action": "10759",
    "animation": "16",
    "comedy": "35",
    "crime": "80",
    "documentary": "99",
    "drama": "18",
    "family": "10751",
    "kids": "10762",
    "mystery": "9648",
    "news": "10763",
    "reality": "10764",
    "fantasy": "10765",
    "soap": "10766",
    "talk": "10767",
    "politics": "10768",
    "western": "37"
}

# ----------------------------
# Kitap Kategorileri (Books)
# ----------------------------
CATEGORY_NAMES_BOOKS = {
    "fiction": "fiction",
    "science": "science",
    "history": "history",
    "fantasy": "fantasy",
    "mystery": "mystery",
    "romance": "romance",
    "horror": "horror",
    "thriller": "thriller",
    "biography": "biography",
    "scifi": "science fiction",
    "poetry": "poetry",
    "philosophy": "philosophy",
    "religion": "religion",
    "health": "health",
    "travel": "travel",
    "humor": "humor",
    "art": "art",
    "music": "music",
    "cooking": "cooking",
    "business": "business",
    "politics": "politics",
    "education": "education",
    "technology": "technology",
    "law": "law",
    "psychology": "psychology",
    "sports": "sports",
    "comics": "comics",
    "children": "children",
    "young": "young adult",
    "environment": "environment",
    "mathematic": "mathematics",
    "astronomy": "astronomy",
    "economy": "economics",
    "parenting": "parenting",
    "hobbies": "crafts",
    "adventure": "adventure",
    "spiritual": "spirituality"
}
# ----------------------------
# Movie, TV, Books type tespiti için kullanılan kelimeler
# ----------------------------
konular = {#hangi konuda öneri istediğini anlamak için kullanılan kelimeler
    "movies": ["movies","movie", "cinema", "theater", "blockbuster", "trailer", "actor", "actress", "director", "oscar", "film","watch"],
    "series": ["serie","series", "season", "episode", "binge", "stream", "cliff", "spin", "renew", "final","tv"],
    "books": ["books","reading","read","book", "novel", "library", "bestseller", "hardcover", "paperback", "audiobook", "ebook", "publisher", "literature","reading"]
}
# ==================================
# keywords for categories
movie_category_keywords = {
    "action": [
        "action", "action-packed movies", "high energy films", "adrenaline rush",
        "explosive", "heroic", "intense", "adrenaline", "combat", "stunts"
    ],
    "adventure": [
        "adventure", "epic journeys", "exploration", "adventurous movies",
        "quest", "expedition", "discovery", "odyssey", "venture", "trek"
    ],
    "animation": [
        "animation", "animated movies", "cartoons", "family-friendly animation",
        "2D", "3D", "toon", "render", "sketch", "frame"
    ],
    "comedy": [
        "comedy", "funny movies", "humorous films", "light-hearted comedies", "funny", "humor", "laugh", "comedian", "joke",
        "satire", "witty", "quirky", "parody", "banter", "silly"
    ],
    "crime": [
        "crime", "criminal stories", "detective movies", "mystery crimes", "criminal investigations", "killing", "murder",
        "heist", "fraud", "scam", "gangster", "underworld", "conspiracy"
    ],
    "documentary": [
        "documentary", "real-life stories", "informative movies", "biographical films",
        "factual", "investigative", "journalism", "authentic", "reality", "exposé"
    ],
    "drama": [
        "drama", "serious stories", "intense plots", "emotional narratives",
        "tragedy", "conflict", "melodrama", "character", "heartfelt", "sentimental"
    ],
    "family": [
        "family", "family-friendly movies", "kids movies", "animated family shows",
        "joy", "together", "warmth", "bond", "loving", "comfort"
    ],
    "fantasy": [
        "fantasy", "magical stories", "mythical worlds", "epic fantasies",
        "myth", "legend", "enchantment", "sorcery", "realm", "fable"
    ],
    "history": [
        "history", "historical movies", "historical events", "war history",
        "past", "ancient", "era", "chronicle", "legacy", "tradition"
    ],
    "horror": [
        "horror", "scary movies", "frightening films", "ghost stories",
        "macabre", "eerie", "terrify", "spooky", "nightmare", "gruesome"
    ],
    "music": [
        "music", "musical movies", "concerts", "musical performances",
        "rhythm", "melody", "tune", "harmony", "beat", "sound"
    ],
    "mystery": [
        "mystery", "detective stories", "whodunit", "suspense",
        "enigma", "puzzle", "clue", "secret", "riddle", "cipher"
    ],
    "romance": [
        "romance", "love stories", "romantic comedies", "emotional romances",
        "passion", "affection", "desire", "heart", "cherish", "intimacy"
    ],
    "science": [
        "science fiction", "sci-fi", "space adventures", "futuristic movies",
        "cyber", "quantum", "tech", "galaxy", "robot", "alien"
    ],
    "tv": [
        "tv movies", "made-for-tv", "television movies",
        "broadcast", "series", "cable", "airing", "episode", "network"
    ],
    "thriller": [
        "thriller", "suspense", "psychological thrillers", "mystery thrillers",
        "tension", "rush", "panic", "intensity", "cliffhanger", "anxiety"
    ],
    "war": [
        "war", "military movies", "warfare stories", "war documentaries",
        "battle", "combat", "soldier", "conflict", "strategy", "frontline"
    ],
    "western": [
        "western", "cowboy movies", "wild west", "frontier stories",
        "sheriff", "ranch", "outlaw", "duel", "saddle", "desert"
    ]
}

tv_category_keywords = {
    "action": [
        "action-packed TV shows", "high-energy TV series", "adrenaline-filled shows",
        "thrill", "explosive", "dynamic", "combat", "intense", "power"
    ],
    "animation": [
        "animated shows", "cartoons", "animated series", "family-friendly animation",
        "toon", "cel", "vector", "sketch", "frame", "render"
    ],
    "comedy": [
        "funny TV shows", "comedic series", "humorous TV shows", "sitcoms", "funny", "humor", "laugh", "comedian", "joke",
        "satire", "witty", "quirky", "parody", "banter", "silly"
    ],
    "crime": [
        "crime shows", "detective TV shows", "mystery crimes", "criminal investigations", "killing", "murder",
        "heist", "gangster", "fraud", "scam", "underworld", "conspiracy"
    ],
    "documentary": [
        "real-life stories", "informative TV shows", "true events", "biographical documentaries",
        "factual", "investigative", "journalism", "authentic", "reality", "exposé"
    ],
    "drama": [
        "serious TV dramas", "emotional series", "intense TV storylines",
        "tragedy", "conflict", "melodrama", "depth", "emotion", "character", "heartfelt"
    ],
    "family": [
        "family-friendly shows", "kids series", "family dramas",
        "together", "bond", "unity", "warmth", "love", "home"
    ],
    "kids": [
        "kids shows", "children’s programming", "TV for young audiences",
        "play", "fun", "learning", "youth", "spark", "smile"
    ],
    "mystery": [
        "mystery series", "detective stories", "suspenseful shows", "horror", "scary movies", "frightening films", "ghost stories", "thriller", "suspense", "psychological thrillers", "mystery thrillers",
        "enigma", "puzzle", "clue", "secret", "riddle", "cipher"
    ],
    "news": [
        "news programs", "breaking news coverage", "current events",
        "report", "anchor", "update", "bulletin", "media", "coverage"
    ],
    "reality": [
        "reality shows", "reality TV competitions", "unscripted shows",
        "unscripted", "spontaneous", "contest", "challenge", "vivid", "authentic"
    ],
    "fantasy": [
        "fantasy series", "mythical TV shows", "magical worlds",
        "myth", "legend", "enchantment", "sorcery", "realm", "fable"
    ],
    "soap": [
        "soap operas", "daily TV dramas", "melodramatic series",
        "melodrama", "betrayal", "affair", "intrigue", "tension", "scandal", "suspense"
    ],
    "talk": [
        "talk shows", "interview programs", "discussion panels",
        "chat", "debate", "forum", "dialogue", "discussion", "insight"
    ],
    "politics": [
        "political dramas", "political debates", "government-related shows",
        "power", "government", "policy", "debate", "ideology", "election"
    ],
    "western": [
        "western TV shows", "cowboy series", "wild west adventures",
        "sheriff", "ranch", "duel", "saddle", "outlaw", "desert"
    ]
}

book_category_keywords = {
    "fiction": [
        "fiction books", "novels", "imaginative literature", "narrative fiction",
        "narrative", "tale", "story", "epic", "fable", "drama"
    ],
    "science": [
        "science books", "scientific literature", "natural sciences",
        "research", "experiment", "theory", "biology", "chemistry", "physics"
    ],
    "history": [
        "historical books", "history-based literature", "books about past events",
        "chronicle", "era", "past", "antiquity", "legacy", "record"
    ],
    "fantasy": [
        "fantasy novels", "magical stories", "mythical adventures", "fantasy worlds",
        "magic", "myth", "legend", "sorcery", "realm", "enchantment"
    ],
    "mystery": [
        "mystery novels", "detective stories", "whodunit books",
        "enigma", "puzzle", "clue", "secret", "riddle", "cipher"
    ],
    "romance": [
        "romantic", "love", "romances", "romance",
        "passion", "affection", "desire", "heart", "cherish", "intimacy"
    ],
    "horror": [
        "horror books", "scary novels", "ghost stories", "thrillers",
        "terror", "ghoul", "eerie", "spook", "dread", "macabre"
    ],
    "thriller": [
        "thriller novels", "suspense books", "psychological thrillers",
        "tension", "rush", "panic", "cliffhanger", "anxiety", "intensity"
    ],
    "biography": [
        "biographies", "life stories", "autobiographies",
        "memoir", "life", "story", "chronicle", "profile", "journey"
    ],
    "scifi": [
        "science fiction novels", "sci-fi books", "futuristic stories",
        "cyber", "alien", "robot", "future", "space", "tech"
    ],
    "poetry": [
        "poetry books", "poems", "literary poetry",
        "verse", "rhyme", "lyric", "sonnet", "haiku", "elegy"
    ],
    "philosophy": [
        "philosophy books", "philosophical works", "theoretical discussions",
        "ethics", "logic", "reason", "metaphysics", "existence", "wisdom"
    ],
    "religion": [
        "religious books", "spiritual literature", "religious texts",
        "faith", "spirit", "belief", "ritual", "worship", "doctrine"
    ],
    "health": [
        "health books", "wellness guides", "medical literature",
        "wellness", "fitness", "nutrition", "medicine", "vitality", "healing"
    ],
    "travel": [
        "travel guides", "travelogues", "books about destinations",
        "journey", "voyage", "expedition", "odyssey", "trek", "exploration"
    ],
    "humor": [
        "humorous books", "funny stories", "comedy literature",
        "wit", "satire", "banter", "quirk", "jest", "fun"
    ],
    "art": [
        "art books", "visual arts", "painting and sculpture",
        "painting", "sculpture", "sketch", "drawing", "design", "aesthetics"
    ],
    "music": [
        "music books", "biographies of musicians", "musical history",
        "melody", "rhythm", "harmony", "tune", "beat", "sound"
    ],
    "cooking": [
        "cookbooks", "cooking guides", "recipes",
        "recipe", "baking", "grill", "simmer", "flavor", "spice"
    ],
    "business": [
        "business guides", "management books", "corporate success stories",
        "entrepreneur", "startup", "market", "finance", "strategy", "investment"
    ],
    "politics": [
        "political literature", "political theory", "government books",
        "policy", "governance", "ideology", "diplomacy", "election", "reform"
    ],
    "education": [
        "educational books", "teaching guides", "academic literature",
        "learning", "academic", "scholar", "study", "knowledge", "curriculum"
    ],
    "technology": [
        "technology books", "tech innovations", "scientific advancements",
        "innovation", "gadget", "cyber", "digital", "tech", "future"
    ],
    "law": [
        "legal books", "law textbooks", "legal history",
        "justice", "court", "legal", "verdict", "trial", "statute"
    ],
    "psychology": [
        "psychology books", "human behavior", "mental health literature",
        "mind", "cognition", "behavior", "emotion", "perception", "therapy"
    ],
    "sports": [
        "sports books", "athletics literature", "sports biographies",
        "athlete", "game", "match", "tournament", "league", "score"
    ],
    "comics": [
        "comic books", "graphic novels", "superhero stories",
        "graphic", "illustration", "hero", "panel", "sketch", "toon"
    ],
    "children": [
        "children’s books", "kids literature", "young readers",
        "storybook", "imagination", "fairy", "tale", "learning", "fun"
    ],
    "young": [
        "young adult novels", "YA fiction", "teen stories",
        "youth", "growth", "identity", "change", "struggle", "hope"
    ],
    "environment": [
        "environmental books", "nature studies", "ecological literature",
        "nature", "eco", "sustainability", "green", "wild", "conservation"
    ],
    "mathematic": [
        "mathematics books", "numbers and logic", "math theory",
        "algebra", "calculus", "geometry", "theorem", "logic", "number"
    ],
    "astronomy": [
        "astronomy books", "space exploration", "cosmology", "space",
        "cosmos", "stars", "galaxy", "planet", "orbit", "nebula"
    ],
    "economy": [
        "economics books", "financial guides", "economic theory",
        "finance", "market", "trade", "budget", "capital", "growth"
    ],
    "parenting": [
        "parenting guides", "family advice", "raising children",
        "child", "care", "love", "nurture", "support", "guide"
    ],
    "hobbies": [
        "hobby books", "DIY crafts", "creative projects",
        "craft", "diy", "leisure", "pastime", "recreation", "interest"
    ],
    "adventure": [
        "adventure novels", "epic journeys", "explorations",
        "quest", "journey", "expedition", "odyssey", "explore", "venture"
    ],
    "spiritual": [
        "spirituality books", "self-discovery", "spiritual growth",
        "soul", "zen", "meditation", "awakening", "inner", "transcendence"
    ]
}

# ==================================
#  cc
# ==================================
rejections = [
    "no",
    "nope",
    "nah",
    "never",
    "not now",
    "not ever",
    "no chance",
    "no way",
    "no thanks",
    "hell no",
    "hard pass",
    "no deal",
    "can't",
    "count me out",
    "certainly not",
    "absolutely not",
    "i refuse",
    "i'm out",
    "not happening",
    "sorry, no",
    "nah, sorry",
    "i'm not interested",
    "i'm good",
    "i'm okay",
    "i'm fine",
    "i'm alright"
]
acceptances = [
    "yes",
    "yes i do",
    "yep",
    "yeah",
    "yup",
    "yea",
    "let's do it",
    "sure",
    "of course",
    "definitely",
    "absolutely",
    "for sure",
    "why not",
    "okay",
    "sounds good",
    "all right",
    "affirmative",
    "you bet",
    "sure thing",
    "gladly",
    "with pleasure",
    "i'm in",
    "fine by me",
    "absolutely yes"
]

greetings_sentences = [
    "hello",
    "hi",
    "welcome",
    "hey"
]
stop_sentences = [
    "stop",
    "exit",
    "quit",
    "bye",
    "goodbye",
    "see you later",
    "end",
    "finish",
    "close",
    "shut down",
    "see you"
]
curse_sentences = [
    "fuck",
    "fuck you",
    "shit",
    "damn",
    "bastard",
    "asshole",
    "dick",
    "son of a bitch",
    "crap",
    "piss off",
    "bloody hell",
    "wanker",
    "prick",
    "screw you",
    "bullshit",
    "dumbass",
    "jackass",
    "motherfucker",
    "bitch",
    "cocksucker"
]
reset_sentences = [
    "reset",
    "restart",
    "begin again",
    "start over"
]
previous_sentences = [
    "previous question",
    "go back",
    "last question",
    "back to the previous",
    "return to the previous",
    "previous step",
    "back one step",
    "show me the last one",
    "previous option",
    "go to the previous"
]

sexual_content = [
    "porn",
    "sex",
    "nude",
    "erotic",
    "adult",
    "xxx",
    "softcore",
    "fetish",
    "porn movie",
    "porn movies",
    "adult movie",
    "adult movies",
    "sex movie",
    "sex movies",
    "porn book",
    "porn books",
    "sex book",
    "sex books",
    "nude book",
    "nude books",
    "erotic book",
    "erotic books",
    "adult book",
    "adult books",
    "xxx book",
    "xxx books",
    "softcore book",
    "softcore books",
    "fetish book",
    "fetish books",
    "erotic series",
    "porn series",
    "sex series",
    "adult series",
    "nude series",
    "xxx series",
    "softcore series",
    "fetish series"
]


# ==================================
#  CÜMLELER 
# ==================================
start_responses = [
    "I can suggest movies, series and books what do you want? ",
    "Do want me to suggest you a movie, series or a book? ",
    "I can suggest you a movie, series or a book. What do you want? ",
    "I can recommend you a movie, series or a book. What do you want? ",
    "Which one do you want me to suggest you? A movie, a series or a book? "
]
start_responses_short = [
    "Movies, series or books?",
    "Movie, series or book?",
    "Want a movie, series or book?",
    "Need a movie, series or book?",
    "Movie, series, or book suggestion?",
    "Looking for a movie, series, or book?",
    "Need a recommendation for a movie, series, or book?",
    "Interested in a movie, series, or book suggestion?",
    "Want a suggestion for a movie, series, or book?",
    "Do you need a movie, series, or book suggestion?",
    "Are you looking for a movie, series, or book?",
]
clarification_responses = [
    "I'm not sure I understand.",
    "Could you specify what you mean?",
    "I couldn't understand what you mean",
    "Could you provide a clearer explanation?"
]
resume_responses = [
    "Do you want any other recommendations?",
    "Would you like another suggestion?",
    "Do you need another recommendation?",
    "Can i suggest something else?",
    "Do you want another suggestion?",
    "Would you like another recommendation?",
    "Any other suggestions?",
    "Do you need another recommendation?"
]
greeting_responses = [
    "Hello! ",
    "Hi! ",
    "Hey! ",
    "Greetings! ",
    "Welcome! "
]
stop_responses = [
    "Goodbye! ",
    "See you later! ",
    "Bye! ",
    "Have a nice day! ",
    "Goodbye! "
]
curse_responses = [
    "That's not very nice.",
    "Please watch your language.",
    "Let's keep this conversation respectful.",
    "I don't appreciate that kind of language.",
    "Can we keep this polite, please?",
    "Is there something bothering you?",
    "Let's try to have a productive conversation.",
    "I understand you're upset, but let's be civil.",
    "Can we talk without the insults?",
    "I'm here to help, not to argue."
]
reset_responses = [
    "Alright, let's start over.",
    "No problem, let's begin again.",
    "Sure, let's reset and start over.",
    "Okay, let's start from the beginning.",
    "Let's reset and try again."
]
invalid_responses = [
    "I'm sorry, I didn't understand that.",
    "I'm not sure what you mean.",
    "Can you please rephrase that?",
    "I'm having trouble understanding you.",
    "I'm not sure what you're asking.",
    "I don't know what you mean by that.",
    "I'm having a hard time understanding you.",
    "Can you please clarify what you mean?",
    "I'm not sure what you're trying to say."
]
previous_responses = [
    "I'm sorry, I can't do that.",
    "I'm afraid I can't do that.",
    "I'm sorry, I can't go back.",
    "I'm afraid I can't go back."]

rejection_responses = [
    "No problem.",
    "Alright, just let me know if you need anything.",
    "No worries, I'm here if you need.",
    "Okay, feel free to ask if you need anything.",
    "Sure, I'll be here if you need me."
]
acceptance_responses = [
    "Great! Let's get started.",
    "Awesome! Let's begin.",
    "Fantastic! Let's start.",
    "Wonderful! Let's get going.",
    "Excellent! Let's begin."
]
sexual_content_responses = [
    "I can't suggest sexual content.",
    "I'm sorry, I can't help with that.",
    "I'm afraid I can't provide that kind of content.",
    "I'm sorry, I can't suggest that.",
    "I can't recommend that kind of content.",
    "I'm sorry, I can't provide suggestions for that."
]
describe_responses = [
    "Do you want me to describe it?",
    "Would you like a description?",
    "Do you need a description?",
    "Do you want more information about it?",
    "Would you like me to provide more details?",
    "Do you need more information?",
    "I can give you a brief description if you'd like."
]
ask_movie_type = [
    "What kind of movies you would like to watch?",
    "What kind of movies do you enjoy?",
    "What genre of movies are you interested in?",
    "What type of films do you like to watch?"
]
ask_serie_type = [
    "What kind of series you would like to watch?",
    "What kind of series do you enjoy?",
    "What genre of series are you interested in?",
    "What type of series do you like to watch?"
]
ask_book_type = [
    "What kind of books you would like to read?",
    "What kind of books do you enjoy?",
    "What genre of books are you interested in?",
    "What type of books do you like to read?"
]    
    