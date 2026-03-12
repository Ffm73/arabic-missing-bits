# Implementation: AI generated

"""
add_context_keywords.py

Adds context_keywords and suggested_sentences to each candidate and example
in examples.json. These keywords power the sentence-input mode's lightweight
context matching.

Each candidate gets a list of Arabic words that, when found in a sentence,
suggest that candidate is the intended reading.
"""

import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "examples.json")

CONTEXT_KEYWORDS = {
    "ktb": {
        "candidates": {
            "kutub": ["مكتبة", "كثيرة", "قراءة", "رف", "مجلد", "صفحات"],
            "kataba": ["طالب", "رسالة", "قلم", "ورقة", "كاتب", "صديق"],
            "kutiba": ["وثيقة", "تاريخ", "سجل", "قديم", "نقش"],
        },
        "suggested_sentences": [
            "في المكتبة كتب كثيرة",
            "كتب الطالب رسالة إلى صديقه",
            "كتب هذا النص في العصر القديم",
        ]
    },
    "elm": {
        "candidates": {
            "ilm": ["طلب", "فريضة", "معرفة", "جامعة", "بحث", "دراسة"],
            "alima": ["خبر", "سر", "حقيقة", "أدرك", "عرف"],
            "alam": ["رفع", "مبنى", "وطني", "بلد", "فوق"],
        },
        "suggested_sentences": [
            "طلب العلم فريضة على كل مسلم",
            "رفع العلم فوق المبنى",
            "علم بالخبر من صديقه",
        ]
    },
    "mlk": {
        "candidates": {
            "malik": ["حكم", "بلاد", "عرش", "تاج", "سلطان"],
            "mulk": ["لله", "سماوات", "أرض", "ملكوت", "سيادة"],
            "malaka": ["رجل", "أرض", "دار", "بيت", "اشترى"],
        },
        "suggested_sentences": [
            "ملك البلاد حكم بالعدل",
            "لله ملك السماوات والأرض",
            "ملك الرجل أرضاً واسعة",
        ]
    },
    "hkm": {
        "candidates": {
            "hukm": ["محكمة", "أصدرت", "براءة", "قانون", "قضاء"],
            "hakama": ["قاضي", "عدل", "بين", "ناس", "فصل"],
            "hakam": ["مباراة", "عادل", "لعب", "كرة", "ملعب"],
        },
        "suggested_sentences": [
            "أصدرت المحكمة حكم بالبراءة",
            "حكم المباراة كان عادلاً",
            "حكم القاضي بين المتخاصمين",
        ]
    },
    "qlb": {
        "candidates": {
            "qalb": ["حب", "ينبض", "أمل", "شعور", "صدر"],
            "qalaba": ["صفحة", "قراءة", "ورقة", "طاولة", "وجه"],
            "quliba": ["تربة", "تفتيش", "بحث", "حفر", "أرض"],
        },
        "suggested_sentences": [
            "القلب ينبض بالحب والأمل",
            "قلب الصفحة وتابع القراءة",
        ]
    },
    "eml": {
        "candidates": {
            "amal": ["صالح", "خير", "ينفع", "حسن", "جزاء"],
            "amila": ["مصنع", "سنوات", "شركة", "وظيفة", "مكتب"],
            "umila": ["آلة", "نظام", "تشغيل", "صنع", "إنتاج"],
        },
        "suggested_sentences": [
            "العمل الصالح ينفع صاحبه",
            "عمل في المصنع سنوات طويلة",
        ]
    },
    "nzr": {
        "candidates": {
            "nazar": ["وجهة", "أخرى", "رأي", "اعتبار", "تأمل"],
            "nazara": ["سماء", "دهشة", "عين", "نافذة", "بعيد"],
            "nuzira": ["نظرية", "فلسفة", "بحث", "علمي", "أكاديمي"],
        },
        "suggested_sentences": [
            "من وجهة نظر أخرى",
            "نظر إلى السماء بدهشة",
        ]
    },
    "fth": {
        "candidates": {
            "fath": ["أندلس", "تاريخي", "إسلامي", "عظيم", "نصر"],
            "fataha": ["باب", "غرفة", "نافذة", "دخل", "مفتاح"],
            "futiha": ["بوابة", "تحقيق", "طريق", "جديد", "رسمي"],
        },
        "suggested_sentences": [
            "فتح الأندلس كان حدثاً تاريخياً عظيماً",
            "فتح الباب ودخل الغرفة",
        ]
    },
    "drs": {
        "candidates": {
            "dars": ["اليوم", "تاريخ", "إسلامي", "أول", "معلم"],
            "darasa": ["طالب", "ليلة", "امتحان", "جامعة", "كتاب"],
            "durisa": ["موضوع", "منهج", "بحث", "تحليل", "علمي"],
        },
        "suggested_sentences": [
            "الدرس اليوم عن التاريخ الإسلامي",
            "درس الطالب ليلة كاملة للامتحان",
        ]
    },
    "hsb": {
        "candidates": {
            "hasb": ["خطة", "متفق", "ترتيب", "برنامج", "موعد"],
            "hasaba": ["مهندس", "تكاليف", "دقة", "رياضيات", "عدد"],
            "hasiba": ["ظن", "اعتقد", "خطأ", "صحيح", "توقع"],
        },
        "suggested_sentences": [
            "حسب الخطة المتفق عليها",
            "حسب المهندس التكاليف بدقة",
        ]
    },
}


def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for ex in data["examples"]:
        eid = ex["id"]
        if eid not in CONTEXT_KEYWORDS:
            continue

        kw_data = CONTEXT_KEYWORDS[eid]

        for candidate in ex["candidates"]:
            cid = candidate["id"]
            keywords = kw_data["candidates"].get(cid, [])
            candidate["context_keywords"] = keywords

        ex["suggested_sentences"] = kw_data.get("suggested_sentences", [])

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {len(data['examples'])} examples with context_keywords and suggested_sentences")


if __name__ == "__main__":
    main()
