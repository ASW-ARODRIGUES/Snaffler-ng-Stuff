# Snaffler Rules Generator + Snaffler-ng Workflow

This project contains:
- A Python script to generate Snaffler TOML rules
- A workflow for running `snaffler-ng` against SMB shares, FTP shares, and locally mounted filesystems (SSHFS)
- Exporting results into HTML reports

---

# 1. Rule Generator Script

## Overview

The script generates Snaffler-compatible TOML rules from:
- `Input.txt` (keyword-based rules)
- Country-specific password keyword mappings

It outputs:
output_rules/

Each keyword becomes an individual `.toml` rule file.

---

## Usage

### 1. Add keywords
Edit `Input.txt`:

```
password
admin
secret
apikey
```

### 2. Run generator

```
python Custom_Rules.py
```

### 3. Select country when prompted

Country: france

Output:
output_rules/france.toml
output_rules/password.toml
output_rules/admin.toml
output_rules/secret.toml
output_rules/apikey.toml
...

---

# 2. Snaffler-ng Setup

## Install

Recommended (venv):

```
python -m venv snaffler-venv
source snaffler-venv/bin/activate
pip install snaffler-ng
```

Or system-wide (not recommended):

```
pip install snaffler-ng --break-system-packages
```

---

# 3. Target Types Supported

Snaffler-ng can scan:

- SMB shares
- FTP shares
- Local filesystem (--local-fs)
- Mounted remote filesystems (SSHFS)

---

# 4. SMB Usage

## Basic SMB scan

```
snaffler --rule-dir Rules/ smb://192.168.1.10/share
```

## With credentials

```
snaffler --rule-dir Rules/ smb://192.168.1.10/share \
  --username Administrator \
  --password 'Password123'
```

---

# 5. FTP Usage

```
snaffler --rule-dir Rules/ ftp://192.168.1.20/
```

With credentials:

```
snaffler --rule-dir Rules/ ftp://192.168.1.20/ \
  --username user \
  --password pass
```

---

# 6. Local Filesystem Scanning

## Standard local scan

```
snaffler --rule-dir Rules/ --local-fs /path/to/mounted/target
```

Example:

```
snaffler --rule-dir Rules/ --local-fs /path/to/mount
```

---

# 7. SSHFS Workflow (Remote Mounting)

SSHFS allows you to mount a remote system and treat it as a local filesystem for Snaffler.

---

## Mount remote directory via SSHFS

```
sshfs user@target_ip:/remote/path /local/mount/point
```

Example:

```
sshfs Administrator@192.168.1.111:C:\\Users\\Administrator /local/mount/point
```

---

## Verify mount

```
cd /local/mount/point
ls -la
```

---

## Run Snaffler on mounted target

```
snaffler --rule-dir Rules/ --local-fs /local/mount/point
```

---

## Unmount

```
fusermount -u /local/mount/point
```

---

# 8. Using --local-auth

## What it is

--local-auth is used when:
- Authentication is local/session-based
- No domain authentication is required
- Lab / single-host testing environments
- Credentials are already valid on the target system

---

## Example usage

```
snaffler --rule-dir Rules/ \
  --local-auth \
  smb://192.168.1.111/C$
```

Or:

```
snaffler --rule-dir Rules/ \
  --local-auth \
  ftp://192.168.1.111/
```

---

## When to use it

Use --local-auth when:
- Working in isolated lab environments
- Target is a single host
- SMB/FTP auth is not domain-controlled
- Scanning mounted filesystems where auth is already handled (SSHFS)

---

# 9. HTML Reporting

Snaffler can export results into a self-contained HTML report for offline viewing.

## Generate HTML report

```
snaffler results -f html > report.html
```

This produces a standalone HTML file that includes:
- Findings overview
- Matches based on rules
- File paths and exposures
- Structured output for sharing or documentation

---

# 10. Recommended Workflow

### Step 1 — Mount target

```
sshfs user@target_ip:/remote/path /local/mount/point
```

### Step 2 — Activate environment

```
source snaffler-venv/bin/activate
```

### Step 3 — Run scan

```
snaffler --rule-dir Snaffler_Rules --local-fs /local/mount/point
```

### Step 4 — Export report

```
snaffler results -f html > report.html
```

### Step 5 — View results

Open `report.html` in a browser.

---

# 11. Notes

- Regenerate rules when updating Input.txt
- SSHFS is often more stable than direct SMB/FTP scanning
- Use --local-fs for mounted targets for best performance
- Do NOT delete `snaffler.db` — it is used for tracking scan state and results
- Keep rules modular (one keyword per file improves control)

---

# 12. Example Structure

Snaffler_Rules/
│
├── Custom_Rules.py
├── Input.txt
├── output_rules/
│
├── TEST-RULES/
│   ├── PasswordRule.toml
│   ├── admin.toml
│   └── ...
│
└── /local/mount/point/   (any SSHFS mount location)

---

# 13. Summary

This setup enables:
- Automated rule generation
- SMB / FTP / local scanning
- SSHFS-based remote analysis
- Flexible authentication modes including --local-auth
- HTML report generation for sharing results
- Modular, scalable rule management