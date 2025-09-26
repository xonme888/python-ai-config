# System Monitor

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

시스템 리소스(CPU, GPU 메모리)를 모니터링하는 Python 라이브러리입니다. **Google Colab**, **Jupyter Notebook**, **VSCode** 등 모든 환경에서 동작하도록 최적화되었습니다.

## 주요 기능

- **CPU 메모리 모니터링** (psutil 기반)
- **GPU 메모리 모니터링** (CuPy 기반) 
- **실시간 메모리 사용량 출력**
- **메모리 단위 변환 유틸리티**
- **Colab/Jupyter 환경 최적화된 로깅**
- **VSCode/로컬 환경 완벽 지원**

## 설치 방법

### 자동 설치 스크립트 (권장)

프로젝트를 자동으로 클론하고 환경에 맞는 패키지를 설치합니다:

```bash
# 설치 스크립트 다운로드 후 실행
curl -O https://raw.githubusercontent.com/xonme888/config/main/install.sh
chmod +x install.sh
./install.sh
```

### Git을 통한 수동 설치

```bash
# 프로젝트 클론
git clone https://github.com/xonme888/config.git system-monitor
cd system-monitor

# 의존성 설치
pip install psutil

# GPU 지원이 필요한 경우
pip install cupy-cuda12x  # CUDA 12.x용
# 또는
pip install cupy-cuda11x  # CUDA 11.x용

# 패키지 설치
pip install -e .
```

### 의존성만 설치 (개발용)

프로젝트가 이미 있는 경우 의존성만 설치:

```bash
# 기본 설치 (CPU 모니터링만)
pip install psutil

# GPU 모니터링 포함 설치
pip install psutil cupy-cuda12x  # CUDA 12.x
pip install psutil cupy-cuda11x  # CUDA 11.x
```

### Google Colab에서 설치

```bash
# Colab 셀에서 실행
!git clone https://github.com/xonme888/config.git system-monitor
%cd system-monitor
!pip install psutil cupy-cuda12x
!pip install -e .
```

### 빠른 시작

설치 후 바로 데모를 실행해보세요:

```bash
python demo.py
```

## 사용법

### 기본 사용법

```python
from system_monitor import SystemMonitor, setup_logger

# 로깅 설정 (Colab과 VSCode 모두에서 로그 출력)
setup_logger('system_monitor', force_setup=True)

# 시스템 모니터 초기화
monitor = SystemMonitor()

# 메모리 사용량 출력
monitor.print_memory_usage("현재 상태", include_cpu=True)
```

### CPU 전용 모니터링

```python
from system_monitor import SystemMonitor

# GPU 없는 환경에서 안전하게 사용
cpu_monitor = SystemMonitor(use_gpu=False)
cpu_monitor.print_cpu_memory("CPU 메모리 상태")
```

### 수동 메모리 정보 접근

```python
from system_monitor import SystemMonitor

monitor = SystemMonitor()

# CPU 메모리 정보
cpu_info = monitor.get_cpu_memory()
if cpu_info:
    print(f"CPU: {cpu_info.used:.1f}MB / {cpu_info.total:.1f}MB")
    print(f"사용률: {cpu_info.usage_percent:.1f}%")

# GPU 메모리 정보
gpu_info = monitor.get_gpu_memory()
if gpu_info:
    print(f"GPU: {gpu_info.used:.1f}MB / {gpu_info.total:.1f}MB")
    print(f"사용률: {gpu_info.usage_percent:.1f}%")
```

### 메모리 단위 변환

```python
from system_monitor import MemoryConverter

bytes_value = 1024 * 1024 * 1024  # 1GB

# 단위 변환
mb_value = MemoryConverter.to_mb(bytes_value)
gb_value = MemoryConverter.to_gb(bytes_value)

# 포맷팅
formatted = MemoryConverter.format_memory(bytes_value, 'GB')
print(f"포맷팅된 값: {formatted}")
```

## 환경별 사용법

### Google Colab에서 사용

#### 방법 1: 환경 최적화 모니터 (권장)
```python
# Colab 셀에서 실행
!pip install psutil cupy-cuda12x

from system_monitor import setup_environment_optimized_monitor

# 환경에 최적화된 모니터 자동 설정
monitor = setup_environment_optimized_monitor()
monitor.print_memory_usage("Colab 메모리 상태", include_cpu=True)
```

#### 방법 2: 수동 설정
```python
from system_monitor import SystemMonitor, setup_logger

# 로깅 설정 (Colab에서 로그 출력 보장)
setup_logger('system_monitor', force_setup=True)

# GPU 런타임 체크
monitor = SystemMonitor()
if monitor.has_gpu:
        print("GPU 런타임이 활성화되어 있습니다!")
    else:
        print("경고: GPU 런타임을 활성화하세요: 런타임 > 런타임 유형 변경 > GPU")# 메모리 상태 출력
monitor.print_memory_usage("Colab 메모리 상태", include_cpu=True)
```

### Jupyter Notebook에서 사용

