"""과제 1 기술 요소 정리 문서(.docx) 생성. 외부 라이브러리 없이 OOXML을 직접 쓴다.
사용: python make_tech_doc.py <출력.docx>
"""
import sys
import zipfile
from xml.sax.saxutils import escape

FONT = "맑은 고딕"
ACCENT = "1F4E79"
HEAD_FILL = "DCE6F1"

body = []


def run(text, bold=False, color=None, size=None):
    rpr = ""
    if bold:
        rpr += "<w:b/>"
    if color:
        rpr += f'<w:color w:val="{color}"/>'
    if size:
        rpr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    return f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def rich(text):
    """**굵게** 표기를 run 목록으로 바꾼다."""
    parts = text.replace("`", "").split("**")
    return "".join(run(p, bold=(i % 2 == 1)) for i, p in enumerate(parts) if p)


def para(text, style=None, after=None, align=None):
    ppr = ""
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if after is not None:
        ppr += f'<w:spacing w:after="{after}"/>'
    if align:
        ppr += f'<w:jc w:val="{align}"/>'
    return f"<w:p><w:pPr>{ppr}</w:pPr>{rich(text) if isinstance(text, str) else ''.join(text)}</w:p>"


def h1(t):
    body.append(para(t, "Heading1"))


def h2(t):
    body.append(para(t, "Heading2"))


def p(t):
    body.append(para(t))


def bullets(items, level=0):
    for it in items:
        if isinstance(it, list):
            bullets(it, level + 1)
            continue
        body.append(
            f'<w:p><w:pPr><w:pStyle w:val="ListParagraph"/><w:numPr><w:ilvl w:val="{level}"/>'
            f'<w:numId w:val="1"/></w:numPr><w:spacing w:after="40"/></w:pPr>{rich(it)}</w:p>'
        )


def table(header, rows, widths):
    total = sum(widths)
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)

    def cell(text, w, head=False):
        shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{HEAD_FILL}"/>' if head else ""
        paras = text.split("\n")
        content = "".join(
            f'<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>{run(x, bold=True) if head else rich(x)}</w:p>' for x in paras
        )
        return (
            f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{shd}'
            f'<w:tcMar><w:top w:w="60" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/>'
            f'<w:left w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tcMar></w:tcPr>{content}</w:tc>'
        )

    trs = "<w:tr><w:trPr><w:tblHeader/></w:trPr>" + "".join(cell(h, w, True) for h, w in zip(header, widths)) + "</w:tr>"
    for r in rows:
        trs += "<w:tr><w:trPr><w:cantSplit/></w:trPr>" + "".join(cell(c, w) for c, w in zip(r, widths)) + "</w:tr>"
    b = '<w:top w:val="single" w:sz="4" w:color="A6A6A6"/><w:left w:val="single" w:sz="4" w:color="A6A6A6"/>' \
        '<w:bottom w:val="single" w:sz="4" w:color="A6A6A6"/><w:right w:val="single" w:sz="4" w:color="A6A6A6"/>' \
        '<w:insideH w:val="single" w:sz="4" w:color="A6A6A6"/><w:insideV w:val="single" w:sz="4" w:color="A6A6A6"/>'
    body.append(
        f'<w:tbl><w:tblPr><w:tblW w:w="{total}" w:type="dxa"/><w:tblBorders>{b}</w:tblBorders>'
        f'<w:tblLayout w:type="fixed"/></w:tblPr><w:tblGrid>{grid}</w:tblGrid>{trs}</w:tbl>'
    )
    body.append(para("", after=120))


# ---------------------------------------------------------------- 본문
body.append(para([run("Extended Reality 과제 1", bold=True, color=ACCENT, size=40)], after=60))
body.append(para([run("나만의 애니메이션 리깅 캐릭터 인터랙션 스토리 — 기술 요소 정리", bold=True, size=26)], after=60))
body.append(para([run("기준일 2026-11-06 · Unreal Engine 5.8.3 · 제출 2026-11-03(클라이맥스), 재제출 2026-11-04(확장판 「갇힌 남자」)", color="595959", size=20)], after=240))

