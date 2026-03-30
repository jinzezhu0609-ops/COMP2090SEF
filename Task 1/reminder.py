class Reminder():
    remind_Before_Seconds = 300 # Remind 5 minutes before the start

    @staticmethod
    def check_reminders(reservations):
        messages = []

        for res in reservations:   
            if not res.is_active():  # Skip inactive reservations
                continue

            if res.is_past_start() and not res.ongoing_notified:
                messages_1 = f"[REMIND] Seat {res.seat.seat_id} reservation time is officially beginning"
                messages.append(messages_1)
                res.ongoing_notified = True

            seconds_to_start = res.time_to_start()   # Calculate time until reservation starts
            if 0 < seconds_to_start <= Reminder.remind_Before_Seconds and not res.start_notified:
                messages_2 = f"[REMIND] Seat {res.seat.seat_id} will start soon!"
                messages.append(messages_2)
                res.start_notified = True

            seconds_to_end = res.time_to_end()  # Calculate time reservation ends
            if 0 < seconds_to_end <= Reminder.remind_Before_Seconds and not res.end_notified:
                messages_3 = f"[REMIND] Seat {res.seat.seat_id} will end soon, please prepare to leave."
                messages.append(messages_3)
                res.end_notified = True

        return messages  # return all collected reminders