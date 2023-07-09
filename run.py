import sdai_api
import os
import threading
import vk_api
import configparser
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import time

config = configparser.ConfigParser()
config.read("config.ini")

user_helpmsg = '''
"/lora" to get all LORAS downloaded. Loras are imported as <lora:NAME:1.0>
"/lyco" to get all LyCORIS (LoCon/LoHA) models. LyCORIS models are imported as <lyco:NAME:1.0>

To generate a picture just type in the prompt
'''

helpmsg = '''
"/lora" to get all LORAS downloaded. Loras are imported as <lora:NAME:1.0>
"/lyco" to get all LyCORIS (LoCon/LoHA) models. LyCORIS models are imported as <lyco:NAME:1.0>

To generate a picture just type in the prompt

Admin settings:
"/samples 30" to change sample count
"/iw 512" to change image width
"/ih 512" to change image height
"/batch 1" to change batch size
"/cfg 7" to change cfg scale
"/hires true/false" to enable/disable hires fix
"/negative" to display current negative prompt
"/negative prompt" to change negative prompt

"/settings" to see current settings
"/interrupt" to stop current image generation

Owner settings:
"/addadmin ananasjkk" to add admins
"/deleteadmin ananasjkk" to remove admins

"/downloadlora URL LoraName" to download LORA
"/downloadlyco URL LycoName" to download LyCORIS (LoCon/LoHA)
"/download URL ModelName" to download the model
Models can be downloaded from civitai.com or huggingface

"/modellist" to see list of all models downloaded
"/model" to see current model
"/model ModelName" to change current checkpoint
"/idcheck True/False" to enable or disable id checking
"/exit" to close vk-sdai
"/shutdown" to shutdown the server

'''

samples = config.get("Settings", "samples")
cfg_scale = config.get("Settings", "cfg_scale")
i_w = config.get("Settings", "i_w")
i_h = config.get("Settings", "i_h")
batch = config.get("Settings", "batch")
tok123 = config.get("Settings", "token")
group_id = config.get('Settings', 'group_id')
path = config.get('Settings', 'path')
hires = config.get('Settings', 'hires')
enable_id_check = config.get('Settings', 'id_check')
Negative_prompt = config.get('Settings', 'neg_prompt')
prompt = ''
lastprompt = ''

MyID = config.get('Admin_IDS', 'owner_id')
adm_str = str(config.get('Admin_IDS', 'adm_ids')).split(sep=', ')
adm_ids = [int(i) for i in adm_str]

start11 = '''
db    db db   dD        .d8888. d8888b.  .d8b.  d888888b 
88    88 88 ,8P'        88'  YP 88  `8D d8' `8b   `88'   
Y8    8P 88,8P          `8bo.   88   88 88ooo88    88    
`8b  d8' 88`8b   C8888D   `Y8b. 88   88 88~~~88    88    
 `8bd8'  88 `88.        db   8D 88  .8D 88   88   .88.   
   YP    YP   YD        `8888Y' Y8888D' YP   YP Y888888P 
'''

cls = lambda: os.system('cls')
cls()

print(start11)
print()
print('Started!')
# print(adm_ids)

vk_session = vk_api.VkApi(token=str(tok123))