h1("1. 작품 개요")
p("**확장판 「갇힌 남자」(「올드보이」 오마주, 3분 22초)**: 어느 날 밀실에서 깨어난 남자가 15년 동안 배식구로 들어오는 군만두만 먹으며 벽에 날짜(X)를 긋는다. "
  "처음 벽을 쳤을 때는 손만 아프지만, TV 앞에서 섀도복싱으로 몸을 만든 끝에 주먹에서 공기포를 쏘아 벽을 부순다. 마지막에는 양팔을 닭처럼 파닥이며 구멍으로 날아 나간다. "
  "\"3~5분 분량의 스토리텔링\" 조건에 맞춰, 처음 제출한 11초 클라이맥스(아래)를 6막으로 쓰고 앞뒤 이야기를 새로 만들었다. 원작 영상·음악은 쓰지 않고 설정만 빌렸다.")
table(
    ["막", "내용", "시간", "주요 기술"],
    [
        ["0", "제목 카드", "0:00~0:07", "ffmpeg drawtext"],
        ["1", "갇힘: 깨어나 뒤척이고 일어나 문을 두드림", "0:07~0:45", "모캡(깨어나기·문 두드리기) + 액터 회전 키로 누운 자세"],
        ["2", "군만두: 배식구로 쟁반이 들어오고 손으로 먹음", "0:45~1:00", "모캡(먹기) + 쟁반 Attach 트랙(hand_l 소켓)"],
        ["3", "세월: 벽에 X를 그음(1일째 → 100일째 → 1년째…)", "1:00~1:18", "모캡(긋기) + Scale 키로 획이 그려지는 X 액터 18개"],
        ["4", "첫 실패: 벽을 쳤다가 손이 아파 움켜쥠", "1:18~1:32", "모캡(펀치 실패)"],
        ["5", "수련: 섀도복싱·먹기·긋기를 섞어 반복(3년째 → 15년째)", "1:32~2:58", "모캡(섀도복싱), 반복마다 다른 카메라 앵글, 결심 얼굴 클로즈업"],
        ["6", "각성: 클라이맥스(공중 정지·공기포·벽 붕괴)", "2:58~3:10", "리깅 가산 레이어 + Chaos Destruction + 슬로모션"],
        ["7", "탈출: 닭처럼 파닥이며 구멍으로 날아 나감", "3:10~3:14", "Control Rig 가산 키로 비행 경로·날갯짓을 새로 만듦"],
        ["8", "THE END 카드", "3:14~3:22", "ffmpeg drawtext"],
    ],
    [400, 3700, 1300, 3626],
)
h2("클라이맥스 (첫 제출본, 11.6초)")
p("**스토리**: 메타휴먼 캐릭터가 사우스포 자세에서 점프하고, 공중에서 멈춰 양팔을 펼치고 파닥이며 기를 모은 뒤, 떨어지며 앞손 스트레이트를 뻗는다. "
  "주먹에서 공기포가 나가는 순간 그 반작용으로 몸이 뒤로 크게 밀려나고, 공기포가 벽을 무너뜨린다. "
  "마지막에 가드를 풀고 숨을 고르며, 카메라가 캐릭터 등 뒤에서 무너진 벽을 바라본다.")
p("**제출 영상**: 약 23초 = 본편 11.6초 + 비교 장면 11.6초 (1920×1080, 30fps, 슬로모션 포함, 직접 합성한 효과음 포함). "
  "비교 장면에서는 직접 촬영한 원본과 최종본을 나란히 재생한다.")
