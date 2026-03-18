# "Design-focused node suite for ComfyUI."
# Copyright 2026 Augment Studio
# Paid Node, credit values may change.
# Augmentstudio.app

import io
import json
import os
import requests
import time
import folder_paths
import numpy as np
import torch
from PIL import Image


NODE_ID = "logo_upscale"
API_URL = "https://augmentstudio.app/api"

UPLOAD_DIR = folder_paths.get_input_directory()


class AugmentLogoUpscale:
    @classmethod
    def INPUT_TYPES(cls):
        files = sorted([
            f for f in os.listdir(UPLOAD_DIR)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
        ])
        return {
            "required": {
                "api_key": ("STRING", {"default": ""}),
                "scale": (["2x"], {"default": "2x"}),
            },
            "optional": {
                "image": ("IMAGE",),
                "image_file": (files, {"image_upload": True}),
                "trigger": ("TRIGGER",),
            },
        }

    RETURN_TYPES = ("IMAGE", "AUGMENT_JSON", "TRIGGER")
    RETURN_NAMES = ("image", "json_result", "trigger")
    FUNCTION = "execute"
    CATEGORY = "Augment/Enhance"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return time.time()

    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        return True

    def execute(self, api_key, scale="2x", image=None, image_file=None, trigger=None):
        api_url = API_URL.rstrip("/")
        auth = {"Authorization": f"Bearer {api_key}"}
        scale_factor = int(scale.replace("x", ""))

        if image is not None:
            img_np = (image[0].cpu().numpy() * 255).astype(np.uint8)
            pil_img = Image.fromarray(img_np, "RGB")
            buf = io.BytesIO()
            pil_img.save(buf, format="PNG")
            img_bytes = buf.getvalue()
            source_name = "image_input.png"
            mime = "image/png"
        elif image_file:
            path = os.path.join(UPLOAD_DIR, image_file)
            with open(path, "rb") as f:
                img_bytes = f.read()
            source_name = image_file
            ext = os.path.splitext(image_file)[1].lower()
            mime_types = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
            mime = mime_types.get(ext, "image/png")
        else:
            raise RuntimeError("No image provided — connect an image input or select a file")

        print(f"[Augment API] Submitting image for {scale} upscale: {source_name} ({len(img_bytes)} bytes)")
        try:
            r = requests.post(
                f"{api_url}/process",
                files={"image": (source_name, img_bytes, mime)},
                data={"node_id": NODE_ID, "scale": scale_factor},
                headers=auth,
                timeout=30,
            )
        except requests.exceptions.RequestException as e:
            print(f"[Augment API] Submit failed: {e}")
            raise

        if r.status_code != 200:
            raise RuntimeError(f"Submit error {r.status_code}: {r.text[:500]}")

        request_id = r.json().get("request_id")
        if not request_id:
            raise RuntimeError(f"No request_id: {r.text[:500]}")

        print(f"[Augment API] Job submitted: {request_id}")

        max_wait = 120
        elapsed = 0
        job_status = "unknown"

        while elapsed < max_wait:
            time.sleep(1)
            elapsed += 1
            try:
                status_r = requests.get(
                    f"{api_url}/job/{request_id}/status",
                    headers=auth, timeout=10,
                )
                job_status = status_r.json().get("status", "unknown")
            except Exception as e:
                print(f"[Augment API] Poll error: {e}")
                continue

            if job_status == "done":
                break
            elif job_status == "error":
                raise RuntimeError(f"Job failed: {status_r.json().get('error')}")

        if job_status != "done":
            raise RuntimeError(f"Timed out after {max_wait}s")

        img_r = requests.get(
            f"{api_url}/job/{request_id}/image",
            headers=auth, timeout=60,
        )
        if img_r.status_code != 200:
            raise RuntimeError(f"Image fetch error: {img_r.status_code}")

        img = Image.open(io.BytesIO(img_r.content)).convert("RGB")
        arr = np.array(img).astype(np.float32) / 255.0

        image_tensor = torch.from_numpy(arr).unsqueeze(0)

        json_result = json.dumps({
            "node": "LogoUpscale",
            "scale": scale,
            "width": img.size[0],
            "height": img.size[1],
            "source": source_name,
        }, indent=2)

        temp_dir = folder_paths.get_temp_directory()
        os.makedirs(temp_dir, exist_ok=True)
        preview_file = f"augment_upscale_{time.time_ns()}.png"
        img.save(os.path.join(temp_dir, preview_file))

        print(f"[Augment API] Done! {img.size[0]}x{img.size[1]} ({scale} upscale)")
        return {
            "ui": {"images": [{"filename": preview_file, "subfolder": "", "type": "temp"}]},
            "result": (image_tensor, json_result, "done"),
        }


NODE_CLASS_MAPPINGS = {
    "AugmentLogoUpscale": AugmentLogoUpscale,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "AugmentLogoUpscale": "Logo Upscale",
}
