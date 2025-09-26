# GPU 메모리 모니터

[![PyPI version](https://badge.fury.io/py/gpu-memory-monitor.svg)](https://badge.fury.io/py/gpu-memory-monitor)
[![Python Version](https://img.shields.io/pypi/pyversions/gpu-memory-monitor.svg)](https://pypi.org/project/gpu-memory-monitor/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

CuPy를 사용하여 GPU와 CPU의 메모리 사용량을 모니터링하는 Python 패키지입니다.

## 목차

- [GPU 메모리 모니터](#gpu-메모리-모니터)
  - [목차](#목차)
  - [특징](#특징)
  - [설치 방법](#설치-방법)
  - [시스템 요구사항](#시스템-요구사항)
  - [사용 방법](#사용-방법)
    - [기본 사용법](#기본-사용법)
  - [출력 예시](#출력-예시)
  - [고급 사용법](#고급-사용법)
    - [커스텀 CuPy 인스턴스 사용](#커스텀-cupy-인스턴스-사용)
    - [예외 처리](#예외-처리)
  - [개발 환경 설정](#개발-환경-설정)
    - [개발 의존성 설치](#개발-의존성-설치)
    - [테스트 실행](#테스트-실행)
    - [코드 스타일 검사](#코드-스타일-검사)
  - [기여하기](#기여하기)
  - [라이선스](#라이선스)
  - [추가 자료](#추가-자료)

## 특징

- 실시간 CPU/GPU 메모리 모니터링
- 상세한 메모리 사용량 정보 제공
- 유연한 로깅 시스템
- 임계값 기반 경고 시스템
- 사용자 정의 가능한 설정
- 체계적인 에러 처리
- 메모리 사용량 통계

## 설치 방법

```bash
# 기본 설치 (CuPy 제외)
pip install gpu-memory-monitor

# CUDA 11.x 사용시
pip install gpu-memory-monitor[cuda11]

# CUDA 12.x 사용시
pip install gpu-memory-monitor[cuda12]
```

## 시스템 요구사항

- Python >= 3.7
- CUDA 11.x 또는 12.x
- CuPy
- psutil

## 사용 방법

### 기본 사용법

```python
from gpu_memory_monitor import GPUMemoryMonitor

# GPU와 CPU 모두 모니터링
monitor = GPUMemoryMonitor(use_gpu=True)

# CPU 메모리 확인
monitor.print_cpu_memory("CPU 상태")

# GPU 메모리 확인
monitor.print_gpu_memory("GPU 상태")

# 전체 시스템 메모리 상태 확인
monitor.print_memory_usage("시스템 상태", include_cpu=True)

# 모니터링 가능 여부 확인
if monitor.has_gpu:
    print("GPU 모니터링 가능")
if monitor.has_cpu:
    print("CPU 모니터링 가능")
```

## 출력 예시

```
[2025-09-26 10:30:15] - gpu_memory_monitor - INFO - CPU 상태
  CPU: 8500.25 MB / 16384.00 MB (사용률: 51.9%)

[2025-09-26 10:30:15] - gpu_memory_monitor - INFO - GPU 상태
  GPU: 2048.50 MB / 8192.00 MB (사용률: 25.0%)

[2025-09-26 10:30:15] - gpu_memory_monitor - INFO - 시스템 상태
  CPU: 8500.25 MB / 16384.00 MB
  GPU: 2048.50 MB / 8192.00 MB
```

## 고급 사용법

### 커스텀 CuPy 인스턴스 사용

```python
import cupy as cp

# 특정 CuPy 인스턴스 사용
monitor = MemoryMonitorManager(cupy_instance=cp)
```

### 예외 처리

```python
from gpu_memory_monitor import GPUNotAvailableError, MemoryMonitorError

try:
    monitor = MemoryMonitorManager()
    gpu_info = monitor.get_gpu_memory()
except GPUNotAvailableError as e:
    print(f"GPU 사용 불가: {e}")
except MemoryMonitorError as e:
    print(f"메모리 모니터링 오류: {e}")
```

## 개발 환경 설정

### 개발 의존성 설치

```bash
pip install gpu-memory-monitor[dev]
```

### 테스트 실행

```bash
pytest tests/
```

### 코드 스타일 검사

패키지 설치 시 기본적인 코드 스타일 도구들이 자동으로 함께 설치됩니다. 다음 명령어로 코드 스타일을 검사하고 수정할 수 있습니다:

```bash
# 코드 자동 포맷팅
black .

# import 문 자동 정렬
isort .

# 타입 힌트 검사
mypy .
```

추가 개발 도구가 필요한 경우 다음과 같이 설치할 수 있습니다:
```bash
pip install gpu-memory-monitor[dev]
```

이 명령어를 통해 다음 추가 도구들이 설치됩니다:
- pytest-cov: 테스트 커버리지 측정
- flake8: 코드 린팅
- pylint: 정적 코드 분석
- sphinx: 문서 생성

## 기여하기

1. 이 저장소를 Fork 합니다
2. 새로운 Feature 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 Push 합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 추가 자료

- [API 문서](docs/API.md)
- [변경 이력](CHANGELOG.md)
- [기여 가이드](CONTRIBUTING.md)