table(
    ["#", "컷", "시퀀스 프레임", "주요 기술"],
    [
        ["1", "대치 (사우스포 자세)", "0~52", "모캡(리깅으로 베이크)"],
        ["2", "도약", "52~65", "모캡(리깅으로 베이크)"],
        ["3", "공중 정지·기 모으기", "65~125", "모캡 구간 정지 + 리깅: 떠오르기, 양팔 펴고 파닥이기"],
        ["4", "착지·스트레이트·충돌", "125~215", "모캡 + 리깅: 공기포 반동(88cm) + 공기포 + Chaos 파괴 + 슬로모션 + 카메라 흔들림"],
        ["5", "마무리", "215~300", "리깅: 가드 풀고 팔 내리며 일어서기 + 카메라 무빙"],
    ],
    [500, 2600, 1600, 4326],
)

h1("2. 과제 명시 사항별 기술 요소")
table(
    ["과제 명시 사항", "사용한 기술", "결과물(에셋)", "상태"],
    [
        ["1. 카메라 모션 캡처", "직접 촬영한 단안 영상 → MetaHuman Animator 마커리스 바디 트래킹", "CD_punch_1 → MHP_punch → AS_MHP_punch", "완료"],
        ["2. 3D 캐릭터 디자인", "MetaHuman Creator(엔진 내) + Assemble", "MH_Puncher → BP_Puncher", "완료"],
        ["3. 리타게팅·\n애니메이션 구성", "IK Rig / IK Retargeter, Level Sequence(구간 편집·슬로모션·카메라)", "AS_MHP_punch_Puncher, LS_Punch", "완료"],
        ["4. 인버스 리깅", "모캡 키프레임을 MetaHuman Control Rig로 베이크 + 가산 섹션에 리깅 동작 추가", "AS_Punch_Sequenced → LS_Punch의 MetaHuman_ControlRig 트랙", "완료"],
        ["5. 피직스·인터랙션", "Chaos Destruction(Geometry Collection) + Field System, 공기포(메시+머티리얼), 반작용 반동", "GC_Wall, BP_WallBreaker(Spawnable), AirCannon", "완료"],
    ],
    [2000, 3200, 2526, 1300],
)

h2("2-1. 카메라 모션 캡처")
bullets([
    "**촬영**: 펀치 동작(자세 → 점프 → 착지 → 스트레이트)을 카메라 한 대로 **직접 촬영**했다(교수님 답변: 직접 촬영한 영상만 인정).",
    "**가져오기**: Live Link Hub → Capture Manager → Mono Video Ingest로 영상을 캡처 데이터 에셋 `CD_punch_1`로 가져왔다.",
    "**솔브**: MetaHuman Performance 에셋 `MHP_punch`에서 Body Tracking만 켜고(Facial Tracking 끔, Head Movement Mode Disable) 처리했다. 마커나 수트 없이 영상만으로 전신 동작을 뽑는 **마커리스 모캡**이다(MetaHumanBodyTracker 플러그인).",
    "**내보내기**: Performer Skeleton으로 애니메이션 `AS_MHP_punch`를 만들었다. Manny 스켈레톤으로 바로 내보내면 척추·목 본 구성이 달라 본 누락 경고가 나서 이 방식을 택했다.",
    "**확장판 촬영 (2026-11-03)**: 방 장면용으로 6개를 더 직접 촬영했다: 깨어나기(18초), 문 두드리기(6초), 바닥에 앉아 손으로 먹기(14.5초), 벽에 X 긋기(8.6초), 펀치 실패 후 손 아파하기(14.4초), 섀도복싱(8.1초). 펀치까지 합쳐 **모캡 클립 7개**다.",
    "**HDR 문제**: 아이폰 영상은 HLG HDR 10비트라 Live Link Hub에서 오류가 났다. ffmpeg로 톤매핑해 8비트 SDR·59.94fps 고정·소리 없음으로 다시 인코딩한 뒤 가져왔다. 같은 이름으로 실패한 에셋이 남아 있으면 다시 가져오기도 실패해서 이름을 바꿨다.",
    "**사전 테스트**: 본 촬영 전에 댄스 영상으로 \"영상 → 모캡 → 기본 마네킹(Manny)\" 파이프라인 전체를 검증했다(제출물에는 쓰지 않음).",
])

