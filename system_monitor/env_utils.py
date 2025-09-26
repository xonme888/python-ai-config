"""Environment detection and setup utilities."""

import os
import sys
from typing import Dict, Any


def detect_environment() -> Dict[str, Any]:
    """
    현재 실행 환경을 감지합니다.

    Returns:
        환경 정보를 담은 딕셔너리
    """
    env_info = {
        "is_colab": False,
        "is_jupyter": False,
        "is_vscode": False,
        "is_terminal": False,
        "python_version": sys.version,
        "platform": sys.platform,
    }

    # Google Colab 감지
    try:
        import google.colab  # noqa: F401

        env_info["is_colab"] = True
    except ImportError:
        pass

    # Jupyter 환경 감지
    try:
        from IPython import get_ipython  # noqa: F401

        ipython = get_ipython()
        if ipython is not None:
            env_info["is_jupyter"] = True
            # Colab이 아닌 일반 Jupyter인지 확인
            if not env_info["is_colab"]:
                env_info["jupyter_type"] = type(ipython).__name__
    except ImportError:
        pass

    # VSCode 환경 감지
    if "VSCODE_PID" in os.environ or "TERM_PROGRAM" in os.environ:
        if os.environ.get("TERM_PROGRAM") == "vscode":
            env_info["is_vscode"] = True

    # 터미널 환경 감지
    special_envs = [
        env_info["is_colab"],
        env_info["is_jupyter"],
        env_info["is_vscode"],
    ]
    if not any(special_envs):
        env_info["is_terminal"] = True

    return env_info


def get_optimal_logging_config(
    env_info: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    환경에 최적화된 로깅 설정을 반환합니다.

    Args:
        env_info: 환경 정보 (없으면 자동 감지)

    Returns:
        로깅 설정 딕셔너리
    """
    if env_info is None:
        env_info = detect_environment()

    config = {
        "level": "INFO",
        "format": "%(asctime)s - [%(name)s] - %(levelname)s - %(message)s",
        "datefmt": "%H:%M:%S",
        "stream": sys.stdout,
        "force_color": False,
    }

    if env_info["is_colab"]:
        # Colab에서는 더 단순한 포맷과 강제 색상
        config.update(
            {
                "format": "[%(levelname)s] %(message)s",
                "datefmt": None,
                "force_color": True,
            }
        )
    elif env_info["is_jupyter"]:
        # Jupyter에서는 시간 포함하되 짧게
        config.update(
            {
                "format": "%(asctime)s [%(levelname)s] %(message)s",
                "datefmt": "%H:%M:%S",
            }
        )
    elif env_info["is_vscode"]:
        # VSCode에서는 상세한 로깅
        config.update(
            {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        )

    return config


def print_environment_info():
    """현재 환경 정보를 출력합니다."""
    env_info = detect_environment()

    print("환경 감지 결과:")
    print("-" * 30)

    if env_info["is_colab"]:
        print("Google Colab 환경")
    elif env_info["is_jupyter"]:
        jupyter_type = env_info.get("jupyter_type", "Unknown")
        print(f"Jupyter 환경 ({jupyter_type})")
    elif env_info["is_vscode"]:
        print("VSCode 환경")
    elif env_info["is_terminal"]:
        print("터미널 환경")
    else:
        print("알 수 없는 환경")

    print(f"Python: {env_info['python_version'].split()[0]}")
    print(f"플랫폼: {env_info['platform']}")

    # GPU 환경 체크
    try:
        import cupy

        print(f"CuPy: {cupy.__version__} (GPU 사용 가능)")
    except ImportError:
        print("CuPy: 미설치 (GPU 모니터링 불가)")

    try:
        import psutil

        print(f"psutil: {psutil.__version__} (CPU 모니터링 가능)")
    except ImportError:
        print("psutil: 미설치 (CPU 모니터링 불가)")


def setup_environment_optimized_monitor():
    """
    환경에 최적화된 SystemMonitor를 설정하고 반환합니다.

    Returns:
        설정된 SystemMonitor 인스턴스
    """
    from .monitor import SystemMonitor
    from .logging_config import setup_logger

    env_info = detect_environment()
    config = get_optimal_logging_config(env_info)

    # 환경 최적화 로깅 설정
    import logging

    level = getattr(logging, config["level"].upper())
    setup_logger("system_monitor", level=level, force_setup=True)

    # GPU 사용 여부 결정 (Colab에서는 더 적극적으로 GPU 시도)
    use_gpu = True
    if env_info["is_colab"]:
        # Colab에서는 GPU 런타임 체크를 더 관대하게
        try:
            import cupy

            # GPU 메모리 접근 테스트
            cupy.cuda.Device(0).compute_capability
            use_gpu = True
        except Exception:
            use_gpu = False

    monitor = SystemMonitor(use_gpu=use_gpu)

    # 환경 정보와 함께 초기화 메시지 출력
    if env_info["is_colab"]:
        print("Google Colab용 System Monitor가 초기화되었습니다.")
    elif env_info["is_jupyter"]:
        print("Jupyter용 System Monitor가 초기화되었습니다.")
    elif env_info["is_vscode"]:
        print("VSCode용 System Monitor가 초기화되었습니다.")
    else:
        print("System Monitor가 초기화되었습니다.")

    print(f"   CPU 모니터링: {'예' if monitor.has_cpu else '아니오'}")
    print(f"   GPU 모니터링: {'예' if monitor.has_gpu else '아니오'}")

    return monitor
