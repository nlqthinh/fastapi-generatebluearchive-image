const fs = require("fs");

const URL = "http://127.0.0.1:8080";

function base64ToImage(base64String, savePath = "output_image.png") {
  const buffer = Buffer.from(base64String, "base64");
  fs.writeFileSync(savePath, buffer);
}

async function textToImage() {
  const payload = {
    prompt:
      "Shiroko_BlueArchive",
    negative_prompt:
      "worst quality, low quality, watermark, text, error, blurry, jpeg artifacts, cropped, jpeg artifacts, signature, watermark, username, artist name, bad anatomy",
    num_inference_steps: 25,
    guidance_scale: 7.5,
    width: 512,
    height: 512,
  };

  try {
    console.log("Sending Inference Request");
    const response = await fetch(`${URL}/sdapi/v1/txt2img`, {
      method: "POST",
      body: JSON.stringify(payload),
      headers: { "Content-Type": "application/json" },
    });
    const result = await response.json();
    console.log(result);

    console.log("Inference Completed");
    base64ToImage(result.image, `output_image.png`);
    console.log("Image saved to output_image.png");
  } catch (error) {
    console.error("Error:", error);
  }
}

textToImage();