h2("2-2. 3D 캐릭터 디자인 (메타휴먼)")
bullets([
    "UE 5.8 엔진 안의 **MetaHuman Creator**로 프리셋을 기반으로 캐릭터 `MH_Puncher`를 만들었다.",
    "**Assemble**(UE Cinematic 품질)로 시네마틱용 블루프린트 `BP_Puncher`(Body·Face·헤어 그룸 포함)를 생성했다.",
    "레벨 `Lvl_ThirdPerson`에 배치(위치 (0, 0, 211.67), yaw −90)하고, 펀치가 벽 정면을 향하도록 맞췄다.",
])

h2("2-3. 리타게팅 및 애니메이션 구성")
bullets([
    "**리타게팅**: Retarget Animations로 IK Rig와 IK Retargeter를 자동 생성해 Performer Skeleton 애니메이션을 메타휴먼 바디(`SKM_MH_Puncher_BodyMesh`)로 옮겼다 → `AS_MHP_punch_Puncher`.",
    "**시퀀스 구성**: Level Sequence `LS_Punch`(30fps, 0~300프레임)에서 애니메이션 트랙을 세 구간으로 나눴다.",
    [
        "0~65: 모캡 그대로 (자세 → 점프)",
        "65~125: 모캡의 점프 최고점(65프레임) 자세에서 정지 → **공중 정지** 연출",
        "125~212: 모캡 65프레임부터 이어서 재생 (착지 → 스트레이트), 이후 마지막 자세 유지",
        "이렇게 편집한 결과를 애니메이션 하나로 내보내 Control Rig에 베이크했다(2-4).",
    ],
    "**슬로모션**: Slomo(Time Dilation) 트랙으로 충돌 구간(180~215)을 0.35배로 늦췄다.",
    "**카메라**: CineCamera 5대 + Camera Cut 트랙으로 컷을 구성했다(대치 20mm 정면 대각선, 도약 측면 로우앵글, 공중 기 모으기 35mm 반원 궤도, 스트레이트~충돌 20mm 측면, 마무리 24mm 등 뒤에서 상승).",
    "**카메라 흔들림**: 충돌 순간(184~200프레임) 카메라 위치·회전에 점점 줄어드는 진동 키를 넣었다. 반동으로 밀려난 캐릭터가 화면에 들어오도록 Cam4를 45cm 옮겼다.",
    "**확장판 방 장면 `LS_Room`** (30fps, 0~5127프레임, 170.9초): 모캡 클립 6개를 스켈레탈 애니메이션 트랙에 이어 붙이고(섞어서 반복), 장면마다 캐릭터 액터의 위치·방향을 키로 옮겼다. Spawnable CineCamera 한 대에 막마다 시작·끝 키를 넣어 컷 20여 개를 만들었다(막 사이 1프레임 차이로 컷이 됨, 초점 거리도 키).",
    [
        "**누운 자세**: 단안 모캡이 바닥에 누운 자세를 풀지 못해 거의 선 자세로 나왔다. 곧게 선 프레임 하나만 반복 재생하고 액터를 회전 키(−103°)로 눕혀 뒤척이게 한 뒤, 카메라 컷과 동시에 원래 모캡(일어나 앉기)으로 넘겼다.",
        "**쟁반**: 배식구로 밀려 들어오는 쟁반(Transform 키)과 손에 드는 쟁반(`MovieScene3DAttachTrack`, Body의 `hand_l` 소켓)을 별도 액터로 나눴다. MRQ에서는 Attach 트랙이 있는 액터가 붙기 전 구간에서 Transform 키대로 움직이지 않았기 때문이다.",
        "**세월 표현**: 벽의 X 표시는 획마다 얇은 큐브의 Scale·위치 키로 \"그려지게\" 했다(장면마다 한 줄 3개, 총 3줄). 자막으로 1일째 → 15년째를 알린다.",
    ],
    "**탈출 엔딩 (LS_Punch 300~430)**: 가산 섹션에 `body_ctrl` 위치 키로 웅크렸다가 구멍 쪽으로 8.5m 날아가는 궤적을, 양팔 `upperarm_*_fk_ctrl.Rotation.Y`에 4프레임마다 110°/45°를 번갈아 넣어 닭 날갯짓을 만들었다. 절대 섹션에는 공중 웅크림 자세를 키로 넣어 날아가는 동안 자세를 유지했다.",
    "**영상용 게임 모드**: 템플릿 게임 모드가 플레이 시 기본 캐릭터(Manny)를 생성하지 않도록 Pawn·HUD가 없는 `BP_CinematicGameMode`를 만들어 적용했다.",
])

