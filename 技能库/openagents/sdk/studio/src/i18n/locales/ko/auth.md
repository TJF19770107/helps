# auth.json

原始格式: JSON

```json
{
    "login": {
        "title": "로그인",
        "subtitle": "계정에 로그인",
        "emailLabel": "이메일",
        "emailPlaceholder": "이메일 주소",
        "passwordLabel": "비밀번호",
        "passwordPlaceholder": "비밀번호",
        "nameLabel": "이름",
        "namePlaceholder": "이름",
        "submitButton": "로그인",
        "forgotPassword": "비밀번호를 잊으셨나요?",
        "noAccount": "계정이 없으신가요?",
        "signUp": "회원가입"
    },
    "networkSelection": {
        "title": "OpenAgents Studio",
        "subtitle": "OpenAgents 네트워크에 연결하여 AI 에이전트와 협업을 시작하세요"
    },
    "agentSetup": {
        "title": "OpenAgents 네트워크 참가",
        "subtitle": "에이전트 이름과 그룹을 선택하여 네트워크에 연결하세요.",
        "adminSubtitle": "관리자 대시보드에 액세스하려면 관리자 비밀번호를 입력하세요.",
        "connectingTo": "연결 대상",
        "previousName": "이전에 사용한 이름",
        "previousNameHint": "이전 이름을 사용하거나 새 이름을 만들 수 있습니다",
        "agentName": "에이전트 이름",
        "agentNamePlaceholder": "에이전트 이름 입력...",
        "agentGroup": "에이전트 그룹",
        "loadingGroups": "그룹 로딩 중...",
        "default": "기본값",
        "defaultAgentGroup": "기본 에이전트 그룹",
        "password": "비밀번호",
        "passwordRequired": "비밀번호 필요",
        "passwordPlaceholder": "'{{group}}' 그룹 비밀번호 입력...",
        "noPasswordRequired": "'{{group}}' 그룹은 비밀번호가 필요하지 않습니다",
        "passwordRequiredHint": "'{{group}}' 그룹용",
        "nameSavedHint": "이름이 이 네트워크에 자동으로 저장됩니다.",
        "groupDescription": "{{group}} 그룹",
        "adminPassword": "관리자 비밀번호",
        "adminPasswordPlaceholder": "관리자 비밀번호 입력...",
        "adminPasswordRequired": "관리자 비밀번호 필요",
        "adminPasswordHint": "관리 기능에 액세스하려면 관리자 그룹의 비밀번호를 입력하세요.",
        "backToRegularLogin": "일반 로그인으로 돌아가기",
        "or": "또는",
        "buttons": {
            "randomName": "🎲 랜덤 이름 생성",
            "usePrevious": "↶ 이전 이름 사용: {{name}}",
            "back": "← 뒤로",
            "connect": "{{name}}(으)로 연결",
            "connecting": "연결 중...",
            "loginAsAdmin": "관리자로 로그인"
        },
        "errors": {
            "passwordRequired": "'{{group}}' 그룹에는 비밀번호가 필요합니다",
            "invalidPassword": "'{{group}}' 그룹의 비밀번호가 올바르지 않습니다",
            "invalidAdminPassword": "관리자 비밀번호가 올바르지 않습니다. 다시 시도해 주세요.",
            "connectionFailed": "네트워크 연결에 실패했습니다. 다시 시도해 주세요.",
            "adminConnectionFailed": "관리자로 연결에 실패했습니다. 비밀번호를 확인하고 다시 시도해 주세요.",
            "adminPasswordRequired": "관리자 비밀번호가 필요합니다"
        }
    },
    "profile": {
        "title": "프로필",
        "editProfile": "프로필 편집",
        "nameLabel": "이름",
        "namePlaceholder": "이름",
        "avatarLabel": "아바타 URL",
        "avatarPlaceholder": "아바타 URL (선택사항)",
        "saveButton": "변경사항 저장",
        "cancelButton": "취소"
    },
    "password": {
        "title": "비밀번호 입력",
        "subtitle": "이 네트워크는 비밀번호가 필요합니다",
        "passwordLabel": "비밀번호",
        "passwordPlaceholder": "비밀번호 입력...",
        "submitButton": "연결",
        "cancelButton": "취소",
        "incorrectPassword": "비밀번호가 올바르지 않습니다",
        "pleaseTryAgain": "다시 시도해 주세요"
    },
    "localNetwork": {
        "title": "로컬 네트워크",
        "detecting": "로컬 네트워크 감지 중...",
        "notFound": "로컬 OpenAgents 네트워크가 감지되지 않았습니다",
        "found": "로컬 OpenAgents 네트워크",
        "runningOn": "{{host}}:{{port}}에서 실행 중",
        "connect": "연결",
        "manageNetwork": "네트워크 관리"
    },
    "manualNetwork": {
        "title": "수동 연결",
        "tabs": {
            "quickConnect": "빠른 연결 호스트 + 포트",
            "networkId": "네트워크 ID",
            "hostPort": "호스트 + 포트"
        },
        "lastConnected": "마지막 연결 서버",
        "lastUsedAs": "마지막 사용 이름: <strong>{{name}}</strong>",
        "cached": "이전 성공적인 연결에서 캐시됨",
        "clearSaved": "저장 지우기",
        "hostLabel": "호스트",
        "hostPlaceholder": "localhost 또는 IP 주소",
        "portLabel": "포트",
        "networkIdLabel": "네트워크 ID",
        "networkIdPlaceholder": "network-id-123 또는 openagents://network-id",
        "hostPortHint": "직접 연결하려면 호스트 주소와 포트 번호를 입력하세요",
        "networkIdHint": "OpenAgents 디렉토리 서비스를 통해 연결하려면 네트워크 ID를 입력하세요",
        "useHttps": "SSL로 연결",
        "connect": "연결",
        "connecting": "연결 중...",
        "savedHint": "성공적인 연결은 빠른 액세스를 위해 자동으로 저장됩니다"
    }
}

```
