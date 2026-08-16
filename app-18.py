"""
AI Video Editor - Free & Open Source (khud ka banaya hua)
------------------------------------------------------------
- FFmpeg: trim, text overlay, speed, mute, gif, audio extract, black&white
- rembg (open-source AI model, khud ke server par chalta hai):
  video background remove karna
Koi third-party paid API use nahi hui - sab kuch khud ke code
aur open-source models se chal raha hai.
"""

import gradio as gr
import subprocess
import os
import re
import uuid
import shutil

WORK_DIR = "workdir"
os.makedirs(WORK_DIR, exist_ok=True)


def run_ffmpeg(cmd):
    print("Running:", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg error:\n{result.stderr[-1500:]}")
    return result


def extract_number(text, default=None):
    match = re.search(r"(\d+(\.\d+)?)", text)
    if match:
        return float(match.group(1))
    return default


def parse_instruction(instruction):
    text = instruction.lower()
    plan = {"action": None, "params": {}}

    if any(word in text for word in ["background hatao", "background remove", "bg hatao", "background nikalo"]):
        plan["action"] = "remove_bg"

    elif any(word in text for word in ["cut", "trim", "kaato", "kato", "hatao"]):
        plan["action"] = "trim"
        seconds = extract_number(text, default=10)
        if "end" in text or "aakhir" in text or "last" in text:
            plan["params"]["from_end"] = seconds
        else:
            plan["params"]["from_start"] = seconds

    elif any(word in text for word in ["text", "likho", "caption", "likh do", "overlay"]):
        plan["action"] = "add_text"
        quoted = re.findall(r'"([^"]+)"|\'([^\']+)\'', instruction)
        if quoted:
            plan["params"]["text"] = quoted[0][0] or quoted[0][1]
        else:
            plan["params"]["text"] = "Sample Text"

    elif any(word in text for word in ["speed", "fast", "slow", "tez", "dheere"]):
        plan["action"] = "speed"
        factor = extract_number(text, default=1.5)
        if any(word in text for word in ["slow", "dheere"]):
            plan["params"]["factor"] = 1 / factor if factor > 1 else factor
        else:
            plan["params"]["factor"] = factor

    elif any(word in text for word in ["mute", "no audio", "audio hatao", "silent"]):
        plan["action"] = "mute"

    elif any(word in text for word in ["gif", "convert to gif"]):
        plan["action"] = "to_gif"

    elif any(word in text for word in ["audio extract", "nikaalo audio", "mp3", "audio nikalo"]):
        plan["action"] = "extract_audio"

    elif any(word in text for word in ["black white", "grayscale", "bw", "kaala safed"]):
        plan["action"] = "grayscale"

    else:
        plan["action"] = "unknown"

    return plan


def remove_background_video(video_path, out_path, progress=None):
    """
    Video ke har frame se background hataata hai using rembg
    (khud ke server par chalne wala open-source AI model).
    """
    from rembg import remove, new_session
    import cv2

    session = new_session("u2net")  # open-source model, ek baar download hota hai

    uid = uuid.uuid4().hex[:6]
    frames_dir = os.path.join(WORK_DIR, f"frames_{uid}")
    out_frames_dir = os.path.join(WORK_DIR, f"out_frames_{uid}")
    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(out_frames_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(frames_dir, f"f_{frame_count:05d}.png")
        cv2.imwrite(frame_path, frame)
        frame_count += 1
    cap.release()

    for i in range(frame_count):
        in_frame = os.path.join(frames_dir, f"f_{i:05d}.png")
        out_frame = os.path.join(out_frames_dir, f"f_{i:05d}.png")
        with open(in_frame, "rb") as f_in:
            result = remove(f_in.read(), session=session)
        with open(out_frame, "wb") as f_out:
            f_out.write(result)
        if progress is not None:
            progress((i + 1) / frame_count, desc=f"Frame {i+1}/{frame_count} process ho raha hai...")

    cmd = [
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", os.path.join(out_frames_dir, "f_%05d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", out_path
    ]
    run_ffmpeg(cmd)

    shutil.rmtree(frames_dir, ignore_errors=True)
    shutil.rmtree(out_frames_dir, ignore_errors=True)


def apply_edit(video_path, instruction, progress=gr.Progress()):
    if video_path is None:
        return None, "Pehle ek video upload karo."

    plan = parse_instruction(instruction)
    action = plan["action"]
    params = plan["params"]

    uid = uuid.uuid4().hex[:8]
    out_path = os.path.join(WORK_DIR, f"output_{uid}.mp4")

    try:
        if action == "remove_bg":
            progress(0, desc="Background remove ho raha hai, thoda time lagega...")
            remove_background_video(video_path, out_path, progress=progress)
            msg = "Video ka background hata diya gaya (khud ke AI model se, koi third-party API nahi)."

        elif action == "trim":
            if "from_start" in params:
                sec = params["from_start"]
                cmd = ["ffmpeg", "-y", "-i", video_path, "-ss", str(sec), "-c", "copy", out_path]
            else:
                sec = params["from_end"]
                probe = subprocess.run(
                    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=noprint_wrappers=1:nokey=1", video_path],
                    capture_output=True, text=True
                )
                duration = float(probe.stdout.strip())
                new_duration = max(duration - sec, 1)
                cmd = ["ffmpeg", "-y", "-i", video_path, "-t", str(new_duration), "-c", "copy", out_path]
            run_ffmpeg(cmd)
            msg = f"Video trim ho gaya ({sec} second hataye gaye)."

        elif action == "add_text":
            text = params["text"].replace(":", r"\:").replace("'", "")
            drawtext = (
                f"drawtext=text='{text}':fontcolor=white:fontsize=48:"
                f"box=1:boxcolor=black@0.5:boxborderw=10:"
                f"x=(w-text_w)/2:y=h-th-40"
            )
            cmd = ["ffmpeg", "-y", "-i", video_path, "-vf", drawtext,
                   "-codec:a", "copy", out_path]
            run_ffmpeg(cmd)
            msg = f"Text overlay add ho gaya: '{params['text']}'"

        elif action == "speed":
            factor = params["factor"]
            atempo_chain = []
            f = factor
            while f > 2.0:
                atempo_chain.append("atempo=2.0")
                f /= 2.0
            while f < 0.5:
                atempo_chain.append("atempo=0.5")
                f /= 0.5
            atempo_chain.append(f"atempo={f:.3f}")
            audio_filter = ",".join(atempo_chain)
            cmd = ["ffmpeg", "-y", "-i", video_path,
                   "-vf", f"setpts={1/factor:.3f}*PTS",
                   "-af", audio_filter, out_path]
            run_ffmpeg(cmd)
            msg = f"Video speed {factor}x kar diya gaya."

        elif action == "mute":
            cmd = ["ffmpeg", "-y", "-i", video_path, "-c", "copy", "-an", out_path]
            run_ffmpeg(cmd)
            msg = "Audio hata diya gaya (video ab mute hai)."

        elif action == "to_gif":
            out_path = os.path.join(WORK_DIR, f"output_{uid}.gif")
            cmd = ["ffmpeg", "-y", "-i", video_path, "-vf",
                   "fps=10,scale=480:-1:flags=lanczos", out_path]
            run_ffmpeg(cmd)
            msg = "Video GIF mein convert ho gaya."

        elif action == "extract_audio":
            out_path = os.path.join(WORK_DIR, f"output_{uid}.mp3")
            cmd = ["ffmpeg", "-y", "-i", video_path, "-vn",
                   "-acodec", "libmp3lame", out_path]
            run_ffmpeg(cmd)
            msg = "Audio alag se nikaal diya gaya (MP3)."

        elif action == "grayscale":
            cmd = ["ffmpeg", "-y", "-i", video_path, "-vf", "hue=s=0", out_path]
            run_ffmpeg(cmd)
            msg = "Video black & white kar diya gaya."

        else:
            return None, (
                "Yeh instruction samajh nahi aaya. Abhi supported commands:\n"
                "- 'background hatao' (AI se background remove)\n"
                "- 'pehle 10 second kaato' (trim)\n"
                "- 'text likho \"Hello\"' (overlay)\n"
                "- 'speed 2x tez karo'\n"
                "- 'audio hatao / mute karo'\n"
                "- 'gif banao'\n"
                "- 'audio nikaalo'\n"
                "- 'black white karo'"
            )

        return out_path, msg

    except Exception as e:
        return None, f"Error aa gaya: {str(e)}"


with gr.Blocks(title="AI Video Editor") as demo:
    gr.Markdown("# 🎬 AI Video Editor (Free & Open Source, khud ka banaya hua)")
    gr.Markdown(
        "Video upload karo, neeche text box mein bata do kya edit karna hai — "
        "jaise *'background hatao'*, *'pehle 10 second kaato'*, ya *'text likho Hello'*."
    )

    with gr.Row():
        with gr.Column():
            video_input = gr.Video(label="Video Upload Karo")
            instruction_input = gr.Textbox(
                label="Instruction Do",
                placeholder='Jaise: background hatao, ya pehle 10 second kaato'
            )
            submit_btn = gr.Button("Edit Karo", variant="primary")

        with gr.Column():
            video_output = gr.File(label="Edited Output")
            status_output = gr.Textbox(label="Status", interactive=False)

    submit_btn.click(
        fn=apply_edit,
        inputs=[video_input, instruction_input],
        outputs=[video_output, status_output]
    )

    gr.Markdown(
        "### Supported Commands (abhi ke liye)\n"
        "- **Background hatao** (AI model se, thoda time lagta hai)\n"
        "- Trim / cut karna\n"
        "- Text overlay add karna\n"
        "- Speed badalna/kam karna\n"
        "- Audio mute karna\n"
        "- GIF banana\n"
        "- Audio nikalna (MP3)\n"
        "- Black & white karna\n"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
