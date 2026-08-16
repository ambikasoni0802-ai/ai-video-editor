# 🎬 AI Video Editor — High Level Version (Free, Open Source)

Ab yeh app **kaisi bhi bhasha mein diya gaya instruction samajh sakta hai**
(Groq ka free LLM use karke), aur bahut saare naye AI-powered edits kar sakta hai.

**Koi paid API nahi.** Groq free tier bahut generous hai (roz hazaron requests
free). Baaki sab (rembg, whisper) khud ke server par chalte hain.

---

## 📁 Files (4 hain)

| File | Kaam |
|---|---|
| `app.py` | Poora app |
| `requirements.txt` | Libraries |
| `Dockerfile` | Setup instructions |
| `README.md` | Yeh file |

---

## 🚀 STEP 1: Groq ka FREE API key lo (5 minute)

Yeh key app ko "smart" banata hai — bina isके bhi app chalega, lekin
sirf fixed keywords samjhega, jaisa pehle tha.

1. **console.groq.com** kholo
2. **"Sign up"** karo (Google se bhi ho sakta hai, free hai)
3. Login hone ke baad left menu mein **"API Keys"** par jao
4. **"Create API Key"** dabao, naam do (jaise `video-editor`)
5. Jo key milegi (`gsk_...` se shuru hogi) — **copy kar lo aur kahin save kar lo**
   (yeh dobara dikhegi nahi)

---

## 🚀 STEP 2: Nayi GitHub repo banao

1. github.com → "+" → "New repository"
2. Naam do: `ai-video-editor-v3`
3. "Create repository"
4. "uploading an existing file" → **chaaron files ek saath** upload karo:
   `app.py`, `requirements.txt`, `Dockerfile`, `README.md`
5. Ek hi baar "Commit changes" dabao

⚠️ Files edit mat karna baad mein — kuch badalna ho toh delete karke naya upload karo.

---

## 🌐 STEP 3: Render par deploy karo (Groq key ke saath)

1. render.com → "New +" → "Web Service"
2. Apni repo (`ai-video-editor-v3`) select karo → "Connect"
3. **Language: Docker**, **Instance: Free**
4. **Environment Variables** section mein (scroll karke neeche milega):
   - **"+ Add Environment Variable"** dabao
   - **Key**: `GROQ_API_KEY`
   - **Value**: apni copy ki hui key paste karo (jo `gsk_...` se shuru hoti hai)
5. **"Deploy Web Service"** dabao

## STEP 4: Wait karo

Build hone mein **15-20 minute** lag sakte hain is baar (Whisper model bhi
download hota hai). Status "Live" hone ka wait karo.

---

## 🛠️ Ab yeh sab kar sakta hai

| Command example | Kya hoga |
|---|---|
| "background hatao" | AI se background remove |
| "subtitles add karo" | Auto speech-to-text captions |
| "pehle 10 second kaato" | Trim |
| "text likho 'Hello'" | Text overlay |
| "speed 2x karo" | Fast forward |
| "slow motion karo" | Slow motion |
| "audio hatao" | Mute |
| "vintage effect lagao" | Retro/vintage look |
| "blur karo" | Background/video blur |
| "zoom karo" | Zoom in effect |
| "black white karo" | Grayscale |
| "rotate karo" | 90 degree rotate |
| "square crop karo" | Instagram-style square |
| "watermark lagao" | Text watermark |
| "fade in fade out karo" | Smooth fade transitions |
| "bright karo" / "dark karo" | Brightness adjust |
| "gif banao" | Video → GIF |

**Smart mode (Groq key ke saath) mein tum multiple cheezein ek saath bol
sakte ho:** *"pehle 5 second kaato, fir vintage effect lagao aur subtitles
add karo"* — sab ek saath ho jayega.

---

## ⚠️ Free tier ki seemayein (honest baat)

- Render free tier **512 MB RAM, 0.1 CPU** deta hai — koi GPU nahi
- **Background removal aur Subtitles** sabse heavy hain — chhoti videos
  (10-20 second) ke liye theek chalega; lambi video (1+ minute) mein bahut
  time lagega ya memory khatam ho ke fail ho sakta hai
- Agar koi feature fail ho, **chhoti video se test karo pehle**
- Free instance kuch der baad "sleep" ho jaata hai, pehli request mein
  30-60 second lag sakta hai

## 🔮 Aage aur kya add ho sakta hai

- Object detection/removal (YOLO — free, lekin bhaari)
- Video upscaling (Real-ESRGAN — free, GPU chahiye achhe se chalne ke liye)
- Background music library se auto-add
- In sabke liye **Google Colab** (jahan free GPU milta hai) better rahega
  Render ke mukable — chaho toh Colab version bhi bana sakte hain
  
