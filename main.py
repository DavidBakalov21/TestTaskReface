import streamlit as st
from gtts import gTTS
from moviepy.editor import *
import tempfile
import os
import zipfile
def text_to_speech(text, target_duration, language='en'):
    temp_audio_path = "temp_output.mp3"
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(temp_audio_path)
    audio_clip = AudioFileClip(temp_audio_path)
    current_duration = audio_clip.duration
    required_playback_speed = current_duration / target_duration
    audio_clip = audio_clip.fx(vfx.speedx, required_playback_speed)
    return audio_clip

st.title('Upload your files there')

clip_num = st.number_input('How many clips do you want:', min_value=1, step=1)
clip_index = st.number_input('Choose clip with generated audio:', min_value=1, step=1)
column_num = st.number_input('Column num:', min_value=1, step=1)
audio_prompt = st.text_area('Enter prompt:')


with st.form(key='file_upload_form'):
    uploaded_file = st.file_uploader(
        "Choose a file", type=['mp4'], accept_multiple_files=False)
    submit_button = st.form_submit_button(label='Upload')

if submit_button:
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_video:
            temp_video.write(uploaded_file.read())
            temp_video_path = temp_video.name
        video = VideoFileClip(temp_video_path)
        duration = video.duration

        part_duration = duration / clip_num

        output_dir = tempfile.mkdtemp()
        parts=[]
        for i in range(clip_num):
            start_time = i * part_duration
            end_time = start_time + part_duration
            part = video.subclip(start_time, end_time)
            
            if (i==clip_index-1):
                new_audio = text_to_speech(audio_prompt, part_duration)
                part = part.without_audio().set_audio(new_audio)
            part_path = os.path.join(output_dir, f'part_{i+1}.mp4')
            part.write_videofile(part_path, codec='libx264')
            parts.append((part_path, f"Part {i+1}"))
            
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
            with zipfile.ZipFile(temp_zip.name, 'w') as zipf:
                for part_path, part_label in parts:
                    zipf.write(part_path, os.path.basename(part_path))
            zip_file_path = temp_zip.name
            
        columns = st.columns(column_num)
        for idx, (part_path, part_label) in enumerate(parts):
            col = columns[idx % column_num]
            with col:
                st.write(f"{part_label} saved at {part_path}")
                st.video(part_path)
                with open(part_path, 'rb') as f:
                    st.download_button(
                        label=f"Download {part_label}",
                        data=f,
                        file_name=f'part_{idx+1}.mp4',
                        mime='video/mp4'
                    )
        os.remove("temp_output.mp3")
        with open(zip_file_path, 'rb') as f:
            zip_data = f.read()

        st.download_button(
            label="Download all",
            data=zip_data,
            file_name='video_parts.zip',
            mime='application/zip'
        )
    else:
        st.write("No file uploaded. Please upload a file.")
    

