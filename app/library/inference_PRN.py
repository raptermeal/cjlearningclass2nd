import cv2
import os
from pathlib import Path
import torch    
from .model_download import *
from .PlaneRecNet.planerecnet import PlaneRecNet
from .PlaneRecNet.data.augmentations import FastBaseTransform
from .PlaneRecNet.planerecnet import PlaneRecNet
from .PlaneRecNet.data.config import set_cfg, cfg, COLORS
from .PlaneRecNet.utils import timer
from .PlaneRecNet.models.functions.funcs import calc_size_preserve_ar, pad_even_divided
from collections import defaultdict
import numpy as np
import easydict
import matplotlib.pyplot as plt
from app.library import model_download



color_cache = defaultdict(lambda: {})

def custom_args(argv=None):
    global args
    path_parents = Path(os.getcwd()).as_posix()
    path_trained_model = path_parents + '/' + 'model' + '/' + 'PlaneRecNet_101_9_125000.pth'
    path_sampleimg = path_parents + '/' + 'images' + '/' + '220803105932_color.png'
    
    args = easydict.EasyDict({ "trained_model": None ,
                              "config": 'PlaneRecNet_101_config' ,
                              "image": path_sampleimg,
                              "trained_model": path_trained_model,
                              "max_img":0,
                              "top_k":100,
                              "nms_mode":'matrix',
                              "score_threshold":0.1,
                              "depth_shift":512,
                              "no_mask":False,
                              "no_box":True,
                              "no_text":True,
                              })

