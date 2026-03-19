# Augment Upscale Pro

Make your logos and brand assets print-ready. Augment Upscale Pro is a ComfyUI node that takes rasterized images and upscales them 2X while keeping lines crisp and colors clean. No more blurry enlargements. A perfect first step to cleaning up assets before vectorizing them. 

Drop in a logo, icon, or any flat artwork and get back a sharp, high-resolution version you can actually use.

## Getting started

1. Grab an API key at [augmentstudio.app/pricing](https://augmentstudio.app/pricing)
2. Install the node from ComfyUI Manager (search "augment Upscale Pro")
3. Add the **Upscale Pro** node to your workflow, paste in your key, and connect an image

## Saving your API key

You can avoid pasting your key every time by using the **Variable Set** and **Variable Get** nodes from [augment-ComfyUI](https://github.com/augment-lib/augment-ComfyUI).

1. Install augment-ComfyUI from ComfyUI Manager (search "augment-ComfyUI")
2. Add a **Variable Set (String)** node and paste your key into `value`
3. Connect its `text` output to the `api_key` input on Upscale Pro
4. Next time, swap it out for a **Variable Get (String)** node and it will pull your saved key automatically

## Also included

**Trigger** flow nodes for wiring up multi-step workflows. Use them to chain the upscaler with other nodes so everything runs in the right order.

## Manual install

```
cd ComfyUI/custom_nodes
git clone https://github.com/augment-lib/augment-upscale-pro.git augment-upscale-pro
```

## License

See [LICENSE.md](LICENSE.MD) for details.
