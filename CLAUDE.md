# ExtendedReality_P1

대학 Extended Reality 수업 Project1. Unreal Engine 5.8 프로젝트이며, 노트북과 데스크톱을 오가며 작업한다.

## 프로젝트 구조

- `Project1/Project1.uproject`: UE 5.8 프로젝트 파일. Third Person 템플릿 기반의 Blueprint 전용 프로젝트이며 C++ `Source/` 폴더는 없다.
- `Project1/Content/`: 에셋 (`ThirdPerson`, `Characters`, `Input`, `LevelPrototyping` 등)
- `Project1/Config/`: 프로젝트 설정
- 활성 플러그인: ModelingToolsEditorMode, GameplayStateTree, ModelContextProtocol, ToolsetRegistry, EditorToolset, AnimationAssistantToolset, PhysicsToolsets, MetaHumanCharacter, MetaHumanGenerator

## Git / LFS

- 원격 저장소: https://github.com/rocky55737/ExtendedReality_P1 (기본 브랜치 `main`)
- `.uasset`, `.umap`, `.fbx`, `.png`, `.wav`, `.mp4` 파일은 Git LFS로 관리한다. 클론하기 전에 `git lfs install`을 먼저 실행한다.
- `Binaries/`, `DerivedDataCache/`, `Intermediate/`, `Saved/`, `*_BuiltData.uasset` 파일은 커밋하지 않는다.
- `Content/MetaHumans/` 폴더는 용량이 커서 git에서 제외했다. 다른 PC에서는 MetaHuman 에셋을 다시 받거나 다시 만들어야 한다.

## Unreal MCP (Claude Code ↔ 에디터)

- 저장소 루트의 `.mcp.json`과 `Project1/.mcp.json`에 `unreal` MCP 서버(`http://127.0.0.1:8000/mcp`)가 똑같이 설정되어 있다. 설정을 바꿀 때는 두 파일을 함께 수정한다.
- 에디터 설정(`Config/DefaultEditorPerProjectUserSettings.ini`)으로 MCP 서버가 에디터 실행 시 포트 8000에서 자동 시작된다.
- MCP 도구는 **Unreal 에디터가 열려 있을 때만** 동작한다. Claude Code는 저장소 루트나 `Project1/` 폴더 중 어디에서 실행해도 된다.

## 작업 규칙

- PC를 바꾸기 전에는 커밋하고 푸시한다. 작업을 시작할 때는 `git pull`을 먼저 한다.
- 에디터가 `.uasset`/`.umap` 파일을 열고 있으면 바이너리 충돌이 날 수 있다. 같은 에셋을 두 PC에서 동시에 수정하지 않는다.

## 진행 상황

- [x] UE5 프로젝트 생성, Git LFS 설정
- [x] Unreal MCP 서버 활성화, Claude Code 연결
- [ ] 프로젝트 목표 및 요구사항 정리 (아직 정하지 않음)
