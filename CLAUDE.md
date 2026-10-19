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
- [ ] 프로젝트 목표 및 요구사항 정리 (아직 정하지 않음. 기존 계획은 GitHub 이슈 #1~#7에 있고, 시나리오 후보는 이슈 #1 코멘트에 있음. 사용자가 확정하기 전에는 계획을 바꾸지 않는다)
- [x] 마커리스 모캡 플러그인 설치 및 프로젝트에서 활성화
- [x] 영상 → 마커리스 모캡 → Manny 리타게팅 파이프라인 테스트 (2026-10-19 데스크톱에서 완료. Manny가 춤 동작을 잘 따라함)
- [x] 모캡 소스 결정 (2026-10-20, 이슈 #1 코멘트): 두 가지를 병행한다. 메인은 테스트에 쓴 유튜브 댄스 영상(`cortis_dance`)으로 다음 단계를 계속 진행한다(수업 제출용, 원본은 커밋 금지, 최종에 쓰면 출처 표기). 중간에 사용자가 같은 안무를 직접 춰서 촬영하고 비교한다. 원곡 음원은 쓰지 않는다(무음 또는 무료 음원).
- [ ] 스토리, 3D 모델(캐릭터) 정하기 → 남은 이슈(#3 메타휴먼, #4 리타게팅·Sequencer, #5 IK, #6 피직스, #7 렌더링)

## 마커리스 모캡 파이프라인 (테스트 완료)

시나리오와 정식 영상은 아직 정하지 않았다. 먼저 "영상 → 애니메이션 → 기본 마네킹(Manny)"이 제대로 움직이는지 확인했다. 정식 영상도 같은 절차로 진행한다.

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

- 테스트 영상 원본: `C:\Users\user\Videos\4K Video Downloader+\cortis_dance.mp4` (유튜브 쇼츠 K-pop 댄스, 데스크톱에만 있음). **커밋하지 않는다.** 이 영상으로 계속 진행하고, 사용자가 직접 춘 영상도 병행해서 비교한다 (진행 상황의 "모캡 소스 결정" 참고).
- 다른 PC에서 할 때: 위 플러그인을 설치하고, 영상 파일을 아무 폴더에 둔 뒤 1단계부터 다시 한다.

절차 (공식 문서: https://dev.epicgames.com/documentation/metahuman/metahuman-animation-from-mono-video-capture-in-unreal-engine)
1. [x] **영상 가져오기 (사용자가 직접)**: Tools → Live Link Hub → 드롭다운에서 Capture Manager → Data Devices에서 Add → Mono Video Ingest → Details에서 소스 경로를 영상 폴더로 지정 → 파일 선택 후 Add to Queue → Start. 결과는 `Content/CaptureManager/Imports/<장치 이름>/`에 캡처 데이터 에셋으로 생긴다. Live Link Hub는 별도 앱이라 MCP로 조작할 수 없다.
2. [x] **솔브**: 콘텐츠 브라우저에서 MetaHuman → MetaHuman Performance 에셋 생성 → Footage Capture Data에 1단계 에셋 지정 → Processing Parameters에서 Facial Tracking 끄기, Body Tracking 켜기, Head Movement Mode는 Disable → 타임라인 트림 → Process
3. [x] **내보내기**: Export Animation에서 Performer Skeleton을 고른다. 그다음 Retarget Animations로 `SKM_Manny_Simple`에 리타게팅한다.
4. [x] 레벨에 Manny를 배치하고 애니메이션을 재생해서 확인한다.
