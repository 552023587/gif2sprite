from PIL import Image, ImageChops
import os

def is_similar(im1, im2, threshold=10):
    """
    比较两个图像的相似度，返回布尔值。
    """
    diff = ImageChops.difference(im1, im2)
    stat = diff.getbbox()
    return stat is None

def extract_key_frames(gif_path, max_frames=10):
    """
    从 GIF 文件中提取关键帧并去除重复帧。
    """
    gif = Image.open(gif_path)
    frame_count = gif.n_frames

    key_frames = []
    previous_frame = None

    for frame in range(frame_count):
        gif.seek(frame)
        current_frame = gif.copy().convert("RGBA")

        if previous_frame is None or not is_similar(previous_frame, current_frame):
            key_frames.append(current_frame)
            previous_frame = current_frame

    # 保留间隔相同的10帧
    total_frames = len(key_frames)
    step = max(1, total_frames // max_frames)
    selected_frames = key_frames[::step][:max_frames]

    return selected_frames

def create_sprite_sheet(frames, output_path, padding=10):
    """
    将帧合并成一个 Sprite 图，每帧之间添加间隔。
    """
    if not frames:
        return

    frame_width, frame_height = frames[0].size
    sprite_sheet_width = frame_width * len(frames) + padding * (len(frames) - 1)
    sprite_sheet_height = frame_height

    sprite_sheet = Image.new("RGBA", (sprite_sheet_width, sprite_sheet_height))

    for i, frame in enumerate(frames):
        sprite_sheet.paste(frame, (i * (frame_width + padding), 0))

    sprite_sheet.save(output_path)

# 批量处理
gif_folder = 'gif'
output_base_folder = 'sprite'

if not os.path.exists(output_base_folder):
    os.makedirs(output_base_folder)

for gif_file in os.listdir(gif_folder):
    if gif_file.endswith('.gif'):
        gif_path = os.path.join(gif_folder, gif_file)
        frames = extract_key_frames(gif_path)
        output_path = os.path.join(output_base_folder, os.path.splitext(gif_file)[0] + '_sprite_sheet.png')
        create_sprite_sheet(frames, output_path)
