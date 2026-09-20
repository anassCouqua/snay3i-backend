import os
import re
from typing import Literal

from mcp.server.fastmcp import FastMCP

PORT = int(os.getenv("PORT", "8000"))

server = FastMCP(
    "snay3i-darija-voice",
    host="0.0.0.0",
    port=PORT,
    stateless_http=True,
    instructions=(
        "Moroccan Darija pronunciation helper. Prefer natural spoken Moroccan phrasing, "
        "not Modern Standard Arabic. For voice work, call prepare_darija_for_tts before "
        "sending text to any TTS engine. Preserve brand pronunciation: صنايعي."
    ),
)

# Phrase-level rewrites are intentionally conservative. They target patterns that
# repeatedly sound written, MSA-like, or translated when spoken in Moroccan ads.
PHRASE_REWRITES = [
    ("ما عارفش على من تعيط", "ما عارفش شكون تعيط ليه"),
    ("ما عارفش لمن تعيط", "ما عارفش شكون تعيط ليه"),
    ("اتصل بالحرفي", "عيط للصنايعي"),
    ("اتصل به", "عيط ليه"),
    ("ابحث عن", "قلب على"),
    ("قم بمقارنة", "قارن"),
    ("اختر الذي يناسبك", "اختار اللي ناسبك"),
    ("في المنزل", "فالدار"),
    ("قريب منك", "حداك"),
    ("لا تنتظر", "ما تبقاش كتسنى"),
]

# A small explicit pronunciation lexicon beats generic Arabic diacritization for
# Moroccan TTS because Darija drops vowels and uses French loanwords heavily.
LEXICON = {
    "واش": "وَاشْ",
    "الما": "لْمَا",
    "كيسرب": "كَيْسَرَّبْ",
    "كيسربليك": "كَيْسَرَّبْ لِيكْ",
    "ليك": "لِيكْ",
    "فالدار": "فَالدَّارْ",
    "وما": "وْمَا",
    "ما": "مَا",
    "عارفش": "عَارْفْشْ",
    "شكون": "شْكُونْ",
    "تعيط": "تْعَيَّطْ",
    "ليه": "لِيهْ",
    "إلا": "إِلَا",
    "قدرت": "قْدَرْتْ",
    "وبلا": "وْبْلَا",
    "بلا": "بْلَا",
    "خطر": "خْطَرْ",
    "سد": "سُدّْ",
    "صور": "صَوَّرْ",
    "التسرب": "التَّسَرُّبْ",
    "باش": "بَاشْ",
    "توريه": "تْوَرِّيهْ",
    "للبلومبي": "لْلْبْلُومْبِي",
    "بلومبي": "بْلُومْبِي",
    "من": "مِنْ",
    "بعد": "بَعْدْ",
    "دخل": "دْخُلْ",
    "لصنايعي": "لْصْنَايْعِي",
    "صنايعي": "صْنَايْعِي",
    "بوان": "بْوَانْ",
    "إم": "إِمْ",
    "أ": "أَ",
    "قلب": "قَلَّبْ",
    "على": "عْلَى",
    "حداك": "حْدَاكْ",
    "شوف": "شُوفْ",
    "البروفايلات": "لْبْرُوفِيلَاتْ",
    "وقارن": "وْقَارَنْ",
    "وعيط": "وْعَيَّطْ",
    "للي": "لِلِّي",
    "ناسبك": "نَاسْبَكْ",
    "الضو": "الضَّوْ",
    "كيطفي": "كَيْطْفِي",
    "بوحدو": "بُوحْدُو",
    "البريز": "لْبْرِيزْ",
    "سخونة": "سْخُونَة",
    "كتشم": "كْتْشَمّْ",
    "ريحة": "رِيحَة",
    "الحريق": "لْحْرِيقْ",
    "دراري": "دْرَارِي",
    "الخدمة": "لْخَدْمَة",
    "الثمن": "الثَّمَنْ",
    "دابا": "دَابَا",
}

WORD_RE = re.compile(r"[\u0600-\u06FF]+|[^\u0600-\u06FF]+")


def _normalise_spacing(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([،,.!?؟])", r"\1", text)
    return text


def naturalise(text: str) -> tuple[str, list[str]]:
    out = _normalise_spacing(text)
    changes: list[str] = []

    # Brand normalization first.
    brand_variants = ["سنايعي", "Snay3i", "snay3i"]
    for variant in brand_variants:
        if variant in out:
            out = out.replace(variant, "صنايعي")
            changes.append(f"{variant} → صنايعي")

    # Spoken .ma convention used by Snay3i ads.
    for variant in [".ma", "دوت ما", "بوان ما", "إم آ"]:
        if variant in out:
            out = out.replace(variant, "بوان إم أ")
            changes.append(f"{variant} → بوان إم أ")

    for old, new in PHRASE_REWRITES:
        if old in out:
            out = out.replace(old, new)
            changes.append(f"{old} → {new}")

    return _normalise_spacing(out), changes


def phoneticise(text: str) -> tuple[str, list[str]]:
    chunks = WORD_RE.findall(text)
    result: list[str] = []
    unknown: list[str] = []

    for chunk in chunks:
        if not re.fullmatch(r"[\u0600-\u06FF]+", chunk):
            result.append(chunk)
            continue

        # Remove existing tashkeel before lookup so repeated calls are stable.
        bare = re.sub(r"[\u064B-\u065F\u0670]", "", chunk)
        if bare in LEXICON:
            result.append(LEXICON[bare])
        else:
            result.append(chunk)
            unknown.append(bare)

    return "".join(result), sorted(set(unknown))


@server.tool()
def normalize_darija(
    text: str,
    style: Literal["casual", "ad", "neutral"] = "casual",
) -> dict:
    """Rewrite text toward natural spoken Moroccan Darija without changing its core meaning."""
    normalized, changes = naturalise(text)
    return {
        "original": text,
        "normalized": normalized,
        "style": style,
        "changes": changes,
        "note": "This is a conservative Moroccan-Darija normalization layer, not MSA translation.",
    }


@server.tool()
def phonetic_darija(text: str) -> dict:
    """Add Moroccan-oriented phonetic tashkeel for TTS using the plugin pronunciation lexicon."""
    phonetic, unknown = phoneticise(text)
    return {
        "original": text,
        "phonetic": phonetic,
        "unknown_words": unknown,
        "coverage_warning": (
            "Unknown words were left unchanged; add them to the lexicon after listening tests."
            if unknown else None
        ),
    }


@server.tool()
def prepare_darija_for_tts(
    text: str,
    voice: Literal["male", "female"] = "male",
    style: Literal["casual", "ad", "neutral"] = "ad",
) -> dict:
    """Normalize Moroccan Darija, apply brand pronunciation rules, then add phonetic tashkeel for TTS."""
    normalized, changes = naturalise(text)
    phonetic, unknown = phoneticise(normalized)
    return {
        "original": text,
        "normalized": normalized,
        "tts_text": phonetic,
        "voice_preference": voice,
        "style": style,
        "changes": changes,
        "unknown_words": unknown,
        "recommended_pacing": {
            "speed": 0.98,
            "chunk_by_sentence": True,
            "pause_seconds": 0.10,
        },
        "brand_pronunciation": {
            "صنايعي": "صْنَايْعِي",
            "Snay3i.ma": "صْنَايْعِي بْوَانْ إِمْ أَ",
        },
    }


if __name__ == "__main__":
    server.run(transport="streamable-http")