def display_on_frame(result, frame, mask_alpha=0.5, fps_str='', no_mask=False, no_box=False, no_text=False):
    draw_point=True
    frame_gpu = frame / 255.0
    h, w, _ = frame.shape

    pred_scores = result["pred_scores"]
    pred_depth = result["pred_depth"].squeeze()
    
    if pred_scores is None:
        return frame.byte().cpu().numpy(), pred_depth.cpu().numpy()
    
    pred_masks = result["pred_masks"].unsqueeze(-1)
    pred_boxes = result["pred_boxes"]
    pred_classes = result["pred_classes"]
    num_dets = pred_scores.size()[0]

    def get_color(j, on_gpu=None):
        global color_cache
        color_idx = (j * 5) % len(COLORS)

        if on_gpu is not None and color_idx in color_cache[on_gpu]:
            return color_cache[on_gpu][color_idx]
        else:
            color = COLORS[color_idx]
            color = (color[2], color[1], color[0])
            if on_gpu is not None:
                color = torch.Tensor(color).to(on_gpu).float() / 255.
                color_cache[on_gpu][color_idx] = color
            return color


    if not no_mask and num_dets>0:
        # Prepare the RGB images for each mask given their color (size [num_dets, h, w, 1])
        colors = torch.cat([get_color(j, on_gpu=frame_gpu.device.index).view(
            1, 1, 1, 3) for j in range(num_dets)], dim=0)
        masks_color = pred_masks.repeat(1, 1, 1, 3) * colors * mask_alpha
        # This is 1 everywhere except for 1-mask_alpha where the mask is
        inv_alph_masks = pred_masks * (-mask_alpha) + 1
        np_mask = -inv_alph_masks[:,:,:,0].byte().cpu().numpy()

        for j in range(num_dets):
            frame_gpu = frame_gpu * inv_alph_masks[j] + masks_color[j]

        frame_numpy = (frame_gpu * 255).byte().cpu().numpy()
        save_list_add = np.array([])
        for j in range(num_dets):
            color = get_color(j)
            masks_color_np = pred_masks[j].cpu().squeeze().numpy().astype(np.uint8)
            contours, hierarchy = cv2.findContours(masks_color_np, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame_numpy,contours,-1,(255,255,255),1)
  
            if draw_point:
                count_zero = np.count_nonzero(np_mask[j] == 0)
                avg_x = round(np.mean(np.where(np_mask[j] == 0)[1]))
                avg_y = round(np.mean(np.where(np_mask[j] == 0)[0]))
                cv2.circle(frame_numpy, (avg_x,avg_y), 5, (0,255, 0), -1, cv2.LINE_AA)

                text_str = 'order:%s d:%.2fm %d x:%d y:%d' % (j, pred_depth.cpu().numpy()[avg_y, avg_x],count_zero,avg_x ,avg_y )
                text_str_pix = 'pix:%d'%(count_zero)
                # print('result%d'%(j),text_str)

                font_face = cv2.FONT_HERSHEY_DUPLEX
                font_scale = 0.6
                font_thickness = 1

                text_w, text_h = cv2.getTextSize(text_str_pix, font_face, font_scale, font_thickness)[0]
                text_pt = (avg_x, avg_y + text_h + 1)
                text_color = [255, 255, 255]
                cv2.rectangle(frame_numpy, (avg_x, avg_y),(avg_x + text_w, avg_y + text_h*5 + 4), color, -1)
                cv2.putText(frame_numpy, 'ord:%s'%(j), (avg_x, avg_y + 1*text_h + 1), font_face,font_scale, text_color, font_thickness, cv2.LINE_AA)
                cv2.putText(frame_numpy, 'dis:%.2fm'%(pred_depth.cpu().numpy()[avg_y, avg_x]), (avg_x, avg_y + 2*text_h + 1), font_face,font_scale, text_color, font_thickness, cv2.LINE_AA)
                cv2.putText(frame_numpy, 'pix:%d'%(count_zero), (avg_x, avg_y + 3*text_h + 1), font_face,font_scale, text_color, font_thickness, cv2.LINE_AA)
                cv2.putText(frame_numpy, 'x_m:%d'%(avg_x), (avg_x, avg_y + 4*text_h + 1), font_face,font_scale, text_color, font_thickness, cv2.LINE_AA)
                cv2.putText(frame_numpy, 'y_m:%d'%(avg_y), (avg_x, avg_y + 5*text_h + 1), font_face,font_scale, text_color, font_thickness, cv2.LINE_AA)

                save_list = np.array([round(avg_x/int(frame_numpy.shape[1]),3) ,round(avg_y/int(frame_numpy.shape[0]),3), round(pred_depth.cpu().numpy()[avg_y, avg_x],3)])
                save_list_add = np.append(save_list_add,save_list)

        if not no_text or not no_box:
            for j in reversed(range(num_dets)):
                x1, y1, x2, y2 = pred_boxes[j].int().cpu().numpy()
                color = get_color(j)
                score = pred_scores[j].detach().cpu().numpy()

                if not no_box:
                    cv2.rectangle(frame_numpy, (x1, y1), (x2, y2), color, 1)
                
                if not no_text:
                    _class = cfg.dataset.class_names[pred_classes[j].cpu().numpy()]
                    text_str = '%s: %.2f' % (_class, score)

                    font_face = cv2.FONT_HERSHEY_DUPLEX
                    font_scale = 0.6
                    font_thickness = 1

                    text_w, text_h = cv2.getTextSize(text_str, font_face, font_scale, font_thickness)[0]
                    text_pt = (x1, y1 + text_h + 1)
                    text_color = [255, 255, 255]

                    cv2.rectangle(frame_numpy, (x1, y1),(x1 + text_w, y1 + text_h + 4), color, -1)
                    cv2.putText(frame_numpy, text_str, text_pt, font_face,font_scale, text_color, font_thickness, cv2.LINE_AA)
        if not no_text:
            score = pred_scores[j].detach().cpu().numpy()
            _class = cfg.dataset.class_names[pred_classes[j].cpu().numpy()]
            text_str = '%s: %.2f' % (_class, score)

            font_face = cv2.FONT_HERSHEY_DUPLEX
            font_scale = 0.6
            font_thickness = 1

            text_w, text_h = cv2.getTextSize(
                text_str, font_face, font_scale, font_thickness)[0]
            text_pt = (x1, y1 + text_h + 1)
            text_color = [255, 255, 255]

            cv2.rectangle(frame_numpy, (x1, y1),
                        (x1 + text_w, y1 + text_h + 4), color, -1)
            cv2.putText(frame_numpy, text_str, text_pt, font_face,
                        font_scale, text_color, font_thickness, cv2.LINE_AA)
                
        return frame_numpy, pred_depth.cpu().numpy(),save_list_add
        # return frame_numpy, pred_depth.cpu().numpy()
    else:
        save_list_add=[]
        return frame.byte().cpu().numpy(), pred_depth.cpu().numpy(), save_list_add
        # return frame.byte().cpu().numpy(), pred_depth.cpu().numpy()


