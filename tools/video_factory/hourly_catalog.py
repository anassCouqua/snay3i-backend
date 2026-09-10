#!/usr/bin/env python3
import argparse, json
from pathlib import Path

CITIES = ["كازا", "الرباط", "مراكش", "طنجة", "فاس", "أكادير"]

TOPICS = [
    {
        "language": "darija",
        "title": "الما كيسرب فالدار؟ دير هادشي قبل ما يكبر المشكل | صنايعي",
        "voice": "واش لقيتي الما كيسرب فالدار وما عارفش شكون تعيط ليه؟ إلا قدرت وبلا خطر، سد الما. صوّر التسرب باش تورّيه للبلومبي. من بعد دخل لصنايعي بوان إم أ، قلب على بلومبي حداك، شوف البروفايلات وعيط للي ناسبك.",
        "images": [
            "https://images.pexels.com/photos/3787025/pexels-photo-3787025.jpeg?auto=compress&cs=tinysrgb&w=1600",
            "https://images.pexels.com/photos/7220892/pexels-photo-7220892.jpeg?auto=compress&cs=tinysrgb&w=1600"
        ],
        "scenes": [
            ["الما كيسرب؟", "ما تبقاش كتسنى", "إلا قدرت وبلا خطر، سد الما."],
            ["صوّر المشكل", "وريه للبلومبي", "باش يفهم شنو واقع قبل ما يجي."],
            ["قلب حداك", "شوف البروفايلات", "وقارن قبل ما تعيط."],
            ["صنايعي", "Snay3i.ma", "قلب. قارن. عيط."]
        ]
    },
    {
        "language": "darija",
        "title": "الضو كيطفي؟ ولا البريز سخونة؟ ما تخاطرش | صنايعي",
        "voice": "واش الضو كيطفي بوحدو؟ ولا البريز سخونة وكتشم شي ريحة ديال الحريق؟ ما تحاولش تصلحها بوحدك. إلا كان آمن، قطع الضو وبعّد الدراري من البلاصة. من بعد دخل لصنايعي بوان إم أ وقلب على كهربائي حداك.",
        "images": [
            "https://images.pexels.com/photos/257736/pexels-photo-257736.jpeg?auto=compress&cs=tinysrgb&w=1600",
            "https://images.pexels.com/photos/8005368/pexels-photo-8005368.jpeg?auto=compress&cs=tinysrgb&w=1600"
        ],
        "scenes": [
            ["كاين مشكل فالضو؟", "البريز سخونة ولا كاينة ريحة؟", "ما تخاطرش."],
            ["ما تصلحهاش بوحدك", "إلا ما كنتيش كهربائي", "بعد على الخطر."],
            ["إلا كان آمن", "قطع الضو", "وبعّد الدراري من البلاصة."],
            ["لقى كهربائي", "Snay3i.ma", "قلب على شي واحد حداك."]
        ]
    },
    {
        "language": "darija",
        "title": "قبل ما تختار شي حرفي… دير هاد 3 الحوايج | صنايعي",
        "voice": "قبل ما تعيط لأي صنايعي، دير غير هاد ثلاثة الحوايج. شوف واش كيخدم فمدينتك. سول على الثمن وشنو داخل فيه. واتفقو شحال غادي تاخد الخدمة. فصنايعي بوان إم أ تقدر تشوف البروفايلات وتقارن قبل ما تختار.",
        "images": [
            "https://images.pexels.com/photos/5691693/pexels-photo-5691693.jpeg?auto=compress&cs=tinysrgb&w=1600",
            "https://images.pexels.com/photos/7480727/pexels-photo-7480727.jpeg?auto=compress&cs=tinysrgb&w=1600"
        ],
        "scenes": [
            ["قبل ما تعيط", "دير هاد 3 الحوايج", "باش ما تبقاش حاير."],
            ["أول حاجة", "واش كيخدم فمدينتك؟", "شوف واش يقدر يجي عندك."],
            ["من بعد", "الثمن والوقت", "اتفقو عليهم من اللول."],
            ["قارن قبل ما تختار", "Snay3i.ma", "شوف البروفايلات."]
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
        "title": "باغي تصبغ الدار؟ ما تمشيش غير مع أرخص ثمن | صنايعي",
        "voice": "باغي تصبغ الدار؟ ما تمشيش غير مع أرخص ثمن. سول الصباغ واش المواد داخلين فالثمن، وشحال من كوش غادي يدير. شوف شي خدمة دارها من قبل. ومن بعد قارن مع ناس خرين فصنايعي بوان إم أ.",
        "images": [
            "https://images.pexels.com/photos/5493655/pexels-photo-5493655.jpeg?auto=compress&cs=tinysrgb&w=1600",
            "https://images.pexels.com/photos/5691693/pexels-photo-5691693.jpeg?auto=compress&cs=tinysrgb&w=1600"
        ],
        "scenes": [
            ["باغي تصبغ؟", "ما تشوفش غير الثمن", "الخدمة والمواد مهمين."],
            ["سول الصباغ", "شنو داخل فالثمن؟", "وشحال من كوش غادي يدير؟"],
            ["شوف خدمتو", "قبل ما تبدأ", "باش تعرف المستوى ديالو."],
            ["قارن", "Snay3i.ma", "واختار اللي ناسبك."]
        ]
    },
    {
        "language": "darija",
        "title": "باغي نجار؟ قبل ما تبدا الخدمة سول على هادشي | صنايعي",
        "voice": "باغي تصلح باب، دريسينغ ولا الكوزينة؟ قبل ما تبدا مع النجار، سول على نوع الخشب. شوف شي خدمة دارها من قبل. واتفقو على الثمن والوقت من اللول. دخل لصنايعي بوان إم أ وقارن قبل ما تعيط.",
        "images": [
            "https://images.pexels.com/photos/7480727/pexels-photo-7480727.jpeg?auto=compress&cs=tinysrgb&w=1600",
            "https://images.pexels.com/photos/6790977/pexels-photo-6790977.jpeg?auto=compress&cs=tinysrgb&w=1600"
        ],
        "scenes": [
            ["باغي نجار؟", "سول على نوع الخشب", "ما تبداش حتى تكون فاهم."],
            ["شوف شي خدمة", "دارها من قبل", "الجودة كتبان."],
            ["اتفقو من اللول", "الثمن والوقت", "باش ما يوقع حتى مشكل."],
            ["قارن", "Snay3i.ma", "ومن بعد عيط."]
        ]
    },
    {
        "language": "darija",
        "title": "نتا صنايعي؟ خلي الناس تلقاك بسهولة | صنايعي",
        "voice": "نتا صنايعي وخدمتك زوينة؟ ما تبقاش غير كتسنى الزبون يجيك. دير بروفايلك فصنايعي بوان إم أ. كتب شنو كتخدم وفين كتخدم. وحط تصاور حقيقية ديال خدمتك. هكا الناس يعرفوك ويقدرو يعيطو ليك.",
        "images": [
            "https://images.pexels.com/photos/7480727/pexels-photo-7480727.jpeg?auto=compress&cs=tinysrgb&w=1600",
            "https://images.pexels.com/photos/13229620/pexels-photo-13229620.jpeg?auto=compress&cs=tinysrgb&w=1600"
        ],
        "scenes": [
            ["نتا صنايعي؟", "خلي الناس تلقاك", "ما تبقاش غير كتسنى."],
            ["دير بروفايلك", "كتب شنو كتخدم", "وفين كتخدم."],
            ["وري خدمتك", "حط تصاور حقيقية", "خلي الخدمة تهضر عليك."],
            ["بدا دابا", "Snay3i.ma", "وخلي الناس يعيطو ليك."]
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
