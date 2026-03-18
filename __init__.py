"""
Augment - Upscale Pro
"""

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
_failed = []

# ── Flow Control ──
try:
    from .trigger import GateNode, make_wait_node, WAIT_TYPES
    NODE_CLASS_MAPPINGS["GateNode"] = GateNode
    NODE_DISPLAY_NAME_MAPPINGS["GateNode"] = "Trigger"
    for _name, _type_str in WAIT_TYPES.items():
        _cls_name = f"AugmentWait{_name}"
        try:
            NODE_CLASS_MAPPINGS[_cls_name] = make_wait_node(_name, _type_str)
            NODE_DISPLAY_NAME_MAPPINGS[_cls_name] = f"{_name} (Improved)"
        except Exception as e:
            _failed.append((_cls_name, e))
            print(f"[augment-upscale] ⚠ {_cls_name} unavailable: {e}")
except Exception as e:
    _failed.append(("Wait nodes", e))
    print(f"[augment-upscale] ⚠ Flow control nodes unavailable: {e}")

# ── Logo Upscale (Paid) ──
try:
    from .logo_upscale import AugmentLogoUpscale
    NODE_CLASS_MAPPINGS["AugmentLogoUpscale"] = AugmentLogoUpscale
    NODE_DISPLAY_NAME_MAPPINGS["AugmentLogoUpscale"] = "Upscale Pro"
except Exception as e:
    _failed.append(("AugmentLogoUpscale", e))
    print(f"[augment-upscale] ⚠ AugmentLogoUpscale unavailable: {e}")

# ── Summary ──
WEB_DIRECTORY = "./web/js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

if _failed:
    print(f"[augment-upscale] ✓ Registered {len(NODE_CLASS_MAPPINGS)} nodes ({len(_failed)} failed)")
    for node_id, err in _failed:
        print(f"[augment-upscale]   ✗ {node_id}: {err}")
else:
    print(f"[augment-upscale] ✓ Registered {len(NODE_CLASS_MAPPINGS)} nodes")
