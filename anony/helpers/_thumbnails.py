# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic


import os
import asyncio
import aiohttp
from PIL import (Image, ImageDraw, ImageEnhance,
                 ImageFilter, ImageFont)

from anony import config
from anony.helpers import Media, Track


class Thumbnail:
    def __init__(self):
        try:
            self.font_title = ImageFont.truetype("anony/helpers/Raleway-Bold.ttf", 55)
            self.font_artist = ImageFont.truetype("anony/helpers/Inter-Light.ttf", 35)
            self.font_time = ImageFont.truetype("anony/helpers/Inter-Light.ttf", 25)
        except:
            self.font_title = ImageFont.load_default()
            self.font_artist = ImageFont.load_default()
            self.font_time = ImageFont.load_default()

    def _make_sq(self, im, radius=60):
        """Creates a rounded square image."""
        mask = Image.new('L', im.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0) + im.size, radius=radius, fill=255)
        out = Image.new('RGBA', im.size, (0, 0, 0, 0))
        out.paste(im, (0, 0), mask)
        return out

    def _draw_player(self, thumb_path, videoid, title, duration, artist):
        # 1. Background
        if thumb_path and os.path.exists(thumb_path):
            background = Image.open(thumb_path)
        else:
            background = Image.new("RGB", (1280, 720), (20, 20, 20))

        background = background.resize((1280, 720))
        background = background.filter(ImageFilter.GaussianBlur(radius=50))

        # Darken background
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.4)

        draw = ImageDraw.Draw(background)

        # 2. Thumbnail image (Left)
        if thumb_path and os.path.exists(thumb_path):
            thumb = Image.open(thumb_path)
        else:
            thumb = Image.new("RGB", (520, 520), (40, 40, 40))

        thumb = thumb.resize((520, 520))
        thumb = self._make_sq(thumb, radius=60)
        background.paste(thumb, (70, 100), thumb)

        # 4. Text (Title & Artist)
        title = str(title)
        artist = str(artist)
        max_title_width = 450
        if draw.textbbox((0, 0), title, font=self.font_title)[2] > max_title_width:
            while draw.textbbox((0, 0), title + "...", font=self.font_title)[2] > max_title_width:
                title = title[:-1]
            title += "..."

        draw.text((630, 220), title, font=self.font_title, fill="white")
        draw.text((630, 290), artist, font=self.font_artist, fill=(200, 200, 200))

        # Star icon
        star_pts = [
            (1130, 268), (1135, 280), (1148, 280), (1138, 288),
            (1142, 301), (1130, 293), (1118, 301), (1122, 288),
            (1112, 280), (1125, 280)
        ]
        draw.polygon(star_pts, fill="white")

        # Three dots (vertical)
        draw.ellipse([1180, 265, 1186, 271], fill="white")
        draw.ellipse([1180, 280, 1186, 286], fill="white")
        draw.ellipse([1180, 295, 1186, 301], fill="white")

        # 5. Progress Bar
        bar_x_start = 630
        bar_x_end = 1180
        bar_y = 420
        progress = 0.35

        draw.line([bar_x_start, bar_y, bar_x_end, bar_y], fill=(100, 100, 100), width=6)
        current_x = bar_x_start + (bar_x_end - bar_x_start) * progress
        draw.line([bar_x_start, bar_y, current_x, bar_y], fill="white", width=6)
        draw.ellipse([current_x - 6, bar_y - 6, current_x + 6, bar_y + 6], fill="white")

        # 6. Time Labels
        draw.text((630, 440), "0:35", font=self.font_time, fill=(200, 200, 200))
        draw.text((1130, 440), str(duration), font=self.font_time, fill=(200, 200, 200))

        # 7. Controls
        draw.polygon([(690, 560), (740, 530), (740, 590)], fill="white")
        draw.polygon([(640, 560), (690, 530), (690, 590)], fill="white")
        draw.rectangle([850, 530, 870, 590], fill="white")
        draw.rectangle([890, 530, 910, 590], fill="white")
        draw.polygon([(1020, 530), (1070, 560), (1020, 590)], fill="white")
        draw.polygon([(1070, 530), (1120, 560), (1070, 590)], fill="white")

        # 8. Volume Bar
        draw.polygon([(710, 675), (730, 675), (745, 660), (745, 690), (730, 675)], fill="white")
        draw.polygon([(1120, 675), (1140, 675), (1155, 660), (1155, 690), (1140, 675)], fill="white")
        draw.arc([1145, 660, 1170, 690], start=-60, end=60, fill="white", width=3)
        draw.arc([1140, 650, 1180, 700], start=-60, end=60, fill="white", width=3)
        draw.line([760, 675, 1110, 675], fill=(150, 150, 150), width=6)
        draw.line([760, 675, 1020, 675], fill="white", width=6)
        draw.ellipse([1014, 669, 1026, 681], fill="white")

        # 9. Bottom Left Icons
        draw.rounded_rectangle([630, 665, 660, 685], radius=5, outline="white", width=2)
        draw.polygon([(638, 685), (645, 685), (638, 693)], fill="white")
        draw.line([685, 668, 705, 668], fill="white", width=2)
        draw.line([685, 676, 705, 676], fill="white", width=2)
        draw.line([685, 684, 705, 684], fill="white", width=2)
        draw.rectangle([678, 667, 680, 669], fill="white")
        draw.rectangle([678, 675, 680, 677], fill="white")
        draw.rectangle([678, 683, 680, 685], fill="white")

        final_thumb = background.convert("RGB")
        out_path = f"cache/{videoid}.png"
        final_thumb.save(out_path)
        return out_path

    async def generate(self, media: Media | Track) -> str:
        try:
            videoid = media.id
            output = f"cache/{videoid}.png"
            if os.path.exists(output):
                return output

            title = media.title
            duration = media.duration
            artist = getattr(media, "channel_name", "Unknown Artist") or "Unknown Artist"
            thumbnail_url = getattr(media, "thumbnail", None)

            thumb_path = f"cache/thumb_{videoid}.png"

            if not os.path.exists(thumb_path) and thumbnail_url:
                async with aiohttp.ClientSession() as session:
                    async with session.get(thumbnail_url) as resp:
                        if resp.status == 200:
                            with open(thumb_path, "wb") as f:
                                f.write(await resp.read())

            if not os.path.exists(thumb_path):
                thumb_path = None

            return await asyncio.to_thread(
                self._draw_player, thumb_path, videoid, title, duration, artist
            )
        except Exception:
            return config.DEFAULT_THUMB
