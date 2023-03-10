import torch
from carvekit.api.high import HiInterface

# Check doc strings for more information
# interface = HiInterface(object_type="object",  # Can be "object" or "hairs-like".
#                         batch_size_seg=1,
#                         batch_size_matting=1,
#                         device='cuda' if torch.cuda.is_available() else 'cpu',
#                         seg_mask_size=640,  # Use 640 for Tracer B7 and 320 for U2Net
#                         matting_mask_size=2048,
#                         trimap_prob_threshold=231,
#                         trimap_dilation=30,
#                         trimap_erosion_iters=1,
#                         fp16=False)
# images_without_background = interface([r"D:\Kaggle\CleanCodeCup\2023\2023\images\images\5gEkVcx0lFzwWoRd8K1sYHNPrf9QJ3thvmLb7XaZ.jpg"])
# cat_wo_bg = images_without_background[0]
# cat_wo_bg.save('2.png')
import PIL.Image

from carvekit.api.interface import Interface
from carvekit.ml.wrap.fba_matting import FBAMatting
from carvekit.ml.wrap.tracer_b7 import TracerUniversalB7
from carvekit.pipelines.postprocessing import MattingMethod
from carvekit.pipelines.preprocessing import PreprocessingStub
from carvekit.trimap.generator import TrimapGenerator

# Check doc strings for more information
seg_net = TracerUniversalB7(device='cuda',
                            batch_size=1)


preprocessing = PreprocessingStub()

interface = Interface(pre_pipe=preprocessing,
                      post_pipe=None,
                      seg_pipe=seg_net)

import glob
import os
for image_path in glob.glob(r"D:\Kaggle\CleanCodeCup\2023\2023\images\images\*.jpg"):
    if not os.path.isfile(r'D:/Kaggle/CleanCodeCup/2023/2023/images/images_without_bg/'+image_path.split("\\")[-1][:-3]+"png"):
        print(image_path)
        image = PIL.Image.open(image_path)
        image = image.convert("RGB")  # remove alpha
        cat_wo_bg = interface([image])[0]
        # cat_wo_bg = cat_wo_bg.convert('RGB')
        try:
            cat_wo_bg.save(r'D:/Kaggle/CleanCodeCup/2023/2023/images/images_without_bg/'+image_path.split("\\")[-1][:-3]+"png")
        except Exception as err:
            print(err)
