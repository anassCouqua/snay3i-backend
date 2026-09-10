#!/usr/bin/env python3
import argparse, json
from pathlib import Path

CITIES = ["كازا", "الرباط", "مراكش", "طنجة", "فاس", "أكادير"]

TOPICS = [
    {
        "language": "darija",
        "title": "الما كيسرب فالدار؟ دير هادشي قبل ما يكبر المشكل | صنايعي",
        "voice": "واش الما كيسرب ليك فالدار وما عارفش على من تعيط؟ ما تضيعش الوقت. سد الما إلا كان ممكن وبلا خطر، وصور المشكل. دخل لصنايعي بوان إم أ، قلب على بلومبي قريب ليك، شوف البروفايلات وقارن قبل ما تعيط.",
        "images": [
            "https://images.pexels.com/photos/3787025/pexels-photo-3787025.jpeg?auto=compress&cs=tinysrgb&w=1600",
            "https://images.pexels.com/photos/7220892/pexels-photo-7220892.jpeg?auto=compress&cs=tinysrgb&w=1600"
        ],
        "scenes": [
            ["تسرب الما؟", "الما كيسرب ليك فالدار؟", "ما تخليش المشكل حتى يكبر."],
            ["ديرها دابا", "سد الما إلا كان ممكن", "وصور المشكل باش تشرح للحرفي."],
            ["قلب وقارن", "شوف البروفايلات قبل ما تعيط", "اختار اللي ناسبك وبلا صداع."],
            ["الحرفي قريب ليك", "Snay3i.ma", "قلب. قارن. عيط."]
        ]
    },
    {
        "language": "darija",
        "title": "ريحة ديال الحريق ولا بريز سخونة؟ ما تخاطرش | صنايعي",
        "voice": "الضو كيقطع؟ بريز سخونات ولا كاينة شي ريحة ديال الحريق؟ ما تجربش تصلح الكهرباء بوحدك إلا ما كنتيش مختص. قطع التيار إلا كان هادشي آمن، وباعد الناس على البلاصة. دخل لصنايعي بوان إم أ وقلب على كهربائي مناسب فالمدينة ديالك.",
        "images": [
            "https://images.pexels.com/photos/257736/pexels-photo-257736.jpeg?auto=compress&cs=tinysrgb&w=1600",
            "https://images.pexels.com/photos/8005368/pexels-photo-8005368.jpeg?auto=compress&cs=tinysrgb&w=1600"
        ],
        "scenes": [
            ["خطر الكهرباء", "البريز سخونة ولا كاينة ريحة؟", "ما تتجاهلش هاد العلامات."],
            ["ما تخاطرش", "ما تصلحهاش بوحدك", "إلا ما كنتيش مختص، بعد على الخطر."],
            ["قلب على مهني", "اختار كهربائي مناسب", "شوف المعلومات وقارن قبل الاتصال."],
            ["بلا صداع", "Snay3i.ma", "قلب. قارن. عيط."]
        ]
    },
    {
        "language": "darija",
        "title": "قبل ما تختار شي حرفي… شوف هاد 3 الحوايج | صنايعي",
        "voice": "قبل ما تعيط لشي حرفي، شوف هاد ثلاثة الحوايج. واش كيخدم فالمنطقة ديالك؟ شنو داخل فالثمن؟ وشحال غادي تاخد الخدمة؟ دخل لصنايعي بوان إم أ، شوف البروفايلات وقارن المعلومات قبل ما تقرر.",
        "images": [
            "https://images.pexels.com/photos/5691693/pexels-photo-5691693.jpeg?auto=compress&cs=tinysrgb&w=1600",
            "https://images.pexels.com/photos/7480727/pexels-photo-7480727.jpeg?auto=compress&cs=tinysrgb&w=1600"
        ],
        "scenes": [
            ["قبل ما تعيط", "3 حوايج خاصك تعرف", "ما تختارش بالصدفة."],
            ["1", "واش كيخدم فالمنطقة ديالك؟", "تأكد من المدينة والخدمة."],
            ["2 و 3", "الثمن والمدة يكونو واضحين", "سول قبل ما تبدأ الخدمة."],
            ["قارن بسهولة", "Snay3i.ma", "شوف البروفايلات واختار."]
        ]
    },
    {
        "language": "french",
        "title": "Comment trouver un artisan sans perdre de temps ? | Snay3i.ma",
        "voice": "Besoin d'un artisan sans perdre de temps ? Commencez par vérifier le métier, la ville, les informations du profil et ce qui est inclus dans le devis. Sur Snay3i point ma, vous pouvez comparer les profils disponibles avant de contacter le professionnel qui vous convient.",
        "images": [
            "https://images.pexels.com/photos/5691668/pexels-photo-5691668.jpeg?auto=compress&cs=tinysrgb&w=1600",
            "https://images.pexels.com/photos/7480727/pexels-photo-7480727.jpeg?auto=compress&cs=tinysrgb&w=1600"
        ],
        "scenes": [
            ["Besoin d'un artisan ?", "Ne choisissez pas au hasard", "Quelques vérifications peuvent vous faire gagner du temps."],
            ["Vérifiez", "Métier, ville et profil", "Regardez les informations disponibles."],
            ["Avant les travaux", "Demandez ce qui est inclus", "Comparez avant de décider."],
            ["Trouvez plus facilement", "Snay3i.ma", "Cherchez. Comparez. Contactez."]
        ]
    },
    {
        "language": "darija",
        "title": "باغي تصبغ الدار؟ هاد الغلطة كتقدر تكلفك بزاف | صنايعي",
        "voice": "باغي تصبغ الدار؟ ما تختارش غير على أرخص ثمن. سول شنو داخل فالخدمة، واش الصباغة والمواد داخلين، وشحال من طبقة غادي تدوز. دخل لصنايعي بوان إم أ وقارن بين المعلومات قبل ما تختار الصباغ.",
        "images": [
            "https://images.pexels.com/photos/5493655/pexels-photo-5493655.jpeg?auto=compress&cs=tinysrgb&w=1600",
            "https://images.pexels.com/photos/5691693/pexels-photo-5691693.jpeg?auto=compress&cs=tinysrgb&w=1600"
        ],
        "scenes": [
            ["باغي تصبغ؟", "ما تختارش غير الأرخص", "الثمن بوحدو ما كافيش."],
            ["سول قبل", "شنو داخل فالخدمة؟", "المواد والطبقات يكونو واضحين."],
            ["قارن", "شوف الخدمة والمعلومات", "اختار الصباغ اللي ناسبك."],
            ["بداية أسهل", "Snay3i.ma", "قلب. قارن. عيط."]
        ]
    },
    {
        "language": "darija",
        "title": "باغي نجار؟ قبل ما تبدا الخدمة دير هادشي | صنايعي",
        "voice": "باغي تصلح باب، دريسينغ ولا مطبخ؟ قبل ما تختار النجار، سول على نوع الخشب، شوف شنو خدم من قبل، واتفق على الثمن والمدة بوضوح. دخل لصنايعي بوان إم أ وقارن البروفايلات قبل الاتصال.",
        "images": [
            "https://images.pexels.com/photos/7480727/pexels-photo-7480727.jpeg?auto=compress&cs=tinysrgb&w=1600",
            "https://images.pexels.com/photos/6790977/pexels-photo-6790977.jpeg?auto=compress&cs=tinysrgb&w=1600"
        ],
        "scenes": [
            ["نجار للدار؟", "قبل ما تبدا، سول", "نوع الخشب مهم."],
            ["شوف الخدمة", "طلب أمثلة من قبل", "الجودة خاصها تبان."],
            ["اتفق بوضوح", "الثمن والمدة", "خلي التفاصيل واضحة من الأول."],
            ["لقى اللي ناسبك", "Snay3i.ma", "قلب. قارن. عيط."]
        ]
    },
    {
        "language": "darija",
        "title": "نتا حرفي؟ خدمتك ما غاديش تبان إلا ما كنتيش باين | صنايعي",
        "voice": "نتا حرفي وخدمتك مزيانة؟ الزبون ما يقدرش يلقاك إلا ما كنتيش باين. دير بروفايل واضح فصنايعي بوان إم أ، زيد المدينة والخدمات ديالك، وحط صور حقيقية من الخدمة باش الناس يفهمو شنو كتقدر تدير.",
        "images": [
            "https://images.pexels.com/photos/7480727/pexels-photo-7480727.jpeg?auto=compress&cs=tinysrgb&w=1600",
            "https://images.pexels.com/photos/13229620/pexels-photo-13229620.jpeg?auto=compress&cs=tinysrgb&w=1600"
        ],
        "scenes": [
            ["نتا حرفي؟", "خدمتك خاصها تبان", "الزبون خاصو يعرف يلقاك."],
            ["كمل البروفايل", "المدينة والخدمات", "خلي المعلومات واضحة."],
            ["وري خدمتك", "حط صور حقيقية", "الثقة كتبدا من التفاصيل."],
            ["خلي الناس يلقاوك", "Snay3i.ma", "صايب البروفايل ديالك."]
        ]
    },
    {
        "language": "french",
        "title": "Avant d'accepter un devis, vérifiez ces 3 points | Snay3i.ma",
        "voice": "Avant d'accepter un devis, vérifiez trois points : ce qui est inclus dans le prix, le délai prévu et les matériaux utilisés. Un devis clair évite beaucoup de malentendus. Sur Snay3i point ma, comparez les informations disponibles avant de choisir votre artisan.",
        "images": [
            "https://images.pexels.com/photos/5691513/pexels-photo-5691513.jpeg?auto=compress&cs=tinysrgb&w=1600",
            "https://images.pexels.com/photos/7480727/pexels-photo-7480727.jpeg?auto=compress&cs=tinysrgb&w=1600"
        ],
        "scenes": [
            ["Avant le devis", "Vérifiez ces 3 points", "Évitez les mauvaises surprises."],
            ["Le prix", "Qu'est-ce qui est inclus ?", "Main-d'œuvre, matériel, déplacement…"],
            ["Le délai", "Quand le travail sera-t-il fini ?", "Mettez les détails au clair."],
            ["Comparez", "Snay3i.ma", "Cherchez. Comparez. Contactez."]
        ]
    }
]