h2("2-4. 인버스 리깅 (Control Rig)")
p("교수님 답변: \"스켈레톤 키프레임 자체를 인버스 리깅으로 구성하고, 해당 리깅으로 추가적인 동작(물리 효과, 뒤로 밀린다든가, 충격으로 날아간다든가)을 구성하라.\" "
  "그리고 처음에 넣은 기 모으기 떨림은 \"애니메이션 버그로 오해할 수 있으니 불필요해 보인다\"고 하셨다. 이에 맞춰 다음과 같이 구성했다.")
bullets([
    "**1) 키프레임을 리깅으로 구성 (베이크)**: 공중 정지까지 편집된 모캡 동작을 애니메이션 `AS_Punch_Sequenced`로 내보낸 뒤 "
    "`bake_to_control_rig`로 **MetaHuman Control Rig에 베이크**했다. 이제 캐릭터를 움직이는 것은 애니메이션 파일이 아니라 리깅 컨트롤 키다(컨트롤마다 0~300프레임 전부 키).",
    "**2) 리깅으로 동작 추가 (가산 섹션)**: 같은 Control Rig 트랙에 **가산(Additive) 섹션**을 하나 더 만들어, 베이크된 모캡 위에 아래 동작을 더했다. "
    "모캡 레이어와 추가 동작 레이어가 분리되어 있어서 시퀀서에서 구조가 그대로 보인다.",
    "**떨림 제거**: 교수님 피드백대로 떨림 키는 모두 지웠다.",
])
table(
    ["구간", "리깅으로 추가한 동작 (사용한 컨트롤)", "상태"],
    [
        ["65~125 공중", "4cm 떠오르기 (body_ctrl) + **양팔을 옆으로 쫙 펴고 위아래로 파닥이기**. 처음엔 느리고 작게, 점점 빠르고 크게(주기 6→3프레임, 폭 ±18°→±30°) (upperarm·lowerarm FK)", "완료"],
        ["178~215 발사", "**공기포 반작용 반동**: 공기포가 생긴 다음 프레임부터 3프레임 만에 74cm, 최종 88cm 뒤로 밀린다. 발은 1프레임 늦게 바닥을 미끄러지고, 무릎이 굽고 상체가 젖혀졌다가 회복한다 (body_ctrl, foot_l/r_ik_ctrl, spine_03_ctrl)", "완료"],
        ["222~300 마무리", "가드를 풀고 양팔을 내리며 무릎을 펴고 일어서서 숨을 고른다 (upperarm·lowerarm, body_ctrl, spine_03_ctrl)", "완료"],
    ],
    [1700, 6026, 1300],
)
bullets([
    "펀치는 스트레이트라서 펀치 자세 과장 대신 **반작용으로 밀려나는 물리적 반응**을 택했다.",
    "각 컨트롤의 축은 Simulate 중 뷰포트 캡처로 하나씩 시험해서 찾았다. 예를 들어 왼발·오른발 IK 컨트롤은 좌우 대칭이라 같은 방향으로 밀려면 부호가 반대다.",
    "처음에는 기 모으기를 가라데 준비자세(주먹을 골반에)로 하려 했다. 하지만 팔꿈치·손목을 키로 정밀하게 맞추기 어려워서, 크고 분명하게 보이는 파닥이기 동작으로 바꿨다.",
    "제출 영상 끝에 **직접 촬영한 원본과 최종본을 나란히 재생**한다. 점프 꼭대기를 맞춰 동시에 재생하므로, 원본은 바로 착지하는데 최종본은 공중에서 파닥이고, 반동하고, 마무리하는 차이가 드러난다.",
])

