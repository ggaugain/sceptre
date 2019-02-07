from troposphere import Join, Ref, Template, GetAtt, Output
from troposphere.ec2 import SecurityGroup, SecurityGroupIngress, SecurityGroupRule

class SceptreRessource():
    def __init__(self, sceptre_user_data):
        self.sceptre_user_data = sceptre_user_data
        self.template = Template()
        self.add_resource()
        self.add_outputs()

    def add_resource(self):
        self.SecurityGroup = self.template.add_resource(SecurityGroup(
            "SecurityGroup",
            **self.sceptre_user_data
        ))

    def add_outputs(self):
        self.out = self.template.add_output([
            Output("SecurityGroup", Value=Ref(self.SecurityGroup)),
        ])

def sceptre_handler(sceptre_user_data):
    return SceptreRessource(sceptre_user_data).template.to_yaml()
