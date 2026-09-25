# RecoVision

RecoVision is a Django 4.2 application that combines a curated media catalogue with an
interactive conversational recommendation engine. Users browse and bookmark Movies, TV
Series and Books stored locally, and separately hold a free-text conversation with a
multi-stage recommender at `/reco` that resolves intent and genre from natural language
before querying TMDB and Google Books for a live suggestion.

The two halves are deliberately independent. The catalogue pages read from PostgreSQL;
the conversational engine never touches the local database and always returns a live
result from an external API.

## Table of Contents

- [Architecture](#architecture)
- [Recommendation Pipeline](#recommendation-pipeline)
- [NLP Stack](#nlp-stack)
- [Data Model](#data-model)
- [URL Map](#url-map)
- [Experiments and Model Training](#experiments-and-model-training)
- [Setup and Local Run](#setup-and-local-run)
- [Deployment](#deployment)
- [Production and Performance Roadmap](#production-and-performance-roadmap)

## Architecture

```
Browser
  |
  |-- catalogue pages ------> Django views -----> PostgreSQL
  |                                         \--> S3 (media)
  |
  '-- POST /reco (JSON) ----> views.reco ---> rv.recommend_RV()
                                                   |
                                                   |-- transformers / sentence-transformers
                                                   |-- scikit-learn (saved_model3.pkl)
                                                   '-- TMDB API / Google Books API
```

Repository layout:

```
.
├── manage.py
├── requirements.txt
├── .env.example
├── Dockerfile
├── movieWeb/              Django project package (settings, urls, wsgi, asgi)
├── movie_uygulama/        Application package
│   ├── models.py          Catalogue and bookmark models
│   ├── views.py           Function-based views, including the /reco endpoint
│   ├── rv.py              Conversational recommendation engine
│   ├── config.py          API keys, genre maps, keyword banks, response banks
│   ├── saved_model3.pkl   Trained RandomForestClassifier
│   ├── vectorizer3.pkl    Fitted CountVectorizer
│   ├── migrations/
│   └── static/            css, js, images
├── templates/             20 Django templates
└── deneme_dosyaları/      Offline ML laboratory and data-population scripts
```

## Recommendation Pipeline

`rv.recommend_RV()` implements a seven-stage state machine. State is held in the module
level `state` dict (`step`, `selection`, `suggestion`). The initial step is `6`, so a
fresh conversation opens in open-domain chat and escalates into the structured flow once
a recommendation intent is detected.

| Step | Role | Primary calls |
| --- | --- | --- |
| 0 | Idle entry point; emits the opening prompt | `send_to_passive`, `start` |
| 1 | Medium selection: movies, series or books | `take_main_type` |
| 2 | Genre extraction and external fetch | `make_recommendation`, `is_category` |
| 3 | Offer structured metadata for the suggestion | `accept_reject`, `inform_user` |
| 4 | Offer the long-form description | `accept_reject`, `inform_user_more` |
| 5 | Offer a further recommendation | `send_to_step_N` |
| 6 | Open-domain conversation fallback | `chat_with_bot` |

Every step first runs two interrupt handlers. `unusual_response1` catches adult-content
requests, profanity and "go back" without changing the step. `unusual_response2` catches
stop, reset and greeting phrases and returns the machine to step 0.

Genre resolution is a three-tier cascade, each tier attempted only if the previous one
returns nothing:

1. Fuzzy match of tokenised input against literal genre names, using
   `difflib.SequenceMatcher` with a ratio above `0.80`.
2. Fuzzy match against the per-genre keyword banks in `config.py`, which hold around ten
   keywords per genre across 19 movie genres, 16 TV genres and 37 book genres.
3. Semantic match using MiniLM sentence embeddings and cosine similarity, accepted above
   `0.5`.

One, two or three resolved genres dispatch to the corresponding
`recommend_*_one_category` / `_two_categories` / `_three_categories` function.

Qualitative modifiers are detected separately by `detect_content_conditions`, which scans
for "new", "good" and "bad" vocabulary and returns a three-bit signature. That rewrites
the outgoing query: `vote_average.gte=7` for high quality, `vote_average.lte=5` for low,
or a three-year release window for recency. External fetches retry up to 16 times against
a randomly selected result page to vary suggestions across calls.

## NLP Stack

All models are loaded at module import, which means they initialise during Django
startup rather than on first request.

| Component | Model | Role |
| --- | --- | --- |
| Intent and yes/no detection | `typeform/distilbert-base-uncased-mnli` | Zero-shot classification. Binary accept/reject in `accept_reject`; four-way intent labelling in `direct_suggestion`, accepted above `0.85` |
| Semantic genre matching | `all-MiniLM-L6-v2` | Sentence embeddings, cosine similarity against genre keyword banks, accepted above `0.5` |
| Genre-request classifier | `saved_model3.pkl` + `vectorizer3.pkl` | Custom-trained `RandomForestClassifier` over `CountVectorizer` features. Detects "list me some genres" requests in `is_category`, accepted above `0.8` |
| Open-domain fallback | `microsoft/DialoGPT-medium` | Free conversation in `chat_with_bot`, sampled at `temperature=0.3` with a short rolling history and a retry pass for degenerate output |
| Preprocessing | NLTK `punkt`, `stopwords`, `wordnet` | Tokenisation, stopword removal, lemmatisation |
| Content sourcing | TMDB API, Google Books API | Live movie, TV and book results |

The two pickled scikit-learn artefacts were produced by scikit-learn 1.6.1. That version
is pinned in `requirements.txt`, since unpickling under a different minor version is not
guaranteed to succeed.

## Data Model

- `Movie`, `Series`, `Books` are the catalogue entities, each carrying a slug, cover
  image, year and description. `Movie` and `Series` additionally carry an IMDb rating.
- `Director`, `Actors`, `Writers` are the people entities, each with its own detail page
  listing associated titles.
- `Category` and `BookCategory` classify titles and books respectively.
- `Save` is a single unified bookmark table holding a user foreign key plus three
  nullable foreign keys to `Movie`, `Books` and `Series`, with a uniqueness constraint
  per user and per target.
- `Profile` extends `auth.User` with an avatar.

The profile view aggregates a user's bookmarks into a top-three genre breakdown per
medium, using `values(...).annotate(Count(...))`, and serialises the result to JSON for
the donut charts rendered by `static/js/donut-charts.js`.

## URL Map

| Path | View | Purpose |
| --- | --- | --- |
| `/home` | `index` | Landing page |
| `/films`, `/series`, `/books` | `films`, `series`, `books` | Catalogue listings |
| `/film/<slug>`, `/serie/<slug>`, `/kitap/<slug>` | `film`, `serie`, `kitap` | Title detail |
| `/actors/<slug>`, `/director/<slug>`, `/yazar/<slug>` | `actor`, `director`, `yazar` | People detail |
| `/kaydet/<id>`, `/kaydet_serie/<id>`, `/kaydet_kitap/<id>` | `kaydet`, `kaydet_serie`, `kaydet_kitap` | Bookmark toggle |
| `/kayitlar`, `/kayitlar_serie`, `/kayitlar_kitap` | `kayitlar`, `kayitlar_serie`, `kayitlar_kitap` | Saved lists |
| `/reco` | `reco` | Conversational recommender; GET renders the UI, POST accepts JSON |
| `/login`, `/register`, `/logout`, `/profil` | auth views | Accounts |
| `/change_password/`, `/reset_saves/<id>` | `change_password`, `reset_user_saves` | Account management |
| `/admin/` | Django admin | All models registered |

## Experiments and Model Training

`deneme_dosyaları` ("trial files") is the offline machine learning laboratory. It is not
imported by the application at runtime and is excluded from the Docker build context via
`.dockerignore`, but it is the provenance of the shipped model artefacts.

| File | Role |
| --- | --- |
| `csv1.py` | Generates the training corpus. Roughly 200 hand-written labelled sentences, where `1` marks a request for genre suggestions and `0` marks unrelated prose. Writes `cleaned_data3.csv`. |
| `deneme11.py` | Trains the classifier. `CountVectorizer` plus `RandomForestClassifier` with `class_weight={0: 1, 1: 6}` to suppress false positives, then serialises both artefacts with joblib. This is what produces `saved_model3.pkl` and `vectorizer3.pkl`. |
| `deneme22.py` | Loads the serialised artefacts and smoke-tests predictions on sample sentences. |
| `tests.py` | Data population script, not a Django test suite. Seeds the `Director` table from a hardcoded list of television directors with biographies and slugs via `update_or_create`. Wrapped in `exec` so it can be pasted into `manage.py shell`. |
| `notlar.txt` | Developer notes in Turkish covering the step-machine design, function responsibilities, required NLTK downloads, and an earlier draft of `chat_with_bot`. |
| `deneme.html` | Standalone 3D CSS carousel prototype. |

To retrain the genre-request classifier:

```bash
cd deneme_dosyaları
python csv1.py       # regenerate cleaned_data3.csv
python deneme11.py   # train and write the .pkl artefacts
python deneme22.py   # smoke-test the artefacts
```

Note that `deneme11.py` evaluates at a decision threshold of `0.85` while the application
applies `0.8` in `is_category`.

## Setup and Local Run

Requires Python 3.9 or newer and a reachable PostgreSQL instance.

Clone and enter the repository:

```bash
git clone https://github.com/sami373761/RecoVision2.git
cd RecoVision2
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Download the NLTK corpora required by `rv.py`:

```bash
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('wordnet')"
```

Configure environment variables. Copy the template and fill in your own values:

```bash
cp .env.example .env
```

`.env.example` documents every recognised variable:

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Django secret key |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | PostgreSQL connection |
| `TMDB_API_KEY` | TMDB movie and TV lookups |
| `GOOGLE_BOOKS_API_KEY` | Google Books lookups |
| `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | S3 media storage |

Each setting is read with `os.getenv("NAME", <existing literal>)`, so any variable left
unset falls back to the value already present in `settings.py` or `config.py`. `.env` is
gitignored and must never be committed.

Apply migrations and create an administrator:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

The site is served at `http://127.0.0.1:8000/home`, the recommender at
`http://127.0.0.1:8000/reco`, and the admin at `http://127.0.0.1:8000/admin/`.

First startup is slow. The transformer weights are downloaded from Hugging Face on first
import, DialoGPT-medium alone being roughly 350 MB, and all models are held in memory
thereafter. Budget approximately 1.5 GB of RAM for the process.

## Deployment

The `Dockerfile` builds from `python:3.9.7-slim`, installs the native toolchain required
by scikit-learn and Pillow, installs a CPU-only build of torch 2.2.2 ahead of the
remaining requirements, runs `collectstatic`, pre-downloads the NLTK corpora into the
image, and serves through Gunicorn:

```bash
docker build -t recovision .
docker run --env-file .env -p 8000:8000 recovision
```

Gunicorn is started with `--timeout 300` to accommodate model loading and the latency of
the external API calls. Media files are served from S3 through `django-storages`, and
`.dockerignore` excludes `deneme_dosyaları/` and `.git/` from the build context.

## Production and Performance Roadmap

The items below are known limitations rather than speculative improvements, listed in
rough order of severity.

**Session-isolated state management.** The `state` dict, the chat history, and the
suggestion detail globals (`title`, `description`, `cast`, `year`, and others) are all
declared at module level in `rv.py`. Under Gunicorn every worker shares one copy, so
concurrent users overwrite each other's conversation position and suggestion payload.
`views.reco` already creates a `reco_state` key in the Django session, but it is read and
written back untouched and never passed into `recommend_RV`, so the scaffolding is
currently inert. Threading this state through the session or a cache store, keyed per
user, is the prerequisite for supporting more than one concurrent conversation.

**Embedding cache.** `make_recommendation` calls `take_movie_type`, `take_serie_type` or
`take_book_type` up to four times per request, and each call can re-encode every keyword
in every genre bank with MiniLM. The keyword embeddings are static and should be computed
once at startup, while the per-request user embedding should be computed once and reused.
This is the single largest available latency reduction in the chat path.

**Asynchronous external fetching.** The TMDB and Google Books calls are synchronous and
retry up to 16 times, and the multi-genre paths issue several requests in sequence. Moving
these to async or concurrent fetches, with a bounded retry budget and a short-lived
response cache, would materially cut worst-case response time.

**Secret rotation and production readiness.** Sensitive values are now read from the
environment, but the original literals remain in git history from the initial commit. The
database password and both API keys should be rotated, after which the fallbacks become
inert defaults. Beyond that, `DEBUG` should be driven by the environment and set to
`False` in production, `ALLOWED_HOSTS` must be populated, and the `@csrf_exempt` decorator
on `reco` can be removed because the client in `reco.html` already sends a valid
`X-CSRFToken` header.

**Known defects.** `reset_user_saves` returns `None` on a GET request, which raises
`ValueError: view didn't return an HttpResponse`. The `kategori` route in
`movie_uygulama/urls.py` reuses the name `director`, which is already bound to the
director detail route; reverse resolution currently disambiguates by argument count, but
the collision is fragile.