h2("2-5. 피직스 + 동작 시뮬레이션 / 인터랙션")
bullets([
    "**벽 파괴 (Chaos Destruction)**: 벽(4m×0.3m×3m)을 Fracture 모드에서 Geometry Collection `GC_Wall`로 바꾸고 Uniform Voronoi로 48조각으로 분할했다.",
    "**파괴 트리거 (Field System)**: `BP_WallBreaker`(FieldSystemActor)가 생성되면 External Cluster Strain(RadialFalloff)으로 조각을 분리하고, Linear Velocity(RadialVector, 900cm/s)로 벽 뒤쪽으로 날린다.",
    "**공기포**: 반투명·Unlit 머티리얼 `M_AirCannon`(Fresnel로 가장자리만 하늘색으로 빛남)을 구체에 입혔다. 시퀀서 Transform 키로 주먹 앞에서 생겨 벽까지 날아가 벽 면에 퍼지고 사라지게 했다.",
    "**타이밍 맞추기**: 처음에는 \"시작 후 N초\" 타이머로 벽을 부쉈다. 그런데 플레이와 렌더링(MRQ)에서 0.25초 어긋났다. 그래서 WallBreaker를 시퀀스의 **Spawnable**로 바꿔, 타임라인 184프레임(공기포가 벽 면에 퍼지는 순간)에 생성되어 바로 터지게 했다. 이제 플레이와 렌더 모두 같은 프레임에 부서진다.",
    "**작용·반작용**: 공기포가 벽을 부수는 작용과 동시에, 캐릭터는 리깅으로 만든 반동(2-4)으로 반대 방향으로 밀려난다.",
])

h1("3. 그 밖의 품질 요소")
table(
    ["항목", "내용"],
    [
        ["환경", "템플릿 배경 메시 40개를 숨기고, 월드 좌표 노이즈 기반 콘크리트 머티리얼 `M_Concrete`(인스턴스: 발판·바닥·벽)를 만들었다. 바닥을 넓히고 안개로 지평선을 정리했다."],
        ["밀실 세트", "침대·TV(Time→Sine으로 깜빡이는 Unlit 화면 + 푸른 RectLight)·문과 배식구·식탁·의자, 천장 전구 하나(3000K). 노출을 EV 0으로 고정해 어두운 방을 유지했다. 벽이 부서지면 바깥 햇빛이 구멍으로 들어오고 조각이 역광 실루엣이 되도록 태양 방향을 맞췄다."],
        ["렌더링", "Movie Render Queue: 1920×1080 PNG, Temporal Sample 8(모션 블러·안티에일리어싱). LS_Room 5127프레임 + LS_Punch 478프레임(슬로모션·탈출 포함)"],
        ["사운드", "원곡·외부 음원 없이 Python(numpy)으로 효과음을 직접 합성했다: 바람, 도약, 기 모으기 드론, 착지, 발사, 폭발, 파편. 슬로모션을 반영한 영상 시간에 맞춰 배치했다."],
        ["확장판 편집", "`Tools/story/make_story.py` 하나로 방 효과음(방 울림·TV 웅웅·쟁반 밀림·날짜 바뀔 때 쉭) 합성, 자막·대사, 계왕권(鷄王拳) 자막, 제목·엔딩 카드, 이어 붙이기까지 한 번에 한다."],
        ["편집", "ffmpeg로 PNG 시퀀스와 효과음을 H.264/AAC MP4로 합쳤다. 비교 장면(원본 세로 영상 | 최종본, 자막 포함)도 ffmpeg 필터로 만들어 본편 뒤에 붙였다."],
    ],
    [1600, 7426],
)

