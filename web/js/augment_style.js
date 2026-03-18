/*"Augment Upscale — AI Image & Logo Upscaler for ComfyUI."
# Copyright 2026 Augment Studio
Augmentstudio.app */

import { app } from "../../../scripts/app.js";

const TITLE_BG = "#443322";
const NODE_BG = "#665533";

const PAID_NODES = [
    "AugmentLogoUpscale",
];

const BADGE_FONT = "bold 9px sans-serif";
const BADGE_RADIUS = 4;
const BADGE_PAD_X = 6;

app.registerExtension({
    name: "augment-upscale.NodeStyle",

    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (!PAID_NODES.includes(nodeData.name)) return;

        const origCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            origCreated?.apply(this, arguments);
            this.addWidget("button", "Get Tokens", null, () => {
                window.open("https://augmentstudio.app/pricing", "_blank");
            });

            const jsonIdx = this.outputs?.findIndex(o => o.name === "json_result");
            if (jsonIdx >= 0) {
                this.outputs.splice(jsonIdx, 1);
            }
        };

        const origDraw = nodeType.prototype.onDrawForeground;
        nodeType.prototype.onDrawForeground = function (ctx) {
            this.color = TITLE_BG;
            this.bgcolor = NODE_BG;

            origDraw?.apply(this, arguments);

            ctx.save();
            ctx.font = BADGE_FONT;

            const creditsText = "🔸 1 export / run";
            const creditsW = ctx.measureText(creditsText).width + BADGE_PAD_X * 2;
            const creditsX = this.size[0] - creditsW - 6;
            const y = -22;

            ctx.beginPath();
            ctx.roundRect(creditsX, y, creditsW, 14, BADGE_RADIUS);
            ctx.fillStyle = "#8d6932";
            ctx.fill();

            ctx.fillStyle = "#ffffff";
            ctx.textAlign = "left";
            ctx.textBaseline = "middle";
            ctx.fillText(creditsText, creditsX + BADGE_PAD_X, y + 7);

            ctx.restore();
        };
    },
});
