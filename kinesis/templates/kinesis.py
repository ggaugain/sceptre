# This is an example of a Kinesis Stream

from troposphere import Join, Ref, Template, GetAtt, Output
from troposphere.kinesis import Stream, StreamEncryption

class KinesisStream():
    def __init__(self, sceptre_user_data):
        self.sceptre_user_data = sceptre_user_data
        self.template = Template()
        self.add_stream()
        self.add_outputs()

    def add_stream(self):
        if "StreamEncryption" in self.sceptre_user_data:
            self.sceptre_user_data.update({
                "StreamEncryption": StreamEncryption(
                    **self.sceptre_user_data.get(
                        "StreamEncryption"
                    )
                )
            })
        self.kinesis = self.template.add_resource(Stream(
            "Name",
            **self.sceptre_user_data
        ))

    def add_outputs(self):
        self.out = self.template.add_output([
            Output("Ref", Value=Ref(self.kinesis)),
            Output("Arn", Value=GetAtt(self.kinesis, "Arn")),
        ])

def sceptre_handler(sceptre_user_data):
    return KinesisStream(sceptre_user_data).template.to_yaml()
