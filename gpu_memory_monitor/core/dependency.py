from importlib.metadata import version, distributions
import logging
import warnings
from threading import Lock
from typing import List, Dict, Set, Optional
from packaging.version import parse as parse_version

logger = logging.getLogger(__name__)


class DependencyManager:
    """패키지 의존성 관리 클래스"""

    def __init__(self):
        self._lock = Lock()
        self._installed_packages: Dict[str, str] = {}
        self._checked_packages: Set[str] = set()
        self._refresh_packages()

    def _refresh_packages(self) -> None:
        """현재 설치된 패키지 목록 갱신"""
        try:
            self._installed_packages = {
                dist.metadata["Name"].lower(): dist.version
                for dist in distributions()
            }
        except Exception as e:
            logger.warning(f"Failed to get installed packages: {e}")
            self._installed_packages = {}

    def check_dependency(
        self,
        package_name: str,
        min_version: Optional[str] = None,
        raise_error: bool = False,
    ) -> bool:
        """
        의존성 패키지 확인

        Args:
            package_name: 확인할 패키지 이름
            min_version: 최소 버전 요구사항
            raise_error: 오류 발생 시 예외 발생 여부

        Returns:
            bool: 패키지가 설치되어 있고 버전 요구사항을 만족하면 True

        Raises:
            ImportError: raise_error=True이고 패키지가 없거나 버전이 맞지 않을 때
        """
        if not package_name:
            raise ValueError("Package name cannot be empty")

        package_name = package_name.lower()  # 패키지 이름 정규화

        with self._lock:
            # 이미 확인한 패키지는 다시 확인하지 않음
            if package_name in self._checked_packages:
                return True

            installed_version = self._installed_packages.get(package_name)

            if not installed_version:
                msg = f"Required package '{package_name}' is not installed"
                if raise_error:
                    raise ImportError(msg)
                warnings.warn(msg, ImportWarning)
                return False

            if min_version:
                try:
                    if parse_version(installed_version) < parse_version(
                        min_version
                    ):
                        msg = (
                            f"Package '{package_name}' version {installed_version} "
                            f"is installed but version >={min_version} is required"
                        )
                        if raise_error:
                            raise ImportError(msg)
                        warnings.warn(msg, ImportWarning)
                        return False
                except Exception as e:
                    logger.warning(
                        f"Failed to compare versions for {package_name}: {e}"
                    )
                    return False

            self._checked_packages.add(package_name)
            return True

    def check_conflicts(self, packages: List[str]) -> None:
        """
        패키지 간 충돌 확인

        Args:
            packages: 확인할 패키지 목록
        """
        if not packages:
            return

        with self._lock:
            for pkg in packages:
                pkg = pkg.lower()  # 패키지 이름 정규화
                if pkg.startswith("cupy-"):
                    cupy_packages = [
                        p
                        for p in self._installed_packages
                        if p.startswith("cupy-")
                    ]
                    if len(cupy_packages) > 1:
                        warnings.warn(
                            f"Multiple CuPy packages detected: {', '.join(cupy_packages)}. "
                            f"This may cause conflicts.",
                            RuntimeWarning,
                        )
                        break
