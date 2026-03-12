# Implementation: AI generated

"""
add_context_patterns.py

Adds structural context_patterns to each example in examples.json.
These patterns power the sentence-aware context engine.

Each pattern has:
  - id: unique name
  - condition: what structural cue to check
  - weights: per-candidate multiplier when the cue fires
  - explanation: human-readable reason shown in the UI
"""

import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "examples.json")

PATTERNS = {
    "ktb": [
        {
            "id": "verb_subject_object",
            "condition": "followed_by_proper_then_definite",
            "weights": {"kutub": 0.2, "kataba": 3.5, "kutiba": 0.5},
            "explanation": "A name followed by a noun after this word is a verb-subject-object pattern — 'he wrote' is most likely."
        },
        {
            "id": "verb_sentence_initial",
            "condition": "sentence_initial_followed_by_noun",
            "weights": {"kutub": 0.3, "kataba": 3.0, "kutiba": 0.8},
            "explanation": "Starting a sentence and followed by a noun suggests a verb — Arabic sentences commonly begin with the verb."
        },
        {
            "id": "noun_demonstrative",
            "condition": "preceded_by_demonstrative",
            "weights": {"kutub": 3.5, "kataba": 0.2, "kutiba": 0.2},
            "explanation": "A demonstrative (هذه/هذا) before this word strongly suggests a noun — 'these books.'"
        },
        {
            "id": "noun_demo_adj",
            "condition": "preceded_by_demonstrative_and_followed_by_adjective",
            "weights": {"kutub": 4.0, "kataba": 0.1, "kutiba": 0.1},
            "explanation": "Demonstrative + word + adjective is a classic noun phrase — 'these new books.'"
        },
        {
            "id": "noun_preposition",
            "condition": "preceded_by_preposition",
            "weights": {"kutub": 2.5, "kataba": 0.4, "kutiba": 0.4},
            "explanation": "After a preposition, a noun reading is more natural — 'in the books.'"
        },
        {
            "id": "library_context",
            "condition": "keyword_match",
            "keywords": ["مكتبة", "رف", "قراءة"],
            "min_matches": 1,
            "weights": {"kutub": 2.5, "kataba": 0.4, "kutiba": 0.3},
            "explanation": "Words about libraries or reading favor the noun 'books.'"
        },
        {
            "id": "writing_context",
            "condition": "keyword_match",
            "keywords": ["رسالة", "قلم", "ورقة", "كاتب"],
            "min_matches": 1,
            "weights": {"kutub": 0.3, "kataba": 2.5, "kutiba": 0.4},
            "explanation": "Words about writing tools or letters favor the verb 'he wrote.'"
        },
    ],
    "elm": [
        {
            "id": "noun_preposition",
            "condition": "preceded_by_preposition",
            "weights": {"ilm": 2.5, "alima": 0.4, "alam": 1.0},
            "explanation": "After a preposition, the noun 'knowledge' or 'flag' is more natural."
        },
        {
            "id": "verb_initial",
            "condition": "sentence_initial_followed_by_noun",
            "weights": {"ilm": 0.3, "alima": 3.0, "alam": 0.3},
            "explanation": "Starting a sentence and followed by a noun suggests a verb — 'he knew.'"
        },
        {
            "id": "noun_demonstrative",
            "condition": "preceded_by_demonstrative",
            "weights": {"ilm": 2.0, "alima": 0.2, "alam": 2.0},
            "explanation": "A demonstrative before this word suggests a noun reading."
        },
        {
            "id": "flag_context",
            "condition": "keyword_match",
            "keywords": ["رفع", "فوق", "مبنى", "وطني"],
            "min_matches": 1,
            "weights": {"ilm": 0.15, "alima": 0.15, "alam": 4.0},
            "explanation": "Words about raising or buildings suggest 'flag.'"
        },
        {
            "id": "knowledge_context",
            "condition": "keyword_match",
            "keywords": ["طلب", "فريضة", "جامعة", "بحث"],
            "min_matches": 1,
            "weights": {"ilm": 3.0, "alima": 0.3, "alam": 0.3},
            "explanation": "Words about seeking or universities favor 'knowledge.'"
        },
    ],
    "mlk": [
        {
            "id": "verb_initial",
            "condition": "sentence_initial_followed_by_noun",
            "weights": {"malik": 0.5, "mulk": 0.3, "malaka": 3.0},
            "explanation": "Starting a sentence followed by a noun suggests the verb 'he owned.'"
        },
        {
            "id": "noun_demonstrative",
            "condition": "preceded_by_demonstrative",
            "weights": {"malik": 2.5, "mulk": 2.0, "malaka": 0.2},
            "explanation": "A demonstrative suggests a noun — 'this king' or 'this kingdom.'"
        },
        {
            "id": "noun_preposition",
            "condition": "preceded_by_preposition",
            "weights": {"malik": 1.5, "mulk": 2.5, "malaka": 0.3},
            "explanation": "After a preposition, noun readings are more natural."
        },
        {
            "id": "king_context",
            "condition": "keyword_match",
            "keywords": ["حكم", "عرش", "تاج", "بلاد"],
            "min_matches": 1,
            "weights": {"malik": 3.0, "mulk": 0.5, "malaka": 0.4},
            "explanation": "Words about ruling or throne favor 'king.'"
        },
    ],
    "hkm": [
        {
            "id": "noun_preposition",
            "condition": "preceded_by_preposition",
            "weights": {"hukm": 2.5, "hakama": 0.4, "hakam": 1.0},
            "explanation": "After a preposition, the noun 'ruling' is more natural."
        },
        {
            "id": "verb_initial",
            "condition": "sentence_initial_followed_by_noun",
            "weights": {"hukm": 0.3, "hakama": 3.0, "hakam": 0.5},
            "explanation": "Starting with this word followed by a noun suggests the verb 'he judged.'"
        },
        {
            "id": "match_context",
            "condition": "keyword_match",
            "keywords": ["مباراة", "لعب", "كرة", "ملعب"],
            "min_matches": 1,
            "weights": {"hukm": 0.3, "hakama": 0.3, "hakam": 3.5},
            "explanation": "Sports-related words favor the reading 'referee.'"
        },
        {
            "id": "court_context",
            "condition": "keyword_match",
            "keywords": ["محكمة", "قضاء", "براءة", "قانون"],
            "min_matches": 1,
            "weights": {"hukm": 3.0, "hakama": 0.5, "hakam": 0.3},
            "explanation": "Legal terms favor the noun 'ruling/judgment.'"
        },
    ],
    "qlb": [
        {
            "id": "noun_demonstrative",
            "condition": "preceded_by_demonstrative",
            "weights": {"qalb": 3.0, "qalaba": 0.2, "quliba": 0.2},
            "explanation": "A demonstrative before suggests the noun 'heart.'"
        },
        {
            "id": "verb_initial",
            "condition": "sentence_initial_followed_by_noun",
            "weights": {"qalb": 0.3, "qalaba": 3.0, "quliba": 0.5},
            "explanation": "Sentence-initial position followed by a noun suggests the verb 'he flipped.'"
        },
        {
            "id": "heart_context",
            "condition": "keyword_match",
            "keywords": ["حب", "ينبض", "شعور", "صدر"],
            "min_matches": 1,
            "weights": {"qalb": 3.5, "qalaba": 0.2, "quliba": 0.2},
            "explanation": "Words about feelings or beating favor 'heart.'"
        },
        {
            "id": "flip_context",
            "condition": "keyword_match",
            "keywords": ["صفحة", "ورقة", "طاولة"],
            "min_matches": 1,
            "weights": {"qalb": 0.3, "qalaba": 3.0, "quliba": 0.3},
            "explanation": "Words about pages or tables favor 'he flipped.'"
        },
    ],
    "eml": [
        {
            "id": "noun_demonstrative",
            "condition": "preceded_by_demonstrative",
            "weights": {"amal": 3.0, "amila": 0.2, "umila": 0.2},
            "explanation": "A demonstrative suggests the noun 'work/deed.'"
        },
        {
            "id": "verb_initial",
            "condition": "sentence_initial_followed_by_noun",
            "weights": {"amal": 0.3, "amila": 3.0, "umila": 0.5},
            "explanation": "Sentence-initial + noun suggests the verb 'he worked.'"
        },
        {
            "id": "noun_preposition",
            "condition": "preceded_by_preposition",
            "weights": {"amal": 2.5, "amila": 0.4, "umila": 0.4},
            "explanation": "After a preposition, a noun reading is more natural."
        },
        {
            "id": "factory_context",
            "condition": "keyword_match",
            "keywords": ["مصنع", "شركة", "وظيفة", "مكتب"],
            "min_matches": 1,
            "weights": {"amal": 0.4, "amila": 3.0, "umila": 0.3},
            "explanation": "Workplace words favor the verb 'he worked.'"
        },
    ],
    "nzr": [
        {
            "id": "noun_preposition",
            "condition": "preceded_by_preposition",
            "weights": {"nazar": 2.5, "nazara": 0.4, "nuzira": 0.4},
            "explanation": "After a preposition, the noun 'view/consideration' is more natural."
        },
        {
            "id": "verb_initial",
            "condition": "sentence_initial_followed_by_noun",
            "weights": {"nazar": 0.3, "nazara": 3.0, "nuzira": 0.5},
            "explanation": "Sentence-initial + noun suggests the verb 'he looked.'"
        },
        {
            "id": "sight_context",
            "condition": "keyword_match",
            "keywords": ["سماء", "دهشة", "عين", "نافذة"],
            "min_matches": 1,
            "weights": {"nazar": 0.3, "nazara": 3.0, "nuzira": 0.3},
            "explanation": "Words about sky or eyes favor 'he looked.'"
        },
    ],
    "fth": [
        {
            "id": "noun_demonstrative",
            "condition": "preceded_by_demonstrative",
            "weights": {"fath": 3.0, "fataha": 0.2, "futiha": 0.2},
            "explanation": "A demonstrative suggests the noun 'opening/conquest.'"
        },
        {
            "id": "verb_initial",
            "condition": "sentence_initial_followed_by_noun",
            "weights": {"fath": 0.4, "fataha": 3.0, "futiha": 0.5},
            "explanation": "Sentence-initial + noun suggests the verb 'he opened.'"
        },
        {
            "id": "door_context",
            "condition": "keyword_match",
            "keywords": ["باب", "نافذة", "غرفة", "مفتاح"],
            "min_matches": 1,
            "weights": {"fath": 0.3, "fataha": 3.0, "futiha": 0.5},
            "explanation": "Words about doors or rooms favor 'he opened.'"
        },
        {
            "id": "history_context",
            "condition": "keyword_match",
            "keywords": ["اندلس", "تاريخ", "نصر", "إسلامي"],
            "min_matches": 1,
            "weights": {"fath": 3.0, "fataha": 0.3, "futiha": 0.3},
            "explanation": "Historical terms favor 'conquest/opening.'"
        },
    ],
    "drs": [
        {
            "id": "noun_demonstrative",
            "condition": "preceded_by_demonstrative",
            "weights": {"dars": 3.0, "darasa": 0.2, "durisa": 0.3},
            "explanation": "A demonstrative suggests the noun 'lesson.'"
        },
        {
            "id": "verb_initial",
            "condition": "sentence_initial_followed_by_noun",
            "weights": {"dars": 0.3, "darasa": 3.0, "durisa": 0.5},
            "explanation": "Sentence-initial + noun suggests the verb 'he studied.'"
        },
        {
            "id": "noun_preposition",
            "condition": "preceded_by_preposition",
            "weights": {"dars": 2.5, "darasa": 0.4, "durisa": 0.4},
            "explanation": "After a preposition, the noun 'lesson' is more natural."
        },
        {
            "id": "student_context",
            "condition": "keyword_match",
            "keywords": ["طالب", "امتحان", "جامعة", "ليلة"],
            "min_matches": 1,
            "weights": {"dars": 0.4, "darasa": 3.0, "durisa": 0.3},
            "explanation": "Student/exam words favor the verb 'he studied.'"
        },
    ],
    "hsb": [
        {
            "id": "particle_followed_by_definite",
            "condition": "followed_by_definite_noun",
            "weights": {"hasb": 3.0, "hasaba": 0.4, "hasiba": 0.4},
            "explanation": "Followed by a definite noun suggests the particle 'according to.'"
        },
        {
            "id": "verb_initial",
            "condition": "sentence_initial_followed_by_noun",
            "weights": {"hasb": 0.5, "hasaba": 2.5, "hasiba": 1.5},
            "explanation": "Sentence-initial + noun could be a verb — 'he calculated' or 'he assumed.'"
        },
        {
            "id": "math_context",
            "condition": "keyword_match",
            "keywords": ["رياضيات", "تكاليف", "دقة", "عدد", "مهندس"],
            "min_matches": 1,
            "weights": {"hasb": 0.3, "hasaba": 3.0, "hasiba": 0.5},
            "explanation": "Math-related words favor 'he calculated.'"
        },
    ],
}


def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for ex in data["examples"]:
        eid = ex["id"]
        if eid in PATTERNS:
            ex["context_patterns"] = PATTERNS[eid]

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {len(PATTERNS)} examples with context_patterns")
    for eid, rules in PATTERNS.items():
        print(f"  {eid}: {len(rules)} pattern rules")


if __name__ == "__main__":
    main()
