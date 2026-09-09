import os
import sys
import threading
import tkinter as tk

import tracker


BG = "#0c0a18"
PANEL = "#17152b"
PANEL_ALT = "#201d3a"
TEXT = "#f4f0ff"
MUTED = "#aaa4c7"
ACCENT = "#5b8cff"
PINK = "#ff3f73"
VERSION = "0.1.0"


def resource_path(filename):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, filename)


class TrackerWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("TAG2.GG Tracker")
        self.root.geometry("640x430")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        try:
            self.root.iconphoto(
                True, tk.PhotoImage(file=resource_path("app-icon-192.png"))
            )
        except tk.TclError:
            pass

        self._build_layout()
        threading.Thread(target=self._run_tracker, daemon=True).start()
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def _build_layout(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=28, pady=(24, 18))

        tk.Label(
            header,
            text="TAG2.GG",
            bg=BG,
            fg=PINK,
            font=("Segoe UI", 24, "bold"),
        ).pack(side="left")
        tk.Label(
            header,
            text=" Tracker",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 22, "bold"),
        ).pack(side="left")

        instructions = tk.Frame(self.root, bg=PANEL)
        instructions.pack(fill="x", padx=28, pady=(0, 14))

        self._section(
            instructions,
            "⚙  사용법",
            [
                "1. RPCS3를 먼저 실행하세요.",
                "2. Tekken Tag Tournament 2를 실행하세요.",
                "3. 이 프로그램을 실행한 상태로 온라인 대전을 진행하세요.",
            ],
            ACCENT,
        )
        self._section(
            instructions,
            "⚠  주의사항",
            [
                "온라인 대전만 기록됩니다.",
                "오프라인 대전은 자동으로 무시됩니다.",
            ],
            PINK,
        )

        footer = tk.Frame(self.root, bg=PANEL_ALT)
        footer.pack(fill="x", padx=28, pady=(0, 20))
        tk.Label(
            footer,
            text="●  프로그램이 실행 중입니다",
            bg=PANEL_ALT,
            fg=ACCENT,
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=11,
        ).pack(anchor="w")
        tk.Label(
            footer,
            text=f"Version {VERSION}\nDeveloped by legbreaker\nCopyright © 2026 legbreaker",
            justify="right",
            anchor="e",
            bg=PANEL_ALT,
            fg=MUTED,
            font=("Segoe UI", 9),
            padx=14,
            pady=(0, 11),
        ).pack(anchor="e")

    @staticmethod
    def _section(parent, heading, lines, color):
        block = tk.Frame(parent, bg=PANEL)
        block.pack(fill="x", padx=20, pady=(16, 2))
        tk.Label(
            block,
            text=heading,
            bg=PANEL,
            fg=color,
            font=("Segoe UI", 13, "bold"),
            anchor="w",
        ).pack(fill="x")
        tk.Label(
            block,
            text="\n".join(lines),
            justify="left",
            anchor="w",
            bg=PANEL,
            fg=TEXT,
            font=("Segoe UI", 11),
            padx=4,
            pady=8,
        ).pack(fill="x")

    @staticmethod
    def _run_tracker():
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        try:
            with open(os.devnull, "w", encoding="utf-8") as sink:
                sys.stdout = sink
                sys.stderr = sink
                tracker.TTT2Tracker().run()
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr


if __name__ == "__main__":
    root = tk.Tk()
    TrackerWindow(root)
    root.mainloop()