def build(slot: int):
    base = TOPICS[slot % len(TOPICS)]
    cycle = slot // len(TOPICS)
    city = CITIES[cycle % len(CITIES)]
    scenes = []
    for i, (eyebrow, headline, body) in enumerate(base["scenes"]):
        scenes.append({
            "eyebrow": eyebrow,
            "headline": headline,
            "body": body,
            "background": f"asset_{i % 2}.jpg",
            "focus_x": 0.5,
            "focus_y": 0.5,
        })
    return {
        "script": {
            "id": f"hourly_{slot:02d}",
            "language": base["language"],
            "format": "1080x1920",
            "voice_text": base["voice"],
            "scenes": scenes,
        },
        "meta": {
            "slot": slot,
            "language": base["language"],
            "title": base["title"],
            "city_rotation": city,
            "images": base["images"],
            "tags": ["Snay3i", "صنايعي", "المغرب", "ArtisanMaroc"],
        }
    }

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--slot", type=int, required=True)
    p.add_argument("--script", required=True)
    p.add_argument("--meta", required=True)
    args = p.parse_args()
    item = build(args.slot % 24)
    Path(args.script).parent.mkdir(parents=True, exist_ok=True)
    Path(args.script).write_text(json.dumps(item["script"], ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.meta).write_text(json.dumps(item["meta"], ensure_ascii=False, indent=2), encoding="utf-8")
