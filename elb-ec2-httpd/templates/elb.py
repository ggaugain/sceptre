from troposphere import Join, Ref, Template, GetAtt, Output, Tags
import troposphere.elasticloadbalancing as elb

class SceptreRessource():
    def __init__(self, sceptre_user_data):
        self.sceptre_user_data = sceptre_user_data
        self.template = Template()
        self.add_resource()
        self.add_outputs()

    def add_resource(self):
        self.ElasticLoadBalancer = self.template.add_resource(elb.LoadBalancer(
            "ElbWeb",
            **self.sceptre_user_data
        ))

    def add_outputs(self):
        self.out = self.template.add_output([
            Output("ElbWeb", Value=Ref(self.ElasticLoadBalancer)),
        ])

def sceptre_handler(sceptre_user_data):
    return SceptreRessource(sceptre_user_data).template.to_yaml()
