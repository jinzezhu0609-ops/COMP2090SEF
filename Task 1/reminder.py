class Reminder:
    REMIND_BEFORE_SECONDS = 5 * 60

    @staticmethod
    def check_reminders(reservations):
        messages = []

        for res in reservations:
            if not res.is_active():
                continue

            seconds_to_start = res.time_to_start()
            if 0 < seconds_to_start <= Reminder.REMIND_BEFORE_SECONDS:
                messages = f"[REMIND] Seat {res.seat.seat_id} will start soon!"
                messages.append(messages)

            seconds_to_end = res.time_to_end()
            if 0 < seconds_to_end <= Reminder.REMIND_BEFORE_SECONDS:
                messages = f"[REMIND] Seat {res.seat.seat_id} will end soon, please prepare to leave."
                messages.append(messages)
        return messages