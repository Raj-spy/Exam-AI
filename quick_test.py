import sys, os
sys.path.insert(0, os.path.abspath('.'))
from src.llm.ai_analysis import analyze_face_landmarks

print(analyze_face_landmarks([]))
print(analyze_face_landmarks([{'left_eye':(0,0),'right_eye':(1,0),'nose_tip':(0.2,0)}]))