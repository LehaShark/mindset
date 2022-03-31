---

## :wrench: Dependencies and Installation

- Python >= 3.7 (Recommend to use [Anaconda](https://www.anaconda.com/download/#linux) 
- [PyTorch >= 1.7](https://pytorch.org/)

### Installation

1. Clone repo

    ```bash
    git clone https://github.com/MindSetLib/iu_ml_models.git
    cd sr_esrgan_kononov 
    ```

1. Install dependent packages

    ```bash
    # Install basicsr - https://github.com/xinntao/BasicSR
    # We use BasicSR for both training and inference
    pip install basicsr
    # facexlib and gfpgan are for face enhancement
    pip install facexlib
    pip install gfpgan
    pip install -r requirements.txt
    python setup.py develop
    ```

## :zap: Quick Inference

### Inference general images

Download pre-trained models: [RealESRGAN_x4plus.pth](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth)

```bash
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -P experiments/pretrained_models
```

Inference!

```bash
python inference_realesrgan.py --model_path experiments/pretrained_models/RealESRGAN_x4plus.pth --input inputs --face_enhance

```bash
# download model
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth -P experiments/pretrained_models
# inference
python inference_realesrgan.py --model_path experiments/pretrained_models/RealESRGAN_x4plus_anime_6B.pth --input inputs
```

Results are in the `results` folder

### Usage of python script

1. You can use X4 model for **arbitrary output size** with the argument `outscale`. The program will further perform cheap resize operation after the Real-ESRGAN output.

```console
Usage: python inference_realesrgan.py --model_path experiments/pretrained_models/RealESRGAN_x4plus.pth --input infile --output outfile [options]...

A common command: python inference_realesrgan.py --model_path experiments/pretrained_models/RealESRGAN_x4plus.pth --input infile --netscale 4 --outscale 3.5 --half --face_enhance

  -h                   show this help
  --input              Input image or folder. Default: inputs
  --output             Output folder. Default: results
  --model_path         Path to the pre-trained model. Default: experiments/pretrained_models/RealESRGAN_x4plus.pth
  --netscale           Upsample scale factor of the network. Default: 4
  --outscale           The final upsampling scale of the image. Default: 4
  --suffix             Suffix of the restored image. Default: out
  --tile               Tile size, 0 for no tile during testing. Default: 0
  --face_enhance       Whether to use GFPGAN to enhance face. Default: False
  --half               Whether to use half precision during inference. Default: False
  --ext                Image extension. Options: auto | jpg | png, auto means using the same extension as inputs. Default: auto
```

## : Model Zoo

- [RealESRGAN_x4plus](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth): X4 model for general images
- [RealESRGAN_x4plus_anime_6B](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth): Optimized for anime images; 6 RRDB blocks (slightly smaller network)
- [RealESRGAN_x2plus](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth): X2 model for general images
- [RealESRNet_x4plus](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.1/RealESRNet_x4plus.pth): X4 model with MSE loss (over-smooth effects)

- [official ESRGAN_x4](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.1/ESRGAN_SRx4_DF2KOST_official-ff704c30.pth): official ESRGAN model (X4)

- [RealESRGAN_x4plus_netD](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.3/RealESRGAN_x4plus_netD.pth)
- [RealESRGAN_x2plus_netD](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.3/RealESRGAN_x2plus_netD.pth)
