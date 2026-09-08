import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from pdf_to_png import convert_pdf_to_images

BG = "#f4f5f7"
CARD_BG = "#ffffff"
BORDER = "#e2e4e9"
TEXT = "#1f2430"
SUBTEXT = "#8a8f9c"
ACCENT = "#4f6df5"
ACCENT_HOVER = "#3d59e0"
ACCENT_DISABLED = "#c3cbf5"
FONT_FAMILY = "Segoe UI"


class PdfToPngApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("PDF to PNG 변환기")
        self.root.geometry("520x360")
        self.root.minsize(520, 360)
        self.root.configure(bg=BG)

        self.pdf_path: Path | None = None

        self._build_style()

        outer = tk.Frame(root, bg=BG)
        outer.pack(fill="both", expand=True, padx=20, pady=(18, 0))

        # 헤더
        header = tk.Frame(outer, bg=BG)
        header.pack(fill="x", pady=(0, 14))
        tk.Label(
            header, text="PDF → PNG 변환기", bg=BG, fg=TEXT,
            font=(FONT_FAMILY, 16, "bold"),
        ).pack(anchor="w")
        tk.Label(
            header, text="PDF의 각 페이지를 개별 PNG 이미지로 저장합니다.",
            bg=BG, fg=SUBTEXT, font=(FONT_FAMILY, 9),
        ).pack(anchor="w")

        # 파일 선택 카드
        file_card = self._card(outer)
        file_card.pack(fill="x", pady=(0, 12))

        file_row = tk.Frame(file_card, bg=CARD_BG)
        file_row.pack(fill="x", padx=16, pady=14)

        self.load_button = self._accent_button(
            file_row, "파일 불러오기", self.load_file
        )
        self.load_button.pack(side="left")

        self.file_label = tk.Label(
            file_row, text="선택된 파일 없음", bg=CARD_BG, fg=SUBTEXT,
            font=(FONT_FAMILY, 9), anchor="w",
        )
        self.file_label.pack(side="left", padx=(14, 0), fill="x", expand=True)

        # 옵션 카드
        options_card = self._card(outer)
        options_card.pack(fill="x", pady=(0, 12))

        options_inner = tk.Frame(options_card, bg=CARD_BG)
        options_inner.pack(fill="x", padx=16, pady=14)

        tk.Label(
            options_inner, text="옵션", bg=CARD_BG, fg=TEXT,
            font=(FONT_FAMILY, 10, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        dpi_row = tk.Frame(options_inner, bg=CARD_BG)
        dpi_row.pack(fill="x", pady=(0, 8))
        tk.Label(
            dpi_row, text="해상도(DPI)", bg=CARD_BG, fg=TEXT, font=(FONT_FAMILY, 9),
        ).pack(side="left")
        self.dpi_var = tk.IntVar(value=96)
        dpi_spinbox = ttk.Spinbox(
            dpi_row, from_=50, to=600, increment=24, textvariable=self.dpi_var,
            width=6, font=(FONT_FAMILY, 9),
        )
        dpi_spinbox.pack(side="left", padx=8)
        tk.Label(
            dpi_row, text="낮을수록 용량이 작아집니다", bg=CARD_BG, fg=SUBTEXT,
            font=(FONT_FAMILY, 8),
        ).pack(side="left")

        self.grayscale_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options_inner, text="흑백(그레이스케일)으로 저장",
            variable=self.grayscale_var, style="Option.TCheckbutton",
        ).pack(anchor="w", pady=2)

        self.optimize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_inner, text="PNG 최적화 (재압축, 컬러 256색 축소)",
            variable=self.optimize_var, style="Option.TCheckbutton",
        ).pack(anchor="w", pady=2)

        # 시작 버튼
        self.start_button = self._accent_button(
            outer, "시작하기", self.start_conversion, big=True
        )
        self.start_button.pack(fill="x", pady=(0, 12))
        self._set_button_enabled(self.start_button, False)

        # 진행 표시줄
        self.progress = ttk.Progressbar(
            outer, mode="determinate", style="Accent.Horizontal.TProgressbar"
        )
        self.progress.pack(fill="x", pady=(0, 10))

        # 상태바
        status_bar = tk.Frame(root, bg=BORDER, height=28)
        status_bar.pack(side="bottom", fill="x")
        self.status_var = tk.StringVar(value="대기 중")
        tk.Label(
            status_bar, textvariable=self.status_var, bg=BORDER, fg=SUBTEXT,
            font=(FONT_FAMILY, 9), anchor="w", padx=12,
        ).pack(fill="both", expand=True)

    # ---------- 스타일 헬퍼 ----------

    def _build_style(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure(
            "TSpinbox", fieldbackground="#ffffff", background="#ffffff",
            bordercolor=BORDER, arrowsize=12,
        )
        style.configure(
            "Option.TCheckbutton", background=CARD_BG, foreground=TEXT,
            font=(FONT_FAMILY, 9),
        )
        style.map("Option.TCheckbutton", background=[("active", CARD_BG)])

        style.configure(
            "Accent.Horizontal.TProgressbar", troughcolor="#e9ebf3",
            background=ACCENT, bordercolor="#e9ebf3", lightcolor=ACCENT,
            darkcolor=ACCENT, thickness=8,
        )

    def _card(self, parent: tk.Widget) -> tk.Frame:
        card = tk.Frame(parent, bg=CARD_BG, highlightbackground=BORDER,
                         highlightthickness=1, bd=0)
        return card

    def _accent_button(self, parent, text, command, big=False) -> tk.Button:
        btn = tk.Button(
            parent, text=text, command=command,
            bg=ACCENT, fg="white", activebackground=ACCENT_HOVER,
            activeforeground="white", disabledforeground="#eef0fb",
            font=(FONT_FAMILY, 10, "bold" if big else "normal"),
            relief="flat", bd=0, cursor="hand2",
            padx=16, pady=10 if big else 6,
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT_HOVER) if btn["state"] != "disabled" else None)
        btn.bind("<Leave>", lambda e: btn.config(bg=ACCENT) if btn["state"] != "disabled" else None)
        return btn

    def _set_button_enabled(self, btn: tk.Button, enabled: bool) -> None:
        btn.configure(
            state="normal" if enabled else "disabled",
            bg=ACCENT if enabled else ACCENT_DISABLED,
        )

    # ---------- 동작 ----------

    def load_file(self) -> None:
        path = filedialog.askopenfilename(
            title="PDF 파일 선택", filetypes=[("PDF 파일", "*.pdf")]
        )
        if path:
            self.pdf_path = Path(path)
            self.file_label.config(text=self.pdf_path.name, fg=TEXT)
            self._set_button_enabled(self.start_button, True)
            self.status_var.set("파일이 선택되었습니다. 시작하기를 눌러주세요.")

    def start_conversion(self) -> None:
        if self.pdf_path is None:
            return
        self._set_button_enabled(self.load_button, False)
        self._set_button_enabled(self.start_button, False)
        self.progress.config(value=0)
        self.status_var.set("변환 중...")
        threading.Thread(target=self._run_conversion, daemon=True).start()

    def _run_conversion(self) -> None:
        pdf_path = self.pdf_path
        output_dir = pdf_path.with_suffix("")
        try:
            def on_progress(current: int, total: int) -> None:
                self.root.after(0, self._update_progress, current, total)

            convert_pdf_to_images(
                pdf_path, output_dir, dpi=self.dpi_var.get(),
                grayscale=self.grayscale_var.get(),
                optimize=self.optimize_var.get(),
                on_progress=on_progress,
            )
        except Exception as exc:
            self.root.after(0, self._on_error, str(exc))
            return
        self.root.after(0, self._on_done, output_dir)

    def _update_progress(self, current: int, total: int) -> None:
        self.progress.config(maximum=total, value=current)
        self.status_var.set(f"변환 중... ({current}/{total})")

    def _on_done(self, output_dir: Path) -> None:
        self.status_var.set(f"완료: {output_dir} 폴더에 저장되었습니다.")
        self._set_button_enabled(self.load_button, True)
        self._set_button_enabled(self.start_button, True)
        messagebox.showinfo("완료", f"변환이 완료되었습니다.\n저장 위치: {output_dir}")

    def _on_error(self, message: str) -> None:
        self.status_var.set("오류가 발생했습니다.")
        self._set_button_enabled(self.load_button, True)
        self._set_button_enabled(self.start_button, True)
        messagebox.showerror("오류", message)


def main() -> None:
    root = tk.Tk()
    PdfToPngApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
