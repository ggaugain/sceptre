from troposphere import Join, Ref, Template, GetAtt, Output
from troposphere.ec2 import SecurityGroup, SecurityGroupIngress, SecurityGroupRule

class EC2SecurityGroup():
    def __init__(self, sceptre_user_data):
        self.sceptre_user_data = sceptre_user_data
        self.template = Template()
        self.add_WebSecurityGroup()
        self.add_outputs()

    def add_WebSecurityGroup(self):
        self.WebSecurityGroup = self.template.add_resource(SecurityGroup(
            "WebSecurityGroup",
            SecurityGroupIngress=[
                {"ToPort": "80", "IpProtocol": "tcp",
                    "CidrIp": "0.0.0.0/0", "FromPort": "80"},
            ],
            VpcId=self.sceptre_user_data.get("VpcId"),
            GroupDescription="WEBsg",
        ))

    def add_outputs(self):
        self.out = self.template.add_output([
            Output("Ref", Value=Ref(self.WebSecurityGroup)),
            Output("GroupId", Value=GetAtt(self.WebSecurityGroup, "GroupId")),
        ])

def sceptre_handler(sceptre_user_data):
    return EC2SecurityGroup(sceptre_user_data).template.to_yaml()
