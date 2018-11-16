from troposphere import Join, Ref, Template, GetAtt, Output
from troposphere.awslambda import Function, Code

class LambdaFunction():
    def __init__(self, sceptre_user_data):
        self.sceptre_user_data = sceptre_user_data
        self.template = Template()
        self.add_function()
        self.add_outputs()

    def add_function(self):
        if "Code" in self.sceptre_user_data:
            self.sceptre_user_data.update({
                "Code": Code(
                    **self.sceptre_user_data.get(
                        "Code"
                    )
                )
            })
        self.Function = self.template.add_resource(Function(
            "LambdaFunction",
                **self.sceptre_user_data
        ))

    def add_outputs(self):
        self.out = self.template.add_output([
            Output("Ref", Value=Ref(self.Function)),
            Output("Arn", Value=GetAtt(self.Function, "Arn")),
        ])

def sceptre_handler(sceptre_user_data):
    return LambdaFunction(sceptre_user_data).template.to_yaml()
