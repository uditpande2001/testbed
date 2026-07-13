from demo.demo_batches import (
    write_command_response_baseline,
    write_meter_data_baseline,
)


def main():
    print("Writing baseline demo batches...")
    write_meter_data_baseline()
    write_command_response_baseline()
    print("Baseline demo batches written.")


if __name__ == "__main__":
    main()
