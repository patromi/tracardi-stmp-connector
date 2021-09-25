from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result
from tracardi_smtp_connector.model.smtp import Configuration, Smtp
from tracardi_smtp_connector.service.sendman import PostMan
from tracardi.service.storage.driver import storage
from tracardi.domain.resource import Resource


class SmtpDispatcherAction(ActionRunner):

    @staticmethod
    async def build(**kwargs) -> 'SmtpDispatcherAction':
        config = Configuration(**kwargs)
        source = await storage.driver.resource.load(config.source.id)
        plugin = SmtpDispatcherAction(config, source)
        return plugin

    def __init__(self, config: Configuration, source: Resource):
        self.config = config
        self.post = PostMan(Smtp(**source.config))

    async def run(self, payload):
        try:
            self.post.send(self.config.message)
            return Result(port='payload', value=True)
        except Exception as e:
            self.console.warning(repr(e))
            return Result(port='payload', value=False)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_smtp_connector.plugin',
            className='SmtpDispatcherAction',
            inputs=["payload"],
            outputs=['payload'],
            init={
                "source": {
                    "id": None
                },
                'message': {
                    "send_to": None,
                    "send_from": None,
                    "reply_to": None,
                    "title": None,
                    "message": None
                }
            },
            version='0.1.1',
            license="MIT",
            author="iLLu"

        ),
        metadata=MetaData(
            name='Send mail',
            desc='Send mail via defined smtp server.',
            type='flowNode',
            width=200,
            height=100,
            icon='email',
            group=["Connectors"]
        )
    )
