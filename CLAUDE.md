# ExtendedReality_P1

대학 Extended Reality 수업 Project1. Unreal Engine 5.8 프로젝트이며, 노트북과 데스크톱을 오가며 작업한다.

## 과제 1 스펙

아래 과정을 모두 거쳐 "나만의 애니메이션 리깅 캐릭터 인터랙션 스토리"를 만든다. 제출물은 **동영상(2026-11-03)**이다.

1. 카메라 모션 캡처
2. 3D 캐릭터 디자인 (메타휴먼)
3. 리타게팅 및 애니메이션 구성
4. 인버스 리깅
5. 피직스 + 동작 시뮬레이션/인터랙션 (스토리텔링)

- 각 기술 요소는 강의 시간에 다룰 예정이다.
- 교수님이 MCP(Claude Code ↔ 에디터) 활용을 적극 권장했다. 그만큼 **높은 수준의 퀄리티를 요구한다.**
- 마커리스 모캡 참고 영상(https://youtu.be/o9u99mIWits)은 교수님이 과제 참고 자료로 준 것이다.

## 프로젝트 구조

- `Project1/Project1.uproject`: UE 5.8 프로젝트 파일. Third Person 템플릿 기반의 Blueprint 전용 프로젝트이며 C++ `Source/` 폴더는 없다.
- `Project1/Content/`: 에셋 (`ThirdPerson`, `Characters`, `Input`, `LevelPrototyping` 등)
- `Project1/Config/`: 프로젝트 설정
- 활성 플러그인: ModelingToolsEditorMode, GameplayStateTree, ModelContextProtocol, ToolsetRegistry, EditorToolset, AnimationAssistantToolset, PhysicsToolsets, MetaHumanCharacter, MetaHumanGenerator, MetaHumanBodyTracker(마커리스 모캡)
- 엔진 버전: UE 5.8.3. MetaHumanBodyTracker 플러그인은 Fab에서 받는 엔진 플러그인이라 git으로 넘어가지 않는다. PC마다 Epic 런처에서 "MetaHuman Animator Markerless Motion Capture Plugin"을 엔진에 설치해야 한다. 런처가 엔진을 업데이트하는 중에는 에디터를 켜지 않는다.

## Git / LFS

- 원격 저장소: https://github.com/rocky55737/ExtendedReality_P1 (기본 브랜치 `main`)
- `.uasset`, `.umap`, `.fbx`, `.png`, `.wav`, `.mp4` 파일은 Git LFS로 관리한다. 클론하기 전에 `git lfs install`을 먼저 실행한다.
- `Binaries/`, `DerivedDataCache/`, `Intermediate/`, `Saved/`, `*_BuiltData.uasset` 파일은 커밋하지 않는다.
- `Content/MetaHumans/` 폴더는 용량이 커서 git에서 제외했다. 다른 PC에서는 MetaHuman 에셋을 다시 받거나 다시 만들어야 한다.
- `Content/CaptureManager/` 폴더(Live Link Hub로 가져온 촬영 영상)도 git에서 제외했다. 용량이 크고 저작권 영상이 섞일 수 있기 때문이다. 다른 PC에서는 원본 영상으로 다시 가져온다.

## Unreal MCP (Claude Code ↔ 에디터)

- 저장소 루트의 `.mcp.json`과 `Project1/.mcp.json`에 `unreal` MCP 서버(`http://127.0.0.1:8000/mcp`)가 똑같이 설정되어 있다. 설정을 바꿀 때는 두 파일을 함께 수정한다.
- 대화 도중에 에디터를 켰다면 MCP 도구가 보이지 않는다. 이때 `/mcp reconnect unreal`로 다시 연결한다. 원격 화면의 `/mcp` 목록에는 unreal이 안 보일 수 있다.
- 에디터 설정(`Config/DefaultEditorPerProjectUserSettings.ini`)으로 MCP 서버가 에디터 실행 시 포트 8000에서 자동 시작된다.
- MCP 도구는 **Unreal 에디터가 열려 있을 때만** 동작한다. Claude Code는 저장소 루트나 `Project1/` 폴더 중 어디에서 실행해도 된다.

## 작업 규칙

- PC를 바꾸기 전에는 커밋하고 푸시한다. 작업을 시작할 때는 `git pull`을 먼저 한다.
- 에디터가 `.uasset`/`.umap` 파일을 열고 있으면 바이너리 충돌이 날 수 있다. 같은 에셋을 두 PC에서 동시에 수정하지 않는다.

## 진행 상황

- [x] UE5 프로젝트 생성, Git LFS 설정
- [x] Unreal MCP 서버 활성화, Claude Code 연결
- [x] 마커리스 모캡 플러그인 설치 및 프로젝트에서 활성화
- [x] 영상 → 마커리스 모캡 → Manny 리타게팅 파이프라인 테스트 (2026-10-19 데스크톱에서 완료. Manny가 춤 동작을 잘 따라함)
- [x] 캐릭터 결정 (2026-10-20, 이슈 #1 코멘트): 메타휴먼을 메인으로 만든다. 로봇과 동물은 쓰지 않는다.
- [x] 교수님 답변 (2026-10-20, 이슈 #1 질문 목록 코멘트에 기록. 4번 이후는 아직 못 물어봄)
  - 1. 모캡 영상은 **꼭 직접 촬영한 영상**이어야 한다.
  - 2. "인버스 리깅"은 IK가 아니다. 애니메이션을 리깅으로 재구현하고 동작을 추가하는 등의 인터랙션을 하라는 뜻이다.
  - 3. 인터랙션 범위는 스토리에 따라 정한다. 캐릭터 움직임만 보여줘도 되고, 3D 물체와 상호작용해도 된다.
- [x] 스토리 확정 (2026-10-20, 이슈 #1 코멘트): **메타휴먼이 주먹을 내지르면 공기포가 나가서 벽을 무너뜨린다.** 댄스 스토리는 폐기했다. 단계별 계획은 이슈 #2~#7에 있다.
  - 모캡(#2): 자세 → 힘 모으기 → 펀치 → 마무리를 직접 촬영한다.
  - 인버스 리깅(#5): Control Rig에 베이크한 뒤 기 모으기 동작 추가, 펀치 자세 과장, 마무리 동작 추가
  - 피직스(#6): 공기포(Niagara) → 벽 파괴(Chaos Destruction)
  - 소리: 원곡 음원은 쓰지 않는다(무료 효과음).
- [x] 콘티 확정 (2026-10-30, 이슈 #4 코멘트): 사우스포 자세 → 점프 → **공중에서 멈춰 기 모으기** → 착지하며 전진 스트레이트 → 공기포로 벽 파괴 → 마무리 자세. 상대 캐릭터(Manny)는 촬영 시간이 없어서 넣지 않는다.
  1. 대치: 벽 앞 와이드, 사우스포 자세 (모캡)
  2. 도약: 측면 로우앵글, 점프 (모캡)
  3. 공중 정지·기 모으기: 점프 꼭대기에서 멈추고 기를 모은다. 카메라가 캐릭터 주위를 돈다 (리깅으로 추가 + Niagara 기 이펙트)
  4. 착지·스트레이트: 착지 힘으로 전진 스트레이트, 펀치 자세 과장 (모캡 + 리깅)
  5. 공기포·벽 붕괴: 주먹에서 벽을 따라가는 카메라, 슬로모션 (Niagara + Chaos)
  6. 마무리: 무너진 벽 앞에서 마무리 자세 (리깅으로 새로 만듦. 펀치 끝 자세에서 자연스럽게 이어지게)
- [x] 펀치 동작 직접 촬영 → 모캡 (#2, 2026-10-29 노트북): `CD_punch_1` → `MHP_punch` → `AS_MHP_punch`(Performer Skeleton)
- [x] 메타휴먼 캐릭터 (#3, 2026-10-30 노트북): 프리셋 기반 `MH_Puncher` → Assemble(UE Cinematic) → `/Game/MetaHumans/Puncher/BP_Puncher`
- [x] 메타휴먼 리타게팅 (#4 일부, 2026-10-30): `AS_MHP_punch` → `AS_MHP_punch_Puncher`(대상 `SKM_MH_Puncher_BodyMesh`). Simulate로 확인했고 결과가 좋다. `AS_MHP_punch1`은 Manny용 테스트라 쓰지 않는다.
- [x] 시퀀스·벽 배치 (#4 일부, 2026-10-31 노트북): `/Game/Cinematics/LS_Punch`(30fps, 0~152프레임)에 `BP_Puncher` Body → `AS_MHP_punch_Puncher` 트랙. `Lvl_ThirdPerson`에서 `BP_Puncher`는 (0, 0, 211.67) yaw -90, 벽 `Wall_Target`(기본 큐브 4m×0.3m×3m)은 (0, 500, 360), 아웃라이너 `Story` 폴더. 펀치가 벽 정면을 향하는 것을 확인했다.
- [x] 벽 Fracture (#6 일부, 2026-10-31 노트북): `Wall_Target`을 Geometry Collection `/Game/Story/GC_Wall`로 바꾸고 Uniform Voronoi(40~60)로 48조각 분할. 레벨 액터 이름은 `Wall_Target`, 위치 (0, 500, 360), 스케일 1(크기는 지오메트리에 반영됨).
- [x] 벽 붕괴 트리거 (#6 일부, 2026-10-31 노트북): `/Game/Story/BP_WallBreaker`(FieldSystemActor 상속). BeginPlay 뒤 `TriggerTime`초가 지나면 자기 위치에서 External Cluster Strain(RadialFalloff, 1e6, 반경 `BlastRadius`)으로 조각을 분리하고, Linear Velocity(RadialVector, `BlastSpeed`)로 날린다. 레벨 배치 (0, 380, 360), TriggerTime 3.0 / BlastSpeed 900 / BlastRadius 400. `LS_Punch_Player`(LevelSequenceActor, Auto Play)가 Simulate/PIE에서 시퀀스를 자동 재생한다. Simulate에서 벽이 서 있다가 3초에 +Y로 무너지는 것을 확인했다. 위쪽 조각이 높이 뜨는 것은 공기포 이펙트와 함께 다시 조정한다.
- [x] 공기포 (#6, 2026-10-31 노트북): Unreal MCP에 Niagara 도구가 없어서 메시+머티리얼+Sequencer로 만들었다. `/Game/Story/M_AirCannon`(Translucent·Unlit, Fresnel 가장자리만 하늘색으로 빛남)을 기본 구체 `AirCannon`(콜리전·그림자 끔, `Story` 폴더)에 입혔다. `LS_Punch`의 Transform 트랙(완료 모드 KeepState): 117프레임까지 스케일 0 → 118 주먹 앞 생성 → 120 주먹 최대로 뻗음 → 124 벽 표면 도달 → 125 벽 면에 크게 퍼짐 → 127 → 129 스케일 0. 레벨에 놓인 `AirCannon`도 스케일 0, Mobility Movable. `WallBreaker` TriggerTime 4.17초(125프레임). Simulate에서 공기포가 처음과 끝에 보이지 않고, 벽에 닿는 것을 확인했다.
- [x] 공중 정지 (#5 일부, 2026-10-31 노트북): 모캡 `AS_MHP_punch_Puncher`에는 점프가 들어 있다(55 준비, 58 이륙, 65 최고점에서 가장 웅크림, 71 착지, 119 주먹 최대, 120 회수 시작). `LS_Punch` Body 애니메이션 트랙을 세 구간으로 나눴다: 0~65 그대로 / 65~125 모캡 65프레임에서 정지(아주 짧은 구간을 반복 재생) / 125~212 모캡 65부터. 그래서 착지 131, 주먹 최대 179, 공기포 177~188, `WallBreaker` TriggerTime 6.133초(184프레임). 시퀀스 길이 0~212.
- 콘티 변경 (2026-10-31): 사우스포 자세 → 점프 후 공중 정지·기 모으기(카메라 클로즈업 후 복귀) → 떨어지며 앞손 스트레이트 → 공기포·벽 붕괴 → 마무리는 리깅이 아니라 카메라 무빙(뒤에서 벽이 부서진 방향을 봄).
- [x] 기 모으기 떨림 (#5, 2026-10-31): Body에 레이어드 `MetaHuman_ControlRig` 트랙. 72~122에서 몸통·가슴·양 주먹·머리가 점점 세게 떨리고, 65~122에 4cm 떠오른다. 레이어드 리그는 깨끗한 바인딩에서는 애니메이션 트랙 위에 정상으로 얹힌다.
- [x] 카메라 (#4, 2026-10-31): `Story/Cameras` 폴더의 CineCamera 6대(Cam5는 컷에서 빠져 안 쓰임). 컷: Cam1 대치 0~52(정면 대각선 20mm) / Cam2 도약 52~65 / Cam3 공중 기 모으기 65~125(앞쪽 반원 궤도, 35mm) / Cam4 125~215(캐릭터-벽 중앙에서 수직, 20mm, 벽 왼쪽·캐릭터 오른쪽, 스트레이트~충돌) / Cam6 마무리 215~300(캐릭터 등 뒤 약 7m, 24mm, 캐릭터 왼쪽·부서진 벽 오른쪽, 천천히 올라감). 180~215 슬로모션 0.35배. 캐릭터는 212~300 마지막 자세 유지. 캐릭터는 사우스포라 가슴이 +X를 향한다(정면 샷은 +X 쪽에서).
- [x] 매니 제거 (2026-10-31): 원래 게임 모드 `BP_ThirdPersonGameMode`가 플레이·렌더 때 PlayerStart(원점)에 매니를 생성했다. `/Game/Story/BP_CinematicGameMode`(GameModeBase, DefaultPawnClass·HUDClass 없음)를 만들어 `Lvl_ThirdPerson` World Settings의 GameMode로 지정했다. PIE에서 Pawn이 생성되지 않는 것을 확인했다.
- [x] 배경 정리 (#7, 2026-11-01): 사용자 결정으로 낮 조명은 유지한다. 템플릿 메시 40개(경사로·바깥 블록·초록 기둥)는 숨겨서 아웃라이너 `HiddenTemplate` 폴더에 넣었다(컴포넌트 bVisible·액터 bHidden 끔). 캐릭터가 서 있는 중앙 발판(z≈210, `SM_Cylinder`·`SM_QuarterCylinder5~12`·`SM_Cube13~16`)은 남겼다. `/Game/Story/M_Concrete`(월드 좌표 노이즈 2톤)의 인스턴스 `MI_Stage`(발판)·`MI_Ground`(바닥)·`MI_Wall`(벽)을 입혔다. 바닥 `Floor`는 스케일 500으로 넓혔고, 안개는 z 0·밀도 0.035·StartDistance 2000으로 지평선을 가린다.
- [x] 카메라 흔들림 (#7): Cam4 Transform에 184~200프레임 감쇠 진동 키(Z ±7cm, Y ±4cm, 롤·피치 1° 이하)
- [x] 효과음 (#7): `Tools/sfx/make_sfx.py`가 numpy로 직접 합성한다(외부 음원 없음) → `Tools/sfx/LS_Punch_sfx.wav`. Slomo 트랙을 반영해 렌더 영상 기준으로 시간을 맞춘다(전체 11.59초, 도약 1.93, 기 모으기 2.17~4.17, 착지 4.37, 발사 5.90, 충돌 6.22, 슬로모션 끝 8.75). Slomo 키를 바꾸면 스크립트의 `SLOMO_KEYS`도 바꾼다.
- [x] Movie Render Queue 플러그인(`MovieRenderPipeline`)을 uproject에 추가 (에디터 재시작 필요)
- [x] MRQ 렌더 (#7, 2026-11-01): 1080p PNG, 웜업 프레임 0, 템포럴 샘플 8 → `Saved/MovieRenders/LS_Punch.0000~0347.png`(348장, Slomo 반영됨). MRQ에서는 `WallBreaker` 타이머가 PIE보다 약 0.25초 일찍 울려서 TriggerTime을 6.38로 늘렸다(영상 기준. PIE에서는 살짝 늦게 부서져 보이는데, 제출물이 영상이라 그대로 둔다). 새 렌더에서는 공기포가 184~186에 벽에 닿고 189~190에 벽이 부서진다. MRQ에서는 파편이 슬로모션 없이 원래 속도로 날아간다.
- [x] 최종 영상: `bash Tools/sfx/mux.sh Project1/Saved/MovieRenders Project1/Saved/LS_Punch_final.mp4` (ffmpeg는 winget `Gyan.FFmpeg`로 설치함) → 11.6초, H.264 + AAC
- [x] v1 영상 완성 (2026-11-01): 사용자가 "괜찮아 보인다"고 했다. 비교용으로 `Saved/LS_Punch_v1.mp4`에 따로 보관했다(Saved라서 git 제외).
- [x] 교수님 답변 2 (2026-11-01, v1 영상을 보시고, 이슈 #1 코멘트): "스켈레톤 키프레임 자체를 인버스 리깅으로 구성하고, 해당 리깅으로 추가적인 동작(물리 효과, 뒤로 밀린다든가, 충격으로 날아간다든가)을 구성하라." "떨리는 것은 불필요해 보인다(애니메이션 버그로 오해할 수 있음)."
  → 모캡을 애니메이션 트랙으로 재생하지 말고 Control Rig로 베이크해서 리깅이 캐릭터를 움직이게 한다. 그 위에 반동 같은 물리적 반응을 리깅으로 얹는다. **떨림은 뺀다.**
- [ ] 리깅 보강 (2026-11-01 계획, 이슈 #5 코멘트. 교수님 답변 2에 맞춰 수정함): 리깅으로 더한 동작이 눈에 잘 안 띄어서 보강한다. 펀치는 스트레이트라 과장하지 않는다(사용자 결정).
  0. [x] **스켈레톤 키프레임을 리깅으로 구성 (2026-11-01)**: 떨림 키를 모두 지웠다. 공중 정지까지 편집된 동작을 `/Game/Story/Anim/AS_Punch_Sequenced`(59.94fps, 약 10초)로 내보냈다. 시퀀스 표시 프레임레이트를 잠깐 59.94로 바꿔서 내보내고 다시 30으로 돌렸다. 30fps에서는 "호환되지 않는 프레임 레이트" 오류가 난다. Body 애니메이션 트랙은 이 파일 섹션 하나(0~300)로 바꿨고, `bake_to_control_rig`로 MetaHuman_ControlRig 절대 트랙 `MovieSceneControlRigParameterTrack_0`의 `Section_0`에 베이크했다(컨트롤마다 0~300 키 301개). 추가 동작은 같은 트랙의 **가산(Additive) 섹션 `Section_1`**에 키로 넣는다. 같은 리그로 `find_or_create_track(is_layered)`를 부르면 기존 절대 트랙이 돌아와서 레이어 트랙을 따로 만들 수 없다.
  1. [x] **기 모으기 자세 — 팔 펴고 파닥이기 (2026-11-01 밤, 사용자 확인 대기)**: 사용자 제안으로 **공중에서 양팔을 양옆으로 쫙 펴고 위아래로 크게 파닥이며 휘젓는 동작**을 리깅(Section_1 FK 가산)으로 만들었다. 편 자세는 `upperarm_*_fk_ctrl.Rotation.Y` 80, `.Rotation.Z` −20, `lowerarm_*_fk_ctrl.Rotation.Z` −80이다(양쪽 같은 값). 위팔 Y 키: 65:0 → 74:80 → 80:98 → 86:60.5 → 91:101 → 96:57.5 → 101:104 → 105:54.5 → 109:107 → 113:51.5 → 116:110 → 118:80 → 124:0. 주기가 6→3프레임으로 빨라지고 폭이 커진다. 아래팔 Z는 위로 올릴 때 −72, 내릴 때 −82. 위팔 Z는 74~118에서 −20.
     - 사용자 요청 "팔꿈치를 더 활짝": `lowerarm_*_fk_ctrl.Rotation.Z`는 −80 너머(−100/−120/−140)로 가도 변화가 없다(리그 각도 제한으로 보임). **왼팔은 `lowerarm_l_fk_ctrl.Rotation.Y` +45~+65로 거의 일직선이 된다.** 오른팔은 아래팔 Y를 ±로 돌려도 꺾이는 방향만 바뀌고 펴지지 않는다. 위팔 X(비틀기)도 마찬가지다. 공중 구간을 IK로 바꾸고 손을 옆으로 멀리(Z±70) 보내 봤지만 깔끔하게 펴지지 않아서 FK로 되돌렸다. 아직 반영하지 않은 상태다(현재 키는 위 값 그대로). 계획: 65→74 가드에서 팔을 옆으로 폄(`upperarm_*_fk_ctrl.Rotation.Y`+로 들어 올림, `lowerarm_*_fk_ctrl.Rotation.Z`−로 팔꿈치 폄, 양쪽 같은 부호) → 74→118 위아래 ±25° 파닥임, 처음엔 느리게 점점 빠르게(떨림처럼 버그로 보이지 않게 크고 분명하게) → 118→124 가드로 복귀. 이게 안 되면 아래 촬영 안으로 간다.
  1-old. [ ] 기 모으기 자세 — 가라데 준비자세 시도 기록 (보류)
     - 지금 상태: 공중 구간(65~125)에는 **떠오르기만** 있다(Section_1 `body_ctrl.Location.Z` 65:0→100:3→122:4→126:0). 팔 자세 키는 모두 지웠고, 팔 FK/IK 스위치도 전 구간 FK(false)로 되돌렸다. 공중에서는 모캡의 가드 자세 그대로다.
     - 사용자가 원하는 자세: 태권도·가라데 준비자세. **양 주먹을 양 골반 옆에 붙이고, 팔꿈치는 바깥으로 돌아 몸통 뒤로 빠지고, 아래팔은 수평, 손목은 곧게.** (첫 시도처럼 팔을 아래로 뻗은 자세는 아니다.)
     - 손으로 키를 맞추다 멈춘 이유: 몇 시간 동안 시험했지만 팔꿈치 방향·주먹 위치·손목을 동시에 맞추지 못했다. 오른팔은 거의 맞췄는데(IK 손 위치 X−8, Y−36, Z−20, 오른쪽 옆에서 보면 주먹이 골반 앞이고 팔꿈치가 뒤), 왼팔은 계속 사타구니 앞이나 등 쪽으로 갔다. 손목은 가드 때처럼 위로 꺾여 있었다. 합장으로 바꾸려고 손가락(`index_01~03_r_ctrl` 등)에 회전을 넣었지만 주먹이 펴지지 않았다. 토큰을 너무 많이 써서 사용자가 중단했다.
     - **다음 방법 (사용자 결정)**: 사용자가 이 자세를 5~6초 **직접 촬영**한다(가드 1초 → 주먹을 골반으로 당김 1초 → 버팀 3초 → 가드로 복귀 1초, 대각선 전신, 2~3m). 이걸 기존 파이프라인(영상 가져오기 → MetaHuman Performance → Performer Skeleton → Puncher로 리타게팅)으로 처리하고, 팔·상체 키만 리깅으로 옮겨 공중 구간에 붙인다. 남의 영상(드래곤볼·품새)은 "직접 촬영" 조건과 저작권 때문에 쓰지 않는다.
     - 손으로 맞출 때 알게 된 축 (Section_1 가산 기준, 혹시 다시 할 때 참고): 팔 IK로 바꾸려면 Section_0의 `arm_*_fk_ik_switch` bool 키를 프레임마다 true로 넣는다(베이크 때 IK 컨트롤 값도 기록돼서 전환해도 자세가 튀지 않는다). `hand_l_ik_ctrl.Location`: X+ 아래, Y+ 앞, Z는 좌우(부호 불확실). `hand_r_ik_ctrl.Location`: X+ 앞, Y+ 위, Z+ 바깥. 캐릭터는 공중에서 대각선(+X+Y)을 본다. 캐릭터 왼쪽 옆 카메라 (270,−270,410) yaw 135, 오른쪽 옆 (−230,230,420) yaw −45, 정면 (300,300,420) yaw −135(화면 왼쪽이 오른팔). Simulate를 켜고 3.1초 뒤에 찍으면 정지 구간 한가운데(약 95프레임)다.
     - 작업 전 백업: `/Game/Cinematics/Backup/LS_Punch_v1` (베이크 전 v1 상태)
  2. [x] 반동 (2026-11-01, Section_1 가산 키): 사용자 요청으로 **공기포가 생긴(178) 다음 프레임부터 폭발적으로** 밀린다. 처음 3프레임에 대부분 밀리고 감속하며, 처음 세 키는 linear다. 사용자가 "더 멀리, 확실하게"라고 해서 **88cm**로 늘렸다. 몸은 벽 반대쪽(−Y)으로 밀리고 끝까지 유지한다. `body_ctrl.Location.X` 178:0→179:30→180:58→181:74→183:83→187:87→192:88. 발은 1프레임 늦게 따라온다(미끄러짐): `foot_l_ik_ctrl.Location.X` 179:0→180:26→181:52→182:68→184:79→188:86→193:88. `foot_r_ik_ctrl.Location.X`는 **부호가 반대**라 같은 값에 −를 붙인다. 무릎 굽힘 `body_ctrl.Location.Z` 178:0→181:−8→188:−9→200:−3→215:0, 상체 젖힘 `spine_03_ctrl.Rotation.Z` 178:0→180:15→183:18→192:8→205:3→225:0.
     - 밀려난 캐릭터가 화면 끝에 걸려서 Cam4 Transform의 Location.Y 키를 모두 −45 했다(250→205, 흔들림 키 포함).
     - 축: `body_ctrl.Location` X+ = 월드 −Y(벽 반대), Y+ = 월드 +X, Z+ = 위. `foot_l_ik_ctrl` X+ = 월드 −Y, `foot_r_ik_ctrl` X+ = 월드 +Y(좌우 대칭), Z+ = 위. `root_ctrl`은 가산 섹션에서 효과가 없다.
  3. [x] 마무리 (2026-11-01, Section_1 가산 키, Cam6가 등 뒤에서 찍는 구간): 가드를 풀고 양팔을 몸 옆으로 내리고(주먹은 쥔 채), 무릎을 펴며 일어서고, 숨을 내쉬듯 상체를 살짝 숙였다가 가슴을 편다. `upperarm_*_fk_ctrl.Rotation.Z` 222:0→240:−20→300:−20, `lowerarm_*_fk_ctrl.Rotation.Z` 222:0→240:−75→300:−75, `body_ctrl.Location.Z` 222:0→242:6→300:6, `spine_03_ctrl.Rotation.Z` 225:0→238:−6→255:2→300:2.
     - 관찰: PIE에서 9~11초에 위쪽 벽 조각 몇 개가 공중에 떠 있는 것처럼 보인다. 렌더에서도 그런지 확인이 필요하다(예전 MRQ 렌더에서는 빠르게 날아갔다).
  4. 비교 영상: **직접 촬영한 원본 영상 | 최종본** 두 개만 나란히 붙여 본편 끝에 넣는다(사용자 결정. 촬영 원본과 비교하면 리깅으로 더한 동작이 다 보이므로 v1은 넣지 않는다).
- [x] 교수님께 리깅 방식 확인 질문 → 답변 2로 받음
- [x] **v2 렌더 (2026-11-01 밤)**: 파닥임·반동(88cm)·Spawnable 벽 붕괴·마무리를 반영했다. MRQ 348장 → `Saved/LS_Punch_final.mp4`(= `Saved/LS_Punch_v2.mp4`로도 보관, 11.6초). 렌더 프레임 기준으로 공기포가 184~186에 벽에 닿고 188부터 부서진다(싱크 맞음). 반동은 180에서 순간적으로 일어난다. 렌더에서는 벽 조각이 공중에 뜨지 않고 바닥에 떨어진다. 효과음은 v1 그대로 붙였다(충돌음 6.22초 = 렌더 186프레임).
- [x] **비교 영상·제출본 (2026-11-01)**: 사용자가 v2를 "괜찮아"라고 했다. 촬영 원본은 `C:\Users\rocky\Downloads\punch.mp4`(세로 1080×1920, 59.94fps, 7.44초, 노트북에만 있음, **커밋 안 함**). 원본에서 점프 꼭대기는 약 2.5초, 펀치는 약 4.25초다. `bash Tools/sfx/make_compare.sh <원본> Project1/Saved/LS_Punch_final.mp4 Project1/Saved`로 만든다. 원본 앞 0.33초를 잘라 점프 꼭대기를 최종본의 공중 정지 시작(2.17초)에 맞추고, 왼쪽에 원본(세로)·오른쪽에 최종본을 놓고 맑은 고딕 자막을 단다(필터는 `Tools/sfx/compare_filter.txt`). ffmpeg 9에서는 `-filter_complex_script` 대신 `-/filter_complex`를 쓴다. 결과는 `Saved/LS_Punch_compare.mp4`(11.6초)와 **제출본 `Saved/LS_Punch_submit.mp4`**(본편+비교, 23.2초)다.
- [x] 기술 문서 갱신 (2026-11-01): `Docs/make_tech_doc.py` → `Docs/과제1_기술요소정리.docx`(6쪽). 베이크, 가산 레이어, 파닥임, 반동, 마무리, Spawnable 벽 싱크, 비교 장면, 결과물 목록을 반영했다.
- **다음에 이어서 할 일**: 11/3에 `Saved/LS_Punch_submit.mp4`와 필요하면 문서를 제출한다. 수정이 생기면 렌더 → `mux.sh` → `make_compare.sh` 순서로 다시 만든다.
- [x] **GitHub README 정리 (2026-11-01 밤 완료, 사용자가 GitHub에서 GIF·모자이크 확인함)**: 사용자 목표는 **XR 콘텐츠(공연·전시·게임·방탈출) 엔지니어 취업** 어필. 루트 `README.md`(GIF 2개, 720p 영상 링크, 파이프라인, 해결한 문제, MCP 자동화). 미디어는 `media/`(mp4는 `.gitattributes`에서 LFS 제외, 1MB 안팎). 비교 영상은 공개 저장소라 **얼굴을 모자이크**했다: `python Tools/sfx/anonymize_face.py <원본> <출력>`(numpy NCC 머리 추적, OpenCV 없음. MSYS2 파이썬이라 opencv 설치 불가) → 그 출력으로 `make_compare.sh`를 임시 폴더에 돌린 뒤 720p로 줄였다. 제출본(`Saved/LS_Punch_submit.mp4`)은 그대로(얼굴 있음).
- (기록용) README 정리 계획 원문 (2026-11-01 밤)
  - 사용자 질문: "이 과제가 취업에 도움이 될까, 굳이 정리해야 할까?" → 답변: 게임·XR·테크니컬 아티스트 쪽이면 파이프라인 전체를 혼자 끝낸 경험, 문제 해결 과정, AI 에이전트(MCP) 자동화가 보여줄 만하다. 비용이 적으니 가볍게라도 해두기를 추천했다. 사용자는 아직 "해줘"라고 하지 않았다. **resume하면 먼저 진행할지, 지원 분야는 어디인지, 저장소가 공개인지 비공개인지를 확인한다.** (2026-11-01 확인: **PUBLIC**)
  - 계획: ① `Saved/LS_Punch_final.mp4`를 720p 저화질(수 MB) mp4로 줄이고 짧은 GIF(반동·벽 붕괴 위주 3~4초)도 만든다. 저장소 `media/` 폴더에 두고, mp4·gif는 LFS가 될 수 있으니 README에서 보이는지 확인한다(GIF는 .gitattributes에 없으면 일반 커밋). ② 저장소 루트 `README.md`: 미리보기, 한 줄 소개, 파이프라인(촬영 → 마커리스 모캡 → 메타휴먼 → 리타게팅 → Control Rig 베이크·가산 레이어 → Chaos 파괴 → MRQ → 효과음 합성), 사용 기술, 해결한 문제(PIE/MRQ 타이밍 → Spawnable, 오른발 IK 부호, 59.94fps 내보내기 오류 → 표시 프레임레이트 전환), Claude Code+MCP로 자동화한 부분, 기술 문서 링크. ③ 커밋·푸시.
  - 주의: 공개 저장소라면 사용자 얼굴이 나오는 촬영 원본(`punch.mp4`)과 비교 영상(`LS_Punch_compare.mp4`, `LS_Punch_submit.mp4` 뒷부분)은 넣지 않는다(넣을지 사용자에게 묻는다).: ① 반동(2) → ② 마무리(3) → ③ 사용자가 기 모으기 자세를 찍어 오면 모캡 처리 후 공중 구간에 붙이기(1) → ④ MRQ 다시 렌더(웜업 0, 템포럴 8) → `Tools/sfx/mux.sh`로 소리 합치기 → ⑤ 촬영 원본과 최종본 비교 영상 → ⑥ `Docs/make_tech_doc.py`의 2-4 표 갱신 후 문서 다시 생성. 이전 사용자 메시지: "이거(기 모으기) 빼고 먼저 진행하고 나중에 찍고 알려줄게".
- [x] 11/3 제출 (v2 제출본 `Saved/LS_Punch_submit.mp4`)
- **과제 조건 재확인 (2026-11-03)**: 교수님 말씀은 "3~5분 스토리텔링. 모션캡처뿐만 아니라 모션캡처를 쓴 액션과 스토리가 있어야 한다"였다. **재제출 마감은 2026-11-04 오전 11:59.** 기존 11.6초 영상은 클라이맥스로 그대로 쓴다.
- [ ] **확장판 「올드보이」 오마주 (2026-11-03 사용자 결정)**: 밀실에 갇혀 군만두만 먹다가 수련해서 벽을 부수고 나간다. 원작 영상·음악은 쓰지 않고 설정만 오마주한다.
  - 1막 갇힘: 밀실(침대·TV·문 배식구, 천장 조명 하나). 깨어나서 문을 두드림 / 2막 군만두: 배식구로 쟁반이 들어오고 먹음. 먹는 클립을 반복하며 "1일째 → 100일째 → 3년째" 자막, 벽에 날짜 표시가 늘어남 / 3막 첫 탈출 실패: 벽 펀치 → 충격으로 튕겨 나가 넘어짐(리깅·물리) / 4막 수련: TV 앞 섀도복싱, 벽 치기, 날짜 표시 계속 늘어남 / 5막 각성: 기존 v2 클라이맥스(벽 너머 햇빛) / 6막 탈출: 빛 속으로 걸어 나감, 군만두 하나 집어 들고 나감(마무리 개그) → 엔딩 → 비교 영상
  - [x] 밀실 세트 1차 (2026-11-03 노트북): 아웃라이너 `Story/Room`, 재질 `/Game/Story/Room/MI_*`(모두 `M_Concrete` 인스턴스). 실내 x −350~350, y −400~485, 바닥 z 210.6(카펫), 천장 z 510. 앞벽은 가운데가 `Wall_Target`(GC), 양옆이 `Room_FrontL/R`. `MI_Wall` 색을 올리브 벽지로 바꿨다(GC도 같은 재질). 소품: 뒷벽 `Room_Door`(0,−398) + `Room_FeedSlot`, `Room_Bed`(−290,−270), `Room_TV`(315,−200), `Room_Table`(−280,60) 위 `Room_Tray` + `Room_Dumpling1~8`, 천장 `Room_Bulb`(PointLight 40cd, Movable). 기존 카메라 몇 대는 방 밖에 있어서 클라이맥스 컷마다 가리는 벽을 숨겨야 한다.
  - [x] 세트 2차 (2026-11-03 노트북)
    - 노출: PPV에서 Min/Max Brightness가 둘 다 0으로 이미 고정(EV 0)이다. `Room_Bulb`는 10cd·3000K. 전구를 꺼도 SkyLight가 조금 새어 들어와서 완전히 어둡지는 않다.
    - TV: `Room_TVScreen`(큐브, x 292 면)에 `/Game/Story/Room/M_TVScreen`(Unlit, Time→Sine 두 개를 곱해 푸른 Emissive가 깜빡임). `Room_TVLight`(RectLight 12cd, 푸른색, Movable). 빛 세기 깜빡임은 필요하면 시퀀스 키로 넣는다.
    - 날짜 표시: `Room_Tally`(Plane, 왼쪽 벽 x −349.5, y −200~0, z 290~380) + `/Game/Story/Room/M_Tally`(Masked, 스칼라 파라미터 **`Count`** 기본 30, 한 줄 40개 × 6줄 = 최대 240). 시퀀스에서 Material Parameter 트랙으로 Count를 키 잡아 늘린다.
    - 태양: DirectionalLight 회전 (pitch −28, yaw −90). 벽(+Y) 바깥에서 방 안쪽으로 비춘다. Simulate에서 벽이 부서지면 구멍으로 빛이 들어오고, 조각이 역광 실루엣으로 보이는 것을 확인했다.
    - 배식구: `Room_FeedSlot`을 바닥 높이(z 218)로 내렸다. `Room_Dumpling1~8`은 `Room_Tray`의 자식이다(모두 Movable). 쟁반 Transform만 키 잡으면 된다(문 밖 y≈−430 → 바닥 y≈−370). 식탁 옆 `Room_Stool`(-200, 60, MI_Wood).
  - 촬영 목록 (2026-11-03 사용자에게 전달): 1 깨어나기(정측면) 2 문 두드리기(앞 대각 45°) 3 쟁반 받기+젓가락질(앞 대각) 4 날짜 긋기(벽 옆 90°) 5 펀치 실패→엉덩방아(측면, 매트) 6 일어나기(측면) 7 섀도복싱 20초(앞 대각) 8 군만두 집고 걸어 나가다 뒤돌아보기. 세로·고정·전신·시작과 끝 1초 정지·각 2번.
  - 촬영 목록: 깨어나기, 문 두드리기, 앉아서 젓가락질 마임, 날짜 표시 긋기, 펀치 후 뒤로 넘어지기, 섀도복싱, 넘어졌다 일어나기, 걸어 나가다 뒤돌아보기(각 10~15초, 2번씩). 실내 조명에서 찍는다.

## 메타휴먼 작업 메모

- 메타휴먼 에셋(`Content/MetaHumans/`)은 git 제외라 노트북에만 있다. 다른 PC에서는 `MH_Puncher`부터 다시 만들어야 한다.
- 리깅/Assemble 중 "용량 부족" 경고는 디스크가 아니라 RAM 부족이다. 에디터를 재시작하고 `MH_Puncher`만 연 상태에서 진행한다.
- Assemble 결과물은 메모리에만 생기고 저장되지 않는다. 끝나면 반드시 Save All(또는 MCP `save_assets`)을 한다.
- 레벨에 배치한 `BP_Puncher`에서 애니메이션을 재생하려면 `Body` 컴포넌트의 AnimationMode를 `AnimationSingleNode`로 바꾸고 AnimationData를 지정한다. MCP `set_properties`를 쓸 때는 `{"AnimationData": {"animToPlay": {"refPath": "..."}}}` 형식이어야 한다. 문자열로 넣으면 실패해도 true를 반환한다.
- 메타휴먼을 Sequencer에 추가하면 에디터가 Body에 키가 없는 Control Rig 트랙을 자동으로 붙인다. 이 트랙이 애니메이션 트랙을 덮어 캐릭터가 멈춰 있게 된다. 애니메이션만 재생할 때는 이 트랙을 지운다.
- MCP `set_actor_transform`에 rotation만 넘기면 location이 (0,0,0)으로 바뀐다. location, rotation, scale을 모두 넘긴다.
- 레벨 액터는 MCP `save_actor`나 경로를 지정한 `save_assets`로 저장되지 않는다("Asset does not exist"). `save_assets`에 빈 목록(`{"asset_paths": []}`)을 넘기면 변경된 액터까지 모두 저장된다.
- 에디터가 한국어라서 Blueprint `write_graph_dsl`이 동작하지 않는다(`AddEvent|...` 노드를 못 찾음). 노드 타입 ID도 `유틸리티|플로컨트롤|Delay`, `필드|AddTransientField`처럼 한국어다. `create_node`·`connect_pins`·`set_pin_value`로 만들고, ProgrammaticToolset 스크립트로 묶어서 실행한다. BeginPlay 노드는 `add_event`에 `ReceiveBeginPlay`를 넘겨 만든다.
- Fracture 모드에서 만든 Geometry Collection은 조각 구분 색(`bShowBoneColors`)이 켜진 채 남는다. 끄지 않으면 Simulate에서 알록달록하게 보인다.
- Simulate 테스트: ProgrammaticToolset 스크립트에서 `StartPIE`(bSimulate) → `time.sleep` → `CaptureViewport`를 여러 번 → `StopPIE`. 결과 base64를 디코딩해서 본다.
- `LS_Punch`의 Tick Resolution은 24000이다(30fps 한 프레임 = 800틱). 애니메이션 섹션의 `startFrameOffset`/`endFrameOffset`은 이 틱 단위다.
- MCP `bake_to_control_rig`와 `load_anim_into_rig`는 시퀀서의 구간 나누기·오프셋을 무시하고 원본 애니메이션을 0프레임부터 그대로 넣는다(`start_frame`도 무시됨). 베이크하면 원본 애니메이션 트랙이 아웃라이너에서 '비활성' 상태가 되고, 섹션의 `bIsActive`를 켜도 풀리지 않는다.
- 메타휴먼 Body에 Control Rig 트랙을 붙였다 떼기를 반복하면 애니메이션 트랙이 더 이상 적용되지 않는다(차렷 또는 A자세로 멈춤). 시퀀스에서 캐릭터 바인딩을 지우고 `add_actors`로 다시 넣은 뒤 트랙을 새로 만들면 해결된다. 다시 넣을 때 자동으로 생기는 트랙(Face Control Rig 등)은 지운다.
- Control Rig가 캐릭터를 움직일 때는 에디터 뷰포트 캡처와 `get_world_transform`(항상 0)에 반영되지 않는다. **Simulate 중 캡처에는 반영된다.** 그래서 리깅 결과는 Simulate로 확인한다(StartPIE → sleep → CaptureViewport. Simulate 뷰포트는 검은 테두리 안에 작게 그려지므로 밝은 영역만 잘라서 본다). 캡처 한 장에 약 0.6초가 걸리니 시간을 계산해서 찍는다.
- 레이어드 MetaHuman_ControlRig 섹션 `MovieSceneControlRigParameterSection_0`(트랙 `MovieSceneControlRigParameterTrack_12`)에는 키프레임 도구 `add_key_float`로 `컨트롤.Rotation.X/Y/Z` 채널에 바로 키를 넣는다. 컨트롤 리그 경로는 `/Game/MetaHumans/Common/Common/MetaHuman_ControlRig`. 섹션은 범위가 무한이라 `get_section_range`가 실패한다.
- 팔 FK 축(레이어드 기준, 양쪽 같은 부호로 대칭으로 움직임): `upperarm_*_fk_ctrl` Z−는 팔꿈치를 옆으로 벌림, Y+는 팔을 옆으로 들어 올림, X는 팔 비틀기. `lowerarm_*_fk_ctrl` Z−는 팔꿈치를 폄(주먹이 아래로), Z+는 더 굽힘. `spine_03_ctrl` Z+는 가슴을 펴고 상체를 젖힘, X·Y는 옆으로 기울임.
- CineCamera를 `add_actors`로 시퀀스에 넣으면 CameraComponent 아래에 CurrentFocalLength(35)·ManualFocusDistance·CurrentAperture 트랙이 자동으로 생긴다. 렌즈를 바꾸려면 컴포넌트 속성이 아니라 이 트랙의 키(채널 이름 `None`)를 바꾼다.
- MCP `set_camera_cut_binding`은 내부 오류가 난다. 컷 섹션에 `set_properties`로 `{"CameraBindingID": {"guid": "<카메라 바인딩 ID>", "sequenceId": 0, "resolveParentIndex": 0}}`을 넣는다.
- CaptureViewport는 화각이 90도로 고정이다. 시네 카메라 구도를 보려면 카메라 위치로 캡처한 뒤 가운데를 잘라낸다(20mm면 가로 59%).
- 시퀀스로 움직일 액터는 Mobility를 Movable로 바꾼다. Static이면 에디터에서 프레임을 넘길 때는 움직이지만 Simulate/렌더에서는 움직이지 않는다.
- MCP `add_actors`로 액터를 시퀀스에 넣으면 Transform 트랙(현재 위치·크기가 키로 들어 있음)이 자동으로 생긴다. 직접 Transform 트랙을 따로 만들면 두 트랙이 섞여 값이 평균이 된다. 자동 트랙을 지우거나 그 트랙에 키를 넣는다.
- Simulate 중 값 확인: PIE 액터 경로는 `/Game/ThirdPerson/UEDPIE_0_Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.<액터 이름>`이다. 캡처보다 `get_actor_transform`으로 숫자를 읽는 쪽이 빠르고 정확하다.
- `AS_MHP_punch_Puncher`(30fps 기준 0~152프레임)에서 주먹이 가장 뻗는 순간은 120프레임(4.0초)이다. 124프레임에는 이미 거둬들인다.
- 캡처 여러 장을 한 스크립트에서 받으면 응답이 커서 MCP 연결이 끊긴다(5장 이상). 4장씩 받고, PIL로 잘라 한 장으로 합쳐서 본다. MCP 도구를 쓰기 전에 `IsPIERunning`으로 Simulate가 켜져 있는지 확인한다(켜져 있으면 PIE 월드가 캡처된다).
- Unreal MCP에는 Fracture(Geometry Collection 생성·분할) 도구가 없다. 파이썬 스크립트 도구도 `unreal` 모듈을 쓸 수 없다. Fracture는 사용자가 Fracture 모드에서 직접 한다.
- Geometry Collection은 부서지기 전에 `RootProxyData`의 프록시 메시(기본 큐브 + BasicShapeMaterial)로 그려진다. 벽 재질을 바꿀 때는 GC 에셋의 `Materials`와 `RootProxyData.meshOverrideMaterials`를 함께 바꾼다. 재질에 `bUsedWithGeometryCollections`가 꺼져 있으면 기본 재질로 보인다. 에디터 뷰포트는 바꾼 뒤에도 캐시된 흰 벽을 보여줄 수 있으니 Simulate에서 확인한다.
- `CaptureViewport`에는 `annotations`를 반드시 넘긴다(주석이 필요 없으면 gridSpacing·maxLabelDistance 0).
- MCP `bake_channel_keys`는 값 1개만 돌려준다(쓸 수 없음). 값은 `get_keys`로 읽는다.
- **벽 붕괴 타이밍 (2026-11-01 변경)**: 예전에는 레벨에 놓인 `BP_WallBreaker`가 BeginPlay 뒤 TriggerTime초 타이머로 터졌다. 그래서 PIE와 MRQ의 타이밍이 0.25초 어긋났다(MRQ에 맞춰 6.38로 하면 PIE에서 늦게 깨짐). 이제는 레벨 액터를 지우고, `LS_Punch`의 **Spawnable 바인딩 `WallBreaker_Spawn`**(TriggerTime 0, BlastSpeed 900, BlastRadius 400, 위치 (0,380,360))으로 바꿨다. Spawn 트랙이 0프레임에 false, **184프레임에 true**라서, 시퀀스가 184에 도달하면 생성되어 바로 터진다. PIE와 렌더 모두 같은 프레임이다. 붕괴 프레임을 바꾸려면 Spawn 섹션 `MovieSceneSpawnTrack_0.MovieSceneSpawnSection_0` 채널 `None`의 true 키를 옮긴다.
- MCP `CaptureViewport`는 Simulate 중에도 동작한다. 응답이 커서 파일로 저장되는데, base64를 디코딩하면 이미지로 볼 수 있다.

## 마커리스 모캡 파이프라인 (테스트 완료)

유튜브 댄스 영상으로 "영상 → 애니메이션 → 기본 마네킹(Manny)"이 제대로 움직이는지 확인했다. 정식 영상(직접 촬영한 펀치 동작)도 같은 절차로 진행한다.

테스트 결과물 (모두 `Content/CaptureManager/` 안에 있어서 git에서 제외됨, 데스크톱에만 있음)
- `Imports/Mono_Video_Ingest/cortis_dance_1/`
  - `CD_cortis_dance_1`: 캡처 데이터 (60fps, 1470프레임)
  - `MHP_cortis_dance`: MetaHuman Performance
  - `SK_cortis_dance`, `AS_cortis_dance`: Performer Skeleton 메시와 애니메이션
  - `AS_cortis_dance1`: Manny(`SK_Mannequin`) 스켈레톤으로 리타게팅한 애니메이션
- `Lv1_MocapTest`: 테스트 레벨. 원점에 `Manny_MocapTest`가 있고, `AS_cortis_dance1`을 반복 재생한다 (Simulate로 확인)

알게 된 점
- Export를 Existing Skeleton + `SKM_Manny_Simple`로 하면 "필요한 바디 본이 누락되었습니다" 경고가 뜬다. MetaHuman과 Manny의 척추·목 본 구성이 다르기 때문이다. 이 경우 **Performer Skeleton**으로 내보낸다.
- 리타게팅: 애니메이션 우클릭 → Retarget Animations → 대상 `SKM_Manny_Simple`로 지정하면 IK Rig와 리타게터가 자동으로 만들어진다. Unreal MCP에는 에셋 생성(Performance, IK Rig, 리타게터, 레벨) 기능이 없어서 이런 에셋은 사용자가 UI에서 만든다. 만든 뒤 속성 설정, 액터 배치, 저장은 MCP로 할 수 있다.
- MetaHuman Performance 처리는 24초 영상에 약 15분 걸렸다.
- MCP의 `CaptureEditorImage`는 에디터가 백그라운드에 있으면 화면이 갱신되지 않은 이미지를 돌려준다. 이럴 때는 사용자에게 직접 확인해 달라고 한다.

- 테스트 영상 원본: `C:\Users\user\Videos\4K Video Downloader+\cortis_dance.mp4` (유튜브 쇼츠 K-pop 댄스, 데스크톱에만 있음). **커밋하지 않는다.** 파이프라인 테스트용일 뿐이고 제출물에는 쓰지 않는다 (교수님 답변: 직접 촬영한 영상만 인정).
- 다른 PC에서 할 때: 위 플러그인을 설치하고, 영상 파일을 아무 폴더에 둔 뒤 1단계부터 다시 한다.

절차 (공식 문서: https://dev.epicgames.com/documentation/metahuman/metahuman-animation-from-mono-video-capture-in-unreal-engine)
1. [x] **영상 가져오기 (사용자가 직접)**: Tools → Live Link Hub → 드롭다운에서 Capture Manager → Data Devices에서 Add → Mono Video Ingest → Details에서 소스 경로를 영상 폴더로 지정 → 파일 선택 후 Add to Queue → Start. 결과는 `Content/CaptureManager/Imports/<장치 이름>/`에 캡처 데이터 에셋으로 생긴다. Live Link Hub는 별도 앱이라 MCP로 조작할 수 없다.
2. [x] **솔브**: 콘텐츠 브라우저에서 MetaHuman → MetaHuman Performance 에셋 생성 → Footage Capture Data에 1단계 에셋 지정 → Processing Parameters에서 Facial Tracking 끄기, Body Tracking 켜기, Head Movement Mode는 Disable → 타임라인 트림 → Process
3. [x] **내보내기**: Export Animation에서 Performer Skeleton을 고른다. 그다음 Retarget Animations로 `SKM_Manny_Simple`에 리타게팅한다.
4. [x] 레벨에 Manny를 배치하고 애니메이션을 재생해서 확인한다.
