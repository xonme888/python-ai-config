from setuptools import setup, find_packages

setup(
    name="gpu-memory-monitor",
    version="0.1.0",
    description="A simple GPU and CPU memory monitoring tool using CuPy",
    author="victor",
    author_email="xonme888@gmail.com",
    packages=find_packages(include=["gpu_memory_monitor*"]),
    install_requires=[
        "psutil>=5.9.0",
        "packaging>=23.0",
    ],
    extras_require={
        "cuda11": ["cupy-cuda11x>=12.0.0"],
        "cuda12": ["cupy-cuda12x>=12.0.0"],
        "dev": [
            "black>=23.9.1",
            "isort>=5.12.0",
            "mypy>=1.5.1",
            "pytest>=7.4.2",
            "pytest-cov>=4.1.0",
            "flake8>=6.1.0",
        ],
    },
    python_requires="==3.11.*",  # Python 3.11.x 버전만 지원
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
