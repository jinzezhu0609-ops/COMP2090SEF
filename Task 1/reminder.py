class Reminder:
    REMIND_BEFORE_SECONDS = 300 # Remind 5 minutes before the start

    @staticmethod
    def check_reminders(reservations):
        messages = []

        for res in reservations:   
            if not res.is_active():  # Skip inactive reservations
                continue

            seconds_to_start = res.time_to_start()   # Calculate time until reservation starts
            if 0 < seconds_to_start <= Reminder.REMIND_BEFORE_SECONDS:
                messages = f"[REMIND] Seat {res.seat.seat_id} will start soon!"
                messages.append(messages)

            seconds_to_end = res.time_to_end()  # Calculate time reservation ends
            if 0 < seconds_to_end <= Reminder.REMIND_BEFORE_SECONDS:
                messages = f"[REMIND] Seat {res.seat.seat_id} will end soon, please prepare to leave."
                messages.append(messages)

        return messages  # return all collected reminders
