# 🛡️ Operation CloudEscape — Stage 2 Complete Solution Guide | מדריך פתרון מלא

> **Challenge Name:** Miss Me Yet? (Stage 2)  
> **Category:** Cloud Security / AWS Lambda + S3 + API Gateway  
> **Solver:** Sagi / Agent freecandy  
> **Captured Flag:** `24dbd66f5c86fbbb7462d6103296e6882c7a0e4931bb8fc5be01ee653acf559c`  
> **Workspace:** `C:\Users\USER\Desktop\CTF\stage2`

---

## 🌐 Language Navigation / ניווט שפות
- [🇮🇱 עברית - מדריך מפורט מלא](#-עברית---מדריך-פתרון-מלא-stage-2)
- [🇬🇧 English - Full Detailed Guide](#-english---full-solution-guide-stage-2)

---

# 🇮🇱 עברית - מדריך פתרון מלא (Stage 2)

## 📌 1. תקציר מנהלים

בשלב 2 קיבלנו credentials זמניים (`ctf_participant_role`) וגישה ל־API של הרצת קוד ב־Lambda בתוך VPC.  
רוב הזמן חקרנו את המסלול “המתוכנן” לפי `docs.html` (קריאת `flag.txt` עם `User-Agent` מדויק מתוך VPC).  
**הפלאג שהתקבל בפועל** לא הגיע מקריאת `flag.txt` עם UA — אלא משדה חדש בתשובת ה־API:

```json
"ctf_out": {
  "c_status": 200,
  "c_md5": "5aa66d248cc567648a1c4ce802bb1754",
  "f_status": 200,
  "f_value": "24dbd66f5c86fbbb7462d6103296e6882c7a0e4931bb8fc5be01ee653acf559c"
}
```

הערך `f_value` (נראה כמו SHA-256, 64 hex) הוא הפלאג שהוגש בהצלחה בפורטל.

---

## 🌳 2. עץ התהליך (Tree View)

```text
📁 Operation CloudEscape (Stage 2 — Miss Me Yet?)
 ├── 🔑 1. זהות והתחלה
 │    ├── Credentials זמניים מהפורטל (Access / Secret / Session)
 │    ├── Role: ctf_participant_role @ account 121774052880
 │    └── בדיקת STS: aws sts get-caller-identity
 │
 ├── 🧭 2. מיפוי נכסים (Recon)
 │    ├── CloudFront: https://d4ysu55xg7wfi.cloudfront.net
 │    ├──   ├── /index.html
 │    ├──   ├── /docs.html          ← מדיניות S3 מרודקטת
 │    ├──   ├── /junior_developer.png
 │    ├──   └── /flag.txt           ← 403 דרך CF
 │    ├── User bucket:  user01906bebf9f38f6c / userd8a2f72fe43094e8
 │    ├── Log bucket:   log01906bebf9f38f6c / logd8a2f72fe43094e8
 │    └── code_exec API: .../dev/code_exec
 │
 ├── 🔬 3. מסלול החקירה הארוך (לא הוביל לפלאג, אבל חשוב)
 │    ├── ניתוח docs.html (Statement1 / Statement2 + REDACTED UA)
 │    ├── אלפי ניסיונות User-Agent מתוך Lambda (timing + trail)
 │    ├── Exfil דרך מפתחות E/<tag>/... בלוגי S3
 │    └── Stego / OCR על junior_developer.png → רק מצביע ל-docs
 │
 ├── ⚡ 4. הפריצה האמיתית
 │    ├── קריאה ל-code_exec עם קוד פשוט (print(1))
 │    ├── קריאת כל ה-JSON בתשובה (לא רק result)
 │    └── חילוץ ctf_out.f_value
 │
 └── 🚩 5. הגשה
      └── Flag: 24dbd66f5c86fbbb7462d6103296e6882c7a0e4931bb8fc5be01ee653acf559c
```

---

## 🔑 3. זהות, באקטים, ו־API

### 3.1 Credentials
מהפורטל / אחרי Stage 1 מקבלים session זמני (~שעה):

| שדה | שימוש |
|-----|--------|
| `AWS_ACCESS_KEY_ID` | ASIA… |
| `AWS_SECRET_ACCESS_KEY` | secret |
| `AWS_SESSION_TOKEN` | session ארוך |
| Region | `us-east-1` |

**טעינה ידנית (PowerShell):**
```powershell
cd C:\Users\USER\Desktop\CTF\stage2
# עדכן set_creds.ps1 ואז:
. .\set_creds.ps1
aws sts get-caller-identity
# צפוי: assumed-role/ctf_participant_role/...
```

קבצים בפרויקט:
- `stage2/set_creds.ps1`
- `stage2/token.txt`

### 3.2 נתיבים ומשאבים שגילינו

| נכס | ערך | הערות |
|-----|------|--------|
| Account | `121774052880` | משתתף |
| Role | `ctf_participant_role` | STS |
| API Gateway + Lambda | `https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec` | POST + SigV4 |
| CloudFront | `https://d4ysu55xg7wfi.cloudfront.net` | אתר האתגר |
| User S3 | `s3://user01906bebf9f38f6c` / `userd8a2f72fe43094e8` | אובייקטי האתגר |
| Log S3 | `s3://log01906bebf9f38f6c` / `logd8a2f72fe43094e8` | לוגים מסוג CloudTrail data events |
| Lambda IP (מלוגים) | `10.0.0.29` | בתוך VPC |
| VPCE | `vpce-04104ef3d57a26557` | גישה ל־S3 מתוך VPC |
| Bucket owner (אתר) | `186769093912` | OAC / CloudFront |

### 3.3 אובייקטים בבאקט המשתמש (דרך CloudFront)

| Path | תוצאה |
|------|--------|
| `/` או `/index.html` | 200 — דף נושא |
| `/docs.html` | 200 — bucket policy עם `REDACTED` |
| `/junior_developer.png` | 200 — תמונה שמצביעה ל־docs |
| `/flag.txt` | **403** |
| נתיבים אקראיים | 404 |

**אין `ListBucket`** למשתתף על `user01906…` / `userd8a...` — אי אפשר לסרוק את כל המפתחות ישירות.

---

## 📜 4. מה `docs.html` אמר לנו (המסלול “המתוכנן”)

בקובץ החי / העותק המקומי `stage2/docs.html`:

- **Statement1:** גישה ציבורית ל־`index.html` / `docs.html` / `junior_developer.png` עם תנאי `aws:UserAgent` בלבד (בפועל דרך CF+OAC).
- **Statement2:** גישה ל־`/*` (כולל `flag.txt`) רק עם:
  - `aws:SourceVpc` = REDACTED
  - `aws:UserAgent` = REDACTED (התאמה מדויקת)

**מסקנה שגרמה לנו לרדוף אחרי UA:**  
צריך להריץ קוד **מתוך Lambda ב־VPC** (כדי לעמוד ב־SourceVpc) ולזייף `User-Agent` מדויק ב־GET ל־S3.

---

## ⚙️ 5. איך עובד `code_exec` (ידנית)

### 5.1 חוזה ה־API
```http
POST /dev/code_exec
Host: l8ssyaz69f.execute-api.us-east-1.amazonaws.com
Content-Type: application/json
X-Amz-Date: ...
X-Amz-Security-Token: ...
X-Amz-Content-Sha256: ...
Authorization: AWS4-HMAC-SHA256 Credential=ASIA.../us-east-1/execute-api/aws4_request, ...

{"code" : "<BASE64 של קוד Python>"}
```

### 5.2 קוד ה־Lambda המקורי (שקיבלנו כרמז מוקדם)
```python
import base64

def lambda_handler(event, context):
    try:
        encoded_code = event.get("code")
        decoded_code = base64.b64decode(encoded_code).decode("utf-8")
        exec(decoded_code)
        return {"result": "Code executed successfully"}
    except Exception:
        return {"error": "Something went wrong!"}
```

כלומר: **אין stdout** בתשובה הרגילה — רק הצלחה/כישלון. לכן בנינו ערוצי exfil.

### 5.3 כלי בפרויקט לחתימה והרצה
- `stage2/invoke_code_exec.py` — חותם SigV4 ומריץ
- `stage2/generate_curl.py` — מייצר `curl` חתום ידני ל־Kali

**דוגמה מקומית:**
```powershell
. .\set_creds.ps1
python invoke_code_exec.py "print(1)"
```

**חשוב לחתימת curl:**  
ה־`--data` חייב להיות **בדיוק** הגוף שנחתם (כולל רווחים סביב `:` אם חתמתם כך). שינוי רווח אחד = SignatureDoesNotMatch.

---

## 🔬 6. מה ניסינו בדרך (רשימת טכניקות + סקריפטים)

זה החלק הארוך — כדי שתוכל לשחזר ידנית גם את המבוי הסתום.

### 6.1 Timing Oracle (זיהוי UA נכון בלי לקרוא את התוכן)
רעיון: בתוך Lambda — אם GET ל־`flag.txt` מצליח → `sleep(4)`; אם 403 → מיד יוצאים.  
תשובה איטית (~4.5s+) = HIT; מהירה (~0.5s) = MISS.

סקריפטים:
- `ua_timing_oracle.py` / `ua_timing_oracle_kali.py`
- `sprint_timing.py`
- `_timing_calibrate.py` (אימות: `sleep(4)` באמת ~4.46s)

דוגמת payload (Python בתוך Lambda):
```python
import urllib.request as u, time
try:
    u.urlopen(u.Request(
        'https://s3.us-east-1.amazonaws.com/userd8a2f72fe43094e8/flag.txt',
        headers={'User-Agent': 'YOUR_UA_HERE'}
    ), timeout=5)
    time.sleep(4)
except Exception:
    pass
```

### 6.2 Trail Exfil דרך לוגי S3
רעיון: מ־Lambda עושים GetObject למפתח כמו:
```text
E/<tag>/<message>
```
גם אם מתקבל AccessDenied — האירוע נרשם ב־`logd8a2f72fe43094e8` תחת:
```text
userd8a2f72fe43094e8/GetObject/<timestamp>.json
```
ואז קוראים את `detail.requestParameters.key` מהלוג.

סקריפטים:
- `trail_pulse.py`, `simple_trail.py`, `checklist_1_trail.py`
- `exfil_net.py` / `exfil_net2.py` / `exfil_net3.py`
- `_lambda_cred_exfil.py` (ניסיון לדלוף env של Lambda ב־hex דרך מפתחות)

פורמט לוג לדוגמה:
```text
s3://logd8a2f72fe43094e8/userd8a2f72fe43094e8/GetObject/2026-08-06-08-52-14-....json
```

### 6.3 חיפוש User-Agent (נכשל כמסלול סופי)
ניסינו אלפי מחרוזות (`ua_tried.txt` ~2500+), כולל:
- שמות האתגר: `Miss Me Yet?`, `"Miss Me Yet?"`, `Junior_Developer`, `junior_developer`
- סלוגנים מהפורטל: `Think You Can Escape the Cloud?`, `not done just yet`, …
- `Agent_Sagi` / `agent_sagi` / `Agent_freecandy`
- מילות docs / Webiks / וכו'

קבצים:
- `ua_candidates_A1.txt`, `UA_CHECKLIST.md`
- `run_wordlist_uas.py`, `ua_bruteforce*.py`, `batch_ua*.py`

**תוצאה:** אחרי warmup — הכל MISS ב־timing. לא זה מה שהביא את הפלאג.

### 6.4 Stego / OCR על התמונה
- `junior_developer.png` — לפטופ פתוח על `cloudfront.net/docs.html`
- `stego_hunt.py`, `inspect_png_meta.py`, crops תחת `ocr_crops/`
- **מסקנה:** מצביע ל־docs בלבד; אין UA סודי קריא על המסך

### 6.5 ניסיונות נוספים (כולם לא היו הפריצה)
| כיוון | סקריפטים / הערות |
|--------|------------------|
| Presign / boto3 GetObject | `sprint_presign.py`, `try_signed_get.py` → עדיין 403 בלי UA |
| CloudFront fuzz | רק index/docs/png = 200 |
| IAM side doors | Lambda get-function / secrets → AccessDenied למשתתף |
| שלב 1 כ־UA | `bgeji4622h3ta5xu` כבר נוסה — לא עובד |
| DVSA-style env leak | `dvsa_style_probe.py` — רעיון טוב, אבל לא הוביל לפלאג |

### 6.6 חוסר יציבות של ה־API (חשוב לשחזור ידני)
במהלך העבודה ה־Lambda התעדכן כמה פעמים. ראינו מצבים שונים:

| תשובה | משמעות |
|--------|---------|
| `Code executed successfully` | exec רגיל עבד |
| `Something went wrong!` | exception בלי פירוט |
| `bad-task` | דחיית משימה / סינון |
| `NameError: _ad_json` / `_advanced_dispatcher` | wrapper חדש שבור/מתחלף |
| `JSONDecodeError` | מצב ביניים של ה־wrapper |
| **`ctf_out` עם `f_value`** | **הפריצה** |

---

## ⚡ 7. הפריצה — איך מצאנו את הפלאג בפועל (שלב־אחר־שלב ידני)

### שלב א' — טען credentials תקינים
```powershell
cd C:\Users\USER\Desktop\CTF\stage2
. .\set_creds.ps1
python -c "import boto3; print(boto3.client('sts').get_caller_identity()['Arn'])"
```

### שלב ב' — קרא ל־`code_exec` עם קוד מינימלי
השתמשנו ב־`invoke_code_exec.py` / `_map_ctf_out.py`:

```powershell
python invoke_code_exec.py "print(1)"
```

או עם הסקריפט שמיפה את `ctf_out`:
```powershell
python _map_ctf_out.py
```

### שלב ג' — קרא את **כל** גוף התשובה
במקום לעצור ב־`result`, שמנו לב שיש שדה נוסף:

```json
{
  "result": "Code executed successfully",
  "ctf_out": {
    "c_status": 200,
    "c_md5": "5aa66d248cc567648a1c4ce802bb1754",
    "f_status": 200,
    "f_value": "24dbd66f5c86fbbb7462d6103296e6882c7a0e4931bb8fc5be01ee653acf559c"
  }
}
```

אותו `f_value` הופיע גם כשהקוד זרק exception — כלומר זה מגיע מה־wrapper של האתגר, לא מ־`print`.

### שלד ד' — שמירה מקומית
נשמר ב־:
```text
stage2/ctf_out_capture.txt
```

### שלב ה' — הגשה בפורטל
הכנסנו את:

```text
24dbd66f5c86fbbb7462d6103296e6882c7a0e4931bb8fc5be01ee653acf559c
```

→ **Success! You completed all the challenges!**

---

## 🧾 8. מה זה `c_md5` ו־`f_value`?

| שדה | ערך | פרשנות |
|-----|------|---------|
| `c_md5` | `5aa66d248cc567648a1c4ce802bb1754` | נראה MD5 (32 hex) — checksum פנימי; **לא** הפלאג |
| `f_value` | `24dbd66f…559c` | נראה SHA-256 (64 hex) — **זה הפלאג שהתקבל** |
| `c_status` / `f_status` | `200` | שניהם הצביעו על “מוכן/תקין” מצד השרת |

לא פיצחנו hash עם john/hashcat.  
**השרת החזיר את `f_value` בתשובת JSON — והגשנו אותו כמו שהוא.**

בדיקה שנעשתה: הערכים **לא** תאמו ל־hash של `index.html` / `docs.html` / `junior_developer.png`.

---

## 🛠️ 9. שחזור ידני מקוצר (Minimal Reproduce)

אם רוצים רק לשחזר את הזכייה (בלי כל הציד):

1. קבל Access Key / Secret / Session מהפורטל.
2. הגדר משתני סביבה (או `set_creds.ps1`).
3. חתום POST ל־`/dev/code_exec` עם body:
   ```json
   {"code" : "cHJpbnQoMSkNCg=="}
   ```
   (`print(1)\r\n` ב־base64)
4. הדפס את התשובה המלאה.
5. העתק `ctf_out.f_value`.
6. הגש ב־`challenges.cloud-escape.com`.

**אם אין `ctf_out`:** ה־API במצב wrapper ישן/שבור — רענן credentials ונסה שוב; במהלך האתגר המנגנון הופיע בחלון זמן קצר.

---

## 📁 10. קבצים מרכזיים בתיקיית `stage2/`

| קובץ | תפקיד |
|------|--------|
| `invoke_code_exec.py` | קריאה חתומה ל־API |
| `generate_curl.py` | יצירת curl ידני ל־Kali |
| `set_creds.ps1` / `token.txt` | credentials |
| `docs.html` | עותק מדיניות |
| `junior_developer.png` | רמז ויזואלי |
| `ua_tried.txt` | UA שניסינו |
| `ua_candidates_A1.txt` | מועמדים מהפורטל |
| `HANDOFF_CLAUDE.md` | סיכום חקירה מוקדם |
| `UA_CHECKLIST.md` | צ'קליסט ציד UA |
| `_map_ctf_out.py` | מיפוי שדה `ctf_out` |
| `ctf_out_capture.txt` | שמירת הפלאג שנמצא |
| `trail_pulse.py` | בדיקת חיים של trail |
| `_timing_calibrate.py` | כיול אורקל זמן |

---

## ✅ 11. סיכום

1. Stage 2 נתן RCE מכוון ב־Lambda (`code_exec`) בתוך VPC + גישה ללוגי S3.  
2. `docs.html` שלח אותנו לצוד `User-Agent` סודי ל־`flag.txt` — בילנו על זה הרבה (timing + trail + wordlists).  
3. **הפלאג הסופי** יצא משדה `ctf_out.f_value` בתשובת ה־API אחרי קריאה פשוטה ל־`code_exec`.  
4. הגשה לפורטל → הצלחה וסיום כל האתגרים.

---

# 🇬🇧 English — Full Solution Guide (Stage 2)

## 1. Executive summary

Stage 2 (“Miss Me Yet?”) gave temporary AWS credentials (`ctf_participant_role`) and a SigV4-protected `code_exec` Lambda API inside a VPC.

We spent most of the time on the **intended-looking path** from `docs.html`: path-style S3 `GetObject` of `flag.txt` with an exact `aws:UserAgent` from inside the VPC (timing oracle + CloudTrail-style trail exfil). Thousands of UA candidates failed.

The **winning flag** was not obtained by guessing the UA. It appeared in a new response field when the Lambda wrapper briefly returned:

```json
"ctf_out": {
  "f_value": "24dbd66f5c86fbbb7462d6103296e6882c7a0e4931bb8fc5be01ee653acf559c"
}
```

Submitting `f_value` on the portal succeeded.

---

## 2. Assets we mapped

| Asset | Value |
|-------|--------|
| API | `https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec` |
| CloudFront | `https://d4ysu55xg7wfi.cloudfront.net` |
| User bucket | `user01906bebf9f38f6c` / `userd8a2f72fe43094e8` |
| Log bucket | `log01906bebf9f38f6c` / `logd8a2f72fe43094e8` |
| Public objects | `index.html`, `docs.html`, `junior_developer.png` |
| Flag object via CF | `flag.txt` → 403 |
| Account / role | `121774052880` / `ctf_participant_role` |

Body format:
```json
{"code" : "<base64 python>"}
```

Helper scripts: `invoke_code_exec.py`, `generate_curl.py`.

---

## 3. Long investigation (did not yield the final flag)

- Parsed redacted bucket policy in `docs.html` (Statement2 = `SourceVpc` + `UserAgent`).
- Timing oracle (`sleep(4)` on HTTP 200) — calibrated in `_timing_calibrate.py`.
- Trail exfil via `E/<tag>/...` keys visible in `log01906…/user…/GetObject/…json`.
- Mass UA hunting (`ua_tried.txt`, wordlists, portal phrases, `junior_developer`, `Miss Me Yet?`, etc.).
- Image stego/OCR — only points to docs.
- Side channels (presign, IAM, CF fuzz) — no flag.

---

## 4. Winning path (manual)

1. Load fresh portal credentials → `set_creds.ps1`.
2. Call `code_exec` with minimal code, e.g. `print(1)`.
3. Read the **full** JSON response.
4. Copy `ctf_out.f_value`.
5. Submit as the flag.

Saved artifact: `stage2/ctf_out_capture.txt`.

**Flag:**
```text
24dbd66f5c86fbbb7462d6103296e6882c7a0e4931bb8fc5be01ee653acf559c
```

---

## 5. Notes on `ctf_out`

- `f_value` looks like SHA-256 (64 hex) — **this was the accepted flag**.
- `c_md5` looks like MD5 — separate internal checksum, not the flag.
- Same `f_value` appeared for success and error responses → emitted by the challenge wrapper, not by our `print`.
- We did **not** crack the hash; we submitted the server-returned value.

---

## ✅ Bottom line

Stage 2 taught a full AWS recon + Lambda RCE + S3 policy story.  
The submitted flag came from reading `ctf_out.f_value` in the `code_exec` API response during a window when the updated Lambda wrapper exposed it.
