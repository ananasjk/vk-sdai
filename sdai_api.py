import requests
import requests as req1
import base64
import vk_api
import io
import time
from PIL import Image, PngImagePlugin
from uuid import uuid4
from vk_api.utils import get_random_id
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll
import configparser
import urllib.request

config = configparser.ConfigParser()
config.read("config.ini")
tok123 = str(config.get("Settings", "token"))
group_id = config.get('Settings', 'group_id')

vk_session = vk_api.VkApi(token=tok123)

vk_upload = VkUpload(vk_session)
longpoll = VkBotLongPoll(vk_session, group_id)
upload = VkUpload(vk_session)
vk = vk_session.get_api()


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


def vkmsg(text, peer_id: int):
    vk.messages.send(
        user_id=peer_id,
        random_id=get_random_id(),
        message=text,
    )


def generate_filename():
    return f"output_images/{uuid4()}.png"


def generate_image(steps, cfg_scale, img_w, img_h: int, prompt: str, batch_size, hires: int, neg_prompt:str):
    payload = {

        "enable_hr": hires,
        "hr_scale": "2",
        "hr_upscaler": "Latent",
        "hr_second_pass_steps": "0",
        "denoising_strength": "0.7",

        "prompt": prompt,
        "seed": "-1",
        "batch_size": batch_size,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "width": img_w,
        "height": img_h,

        "negative_prompt": neg_prompt,
        "send_images": "true",
        "save_images": "false",

        "do_not_save_grid": "true"
    }

    response = requests.post(url="http://localhost:7861/sdapi/v1/txt2img", json=payload).json()

    generated_files = []

    for i in response['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }

        response2 = requests.post(url='http://localhost:7861/sdapi/v1/png-info', json=png_payload).json()

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2['info'])

        file_name = generate_filename()
        image.save(file_name, pnginfo=pnginfo)
        generated_files.append(file_name)
    return (generated_files)


def send_image(samples, cfg_scale, i_w, i_h: int, prompt: str, batch, hires: int, message_id1: int, peer_id, neg_prompt:str):
    start_time = time.time()
    images = generate_image(samples, cfg_scale, i_w, i_h, prompt, batch, hires, neg_prompt)
    attachments = []

    for i in range(int(batch)):
        photo = upload.photo_messages(photos=images[i])[0]
        attachments.append(
            'photo{}_{}'.format(photo['owner_id'], photo['id'])
        )

    end_time = time.time()
    mess = 'Elapsed time: ' + str(toFixed(end_time - start_time, 2)) + ' seconds.'
    vk.messages.edit(
        peer_id=peer_id,
        message_id=message_id1 + 1,
        user_id=peer_id,
        random_id=get_random_id(),
        message=mess,
        attachment=','.join(attachments),

    )


def prog():
    response = req1.get(url="http://127.0.0.1:7861/sdapi/v1/progress?skip_current_image=false").json()
    for key, value in response.items():
        if key == 'progress':
            progress = float(str(value)[:4])
            return progress


def get_prog(msg_id1: int, peer_id1: int):
    time.sleep(3)
    prog1 = prog()
    while prog1 != 0:
        vk.messages.edit(
            peer_id=peer_id1,
            message_id=msg_id1 + 1,
            user_id=peer_id1,
            random_id=get_random_id(),
            message='Generating! ' + str(prog1 * 100) + '%',
        )
        time.sleep(3)
        prog1 = prog()

    vk.messages.edit(
        peer_id=peer_id1,
        message_id=msg_id1 + 1,
        user_id=peer_id1,
        random_id=get_random_id(),
        message='Done! Uploading...',
    )


def get_model_list():
    requests.post(url='http://127.0.0.1:7861/sdapi/v1/refresh-checkpoints')
    response = requests.get(url="http://127.0.0.1:7861/sdapi/v1/sd-models").json()

    models = ''
    for i in range(len(response)):
        models = models + response[i]["model_name"] + '\n'

    return models


def model(modelname: str):
    opt = requests.get(url='http://127.0.0.1:7861/sdapi/v1/options').json()
    print(opt["sd_model_checkpoint"])
    opt["sd_model_checkpoint"] = modelname
    requests.post(url='http://127.0.0.1:7861/sdapi/v1/options', json=opt)


def get_model():
    model1 = requests.get(url='http://127.0.0.1:7861/sdapi/v1/options').json()['sd_model_checkpoint']
    return model1


def download_model(url, path: str, peer_id: int):
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, path)
    except (ContentTooShortError):
        vkmsg('Failed! Try to restart the download', peer_id)
        pass


def get_lora():
    requests.post(url='http://127.0.0.1:7861/sdapi/v1/refresh-loras')
    response = requests.get(url="http://127.0.0.1:7861/sdapi/v1/loras").json()
    lora = ''
    for i in range(len(response)):
        lora = lora + response[i]["name"] + '\n'
    return lora

def interrupt():
    requests.post(url='http://127.0.0.1:7861/sdapi/v1/interrupt')