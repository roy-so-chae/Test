"""
배경 회색 → 흰색 변환기 (Windows .exe)
이미지 가장자리에서 연결된 회색 배경만 흰색으로 변환합니다.
바닥 음영(3D 그림자)도 포함하여 처리합니다.
"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import os
import threading
from collections import deque


class GrayToWhiteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("배경 회색→흰색 변환기")
        self.root.geometry("920x720")
        self.root.configure(bg="#f0f0f0")
        self.root.minsize(700, 600)

        self.loaded_files = []
        self.result_images = []
        self.current_index = 0
        self.processing = False

        self.build_ui()

    def build_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#2d3436", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="배경 회색 → 흰색 변환기",
                 font=("맑은 고딕", 16, "bold"), fg="white", bg="#2d3436").pack(pady=15)

        # Main area
        main = tk.Frame(self.root, bg="#f0f0f0")
        main.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)

        # Top: file controls
        file_frame = tk.LabelFrame(main, text="파일 선택", font=("맑은 고딕", 10, "bold"),
                                   bg="#f0f0f0", padx=10, pady=8)
        file_frame.pack(fill=tk.X, pady=(0, 8))

        btn_frame = tk.Frame(file_frame, bg="#f0f0f0")
        btn_frame.pack(fill=tk.X)
        tk.Button(btn_frame, text="파일 열기", font=("맑은 고딕", 10),
                  command=self.open_files, width=12, bg="#6c5ce7", fg="white",
                  relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(btn_frame, text="폴더 열기", font=("맑은 고딕", 10),
                  command=self.open_folder, width=12, bg="#0984e3", fg="white",
                  relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=(0, 8))
        self.file_label = tk.Label(btn_frame, text="선택된 파일 없음",
                                   font=("맑은 고딕", 9), bg="#f0f0f0", fg="#636e72")
        self.file_label.pack(side=tk.LEFT, padx=8)

        # Settings
        settings_frame = tk.LabelFrame(main, text="설정", font=("맑은 고딕", 10, "bold"),
                                       bg="#f0f0f0", padx=10, pady=8)
        settings_frame.pack(fill=tk.X, pady=(0, 8))

        # Gray brightness range
        row1 = tk.Frame(settings_frame, bg="#f0f0f0")
        row1.pack(fill=tk.X, pady=2)
        tk.Label(row1, text="회색 밝기 범위:", font=("맑은 고딕", 9),
                 bg="#f0f0f0", width=14, anchor="w").pack(side=tk.LEFT)
        self.min_brightness = tk.IntVar(value=80)
        self.max_brightness = tk.IntVar(value=245)
        tk.Label(row1, text="최소", font=("맑은 고딕", 8), bg="#f0f0f0").pack(side=tk.LEFT)
        tk.Scale(row1, from_=30, to=200, orient=tk.HORIZONTAL, variable=self.min_brightness,
                 length=150, bg="#f0f0f0", highlightthickness=0).pack(side=tk.LEFT, padx=4)
        tk.Label(row1, text="최대", font=("맑은 고딕", 8), bg="#f0f0f0").pack(side=tk.LEFT)
        tk.Scale(row1, from_=180, to=254, orient=tk.HORIZONTAL, variable=self.max_brightness,
                 length=150, bg="#f0f0f0", highlightthickness=0).pack(side=tk.LEFT, padx=4)

        # Saturation threshold
        row2 = tk.Frame(settings_frame, bg="#f0f0f0")
        row2.pack(fill=tk.X, pady=2)
        tk.Label(row2, text="채도 허용치:", font=("맑은 고딕", 9),
                 bg="#f0f0f0", width=14, anchor="w").pack(side=tk.LEFT)
        self.sat_threshold = tk.IntVar(value=35)
        tk.Scale(row2, from_=5, to=80, orient=tk.HORIZONTAL, variable=self.sat_threshold,
                 length=200, bg="#f0f0f0", highlightthickness=0).pack(side=tk.LEFT, padx=4)
        tk.Label(row2, text="높일수록 색이 있는 배경도 포함", font=("맑은 고딕", 8),
                 bg="#f0f0f0", fg="#b2bec3").pack(side=tk.LEFT, padx=8)

        # Edge feathering
        row3 = tk.Frame(settings_frame, bg="#f0f0f0")
        row3.pack(fill=tk.X, pady=2)
        tk.Label(row3, text="경계 부드럽게:", font=("맑은 고딕", 9),
                 bg="#f0f0f0", width=14, anchor="w").pack(side=tk.LEFT)
        self.feather = tk.IntVar(value=15)
        tk.Scale(row3, from_=0, to=50, orient=tk.HORIZONTAL, variable=self.feather,
                 length=200, bg="#f0f0f0", highlightthickness=0).pack(side=tk.LEFT, padx=4)
        tk.Label(row3, text="경계 블렌딩 강도", font=("맑은 고딕", 8),
                 bg="#f0f0f0", fg="#b2bec3").pack(side=tk.LEFT, padx=8)

        # Format selection
        row4 = tk.Frame(settings_frame, bg="#f0f0f0")
        row4.pack(fill=tk.X, pady=2)
        tk.Label(row4, text="저장 형식:", font=("맑은 고딕", 9),
                 bg="#f0f0f0", width=14, anchor="w").pack(side=tk.LEFT)
        self.save_format = tk.StringVar(value="PNG")
        for fmt in ["PNG", "JPG", "WEBP"]:
            tk.Radiobutton(row4, text=fmt, variable=self.save_format, value=fmt,
                           font=("맑은 고딕", 9), bg="#f0f0f0").pack(side=tk.LEFT, padx=8)

        # Action buttons
        action_frame = tk.Frame(main, bg="#f0f0f0")
        action_frame.pack(fill=tk.X, pady=(0, 8))

        self.btn_convert = tk.Button(action_frame, text="변환하기", font=("맑은 고딕", 11, "bold"),
                                     command=self.start_convert, width=14, bg="#6c5ce7", fg="white",
                                     relief=tk.FLAT, cursor="hand2", state=tk.DISABLED)
        self.btn_convert.pack(side=tk.LEFT, padx=(0, 8))

        self.btn_save = tk.Button(action_frame, text="저장하기", font=("맑은 고딕", 11, "bold"),
                                  command=self.save_results, width=14, bg="#00b894", fg="white",
                                  relief=tk.FLAT, cursor="hand2", state=tk.DISABLED)
        self.btn_save.pack(side=tk.LEFT, padx=(0, 8))

        self.status_label = tk.Label(action_frame, text="", font=("맑은 고딕", 9),
                                     bg="#f0f0f0", fg="#636e72")
        self.status_label.pack(side=tk.LEFT, padx=8)

        # Progress bar
        self.progress = ttk.Progressbar(main, mode="determinate", length=400)
        self.progress.pack(fill=tk.X, pady=(0, 8))

        # Preview
        preview_frame = tk.LabelFrame(main, text="미리보기", font=("맑은 고딕", 10, "bold"),
                                      bg="#f0f0f0", padx=8, pady=8)
        preview_frame.pack(fill=tk.BOTH, expand=True)

        preview_inner = tk.Frame(preview_frame, bg="#f0f0f0")
        preview_inner.pack(fill=tk.BOTH, expand=True)

        # Original preview
        left = tk.Frame(preview_inner, bg="#f0f0f0")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))
        tk.Label(left, text="원본", font=("맑은 고딕", 9, "bold"), bg="#f0f0f0").pack()
        self.canvas_orig = tk.Canvas(left, bg="#e0e0e0", highlightthickness=1,
                                     highlightbackground="#ccc")
        self.canvas_orig.pack(fill=tk.BOTH, expand=True)

        # Result preview
        right = tk.Frame(preview_inner, bg="#f0f0f0")
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(4, 0))
        tk.Label(right, text="변환 결과", font=("맑은 고딕", 9, "bold"), bg="#f0f0f0").pack()
        self.canvas_result = tk.Canvas(right, bg="#e0e0e0", highlightthickness=1,
                                       highlightbackground="#ccc")
        self.canvas_result.pack(fill=tk.BOTH, expand=True)

        # Nav buttons for multi-file
        nav_frame = tk.Frame(preview_frame, bg="#f0f0f0")
        nav_frame.pack(fill=tk.X, pady=(6, 0))
        self.btn_prev = tk.Button(nav_frame, text="◀ 이전", font=("맑은 고딕", 9),
                                  command=self.prev_image, state=tk.DISABLED, bg="#dfe6e9",
                                  relief=tk.FLAT, cursor="hand2")
        self.btn_prev.pack(side=tk.LEFT)
        self.nav_label = tk.Label(nav_frame, text="", font=("맑은 고딕", 9), bg="#f0f0f0")
        self.nav_label.pack(side=tk.LEFT, padx=16)
        self.btn_next = tk.Button(nav_frame, text="다음 ▶", font=("맑은 고딕", 9),
                                  command=self.next_image, state=tk.DISABLED, bg="#dfe6e9",
                                  relief=tk.FLAT, cursor="hand2")
        self.btn_next.pack(side=tk.LEFT)

        # Keep references for PhotoImage (prevent GC)
        self._photo_orig = None
        self._photo_result = None

    def open_files(self):
        paths = filedialog.askopenfilenames(
            title="이미지 파일 선택",
            filetypes=[("이미지 파일", "*.png *.jpg *.jpeg *.webp *.bmp *.tiff"),
                       ("모든 파일", "*.*")])
        if paths:
            self.loaded_files = list(paths)
            self.result_images = []
            self.current_index = 0
            self.file_label.config(text=f"{len(self.loaded_files)}개 파일 선택됨")
            self.btn_convert.config(state=tk.NORMAL)
            self.btn_save.config(state=tk.DISABLED)
            self.show_original_preview(0)

    def open_folder(self):
        folder = filedialog.askdirectory(title="이미지 폴더 선택")
        if folder:
            exts = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"}
            self.loaded_files = [os.path.join(folder, f) for f in sorted(os.listdir(folder))
                                 if os.path.splitext(f)[1].lower() in exts]
            self.result_images = []
            self.current_index = 0
            if not self.loaded_files:
                self.file_label.config(text="이미지 파일이 없습니다")
                return
            self.file_label.config(text=f"{len(self.loaded_files)}개 파일 선택됨")
            self.btn_convert.config(state=tk.NORMAL)
            self.btn_save.config(state=tk.DISABLED)
            self.show_original_preview(0)

    def show_original_preview(self, index):
        if index < 0 or index >= len(self.loaded_files):
            return
        img = Image.open(self.loaded_files[index])
        self._photo_orig = self._fit_to_canvas(img, self.canvas_orig)
        self.canvas_orig.delete("all")
        self.canvas_orig.create_image(
            self.canvas_orig.winfo_width() // 2, self.canvas_orig.winfo_height() // 2,
            image=self._photo_orig, anchor=tk.CENTER)
        self.update_nav()

    def show_result_preview(self, index):
        if index < 0 or index >= len(self.result_images):
            return
        self._photo_result = self._fit_to_canvas(self.result_images[index], self.canvas_result)
        self.canvas_result.delete("all")
        self.canvas_result.create_image(
            self.canvas_result.winfo_width() // 2, self.canvas_result.winfo_height() // 2,
            image=self._photo_result, anchor=tk.CENTER)

    def _fit_to_canvas(self, img, canvas):
        canvas.update_idletasks()
        cw = max(canvas.winfo_width(), 100)
        ch = max(canvas.winfo_height(), 100)
        iw, ih = img.size
        ratio = min(cw / iw, ch / ih, 1.0)
        new_size = (max(int(iw * ratio), 1), max(int(ih * ratio), 1))
        resized = img.resize(new_size, Image.LANCZOS)
        return ImageTk.PhotoImage(resized)

    def update_nav(self):
        total = len(self.loaded_files)
        if total > 1:
            self.nav_label.config(text=f"{self.current_index + 1} / {total}")
            self.btn_prev.config(state=tk.NORMAL if self.current_index > 0 else tk.DISABLED)
            self.btn_next.config(state=tk.NORMAL if self.current_index < total - 1 else tk.DISABLED)
        else:
            self.nav_label.config(text="")
            self.btn_prev.config(state=tk.DISABLED)
            self.btn_next.config(state=tk.DISABLED)

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_original_preview(self.current_index)
            if self.current_index < len(self.result_images):
                self.show_result_preview(self.current_index)

    def next_image(self):
        if self.current_index < len(self.loaded_files) - 1:
            self.current_index += 1
            self.show_original_preview(self.current_index)
            if self.current_index < len(self.result_images):
                self.show_result_preview(self.current_index)

    def start_convert(self):
        if self.processing or not self.loaded_files:
            return
        self.processing = True
        self.btn_convert.config(state=tk.DISABLED)
        self.btn_save.config(state=tk.DISABLED)
        self.result_images = []
        self.progress["value"] = 0
        threading.Thread(target=self.convert_all, daemon=True).start()

    def convert_all(self):
        total = len(self.loaded_files)
        for i, path in enumerate(self.loaded_files):
            self.root.after(0, lambda i=i, p=path: self.status_label.config(
                text=f"({i+1}/{total}) {os.path.basename(p)} 처리 중..."))
            try:
                img = Image.open(path).convert("RGB")
                result = self.process_image(img)
                self.result_images.append(result)
            except Exception as e:
                self.result_images.append(Image.open(path))
                print(f"Error processing {path}: {e}")
            self.root.after(0, lambda v=(i + 1) / total * 100: self.progress.configure(value=v))

        self.root.after(0, self.convert_done)

    def convert_done(self):
        self.processing = False
        self.btn_convert.config(state=tk.NORMAL)
        self.btn_save.config(state=tk.NORMAL)
        self.status_label.config(text=f"{len(self.result_images)}개 파일 변환 완료!")
        self.current_index = 0
        self.show_original_preview(0)
        self.show_result_preview(0)

    def process_image(self, img):
        """
        Flood-fill 방식: 이미지 가장자리에서 시작하여 연결된 회색 픽셀만 흰색으로 변환.
        제품 본체의 회색은 건드리지 않고, 배경+바닥 음영만 처리.
        """
        arr = np.array(img, dtype=np.float64)
        h, w, _ = arr.shape

        min_b = self.min_brightness.get()
        max_b = self.max_brightness.get()
        sat_t = self.sat_threshold.get()
        feather = self.feather.get()

        # Build a mask of pixels that could be "gray background"
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        max_c = np.maximum(np.maximum(r, g), b)
        min_c = np.minimum(np.minimum(r, g), b)
        lightness = (max_c + min_c) / 2.0
        delta = max_c - min_c
        denom = 255.0 - np.abs(2.0 * lightness - 255.0)
        saturation = np.where(denom > 0, (delta / denom) * 100.0, 0.0)

        # A pixel is "gray-ish" if within brightness range and low saturation
        gray_mask = (lightness >= min_b) & (lightness <= max_b) & (saturation <= sat_t)

        # Flood-fill from all edge pixels that are gray
        visited = np.zeros((h, w), dtype=bool)
        bg_mask = np.zeros((h, w), dtype=bool)
        queue = deque()

        # Seed from all 4 edges
        for x in range(w):
            if gray_mask[0, x] and not visited[0, x]:
                queue.append((0, x))
                visited[0, x] = True
            if gray_mask[h - 1, x] and not visited[h - 1, x]:
                queue.append((h - 1, x))
                visited[h - 1, x] = True
        for y in range(h):
            if gray_mask[y, 0] and not visited[y, 0]:
                queue.append((y, 0))
                visited[y, 0] = True
            if gray_mask[y, w - 1] and not visited[y, w - 1]:
                queue.append((y, w - 1))
                visited[y, w - 1] = True

        # BFS flood-fill
        while queue:
            cy, cx = queue.popleft()
            bg_mask[cy, cx] = True
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx] and gray_mask[ny, nx]:
                    visited[ny, nx] = True
                    queue.append((ny, nx))

        # Apply feathering: compute distance from bg boundary for smooth blend
        if feather > 0:
            from scipy.ndimage import distance_transform_edt
            # Distance of bg pixels from the boundary (non-bg neighbors)
            inner_dist = distance_transform_edt(bg_mask)
            blend = np.clip(inner_dist / max(feather, 1), 0, 1)
        else:
            blend = bg_mask.astype(np.float64)

        # Apply: blend toward white
        for c in range(3):
            arr[:, :, c] = arr[:, :, c] + (255.0 - arr[:, :, c]) * blend

        arr = np.clip(arr, 0, 255).astype(np.uint8)
        return Image.fromarray(arr)

    def save_results(self):
        if not self.result_images:
            return

        fmt = self.save_format.get().lower()
        ext = "jpg" if fmt == "jpg" else fmt

        if len(self.result_images) == 1:
            path = filedialog.asksaveasfilename(
                title="저장",
                defaultextension=f".{ext}",
                filetypes=[(f"{fmt.upper()} 파일", f"*.{ext}")],
                initialfile=os.path.splitext(os.path.basename(self.loaded_files[0]))[0] + f"_white.{ext}")
            if path:
                self._save_one(self.result_images[0], path, fmt)
                self.status_label.config(text=f"저장 완료: {os.path.basename(path)}")
        else:
            folder = filedialog.askdirectory(title="저장할 폴더 선택")
            if folder:
                for i, result in enumerate(self.result_images):
                    base = os.path.splitext(os.path.basename(self.loaded_files[i]))[0]
                    out_path = os.path.join(folder, f"{base}_white.{ext}")
                    self._save_one(result, out_path, fmt)
                self.status_label.config(text=f"{len(self.result_images)}개 파일 저장 완료!")

    def _save_one(self, img, path, fmt):
        if fmt == "jpg":
            if img.mode == "RGBA":
                img = img.convert("RGB")
            img.save(path, "JPEG", quality=95)
        elif fmt == "webp":
            img.save(path, "WEBP", quality=95)
        else:
            img.save(path, "PNG")


if __name__ == "__main__":
    root = tk.Tk()
    app = GrayToWhiteApp(root)
    root.mainloop()
