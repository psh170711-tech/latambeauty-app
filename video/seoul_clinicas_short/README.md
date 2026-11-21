# 서울 성형 쇼츠: "Clínicas en Seúl" (스페인어, 약 49초)

- 결과물: `out/seoul_clinicas_short.mp4` (1080x1920, 30fps, H.264/AAC, -14 LUFS)
- 자막 파일: `out/seoul_clinicas_short.srt` (유튜브에 따로 올리는 스페인어 자막)
- 음성: Higgsfield `seed_audio`, 프리셋 목소리 "Marisol". 원본은 장면별 `audio_raw/`, 다듬은 버전은 `audio/`

## 장면 구성

| # | 시간 | 화면 | 내레이션 (ES) | 뜻 (KO) |
|---|------|------|---------------|---------|
| 1 | 0–5s | 훅 "ESPERA." | ¿Vienes a Seúl para una cirugía? Espera. Esto nadie te lo dice. | 서울에 수술하러 와? 잠깐, 이건 아무도 안 알려줘. |
| 2 | 5–15s | 지역 카드 (성형 / 피부) | La zona de las clínicas es Gangnam: Sinsa, Apgujeong y la estación de Gangnam. Para tratamientos de piel, mucha gente va a Myeongdong o Cheongdam. | 성형은 강남(신사·압구정·강남역), 피부 시술은 명동·청담 |
| 3 | 15–24s | ⚠ 공장형 병원, 환자 아이콘, 줄어드는 진료 시간 막대 | Pero ojo: hay clínicas enormes que los coreanos llaman «fábricas»… | 한국인이 '공장'이라 부르는 대형 병원 주의 |
| 4 | 24–38s | 팁 카드 1·2·3 | Uno… Dos… Tres… | 집도의 직접 상담 / 당일 결제 압박 거절 / 실사진 후기 |
| 5 | 38–49s | CTA "Comenta CLÍNICA" + 고지 문구 | Comenta CLÍNICA y te paso mi checklist en español… | 체크리스트 + 정부 등록 병원 확인법 |

마지막 화면에는 "Información general · No es consejo médico"(일반 정보이며 의료 조언이 아님) 문구를 넣었습니다.
화면에도, 내레이션에도 특정 병원 이름은 나오지 않습니다.

## 다시 렌더링하기

```bash
apt-get install -y fonts-montserrat      # 영상에 쓰는 폰트
python3 prep_audio.py .                  # audio_raw/ → audio/ (긴 공백 줄이기, 팁 1~3 합치기)
python3 render.py .                      # → out/seoul_clinicas_short.mp4 + .srt
python3 render.py . --still 2.7,20,45    # 지정한 시간의 프레임을 PNG로 미리보기
```

문구를 바꾸려면 `render.py`의 `SCENES`(자막 덩어리)와 각 `sceneN()` 함수(화면 그래픽)를 고치면 됩니다.
음성을 새로 만들었다면 `CUES`(자막 시작 시각)도 새 음성에 맞춰 다시 맞춰야 합니다.
