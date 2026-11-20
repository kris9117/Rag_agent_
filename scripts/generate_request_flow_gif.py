"""
Generate high-resolution, theme-friendly animated GIF of the request flow.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = Path(__file__).resolve().parents[1] / "docs" / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_GIF = ASSETS_DIR / "request-flow.gif"

WIDTH = 1000
HEIGHT = 620

# Colors matching GitHub dark mode aesthetic with high contrast
BG_COLOR = (13, 17, 23)        # #0D1117
CARD_BG = (22, 27, 34)         # #161B22
CARD_BORDER = (48, 54, 61)     # #30363D
TEXT_MAIN = (240, 246, 252)    # #F0F6FC
TEXT_MUTED = (139, 148, 158)   # #8B949E
TEXT_CODE = (121, 192, 255)    # #79C0FF
BANNER_BG = (28, 33, 40)       # #1C2128

BLUE = (88, 166, 255)          # #58A6FF
GREEN = (126, 231, 135)        # #7EE787
PURPLE = (210, 168, 255)       # #D2A8FF
ORANGE = (255, 166, 87)        # #FFA657
RED = (255, 123, 114)          # #FF7B72

# Load Fonts
FONT_NAME = "C:\\Windows\\Fonts\\segoeui.ttf"
FONT_BOLD = "C:\\Windows\\Fonts\\segoeuib.ttf"
FONT_CODE = "C:\\Windows\\Fonts\\consola.ttf"

try:
    font_title = ImageFont.truetype(FONT_BOLD, 18)
    font_subtitle = ImageFont.truetype(FONT_NAME, 12)
    font_card_title = ImageFont.truetype(FONT_BOLD, 13)
    font_body = ImageFont.truetype(FONT_NAME, 11)
    font_badge = ImageFont.truetype(FONT_BOLD, 10)
    font_code = ImageFont.truetype(FONT_CODE, 10)
    font_banner = ImageFont.truetype(FONT_BOLD, 12)
except Exception:
    font_title = font_subtitle = font_card_title = ImageFont.load_default()
    font_body = font_badge = font_code = font_banner = ImageFont.load_default()


def draw_rounded_card(draw, box, fill=CARD_BG, outline=CARD_BORDER, width=1, radius=6):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_badge(draw, x, y, text, color, bg_alpha_color=(35, 45, 55)):
    text_bbox = font_badge.getbbox(text)
    w = (text_bbox[2] - text_bbox[0]) + 12
    h = (text_bbox[3] - text_bbox[1]) + 8
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=bg_alpha_color, outline=color, width=1)
    draw.text((x + 6, y + 3), text, font=font_badge, fill=color)


def create_base_canvas():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Title & Subtitle
    draw.text((30, 20), "Enterprise IT Support Agent — Request Lifecycle", font=font_title, fill=TEXT_MAIN)
    draw.text(
        (30, 46),
        "Deterministic LangGraph state machine, hybrid RAG (FAISS + BM25), authorization & observability",
        font=font_subtitle,
        fill=TEXT_MUTED,
    )

    return img, draw


def render_frame(step_index: int, banner_text: str, active_branch: str = None) -> Image.Image:
    img, draw = create_base_canvas()

    # Step 1 Card: Client
    is_step1 = (step_index == 1)
    border_c1 = BLUE if is_step1 else CARD_BORDER
    width_1 = 2 if is_step1 else 1
    draw_rounded_card(draw, [30, 75, 290, 215], outline=border_c1, width=width_1)
    draw_badge(draw, 42, 85, "1. INGESTION", BLUE if is_step1 else TEXT_MUTED)
    draw.text((42, 115), "Client Support Request", font=font_card_title, fill=TEXT_MAIN)
    draw.text((42, 137), "POST /api/v1/support", font=font_code, fill=TEXT_CODE)
    draw.text((42, 155), "X-API-Key: demo-key-emp0001", font=font_code, fill=TEXT_MUTED)
    draw.text((42, 175), "Query: 'VPN failing with 403 error'", font=font_body, fill=TEXT_MUTED)
    draw.text((42, 192), "Pydantic v2 Payload Validation", font=font_body, fill=GREEN if is_step1 else TEXT_MUTED)

    # Arrow 1 -> 2
    arr_c12 = BLUE if step_index >= 2 else CARD_BORDER
    draw.line([(290, 145), (340, 145)], fill=arr_c12, width=2)
    draw.polygon([(340, 145), (332, 140), (332, 150)], fill=arr_c12)

    # Step 2 Card: FastAPI & Auth
    is_step2 = (step_index == 2)
    border_c2 = GREEN if is_step2 else CARD_BORDER
    width_2 = 2 if is_step2 else 1
    draw_rounded_card(draw, [340, 75, 630, 215], outline=border_c2, width=width_2)
    draw_badge(draw, 352, 85, "2. AUTH & IDENTITY", GREEN if is_step2 else TEXT_MUTED)
    draw.text((352, 115), "Identity & Authorization Guard", font=font_card_title, fill=TEXT_MAIN)
    draw.text((352, 137), "get_current_user dependency", font=font_code, fill=TEXT_CODE)
    draw.text((352, 155), "• Validates API key / Bearer token", font=font_body, fill=TEXT_MUTED)
    draw.text((352, 173), "• Binds effective_user_id (EMP0001)", font=font_body, fill=GREEN if is_step2 else TEXT_MUTED)
    draw.text((352, 192), "• Prevents cross-user spoofing (403)", font=font_body, fill=TEXT_MUTED)

    # Arrow 2 -> 3
    arr_c23 = BLUE if step_index >= 3 else CARD_BORDER
    draw.line([(630, 145), (680, 145)], fill=arr_c23, width=2)
    draw.polygon([(680, 145), (672, 140), (672, 150)], fill=arr_c23)

    # Step 3 Card: LangGraph State Machine
    is_step3 = (step_index == 3)
    border_c3 = PURPLE if is_step3 else CARD_BORDER
    width_3 = 2 if is_step3 else 1
    draw_rounded_card(draw, [680, 75, 970, 215], outline=border_c3, width=width_3)
    draw_badge(draw, 692, 85, "3. ORCHESTRATION", PURPLE if is_step3 else TEXT_MUTED)
    draw.text((692, 115), "LangGraph State Machine", font=font_card_title, fill=TEXT_MAIN)
    draw.text((692, 137), "understand_request -> route_request", font=font_code, fill=TEXT_CODE)
    draw.text((692, 155), "• 9 Canonical Intent Classes", font=font_body, fill=TEXT_MUTED)
    draw.text((692, 173), "• Intent: VPN_TROUBLESHOOTING", font=font_body, fill=PURPLE if is_step3 else TEXT_MUTED)
    draw.text((692, 192), "• Route: KNOWLEDGE (Deterministic)", font=font_body, fill=GREEN if is_step3 else TEXT_MUTED)

    # Branch Connectors (Y: 215 -> 255)
    branch_active = (step_index >= 4)
    trunk_color = BLUE if branch_active else CARD_BORDER
    draw.line([(825, 215), (825, 240)], fill=trunk_color, width=2)
    draw.line([(145, 240), (875, 240)], fill=trunk_color, width=2)

    # 4 Branch Drops
    c_b1 = GREEN if active_branch == "KNOWLEDGE" else (BLUE if branch_active else CARD_BORDER)
    c_b2 = PURPLE if active_branch == "TOOL" else (BLUE if branch_active else CARD_BORDER)
    c_b3 = ORANGE if active_branch == "ACTION" else (BLUE if branch_active else CARD_BORDER)
    c_b4 = RED if active_branch == "ESCALATION" else (BLUE if branch_active else CARD_BORDER)

    draw.line([(145, 240), (145, 260)], fill=c_b1, width=2)
    draw.line([(385, 240), (385, 260)], fill=c_b2, width=2)
    draw.line([(625, 240), (625, 260)], fill=c_b3, width=2)
    draw.line([(865, 240), (865, 260)], fill=c_b4, width=2)

    # Branch 1: Knowledge RAG
    is_b1 = (active_branch == "KNOWLEDGE")
    draw_rounded_card(draw, [30, 260, 260, 440], outline=GREEN if is_b1 else CARD_BORDER, width=2 if is_b1 else 1)
    draw_badge(draw, 42, 270, "ROUTE: KNOWLEDGE", GREEN if is_b1 else TEXT_MUTED)
    draw.text((42, 298), "Hybrid RAG Pipeline", font=font_card_title, fill=TEXT_MAIN)
    draw.text((42, 320), "1. FAISS Dense Retrieval", font=font_body, fill=GREEN if is_b1 else TEXT_MUTED)
    draw.text((42, 338), "2. BM25Okapi Lexical Match", font=font_body, fill=GREEN if is_b1 else TEXT_MUTED)
    draw.text((42, 356), "3. Reciprocal Rank Fusion", font=font_body, fill=TEXT_MUTED)
    draw.text((42, 374), "4. Cross-Encoder Reranker", font=font_body, fill=TEXT_MUTED)
    draw.text((42, 394), "ms-marco-MiniLM-L-6-v2", font=font_code, fill=TEXT_CODE)
    draw.text((42, 414), "Grounded + markdown sources", font=font_body, fill=GREEN if is_b1 else TEXT_MUTED)

    # Branch 2: Tool Execution
    is_b2 = (active_branch == "TOOL")
    draw_rounded_card(draw, [270, 260, 500, 440], outline=PURPLE if is_b2 else CARD_BORDER, width=2 if is_b2 else 1)
    draw_badge(draw, 282, 270, "ROUTE: TOOL", PURPLE if is_b2 else TEXT_MUTED)
    draw.text((282, 298), "Read-Only Status Tools", font=font_card_title, fill=TEXT_MAIN)
    draw.text((282, 320), "• Account Status (MFA/Lock)", font=font_body, fill=TEXT_MUTED)
    draw.text((282, 338), "• Device Health & Check", font=font_body, fill=TEXT_MUTED)
    draw.text((282, 356), "• Existing Ticket Lookup", font=font_body, fill=TEXT_MUTED)
    draw.text((282, 376), "Authorization Check", font=font_card_title, fill=PURPLE if is_b2 else TEXT_MUTED)
    draw.text((282, 396), "Verifies caller owns record", font=font_body, fill=TEXT_MUTED)
    draw.text((282, 414), "Status: TOOL_COMPLETED", font=font_code, fill=PURPLE if is_b2 else TEXT_MUTED)

    # Branch 3: Action Execution
    is_b3 = (active_branch == "ACTION")
    draw_rounded_card(draw, [510, 260, 740, 440], outline=ORANGE if is_b3 else CARD_BORDER, width=2 if is_b3 else 1)
    draw_badge(draw, 522, 270, "ROUTE: ACTION", ORANGE if is_b3 else TEXT_MUTED)
    draw.text((522, 298), "Write Operations", font=font_card_title, fill=TEXT_MAIN)
    draw.text((522, 320), "• Create Support Ticket", font=font_body, fill=TEXT_MUTED)
    draw.text((522, 338), "• Validate Category & Priority", font=font_body, fill=TEXT_MUTED)
    draw.text((522, 356), "• Password Reset Self-Service", font=font_body, fill=TEXT_MUTED)
    draw.text((522, 376), "Atomic SQLite Write", font=font_card_title, fill=ORANGE if is_b3 else TEXT_MUTED)
    draw.text((522, 396), "Generates INC000XXX ID", font=font_body, fill=TEXT_MUTED)
    draw.text((522, 414), "Status: ACTION_COMPLETED", font=font_code, fill=ORANGE if is_b3 else TEXT_MUTED)

    # Branch 4: Escalation
    is_b4 = (active_branch == "ESCALATION")
    draw_rounded_card(draw, [750, 260, 970, 440], outline=RED if is_b4 else CARD_BORDER, width=2 if is_b4 else 1)
    draw_badge(draw, 762, 270, "ROUTE: ESCALATION", RED if is_b4 else TEXT_MUTED)
    draw.text((762, 298), "Human Escalation Path", font=font_card_title, fill=TEXT_MAIN)
    draw.text((762, 320), "• Repeated Troubleshoot Fail", font=font_body, fill=TEXT_MUTED)
    draw.text((762, 338), "• Security / Phishing Threat", font=font_body, fill=TEXT_MUTED)
    draw.text((762, 356), "• Explicit Tier-2 Requests", font=font_body, fill=TEXT_MUTED)
    draw.text((762, 376), "Handover Guidance", font=font_card_title, fill=RED if is_b4 else TEXT_MUTED)
    draw.text((762, 396), "Passes state context to L2", font=font_body, fill=TEXT_MUTED)
    draw.text((762, 414), "Status: ESCALATED", font=font_code, fill=RED if is_b4 else TEXT_MUTED)

    # Converging Lines to Step 5 (Y: 440 -> 475)
    c_conv = BLUE if step_index >= 5 else CARD_BORDER
    draw.line([(145, 440), (145, 460)], fill=c_conv, width=2)
    draw.line([(385, 440), (385, 460)], fill=c_conv, width=2)
    draw.line([(625, 440), (625, 460)], fill=c_conv, width=2)
    draw.line([(865, 440), (865, 460)], fill=c_conv, width=2)
    draw.line([(145, 460), (865, 460)], fill=c_conv, width=2)
    draw.line([(500, 460), (500, 475)], fill=c_conv, width=2)
    draw.polygon([(500, 475), (495, 468), (505, 468)], fill=c_conv)

    # Step 5 Card: Structured Response Delivery
    is_step5 = (step_index == 5)
    border_c5 = BLUE if is_step5 else CARD_BORDER
    width_5 = 2 if is_step5 else 1
    draw_rounded_card(draw, [30, 475, 970, 565], outline=border_c5, width=width_5)
    draw_badge(draw, 42, 485, "5. RESPONSE DELIVERY", BLUE if is_step5 else TEXT_MUTED)
    draw.badge_text = "HTTP 200 OK — Structured SupportResponse (Pydantic)"
    draw.text((200, 486), draw.badge_text, font=font_card_title, fill=TEXT_MAIN)
    json_summary = (
        '{ "request_id": "REQ-7B9F10", "intent": "VPN_TROUBLESHOOTING", '
        '"status": "COMPLETED", "effective_user": "EMP0001" }'
    )
    draw.text((42, 514), json_summary, font=font_code, fill=TEXT_CODE)
    resp_summary = (
        '"response": "1. Verify MFA authentication. 2. Clear credentials cache at '
        '%APPDATA%\\\\Cisco... | Sources: [vpn_guide.md]"'
    )
    draw.text((42, 532), resp_summary, font=font_body, fill=TEXT_MUTED)
    telem_summary = (
        "Telemetry logged: Duration 124ms | Tokens: 320 in, 142 out | "
        "Prometheus & JSONL structured audit event emitted"
    )
    draw.text((42, 548), telem_summary, font=font_body, fill=GREEN if is_step5 else TEXT_MUTED)

    # Bottom Status Banner
    draw_rounded_card(draw, [30, 575, 970, 608], fill=BANNER_BG, outline=CARD_BORDER, radius=4)
    banner_color = GREEN if is_step5 else (BLUE if step_index > 0 else TEXT_MUTED)
    draw.text((45, 584), banner_text, font=font_banner, fill=banner_color)

    return img


def generate_gif():
    scenarios = [
        # (step_index, banner_text, active_branch, duration_ms)
        (0, "● Idle: Enterprise IT Support Agent listening on /api/v1/support...", None, 1400),
        (1, "● Step 1: Employee submits support query via authenticated HTTP POST request...", None, 1200),
        (2, "● Step 2: FastAPI validates payload and verifies API key (blocks cross-user spoofing)...", None, 1300),
        (3, "● Step 3: LangGraph parses intent (OpenAI) and deterministically selects route...", None, 1400),
        (4, "● Step 4a: KNOWLEDGE Route: FAISS + BM25 hybrid search -> RRF -> Reranking...", "KNOWLEDGE", 1800),
        (4, "● Step 4b: TOOL Route: Verify entity ownership -> Query hardware/account status...", "TOOL", 1500),
        (4, "● Step 4c: ACTION Route: Validate category/priority -> Create incident ticket...", "ACTION", 1500),
        (4, "● Step 4d: ESCALATION Route: Repeated troubleshooting triggers Tier-2 handoff...", "ESCALATION", 1500),
        (4, "● Step 4: Knowledge grounded response generated with verified source citations...", "KNOWLEDGE", 1400),
        (5, "● Step 5: FastAPI returns structured SupportResponse with request_id & audit telemetry!", None, 2500),
    ]

    frames = []
    durations = []
    for step_idx, banner, branch, dur in scenarios:
        frame = render_frame(step_idx, banner, branch)
        # Convert to P-mode with adaptive palette for crisp rendering and small file size
        frame_p = frame.convert("P", palette=Image.ADAPTIVE, colors=128)
        frames.append(frame_p)
        durations.append(dur)

    frames[0].save(
        OUTPUT_GIF,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
    )
    print(f"Generated {OUTPUT_GIF} ({OUTPUT_GIF.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    generate_gif()
