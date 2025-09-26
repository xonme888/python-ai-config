from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="system-monitor",
    version="0.3.1",
    description="System resource monitoring for Colab, Jupyter, VSCode",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="victor",
    author_email="xonme888@gmail.com",
    url="https://github.com/xonme888/system-monitor",
    packages=find_packages(include=["system_monitor*"]),
    install_requires=[
        "psutil>=5.9.0",
    ],
    extras_require={
        "gpu": ["cupy-cuda12x>=12.0.0"],  # 기본 GPU 지원
        "cuda11": ["cupy-cuda11x>=12.0.0"],
        "cuda12": ["cupy-cuda12x>=12.0.0"],
        "colab": ["cupy-cuda12x>=12.0.0"],  # Colab용 (보통 CUDA 12.x)
        "dev": [
            "black>=23.9.1",
            "isort>=5.12.0",
            "mypy>=1.5.1",
            "pytest>=7.4.2",
            "pytest-cov>=4.1.0",
            "flake8>=6.1.0",
        ],
    },
    python_requires=">=3.8",  # 더 넓은 호환성 지원
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Monitoring",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Environment :: GPU :: NVIDIA CUDA",
    ],
    keywords="monitoring memory gpu cpu colab jupyter vscode ml ai",
    project_urls={
        "Bug Reports": "https://github.com/xonme888/system-monitor/issues",
        "Source": "https://github.com/xonme888/system-monitor",
        "Documentation": "https://github.com/xonme888/system-monitor#readme",
    },
)