h1("4. Claude Code + Unreal MCP 활용")
p("교수님 권장에 따라 Claude Code를 Unreal 에디터의 MCP 서버에 연결해 작업 대부분을 자동화했다.")
table(
    ["MCP로 한 작업", "UI에서 직접 한 작업 (MCP 미지원)"],
    [
        ["액터 배치·트랜스폼, 시퀀스 트랙·섹션·키프레임, 카메라 컷, 애니메이션 내보내기와 Control Rig 베이크, 리깅 가산 키, Spawnable 바인딩, 머티리얼 그래프 생성, Field System 블루프린트 노드 구성, Simulate 실행·뷰포트 캡처로 결과 검증, 저장",
         "영상 가져오기(Live Link Hub), MetaHuman Performance 처리, 메타휴먼 생성·Assemble, 리타게터 생성, Fracture(벽 분할), Movie Render Queue 실행"],
    ],
    [4513, 4513],
)

h1("5. 결과물")
bullets([
    "재제출 영상(확장판) `Oldboy_v1.mp4` (3분 22초, 11/4 마감 전 제출). 마감 뒤 쟁반 장면·대사 자막을 고친 `Oldboy_submit.mp4`",
    "첫 제출 영상 `LS_Punch_submit.mp4` (약 23초) = 본편 `LS_Punch_final.mp4` + 비교 장면 `LS_Punch_compare.mp4`",
    "재현 스크립트: `Tools/story/make_story.py`(확장판 최종 편집), `Tools/sfx/make_sfx.py`(효과음), `Tools/sfx/mux.sh`(PNG+소리→MP4), `Tools/sfx/make_compare.sh`(비교 장면·제출본), `Docs/make_tech_doc.py`(이 문서)",
    "작업 과정 기록: GitHub 저장소 이슈 #1~#7, `CLAUDE.md`",
])

# ---------------------------------------------------------------- 패키지
W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
R = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'

document = (
    f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {W} {R}><w:body>'
    + "".join(body)
    + '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
    '<w:pgMar w:top="1300" w:right="1440" w:bottom="1300" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>'
    "</w:sectPr></w:body></w:document>"
)

fonts = f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:eastAsia="{FONT}" w:cs="{FONT}"/>'
styles = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles {W}>
<w:docDefaults><w:rPrDefault><w:rPr>{fonts}<w:sz w:val="20"/><w:szCs w:val="20"/><w:lang w:val="ko-KR" w:eastAsia="ko-KR"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="100" w:line="300" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>
<w:pPr><w:keepNext/><w:spacing w:before="320" w:after="140"/><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="2" w:color="{ACCENT}"/></w:pBdr><w:outlineLvl w:val="0"/></w:pPr>
<w:rPr><w:b/><w:color w:val="{ACCENT}"/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>
<w:pPr><w:keepNext/><w:spacing w:before="220" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr>
<w:rPr><w:b/><w:color w:val="{ACCENT}"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/></w:style>
<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/><w:tblPr><w:tblCellMar><w:left w:w="108" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>
</w:styles>"""

levels = "".join(
    f'<w:lvl w:ilvl="{i}"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="{c}"/><w:lvlJc w:val="left"/>'
    f'<w:pPr><w:ind w:left="{360 + 360 * i}" w:hanging="260"/></w:pPr></w:lvl>'
    for i, c in enumerate(["•", "–", "▪"])
)
numbering = (
    f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering {W}>'
    f'<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/>{levels}</w:abstractNum>'
    '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>'
)

content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>"""
rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""
doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>"""

out = sys.argv[1] if len(sys.argv) > 1 else "과제1_기술요소정리.docx"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", document)
    z.writestr("word/styles.xml", styles)
    z.writestr("word/numbering.xml", numbering)
    z.writestr("word/_rels/document.xml.rels", doc_rels)
print("wrote", out)
