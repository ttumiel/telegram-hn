import json, logging, os, telepot

from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from .utils import *


TOKEN = os.environ["BOT_TOKEN"]
TelegramBot = telepot.Bot(TOKEN)
logger = logging.getLogger('telegram.bot')


def _display_help():
    return render_to_string('telegram/help.md')


def _display_hn(option="top", number=5):
    return render_to_string('telegram/feed.md', {'latest': parse_hn(option, number)})


class CommandReceiveView(View):
    def post(self, request, bot_token):

        if bot_token != TOKEN:
            return HttpResponseForbidden('Invalid token')

        commands = {
            '/start': _display_help,
            '/help': _display_help,
            'new': _display_hn,
            'top': _display_hn,
            'best': _display_hn,
            'show': _display_hn,
            'jobs': _display_hn,
            'ask': _display_hn,
        }

        raw = request.body.decode('utf-8')
        logger.info(raw)

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            chat_id = payload['message']['chat']['id']
            command = payload['message']['chat']['text'].split()
            func = commands.get(command[0].lower())
            if func:
                if len(command) > 1:
                    n_posts = check_string_num(command[1]) or 5
                if command[0][0] != "/":
                    TelegramBot.sendMessage(
                        chat_id, func(option=command[0], number=n_posts), parse_mode='Markdown')
                else:
                    TelegramBot.sendMessage(
                        chat_id, func(), parse_mode='Markdown')
            else:
                TelegramBot.sendMessage(
                    chat_id, _display_help(), parse_mode='Markdown')

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
