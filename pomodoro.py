class PomodoroTimer:

    def __init__(self):
        self.work_minutes = 25
        self.break_minutes = 5

        self.remaining = self.work_minutes * 60

        self.running = False
        self.on_break = False

    def reset(self):
        self.running = False
        self.on_break = False
        self.remaining = self.work_minutes * 60

    def toggle(self):
        self.running = not self.running

    def tick(self):
        if not self.running:
            return False

        self.remaining -= 1

        if self.remaining <= 0:
            self.on_break = not self.on_break

            if self.on_break:
                self.remaining = self.break_minutes * 60
            else:
                self.remaining = self.work_minutes * 60

            return True

        return False

    def time_string(self):
        minutes = self.remaining // 60
        seconds = self.remaining % 60

        return f"{minutes:02}:{seconds:02}"