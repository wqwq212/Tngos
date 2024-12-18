#분류 결과 + 이미지 + 텍스트와 함께 분류 결과에 따라 다른 출력 보여주기
#파일 이름 streamlit_app.py
import streamlit as st
from fastai.vision.all import *
from PIL import Image
import gdown

# Google Drive 파일 ID
file_id = '1s12QBURrTDKEXdfwDN7_AvchfUxCB9Ch'

# Google Drive에서 파일 다운로드 함수
#@st.cache(allow_output_mutation=True)
@st.cache_resource
def load_model_from_drive(file_id):
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model.pkl'
    gdown.download(url, output, quiet=False)

    # Fastai 모델 로드
    learner = load_learner(output)
    return learner

def display_left_content(image, prediction, probs, labels):
    st.write("### 왼쪽: 기존 출력 결과")
    if image is not None:
        st.image(image, caption="업로드된 이미지", use_container_width=True)
    st.write(f"예측된 클래스: {prediction}")
    st.markdown("<h4>클래스별 확률:</h4>", unsafe_allow_html=True)
    for label, prob in zip(labels, probs):
        st.markdown(f"""
            <div style="background-color: #f0f0f0; border-radius: 5px; padding: 5px; margin: 5px 0;">
                <strong style="color: #333;">{label}:</strong>
                <div style="background-color: #d3d3d3; border-radius: 5px; width: 100%; padding: 2px;">
                    <div style="background-color: #4CAF50; width: {prob*100}%; padding: 5px 0; border-radius: 5px; text-align: center; color: white;">
                        {prob:.4f}
                    </div>
                </div>
        """, unsafe_allow_html=True)

def display_right_content(prediction, data):
    st.write("### 오른쪽: 동적 분류 결과")
    cols = st.columns(3)

    # 1st Row - Images
    for i in range(3):
        with cols[i]:
            st.image(data['images'][i], caption=f"이미지: {prediction}", use_container_width=True)
    # 2nd Row - YouTube Videos
    for i in range(3):
        with cols[i]:
            st.video(data['videos'][i])
            st.caption(f"유튜브: {prediction}")
    # 3rd Row - Text
    for i in range(3):
        with cols[i]:
            st.write(data['texts'][i])

# 모델 로드
st.write("모델을 로드 중입니다. 잠시만 기다려주세요...")
learner = load_model_from_drive(file_id)
st.success("모델이 성공적으로 로드되었습니다!")

labels = learner.dls.vocab

# 스타일링을 통해 페이지 마진 줄이기
st.markdown("""
    <style>
    .reportview-container .main .block-container {
        max-width: 90%;
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 분류에 따라 다른 콘텐츠 관리
content_data = {
    labels[0]: {
        'images': [
            "https://i.ibb.co/KGwHPYb/toy-poodle-grassy-field-1359-54.jpg",
            "https://i.ibb.co/khdZ3j9/1.jpg",
            "https://i.ibb.co/WkWjtqd/62f9a36ea3cea.jpg"
        ],
        'videos': [
            "https://youtu.be/pbBADBjZ-pA?feature=shared",
            "https://youtu.be/g1PCVPYCa0Y?feature=shared",
            "https://youtu.be/nGt4nb2TdqI?feature=shared"
        ],
        'texts': [
            "강쥐는우리에게매우친숙한동물이죠",
            "멍멍하고짖기도하고",
            "왈왈하고짖기도하고"
        ]
    },
    labels[1]: {
        'images': [
            "https://i.ibb.co/zsR04dN/image.jpg",
            "https://i.ibb.co/N9kQXW4/1.jpg",
            "https://i.ibb.co/QQDXyF4/2.jpg"
        ],
        'videos': [
            "https://youtu.be/4Qry1Osot08?feature=shared",
            "https://youtu.be/OzkJqjFwcyc?feature=shared",
            "https://youtu.be/FhA37Sw4j8w?feature=shared"
        ],
        'texts': [
            "고양이는",
            "귀엽습니다",
            "나만없어고양이"
        ]
    },
    labels[2]: {
        'images': [
            "https://i.ibb.co/z5ZtZws/157681-27857-45.jpg",
            "https://i.ibb.co/CQTjP11/d4-W-Ib-UYm-I-l-ONb-MMSSWSUFd-R3-Nve5-eoz-U5-NCe-Yp8-VMLStp0-Ipe-CJU7s1r3-Rxpl-Gj-V17-3-USTjj-To-Ca0.webp",
            "https://i.ibb.co/R7pJY2D/image-readtop-2018-265364-15247057823291378.jpg"
        ],
        'videos': [
            "https://youtu.be/z0uh9Z62_r4?feature=shared",
            "https://youtu.be/MToDABYSEwk?feature=shared",
            "https://youtu.be/m_ALU4sqVoU?feature=shared"
        ],
        'texts': [
            "토끼사진이군요!",
            "바쁜일상속",
            "토끼영상보며힐링하세요"
        ]
    }
}

# 레이아웃 설정
left_column, right_column = st.columns([1, 2])  # 왼쪽과 오른쪽의 비율 조정

# 파일 업로드 컴포넌트 (jpg, png, jpeg, webp, tiff 지원)
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "png", "jpeg", "webp", "tiff"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img = PILImage.create(uploaded_file)
    prediction, _, probs = learner.predict(img)

    with left_column:
        display_left_content(image, prediction, probs, labels)

    with right_column:
        # 분류 결과에 따른 콘텐츠 선택
        data = content_data.get(prediction, {
            'images': ["https://via.placeholder.com/300"] * 3,
            'videos': ["https://www.youtube.com/watch?v=3JZ_D3ELwOQ"] * 3,
            'texts': ["기본 텍스트"] * 3
        })
        display_right_content(prediction, data)