vk_upload = VkUpload(vk_session)
longpoll = VkBotLongPoll(vk_session, group_id)
upload = VkUpload(vk_session)
vk = vk_session.get_api()

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.message.peer_id == int(MyID) or enable_id_check == 'False' or event.message.peer_id in adm_ids:
            if str(event.message.text)[:1] == '/':
                txt = str(event.message.text)[1:]
                words = txt.split()
                if len(words) != 0:
                    if event.message.peer_id == int(MyID):
                        match words[0]:
                            # closes vk-sdai executable
                            case 'exit':
                                sdai_api.vkmsg('Exiting...', event.message.peer_id)
                                sdai_api.interrupt()
                                print('User prompted to exit! Exiting...  Dont forget to close StableDiffusion!')
                                break

                            # shuts down the pc
                            case 'shutdown':
                                os.system("shutdown /s /t 1")

                            # enable or disable id checking
                            case 'idcheck':
                                config.set('Settings', 'id_check', words[1])
                                enable_id_check = words[1]
                                sdai_api.vkmsg('Changed id checking to ' + words[1], event.message.peer_id)

                            # download models, loras or lycoris models respectively
                            case 'download':
                                print('downloading model ' + words[2] + ' from ' + words[1])
                                sdai_api.download_model(words[1], str(path + "models\\Stable-diffusion\\" + words[
                                    2] + '.safetensors'), event.message.peer_id)
                                sdai_api.vkmsg('Downloaded model ' + words[2] + '.safetensors ' + 'from ' + words[1],
                                               event.message.peer_id)

                            case 'downloadlora':
                                print('downloading model ' + words[2] + ' from ' + words[1])
                                sdai_api.download_model(words[1],
                                                        str(path + "models\\Lora\\" + words[2] + '.safetensors'),
                                                        event.message.peer_id)
                                sdai_api.vkmsg('Downloaded model ' + words[2] + '.safetensors ' + 'from ' + words[1],
                                               event.message.peer_id)

                            case 'downloadlyco':
                                print('downloading model ' + words[2] + ' from ' + words[1])
                                sdai_api.download_model(words[1],
                                                        str(path + "models\\LyCORIS\\" + words[2] + '.safetensors'),
                                                        event.message.peer_id)
                                sdai_api.vkmsg('Downloaded model ' + words[2] + '.safetensors ' + 'from ' + words[1],
                                               event.message.peer_id)

                            # model changing and displaying
                            case 'model':
                                if len(words) == 1:
                                    sdai_api.vkmsg(sdai_api.get_model(), event.message.peer_id)
                                else:
                                    print('changing model to ', words[1])
                                    sdai_api.model(words[1])
                                    time.sleep(10)
                                    sdai_api.vkmsg('changed model to ' + sdai_api.get_model(), event.message.peer_id)
                            case 'modellist':
                                sdai_api.vkmsg(sdai_api.get_model_list(), event.message.peer_id)

                            # add admins
                            case 'addadmin':
                                new_adm_id = int(vk.utils.resolveScreenName(screen_name=words[1])['object_id'])
                                adm_ids.append(new_adm_id)
                                config.set('Admin_IDS', 'adm_ids', str(adm_ids)[1:-1])
                                sdai_api.vkmsg(f'Added @id{new_adm_id} as an Admin', event.message.peer_id)
                                print(f'added @id{new_adm_id} as admin')

                            case 'deleteadmin':
                                new_adm_id = int(vk.utils.resolveScreenName(screen_name=words[1])['object_id'])
                                adm_ids.remove(new_adm_id)
                                config.set('Admin_IDS', 'adm_ids', str(adm_ids)[1:-1])
                                sdai_api.vkmsg(f'Removed @id{new_adm_id} as an Admin', event.message.peer_id)
                                print(f'removed @id{new_adm_id} as admin')

                            case 'interrupt':
                                sdai_api.vkmsg('Interrupting current generation...', event.message.peer_id)
                                sdai_api.interrupt()

                                # allows to change generation settings
                            case 'samples':
                                print('changing samples to', words[1])
                                config.set('Settings', 'samples', words[1])
                                samples = words[1]
                                sdai_api.vkmsg('Changed samples to ' + words[1], event.message.peer_id)
                            case 'iw':
                                print('changing image width to', words[1])
                                config.set('Settings', 'i_w', words[1])
                                i_w = words[1]
                                sdai_api.vkmsg('Changed Image Width to ' + words[1], event.message.peer_id)
                            case 'ih':
                                print('changing image height to', words[1])
                                config.set('Settings', 'i_h', words[1])
                                i_h = words[1]
                                sdai_api.vkmsg('Changed Image Height to ' + words[1], event.message.peer_id)
                            case 'batch':
                                print('changing batch to', words[1])
                                config.set('Settings', 'batch', words[1])
                                batch = words[1]
                                sdai_api.vkmsg('Changed batch size to ' + words[1], event.message.peer_id)
                            case 'hires':
                                print('changing hires to', words[1])
                                config.set('Settings', 'hires', words[1])
                                hires = words[1]
                                sdai_api.vkmsg('Changed hires fix to ' + words[1], event.message.peer_id)
                            case 'negative':
                                if len(words) == 1:
                                    print('current negative: ', Negative_prompt)
                                    sdai_api.vkmsg('Current negative:', event.message.peer_id)
                                    sdai_api.vkmsg(Negative_prompt, event.message.peer_id)
                                else:
                                    Negative_prompt = ''
                                    for i in range(1, len(words)):
                                        Negative_prompt = Negative_prompt + words[i] + ' '
                                    print('changing negative prompt to: ' + Negative_prompt)
                                    config.set('Settings', 'neg_prompt', Negative_prompt)
                                    sdai_api.vkmsg('New negative:', event.message.peer_id)
                                    sdai_api.vkmsg(Negative_prompt, event.message.peer_id)
                            case 'cfg':
                                print('changing cfg scale to', words[1])
                                config.set('Settings', 'cfg_scale', words[1])
                                cfg_scale = words[1]
                                sdai_api.vkmsg('Changed cfg_scale to ' + words[1], event.message.peer_id)

                                # displays current settings
                            case 'settings':
                                sdai_api.vkmsg(
                                    f'Samples: {str(samples)} \n Image dimensions: {str(i_w)} x {str(i_h)} \n Cfg scale: {str(cfg_scale)} \n Batch size: {str(batch)} \n HiRes_Fix: {str(hires)} \n ID Checking: {str(enable_id_check)} \n Current model: {sdai_api.get_model()}',
                                    event.message.peer_id)

                                # displays lora, lycos downloaded
                            case 'lora':
                                loras = sdai_api.get_lora()
                                sdai_api.vkmsg(loras, event.message.peer_id)
                            case 'lyco':
                                lyco = os.listdir(path + 'models\\LyCORIS')
                                lyco_str = ''
                                for i in range(len(lyco)):
                                    lyco_str = lyco_str + str(lyco[i])[: -12] + '\n'
                                sdai_api.vkmsg(lyco_str, event.message.peer_id)

                            case 'help':
                                sdai_api.vkmsg(helpmsg, event.message.peer_id)

                            # unknown message handling
                            case _:
                                sdai_api.vkmsg('Setting is not available', event.message.peer_id)

                    elif event.message.peer_id in adm_ids:
                        match words[0]:

                            # interrupts current image generation
                            case 'interrupt':
                                sdai_api.vkmsg('Interrupting current generation...', event.message.peer_id)
                                sdai_api.interrupt()

                            # allows to change generation settings
                            case 'samples':
                                print('changing samples to', words[1])
                                config.set('Settings', 'samples', words[1])
                                samples = words[1]
                                sdai_api.vkmsg('Changed samples to ' + words[1], event.message.peer_id)
                            case 'iw':
                                print('changing image width to', words[1])
                                config.set('Settings', 'i_w', words[1])
                                i_w = words[1]
                                sdai_api.vkmsg('Changed Image Width to ' + words[1], event.message.peer_id)
                            case 'ih':
                                print('changing image height to', words[1])
                                config.set('Settings', 'i_h', words[1])
                                i_h = words[1]
                                sdai_api.vkmsg('Changed Image Height to ' + words[1], event.message.peer_id)
                            case 'batch':
                                print('changing batch to', words[1])
                                config.set('Settings', 'batch', words[1])
                                batch = words[1]
                                sdai_api.vkmsg('Changed batch size to ' + words[1], event.message.peer_id)
                            case 'hires':
                                print('changing hires to', words[1])
                                config.set('Settings', 'hires', words[1])
                                hires = words[1]
                                sdai_api.vkmsg('Changed hires fix to ' + words[1], event.message.peer_id)
                            case 'negative':
                                if len(words) == 1:
                                    print('current negative: ', Negative_prompt)
                                    sdai_api.vkmsg('Current negative:', event.message.peer_id)
                                    sdai_api.vkmsg(Negative_prompt, event.message.peer_id)
                                else:
                                    Negative_prompt = ''
                                    for i in range(1, len(words)):
                                        Negative_prompt = Negative_prompt + words[i] + ' '
                                    print('changing negative prompt to: ' + Negative_prompt)
                                    config.set('Settings', 'neg_prompt', Negative_prompt)
                                    sdai_api.vkmsg('New negative:', event.message.peer_id)
                                    sdai_api.vkmsg(Negative_prompt, event.message.peer_id)
                            case 'cfg':
                                print('changing cfg scale to', words[1])
                                config.set('Settings', 'cfg_scale', words[1])
                                cfg_scale = words[1]
                                sdai_api.vkmsg('Changed cfg_scale to ' + words[1], event.message.peer_id)

                            # displays current settings
                            case 'settings':
                                sdai_api.vkmsg(
                                    f'Samples: {str(samples)} \n Image dimensions: {str(i_w)} x {str(i_h)} \n Cfg scale: {str(cfg_scale)} \n Batch size: {str(batch)} \n HiRes_Fix: {str(hires)} \n ID Checking: {str(enable_id_check)} \n Current model: {sdai_api.get_model()}',
                                    event.message.peer_id)

                            # displays lora, lycos downloaded
                            case 'lora':
                                loras = sdai_api.get_lora()
                                sdai_api.vkmsg(loras, event.message.peer_id)
                            case 'lyco':
                                lyco = os.listdir(path + 'models\\LyCORIS')
                                lyco_str = ''
                                for i in range(len(lyco)):
                                    lyco_str = lyco_str + str(lyco[i])[: -12] + '\n'
                                sdai_api.vkmsg(lyco_str, event.message.peer_id)

                            case 'help':
                                sdai_api.vkmsg(helpmsg, event.message.peer_id)

                            case _:
                                sdai_api.vkmsg('Setting is not available or you are not privileged enough',
                                               event.message.peer_id)
                    else:
                        match words[0]:
                            case 'help':
                                sdai_api.vkmsg(user_helpmsg, event.message.peer_id)
                            case 'lora':
                                loras = sdai_api.get_lora()
                                sdai_api.vkmsg(loras, event.message.peer_id)
                            case 'lyco':
                                lyco = os.listdir(path + 'models\\LyCORIS')
                                lyco_str = ''
                                for i in range(len(lyco)):
                                    lyco_str = lyco_str + str(lyco[i])[: -12] + '\n'
                                sdai_api.vkmsg(lyco_str, event.message.peer_id)
                            case _:
                                sdai_api.vkmsg('Setting is not available or you are not privileged enough',
                                               event.message.peer_id)
                    with open("config.ini", "w") as config_file:
                        config.write(config_file)
            else:
                if event.message.text == 'repeat':
                    prompt = lastprompt
                else:
                    prompt = event.message.text
                lastprompt = prompt
                message_id1 = int(event.message.id)
                sdai_api.vkmsg('Generating! Please wait...', event.message.peer_id)
                print(prompt + '\n')
                thread1 = threading.Thread(target=sdai_api.get_prog,
                                           args=(int(message_id1), int(event.message.peer_id)))

                thread2 = threading.Thread(target=sdai_api.send_image,
                                        args=(
                                            samples, cfg_scale, i_w, i_h, str(prompt), batch, hires,
                                            message_id1,
                                            int(event.message.peer_id), str(Negative_prompt)))
                #thread1.start()
                thread2.start()
                lastprompt = prompt