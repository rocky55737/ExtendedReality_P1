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
body.append(para([run("기준일 2026-11-01 · Unreal Engine 5.8.3 · 제출 2026-11-03(동영상)", color="595959", size=20)], after=240))

h1("1. 작품 개요")
p("**스토리**: 메타휴먼 캐릭터가 사우스포 자세에서 점프하고, 공중에서 멈춰 기를 모은 뒤, 떨어지며 앞손 스트레이트를 뻗는다. "
  "주먹에서 공기포가 나가 벽을 무너뜨리고, 카메라가 캐릭터 등 뒤에서 무너진 벽을 바라보며 끝난다.")
p("**영상 길이**: 약 11.6초 (1920×1080, 30fps, 슬로모션 포함), 직접 합성한 효과음 포함")
table(
    ["#", "컷", "시퀀스 프레임", "주요 기술"],
    [
        ["1", "대치 (사우스포 자세)", "0~52", "모캡"],
        ["2", "도약", "52~65", "모캡"],
        ["3", "공중 정지·기 모으기", "65~125", "애니메이션 구간 정지 + Control Rig 떨림"],
        ["4", "착지·스트레이트·충돌", "125~215", "모캡 + 공기포 + Chaos 파괴 + 슬로모션 + 카메라 흔들림"],
        ["5", "마무리", "215~300", "카메라 무빙(등 뒤에서 무너진 벽)"],
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
        ["4. 인버스 리깅", "Control Rig 레이어드 트랙(모캡 위에 동작 겹치기)", "LS_Punch의 MetaHuman_ControlRig 트랙", "일부 완료\n보강 예정"],
        ["5. 피직스·인터랙션", "Chaos Destruction(Geometry Collection) + Field System, 공기포(메시+머티리얼)", "GC_Wall, BP_WallBreaker, AirCannon", "완료"],
    ],
    [2000, 3200, 2526, 1300],
)

h2("2-1. 카메라 모션 캡처")
bullets([
    "**촬영**: 펀치 동작(자세 → 점프 → 착지 → 스트레이트)을 카메라 한 대로 **직접 촬영**했다(교수님 답변: 직접 촬영한 영상만 인정).",
    "**가져오기**: Live Link Hub → Capture Manager → Mono Video Ingest로 영상을 캡처 데이터 에셋 `CD_punch_1`로 가져왔다.",
    "**솔브**: MetaHuman Performance 에셋 `MHP_punch`에서 Body Tracking만 켜고(Facial Tracking 끔, Head Movement Mode Disable) 처리했다. 마커나 수트 없이 영상만으로 전신 동작을 뽑는 **마커리스 모캡**이다(MetaHumanBodyTracker 플러그인).",
    "**내보내기**: Performer Skeleton으로 애니메이션 `AS_MHP_punch`를 만들었다. Manny 스켈레톤으로 바로 내보내면 척추·목 본 구성이 달라 본 누락 경고가 나서 이 방식을 택했다.",
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
    ],
    "**슬로모션**: Slomo(Time Dilation) 트랙으로 충돌 구간(180~215)을 0.35배로 늦췄다.",
    "**카메라**: CineCamera 5대 + Camera Cut 트랙으로 컷을 구성했다(대치 20mm 정면 대각선, 도약 측면 로우앵글, 공중 기 모으기 35mm 반원 궤도, 스트레이트~충돌 20mm 측면, 마무리 24mm 등 뒤에서 상승).",
    "**카메라 흔들림**: 충돌 순간(184~200프레임) 카메라 위치·회전에 점점 줄어드는 진동 키를 넣었다.",
    "**영상용 게임 모드**: 템플릿 게임 모드가 플레이 시 기본 캐릭터(Manny)를 생성하지 않도록 Pawn·HUD가 없는 `BP_CinematicGameMode`를 만들어 적용했다.",
])

h2("2-4. 인버스 리깅 (Control Rig)")
p("교수님 답변에 따르면 \"인버스 리깅\"은 IK가 아니라, **애니메이션을 리깅으로 재구현하고 동작을 추가하는 인터랙션**을 뜻한다. "
  "모캡 애니메이션 위에 메타휴먼 Control Rig를 **레이어드(가산) 트랙**으로 얹어 모캡에 없는 동작을 더하는 방식으로 진행한다.")
