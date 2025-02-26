import torch

from models import ImageRequest
from diffusers import DiffusionPipeline, EulerDiscreteScheduler, DPMSolverMultistepScheduler
from PIL.Image import Image

scheduler = EulerDiscreteScheduler.from_pretrained("John6666/baxl-v3-sdxl", subfolder="scheduler")
pipeline = DiffusionPipeline.from_pretrained(
    "John6666/baxl-v3-sdxl",
    scheduler=scheduler,
    use_safetensors=True,
    # torch_dtype=torch.float16
)
pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
    pipeline.scheduler.config)

device = "cuda" if torch.cuda.is_available() else "cpu"
# MPS is only available on MacBook M1 series and later
device = 'mps' if torch.backends.mps.is_available() else device
pipeline.to(device)


async def generate_image(imgRequest: ImageRequest) -> Image:
    print(f"Pipeline input: {imgRequest.dict()}")
    image: Image = pipeline(
        prompt=imgRequest.prompt,
        negative_prompt=imgRequest.negative_prompt,
        width=imgRequest.width,
        height=imgRequest.height,
        guidance_scale=imgRequest.guidance_scale,
        num_inference_steps=imgRequest.num_inference_steps,
        added_cond_kwargs={}
    ).images[0]
    return image
