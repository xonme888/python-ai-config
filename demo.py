#!/usr/bin/env python3
"""
System Monitor Demo - 환경별 최적화 데모

이 스크립트는 다양한 환경(Colab, Jupyter, VSCode, 터미널)에서
System Monitor가 어떻게 작동하는지 보여줍니다.
"""

from system_monitor import (
    print_environment_info,
    setup_environment_optimized_monitor,
    setup_logger,
)


def main():
    """메인 데모 함수."""

    print("System Monitor v0.3.1 - 환경 최적화 데모")
    print("=" * 60)

    # 1. 환경 감지 및 정보 출력
    print("\n1단계: 환경 감지")
    print("-" * 30)
    print_environment_info()

    # 2. 환경 최적화 모니터 설정
    print("\n2단계: 환경 최적화 모니터 설정")
    print("-" * 40)
    monitor = setup_environment_optimized_monitor()

    # 3. 기본 메모리 모니터링
    print("\n3단계: 메모리 모니터링")
    print("-" * 30)
    monitor.print_memory_usage("현재 시스템 상태", include_cpu=True)

    # 4. 개별 모니터링 테스트
    print("\n4단계: 개별 모니터링 테스트")
    print("-" * 35)

    if monitor.has_cpu:
        monitor.print_cpu_memory("CPU 메모리 상태")
    else:
        print("경고: CPU 모니터링을 사용할 수 없습니다 (psutil 필요)")

    if monitor.has_gpu:
        monitor.print_gpu_memory("GPU 메모리 상태")
    else:
        print("정보: GPU 모니터링을 사용할 수 없습니다 (CuPy 필요)")

    # 5. 수동 메모리 접근 예제
    print("\n5단계: 수동 메모리 접근")
    print("-" * 30)

    cpu_info = monitor.get_cpu_memory()
    gpu_info = monitor.get_gpu_memory()

    print("메모리 정보 (상세):")
    if cpu_info:
        print(
            f"  CPU: {cpu_info.used:.1f}MB / {cpu_info.total:.1f}MB "
            f"({cpu_info.usage_percent:.1f}%)"
        )
    else:
        print("  CPU: 정보 없음")

    if gpu_info:
        print(
            f"  GPU: {gpu_info.used:.1f}MB / {gpu_info.total:.1f}MB "
            f"({gpu_info.usage_percent:.1f}%)"
        )
    else:
        print("  GPU: 정보 없음")

    # 6. 환경별 사용팁
    print("\n6단계: 환경별 사용팁")
    print("-" * 25)

    from system_monitor.env_utils import detect_environment

    env_info = detect_environment()

    if env_info["is_colab"]:
        print("Google Colab 사용팁:")
        print("  - GPU 런타임 활성화: 런타임 > 런타임 유형 변경 > GPU")
        print("  - 패키지 설치: !pip install psutil cupy-cuda12x")
        print("  - 권장 사용법:")
        print(
            "    from system_monitor import "
            "setup_environment_optimized_monitor"
        )
        print("    monitor = setup_environment_optimized_monitor()")

    elif env_info["is_jupyter"]:
        print("Jupyter 사용팁:")
        print("  - 로깅 활성화를 위해 setup_logger() 호출 필요")
        print("  - 권장 사용법:")
        print("    from system_monitor import SystemMonitor, setup_logger")
        print("    setup_logger('system_monitor', force_setup=True)")

    elif env_info["is_vscode"]:
        print("VSCode 사용팁:")
        print("  - 터미널에서 직접 실행 가능")
        print("  - 디버깅 모드에서 상세 로깅 제공")
        print("  - 권장 사용법:")
        print("    from system_monitor import SystemMonitor")
        print("    monitor = SystemMonitor()")

    else:
        print("터미널 사용팁:")
        print("  - 스크립트에서 직접 사용 가능")
        print("  - 권장 사용법:")
        print("    from system_monitor import SystemMonitor")
        print("    monitor = SystemMonitor()")

    print("\n데모 완료!")
    print("자세한 정보: README.md 참조")
    return monitor


if __name__ == "__main__":
    # 로깅 초기화 (강제)
    setup_logger("system_monitor", force_setup=True)

    # 데모 실행
    demo_monitor = main()

    print("\n" + "=" * 60)
    print("System Monitor가 성공적으로 설정되었습니다!")
    print("이제 demo_monitor 객체를 사용하여 메모리를 모니터링할 수 있습니다.")
