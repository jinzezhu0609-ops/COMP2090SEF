import datetime

class Reservation:
    def __init__(self, user, seat, start_time, duration_minutes):
        self.user = user
        self.seat = seat
        self.start_time = start_time
        self.duration_minutes = duration_minutes
        self.end_time = start_time + datetime.timedelta(minutes = duration_minutes)

    def __str__(self):
        return (f"{self.user.username} reserved seat {self.seat.seat_id} "
                f"from {self.start_time.strftime('%Y-%m-%d %H:%M')} "
                f"to {self.end_time.strftime('%Y-%m-%d %H:%M')} "
                f"({self.duration_minutes} min)")

    def __repr__(self):
        return f"Reservation(user={self.user.username}, seat={self.seat.seat_id}, start={self.start_time})"

    def is_active(self):
        return datetime.datetime.now() < self.end_time

    def time_to_start(self):
        diff = self.start_time - datetime.datetime.now()
        return diff.total_seconds() if diff.total_seconds() > 0 else 0

    def time_to_end(self):
        diff = self.end_time - datetime.datetime.now()
        return diff.total_seconds() if diff.total_seconds() > 0 else 0