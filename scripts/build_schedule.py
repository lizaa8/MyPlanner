import argparse
import json


def build_schedule(minutes, assignment):
    blocks = []
    remaining = minutes

    # Save up to 10 minutes for wrapping up
    wrap_up = min(10, remaining)
    remaining -= wrap_up

    work_number = 1

    while remaining > 0:
        # Work for up to 45 minutes
        work_time = min(45, remaining)

        blocks.append({
            "type": "work",
            "minutes": work_time,
            "label": f"Work block {work_number}: {assignment}"
        })

        remaining -= work_time

        # Add a break if there is enough time left
        if remaining > 5:
            blocks.append({
                "type": "break",
                "minutes": 5,
                "label": "Short break"
            })
            remaining -= 5

        work_number += 1

    blocks.append({
        "type": "wrap_up",
        "minutes": wrap_up,
        "label": "Save progress and list next steps"
    })

    return {
        "assignment": assignment,
        "available_minutes": minutes,
        "total_scheduled_minutes": sum(
            block["minutes"] for block in blocks
        ),
        "blocks": blocks
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--minutes", type=int, required=True)
    parser.add_argument("--assignment", required=True)

    args = parser.parse_args()

    if args.minutes <= 0:
        parser.error("Minutes must be greater than zero")

    schedule = build_schedule(args.minutes, args.assignment)
    print(json.dumps(schedule, indent=2))
