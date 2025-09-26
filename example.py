"""Example usage of System Monitor."""

from system_monitor import SystemMonitor, MemoryConverter, setup_logger

# 로깅 설정 (Colab과 VSCode 모두에서 동작)
logger = setup_logger('system_monitor', force_setup=True)


def main():
    """Example usage."""
    print("GPU Memory Monitor - Example Usage")
    print("=" * 40)

    # CPU only monitoring (safe for all environments)
    print("\n1. CPU Only Monitoring:")
    cpu_monitor = SystemMonitor(use_gpu=False)
    cpu_monitor.print_cpu_memory("Current CPU Memory")

    # Full system monitoring (works with or without GPU)
    print("\n2. Full System Monitoring:")
    monitor = SystemMonitor()
    print(f"   CPU Available: {monitor.has_cpu}")
    print(f"   GPU Available: {monitor.has_gpu}")
    monitor.print_memory_usage("System Status", include_cpu=True)

    # Manual memory info access
    print("\n3. Manual Memory Access:")
    cpu_info = monitor.get_cpu_memory()
    if cpu_info:
        print(f"   CPU: {cpu_info.used:.1f}MB/{cpu_info.total:.1f}MB "
              f"({cpu_info.usage_percent:.1f}%)")

    gpu_info = monitor.get_gpu_memory()
    if gpu_info:
        print(f"   GPU: {gpu_info.used:.1f}MB/{gpu_info.total:.1f}MB "
              f"({gpu_info.usage_percent:.1f}%)")
    else:
        print("   GPU: Not available")

    # Memory conversion utilities
    print("\n4. Memory Conversion Examples:")
    bytes_1gb = 1024 * 1024 * 1024
    mb_val = MemoryConverter.to_mb(bytes_1gb)
    gb_val = MemoryConverter.to_gb(bytes_1gb)
    print(f"   {bytes_1gb} bytes = {mb_val:.0f} MB")
    print(f"   {bytes_1gb} bytes = {gb_val:.0f} GB")
    formatted = MemoryConverter.format_memory(bytes_1gb, 'GB')
    print(f"   Formatted: {formatted}")


if __name__ == "__main__":
    main()
