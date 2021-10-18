from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result
from tracardi_smtp_connector.model.smtp import Configuration, Smtp
from tracardi_smtp_connector.service.sendman import PostMan
from tracardi.service.storage.driver import storage
from tracardi.domain.resource import Resource
from tracardi_dot_notation.dot_accessor import DotAccessor
from tracardi_dot_notation.dot_template import DotTemplate


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
            dot = DotAccessor(self.profile, self.session, payload, self.event, self.flow)
            template = DotTemplate()
            self.post.send(template.render(self.config.message, dot))
            return Result(port='payload', value={"result": True})
        except Exception as e:
            self.console.warning(repr(e))
            return Result(port='payload', value={"result": False})


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
            manual="smtp_connector_action",
            version='0.1.3',
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