```python
from system_monitor import SystemMonitor, setup_logger
import logging

# 로깅 레벨 설정
setup_logger('system_monitor', level=logging.INFO, force_setup=True)

monitor = SystemMonitor()
monitor.print_memory_usage("Jupyter 환경", include_cpu=True)
```

### VSCode/로컬 환경에서 사용

```python
from system_monitor import SystemMonitor, setup_logger

# 개발 환경용 상세 로깅
setup_logger('system_monitor', level=logging.DEBUG)

monitor = SystemMonitor()
monitor.print_memory_usage("개발 환경", include_cpu=True)
```

## API 문서

### SystemMonitor 클래스

#### 생성자
```python
SystemMonitor(use_gpu: bool = True, cupy_instance=None)
```

- `use_gpu`: GPU 모니터링 사용 여부 (기본값: True)
- `cupy_instance`: 사용할 CuPy 인스턴스 (선택사항)

#### 속성
- `has_cpu: bool` - CPU 모니터링 가능 여부
- `has_gpu: bool` - GPU 모니터링 가능 여부

#### 메서드
- `get_cpu_memory() -> Optional[MemoryInfo]` - CPU 메모리 정보 반환
- `get_gpu_memory() -> Optional[MemoryInfo]` - GPU 메모리 정보 반환
- `print_cpu_memory(label: str = "CPU Memory")` - CPU 메모리 상태 출력
- `print_gpu_memory(label: str = "GPU Memory")` - GPU 메모리 상태 출력
- `print_memory_usage(label: str = "Memory Status", include_cpu: bool = False)` - 전체 메모리 상태 출력

### MemoryInfo 클래스

메모리 정보를 담는 데이터 클래스입니다.

```python
class MemoryInfo:
    used: float      # 사용된 메모리 (MB)
    total: float     # 전체 메모리 (MB)
    usage_percent: float  # 사용률 (%)
```

### MemoryConverter 클래스

메모리 단위 변환을 위한 유틸리티 클래스입니다.

```python
MemoryConverter.to_mb(bytes_value: int) -> float    # bytes를 MB로 변환
MemoryConverter.to_gb(bytes_value: int) -> float    # bytes를 GB로 변환
MemoryConverter.format_memory(bytes_value: int, unit: str = 'MB') -> str  # 포맷팅
```

### 로깅 함수들

```python
setup_logger(name: str = 'system_monitor', level: int = logging.INFO, force_setup: bool = False) -> logging.Logger
get_logger(name: str = 'system_monitor') -> logging.Logger
reset_logger_config()  # 로거 설정 초기화
```

## 문제 해결

### 로그가 보이지 않을 때

```python
from system_monitor import setup_logger, reset_logger_config

# 로거 설정 초기화 후 재설정
reset_logger_config()
setup_logger('system_monitor', force_setup=True)
```

### GPU 인식 안될 때

1. **CUDA 드라이버 확인**
   ```bash
   nvidia-smi
   ```

2. **CuPy 설치 확인**
   ```python
   try:
       import cupy
       print(f"CuPy 버전: {cupy.__version__}")
   except ImportError:
       print("CuPy가 설치되지 않았습니다.")
   ```

3. **Colab에서 GPU 런타임 활성화**
   - 런타임 → 런타임 유형 변경 → 하드웨어 가속기: GPU

### CPU 메모리 인식 안될 때

```bash
pip install --upgrade psutil
```

## 테스트

```bash
# 전체 테스트 실행
python -m pytest tests/

# 특정 테스트 실행
python -m pytest tests/test_monitor.py -v

# 커버리지 포함 테스트
python -m pytest tests/ --cov=system_monitor --cov-report=html
```

## 예제 파일

프로젝트에는 다음 예제 파일들이 포함되어 있습니다:

- `example.py` - 기본 사용법 예제
- `colab_example.py` - Google Colab/Jupyter 환경용 예제

```bash
# 예제 실행
python example.py
python colab_example.py
```

## 프로젝트 구조

```
system_monitor/
├── __init__.py          # 메인 모듈
├── monitor.py           # SystemMonitor 클래스
├── logging_config.py    # 로깅 설정
├── core/
│   ├── __init__.py
│   ├── info.py         # MemoryInfo 클래스
│   └── converter.py    # MemoryConverter 클래스
└── monitors/
    ├── __init__.py
    ├── base.py         # BaseMonitor 추상 클래스
    ├── cpu.py          # CPU 모니터
    └── gpu.py          # GPU 모니터
```

## 하위 호환성

기존 코드와의 호환성을 위해 다음 별칭들을 제공합니다:

```python
# 이전 버전 호환
from system_monitor import GPUMemoryMonitor, MemoryMonitorManager

# 모두 SystemMonitor와 동일
monitor = GPUMemoryMonitor()  # SystemMonitor()와 같음
manager = MemoryMonitorManager()  # SystemMonitor()와 같음
```

## 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/name`)
3. Commit your Changes (`git commit -m 'Add --'`)
4. Push to the Branch (`git push origin feature/name`)
5. Open a Pull Request

## 라이선스

MIT License로 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 지원

문제가 있거나 기능 요청이 있다면 [Issues](https://github.com/xonme888/system-monitor/issues)를 통해 알려주세요.

---