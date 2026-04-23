import gradio as gr
from konlpy.tag import Okt
import pandas as pd

# 형태소 분석기 초기화
okt = Okt()

def analyze_speech(text):
    if not text.strip():
        return "문장을 입력해주세요.", None
    
    # 형태소 분석
    pos = okt.pos(text)
    tokens = okt.morphs(text)
    
    # 간단한 특성 분석 (예시)
    features = []
    if "?" in text:
        features.append("질문형")
    if any(word in text for word in ["안 돼", "못", "아니"]):
        features.append("부정적 표현 포함")
    if not features:
        features.append("일반 평서문")
    
    analysis_summary = f"전체 단어 수: {len(tokens)}\n특성: {', '.join(features)}"
    
    # 데이터프레임 생성
    df = pd.DataFrame(pos, columns=['단어', '품사'])
    return analysis_summary, df

# 그라디오 인터페이스 구성
with gr.Blocks() as demo:
    gr.Markdown("## 🗣️ AI 언어치료 발화 분석기 (Gradio 버전)")
    gr.Markdown("아동의 문장을 입력하면 AI가 형태소와 문장 특성을 분석합니다.")
    
    with gr.Row():
        input_text = gr.Textbox(label="발화 입력", placeholder="예: 엄마 사과 먹어?", lines=3)
    
    with gr.Row():
        submit_btn = gr.Button("분석하기", variant="primary")
    
    with gr.Column():
        output_summary = gr.Textbox(label="분석 요약")
        output_df = gr.Dataframe(label="상세 형태소 분석")

    submit_btn.click(fn=analyze_speech, inputs=input_text, outputs=[output_summary, output_df])

if __name__ == "__main__":
    demo.launch()
