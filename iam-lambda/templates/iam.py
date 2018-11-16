from troposphere import Join, Ref, Template, GetAtt, Output
from troposphere.iam import Role

class IamRole():
    def __init__(self, sceptre_user_data):
        self.sceptre_user_data = sceptre_user_data
        self.template = Template()
        self.add_role()
        self.add_outputs()

    def add_role(self):
        self.IamRole = self.template.add_resource(Role(
            "Role",
            **self.sceptre_user_data
        ))

    def add_outputs(self):
        self.out = self.template.add_output([
            Output("Ref", Value=Ref(self.IamRole)),
            Output("Arn", Value=GetAtt(self.IamRole, "Arn")),
            Output("RoleId", Value=GetAtt(self.IamRole, "RoleId")),
        ])

def sceptre_handler(sceptre_user_data):
    return IamRole(sceptre_user_data).template.to_yaml()
