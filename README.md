
# Vk-SDAI

Бот на vk-longpoll для Automatic1111 Stable diffusion




## Преимущества

- Скачивание и смена моделей stable diffusion на лету
- Скачивание и использование моделей lora и lyCORIS
- Изменение и сохранение настроек прямо через бота
- Сохранение настроек в конфиг файл
- Включаемая проверка по айди пользователя
- Разделение на владельца и админов:

    - Владелец может добавлять админов, скачивать модели, менять модели на лету, выключать бота и/или сервер
    - Админы могут менять настройки генерации, прерывать текущую генерацию изображения

    - Пользователи при выключенной проверке по айди могут запрашивать список скаченных моделей lora и lycoRis и генерировать изображения

- Повторение прошлой генерации одной коммандой

Комманды бота:
```
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
```


## Установка


```bash
  git clone https://github.com/ananasjk/vk-sdai
  cd vk-sdai
  pip install -r requirements.txt
```

## Настройка config.ini

owner_id = 123456789 - айди владельца бота

admin_ids = 123456789, 234567890 - айди админов, через запятую

token - токен группы

Для получения токена группы:

Настройки группы -> Работа с API -> Создать ключ

Права доступа ключа - сообщения сообщества, фотографии, документы, управление сообществом

Также необходимо включить longpoll в соседней вкладке и дать ему права доступа к сообщениям 

path - путь до директории stable-diffusion-webui, обязательно с / в конце


    
## Запуск

```python
python run.py
```

Или launch.bat

В параметрах запуска stable diffusion (launcher.bat по умолчанию) добавить пункты --api и --port 7861

Рекомендую создать файл запуска прямо в директории vk-sdai, вида:

```bash
@echo off

set PYTHON=
set GIT=
set VENV_DIR=
set COMMANDLINE_ARGS= --xformers --listen --port 7861 --api


cd "...\stable-diffusion-webui"
call webui.bat

```

где ... это путь до вашей директории stable-diffusion-webui

/help в лс с ботом группы выдаёт все доступные команды
