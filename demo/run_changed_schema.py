from demo.demo_batches import (
    write_command_response_changed,
    write_meter_data_changed,
)


def main():
    print("Writing changed-schema demo batches...")
    write_meter_data_changed()
    write_command_response_changed()
    print("Changed-schema demo batches written.")


if __name__ == "__main__":
    main()
