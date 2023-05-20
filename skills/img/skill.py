import logging
import discord as dislib
import io, base64
import requests
from PIL import Image, PngImagePlugin

class img():
    def __init__(self, config, events):
        self.logger = logging.getLogger('mogrilla')
        self.events = events
        self.config = config
        events.add_command('img', self.img)
        events.add_command('models', self.models)
        events.add_command('model', self.model)

    # Fetch models from SD-webui
    def fetch_models(self):
        models = {}
        resp = requests.get(url=f'{self.config["url"]}/sdapi/v1/sd-models')
        for model in resp.json():
            models[model['model_name']] = model['filename']
        return models

    # Load a specific model
    def model(self, data):

        # Prompt == model name
        prompt = data['message']
        if not prompt:
            return 'No model?'

        # Fetch models from SD-webui
        self.logger.info(f'(img) got request to switch to {prompt}')
        models = self.fetch_models()

        # Check if model exists
        if not prompt in models.keys():
            return f'Model {prompt} does not exist'

        # Switch model
        self.logger.info(f'(img) switching model to {prompt}')
        payload = {'sd_model_checkpoint': prompt}
        response = requests.post(url=f'{self.config["url"]}/sdapi/v1/options', json=payload, timeout=60)

        return f'Changed to {prompt}'

    # List all models
    def models(self, data):
        models = 'Models:\n'
        for model, file in self.fetch_models().items():
            models += f'  {model}\n'
        return models

    # Generate image
    def img(self, data):
        prompt = data['message']
        author = data['author']
        imgfile = io.BytesIO()
        self.logger.info(f'(img) got request from {author.mention} for image {prompt}')

        payload = {
            "prompt": prompt,
            "steps": self.config['steps'],
            "override_settings": {
                "filter_nsfw": true
            }
        }

        self.logger.info('(img) sending request')
        response = requests.post(url=f'{self.config["url"]}/sdapi/v1/txt2img', json=payload)

        img = response.json()['images'][0]
        self.logger.info(f'(img) got image')

        self.logger.info('(img) reading image')
        image = Image.open(io.BytesIO(base64.b64decode(img)))

        self.logger.info('(img) fetching png info')
        png_payload = {
            "image": "data:image/png;base64," + img
        }
        response2 = requests.post(url=f'{self.config["url"]}/sdapi/v1/png-info', json=png_payload)

        self.logger.info('(img) preparing png info')
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))

        self.logger.info('(img) writing tmp png')
        try:
            image.save(imgfile, pnginfo=pnginfo, format='PNG')
            imgfile.seek(0)
        except Exception as e:
            self.logger.error(e)

        self.logger.info('(img) attaching file')
        disimg = dislib.File(imgfile, filename="image.png")

        self.logger.info(f'(img) responsing with file {disimg}')
        msg = f'{author.mention} requested image with {prompt}'
        self.events.send_message(self.config['chan'], msg, file=disimg)
