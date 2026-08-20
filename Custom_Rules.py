#!/usr/bin/env python3
"""
Snaffler custom rule generator.

Generates one TOML rule per keyword (from Input.txt) and, optionally,
one TOML rule per selected country's local "password" keyword(s)
(from Countries.txt or --country CLI args) -- all into a single,
flat output directory.

Rule-writing logic (sanitize/regex/write_toml/TOML template/country
keyword mappings) is unchanged from the original script.
"""

from pathlib import Path
import argparse
import re


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "Input.txt"
OUTPUT_DIR = BASE_DIR / "rules"
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
# CLI: either pass --country (repeatable) / --all-countries up front,
# or run the script with no country flags and it asks interactively.
# -------------------------
def resolve_countries():
    parser = argparse.ArgumentParser(description="Generate Snaffler TOML rules.")
    parser.add_argument(
        "--country",
        action="append",
        default=[],
        help="Country name to include (repeatable: --country france --country italy). "
             "If omitted, you'll be prompted interactively.",
    )
    parser.add_argument(
        "--all-countries",
        action="store_true",
        help="Generate rules for every supported country.",
    )
    args = parser.parse_args()

    if args.all_countries:
        return list(country_passwords.keys())

    countries = [c.strip().lower() for c in args.country if c.strip()]

    if not countries:
        entered = input("Country (blank to skip): ").strip().lower()
        if entered:
            countries = [entered]

    return countries


# -------------------------
# PART 1: Input.txt keyword rules
# -------------------------
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    terms = [l.strip() for l in f if l.strip() and not l.startswith("#")]

for term in terms:
    rule_file = OUTPUT_DIR / f"{sanitize(term)}.toml"
    write_toml(rule_file, [regex(term)])

print(f"Wrote {len(terms)} keyword rule(s) to {OUTPUT_DIR}/")

# -------------------------
# PART 2: Country rules -- same output dir, same pass
# -------------------------
countries = resolve_countries()
written = 0

for country in countries:
    if country not in country_passwords:
        print(f"Skipping unsupported country: {country}")
        continue