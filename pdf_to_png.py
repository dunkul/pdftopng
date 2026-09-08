import argparse
import sys
from pathlib import Path
from typing import Callable, Optional

import fitz  # PyMuPDF
from PIL import Image


def convert_pdf_to_images(
    pdf_path: Path,
    output_dir: Path,
    dpi: int,
    grayscale: bool = False,
    optimize: bool = False,
    on_progress: Optional[Callable[[int, int], None]] = None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)
    colorspace = fitz.csGRAY if grayscale else fitz.csRGB

    with fitz.open(pdf_path) as doc:
        total = doc.page_count
        digits = len(str(total))
        for page_index in range(total):
            page = doc.load_page(page_index)
            pix = page.get_pixmap(matrix=matrix, colorspace=colorspace)
            out_path = output_dir / f"{pdf_path.stem}_{page_index + 1:0{digits}d}.png"

            if optimize:
                mode = "L" if grayscale else "RGB"
                img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)
                if mode == "RGB":
                    img = img.quantize(colors=256, method=Image.MEDIANCUT)
                img.save(out_path, format="PNG", optimize=True)
            else:
                pix.save(out_path)

            print(f"저장됨: {out_path}")
            if on_progress:
                on_progress(page_index + 1, total)


def main() -> None:
    parser = argparse.ArgumentParser(description="PDF의 각 페이지를 개별 PNG 이미지로 변환합니다.")
    parser.add_argument("pdf", type=Path, help="변환할 PDF 파일 경로")
    parser.add_argument(
        "-o", "--output", type=Path, default=None,
        help="출력 폴더 (기본값: PDF와 같은 이름의 폴더)"
    )
    parser.add_argument(
        "-d", "--dpi", type=int, default=96,
        help="출력 이미지 해상도 (기본값: 96, 화면 표시 기준 해상도)"
    )
    parser.add_argument(
        "-g", "--grayscale", action="store_true",
        help="흑백(그레이스케일)으로 변환하여 용량을 줄입니다"
    )
    parser.add_argument(
        "--optimize", action="store_true",
        help="PNG를 재압축하여 용량을 줄입니다 (컬러는 256색으로 축소)"
    )
    args = parser.parse_args()

    if not args.pdf.exists():
        print(f"오류: 파일을 찾을 수 없습니다 - {args.pdf}", file=sys.stderr)
        sys.exit(1)

    output_dir = args.output or args.pdf.with_suffix("")
    convert_pdf_to_images(
        args.pdf, output_dir, args.dpi,
        grayscale=args.grayscale, optimize=args.optimize,
    )


if __name__ == "__main__":
    main()
