import math
import secrets
import string
import time
from typing import Dict, List, Tuple

DICEWARE_WORDS = [
    "apple", "brave", "cloud", "delta", "eagle", "flame", "grape", "house",
    "ivory", "joker", "karma", "lemon", "maple", "noble", "ocean", "piano",
    "queen", "river", "solar", "tiger", "ultra", "vivid", "whale", "xenon",
    "yacht", "zebra", "amber", "bison", "cedar", "drift", "ember", "frost",
    "giant", "haven", "index", "jewel", "knack", "lotus", "mango", "nexus",
    "orbit", "pearl", "quest", "radar", "storm", "tulip", "unity", "vapor",
    "waltz", "yield", "acorn", "blaze", "coral", "dunes", "epoch", "flora",
    "gleam", "haste", "inlet", "jaunt", "koala", "lunar", "mirth", "north"
]

CONSONANTS = "bcdfghjklmnpqrstvwxz"
VOWELS = "aeiouy"

#Расчёт информационной энтропии пароля по Шеннону (в битах)
def shannon_entropy(password: str) -> float:
    if not password:
        return 0.0
    length = len(password)
    freqs: Dict[str, int] = {}
    for ch in password:
        freqs[ch] = freqs.get(ch, 0) + 1
    h_per_char = -sum((cnt / length) * math.log2(cnt / length) for cnt in freqs.values())
    return h_per_char * length


#Расчёт теоретической (алфавитной) энтропии пароля (в битах)
def pool_entropy(password: str) -> float:
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += len(string.punctuation)
    return len(password) * math.log2(max(pool, 26))

#Baseline: классический буквенно-цифровой пароль
def generate_baseline(length: int = 8) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

#Генератор 1: криптостойкая случайная последовательность символов
def generate_random_chars(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*_-+="
    return "".join(secrets.choice(alphabet) for _ in range(length))

#Генератор 2: парольная фраза по методике Diceware
def generate_diceware(num_words: int = 4, separator: str = "-") -> str:
    return separator.join(secrets.choice(DICEWARE_WORDS) for _ in range(num_words))

#Генератор 3: фонетически произносимый пароль шаблона CVCV + цифры
def generate_phonetic(syllables: int = 5) -> str:
    parts: List[str] = []
    for i in range(syllables):
        c = secrets.choice(CONSONANTS)
        if i % 2 == 1:
            c = c.upper()
        v = secrets.choice(VOWELS)
        parts.append(c + v)
    digits = f"{secrets.randbelow(90) + 10}"
    return "".join(parts) + digits

#Генерация выборки и оценка энтропии для всех методов
def run_benchmark(sample_size: int = 1000) -> None:
    generators = {
        "Baseline (8 символов)": lambda: generate_baseline(8),
        "Случайные символы (12 символов)": lambda: generate_random_chars(12),
        "Passphrase Diceware (4 слова)": lambda: generate_diceware(4),
        "Фонетические (5 слогов + 2 цифры)": lambda: generate_phonetic(5),
    }
    for name, gen_fn in generators.items():
        t0 = time.perf_counter()
        samples = [gen_fn() for _ in range(sample_size)]
        sh_vals = [shannon_entropy(p) for p in samples]
        pl_vals = [pool_entropy(p) for p in samples]
        dt_ms = (time.perf_counter() - t0) * 1000
        print(
            f"{name}: L={sum(len(p) for p in samples)/sample_size:.1f}, "
            f"H_pool={sum(pl_vals)/sample_size:.1f} бит, "
            f"H_sh={sum(sh_vals)/sample_size:.1f} бит, "
            f"t={dt_ms:.2f} мс"
        )


if __name__ == "__main__":
    run_benchmark(1000)