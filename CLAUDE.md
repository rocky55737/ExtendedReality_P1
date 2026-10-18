# ExtendedReality_P1

대학 Extended Reality 수업 Project1. Unreal Engine 5.8 프로젝트이며, 노트북과 데스크톱을 오가며 작업한다.

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
- [ ] 프로젝트 목표 및 요구사항 정리 (아직 정하지 않음. 기존 계획은 GitHub 이슈 #1~#7에 있고, 시나리오 후보는 이슈 #1 코멘트에 있음. 사용자가 확정하기 전에는 계획을 바꾸지 않는다)
- [x] 마커리스 모캡 플러그인 설치 및 프로젝트에서 활성화
- [ ] **진행 중: 영상 → 마커리스 모캡 → Manny 리타게팅 파이프라인 테스트** (아래 참고)

## 현재 작업: 마커리스 모캡 파이프라인 테스트

목표: 시나리오와 정식 영상은 나중에 정하고, 먼저 "영상 → 애니메이션 → 기본 마네킹(Manny)"이 제대로 움직이는지 확인한다.

- 테스트 영상: `C:\Users\user\Videos\4K Video Downloader+\cortis_dance.mp4` (유튜브 쇼츠 K-pop 댄스, 데스크톱에만 있음). **테스트 전용이므로 커밋하지 않는다.** 정식 영상은 사용자가 합법적인 것으로 따로 찾는다.
- 노트북에서 이어갈 때: 위 플러그인을 설치하고, 영상 파일을 아무 폴더에 둔 뒤 1단계부터 다시 한다.

절차 (공식 문서: https://dev.epicgames.com/documentation/metahuman/metahuman-animation-from-mono-video-capture-in-unreal-engine)
1. [ ] **영상 가져오기 (사용자가 직접)**: Tools → Live Link Hub → 드롭다운에서 Capture Manager → Data Devices에서 Add → Mono Video Ingest → Details에서 소스 경로를 영상 폴더로 지정 → 파일 선택 후 Add to Queue → Start. 결과는 `Content/CaptureManager/Imports/<장치 이름>/`에 캡처 데이터 에셋으로 생긴다. Live Link Hub는 별도 앱이라 MCP로 조작할 수 없다.
2. [ ] **솔브**: 콘텐츠 브라우저에서 MetaHuman → MetaHuman Performance 에셋 생성 → Footage Capture Data에 1단계 에셋 지정 → Processing Parameters에서 Facial Tracking 끄기, Body Tracking 켜기, Head Movement Mode는 Disable → 타임라인 트림 → Process
3. [ ] **내보내기**: Export Animation. 먼저 Existing Skeleton으로 대상에 `SKM_Manny`를 지정해 본다. 안 되면 Performer Skeleton으로 내보낸 뒤 IK Retargeter로 Manny에 리타게팅한다.
4. [ ] 레벨에 Manny를 배치하고 애니메이션을 재생해서 확인한다.
