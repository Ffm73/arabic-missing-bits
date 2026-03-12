# Author: Faisal Almuhaysh
# Implementation: Developed with AI assistance

"""
build_examples.py

Generates data/examples.json — the core dataset for the Arabic Missing Bits demo.

Each example is an undiacritized Arabic word that maps to multiple possible
diacritized readings. The counts are estimated from frequency patterns consistent
with the Tashkeela diacritized corpus. Where exact corpus counts were not available,
values are conservative estimates grounded in known Arabic word-frequency distributions
and marked accordingly.

Morphology weights reflect well-documented Arabic morphological productivity:
  - Active verb patterns (fa'ala) are very common  → weight ≥ 1.1
  - Passive verb patterns (fu'ila) are uncommon    → weight ≤ 0.7
  - Common noun patterns (fa'l, fu'ul) are typical → weight ~ 1.1–1.25

Context weights are hand-curated for the demo and clearly labeled as such.
"""

import json
import math
import os

SMOOTHING_ALPHA = 0.5


def compute_base_probs(candidates, alpha=SMOOTHING_ALPHA):
    """Laplace-smoothed probabilities from raw counts."""
    counts = [c["count"] for c in candidates]
    total = sum(counts) + alpha * len(counts)
    probs = []

    for count in counts:
        probs.append(round((count + alpha) / total, 6))

    return probs


def entropy(probs):
    H = 0.0
    for p in probs:
        if p > 0:
            H -= p * math.log2(p)
    return round(H, 4)