def inference_image(net: PlaneRecNet, path: str, output_type: int):
    frame_np = cv2.imread(str(path))
    H, W, _ = frame_np.shape

    if frame_np is None:
        return
    frame_np = cv2.resize(frame_np, calc_size_preserve_ar(W, H, cfg.max_size), interpolation=cv2.INTER_LINEAR)
    frame_np = pad_even_divided(frame_np) #pad image to be evenly divided by 32

    frame = torch.from_numpy(frame_np).cuda().float()
    batch = FastBaseTransform()(frame.unsqueeze(0))
    results = net(batch)

    blended_frame, depth,save_list_add = display_on_frame(results[0], frame, no_mask=args.no_mask, no_box=args.no_box, no_text=args.no_text)

    
    name, ext = os.path.splitext(path)
    save_path = name + '_seg' + ext
    depth_path1 = name + '_dep1.png'
    depth_path2 = name + '_dep2.png'

    # 절대 값을 기준으로 시각화(0~5m)
    depth_copy1 = depth
    vmin = 0
    vmax = 10
    depth_copy1 = depth_copy1.clip(min=vmin, max=vmax)
    depth_copy1 = ((depth_copy1 - vmin) / (vmax - vmin) * 255).astype(np.uint8)
    depth_color1 = cv2.applyColorMap(depth_copy1, cv2.COLORMAP_PLASMA)
    cv2.putText(depth_color1,str(round(depth[240,320],2)),(320,240),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA)
    cv2.circle(depth_color1,(320,240), 5, (0,255,0), -1)
    
    # 획득 데이터 기준 시각화
    depth_copy2 = depth
    vmin = np.percentile(depth_copy2, 1)
    vmax = np.percentile(depth_copy2, 99) 
    depth_copy2 = depth_copy2.clip(min=vmin, max=vmax)
    depth_copy2 = ((depth_copy2 - depth.min()) / (depth.max() - depth.min()) * 255).astype(np.uint8)
    depth_color2 = cv2.applyColorMap(depth_copy2, cv2.COLORMAP_PLASMA)
    cv2.putText(depth_color2,str(round(depth[240,320],2)),(320,240),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA)
    cv2.circle(depth_color2,(320,240), 5, (0,255,0), -1)
    
    cv2.imwrite(save_path, blended_frame)
    cv2.imwrite(depth_path1, depth_color1)
    cv2.imwrite(depth_path2, depth_color2)
    
    return save_path, depth_path1, depth_path2, save_list_add
    
    if output_type == 0:
        cv2.imwrite(save_path, blended_frame)
        return save_path, save_list_add
    elif output_type == 1:
        cv2.imwrite(depth_path1, depth_color1)
        return depth_path1, save_list_add
    elif output_type == 2:
        cv2.imwrite(depth_path2, depth_color2)
        return depth_path2, save_list_add

def main(input_path : str, output_type = 0):
    # model 가져오기
    model_download.get_model_planerecnet()
    timer.disable_all()
    new_nms_config = {
        'nms_type': "mask", 
        'mask_thr': 0.5, 
        'update_thr': 0.5,
        'top_k': 5,
        }

    custom_args()
    set_cfg(args.config)
    cfg.solov2.replace(new_nms_config)

    net = PlaneRecNet(cfg)
    net.load_weights(args.trained_model)
    net.train(mode=False)
    net = net.cuda()
    torch.set_default_tensor_type("torch.cuda.FloatTensor")

    save_path, depth_path1, depth_path2, save_list_add = inference_image(net, path = input_path, output_type=output_type)

    return save_path, depth_path1, depth_path2, save_list_add