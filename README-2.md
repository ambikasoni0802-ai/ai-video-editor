# 🎬 AI Video Editor (Free, Open Source, khud ka banaya hua)

Video upload karo, text mein bata do kya edit karna hai, edited video wapas milega.
**Koi third-party paid API nahi** — sirf FFmpeg (video processing) aur rembg
(open-source AI model, background remove karne ke liye) — dono khud ke server
par chalte hain.

---

## 📁 Files (sirf 4 hain, sab yahin hain)

| File | Kaam |
|---|---|
| `app.py` | Poora app ka code |
| `requirements.txt` | Python libraries |
| `Dockerfile` | FFmpeg + system setup ka instruction |
| `README.md` | Yeh file |

---

## 🚀 STEP 1: Nayi GitHub repo banao (fresh start)

**Agar purani repo mein confusion ho chuki hai, ise use mat karo — nayi banao:**

1. **github.com** kholo, login karo
2. Top-right "**+**" → "**New repository**"
3. Naam do: `ai-video-editor-v2` (ya koi bhi naya naam)
4. **"Create repository"** dabao

## STEP 2: Saari files EK SAATH upload karo (bahut zaroori)

1. Naye repo page par **"uploading an existing file"** link par tap karo
2. **Chaaron files ek saath select karo** apne phone se (ek-ek karke mat karo):
   - `app.py`
   - `requirements.txt`
   - `Dockerfile`
   - `README.md`
3. Sab select hone ke baad **ek hi baar** "**Commit changes**" dabao

⚠️ **Zaroori:** files ko **edit mat karo** GitHub par baad mein. Agar kuch badalna ho,
toh purani file **delete karke** naya upload karo — edit karne mein mobile par
purani lines reh jaane ka risk hota hai.

---

## 🌐 STEP 3: Render par deploy karo

1. **render.com** kholo → "**Sign up with GitHub**" se login karo
2. Dashboard mein **"New +"** → "**Web Service**"
3. Apni nayi repo (`ai-video-editor-v2`) select karo → "**Connect**"
4. Settings bharo:
   - **Language**: "**Docker**" select karo (Python 3 nahi!)
   - **Instance Type**: "**Free**" (already selected hoga)
5. Neeche **"Deploy Web Service"** dabao

## STEP 4: Wait karo

- Build hone mein **10-15 minute** lagenge (rembg ka AI model bhi download hota hai)
- Status **"Building"** se **"Live"** hone ka wait karo
- Beech mein page baar-baar refresh mat karo, button dobara mat dabao

## STEP 5: App use karo

Link milega:
```
https://ai-video-editor-v2.onrender.com
```
(exact naam tumhare service name ke hisaab se hoga)

Video upload karo, likho **"background hatao"** ya koi aur command, "Edit Karo" dabao.

---

## 🛠️ Abhi kya kya edit kar sakta hai

- **Background hatao** (AI model se — thoda time lagta hai, khaas kar lambi videos mein)
- Trim/cut karna
- Text overlay add karna
- Speed fast/slow karna
- Audio mute karna
- GIF banana
- Audio nikaal ke MP3 banana
- Black & white karna

## ⚠️ Free tier ki seemayein

- **Background removal** heavy hai — chhoti videos (10-20 second) ke liye theek
  chalega, lambi videos mein bahut time lagega ya timeout ho sakta hai (Render
  free tier mein limited CPU hai, GPU nahi)
- Free instance kuch der use na hone par "sleep" ho jaata hai — pehli request
  mein 30-60 second lag sakte hain jagne mein
- Agar background removal bahut slow lage, toh chhoti (5-10 second) test
  videos se try karo pehle

## 🔮 Aage kya add kar sakte ho

- Object removal (open-source model: `lama-cleaner`)
- Auto subtitles (open-source model: `whisper`)
- Face blur/detect (open-source: `opencv` face detection already installed hai)
- Smarter instruction samajhna: keyword matching ki jagah ek free/local LLM
  (jaise `ollama` se local model chalana) add kar sakte ho
