exec("""
from movie_uygulama.models import Director

directors_data = [
  {
    "fields": {
      "name": "Vince Gilligan",
      "birthdate": "1967-02-10",
      "description": "Vince Gilligan is an American showrunner, writer, and director best known for creating the groundbreaking television series 'Breaking Bad' and co-creating its spin-off, 'Better Call Saul'. His work is praised for its meticulous plotting, dark humor, and deep exploration of moral ambiguity, often pushing characters to their psychological and ethical limits. Gilligan’s distinct storytelling approach has had a lasting impact on the modern golden age of television drama.",
      "image": "",
      "slug": "vince-gilligan"
    }
  },
  {
    "fields": {
      "name": "Michelle MacLaren",
      "birthdate": "1965-01-01",
      "description": "Michelle MacLaren is a Canadian television director and producer recognized for her work on episodes of 'Breaking Bad', 'Game of Thrones', and 'The Walking Dead'. She is noted for her dynamic action sequences, strong character-driven storytelling, and ability to handle large ensemble casts effectively. MacLaren’s influential contributions have helped shape the visual language of premium television, earning her numerous industry accolades.",
      "image": "",
      "slug": "michelle-maclaren"
    }
  },
  {
    "fields": {
      "name": "David Chase",
      "birthdate": "1945-08-22",
      "description": "David Chase is an American writer, director, and producer celebrated for creating the critically acclaimed HBO series 'The Sopranos'. Known for blending raw crime drama with existential themes and dark humor, Chase played a pivotal role in ushering in a new era of television storytelling. His layered characters and morally complex narratives continue to influence contemporary showrunners and screenwriters worldwide.",
      "image": "",
      "slug": "david-chase"
    }
  },
  {
    "fields": {
      "name": "Tim Van Patten",
      "birthdate": "1959-06-10",
      "description": "Tim Van Patten is an American television director, producer, and screenwriter who has directed numerous episodes of iconic series such as 'The Sopranos', 'Boardwalk Empire', and 'Game of Thrones'. With a keen eye for visual storytelling and a talent for building suspense, Van Patten has garnered critical praise for his ability to handle complex plots and large casts. His skillful direction has been instrumental in shaping the stylistic and dramatic identity of premium cable dramas.",
      "image": "",
      "slug": "tim-van-patten"
    }
  },
  {
    "fields": {
      "name": "David Nutter",
      "birthdate": "1960-02-14",
      "description": "David Nutter is an American television director highly respected for his work on multiple major series, including 'Game of Thrones', 'The X-Files', and 'Band of Brothers'. Often referred to as the 'pilot whisperer', he has directed numerous successful pilot episodes that effectively set the tone for entire series. His contributions to 'Game of Thrones' include some of the show’s most pivotal and emotionally charged episodes.",
      "image": "",
      "slug": "david-nutter"
    }
  },
  {
    "fields": {
      "name": "Miguel Sapochnik",
      "birthdate": "1974-01-01",
      "description": "Miguel Sapochnik is a British film and television director who rose to international prominence by directing major episodes of 'Game of Thrones', including the Emmy Award-winning 'Battle of the Bastards'. He is known for his immersive visual style, meticulous choreography of large-scale battle scenes, and ability to convey intense emotional depth. Sapochnik’s work continues to influence modern fantasy and action storytelling on television.",
      "image": "",
      "slug": "miguel-sapochnik"
    }
  },
  {
    "fields": {
      "name": "Clark Johnson",
      "birthdate": "1954-09-10",
      "description": "Clark Johnson is an American-Canadian actor and director famous for his involvement in gritty, realistic television dramas. He directed the pilot of 'The Wire', helping establish the show’s documentary-like tone and immersive depiction of urban life. Johnson’s directing style focuses on naturalistic performances and tight pacing, adding to the authenticity that defines 'The Wire'.",
      "image": "",
      "slug": "clark-johnson"
    }
  },
  {
    "fields": {
      "name": "Agnieszka Holland",
      "birthdate": "1948-11-28",
      "description": "Agnieszka Holland is a Polish film and TV director known for her nuanced storytelling and willingness to tackle politically and morally complex subjects. In 'The Wire', she helmed several episodes that delved deeply into character development and societal critique. Holland’s international background and extensive filmography lend a unique perspective to her television work, making her episodes stand out for their depth and social realism.",
      "image": "",
      "slug": "agnieszka-holland"
    }
  },
  {
    "fields": {
      "name": "Paul McGuigan",
      "birthdate": "1963-09-19",
      "description": "Paul McGuigan is a Scottish filmmaker whose diverse portfolio includes directing episodes of 'Sherlock' as well as feature films like 'Lucky Number Slevin'. In 'Sherlock', he established a highly stylized visual approach that combined rapid editing, on-screen text, and kinetic camera movements to reflect the protagonist’s swift deductive reasoning. McGuigan’s cinematic flair greatly contributed to the show’s modern reinterpretation of the classic detective stories.",
      "image": "",
      "slug": "paul-mcguigan"
    }
  },
  {
    "fields": {
      "name": "Toby Haynes",
      "birthdate": "1976-01-01",
      "description": "Toby Haynes is a British television director recognized for his work on critically acclaimed shows like 'Sherlock', 'Doctor Who', and 'Black Mirror'. In 'Sherlock', he focused on character-driven suspense and maintained a refined balance between humor and drama. Haynes’s ability to convey emotional intensity while also emphasizing the intellectual aspects of the narrative made his episodes memorable contributions to the series.",
      "image": "",
      "slug": "toby-haynes"
    }
  },
  {
    "fields": {
      "name": "Matt Duffer",
      "birthdate": "1984-02-15",
      "description": "Matt Duffer, alongside his twin brother Ross, co-created the Netflix sensation 'Stranger Things'. Their shared vision combines 1980s pop culture nostalgia with science fiction and horror elements, capturing the imagination of audiences worldwide. Matt’s work on the series emphasizes strong character development, atmospheric tension, and a heartfelt homage to the era’s beloved films and literature.",
      "image": "",
      "slug": "matt-duffer"
    }
  },
  {
    "fields": {
      "name": "Ross Duffer",
      "birthdate": "1984-02-15",
      "description": "Ross Duffer is the other half of the Duffer Brothers duo, whose collaboration brought 'Stranger Things' to life. Working closely with his brother Matt, Ross has been instrumental in crafting the show’s eerie yet endearing small-town vibe, blending supernatural elements with coming-of-age drama. His storytelling approach highlights youthful camaraderie, mystery, and suspense, drawing audiences into a richly woven narrative universe.",
      "image": "",
      "slug": "ross-duffer"
    }
  },
  {
    "fields": {
      "name": "James Foley",
      "birthdate": "1953-12-28",
      "description": "James Foley is an American filmmaker who directed multiple episodes of 'House of Cards', bringing his cinematic experience from films like 'Glengarry Glen Ross' to the small screen. He navigates intense character interactions and nuanced power struggles, matching the show’s high-stakes political environment. Foley’s ability to capture subtle shifts in tone and emotion helps maintain the suspenseful momentum of the narrative.",
      "image": "",
      "slug": "james-foley"
    }
  },
  {
    "fields": {
      "name": "Johan Renck",
      "birthdate": "1966-12-05",
      "description": "Johan Renck is a Swedish director and former musician who achieved critical acclaim for his work on the HBO miniseries 'Chernobyl'. His directing style emphasizes stark realism and emotional weight, effectively portraying the human and environmental cost of the 1986 nuclear disaster. Renck’s background in music videos gives his projects a distinct visual flair, balancing grim authenticity with compelling cinematic composition.",
      "image": "",
      "slug": "johan-renck"
    }
  },
  {
    "fields": {
      "name": "Owen Harris",
      "birthdate": "1975-01-01",
      "description": "Owen Harris is a British television and film director noted for his poignant storytelling and striking visual style, particularly on episodes of 'Black Mirror' such as the acclaimed 'San Junipero'. He focuses on creating emotionally resonant stories within speculative, near-future scenarios. Harris’s ability to integrate vibrant cinematography with psychological depth has made his episodes standout contributions to the anthology series.",
      "image": "",
      "slug": "owen-harris"
    }
  },
  {
    "fields": {
      "name": "David Slade",
      "birthdate": "1969-09-26",
      "description": "David Slade is an English film and television director who has brought his distinct, often dark visual sensibility to projects like 'Hard Candy', 'Hannibal', and several episodes of 'Black Mirror'. Known for his edgy and intense approach to storytelling, Slade expertly balances tension, horror, and human drama. His work on 'Black Mirror' episodes, such as 'Metalhead', demonstrates his talent for creating bleak yet gripping futuristic narratives.",
      "image": "",
      "slug": "david-slade"
    }
  }
]

def load_directors(directors_data):
    for data in directors_data:
        fields = data["fields"]
        
        director_obj, created = Director.objects.update_or_create(
            name=fields["name"],
            defaults={
                "birthdate": fields["birthdate"],
                "description": fields["description"],
                "image": fields["image"],
                "slug": fields["slug"]
            }
        )

        action = "Created" if created else "Updated"
        print(f"{action}: {director_obj.name}")

load_directors(directors_data)

""")