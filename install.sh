#!/bin/bash

# System Monitor 설치 스크립트
# Google Colab, Jupyter, VSCode 등 모든 환경을 지원

set -e  # 오류 발생 시 스크립트 중단

echo "System Monitor 설치 시작"
echo "========================================"

# Python과 pip 확인
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "오류: Python이 설치되어 있지 않습니다."
    exit 1
fi

if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "오류: pip이 설치되어 있지 않습니다."
    exit 1
fi

# Python 버전 확인
PYTHON_VERSION=$(python3 --version 2>/dev/null || python --version 2>/dev/null)
echo "Python 버전: $PYTHON_VERSION"

# Git 확인
if ! command -v git &> /dev/null; then
    echo "오류: Git이 설치되어 있지 않습니다."
    echo "Git을 먼저 설치해주세요: https://git-scm.com/downloads"
    exit 1
fi

# 환경 감지
if [ -n "$COLAB_GPU" ] || [ -n "$COLAB_TPU_ADDR" ]; then
    echo "Google Colab 환경 감지됨"
    ENVIRONMENT="colab"
elif [ -n "$JUPYTER_SERVER_ROOT" ] || [ -n "$JUPYTER_CONFIG_DIR" ]; then
    echo "Jupyter 환경 감지됨"
    ENVIRONMENT="jupyter"
elif [ -n "$VSCODE_PID" ] || [ "$TERM_PROGRAM" = "vscode" ]; then
    echo "VSCode 환경 감지됨"
    ENVIRONMENT="vscode"
else
    echo "터미널 환경 감지됨"
    ENVIRONMENT="terminal"
fi

echo ""
echo "System Monitor 프로젝트 설치 중..."

# 프로젝트 디렉토리 설정
PROJECT_DIR="system-monitor"
REPO_URL="https://github.com/xonme888/config.git"

if [ -d "$PROJECT_DIR" ]; then
    echo "   기존 프로젝트 디렉토리 발견. 업데이트 중..."
    cd "$PROJECT_DIR"
    if ! git pull; then
        echo "경고: Git pull 실패. 기존 디렉토리를 삭제하고 다시 클론합니다."
        cd ..
        rm -rf "$PROJECT_DIR"
        git clone "$REPO_URL" "$PROJECT_DIR"
        cd "$PROJECT_DIR"
    fi
else
    echo "   GitHub에서 프로젝트 클론 중..."
    if ! git clone "$REPO_URL" "$PROJECT_DIR"; then
        echo "오류: 프로젝트 클론에 실패했습니다."
        echo "네트워크 연결을 확인하고 다시 시도해주세요."
        exit 1
    fi
    cd "$PROJECT_DIR"
fi

# setup.py 파일 존재 확인
if [ ! -f "setup.py" ]; then
    echo "오류: setup.py 파일을 찾을 수 없습니다."
    echo "올바른 프로젝트 디렉토리인지 확인해주세요."
    exit 1
fi

echo ""
echo "필수 패키지 설치 중..."

# 기본 패키지 설치 (CPU 모니터링용)
echo "   psutil 설치 중..."
pip install psutil

# GPU 모니터링을 위한 CuPy 설치
echo "   GPU 지원 패키지 확인 중..."

# CUDA 버전 감지 시도
CUDA_VERSION=""
if command -v nvidia-smi &> /dev/null; then
    CUDA_VERSION=$(nvidia-smi | grep "CUDA Version" | sed 's/.*CUDA Version: \([0-9]*\.[0-9]*\).*/\1/')
    echo "   CUDA 버전 감지됨: $CUDA_VERSION"
elif command -v nvcc &> /dev/null; then
    CUDA_VERSION=$(nvcc --version | grep "release" | sed 's/.*release \([0-9]*\.[0-9]*\).*/\1/')
    echo "   CUDA 버전 감지됨 (nvcc): $CUDA_VERSION"
fi

# CuPy 설치
if [ -n "$CUDA_VERSION" ]; then
    CUDA_MAJOR=$(echo $CUDA_VERSION | cut -d. -f1)
    if [ "$CUDA_MAJOR" = "12" ]; then
        echo "   CuPy CUDA 12.x 설치 중..."
        pip install cupy-cuda12x
    elif [ "$CUDA_MAJOR" = "11" ]; then
        echo "   CuPy CUDA 11.x 설치 중..."
        pip install cupy-cuda11x
    else
        echo "   경고: 지원되지 않는 CUDA 버전: $CUDA_VERSION"
        echo "   수동으로 CuPy를 설치하세요: pip install cupy-cuda11x 또는 cupy-cuda12x"
    fi
else
    echo "   정보: CUDA가 감지되지 않았습니다. CPU 모니터링만 사용 가능합니다."
    echo "   GPU 모니터링을 원한다면 수동으로 CuPy를 설치하세요:"
    echo "      - CUDA 11.x: pip install cupy-cuda11x"
    echo "      - CUDA 12.x: pip install cupy-cuda12x"
fi

echo ""
echo "System Monitor 패키지 설치 중..."
if ! pip install -e .; then
    echo "오류: 패키지 설치에 실패했습니다."
    echo "pip 권한을 확인하거나 다음 명령어를 시도해보세요:"
    echo "pip install --user -e ."
    exit 1
fi

echo ""
echo "설치 검증 중..."
if python -c "import system_monitor; print('System Monitor 설치 성공!')" 2>/dev/null; then
    echo "설치 완료!"
else
    echo "경고: 설치는 완료되었으나 모듈 import에 실패했습니다."
    echo "Python 경로 설정을 확인해주세요."
fi

echo ""
echo "설치된 위치: $(pwd)"
echo "Python 경로에 system_monitor 모듈이 추가되었습니다."
echo ""

# 환경별 사용법 안내
echo "사용법:"
case $ENVIRONMENT in
    "colab")
        echo "   Google Colab에서는 다음과 같이 사용하세요:"
        echo ""
        echo "   from system_monitor import setup_environment_optimized_monitor"
        echo "   monitor = setup_environment_optimized_monitor()"
        echo "   monitor.print_memory_usage('Colab 메모리', include_cpu=True)"
        ;;
    "jupyter")
        echo "   Jupyter에서는 다음과 같이 사용하세요:"
        echo ""
        echo "   from system_monitor import SystemMonitor, setup_logger"
        echo "   setup_logger('system_monitor', force_setup=True)"
        echo "   monitor = SystemMonitor()"
        echo "   monitor.print_memory_usage('Jupyter 메모리', include_cpu=True)"
        ;;
    *)
        echo "   일반 Python 스크립트에서는 다음과 같이 사용하세요:"
        echo ""
        echo "   from system_monitor import SystemMonitor"
        echo "   monitor = SystemMonitor()"
        echo "   monitor.print_memory_usage('시스템 메모리', include_cpu=True)"
        ;;
esac

echo ""
echo "설치 확인:"
echo "   python -c \"from system_monitor import SystemMonitor; print('System Monitor 설치 완료!')\"" 
echo ""
echo "자세한 문서는 README.md를 참조하세요."
echo "문제가 있다면 GitHub Issues에 등록해주세요."
echo ""
echo "데모 실행: python demo.py"