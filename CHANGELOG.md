# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- Network usage monitoring module
- Process-specific memory tracking module  
- Storage I/O monitoring module
- Performance metrics collection
- Historical data logging with persistence
- Web dashboard for real-time monitoring
- Integration with Jupyter widgets
- Export functionality (CSV, JSON, Prometheus metrics)

## [0.3.1] - 2025-01-16

### Added
- **환경 최적화 로깅 시스템**: Colab, Jupyter, VSCode 각각에 최적화된 로깅
- **자동 환경 감지**: Google Colab, Jupyter, VSCode, 터미널 환경 자동 인식
- **Colab 전용 최적화**: Google Colab에서 로그 출력 보장 및 GPU 런타임 자동 감지
- **환경별 설정 유틸리티**: `setup_environment_optimized_monitor()` 함수 추가
- **환경 정보 출력**: `print_environment_info()` 함수로 현재 환경 상태 확인
- **자동 설치 스크립트**: `install.sh` 스크립트로 환경별 최적 패키지 자동 설치
- **데모 스크립트**: 모든 기능을 보여주는 `demo.py` 추가
- **Colab 예제**: Google Colab 환경을 위한 전용 예제 파일

### Enhanced
- **로깅 시스템 완전 재작성**: 환경별 최적화된 포맷과 출력 방식
- **README.md 대폭 개선**: 환경별 상세한 사용법과 문제 해결 가이드 추가
- **setup.py 개선**: 환경별 옵션 설치(`gpu`, `colab`, `cuda11`, `cuda12`)
- **Python 호환성 확장**: Python 3.8+ 지원으로 확대

### Fixed
- **Colab 로그 출력 문제 해결**: 로깅이 제대로 표시되지 않던 문제 수정
- **VSCode 환경 감지 개선**: VSCode에서의 환경 감지 정확도 향상
- **Jupyter 호환성 향상**: 다양한 Jupyter 환경에서의 안정성 개선

### Documentation
- **완전한 사용 가이드**: 환경별 상세한 설정 및 사용법
- **문제 해결 섹션**: 일반적인 문제들에 대한 해결책 제시
- **API 문서 확장**: 모든 새로운 함수들에 대한 상세 문서

## [0.3.0] - 2025-01-16

### Changed
- **BREAKING**: Renamed package from `gpu_memory_monitor` to `system_monitor`
- Restructured project for better extensibility and future modules
- Updated all import paths and documentation

### Added  
- Modular architecture with `core/` and `monitors/` subdirectories
- Enhanced SystemMonitor class with improved error handling
- Backward compatibility aliases for existing code migration
- Comprehensive API documentation in README.md
- Development environment setup guide
- Contribution guidelines with coding standards
- Detailed usage examples for Colab and Jupyter environments

### Fixed
- Import path consistency across all modules
- Test coverage reporting accuracy
- Documentation formatting and structure

### Deprecated
- Old class names `GPUMemoryMonitor` and `MemoryMonitorManager` (use `SystemMonitor`)
- Direct imports from submodules (use main package imports)

### Removed
- Dependency.py complexity - simplified architecture
- Unused legacy code and comments
- Redundant test fixtures

## [0.2.0] - 2025-01-15

### Added
- Enhanced test coverage achieving 99% (169/171 lines)
- CPUMonitor and GPUMonitor class separation
- BaseMonitor abstract class for extensibility
- MemoryConverter utility class for unit conversions
- Comprehensive error handling and fallback mechanisms
- Type hints throughout the codebase
- pytest configuration with coverage reporting

### Changed
- Improved memory info data structure with MemoryInfo dataclass
- Better separation of concerns between monitoring components  
- Enhanced documentation with usage examples

### Fixed
- Memory calculation accuracy for edge cases
- GPU availability detection reliability
- Cross-platform compatibility issues

## [0.1.0] - 2025-09-26

### Added
- Initial release of GPU memory monitoring functionality
- SystemMonitor class for real-time GPU memory tracking
- Support for CuPy-based GPU memory monitoring  
- CPU memory monitoring using psutil
- Cross-platform compatibility (Linux, Windows, macOS)
- Python 3.11 to 3.12.11 support
- Basic test coverage setup

### Features
- Real-time GPU memory usage tracking
- CPU memory monitoring with psutil integration
- Memory usage formatting (MB, GB) with proper precision
- Safe fallback when GPU is not available
- Zero-dependency CPU monitoring
- Google Colab and Jupyter Notebook optimization

### Technical Details
- MIT License for open source distribution
- Setuptools-based packaging with proper metadata
- Clean package structure with __init__.py organization
- Basic error handling for missing dependencies

### Known Issues
- None reported for this release

[Unreleased]: https://github.com/xonme888/system-monitor/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/xonme888/system-monitor/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/xonme888/system-monitor/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/xonme888/system-monitor/releases/tag/v0.1.0