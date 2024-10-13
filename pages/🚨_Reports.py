import streamlit as st
#from models.video_analyzer import analyze_video, chat_prompt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.mongo_connection import *
from models.face_detection import video_timestamp_detection, destroy_windwows

st.set_page_config(
    page_title="Reports",
    page_icon="🚨",
)

st.selectbox("Select a report", ["Report 1", "Report 2", "Report 3"])

for index, col in enumerate(st.columns(2)):
    with col:
        if index == 0:
            st.write(f"Surveillance video")     
            if not os.path.exists("vid1_cam1_labeled.mp4"):
                get_file("vid1_cam1_labeled.mp4", "videoData")
            st.video("vid1_cam1_labeled.mp4")
        elif index == 1:    
            st.write(f"Detected face")     
            res = get_one_data({"filename" : "vid1_cam1_predictions.json"}, "predictionData", "prediction")

            data = json.loads(res)

            non_empty_count = 0
            for frame_data in data["data"]:
                if non_empty_count >= 5:
                    video_timestamp_detection("vid1_cam1_labeled.mp4", frame_data["frame"], show_frame=False, target_x=frame_data["predictions"][0]["x"], target_y=frame_data["predictions"][0]["y"], target_width=frame_data["predictions"][0]["width"], target_height=frame_data["predictions"][0]["height"], save_image=True)
                    break

                if frame_data["predictions"]:
                    if frame_data["predictions"][0]["level"] == "dangerous" and frame_data["predictions"][0]["confidence"] > 0.5:
                        non_empty_count += 1
                else:
                    non_empty_count = 0 
            
            st.image('vid1_cam1_labeled_face_detection.jpg', use_column_width=True)

st.subheader("Insights")

from models.video_analyzer import analyze_video, openai_analsis_extended_crop

text = openai_analsis_extended_crop('vid1_cam1_labeled', 'mp4')

text = analyze_video('vid1_cam1_labeled', 'mp4', facial_context=text)

st.write(text)