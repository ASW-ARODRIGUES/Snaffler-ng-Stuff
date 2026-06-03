#!/usr/bin/env python3
from pathlib import Path
import re

# Always resolve paths relative to script location
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "Input.txt"
OUTPUT_DIR = BASE_DIR / "output_rules"
OUTPUT_DIR.mkdir(exist_ok=True)

country_passwords = {
    "indonesia": ["kata sandi"],
    "malaysia": ["kata laluan"],
    "philippines": ["password"],
    "singapore": ["password"],
    "taiwan": ["密碼"],
    "thailand": ["รหัสผ่าน"],
    "vietnam": ["mật khẩu"],
    "austria": ["Passwort"],
    "czech republic": ["heslo"],
    "france": ["mot de passe"],
    "hungary": ["jelszó"],
    "italy": ["password"],
    "latvia": ["parole"],
    "lithuania": ["slaptažodis"],
    "romania": ["parolă"],
    "switzerland": ["Passwort", "mot de passe", "parola"],
    "ukraine": ["пароль"],
    "turkey": ["şifre", "parola"]
}

def sanitize(name):
    return re.sub(r'[\\/*?:"<>|\s]', '_', name)

def regex(term):
    return rf"\b{re.escape(term.strip())}\b"

def write_toml(path, words):
    wordlist = ", ".join(f'"{w}"' for w in words)

    content = f"""[[ClassifierRules]]
EnumerationScope = "ContentsEnumeration"
RuleName = "{path.stem}"
Description = "Auto-generated rule"
MatchAction = "Snaffle"
MatchLocation = "FileContentAsString"
WordListType = "Regex"
WordList = [{wordlist}]
CaseSensitive = false
Triage = "Red"
"""

    path.write_text(content, encoding="utf-8")

# -------------------------
# PART 1: Input.txt rules
# -------------------------
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    terms = [l.strip() for l in f if l.strip() and not l.startswith("#")]

for term in terms:
    rule_file = OUTPUT_DIR / f"{sanitize(term)}.toml"
    write_toml(rule_file, [regex(term)])

# -------------------------
# PART 2: Country rules
# -------------------------
country = input("Country: ").strip().lower()

if country not in country_passwords:
    raise SystemExit(f"Unsupported country: {country}")

rule_file = OUTPUT_DIR / f"{sanitize(country)}.toml"
write_toml(rule_file, [regex(w) for w in country_passwords[country]])

print(f"Created: {rule_file}")