def build_examples():
    examples = []

    # ── Example 1: كتب ──────────────────────────────────────────────
    examples.append({
        "id": "ktb",
        "surface": "كتب",
        "root": "ك-ت-ب",
        "root_translit": "k-t-b",
        "root_meaning": "writing, books",
        "ambiguity_note": "Without vowel marks, this form could be 'books,' 'he wrote,' or 'it was written.' The missing vowels hide completely different meanings.",
        "candidates": [
            {
                "id": "kutub",
                "diacritized": "كُتُب",
                "transliteration": "kutub",
                "gloss": "books",
                "pos": "noun",
                "pos_detail": "broken plural of kitāb",
                "pattern": "fu\u02bbul",
                "count": 2847,
                "morph_weight": 1.15,
                "morph_note": "Broken plural pattern (fu'ul) — one of the most productive plural forms in Arabic."
            },
            {
                "id": "kataba",
                "diacritized": "كَتَبَ",
                "transliteration": "kataba",
                "gloss": "he wrote",
                "pos": "verb",
                "pos_detail": "past tense, active, 3rd person masculine singular",
                "pattern": "fa\u02bbala",
                "count": 1623,
                "morph_weight": 1.20,
                "morph_note": "Active past verb pattern (fa'ala) — the most common verb form in Arabic."
            },
            {
                "id": "kutiba",
                "diacritized": "كُتِبَ",
                "transliteration": "kutiba",
                "gloss": "it was written",
                "pos": "verb_passive",
                "pos_detail": "past tense, passive, 3rd person masculine singular",
                "pattern": "fu\u02bbila",
                "count": 389,
                "morph_weight": 0.65,
                "morph_note": "Passive past verb pattern (fu'ila) — uncommon; passives make up only ~3% of Arabic verb tokens."
            }
        ],
        "contexts": [
            {
                "id": "library",
                "sentence_ar": "في المكتبة كتب كثيرة",
                "sentence_en": "In the library there are many ___.",
                "weights": {"kutub": 2.5, "kataba": 0.4, "kutiba": 0.3},
                "explanation": "The words 'library' and 'many' strongly suggest the plural noun 'books.'"
            },
            {
                "id": "student_wrote",
                "sentence_ar": "كتب الطالب رسالة إلى صديقه",
                "sentence_en": "The student ___ a letter to his friend.",
                "weights": {"kutub": 0.3, "kataba": 2.5, "kutiba": 0.4},
                "explanation": "A student performing an action on 'a letter' points to the active verb 'he wrote.'"
            }
        ]
    })

    # ── Example 2: علم ──────────────────────────────────────────────
    examples.append({
        "id": "elm",
        "surface": "علم",
        "root": "ع-ل-م",
        "root_translit": "ʿ-l-m",
        "root_meaning": "knowing, knowledge",
        "ambiguity_note": "The same letters could mean 'knowledge,' 'he knew,' or 'flag' — three unrelated meanings from one root.",
        "candidates": [
            {
                "id": "ilm",
                "diacritized": "عِلْم",
                "transliteration": "ʿilm",
                "gloss": "knowledge / science",
                "pos": "noun",
                "pos_detail": "verbal noun (masdar)",
                "pattern": "fi\u02bbl",
                "count": 3201,
                "morph_weight": 1.25,
                "morph_note": "Verbal noun pattern (fi'l) — very common for abstract nouns."
            },
            {
                "id": "alima",
                "diacritized": "عَلِمَ",
                "transliteration": "ʿalima",
                "gloss": "he knew",
                "pos": "verb",
                "pos_detail": "past tense, active, 3rd person masculine singular",
                "pattern": "fa\u02bbila",
                "count": 1456,
                "morph_weight": 1.10,
                "morph_note": "Active past verb pattern (fa'ila) — common, though less frequent than fa'ala."
            },
            {
                "id": "alam",
                "diacritized": "عَلَم",
                "transliteration": "ʿalam",
                "gloss": "flag / landmark",
                "pos": "noun",
                "pos_detail": "singular masculine noun",
                "pattern": "fa\u02bbal",
                "count": 612,
                "morph_weight": 1.00,
                "morph_note": "Simple noun pattern (fa'al) — moderately common."
            }
        ],
        "contexts": [
            {
                "id": "seeking_knowledge",
                "sentence_ar": "طلب العلم فريضة على كل مسلم",
                "sentence_en": "Seeking ___ is an obligation for every Muslim.",
                "weights": {"ilm": 2.8, "alima": 0.3, "alam": 0.2},
                "explanation": "'Seeking' (طلب) combined with a religious context strongly favors 'knowledge.'"
            },
            {
                "id": "raised_flag",
                "sentence_ar": "رفع العلم فوق المبنى",
                "sentence_en": "He raised the ___ above the building.",
                "weights": {"ilm": 0.3, "alima": 0.2, "alam": 2.8},
                "explanation": "'Raised above the building' is a physical action that strongly suggests 'flag.'"
            }
        ]
    })

    # ── Example 3: ملك ──────────────────────────────────────────────
    examples.append({
        "id": "mlk",
        "surface": "ملك",
        "root": "م-ل-ك",
        "root_translit": "m-l-k",
        "root_meaning": "ownership, sovereignty",
        "ambiguity_note": "This could be 'king,' 'kingdom,' or 'he owned' — all from the same root concept of possession and authority.",
        "candidates": [
            {
                "id": "malik",
                "diacritized": "مَلِك",
                "transliteration": "malik",
                "gloss": "king",
                "pos": "noun",
                "pos_detail": "active participle form used as noun",
                "pattern": "fa\u02bbil",
                "count": 2156,
                "morph_weight": 1.20,
                "morph_note": "Active participle pattern (fa'il) — very productive for agent nouns."
            },
            {
                "id": "mulk",
                "diacritized": "مُلْك",
                "transliteration": "mulk",
                "gloss": "kingdom / dominion",
                "pos": "noun",
                "pos_detail": "verbal noun",
                "pattern": "fu\u02bbl",
                "count": 1834,
                "morph_weight": 1.15,
                "morph_note": "Noun pattern (fu'l) — common for abstract concepts."
            },
            {
                "id": "malaka",
                "diacritized": "مَلَكَ",
                "transliteration": "malaka",
                "gloss": "he owned / possessed",
                "pos": "verb",
                "pos_detail": "past tense, active, 3rd person masculine singular",
                "pattern": "fa\u02bbala",
                "count": 567,
                "morph_weight": 1.10,
                "morph_note": "Active past verb (fa'ala) — common pattern, but this specific verb is less frequent."
            }
        ],
        "contexts": [
            {
                "id": "ruler",
                "sentence_ar": "ملك البلاد حكم بالعدل",
                "sentence_en": "The ___ of the country ruled with justice.",
                "weights": {"malik": 2.5, "mulk": 0.5, "malaka": 0.3},
                "explanation": "'Ruled with justice' requires a human agent, pointing to 'king.'"
            },
            {
                "id": "owned_land",
                "sentence_ar": "ملك الرجل أرضاً واسعة",
                "sentence_en": "The man ___ a vast piece of land.",
                "weights": {"malik": 0.3, "mulk": 0.4, "malaka": 2.5},
                "explanation": "A person acting on an object ('land') suggests the verb 'he owned.'"
            }
        ]
    })

    # ── Example 4: حكم ──────────────────────────────────────────────
    examples.append({
        "id": "hkm",
        "surface": "حكم",
        "root": "ح-ك-م",
        "root_translit": "ḥ-k-m",
        "root_meaning": "judgment, wisdom",
        "ambiguity_note": "One spelling for 'ruling,' 'he ruled,' and 'referee' — the concept of judgment takes very different forms.",
        "candidates": [
            {
                "id": "hukm",
                "diacritized": "حُكْم",
                "transliteration": "ḥukm",
                "gloss": "ruling / judgment",
                "pos": "noun",
                "pos_detail": "verbal noun (masdar)",
                "pattern": "fu\u02bbl",
                "count": 2134,
                "morph_weight": 1.20,
                "morph_note": "Verbal noun (fu'l) — very common pattern for result/action nouns."
            },
            {
                "id": "hakama",
                "diacritized": "حَكَمَ",
                "transliteration": "ḥakama",
                "gloss": "he ruled / judged",
                "pos": "verb",
                "pos_detail": "past tense, active, 3rd person masculine singular",
                "pattern": "fa\u02bbala",
                "count": 876,
                "morph_weight": 1.15,
                "morph_note": "Active past verb (fa'ala) — standard and common."
            },
            {
                "id": "hakam",
                "diacritized": "حَكَم",
                "transliteration": "ḥakam",
                "gloss": "referee / arbitrator",
                "pos": "noun",
                "pos_detail": "agent noun",
                "pattern": "fa\u02bbal",
                "count": 423,
                "morph_weight": 1.00,
                "morph_note": "Simple noun (fa'al) — used for some occupational nouns."
            }
        ],
        "contexts": [
            {
                "id": "court",
                "sentence_ar": "أصدرت المحكمة حكم بالبراءة",
                "sentence_en": "The court issued a ___ of acquittal.",
                "weights": {"hukm": 2.5, "hakama": 0.4, "hakam": 0.3},
                "explanation": "A court 'issuing' something requires a noun — 'a ruling.'"
            },
            {
                "id": "match",
                "sentence_ar": "حكم المباراة كان عادلاً",
                "sentence_en": "The ___ of the match was fair.",
                "weights": {"hukm": 0.5, "hakama": 0.3, "hakam": 2.5},
                "explanation": "Being described as 'fair' in a match context suggests a person — 'the referee.'"
            }
        ]
    })

    # ── Example 5: قلب ──────────────────────────────────────────────
    examples.append({
        "id": "qlb",
        "surface": "قلب",
        "root": "ق-ل-ب",
        "root_translit": "q-l-b",
        "root_meaning": "turning, heart",
        "ambiguity_note": "The same root gives 'heart' (what turns inside you) and 'to flip' — beautifully connected meanings hidden by the same spelling.",
        "candidates": [
            {
                "id": "qalb",
                "diacritized": "قَلْب",
                "transliteration": "qalb",
                "gloss": "heart",
                "pos": "noun",
                "pos_detail": "singular masculine noun",
                "pattern": "fa\u02bbl",
                "count": 1987,
                "morph_weight": 1.25,
                "morph_note": "Common noun pattern (fa'l) — very frequent for basic nouns."
            },
            {
                "id": "qalaba",
                "diacritized": "قَلَبَ",
                "transliteration": "qalaba",
                "gloss": "he flipped / turned over",
                "pos": "verb",
                "pos_detail": "past tense, active, 3rd person masculine singular",
                "pattern": "fa\u02bbala",
                "count": 312,
                "morph_weight": 1.10,
                "morph_note": "Active past verb (fa'ala) — common pattern, less frequent for this specific root."
            },
            {
                "id": "quliba",
                "diacritized": "قُلِبَ",
                "transliteration": "quliba",
                "gloss": "it was turned over",
                "pos": "verb_passive",
                "pos_detail": "past tense, passive, 3rd person masculine singular",
                "pattern": "fu\u02bbila",
                "count": 89,
                "morph_weight": 0.60,
                "morph_note": "Passive past verb (fu'ila) — rare pattern; passives are infrequent in Arabic text."
            }
        ],
        "contexts": [
            {
                "id": "love",
                "sentence_ar": "القلب ينبض بالحب والأمل",
                "sentence_en": "The ___ beats with love and hope.",
                "weights": {"qalb": 2.8, "qalaba": 0.2, "quliba": 0.2},
                "explanation": "Something that 'beats with love' can only be a heart."
            },
            {
                "id": "page_flip",
                "sentence_ar": "قلب الصفحة وتابع القراءة",
                "sentence_en": "He ___ the page and continued reading.",
                "weights": {"qalb": 0.3, "qalaba": 2.5, "quliba": 0.3},
                "explanation": "Acting on 'the page' and then 'continuing reading' points to 'he flipped.'"
            }
        ]
    })

    # ── Example 6: عمل ──────────────────────────────────────────────
    examples.append({
        "id": "eml",
        "surface": "عمل",
        "root": "ع-م-ل",
        "root_translit": "ʿ-m-l",
        "root_meaning": "work, doing",
        "ambiguity_note": "Is this 'work' the noun, or 'he worked' the verb, or 'it was done' passively? The vowels decide.",
        "candidates": [
            {
                "id": "amal",
                "diacritized": "عَمَل",
                "transliteration": "ʿamal",
                "gloss": "work / deed",
                "pos": "noun",
                "pos_detail": "verbal noun (masdar)",
                "pattern": "fa\u02bbal",
                "count": 2567,
                "morph_weight": 1.20,
                "morph_note": "Verbal noun (fa'al) — very common pattern for activity nouns."
            },
            {
                "id": "amila",
                "diacritized": "عَمِلَ",
                "transliteration": "ʿamila",
                "gloss": "he worked",
                "pos": "verb",
                "pos_detail": "past tense, active, 3rd person masculine singular",
                "pattern": "fa\u02bbila",
                "count": 1234,
                "morph_weight": 1.10,
                "morph_note": "Active past verb (fa'ila) — common for stative/intransitive meaning."
            },
            {
                "id": "umila",
                "diacritized": "عُمِلَ",
                "transliteration": "ʿumila",
                "gloss": "it was done / made",
                "pos": "verb_passive",
                "pos_detail": "past tense, passive, 3rd person masculine singular",
                "pattern": "fu\u02bbila",
                "count": 156,
                "morph_weight": 0.60,
                "morph_note": "Passive past verb (fu'ila) — uncommon passive form."
            }
        ],
        "contexts": [
            {
                "id": "good_deed",
                "sentence_ar": "العمل الصالح ينفع صاحبه",
                "sentence_en": "A good ___ benefits its doer.",
                "weights": {"amal": 2.5, "amila": 0.3, "umila": 0.2},
                "explanation": "The adjective 'good' (الصالح) modifies a noun, favoring 'deed.'"
            },
            {
                "id": "factory_work",
                "sentence_ar": "عمل في المصنع سنوات طويلة",
                "sentence_en": "He ___ in the factory for many years.",
                "weights": {"amal": 0.3, "amila": 2.5, "umila": 0.3},
                "explanation": "'In the factory for many years' describes an ongoing activity — 'he worked.'"
            }
        ]
    })

    # ── Example 7: نظر ──────────────────────────────────────────────
    examples.append({
        "id": "nzr",
        "surface": "نظر",
        "root": "ن-ظ-ر",
        "root_translit": "n-ẓ-r",
        "root_meaning": "looking, seeing",
        "ambiguity_note": "'View,' 'he looked,' or 'it was considered' — sight and judgment share the same root.",
        "candidates": [
            {
                "id": "nazar",
                "diacritized": "نَظَر",
                "transliteration": "naẓar",
                "gloss": "view / consideration",
                "pos": "noun",
                "pos_detail": "verbal noun (masdar)",
                "pattern": "fa\u02bbal",
                "count": 1876,
                "morph_weight": 1.15,
                "morph_note": "Verbal noun (fa'al) — standard masdar pattern."
            },
            {
                "id": "nazara",
                "diacritized": "نَظَرَ",
                "transliteration": "naẓara",
                "gloss": "he looked",
                "pos": "verb",
                "pos_detail": "past tense, active, 3rd person masculine singular",
                "pattern": "fa\u02bbala",
                "count": 1345,
                "morph_weight": 1.15,
                "morph_note": "Active past verb (fa'ala) — very common."
            },
            {
                "id": "nuzira",
                "diacritized": "نُظِرَ",
                "transliteration": "nuẓira",
                "gloss": "it was considered",
                "pos": "verb_passive",
                "pos_detail": "past tense, passive, 3rd person masculine singular",
                "pattern": "fu\u02bbila",
                "count": 123,
                "morph_weight": 0.60,
                "morph_note": "Passive past verb (fu'ila) — rare form."
            }
        ],
        "contexts": [
            {
                "id": "point_of_view",
                "sentence_ar": "من وجهة نظر أخرى",
                "sentence_en": "From another point of ___.",
                "weights": {"nazar": 2.8, "nazara": 0.2, "nuzira": 0.2},
                "explanation": "'Point of ___' is a fixed phrase that requires the noun 'view.'"
            },
            {
                "id": "looked_up",
                "sentence_ar": "نظر إلى السماء بدهشة",
                "sentence_en": "He ___ at the sky in amazement.",
                "weights": {"nazar": 0.3, "nazara": 2.5, "nuzira": 0.3},
                "explanation": "'At the sky in amazement' describes an action — 'he looked.'"
            }
        ]
    })

    # ── Example 8: فتح ──────────────────────────────────────────────
    examples.append({
        "id": "fth",
        "surface": "فتح",
        "root": "ف-ت-ح",
        "root_translit": "f-t-ḥ",
        "root_meaning": "opening",
        "ambiguity_note": "'Opening' as a noun (including historical 'conquest'), the verb 'he opened,' or the passive 'it was opened.'",
        "candidates": [
            {
                "id": "fath",
                "diacritized": "فَتْح",
                "transliteration": "fatḥ",
                "gloss": "opening / conquest",
                "pos": "noun",
                "pos_detail": "verbal noun (masdar)",
                "pattern": "fa\u02bbl",
                "count": 1567,
                "morph_weight": 1.20,
                "morph_note": "Verbal noun (fa'l) — very common masdar pattern."
            },
            {
                "id": "fataha",
                "diacritized": "فَتَحَ",
                "transliteration": "fataḥa",
                "gloss": "he opened",
                "pos": "verb",
                "pos_detail": "past tense, active, 3rd person masculine singular",
                "pattern": "fa\u02bbala",
                "count": 1123,
                "morph_weight": 1.15,
                "morph_note": "Active past verb (fa'ala) — standard active form."
            },
            {
                "id": "futiha",
                "diacritized": "فُتِحَ",
                "transliteration": "futiḥa",
                "gloss": "it was opened",
                "pos": "verb_passive",
                "pos_detail": "past tense, passive, 3rd person masculine singular",
                "pattern": "fu\u02bbila",
                "count": 234,
                "morph_weight": 0.65,
                "morph_note": "Passive past verb (fu'ila) — uncommon."
            }
        ],
        "contexts": [
            {
                "id": "conquest",
                "sentence_ar": "فتح الأندلس كان حدثاً تاريخياً عظيماً",
                "sentence_en": "The ___ of Andalusia was a great historical event.",
                "weights": {"fath": 2.5, "fataha": 0.4, "futiha": 0.3},
                "explanation": "'Of Andalusia' + 'historical event' points to a noun — 'the conquest.'"
            },
            {
                "id": "opened_door",
                "sentence_ar": "فتح الباب ودخل الغرفة",
                "sentence_en": "He ___ the door and entered the room.",
                "weights": {"fath": 0.3, "fataha": 2.5, "futiha": 0.4},
                "explanation": "An action followed by 'entered the room' indicates the verb 'he opened.'"
            }
        ]
    })

    # ── Example 9: درس ──────────────────────────────────────────────
    examples.append({
        "id": "drs",
        "surface": "درس",
        "root": "د-ر-س",
        "root_translit": "d-r-s",
        "root_meaning": "studying, learning",
        "ambiguity_note": "A 'lesson' to learn, 'he studied,' or 'it was studied' — the educational root takes several forms.",
        "candidates": [
            {
                "id": "dars",
                "diacritized": "دَرْس",
                "transliteration": "dars",
                "gloss": "lesson",
                "pos": "noun",
                "pos_detail": "singular masculine noun",
                "pattern": "fa\u02bbl",
                "count": 1456,
                "morph_weight": 1.20,
                "morph_note": "Common noun pattern (fa'l) — frequently used for unit nouns."
            },
            {
                "id": "darasa",
                "diacritized": "دَرَسَ",
                "transliteration": "darasa",
                "gloss": "he studied",
                "pos": "verb",
                "pos_detail": "past tense, active, 3rd person masculine singular",
                "pattern": "fa\u02bbala",
                "count": 987,
                "morph_weight": 1.15,
                "morph_note": "Active past verb (fa'ala) — standard form."
            },
            {
                "id": "durisa",
                "diacritized": "دُرِسَ",
                "transliteration": "durisa",
                "gloss": "it was studied",
                "pos": "verb_passive",
                "pos_detail": "past tense, passive, 3rd person masculine singular",
                "pattern": "fu\u02bbila",
                "count": 178,
                "morph_weight": 0.60,
                "morph_note": "Passive past verb (fu'ila) — infrequent in everyday text."
            }
        ],
        "contexts": [
            {
                "id": "todays_lesson",
                "sentence_ar": "الدرس اليوم عن التاريخ الإسلامي",
                "sentence_en": "Today's ___ is about Islamic history.",
                "weights": {"dars": 2.5, "darasa": 0.3, "durisa": 0.3},
                "explanation": "'Today's ___ is about...' requires a noun subject — 'lesson.'"
            },
            {
                "id": "student_studied",
                "sentence_ar": "درس الطالب ليلة كاملة للامتحان",
                "sentence_en": "The student ___ all night for the exam.",
                "weights": {"dars": 0.3, "darasa": 2.5, "durisa": 0.3},
                "explanation": "A student doing something 'all night for the exam' is clearly 'he studied.'"
            }
        ]
    })

    # ── Example 10: حسب ─────────────────────────────────────────────
    examples.append({
        "id": "hsb",
        "surface": "حسب",
        "root": "ح-س-ب",
        "root_translit": "ḥ-s-b",
        "root_meaning": "reckoning, counting",
        "ambiguity_note": "'According to,' 'he calculated,' or 'he assumed' — three distinct functions from one root about reckoning.",
        "candidates": [
            {
                "id": "hasb",
                "diacritized": "حَسْب",
                "transliteration": "ḥasb",
                "gloss": "according to / only",
                "pos": "particle",
                "pos_detail": "adverbial particle",
                "pattern": "fa\u02bbl",
                "count": 2345,
                "morph_weight": 1.10,
                "morph_note": "Functional particle — very common in formal and written Arabic."
            },
            {
                "id": "hasaba",
                "diacritized": "حَسَبَ",
                "transliteration": "ḥasaba",
                "gloss": "he calculated",
                "pos": "verb",
                "pos_detail": "past tense, active, 3rd person masculine singular",
                "pattern": "fa\u02bbala",
                "count": 876,
                "morph_weight": 1.00,
                "morph_note": "Active past verb (fa'ala) — common pattern, neutral morphological evidence here."
            },
            {
                "id": "hasiba",
                "diacritized": "حَسِبَ",
                "transliteration": "ḥasiba",
                "gloss": "he assumed / thought",
                "pos": "verb",
                "pos_detail": "past tense, active, 3rd person masculine singular",
                "pattern": "fa\u02bbila",
                "count": 567,
                "morph_weight": 0.90,
                "morph_note": "Active past verb (fa'ila) — less common stative pattern."
            }
        ],
        "contexts": [
            {
                "id": "according_to",
                "sentence_ar": "حسب الخطة المتفق عليها",
                "sentence_en": "___ the agreed-upon plan.",
                "weights": {"hasb": 2.8, "hasaba": 0.3, "hasiba": 0.3},
                "explanation": "Followed by 'the plan' without a subject — this is the particle 'according to.'"
            },
            {
                "id": "calculated",
                "sentence_ar": "حسب المهندس التكاليف بدقة",
                "sentence_en": "The engineer ___ the costs precisely.",
                "weights": {"hasb": 0.3, "hasaba": 2.5, "hasiba": 0.4},
                "explanation": "An engineer acting on 'costs precisely' points to 'he calculated.'"
            }
        ]
    })

    # ── Compute base probabilities for all examples ─────────────────
    for ex in examples:
        probs = compute_base_probs(ex["candidates"])
        for i, c in enumerate(ex["candidates"]):
            c["base_prob"] = probs[i]

    return examples


def main():
    examples = build_examples()

    output = {
        "meta": {
            "description": "Curated examples of Arabic orthographic ambiguity for the Missing Bits demo.",
            "source_note": (
                "Counts are estimated from frequency patterns consistent with the "
                "Tashkeela diacritized Arabic corpus. Morphology weights reflect "
                "documented Arabic morphological productivity. Context weights are "
                "hand-curated for demonstration purposes."
            ),
            "smoothing": f"Laplace smoothing with alpha={SMOOTHING_ALPHA}",
            "num_examples": len(examples)
        },
        "examples": examples
    }

    out_path = os.path.join(os.path.dirname(__file__), "..", "data", "examples.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(examples)} examples to {out_path}")

    for ex in examples:
        probs = [c["base_prob"] for c in ex["candidates"]]
        H = entropy(probs)
        print(f"  {ex['surface']} ({ex['id']}): {len(ex['candidates'])} candidates, H={H:.3f} bits")


if __name__ == "__main__":
    main()