table(
    ["구간", "리깅으로 추가한 동작", "상태"],
    [
        ["65~122 공중", "4cm 떠오르기 + 몸통·가슴·양 주먹·머리가 점점 세게 떨림(기 모으기)", "완료"],
        ["65~125 공중", "두 주먹을 허리 옆으로 끌어당겨 모으는 자세", "예정"],
        ["177~200 발사", "공기포 반작용으로 몸이 30~40cm 뒤로 밀리고 상체가 젖혀지는 반동", "예정"],
        ["215~300 마무리", "주먹을 거두고 숨을 고르며 바로 서기", "예정"],
    ],
    [2000, 5726, 1300],
)
bullets([
    "펀치는 스트레이트라서 펀치 자세 과장 대신 **반작용으로 밀려나는 동작**을 택했다.",
    "영상 끝에 **직접 촬영한 원본 영상과 최종본을 나란히 비교**하는 장면을 넣어, 리깅으로 더한 동작이 드러나게 할 예정이다.",
])

h2("2-5. 피직스 + 동작 시뮬레이션 / 인터랙션")
bullets([
    "**벽 파괴 (Chaos Destruction)**: 벽(4m×0.3m×3m)을 Fracture 모드에서 Geometry Collection `GC_Wall`로 바꾸고 Uniform Voronoi로 48조각으로 분할했다.",
    "**파괴 트리거 (Field System)**: `BP_WallBreaker`(FieldSystemActor)가 정해진 시간에 External Cluster Strain(RadialFalloff)으로 조각을 분리하고, Linear Velocity(RadialVector, 900cm/s)로 벽 뒤쪽으로 날린다.",
    "**공기포**: 반투명·Unlit 머티리얼 `M_AirCannon`(Fresnel로 가장자리만 하늘색으로 빛남)을 구체에 입혔다. 시퀀서 Transform 키로 주먹 앞에서 생겨 벽까지 날아가 벽 면에 퍼지고 사라지게 했다.",
    "**타이밍 맞추기**: 공기포가 벽에 닿는 순간 벽이 부서지도록 맞췄다. 렌더링(MRQ)에서는 타이머가 플레이 때보다 약 0.25초 일찍 동작해서 렌더 결과를 보고 트리거 시간을 6.38초로 조정했다.",
])

h1("3. 그 밖의 품질 요소")
table(
    ["항목", "내용"],
    [
        ["환경", "템플릿 배경 메시 40개를 숨기고, 월드 좌표 노이즈 기반 콘크리트 머티리얼 `M_Concrete`(인스턴스: 발판·바닥·벽)를 만들었다. 바닥을 넓히고 안개로 지평선을 정리했다."],
        ["렌더링", "Movie Render Queue: 1920×1080 PNG, Temporal Sample 8(모션 블러·안티에일리어싱), Warm-up 0. 슬로모션이 반영된 348프레임"],
        ["사운드", "원곡·외부 음원 없이 Python(numpy)으로 효과음을 직접 합성했다: 바람, 도약, 기 모으기 드론, 착지, 발사, 폭발, 파편. 슬로모션을 반영한 영상 시간에 맞춰 배치했다."],
        ["편집", "ffmpeg로 PNG 시퀀스와 효과음을 H.264/AAC MP4로 합쳤다."],
    ],
    [1600, 7426],
)

h1("4. Claude Code + Unreal MCP 활용")
p("교수님 권장에 따라 Claude Code를 Unreal 에디터의 MCP 서버에 연결해 작업 대부분을 자동화했다.")
table(
    ["MCP로 한 작업", "UI에서 직접 한 작업 (MCP 미지원)"],
    [
        ["액터 배치·트랜스폼, 시퀀스 트랙·섹션·키프레임, 카메라 컷, Control Rig 레이어드 키, 머티리얼 그래프 생성, Field System 블루프린트 노드 구성, Simulate 실행·뷰포트 캡처로 결과 검증, 저장",
         "영상 가져오기(Live Link Hub), MetaHuman Performance 처리, 메타휴먼 생성·Assemble, 리타게터 생성, Fracture(벽 분할), Movie Render Queue 실행"],
    ],
    [4513, 4513],
)

h1("5. 남은 작업")
bullets([
    "리깅 보강: 기 모으기 자세 → 반동 → 마무리 동작 (2-4 표의 \"예정\")",
    "다시 렌더링 → 효과음 합치기 → 촬영 원본과 최종본 비교 장면 추가",
    "교수님께 리깅 방향 확인 질문 (v1 영상 첨부)",
    "2026-11-03 동영상 제출",
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
